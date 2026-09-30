import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "jobs.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            status TEXT NOT NULL DEFAULT 'Applied',
            source TEXT NOT NULL DEFAULT 'Other',
            applied_date TEXT NOT NULL,
            job_url TEXT,
            salary TEXT,
            follow_up TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def add_application(company, role, location, status, source, applied_date, job_url, salary, follow_up, notes):
    with connect() as conn:
        conn.execute("""INSERT INTO applications
        (company,role,location,status,source,applied_date,job_url,salary,follow_up,notes)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (company.strip(),role.strip(),location,status,source,str(applied_date),job_url,salary,str(follow_up) if follow_up else None,notes))
        conn.commit()

def update_application(app_id, company, role, location, status, source, applied_date, job_url, salary, follow_up, notes):
    with connect() as conn:
        conn.execute("""UPDATE applications SET company=?,role=?,location=?,status=?,source=?,
        applied_date=?,job_url=?,salary=?,follow_up=?,notes=?,updated_at=CURRENT_TIMESTAMP WHERE id=?""",
        (company.strip(),role.strip(),location,status,source,str(applied_date),job_url,salary,str(follow_up) if follow_up else None,notes,app_id))
        conn.commit()

def delete_application(app_id):
    with connect() as conn:
        conn.execute("DELETE FROM applications WHERE id=?", (app_id,))
        conn.commit()

def fetch_applications():
    with connect() as conn:
        return pd.read_sql_query("SELECT * FROM applications", conn)

def get_application(app_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM applications WHERE id=?", (app_id,)).fetchone()
        return dict(row) if row else None
