import requests
from flask import Flask, request, jsonify, render_template
import torch
import pandas as pd
import os
import re
from pymongo import MongoClient  # For MongoDB connection and querying

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface import HuggingFacePipeline

app = Flask(__name__)

# === Configuration section ===
VECTOR_STORE_PATH = "vectorstore/db_faiss"
LOCAL_MODEL_NAME = "google/flan-t5-small"
JOBS_CSV_PATH = "data/ncs_jobs.csv"
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DBNAME = "SainikHire"
MONGODB_COLLECTION = "information"

#loading the api key
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Prompt template to guide the language model for ex-servicemen related queries
PROMPT_TEMPLATE = """
You are a highly knowledgeable, supportive, and extremely concise chatbot assistant for ex-servicemen and their families.
Based exclusively on the following context, provide direct, clear, and absolutely non-repetitive information.
*Your response must be unique and contain no redundant words, phrases, sentences, or ideas whatsoever.*
Focus on delivering complete answers without any duplication.

*Key Requirements for Your Answer:*
* **Absolute Non-Repetition:** Do NOT re-state, re-explain, or repeat any information already given in the answer. Rephrase entirely if a concept needs to be revisited, but ensure it's truly distinct.
* **Concise and Direct:** Provide information as directly as possible, avoiding unnecessary words or conversational filler.
* **Strictly Context-Bound:** Use ONLY the provided context. If the context lacks sufficient information, state: "I apologize, but I do not have enough specific information in my knowledge base to answer that question comprehensively." Do NOT invent or use external knowledge.
* **Content Focus:** Prioritize information related to:
    * Benefits and Entitlements (pensions, healthcare, education, welfare schemes).
    * Resettlement and Employment (job opportunities, training, entrepreneurship).
    * Support Services (counseling, legal aid, disability support).
    * Community and Associations (veteran organizations, events).
    * General Information (policies, application processes, required documents).
* **Tone:** Maintain a helpful, respectful, and empathetic tone.
* **No Metadata:** Do NOT include any source document identifiers, page numbers, or file names.

Context: {context}
Question: {question}

Helpful Answer:
"""

# Global variables to hold various resources and clients
our_knowledge_base = None
llm_model = None
job_data_df = None
mongo_client = None
mongo_collection = None

# Function to call Gemini 1.5 Flash API for generative responses
def ask_gemini_flash(prompt, api_key=None):
    api_key = api_key or GEMINI_API_KEY
    if not api_key:
        return "Gemini API key missing."

    restriction_prefix = (
    "You are a dedicated assistant for Indian ex-servicemen and veteran-related matters.\n"
    "This assistant is built specifically for ex-servicemen, so assume every user query is related to the Indian defense background — even if the word 'ex-serviceman' is not mentioned.\n\n"
    "You must respond confidently to:\n"
    "- Job-related queries (openings, resettlement, AWPO, DGR, placement support)\n"
    "- Welfare schemes, SPARSH portal, ECHS, pensions, AFD online store\n"
    "- Exams and institutions like NDA, CDS, SSB\n"
    "- Defense documentation, ID cards, benefits, quota in education or jobs\n"
    "- Anything involving the Indian Army, Navy, Air Force, or Ministry of Defence\n\n"
    "You must correctly interpret short forms or abbreviations in defense context:\n"
    "- 'NDA' = National Defence Academy\n"
    "- 'AWPO' = Army Welfare Placement Organisation\n"
    "- 'DGR' = Directorate General Resettlement\n"
    "- 'ECHS' = Ex-Servicemen Contributory Health Scheme\n"
    "- 'SPARSH' = Pension system for defense pensioners\n"
    "- 'AFD' = Armed Forces CSD Canteen Store Department portal\n"
    "If users write abbreviations like 'a w p o', or lowercase like 'echs', still understand the correct meaning.\n\n"
    "Only if the query is completely unrelated to defense or veterans — such as about celebrities, general trivia, entertainment, politics, or religion — then politely respond with:\n"
    "'Sorry, I can only assist with queries related to Indian ex-servicemen, defense services, or veteran affairs.'\n\n"
    f"User Query: {prompt}"
    )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    body = {"contents": [{"parts": [{"text": restriction_prefix}]}]}

    try:
        response = requests.post(url, headers=headers, params=params, json=body, timeout=10)
        if response.ok:
            data = response.json()
            return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        return "Gemini API error: " + response.text
    except Exception as e:
        return f"Gemini request failed: {e}"


