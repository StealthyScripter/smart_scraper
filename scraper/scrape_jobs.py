from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()

job_data = []

#Number of pages to scrape per keyword (25 jobs per page)
pages = 3

# List of keywords to search for. You can modify this list based on your needs.
keywords = [
    "data analyst",
    "software engineer",
    "data engineer",
    "system administrator",
    "database administrator",
    "devops engineer",
    "machine learning engineer",
    "backend developer",
    "frontend developer",
    "full stack developer"
]

for keyword in keywords:

    search = keyword.replace(" ", "%20")

    print(f"\nSearching: {keyword}")

    # Loop through the specified number of pages for each keyword
    for page in range(0,pages):

        url = f"https://www.linkedin.com/jobs/search/?keywords={search}&location=United%20States&start={page*25}"

        driver.get(url)

        time.sleep(5)

        jobs = driver.find_elements(By.CSS_SELECTOR, ".base-card")

        print(f"Page {page} cards:", len(jobs))

        for job in jobs:

            try:
                title = job.find_element(By.CSS_SELECTOR, ".base-search-card__title").text.strip()
            except:
                title = None

            try:
                company = job.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle a").text.strip()
            except:
                company = None

            try:
                location = job.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
            except:
                location = None

            try:
                date = job.find_element(By.CSS_SELECTOR, "time").text.strip()
            except:
                date = None

            try:
                link = job.find_element(By.CSS_SELECTOR, ".base-card__full-link").get_attribute("href")
            except:
                link = None

            if title and company and location:
                job_data.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "date": date,
                    "search_role": keyword,
                    "job_link": link
                })

driver.quit()

# Create a DataFrame and remove duplicates based on title, company, and location
df = pd.DataFrame(job_data)

print("\nRows before dedup:", len(df))

# duplicate rule: same title + company + location
df = df.drop_duplicates(subset=["title", "company", "location"])

print("Rows after dedup:", len(df))

df.to_csv("data/raw_jobs.csv", index=False)

print("\nSaved jobs:", len(df))