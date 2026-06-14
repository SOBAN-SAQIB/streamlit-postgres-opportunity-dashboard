import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_login, show_user_info
from queries import fetch_filtered
from utils import CATEGORIES, VALID_WORK_MODES, VALID_STATUSES, EXPERIENCE_LEVELS, CITIES, df_to_csv_bytes
import pandas as pd

st.set_page_config(page_title="View & Search", page_icon="search", layout="wide")
require_login()
show_user_info()

st.title("View & Search Opportunities")

with st.sidebar:
    st.header("Filters")
    search_text = st.text_input("Search (company/title/skills)", "")
    selected_category = st.selectbox("Category", ["All"] + CATEGORIES)
    selected_city = st.selectbox("City", ["All"] + CITIES + ["Other"])
    selected_work_mode = st.selectbox("Work Mode", ["All"] + VALID_WORK_MODES)
    selected_status = st.selectbox("Status", ["All"] + VALID_STATUSES)
    selected_exp = st.selectbox("Experience Level", ["All", "Internship", "Entry Level", "Mid Level", "Senior Level"])
    st.markdown("**Salary Range (PKR)**")
    salary_min_filter = st.number_input("Min Salary", min_value=0, value=0, step=5000)
    salary_max_filter = st.number_input("Max Salary", min_value=0, value=0, step=5000)
    apply_filters = st.button("Apply Filters", type="primary")
    reset = st.button("Reset Filters")

if reset:
    st.rerun()

params = {}
if selected_category != "All":
    params["category"] = selected_category
if selected_city != "All":
    params["city"] = selected_city
if selected_work_mode != "All":
    params["work_mode"] = selected_work_mode
if selected_status != "All":
    params["status"] = selected_status
if selected_exp != "All":
    params["experience_level"] = selected_exp
if salary_min_filter > 0:
    params["salary_min"] = salary_min_filter
if salary_max_filter > 0:
    params["salary_max"] = salary_max_filter
if search_text.strip():
    params["search_text"] = search_text.strip()

try:
    df = fetch_filtered(**params)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.markdown(f"**{len(df)} records found**")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", len(df))
with col2:
    open_count = len(df[df["status"] == "Open"]) if not df.empty else 0
    st.metric("Open", open_count)
with col3:
    shortlisted = len(df[df["status"] == "Shortlisted"]) if not df.empty else 0
    st.metric("Shortlisted", shortlisted)
with col4:
    expired = len(df[df["status"] == "Expired"]) if not df.empty else 0
    st.metric("Expired", expired)

st.divider()

if df.empty:
    st.info("No records match the selected filters.")
else:
    display_cols = ["opportunity_id", "company_name", "job_title", "category", "city",
                    "work_mode", "experience_level", "salary_min", "salary_max",
                    "currency", "status", "application_deadline"]
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        column_config={
            "opportunity_id": st.column_config.NumberColumn("ID", width="small"),
            "company_name": st.column_config.TextColumn("Company"),
            "job_title": st.column_config.TextColumn("Job Title"),
            "category": st.column_config.TextColumn("Category"),
            "city": st.column_config.TextColumn("City"),
            "work_mode": st.column_config.TextColumn("Mode"),
            "experience_level": st.column_config.TextColumn("Experience"),
            "salary_min": st.column_config.NumberColumn("Salary Min", format="%.0f"),
            "salary_max": st.column_config.NumberColumn("Salary Max", format="%.0f"),
            "currency": st.column_config.TextColumn("Currency", width="small"),
            "status": st.column_config.TextColumn("Status"),
            "application_deadline": st.column_config.DateColumn("Deadline"),
        }
    )

    st.divider()
    st.subheader("Record Details")
    selected_id = st.selectbox("Select Opportunity ID to view full details", df["opportunity_id"].tolist())
    if selected_id:
        rec = df[df["opportunity_id"] == selected_id].iloc[0]
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**Company:** {rec['company_name']}")
            st.write(f"**Job Title:** {rec['job_title']}")
            st.write(f"**Category:** {rec['category']}")
            st.write(f"**City:** {rec['city']}, {rec['country']}")
            st.write(f"**Work Mode:** {rec['work_mode']}")
            st.write(f"**Experience Level:** {rec['experience_level']}")
        with col_b:
            st.write(f"**Salary:** {rec['salary_min']} - {rec['salary_max']} {rec['currency']}")
            st.write(f"**Status:** {rec['status']}")
            st.write(f"**Deadline:** {rec['application_deadline']}")
            st.write(f"**Skills:** {rec['required_skills']}")
            if rec["source_link"]:
                st.write(f"**Apply:** {rec['source_link']}")
            st.write(f"**Posted:** {rec['created_at']}")

    st.divider()
    csv_bytes = df_to_csv_bytes(df)
    st.download_button(
        label="Export Current View as CSV",
        data=csv_bytes,
        file_name="opportunities_export.csv",
        mime="text/csv"
    )