# Helper function to detect if the query is about salaries
def is_salary_query(prompt):
    keywords = ["salary", "pay", "monthly salary", "ctc", "package", "income", "expected salary", "expected pay"]
    return any(kw in prompt.lower() for kw in keywords)

# Setup connection and indexes for MongoDB
def initialize_mongodb():
    global mongo_client, mongo_collection
    try:
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[MONGODB_DBNAME]
        mongo_collection = mongo_db[MONGODB_COLLECTION]
        print("MongoDB connected successfully.")
        existing_indexes = mongo_collection.index_information()
        for name, info in existing_indexes.items():
            if info.get("weights"):
                print(f"Dropping existing text index: {name}")
                mongo_collection.drop_index(name)
        # Create text index to support full-text search on important fields
        mongo_collection.create_index([
            ("title", "text"),
            ("description", "text"),
            ("skills", "text"),
            ("location", "text"),
            ("rank", "text"),
            ("education", "text"),
            ("last_date", "text")
        ])
        print("Text index created/verified on MongoDB collection.")
        print(mongo_collection.index_information())
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        mongo_client = None
        mongo_collection = None

# Load the vector store (FAISS) for document retrieval
def initialize_vector_store():
    global our_knowledge_base
    try:
        embedding_engine = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        our_knowledge_base = FAISS.load_local(
            VECTOR_STORE_PATH,
            embedding_engine,
            allow_dangerous_deserialization=True
        )
        print("Vector store loaded successfully.")
    except Exception as e:
        our_knowledge_base = None
        print(f"Error loading vector store: {e}")

# Initialize the FLAN-T5 small model pipeline
def initialize_flan_t5_model(model_name):
    global llm_model
    if llm_model:  # If the model has already been loaded once, it avoids reloading it again
        return llm_model
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        device_index = 0 if torch.cuda.is_available() else -1
        print(f"Running model on {'GPU' if device_index == 0 else 'CPU'}")
        model_pipeline = pipeline(
            task="text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.2,
            device=device_index
        )
        llm_model = HuggingFacePipeline(pipeline=model_pipeline)
        print(f"Model '{model_name}' is ready.")
        return llm_model
    except Exception as e:
        llm_model = None
        print(f"Failed to load model: {e}")
        return None

# Load job listings CSV into a DataFrame
def load_jobs_csv():
    global job_data_df
    if os.path.exists(JOBS_CSV_PATH):
        job_data_df = pd.read_csv(JOBS_CSV_PATH)
        if job_data_df.empty:
            print("Warning: Jobs CSV file is empty.")
        else:
            print(f"Loaded {len(job_data_df)} job listings.")
    else:
        job_data_df = pd.DataFrame()
        print("Jobs CSV file not found.")

# Check if query is related to jobs
def is_job_related(prompt):
    job_keywords = [
        "job", "jobs", "employment", "vacancy", "career", "openings", "hiring",
        "description", "skills", "requirements", "key requirement"
    ]
    return any(keyword in prompt.lower() for keyword in job_keywords)

# Check if query pertains to ex-servicemen info
def is_ex_servicemen_info(prompt):
    ex_keywords = ["retired officer", "veteran", "retired", "army", "navy", "air force", "military", "defence"]
    return any(word in prompt.lower() for word in ex_keywords)

