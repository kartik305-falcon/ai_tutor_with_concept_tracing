import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "concept_traces.db")


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Core traces table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            concepts TEXT,
            intent TEXT,
            confidence REAL
        )
    """)

    # Gamification: XP log
    cur.execute("""
        CREATE TABLE IF NOT EXISTS xp_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            event     TEXT NOT NULL,
            xp_earned INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Gamification: Streak tracker
    cur.execute("""
        CREATE TABLE IF NOT EXISTS streak_log (
            date TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully")
