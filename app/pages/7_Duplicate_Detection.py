import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_login, show_user_info, is_admin
from queries import fetch_duplicates, delete_opportunity

st.set_page_config(page_title="Duplicate Detection", page_icon="copy", layout="wide")
require_login()
show_user_info()

st.title("Duplicate Detection")
st.markdown("""
Identifies possible duplicate opportunities based on matching:
**Company Name + Job Title + City + Source Link**
""")

try:
    dupes_df = fetch_duplicates()
except Exception as e:
    st.error(f"Error checking duplicates: {e}")
    st.stop()

if dupes_df.empty:
    st.success("No duplicate records detected in the database.")
else:
    st.warning(f"{len(dupes_df)} duplicate group(s) found.")

    for _, row in dupes_df.iterrows():
        with st.expander(f"{row['company_name']} — {row['job_title']} ({row['city']}) — {row['duplicate_count']} copies"):
            st.write(f"**Company:** {row['company_name']}")
            st.write(f"**Job Title:** {row['job_title']}")
            st.write(f"**City:** {row['city']}")
            st.write(f"**Source Link:** {row['source_link']}")
            st.write(f"**Duplicate Count:** {row['duplicate_count']}")
            st.write(f"**Opportunity IDs:** {row['ids']}")

            if is_admin():
                ids_to_remove = row["ids"][1:]  # Keep first, remove rest
                if ids_to_remove:
                    if st.button(f"Remove {len(ids_to_remove)} Duplicate(s) — Keep ID {row['ids'][0]}", key=f"del_{row['ids'][0]}"):
                        removed = 0
                        for dup_id in ids_to_remove:
                            try:
                                delete_opportunity(dup_id)
                                removed += 1
                            except Exception as e:
                                st.error(f"Failed to delete ID {dup_id}: {e}")
                        st.success(f"Removed {removed} duplicate(s).")
                        st.rerun()

st.divider()
st.subheader("Duplicate Detection Logic")
st.info("""
The system detects duplicates by grouping records with identical values in:
1. **company_name** — Same company
2. **job_title** — Same job title
3. **city** — Same location
4. **source_link** — Same application URL

If all four fields match across multiple records, they are flagged as duplicates.
Admins can remove all duplicates while keeping the oldest (first inserted) record.
""")
