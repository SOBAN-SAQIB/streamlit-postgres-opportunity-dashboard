import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_login, show_user_info, is_admin
from queries import fetch_filtered, bulk_insert
from utils import validate_csv, df_to_csv_bytes, dataframe_to_records, sample_csv_template, REQUIRED_CSV_COLUMNS

st.set_page_config(page_title="CSV Upload / Export", page_icon="file_folder", layout="wide")
require_login()
show_user_info()

st.title("CSV Upload & Export")

tab_upload, tab_export = st.tabs(["CSV Upload (Bulk Insert)", "CSV Export"])

with tab_upload:
    st.subheader("Upload CSV File")
    if not is_admin():
        st.warning("Only Admin users can upload CSV files.")
    else:
        st.markdown("Upload a CSV file with opportunity data to bulk-insert records into the database.")
        st.info(f"Required columns: {', '.join(REQUIRED_CSV_COLUMNS)}")

        col_dl, _ = st.columns([1, 3])
        with col_dl:
            st.download_button(
                "Download CSV Template",
                data=sample_csv_template(),
                file_name="opportunities_template.csv",
                mime="text/csv"
            )

        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file:
            try:
                df_raw = pd.read_csv(uploaded_file)
                st.markdown(f"**Uploaded:** {len(df_raw)} rows, {len(df_raw.columns)} columns")
                st.dataframe(df_raw.head(10), use_container_width=True)

                valid_df, errors = validate_csv(df_raw)

                if errors:
                    st.subheader("Validation Issues")
                    for err in errors:
                        st.warning(err)

                if valid_df.empty:
                    st.error("No valid rows to insert after validation.")
                else:
                    st.success(f"{len(valid_df)} valid rows ready to insert.")
                    st.dataframe(valid_df, use_container_width=True)

                    if st.button("Insert Valid Rows into Database", type="primary"):
                        records = dataframe_to_records(valid_df)
                        inserted, skipped = bulk_insert(records)
                        st.success(f"Inserted: {inserted} records")
                        if skipped:
                            st.warning(f"Skipped (errors): {skipped} records")

            except Exception as e:
                st.error(f"Error reading CSV: {e}")

with tab_export:
    st.subheader("Export Filtered Data as CSV")
    st.markdown("Apply filters below and download the results.")

    col1, col2, col3 = st.columns(3)
    with col1:
        exp_category = st.selectbox("Category", ["All", "Data Science", "AI", "Web Development", "Cyber Security", "Software Engineering"], key="exp_cat")
    with col2:
        exp_status = st.selectbox("Status", ["All", "Open", "Closed", "Expired", "Shortlisted"], key="exp_status")
    with col3:
        exp_work_mode = st.selectbox("Work Mode", ["All", "Remote", "Onsite", "Hybrid"], key="exp_mode")

    export_params = {}
    if exp_category != "All":
        export_params["category"] = exp_category
    if exp_status != "All":
        export_params["status"] = exp_status
    if exp_work_mode != "All":
        export_params["work_mode"] = exp_work_mode

    try:
        df_export = fetch_filtered(**export_params)
        st.markdown(f"**{len(df_export)} records** match the selected filters.")
        if not df_export.empty:
            st.dataframe(df_export.head(20), use_container_width=True)
            csv_bytes = df_to_csv_bytes(df_export)
            st.download_button(
                label=f"Download {len(df_export)} Records as CSV",
                data=csv_bytes,
                file_name=f"opportunities_export_{exp_category}_{exp_status}.csv",
                mime="text/csv",
                type="primary"
            )
    except Exception as e:
        st.error(f"Error fetching data: {e}")