# Generate job-related response based on user query
def get_job_response(prompt=None):
    if job_data_df is None or job_data_df.empty:
        return "Sorry, job data is currently unavailable."

    prompt_lower = prompt.lower() if prompt else ""

    # If user requests recent or top jobs, sort and return top 5
    if any(term in prompt_lower for term in ["latest jobs", "top jobs", "recent jobs", "5 jobs", "recent job opening"]):
        top_jobs = job_data_df.sort_values(by="Post Date", ascending=False).head(5)
        result_lines = []
        for _, row in top_jobs.iterrows():
            title = row.get('Job Title', 'N/A')
            company = row.get('Company Name', 'N/A')
            location = row.get('Location', 'N/A')
            salary = row.get('Salary', 'Not given')
            link = row.get('Job Link', '')
            line = f"🔹 **{title}** at *{company}* in {location} | 💰 {salary}"
            if pd.notna(link):
                line += f" → [View Job]({link})"
            result_lines.append(line)
        return "\n".join(result_lines)

    all_locations = job_data_df['Location'].dropna().unique()
    all_titles = job_data_df['Job Title'].dropna().unique()

    # Enhanced location matching logic
    def normalize_location(loc):
        # Convert to lowercase, remove special chars, standardize some common variations
        loc = loc.lower().strip()
        loc = re.sub(r'[^\w\s]', ' ', loc)  # Replace special chars with space
        
        # Standardize state names and common variations
        state_mapping = {
            'andra pradesh': 'andhra pradesh',
            'andhrapradesh': 'andhra pradesh',
            'ap': 'andhra pradesh',
            'telengana': 'telangana',
            'telagana': 'telangana',
            'tg': 'telangana',
            'tn': 'tamil nadu',
            'tamilnadu': 'tamil nadu',
            'up': 'uttar pradesh',
            'mp': 'madhya pradesh',
            'mh': 'maharashtra',
            'maha': 'maharashtra',
            'ka': 'karnataka',
            'kar': 'karnataka',
            'wb': 'west bengal',
            'delhi ncr': 'delhi',
            'ncr': 'delhi',
            'new delhi': 'delhi',
            'bangalore': 'bengaluru',
            'bengalore': 'bengaluru',
            'bombay': 'mumbai',
            'calcutta': 'kolkata',
            'madras': 'chennai',
            'hyd': 'hyderabad',
            'secunderabad': 'hyderabad',
            'pune city': 'pune',
            'jaipur city': 'jaipur',
            'kochi': 'cochin',
            'trivandrum': 'thiruvananthapuram',
            'tvpm': 'thiruvananthapuram'
        }
        
        for variant, standard in state_mapping.items():
            if variant in loc:
                return standard
        return loc

    # Process user query for location
    query_locations = []
    prompt_normalized = normalize_location(prompt_lower)
    
    # Extract all possible locations from the user query
    for loc in all_locations:
        # Split multi-location entries and check each part
        location_parts = str(loc).split(';')
        for part in location_parts:
            part = part.strip()
            normalized_part = normalize_location(part)
            
            # Check if this location part is mentioned in the query
            if (normalized_part in prompt_normalized or 
                prompt_normalized in normalized_part or
                any(word in prompt_normalized.split() for word in normalized_part.split() if len(word) > 3)):
                query_locations.append(loc)  # Add the full original location entry
                break  # Found a match in this location entry, no need to check other parts
    
    # Match job titles (keeping existing logic)
    matched_titles = [title for title in all_titles if title.lower() in prompt_lower]

    matched_jobs = job_data_df.copy()
    if matched_titles:
        matched_jobs = matched_jobs[matched_jobs['Job Title'].apply(
            lambda x: any(t.lower() in str(x).lower() for t in matched_titles)
        )]
    
    # Apply the enhanced location filter
    if query_locations:
        matched_jobs = matched_jobs[matched_jobs['Location'].isin(query_locations)]

    if matched_jobs.empty:
        return ask_gemini_flash(prompt)

    # Check if user explicitly asks for description
    wants_description_only = (
        "description" in prompt_lower and "job" in prompt_lower and
        any(t.lower() in prompt_lower for t in matched_titles)
    )

    show_only_summary = (
        any(keyword in prompt_lower for keyword in ["job openings", "jobs in", "all jobs", "looking for"]) and
        not wants_description_only
    )

    # Helper function to filter by field keywords
    def filter_by_field_keyword(prompt, jobs_df):
        field_keywords = [
            "logistics", "supply chain", "warehouse", "inventory", "store", "distribution",
            "fleet", "transport", "driver", "material", "shipping", "procurement", "dispatch",
            "operations", "operation", "admin", "administrative", "compliance", "training",
            "security", "patrol", "fire", "defense", "surveillance", "guard", "supervisor",
            "monitoring", "control room", "emergency", "safety", "safety officer", "coordinator","executive",
            "sales", "banking", "customer", "marketing", "manager", "assistant",
            "data entry", "operator", "back office", "service", "trainer",
            "bank", "executive officer", "security officer", "field officer",
            "officer", "computer operator", "customer care", "call center",
            "receptionist", "hr", "human resource", "clerk"
        ]

        prompt = prompt.lower()
        matched_keywords = [kw for kw in field_keywords if kw in prompt]

        if matched_keywords:
            pattern = "|".join(matched_keywords)
            return jobs_df[jobs_df["Job Title"].str.lower().str.contains(pattern, na=False)]
        return jobs_df


    # Apply field-based filtering only if summary is requested
    if show_only_summary:
        matched_jobs = filter_by_field_keyword(prompt, matched_jobs)
        matched_jobs["Job Title"] = matched_jobs["Job Title"].astype(str).str.strip().str.lower()
        matched_jobs["Job Link"] = matched_jobs["Job Link"].astype(str).str.strip()
        matched_jobs = matched_jobs.drop_duplicates(subset=["Job Title", "Job Link"]).reset_index(drop=True)
    
        # If after filtering, jobs are empty then call Gemini
        if matched_jobs.empty:
            return "Sorry, no relevant job found in our data.\n\n" + ask_gemini_flash(prompt)


    # Final formatting loop
    result_lines = []

    for _, job in matched_jobs.iterrows():
        title = job.get('Job Title', 'N/A')
        expiry_status = job.get('Expiry', 'Unknown')  # e.g. "Expired" or "Available"
        status_label = f"[❌ Expired]" if expiry_status.lower() == "expired" else f"[✅ Available]"
        job_title_with_status = f"{title} {status_label}"
        company = job.get('Company Name', 'N/A')
        location = job.get('Location', 'N/A')
        salary = job.get('Salary', 'Not given')
        link = job.get('Job Link', 'N/A')
        #post_date = job.get('Post Date', 'Unknown')
        last_date = job.get('Last Date to Apply', 'Unknown')
        description = str(job.get("Job Description", "")).strip()

        if wants_description_only:
            lines = [
                f"🔹**Job Title:** {job_title_with_status}",
              # f"🗓️**Post Date:** {post_date}",
                f"📅**Last Date to Apply:** {last_date}",
                f"📝**Description:** {description}"
                f"🎯**Skills Required:** {job.get('Skills', 'Not specified')}"
            ]

        elif query_locations and not matched_titles:
            lines = [
                f"🔹**Job Title:** {job_title_with_status}",
                f"🏢**Company:** {company}",
                f"💰**Salary:** {salary}",
                f"📍**Location:** {location}",
                f"🔗**Link:** {link}",
                #f"🗓️**Post Date:** {post_date}",
                f"📅**Last Date to Apply:** {last_date}"
            ]

        elif show_only_summary:
            lines = [
                f"🔹**Job Title:** {job_title_with_status}",
                f"🔗**Link:** {link}",
               # f"🗓️**Post Date:** {post_date}",
                f"📅**Last Date to Apply:** {last_date}"
            ]

        else:
            lines = [
                f"🔹**Job Title:** {job_title_with_status}",
                f"🏢**Company:** {company}",
                f"💰**Salary:** {salary}",
                f"📍**Location:** {location}",
                f"🔗**Link:** {link}",
                #f"🗓️**Post Date:** {post_date}",
                f"📅**Last Date to Apply:** {last_date}"
            ]
            if description:
                lines.append(f"📝**Description:** {description}")
            skills = job.get("Skills", "")
            if skills:
                lines.append(f"🎯**Skills Required:** {skills}")

        result_lines.append("\n".join(lines))

    return "\n\n".join(result_lines)

