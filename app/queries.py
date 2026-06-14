import pandas as pd
from sqlalchemy import text
from db import get_connection

COLUMNS = [
    "opportunity_id", "company_name", "job_title", "category", "city", "country",
    "work_mode", "required_skills", "salary_min", "salary_max", "currency",
    "experience_level", "application_deadline", "status", "source_link", "created_at"
]

def fetch_all():
    with get_connection() as conn:
        result = conn.execute(text("SELECT * FROM opportunities ORDER BY created_at DESC"))
        return pd.DataFrame(result.fetchall(), columns=COLUMNS)

def fetch_filtered(category=None, city=None, work_mode=None, status=None,
                   salary_min=None, salary_max=None, experience_level=None, search_text=None):
    conditions = []
    params = {}
    if category:
        conditions.append("category = :category")
        params["category"] = category
    if city:
        conditions.append("city = :city")
        params["city"] = city
    if work_mode:
        conditions.append("work_mode = :work_mode")
        params["work_mode"] = work_mode
    if status:
        conditions.append("status = :status")
        params["status"] = status
    if salary_min is not None:
        conditions.append("salary_min >= :salary_min")
        params["salary_min"] = salary_min
    if salary_max is not None:
        conditions.append("salary_max <= :salary_max")
        params["salary_max"] = salary_max
    if experience_level:
        conditions.append("experience_level = :experience_level")
        params["experience_level"] = experience_level
    if search_text:
        conditions.append(
            "(company_name ILIKE :search OR job_title ILIKE :search OR required_skills ILIKE :search)"
        )
        params["search"] = f"%{search_text}%"

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"SELECT * FROM opportunities {where} ORDER BY created_at DESC"
    with get_connection() as conn:
        result = conn.execute(text(sql), params)
        return pd.DataFrame(result.fetchall(), columns=COLUMNS)

def insert_opportunity(data: dict):
    sql = text("""
        INSERT INTO opportunities (
            company_name, job_title, category, city, country, work_mode,
            required_skills, salary_min, salary_max, currency,
            experience_level, application_deadline, status, source_link
        ) VALUES (
            :company_name, :job_title, :category, :city, :country, :work_mode,
            :required_skills, :salary_min, :salary_max, :currency,
            :experience_level, :application_deadline, :status, :source_link
        ) RETURNING opportunity_id
    """)
    with get_connection() as conn:
        result = conn.execute(sql, data)
        conn.commit()
        return result.fetchone()[0]

def update_opportunity(opportunity_id: int, data: dict):
    set_clauses = ", ".join([f"{k} = :{k}" for k in data.keys()])
    sql = text(f"UPDATE opportunities SET {set_clauses} WHERE opportunity_id = :opportunity_id")
    data["opportunity_id"] = opportunity_id
    with get_connection() as conn:
        conn.execute(sql, data)
        conn.commit()

def delete_opportunity(opportunity_id: int):
    with get_connection() as conn:
        conn.execute(text("DELETE FROM opportunities WHERE opportunity_id = :id"), {"id": opportunity_id})
        conn.commit()

def fetch_by_id(opportunity_id: int):
    with get_connection() as conn:
        result = conn.execute(
            text("SELECT * FROM opportunities WHERE opportunity_id = :id"),
            {"id": opportunity_id}
        )
        row = result.fetchone()
        if row:
            return dict(zip(COLUMNS, row))
        return None

def fetch_duplicates():
    sql = text("""
        SELECT company_name, job_title, city, source_link, COUNT(*) as duplicate_count,
               array_agg(opportunity_id) as ids
        FROM opportunities
        GROUP BY company_name, job_title, city, source_link
        HAVING COUNT(*) > 1
        ORDER BY duplicate_count DESC
    """)
    with get_connection() as conn:
        result = conn.execute(sql)
        rows = result.fetchall()
        return pd.DataFrame(rows, columns=["company_name", "job_title", "city", "source_link", "duplicate_count", "ids"])

def fetch_deadline_alerts():
    sql = text("""
        SELECT * FROM opportunities
        WHERE application_deadline BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
        AND status = 'Open'
        ORDER BY application_deadline ASC
    """)
    expired_sql = text("""
        SELECT * FROM opportunities
        WHERE application_deadline < CURRENT_DATE OR status = 'Expired'
        ORDER BY application_deadline DESC
    """)
    with get_connection() as conn:
        soon = pd.DataFrame(conn.execute(sql).fetchall(), columns=COLUMNS)
        expired = pd.DataFrame(conn.execute(expired_sql).fetchall(), columns=COLUMNS)
    return soon, expired

def count_rows():
    with get_connection() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM opportunities"))
        return result.fetchone()[0]

def get_latest_record():
    with get_connection() as conn:
        result = conn.execute(text("SELECT * FROM opportunities ORDER BY created_at DESC LIMIT 1"))
        row = result.fetchone()
        if row:
            return dict(zip(COLUMNS, row))
        return None

def get_table_columns():
    sql = text("""
        SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'opportunities'
        ORDER BY ordinal_position
    """)
    with get_connection() as conn:
        result = conn.execute(sql)
        return pd.DataFrame(result.fetchall(), columns=["Column", "Type", "Max Length", "Nullable", "Default"])

def bulk_insert(records: list[dict]):
    inserted = 0
    skipped = 0
    for rec in records:
        try:
            insert_opportunity(rec)
            inserted += 1
        except Exception:
            skipped += 1
    return inserted, skipped

def get_analytics_data():
    with get_connection() as conn:
        category_counts = pd.DataFrame(
            conn.execute(text("SELECT category, COUNT(*) as count FROM opportunities GROUP BY category ORDER BY count DESC")).fetchall(),
            columns=["category", "count"]
        )
        status_counts = pd.DataFrame(
            conn.execute(text("SELECT status, COUNT(*) as count FROM opportunities GROUP BY status ORDER BY count DESC")).fetchall(),
            columns=["status", "count"]
        )
        work_mode_counts = pd.DataFrame(
            conn.execute(text("SELECT work_mode, COUNT(*) as count FROM opportunities GROUP BY work_mode ORDER BY count DESC")).fetchall(),
            columns=["work_mode", "count"]
        )
        city_counts = pd.DataFrame(
            conn.execute(text("SELECT city, COUNT(*) as count FROM opportunities GROUP BY city ORDER BY count DESC")).fetchall(),
            columns=["city", "count"]
        )
        salary_data = pd.DataFrame(
            conn.execute(text("SELECT category, AVG(salary_min) as avg_min, AVG(salary_max) as avg_max FROM opportunities WHERE salary_min IS NOT NULL GROUP BY category")).fetchall(),
            columns=["category", "avg_min", "avg_max"]
        )
        monthly_data = pd.DataFrame(
            conn.execute(text("SELECT TO_CHAR(created_at, 'YYYY-MM') as month, COUNT(*) as count FROM opportunities GROUP BY month ORDER BY month")).fetchall(),
            columns=["month", "count"]
        )
        experience_counts = pd.DataFrame(
            conn.execute(text("SELECT experience_level, COUNT(*) as count FROM opportunities GROUP BY experience_level ORDER BY count DESC")).fetchall(),
            columns=["experience_level", "count"]
        )
    return {
        "category": category_counts,
        "status": status_counts,
        "work_mode": work_mode_counts,
        "city": city_counts,
        "salary": salary_data,
        "monthly": monthly_data,
        "experience": experience_counts,
    }
