import os
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_db_url():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "student_opportunities_db")
    user = os.getenv("DB_USER", "app_user")
    password = os.getenv("DB_PASSWORD", "app_password")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

@st.cache_resource
def get_engine():
    return create_engine(get_db_url(), pool_pre_ping=True)

def get_connection():
    return get_engine().connect()

def test_connection():
    try:
        with get_connection() as conn:
            result = conn.execute(text("SELECT version()"))
            return True, result.fetchone()[0]
    except Exception as e:
        return False, str(e)
