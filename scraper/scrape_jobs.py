from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

job_data = []

for page in range(0,3):

    url = f"https://www.linkedin.com/jobs/search/?keywords=data%20analyst&start={page*25}"

    driver.get(url)

    time.sleep(5)

    jobs = driver.find_elements(By.CLASS_NAME, "base-card")

    for job in jobs:

        try:
            title = job.find_element(By.CLASS_NAME, "base-search-card__title").text
        except:
            title = None

        try:
            company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
        except:
            company = None

        try:
            location = job.find_element(By.CLASS_NAME, "job-search-card__location").text
        except:
            location = None

        job_data.append({
            "title": title,
            "company": company,
            "location": location
        })

driver.quit()

df = pd.DataFrame(job_data)

df.to_csv("data/raw_jobs.csv", index=False)

print("Saved", len(df), "jobs")