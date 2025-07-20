from secret import password
import schedule
import smtplib
from email.message import EmailMessage
from pymongo import MongoClient
from datetime import datetime, timedelta
import time
import threading

password=password()
# Email 
SENDER_EMAIL = "shristikumarisingh125@gmail.com"
APP_PASSWORD = password

client = MongoClient("mongodb://localhost:27017/")
db = client["SainikHire"]
users_col = db["new_user"]
jobs_col = db["database1"]

def send_job_reminders():
    print(f"[{datetime.now()}] Loading!")

    today = datetime.now().date()
    cutoff = today + timedelta(days=5)

    upcoming_jobs = list(jobs_col.find({
        "last_date": {
            "$gte": today.strftime('%Y-%m-%d'),
            "$lte": cutoff.strftime('%Y-%m-%d')
        }
    }))

    if not upcoming_jobs:
        print("No upcoming jobs found.")
        return

    # summary
    job_lines = []
    for job in upcoming_jobs:
        job_lines.append(f"{job['title']} - Last Date: {job['last_date']}\nLink: {job.get('link', 'http://localhost:5173/')}\n")

    job_summary = "\n".join(job_lines)

    subject = "Upcoming Job Deadlines within Next 5 Days"
    body = f"""Hi there,
    
    Here are some jobs whose last dates are coming soon, apply as soon as possible
    {job_summary}
    
    Regards,
    SainikHire
    """

    user_emails = [user['email'] for user in users_col.find()]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        for email in user_emails:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = email
            msg.set_content(body)
            smtp.send_message(msg)
            print(f"Sent to: {email}")

send_job_reminders() 
#schedule.every(1).days.do()

#print("Scheduler started. Waiting to send reminders every 1 days...")

def run_scheduler():
    schedule.every(1).days.do(send_job_reminders)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Run scheduler in background
t = threading.Thread(target=run_scheduler)
t.start()
