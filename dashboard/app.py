import streamlit as st
import pandas as pd
import plotly.express as px
import re

# PAGE SETUP
st.set_page_config(
    page_title="Job Market Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
df = pd.read_csv("data/cleaned_jobs.csv")

# SKILL EXTRACTION
skills = [
    "python","sql","aws","azure","docker","kubernetes",
    "machine learning","tensorflow","pytorch",
    "javascript","react","node","spark"
]

def extract_skills(title):
    found=[]
    for s in skills:
        if re.search(s,title.lower()):
            found.append(s)
    return found

df["skills"] = df["title"].apply(lambda x: ", ".join(extract_skills(str(x))))

# REMOTE VS ONSITE
df["work_type"] = df["location"].apply(
    lambda x: "Remote" if "remote" in str(x).lower() else "Onsite"
)

# HEADER
st.title("📊 Job Market Analytics Dashboard")

# FILTERS WITH CHECKBOX DROPDOWNS
col1,col2,col3,col4 = st.columns(4)

# ---------- ROLE ----------
roles = sorted(df["search_role"].unique())

if "selected_roles" not in st.session_state:
    st.session_state.selected_roles = roles

with col1.popover(f"Role ({len(st.session_state.selected_roles)})"):
    new_selection=[]
    for r in roles:
        checked = st.checkbox(r, value=r in st.session_state.selected_roles)
        if checked:
            new_selection.append(r)
    st.session_state.selected_roles = new_selection

# ---------- LOCATION ----------
locations = sorted(df["location"].unique())

if "selected_locations" not in st.session_state:
    st.session_state.selected_locations = locations

with col2.popover(f"Location ({len(st.session_state.selected_locations)})"):
    new_selection=[]
    for loc in locations:
        checked = st.checkbox(loc, value=loc in st.session_state.selected_locations)
        if checked:
            new_selection.append(loc)
    st.session_state.selected_locations = new_selection

# ---------- COMPANY ----------
companies = sorted(df["company"].unique())

if "selected_companies" not in st.session_state:
    st.session_state.selected_companies = companies

with col3.popover(f"Company ({len(st.session_state.selected_companies)})"):
    new_selection=[]
    for c in companies:
        checked = st.checkbox(c, value=c in st.session_state.selected_companies)
        if checked:
            new_selection.append(c)
    st.session_state.selected_companies = new_selection

# ---------- SEARCH ----------
search = col4.text_input("🔎 Search Job Title")

# APPLY FILTERS
filtered = df[
    (df["search_role"].isin(st.session_state.selected_roles)) &
    (df["location"].isin(st.session_state.selected_locations)) &
    (df["company"].isin(st.session_state.selected_companies))
]

if search:
    filtered = filtered[filtered["title"].str.contains(search,case=False)]

# KPI METRICS
total_jobs=len(filtered)
companies_count=filtered["company"].nunique()
locations_count=filtered["location"].nunique()
top_role=filtered["search_role"].value_counts().idxmax()

k1,k2,k3,k4 = st.columns(4)

k1.metric("📊 Total Jobs", total_jobs)
k2.metric("🏢 Companies Hiring", companies_count)
k3.metric("📍 Locations", locations_count)
k4.metric("⭐ Top Role", top_role)

st.divider()

# JOBS BY ROLE
col1,col2 = st.columns(2)

role_counts = filtered["search_role"].value_counts().reset_index()
role_counts.columns=["role","count"]

fig_role = px.bar(
    role_counts,
    x="count",
    y="role",
    orientation="h",
    color="role",
    title="Jobs by Role"
)

col1.plotly_chart(fig_role,width="stretch")

# ROLE DISTRIBUTION
fig_pie = px.pie(
    role_counts,
    values="count",
    names="role",
    title="Role Distribution"
)

col2.plotly_chart(fig_pie,width="stretch")

# TOP COMPANIES
col3,col4 = st.columns(2)

top_companies = (
    filtered["company"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_companies.columns=["company","count"]

fig_companies = px.bar(
    top_companies,
    x="count",
    y="company",
    orientation="h",
    title="Top Hiring Companies",
    color="count"
)

col3.plotly_chart(fig_companies,width="stretch")

# TOP LOCATIONS
top_locations = (
    filtered["location"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_locations.columns=["location","count"]

fig_locations = px.bar(
    top_locations,
    x="location",
    y="count",
    title="Top Job Locations",
    color="count"
)

col4.plotly_chart(fig_locations,width="stretch")

# JOB TIMELINE
st.subheader("📈 Job Posting Timeline")

date_counts = (
    filtered["date"]
    .value_counts()
    .reset_index()
)

date_counts.columns=["date","count"]

fig_time = px.line(
    date_counts,
    x="date",
    y="count",
    markers=True
)

st.plotly_chart(fig_time,width="stretch")

# REMOTE VS ONSITE
st.subheader("🌍 Remote vs Onsite")

remote_counts = (
    filtered["work_type"]
    .value_counts()
    .reset_index()
)

remote_counts.columns=["type","count"]

fig_remote = px.pie(
    remote_counts,
    values="count",
    names="type"
)

st.plotly_chart(fig_remote,width="stretch")

# SKILL DISTRIBUTION
st.subheader("🧠 Skill Demand")

skills_series = (
    filtered["skills"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
    .reset_index()
)

skills_series.columns=["skill","count"]

fig_skills = px.bar(
    skills_series,
    x="skill",
    y="count",
    color="skill"
)

st.plotly_chart(fig_skills,width="stretch")

# DATA TABLE
st.subheader("📋 Explore Job Listings")

st.dataframe(
    filtered[["title","company","location","date","job_link"]],
    width="stretch"
)
