import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_admin, show_user_info
from queries import fetch_all, fetch_by_id, delete_opportunity

st.set_page_config(page_title="Delete Opportunity", page_icon="trash", layout="wide")
require_admin()
show_user_info()

st.title("Delete Opportunity")
st.warning("This action is permanent and cannot be undone.")

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

selected_label = st.selectbox("Select Opportunity to Delete", list(options.keys()))
selected_id = options[selected_label]

record = fetch_by_id(selected_id)
if not record:
    st.error("Record not found.")
    st.stop()

st.subheader("Record Preview")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**ID:** {record['opportunity_id']}")
    st.write(f"**Company:** {record['company_name']}")
    st.write(f"**Job Title:** {record['job_title']}")
    st.write(f"**Category:** {record['category']}")
    st.write(f"**City:** {record['city']}, {record['country']}")
with col2:
    st.write(f"**Work Mode:** {record['work_mode']}")
    st.write(f"**Status:** {record['status']}")
    st.write(f"**Deadline:** {record['application_deadline']}")
    st.write(f"**Salary:** {record['salary_min']} - {record['salary_max']} {record['currency']}")
    st.write(f"**Skills:** {record['required_skills']}")

st.divider()
st.error(f"You are about to permanently delete: **{record['company_name']} — {record['job_title']}**")

confirm = st.checkbox("I confirm I want to delete this record permanently.")

if confirm:
    if st.button("Delete Record", type="primary"):
        try:
            delete_opportunity(selected_id)
            st.success(f"Record ID {selected_id} has been deleted.")
            st.rerun()
        except Exception as e:
            st.error(f"Deletion failed: {e}")
else:
    st.info("Check the confirmation box to enable the delete button.")
