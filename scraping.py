import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- Config ---
CHROMEDRIVER_PATH = r"C:\Users\hp\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
NCS_URL = "https://www.ncs.gov.in/job-seeker/Pages/Search.aspx?E=6gqhwycyVHE%3D&jn=Rca60ftwa7T5VLzMeheBcg%3D%3D&OT=fheFJjl41aGWG85YSvGqng%3D%3D&Source=https://www.ncs.gov.in/"
MAX_PAGES = 16
CSV_SAVE_PATH = "data/ncs_jobs.csv"

# --- Setup Selenium Options ---
options = Options()
options.add_argument("--headless")  # Run without opening browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# --- Helper: Extract Job Data from Page ---
def extract_jobs_from_page(driver):
    jobs = []
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
            salary = job.find_element(By.XPATH, ".//span[contains(text(), 'Salary:')]/following-sibling::span").text
        except:
            salary = "Not given"

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
            post_date = datetime.strptime(posted_on, "%d/%m/%Y")
            last_date = post_date + timedelta(days=30)
            last_date_str = last_date.strftime("%Y-%m-%d")
            post_date_str = post_date.strftime("%Y-%m-%d")
            status = "Expired" if datetime.today().date() > last_date.date() else "Currently Open"
        except:
            post_date_str = ""
            last_date_str = ""
            status = "Unknown"

        job_info = {
            "Job Title": title,
            "Job Link": apply_link,
            "Company Name": company,
            "Location": location,
            "Salary": salary,  
            "Post Date": post_date_str,
            "Job Description": description,
            "Skills": skills,
            "Last Date to Apply": last_date_str,
            "Expiry": status
        }
        
        required_fields = [title, company, location, description, skills]
        if not all(field.strip() for field in required_fields):
            print("Skipping job due to missing essential information")
            continue
        jobs.append(job_info)
    return jobs

# --- Main Scraping Function ---
def scrape_ncs_jobs():
    print("Starting NCS job scraping...")
    all_jobs = []

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get(NCS_URL)
    time.sleep(5)

    all_jobs.extend(extract_jobs_from_page(driver))

    for page in range(2, MAX_PAGES + 1):
        try:
            print(f"Navigating to page {page}...")
            link = driver.find_element(By.LINK_TEXT, str(page))
            driver.execute_script("arguments[0].click();", link)
            time.sleep(4)
            all_jobs.extend(extract_jobs_from_page(driver))
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    driver.quit()
    print(f"Total jobs scraped: {len(all_jobs)}")
    return pd.DataFrame(all_jobs)

# --- Save to CSV ---
def save_jobs_to_csv(jobs_df):
    os.makedirs(os.path.dirname(CSV_SAVE_PATH), exist_ok=True)
    if os.path.exists(CSV_SAVE_PATH):
        old_df = pd.read_csv(CSV_SAVE_PATH)
        combined_df = pd.concat([old_df, jobs_df], ignore_index=True)
        combined_df.drop_duplicates(subset=["Job Title", "Company Name"], inplace=True)
        combined_df.to_csv(CSV_SAVE_PATH, index=False)
        print(f"Updated CSV: {CSV_SAVE_PATH} ({len(combined_df)} total jobs)")
    else:
        jobs_df.to_csv(CSV_SAVE_PATH, index=False)
        print(f"Saved jobs to new CSV: {CSV_SAVE_PATH}")

# --- Main Execution ---
if __name__ == "__main__":
    df = scrape_ncs_jobs()
    if not df.empty:
        save_jobs_to_csv(df)
    else:
        print("No jobs found.")
