import json
import sqlite3
print(">>> mastery_updater.py LOADED")


DB_NAME = "concept_traces.db"

POSITIVE_DELTA = 0.1
NEGATIVE_DELTA = 0.2


def update_mastery(concepts, success):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for concept in concepts:
        print(">>> update_mastery CALLED | concepts =",
              concepts, "| success =", success)

        if success:
            cur.execute("""
                INSERT INTO traces (question, concepts, intent, confidence)
                VALUES (?, ?, ?, ?)
            """, (
                "[CODE PASS]",
                json.dumps([concept]),
                "practice",
                POSITIVE_DELTA
            ))
        else:
            cur.execute("""
                INSERT INTO traces (question, concepts, intent, confidence)
                VALUES (?, ?, ?, ?)
            """, (
                "[CODE FAIL]",
                json.dumps([concept]),
                "practice",
                -NEGATIVE_DELTA
            ))

    conn.commit()
    conn.close()
