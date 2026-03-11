from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

job_data = []

for page in range(0,5):

    url = f"https://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=United%20States&start={page*25}"

    driver.get(url)

    time.sleep(5)

    jobs = driver.find_elements(By.CSS_SELECTOR, ".base-card")

    print(f"Page {page} jobs found:", len(jobs))

    for job in jobs:

        try:
            title = job.find_element(By.CSS_SELECTOR, ".base-search-card__title").text
        except:
            title = None

        try:
            company = job.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle a").text
        except:
            company = None

        try:
            location = job.find_element(By.CSS_SELECTOR, ".job-search-card__location").text
        except:
            location = None

        try:
            date = job.find_element(By.CSS_SELECTOR, "time").text
        except:
            date = None

        if title and company:
            job_data.append({
                "title": title,
                "company": company,
                "location": location,
                "date": date
            })

driver.quit()

df = pd.DataFrame(job_data)

df = df.drop_duplicates()

df.to_csv("data/raw_jobs.csv", index=False)

print("Saved", len(df), "jobs")