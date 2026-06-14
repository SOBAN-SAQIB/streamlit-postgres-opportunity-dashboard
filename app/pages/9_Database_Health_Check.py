import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_login, show_user_info
from db import test_connection, get_engine
from queries import count_rows, get_latest_record, get_table_columns
from sqlalchemy import text
import datetime

st.set_page_config(page_title="Database Health Check", page_icon="database", layout="wide")
require_login()
show_user_info()

st.title("Database Health Check")
st.markdown("Monitor the PostgreSQL connection, table status, and database metadata.")

col_refresh, _ = st.columns([1, 5])
with col_refresh:
    if st.button("Refresh Health Check", type="primary"):
        st.rerun()

st.divider()

# Connection test
st.subheader("Connection Status")
db_ok, version_or_error = test_connection()

if db_ok:
    st.success("Database connection is healthy.")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**PostgreSQL Version:** {version_or_error}")
    with col2:
        st.info(f"**Checked at:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.error(f"Database connection FAILED: {version_or_error}")
    st.markdown("**Troubleshooting Tips:**")
    st.markdown("""
    - Verify Docker containers are running: `docker compose ps`
    - Check PostgreSQL logs: `docker compose logs postgres_db`
    - Verify environment variables (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
    - Ensure the postgres_db service is healthy before the streamlit_app starts
    """)
    st.stop()

st.divider()

# Row count
st.subheader("Table Statistics")
try:
    row_count = count_rows()
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total Rows in opportunities", row_count)
    with col_b:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT pg_database_size(current_database())"))
            db_size = result.fetchone()[0]
        st.metric("Database Size (bytes)", f"{db_size:,}")
    with col_c:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT pg_size_pretty(pg_total_relation_size('opportunities'))"))
            table_size = result.fetchone()[0]
        st.metric("Table Size", table_size)
except Exception as e:
    st.error(f"Error fetching stats: {e}")

st.divider()

# Latest record
st.subheader("Latest Record")
try:
    latest = get_latest_record()
    if latest:
        col_x, col_y = st.columns(2)
        with col_x:
            st.write(f"**ID:** {latest['opportunity_id']}")
            st.write(f"**Company:** {latest['company_name']}")
            st.write(f"**Job Title:** {latest['job_title']}")
            st.write(f"**Status:** {latest['status']}")
        with col_y:
            st.write(f"**Category:** {latest['category']}")
            st.write(f"**City:** {latest['city']}")
            st.write(f"**Created At:** {latest['created_at']}")
    else:
        st.info("No records found in the opportunities table.")
except Exception as e:
    st.error(f"Error fetching latest record: {e}")

st.divider()

# Table columns
st.subheader("Table Schema — opportunities")
try:
    cols_df = get_table_columns()
    st.dataframe(cols_df, use_container_width=True)
except Exception as e:
    st.error(f"Error fetching schema: {e}")

st.divider()

# Manual SQL runner (admin educational view)
st.subheader("Quick SQL Queries")
st.markdown("Run predefined verification queries against the database.")

queries = {
    "Count all records": "SELECT COUNT(*) FROM opportunities",
    "Records by category": "SELECT category, COUNT(*) as count FROM opportunities GROUP BY category ORDER BY count DESC",
    "Records by work mode": "SELECT work_mode, COUNT(*) as count FROM opportunities GROUP BY work_mode ORDER BY count DESC",
    "Open opportunities": "SELECT * FROM opportunities WHERE status = 'Open' LIMIT 10",
    "Closing within 7 days": "SELECT company_name, job_title, application_deadline FROM opportunities WHERE application_deadline <= CURRENT_DATE + INTERVAL '7 days' AND status = 'Open'",
    "Recent 5 inserts": "SELECT opportunity_id, company_name, job_title, created_at FROM opportunities ORDER BY created_at DESC LIMIT 5",
}

selected_query = st.selectbox("Select a query to run", list(queries.keys()))
if st.button("Run Query"):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(queries[selected_query]))
            rows = result.fetchall()
            keys = result.keys()
        import pandas as pd
        df_result = pd.DataFrame(rows, columns=list(keys))
        st.dataframe(df_result, use_container_width=True)
        st.code(queries[selected_query], language="sql")
    except Exception as e:
        st.error(f"Query failed: {e}")
