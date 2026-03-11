import pandas as pd

df = pd.read_csv("data/raw_jobs.csv")

print("Initial dataset size:", len(df))

df = df.dropna(how="all")

df = df.dropna(subset=["title"])

df = df.dropna(subset=["company"])

df = df.drop_duplicates()

df["title"] = df["title"].str.strip()
df["company"] = df["company"].str.strip()
df["location"] = df["location"].str.strip()

print("Final dataset size:", len(df))

df.to_csv("data/cleaned_jobs.csv", index=False)

print("Clean dataset saved.")