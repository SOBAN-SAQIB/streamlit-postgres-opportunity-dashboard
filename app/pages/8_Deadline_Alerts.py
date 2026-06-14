import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_login, show_user_info
from queries import fetch_deadline_alerts
import datetime

st.set_page_config(page_title="Deadline Alerts", page_icon="bell", layout="wide")
require_login()
show_user_info()

st.title("Deadline Alerts")
st.markdown(f"Today: **{datetime.date.today()}**")

try:
    closing_soon, expired = fetch_deadline_alerts()
except Exception as e:
    st.error(f"Error loading deadline data: {e}")
    st.stop()

tab1, tab2 = st.tabs([
    f"Closing Within 7 Days ({len(closing_soon)})",
    f"Expired / Closed ({len(expired)})"
])

with tab1:
    st.subheader("Opportunities Closing Soon")
    if closing_soon.empty:
        st.success("No opportunities closing within the next 7 days.")
    else:
        st.warning(f"{len(closing_soon)} opportunity/opportunities closing within 7 days!")
        display_cols = ["opportunity_id", "company_name", "job_title", "category",
                        "city", "work_mode", "status", "application_deadline"]
        st.dataframe(
            closing_soon[display_cols],
            use_container_width=True,
            column_config={
                "application_deadline": st.column_config.DateColumn("Deadline", format="YYYY-MM-DD"),
                "opportunity_id": st.column_config.NumberColumn("ID", width="small"),
            }
        )
        for _, row in closing_soon.iterrows():
            deadline = row["application_deadline"]
            if hasattr(deadline, "date"):
                deadline = deadline.date()
            days_left = (deadline - datetime.date.today()).days
            label = "TODAY" if days_left == 0 else f"{days_left} day(s) left"
            st.info(f"**{row['company_name']}** — {row['job_title']} | Deadline: {deadline} | {label}")

with tab2:
    st.subheader("Expired and Closed Opportunities")
    if expired.empty:
        st.success("No expired or closed opportunities found.")
    else:
        st.error(f"{len(expired)} expired or closed opportunity/opportunities found.")
        display_cols = ["opportunity_id", "company_name", "job_title", "category",
                        "city", "status", "application_deadline"]
        st.dataframe(
            expired[display_cols],
            use_container_width=True,
            column_config={
                "application_deadline": st.column_config.DateColumn("Deadline", format="YYYY-MM-DD"),
                "opportunity_id": st.column_config.NumberColumn("ID", width="small"),
            }
        )
