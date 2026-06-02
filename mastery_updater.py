import json
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "concept_traces.db")

POSITIVE_CONFIDENCE = 0.8   # stored on code pass
NEGATIVE_CONFIDENCE = 0.2   # stored on code fail (low but never negative)


def update_mastery(concepts, success):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    confidence = POSITIVE_CONFIDENCE if success else NEGATIVE_CONFIDENCE

    for concept in concepts:
        cur.execute("""
            INSERT INTO traces (question, concepts, intent, confidence)
            VALUES (?, ?, ?, ?)
        """, (
            "[CODE PASS]" if success else "[CODE FAIL]",
            json.dumps([concept]),
            "practice",
            confidence
        ))

    conn.commit()
    conn.close()
