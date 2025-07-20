import requests
from bs4 import BeautifulSoup as s
from urllib.parse import quote
#from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import threading
import time
import schedule

print("Connecting to MongoDB")
client = MongoClient("mongodb://localhost:27017/")
db = client["SainikHire"]
collection = db["database1"]


print("Loading model")
model = SentenceTransformer("all-MiniLM-L6-v2")

urls = [
    "https://dgrindia.gov.in/Content2/job-assistance/job-for-jcos-or",  # JCO/OR
    "https://dgrindia.gov.in/Content1/job-assistance/job-for-officers"  # Officers
]
base_url = "https://dgrindia.gov.in"
job_type_counter = 0  


def extracted_jobs():
    global job_type_counter
    url = urls[job_type_counter % 2]  # adding url one by one, both
    job_type_counter += 1

    print(f"Fetching job listings from: {url}")
    try:
        response = requests.get(url)
        soup = s(response.text, 'html.parser')
    except Exception as e:
        print(f" Can't fetch jobs: {e}")
        return

    jobs = []
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")[1:]  
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 7:
                continue

            href = cols[6].find("a")["href"] if cols[6].find("a") else None
            apply_link = base_url + quote(href) if href else "https://dgrindia.gov.in/Content2/job-assistance/job-for-jcos-or"


            job = {
                "title": cols[3].text.strip(),
                "company": cols[1].text.strip(),
                "location": "As per notification in apply link",
                "description": cols[4].text.strip(),
                "date_of_posting": "Apply soon",
                "last_date": cols[5].text.strip(),
                "education": "As per Notification",
                "skills": "Communication",
                "rank": "Any",
                "apply_link": apply_link 
            }

            jobs.append(job)
            print(job)

    print(f"Extracted {len(jobs)} jobs from DGR.")

    inserted_count = 0
    for job in jobs:
        try:
            combined_text = f"{job['title']} {job['description']} {job['company']} {job['skills']} {job['location']}"
            skill_encode = model.encode(job['skills'])
            embedding = model.encode(combined_text)

            job["skills_embedding"] = skill_encode.tolist()
            job["all_combined_embedding"] = embedding.tolist()

            if job.get("title", "").strip() and job.get("company", "").strip():
                if not collection.find_one({"title": job["title"], "company": job["company"]}):
                    collection.insert_one(job)
                    inserted_count += 1
        except Exception as e:
            print(f"Skipping job due to error: {e}")

    print(f" Inserted {inserted_count} new jobs (skipped {len(jobs) - inserted_count} duplicates).")


#Scheduler Setup
#scheduler = BackgroundScheduler()
#scheduler.add_job(extracted_jobs, 'cron',hour=14,minute=42)
#scheduler.start()

def run_scheduler():
    schedule.every(1).days.do(extracted_jobs)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Run scheduler in background
t = threading.Thread(target=run_scheduler)
t.start()