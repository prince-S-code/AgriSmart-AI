import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "agrismart.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        mobile_number TEXT,
        password_hash TEXT NOT NULL,
        state TEXT,
        district TEXT,
        village TEXT,
        preferred_language TEXT DEFAULT 'en',
        role TEXT DEFAULT 'farmer',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS disease_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_name TEXT,
        crop_name TEXT,
        predicted_disease TEXT,
        confidence REAL,
        model_used TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS crop_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nitrogen REAL NOT NULL,
        phosphorus REAL NOT NULL,
        potassium REAL NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        ph REAL NOT NULL,
        rainfall REAL NOT NULL,
        recommended_crop TEXT NOT NULL,
        alternatives TEXT,
        model_used TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()

    conn = get_db()
    def columns(table):
        return {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}

    if "crop_recommendations" in {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}:
        if "user_id" not in columns("crop_recommendations"):
            conn.execute("ALTER TABLE crop_recommendations ADD COLUMN user_id INTEGER")
    if "disease_predictions" in {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}:
        if "user_id" not in columns("disease_predictions"):
            conn.execute("ALTER TABLE disease_predictions ADD COLUMN user_id INTEGER")
    conn.commit()
    conn.close()
