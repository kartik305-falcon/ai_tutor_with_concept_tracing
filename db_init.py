import sqlite3

DB_NAME = "concept_traces.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            concepts TEXT,
            intent TEXT,
            confidence REAL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully")
