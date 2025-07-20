# SainikHire – Backend (Searching, Recommendation, Email)

Built with:
- Flask for Backend 
- MongoDB for Database
- Selenium and BeautifulSoup for Web Scraping
- SentenceTransformer for Semantic Search

##  Features
-  Semantically job matching using SentenceTransformer
-  Recommends job based on profile
-  Email reminders for job deadlines before 5 days
-  Daily scraping from [NCS](https://www.ncs.gov.in) and [DGR](https://dgrindia.gov.in)
-  Automatic deletion of expired jobs


# Project Structure
<pre>  
├── Search and Recommendation Backend/
│   ├── app.py
│   ├── data_deletion.py
│   ├── email_sending.py
│   ├── jobForm.py
│   ├── match_job.py
│   ├── recommend_job_logic.py
│   ├── signupForm.py
│   ├── updating_database.py
│   ├── updating_from_dgr.py
│   └── requirements.txt
</pre>

## 🔧 Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SHRISTI-125/SainikHire.git
   cd SainikHire
   cd "Searching and Recommendation Backend"
2. Install Dependencies
   ```bash
   pip install -r requirements.txt
3. Run the development server
   ```bash
   python app.py

<br>
It will run on http://localhost:5000/
