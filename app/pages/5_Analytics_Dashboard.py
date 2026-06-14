import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_login, show_user_info
from queries import get_analytics_data, count_rows, fetch_all
import pandas as pd

st.set_page_config(page_title="Analytics Dashboard", page_icon="chart_bar", layout="wide")
require_login()
show_user_info()

st.title("Analytics Dashboard")
st.markdown("Comprehensive insights and trends from the opportunities database.")

try:
    data = get_analytics_data()
    total = count_rows()
    df_all = fetch_all()
except Exception as e:
    st.error(f"Error loading analytics: {e}")
    st.stop()

# KPIs
st.subheader("Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1:
    st.metric("Total Opportunities", total)
with kpi2:
    open_count = len(df_all[df_all["status"] == "Open"]) if not df_all.empty else 0
    st.metric("Open Positions", open_count)
with kpi3:
    shortlisted = len(df_all[df_all["status"] == "Shortlisted"]) if not df_all.empty else 0
    st.metric("Shortlisted", shortlisted)
with kpi4:
    remote_count = len(df_all[df_all["work_mode"] == "Remote"]) if not df_all.empty else 0
    st.metric("Remote Jobs", remote_count)
with kpi5:
    intern_count = len(df_all[df_all["experience_level"] == "Internship"]) if not df_all.empty else 0
    st.metric("Internships", intern_count)
with kpi6:
    companies = df_all["company_name"].nunique() if not df_all.empty else 0
    st.metric("Companies", companies)

st.divider()

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Opportunities by Category")
    if not data["category"].empty:
        fig = px.pie(
            data["category"], names="category", values="count",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Opportunities by Status")
    if not data["status"].empty:
        color_map = {"Open": "#2ecc71", "Closed": "#e74c3c", "Expired": "#95a5a6", "Shortlisted": "#f39c12"}
        fig = px.bar(
            data["status"], x="status", y="count",
            color="status", color_discrete_map=color_map,
            text="count"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Status", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

# Charts Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Work Mode Distribution")
    if not data["work_mode"].empty:
        fig = px.pie(
            data["work_mode"], names="work_mode", values="count",
            color_discrete_sequence=["#3498db", "#e67e22", "#9b59b6"],
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Opportunities by City")
    if not data["city"].empty:
        fig = px.bar(
            data["city"], x="count", y="city", orientation="h",
            color="count", color_continuous_scale="Blues",
            text="count"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# Charts Row 3
col5, col6 = st.columns(2)

with col5:
    st.subheader("Average Salary by Category (PKR)")
    if not data["salary"].empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Avg Min Salary",
            x=data["salary"]["category"],
            y=data["salary"]["avg_min"],
            marker_color="#3498db"
        ))
        fig.add_trace(go.Bar(
            name="Avg Max Salary",
            x=data["salary"]["category"],
            y=data["salary"]["avg_max"],
            marker_color="#2ecc71"
        ))
        fig.update_layout(barmode="group", xaxis_title="Category", yaxis_title="Salary (PKR)")
        st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Experience Level Breakdown")
    if not data["experience"].empty:
        fig = px.bar(
            data["experience"], x="experience_level", y="count",
            color="experience_level",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text="count"
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Experience Level", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

# Chart Row 4 — Monthly trend
st.subheader("Monthly Posting Trend")
if not data["monthly"].empty:
    fig = px.line(
        data["monthly"], x="month", y="count",
        markers=True, line_shape="spline",
        color_discrete_sequence=["#e74c3c"]
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Opportunities Posted")
    st.plotly_chart(fig, use_container_width=True)

# Skills word frequency
st.subheader("Most In-Demand Skills")
if not df_all.empty:
    all_skills = " ".join(df_all["required_skills"].dropna().tolist()).split(", ")
    skill_counts = pd.Series(all_skills).value_counts().head(20).reset_index()
    skill_counts.columns = ["skill", "count"]
    fig = px.bar(
        skill_counts, x="count", y="skill", orientation="h",
        color="count", color_continuous_scale="Viridis", text="count"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False,
                      xaxis_title="Frequency", yaxis_title="Skill")
    st.plotly_chart(fig, use_container_width=True)
