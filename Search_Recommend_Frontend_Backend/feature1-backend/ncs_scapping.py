from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

def scrape_ncs_jobs():
    print("Opening NCS job search page...")

    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.ncs.gov.in/job-seeker/Pages/Search.aspx")

    try:
        # Wait and click the Search button (don't fill anything)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ctl00_spMainContent_btnSearch"))
        ).click()

        time.sleep(5)  # Let job results load

        job_cards = driver.find_elements(By.CLASS_NAME, "card-job")
        print(f"Found {len(job_cards)} job cards.")

        jobs = []
        for card in job_cards:
            try:
                title = card.find_element(By.CLASS_NAME, "job-title").text.strip()
                org = card.find_element(By.CLASS_NAME, "job-company").text.strip()
                loc = card.find_element(By.CLASS_NAME, "job-location").text.strip()
                posted = card.find_element(By.CLASS_NAME, "job-posted-date").text.strip()

                jobs.append({
                    "title": title,
                    "organization": org,
                    "location": loc,
                    "date_posted": posted,
                    "source": "ncs.gov.in"
                })
            except Exception as e:
                continue

        driver.quit()

        if jobs:
            df = pd.DataFrame(jobs)
            filename = f"ncs_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Scraped and saved {len(jobs)} jobs to {filename}")
        else:
            print("⚠️ Search worked, but no jobs found.")
    except Exception as e:
        print("❌ Error during scraping:", e)
        driver.quit()

if __name__ == "__main__":
    scrape_ncs_jobs()
