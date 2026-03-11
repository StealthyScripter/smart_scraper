import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_jobs.csv")

print("Dataset shape:", df.shape)
print()

# Top companies hiring
top_companies = df["company"].value_counts().head(10)

print("\nTop Hiring Companies:")
print(top_companies)

# Jobs by role category
role_counts = df["search_role"].value_counts()

print("\nJobs by Role Category:")
print(role_counts)

# Jobs by location
top_locations = df["location"].value_counts().head(10)

print("\nTop Locations:")
print(top_locations)

# Store results for later visualization
analysis = {
    "role_counts": role_counts,
    "top_companies": top_companies,
    "top_locations": top_locations
}

print("\nEDA completed successfully.")
