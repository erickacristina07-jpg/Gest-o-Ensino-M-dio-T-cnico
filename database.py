"""Persistência SQLite. O banco é criado automaticamente na primeira execução."""
import sqlite3
from pathlib import Path

DB_PATH = Path("data/gestao_senac.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date TEXT NOT NULL,
            campus TEXT NOT NULL,
            indicator TEXT NOT NULL,
            category TEXT NOT NULL,
            series TEXT,
            status TEXT NOT NULL,
            value REAL NOT NULL CHECK(value >= 0),
            unit TEXT NOT NULL,
            source TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_records_date ON records(record_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_records_campus ON records(campus)")

def insert_record(data):
    fields = ["record_date","campus","indicator","category","series","status","value","unit","source","notes"]
    with get_connection() as conn:
        conn.execute(
            f"INSERT INTO records ({','.join(fields)}) VALUES ({','.join(['?']*len(fields))})",
            [data.get(field) for field in fields]
        )

def fetch_records():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM records ORDER BY record_date DESC, id DESC").fetchall()
    return [dict(row) for row in rows]

def update_record(record_id, data):
    fields = ["record_date","campus","indicator","category","series","status","value","unit","source","notes"]
    assignments = ", ".join(f"{field}=?" for field in fields)
    with get_connection() as conn:
        conn.execute(f"UPDATE records SET {assignments} WHERE id=?", [data.get(field) for field in fields] + [record_id])

def delete_record(record_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM records WHERE id=?", [record_id])