# Prepare the prompt template for LangChain QA
def prepare_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

@app.route('/')
def home():
    # Serve the main landing page
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_input = request.json.get('prompt')
    if not user_input:
        return jsonify({"error": "Prompt missing from request."}), 400

    prompt_lower = user_input.lower()  


    # Priority 1: If user question starts with "what is", "who is", or "tell me about", use Gemini
    if prompt_lower.startswith(("what is", "who is", "tell me about","tell")):
        gemini_reply = ask_gemini_flash(user_input)
        return jsonify({"response": gemini_reply})


    # Priority 2: If query is salary-related, use specialized Gemini prompt
    if is_salary_query(user_input):
        salary_prompt = (
            "You are an expert on Indian police and defense salaries. "
            "Always begin with an estimated monthly salary range in INR. "
            "Then mention pay structure, allowances, and growth prospects concisely.\n\nQuery: " + user_input
        )
        salary_response = ask_gemini_flash(salary_prompt)
        return jsonify({"response": salary_response})

    # Priority 3: Job-related queries handled with CSV data
    if is_job_related(user_input):
        return jsonify({"response": get_job_response(user_input)})

    # Priority 4: Queries related to ex-servicemen info go to MongoDB text search
    if is_ex_servicemen_info(user_input):
        if mongo_collection is None:
            return jsonify({"error": "MongoDB not connected."}), 500
        try:
            # Prepare text search query
            search_query = {"$text": {"$search": user_input}}
            user_input_lower = user_input.lower()
            possible_locations = [
                "punjab", "delhi", "maharashtra", "uttar pradesh", "kerala", "jamshedpur",
                "haryana", "gujarat", "karnataka", "rajasthan", "bihar", "madhya pradesh",
                "telangana", "andhra pradesh", "tamil nadu", "jammu", "kashmir", "srinagar",
                "ahmedabad", "bangalore", "bhopal", "chandigarh", "chennai", "dehradun",
                "guwahati", "hyderabad", "jaipur", "kolkata", "lucknow", "mumbai",
                "nagpur", "patna", "pune", "ranchi", "shimla", "thiruvananthapuram"
            ]
            possible_ranks = [
                "major", "colonel", "brigadier",
                "any", "captain", "havildar", "jco", "lieutenant", "lt colonel",
                "naik", "officer cadet", "sepoy", "subedar","subedar major"
            ]

            possible_educations = [
            "10th", "12th", "diploma", "graduate", "graduation", "bachelor", "postgraduate", "10th pass", "12th pass",
            "pg", "btech", "mtech", "mba", "phd", "ba", "ma", "bcom", "mcom", "bsc", "msc","ug", "iti"
            ]
            # Add regex filters if location or rank found in query
            matched_location = next((loc for loc in possible_locations if loc in user_input_lower), None)
            matched_rank = next((rk for rk in possible_ranks if rk in user_input_lower), None)
            matched_education = next((edu for edu in possible_educations if edu in user_input_lower), None)
            if matched_location:
                search_query["location"] = {"$regex": matched_location, "$options": "i"}
            if matched_rank:
                search_query["rank"] = {"$regex": matched_rank, "$options": "i"}
            if matched_education:
                search_query["education"] = {"$regex": matched_education, "$options": "i"}

            results = mongo_collection.find(
                search_query,
                {"score": {"$meta": "textScore"}}
            ).sort([("score", {"$meta": "textScore"})]).limit(5)

            response_lines = []
            for doc in results:
                title = doc.get("title", "No Title")
                desc = doc.get("description", "No Description")
                skills = doc.get("skills", "Skills not mentioned")
                rank = doc.get("rank", "Rank not available")
                location = doc.get("location", "Location unknown")
                education = doc.get("education", "Education not listed")
                last_date = doc.get("last_date", "Last date not available")

                response_lines.append(
                    f"🔹 **{title}**\n"
                    f"- 🏅 Rank: {rank}\n"
                    f"- 📍 Location: {location}\n"
                    f"- 🎓 Education: {education}\n"
                    f"- 📜 Description: {desc}\n"
                    f"- 🛠️ Skills: {skills}\n"
                    f"- 🗓️ Last Date to Apply: {last_date}"
                )

            if response_lines:
                return jsonify({"response": "\n\n".join(response_lines)})
            else:
                # Fallback to Gemini if MongoDB gives no result
                gemini_fallback = ask_gemini_flash(user_input)
                return jsonify({"response": gemini_fallback})

        except Exception as e:
            return jsonify({"error": f"MongoDB query failed: {str(e)}"}), 500

    # Final fallback: Use vector store + language model to answer from indexed documents
    if our_knowledge_base is None:
        return jsonify({"error": "Vector store not loaded."}), 500
    if llm_model is None:
        return jsonify({"error": "LLM model not initialized."}), 500

    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=our_knowledge_base.as_retriever(search_kwargs={'k': 4}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prepare_prompt(PROMPT_TEMPLATE)}
        )
        response = qa_chain.invoke({'query': user_input})
        answer_text = response.get("result", "").strip().lower()
        generic_failures = [
            "i apologize", "not enough specific", "i do not have enough",
            "sorry", "insufficient", "unable to find", "no relevant information", "helpful"
        ]

        if answer_text and not any(frag in answer_text for frag in generic_failures):
            return jsonify({"response": response["result"]})
        else:
            return jsonify({"response": ask_gemini_flash(user_input)})

    except Exception as e:
        return jsonify({"error": f"Vector store error: {e}"}), 500

if __name__ == "__main__":
    if not os.path.exists('templates'):
        os.makedirs('templates')
    print("Starting server...")
    initialize_vector_store()
    initialize_flan_t5_model(LOCAL_MODEL_NAME)
    load_jobs_csv()
    initialize_mongodb()
    print("Initialization complete. Server is live.")
    app.run(debug=True, port=5000)