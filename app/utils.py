import pandas as pd
import io
import streamlit as st

REQUIRED_CSV_COLUMNS = [
    "company_name", "job_title", "category", "city", "country", "work_mode",
    "required_skills", "salary_min", "salary_max", "currency",
    "experience_level", "application_deadline", "status", "source_link"
]

VALID_WORK_MODES = ["Remote", "Onsite", "Hybrid"]
VALID_STATUSES = ["Open", "Closed", "Expired", "Shortlisted"]
CATEGORIES = ["Data Science", "AI", "Web Development", "Cyber Security", "Software Engineering"]
EXPERIENCE_LEVELS = ["Internship", "Entry Level", "Mid Level", "Senior Level"]
CITIES = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar"]

def validate_csv(df: pd.DataFrame):
    errors = []
    missing = [c for c in REQUIRED_CSV_COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return df, errors

    valid_mask = pd.Series([True] * len(df))

    invalid_mode = ~df["work_mode"].isin(VALID_WORK_MODES)
    if invalid_mode.any():
        errors.append(f"{invalid_mode.sum()} rows have invalid work_mode (must be Remote/Onsite/Hybrid)")
        valid_mask &= ~invalid_mode

    invalid_status = ~df["status"].isin(VALID_STATUSES)
    if invalid_status.any():
        errors.append(f"{invalid_status.sum()} rows have invalid status (must be Open/Closed/Expired/Shortlisted)")
        valid_mask &= ~invalid_status

    empty_company = df["company_name"].isna() | (df["company_name"].str.strip() == "")
    if empty_company.any():
        errors.append(f"{empty_company.sum()} rows have empty company_name")
        valid_mask &= ~empty_company

    empty_title = df["job_title"].isna() | (df["job_title"].str.strip() == "")
    if empty_title.any():
        errors.append(f"{empty_title.sum()} rows have empty job_title")
        valid_mask &= ~empty_title

    return df[valid_mask], errors

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def dataframe_to_records(df: pd.DataFrame) -> list[dict]:
    records = []
    for _, row in df.iterrows():
        rec = {}
        for col in REQUIRED_CSV_COLUMNS:
            val = row.get(col)
            if pd.isna(val) if not isinstance(val, str) else False:
                val = None
            rec[col] = val
        records.append(rec)
    return records

def sample_csv_template() -> bytes:
    sample = pd.DataFrame([{
        "company_name": "Example Corp",
        "job_title": "Software Engineer",
        "category": "Software Engineering",
        "city": "Karachi",
        "country": "Pakistan",
        "work_mode": "Hybrid",
        "required_skills": "Python, Django, PostgreSQL",
        "salary_min": 80000,
        "salary_max": 120000,
        "currency": "PKR",
        "experience_level": "Mid Level",
        "application_deadline": "2026-08-01",
        "status": "Open",
        "source_link": "https://example.com/careers"
    }])
    return df_to_csv_bytes(sample)
