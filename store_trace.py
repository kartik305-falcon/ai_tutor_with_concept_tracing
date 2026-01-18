import sqlite3
import json

DB_NAME = "concept_traces.db"


def store_trace(question, trace_json):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO traces (question, concepts, intent, confidence)
        VALUES (?, ?, ?, ?)
    """, (
        question,
        json.dumps(trace_json["concepts"]),
        trace_json["intent"],
        trace_json["confidence"]
    ))

    conn.commit()
    conn.close()
