import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_admin, show_user_info
from queries import insert_opportunity, fetch_duplicates
from utils import CATEGORIES, VALID_WORK_MODES, VALID_STATUSES, EXPERIENCE_LEVELS, CITIES
import datetime

st.set_page_config(page_title="Add Opportunity", page_icon="plus", layout="wide")
require_admin()
show_user_info()

st.title("Add New Opportunity")
st.markdown("Fill in the form below to add a new internship or job opportunity to the database.")

def check_potential_duplicate(company, title, city):
    dupes = fetch_duplicates()
    if dupes.empty:
        return False
    for _, row in dupes.iterrows():
        if (row["company_name"].lower() == company.lower() and
                row["job_title"].lower() == title.lower() and
                row["city"].lower() == city.lower()):
            return True
    return False

with st.form("add_opportunity_form", clear_on_submit=True):
    st.subheader("Company Information")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Name *", placeholder="e.g. Systems Ltd")
        city = st.selectbox("City", options=CITIES + ["Other"])
        if city == "Other":
            city = st.text_input("Enter City Name")
    with col2:
        country = st.text_input("Country", value="Pakistan")
        work_mode = st.selectbox("Work Mode *", options=VALID_WORK_MODES)

    st.subheader("Job Details")
    col3, col4 = st.columns(2)
    with col3:
        job_title = st.text_input("Job Title *", placeholder="e.g. Junior Data Scientist")
        category = st.selectbox("Category *", options=CATEGORIES)
        experience_level = st.selectbox("Experience Level", options=EXPERIENCE_LEVELS)
    with col4:
        required_skills = st.text_area("Required Skills *", placeholder="e.g. Python, Pandas, SQL, Machine Learning", height=100)
        source_link = st.text_input("Source Link / Apply URL", placeholder="https://company.com/careers")

    st.subheader("Salary & Timeline")
    col5, col6, col7 = st.columns(3)
    with col5:
        salary_min = st.number_input("Minimum Salary", min_value=0.0, value=0.0, step=1000.0)
    with col6:
        salary_max = st.number_input("Maximum Salary", min_value=0.0, value=0.0, step=1000.0)
    with col7:
        currency = st.selectbox("Currency", options=["PKR", "USD", "EUR", "GBP", "AED"])

    col8, col9 = st.columns(2)
    with col8:
        application_deadline = st.date_input(
            "Application Deadline",
            value=datetime.date.today() + datetime.timedelta(days=30)
        )
    with col9:
        status = st.selectbox("Status", options=VALID_STATUSES, index=0)

    submitted = st.form_submit_button("Add Opportunity", type="primary")

if submitted:
    errors = []
    if not company_name.strip():
        errors.append("Company Name is required.")
    if not job_title.strip():
        errors.append("Job Title is required.")
    if not required_skills.strip():
        errors.append("Required Skills are required.")
    if salary_min and salary_max and salary_min > salary_max:
        errors.append("Minimum salary cannot be greater than maximum salary.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        if check_potential_duplicate(company_name, job_title, city):
            st.warning("A similar opportunity (same company, title, and city) already exists. Proceeding anyway.")

        data = {
            "company_name": company_name.strip(),
            "job_title": job_title.strip(),
            "category": category,
            "city": city,
            "country": country,
            "work_mode": work_mode,
            "required_skills": required_skills.strip(),
            "salary_min": salary_min if salary_min > 0 else None,
            "salary_max": salary_max if salary_max > 0 else None,
            "currency": currency,
            "experience_level": experience_level,
            "application_deadline": application_deadline,
            "status": status,
            "source_link": source_link.strip() if source_link else None,
        }
        try:
            new_id = insert_opportunity(data)
            st.success(f"Opportunity added successfully! ID: {new_id}")
            st.balloons()
        except Exception as e:
            st.error(f"Database error: {e}")
