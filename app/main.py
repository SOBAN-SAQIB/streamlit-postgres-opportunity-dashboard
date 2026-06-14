import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from auth import require_login, show_user_info, login_form
from db import test_connection

st.set_page_config(
    page_title="Internship & Job Tracking Dashboard",
    page_icon="briefcase",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

if not st.session_state.get("logged_in"):
    login_form()
    st.stop()

show_user_info()

st.title("Internship & Job Tracking Dashboard")
st.markdown("### University Department Opportunity Management System")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Project:** Internship & Job Tracking Dashboard")
with col2:
    st.info("**Database:** PostgreSQL via Docker")
with col3:
    db_ok, msg = test_connection()
    if db_ok:
        st.success("Database: Connected")
    else:
        st.error("Database: Disconnected")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Team Members")
    st.markdown("""
    | Name | Role |
    |------|------|
    | Soban | Database Developer |
    | Ahmed | CRUD + Authentication |
    | Adil | Analytics + Deployment |
    """)

with col_right:
    st.subheader("Tools Used")
    st.markdown("""
    - **Streamlit** — Web application framework
    - **PostgreSQL** — Relational database
    - **pgAdmin** — Database administration
    - **Docker Compose** — Multi-container deployment
    - **Python** — Application language
    - **Plotly** — Interactive charts
    - **SQLAlchemy / psycopg2** — Database connectivity
    - **Pandas** — Data processing
    """)

st.divider()

st.subheader("Application Guide")
tabs = st.tabs([
    "Navigation", "Add Opportunities", "View & Search",
    "Analytics", "CSV Features", "Admin Tools"
])

with tabs[0]:
    st.markdown("""
    Use the **sidebar** to navigate between pages. Your role determines what actions are available:
    - **Admin**: Full access — add, edit, delete, upload CSV, manage records
    - **Viewer**: Read-only access — view records, search, and explore analytics
    """)
with tabs[1]:
    st.markdown("""
    Go to **Add New Opportunity** to insert internship or job postings with full validation.
    Fill in company details, job info, salary range, and deadline.
    """)
with tabs[2]:
    st.markdown("""
    **View & Search** lets you browse all records, apply filters (category, city, work mode,
    status, salary range, experience level), and perform text search.
    """)
with tabs[3]:
    st.markdown("""
    **Analytics Dashboard** displays KPIs, charts by category, work mode, salary ranges,
    top cities, experience level distribution, and monthly posting trends.
    """)
with tabs[4]:
    st.markdown("""
    **CSV Upload** imports bulk records from a CSV file with validation and preview.
    **CSV Export** lets you download filtered results for external reporting.
    """)
with tabs[5]:
    st.markdown("""
    Admin tools include **Duplicate Detection**, **Deadline Alerts**, **Update/Delete** records,
    and a **Database Health Check** to verify the PostgreSQL connection.
    """)

st.divider()

st.subheader("System Architecture")
st.code("""
User Browser
    |
    v
Streamlit App Container (port 8501)
    |
    v
PostgreSQL Container (port 5432)  <---->  pgAdmin Container (port 5050)
    |
    v
Docker Named Volume (postgres_data) — Persistent Storage

GitHub Repository — Source code, commits, documentation
""", language="text")