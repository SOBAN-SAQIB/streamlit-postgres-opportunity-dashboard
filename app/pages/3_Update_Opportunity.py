import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_admin, show_user_info
from queries import fetch_all, fetch_by_id, update_opportunity
from utils import VALID_WORK_MODES, VALID_STATUSES, CATEGORIES, EXPERIENCE_LEVELS
import datetime

st.set_page_config(page_title="Update Opportunity", page_icon="pencil", layout="wide")
require_admin()
show_user_info()

st.title("Update Opportunity")
st.markdown("Select a record to update its details.")

try:
    df = fetch_all()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if df.empty:
    st.info("No opportunities in the database.")
    st.stop()

options = {f"[{row['opportunity_id']}] {row['company_name']} — {row['job_title']}": row["opportunity_id"]
           for _, row in df.iterrows()}

selected_label = st.selectbox("Select Opportunity to Update", list(options.keys()))
selected_id = options[selected_label]

record = fetch_by_id(selected_id)
if not record:
    st.error("Record not found.")
    st.stop()

st.subheader("Current Record")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.write(f"**Company:** {record['company_name']}")
    st.write(f"**Job Title:** {record['job_title']}")
    st.write(f"**Category:** {record['category']}")
with col_b:
    st.write(f"**Status:** {record['status']}")
    st.write(f"**Work Mode:** {record['work_mode']}")
    st.write(f"**City:** {record['city']}")
with col_c:
    st.write(f"**Deadline:** {record['application_deadline']}")
    st.write(f"**Salary:** {record['salary_min']} - {record['salary_max']}")
    st.write(f"**Experience:** {record['experience_level']}")

st.divider()
st.subheader("Edit Fields")

with st.form("update_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_status = st.selectbox(
            "Status",
            VALID_STATUSES,
            index=VALID_STATUSES.index(record["status"]) if record["status"] in VALID_STATUSES else 0
        )
        new_work_mode = st.selectbox(
            "Work Mode",
            VALID_WORK_MODES,
            index=VALID_WORK_MODES.index(record["work_mode"]) if record["work_mode"] in VALID_WORK_MODES else 0
        )
        new_experience = st.selectbox(
            "Experience Level",
            EXPERIENCE_LEVELS,
            index=EXPERIENCE_LEVELS.index(record["experience_level"]) if record["experience_level"] in EXPERIENCE_LEVELS else 0
        )
    with col2:
        deadline_val = record["application_deadline"]
        if isinstance(deadline_val, str):
            deadline_val = datetime.date.fromisoformat(deadline_val)
        elif deadline_val is None:
            deadline_val = datetime.date.today()
        new_deadline = st.date_input("Application Deadline", value=deadline_val)
        new_salary_min = st.number_input("Minimum Salary", value=float(record["salary_min"] or 0), step=1000.0)
        new_salary_max = st.number_input("Maximum Salary", value=float(record["salary_max"] or 0), step=1000.0)

    new_skills = st.text_area("Required Skills", value=record["required_skills"] or "", height=100)
    new_source = st.text_input("Source Link", value=record["source_link"] or "")

    submitted = st.form_submit_button("Save Changes", type="primary")

if submitted:
    errors = []
    if new_salary_min and new_salary_max and new_salary_min > new_salary_max:
        errors.append("Minimum salary cannot exceed maximum salary.")
    if not new_skills.strip():
        errors.append("Required Skills cannot be empty.")
    if errors:
        for err in errors:
            st.error(err)
    else:
        update_data = {
            "status": new_status,
            "work_mode": new_work_mode,
            "experience_level": new_experience,
            "application_deadline": new_deadline,
            "salary_min": new_salary_min if new_salary_min > 0 else None,
            "salary_max": new_salary_max if new_salary_max > 0 else None,
            "required_skills": new_skills.strip(),
            "source_link": new_source.strip() if new_source else None,
        }
        try:
            update_opportunity(selected_id, update_data)
            st.success(f"Opportunity ID {selected_id} updated successfully!")
        except Exception as e:
            st.error(f"Update failed: {e}")
