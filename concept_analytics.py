import sqlite3
import json
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "concept_traces.db")


def load_traces():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT concepts, confidence FROM traces")
    rows = cur.fetchall()
    conn.close()
    return rows


def compute_mastery():
    try:
        traces = load_traces()
    except Exception:
        return {}

    if not traces:
        return {}

    concept_stats = defaultdict(lambda: {
        "attempts": 0,
        "confidence_sum": 0.0
    })

    for concepts_json, confidence in traces:
        try:
            concepts = json.loads(concepts_json)
        except Exception:
            continue

        for c in concepts:
            concept_stats[c]["attempts"] += 1
            concept_stats[c]["confidence_sum"] += max(0.0, float(confidence))

    mastery = {}
    for concept, stats in concept_stats.items():
        if stats["attempts"] > 0:
            mastery[concept] = {
                "attempts": stats["attempts"],
                "avg_confidence": round(
                    stats["confidence_sum"] / stats["attempts"], 2
                )
            }

    return mastery


if __name__ == "__main__":
    mastery = compute_mastery()
    print("\n===== CONCEPT MASTERY =====\n")
    for concept, data in mastery.items():
        print(
            f"{concept:25} | "
            f"Attempts: {data['attempts']:3} | "
            f"Avg Confidence: {data['avg_confidence']}"
        )
