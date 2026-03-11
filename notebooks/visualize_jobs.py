import pandas as pd
import plotly.express as px

# Load cleaned dataset
df = pd.read_csv("data/cleaned_jobs.csv")

# -----------------------------
# 1️⃣ BAR CHART — Jobs by Role
# -----------------------------
role_counts = df["search_role"].value_counts()

fig1 = px.bar(
    role_counts,
    title="Job Distribution by Role",
    labels={"value": "Number of Jobs", "index": "Role"},
)

fig1.show()


# ----------------------------------
# 2️⃣ PIE CHART — Job Role Share
# ----------------------------------
fig2 = px.pie(
    values=role_counts.values,
    names=role_counts.index,
    title="Share of Jobs by Role"
)

fig2.show()


# ----------------------------------
# 3️⃣ HORIZONTAL BAR — Top Companies
# ----------------------------------
top_companies = df["company"].value_counts().head(10)

fig3 = px.bar(
    top_companies,
    orientation="h",
    title="Top Hiring Companies",
    labels={"value": "Number of Jobs", "index": "Company"}
)

fig3.show()


# ----------------------------------
# 4️⃣ LINE CHART — Job Posting Dates
# ----------------------------------
date_counts = df["date"].value_counts()

fig4 = px.line(
    x=date_counts.index,
    y=date_counts.values,
    title="Job Posting Frequency by Date",
    labels={"x": "Date Posted", "y": "Number of Jobs"}
)

fig4.show()


# ----------------------------------
# 5️⃣ TREEMAP — Jobs by Company
# ----------------------------------
company_counts = df["company"].value_counts().reset_index()
company_counts.columns = ["company", "count"]

fig5 = px.treemap(
    company_counts,
    path=["company"],
    values="count",
    title="Job Distribution by Company"
)

fig5.show()
