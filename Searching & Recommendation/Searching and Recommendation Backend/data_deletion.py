from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["SainikHire"]
collection = db["database1"]

#deleting expired jobs
def delete_expired_jobs():
    today = datetime.today().date()
    deleted_count = 0

    for job in collection.find():
        last_date_str = job.get("last_date")
        if last_date_str:
            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                if last_date < today:
                    collection.delete_one({"_id": job["_id"]})
                    deleted_count += 1
            except ValueError:
                print(f" Invalid date format: {last_date_str}")
    print(f"[{datetime.now()}]  Deleted {deleted_count} expired job(s).")

#automation of detetion of expired jobs
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_jobs, 'cron', hour=16, minute=17)
scheduler.start()