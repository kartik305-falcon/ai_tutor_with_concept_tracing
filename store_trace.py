import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "concept_traces.db")


def store_trace(question, trace_json):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO traces (question, concepts, intent, confidence)
        VALUES (?, ?, ?, ?)
    """, (
        question,
        json.dumps(trace_json["concepts"]),
        trace_json["intent"],
        max(0.0, min(1.0, float(trace_json["confidence"])))  # clamp 0-1
    ))

    conn.commit()
    conn.close()
