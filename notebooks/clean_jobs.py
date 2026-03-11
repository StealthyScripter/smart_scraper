import pandas as pd

df = pd.read_csv("data/raw_jobs.csv")

print("Initial dataset size:", len(df))

# remove rows that are completely empty
df = df.dropna(how="all")

# remove rows missing essential fields
df = df.dropna(subset=["title", "company", "location"])

# clean whitespace
df["title"] = df["title"].str.strip()
df["company"] = df["company"].str.strip()
df["location"] = df["location"].str.strip()

# deduplicate using your rule
df = df.drop_duplicates(subset=["title", "company", "location"])

print("Final dataset size:", len(df))

df.to_csv("data/cleaned_jobs.csv", index=False)

print("Clean dataset saved.")