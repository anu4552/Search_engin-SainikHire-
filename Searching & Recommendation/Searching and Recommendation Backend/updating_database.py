from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
#from apscheduler.schedulers.background import BackgroundScheduler
import time
import schedule
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import threading


driver_path = r"D:\Shristi Kumari\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
url = "https://www.ncs.gov.in/job-seeker/Pages/Search.aspx?E=6gqhwycyVHE%3D&jn=Rca60ftwa7T5VLzMeheBcg%3D%3D&OT=fheFJjl41aGWG85YSvGqng%3D%3D&Source=https://www.ncs.gov.in/"
maximum_pages = 16

client = MongoClient("mongodb://localhost:27017/")
db = client["SainikHire"]
collection = db["database1"]

model = SentenceTransformer("all-MiniLM-L6-v2")
print("model connected")

options = Options()
print("1")
options.add_argument("--headless")  
print("2")
options.add_argument("--no-sandbox")
print("3")
options.add_argument("--disable-dev-shm-usage")
print("4")

def updateJobs():
  collection.delete_many({"title": "", "company": ""})
  print("Scraping NCS")
  driver = webdriver.Chrome(service=Service(driver_path), options=options)
  print("searching")
  driver.get(url)
  print("url")
  time.sleep(5)
  print("sleeping after 5 seconds")
  jobs = []
  print("extracting jobs")
  def extract_jobs():
      nonlocal jobs
      job_cards = driver.find_elements(By.CLASS_NAME, "paddingTop5")
      for job in job_cards:
          try:
              title = job.find_element(By.XPATH, ".//span[contains(@id, 'lblJobTitle')]").text
          except: title = ""
          try:
              company = job.find_element(By.XPATH, ".//span[contains(@id, 'lblOrganization')]").text
          except: company = ""
          try:
              location = job.find_element(By.XPATH, ".//span[contains(@id, 'lblStateName')]").text
          except: location = ""
          try:
              skills = job.find_element(By.XPATH, ".//span[contains(@id, 'lblKeywords')]").text
          except: skills = ""
          try:
              posted_on = job.find_element(By.XPATH, ".//span[contains(@id, 'lblPostedOn')]").text
          except: posted_on = ""
          try:
              description = job.find_element(By.XPATH, ".//span[contains(text(), 'Job Description:')]/following-sibling::span").text
          except: description = ""
          try:
              apply_element = job.find_element(By.XPATH, ".//a[contains(@onclick, 'ViewJobPopup')]")
              onclick_attr = apply_element.get_attribute("onclick")
              apply_link = onclick_attr.split("ViewJobPopup('")[1].split("')")[0]
          except: apply_link = ""
          try:
              posted_date = datetime.strptime(posted_on, "%d/%m/%Y")  
              last_date = posted_date + timedelta(days=30)
              last_date_str = last_date.strftime("%d/%m/%Y")
          except:
              last_date_str = ""
          jobs.append({
              "title": title,
              "company": company,
              "location": location,
              "skills": skills,
              "date_of_posting": posted_on,
              "rank":"any",
              "education":"10th pass",
              "description": description,
              "apply_link": apply_link,
              "last_date" : last_date_str
          })
  extract_jobs()
  print("arranging extracted jobs")
  for page_num in range(2, maximum_pages + 1):
      try:
          print(f"Moving to page {page_num}...")
          link = driver.find_element(By.LINK_TEXT, str(page_num))
          driver.execute_script("arguments[0].click();", link)
          time.sleep(4)
          extract_jobs()
      except Exception as e:
          print(f"Couldn't fetch page {page_num}: {e}")
          break
  driver.quit()
  inserted_count = 0
  print("database using")
  for job in jobs:
      combined_text = f"{job.get('skills', '')} {job.get('location', '')} 10th pass any"
      skills = f"{job.get('skills', '')} "
      skill_encode = model.encode(skills)
      embedding = model.encode(combined_text)
      job["skills_embedding"] = skill_encode.tolist()
      job["all_combined_embedding"] = embedding.tolist()
      job.pop("_id", None)
      if not collection.find_one({"title": job["title"], "company": job["company"]}):
          collection.insert_one(job)
          inserted_count += 1
  print(f"Inserted {inserted_count} new jobs (skipped {len(jobs) - inserted_count} duplicates).")

print("again scheduling")

# Scheduling scraping 
#scheduler = BackgroundScheduler()
#scheduler.add_job(updateJobs, 'cron', hour=14, minute=41)
#scheduler.start()
#
#while True:
#    schedule.run_pending()
#    time.sleep(60)


def run_scheduler():
    schedule.every(1).days.do(updateJobs)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Run scheduler in background
t = threading.Thread(target=run_scheduler)
t.start()