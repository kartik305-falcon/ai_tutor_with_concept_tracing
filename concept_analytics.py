import sqlite3
import json
from collections import defaultdict

DB_NAME = "concept_traces.db"


def load_traces():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT concepts, confidence FROM traces")
    rows = cur.fetchall()
    conn.close()
    return rows


def compute_mastery():
    traces = load_traces()

    concept_stats = defaultdict(lambda: {
        "attempts": 0,
        "confidence_sum": 0.0
    })

    for concepts_json, confidence in traces:
        concepts = json.loads(concepts_json)
        for c in concepts:
            concept_stats[c]["attempts"] += 1
            concept_stats[c]["confidence_sum"] += confidence

    mastery = {}
    for concept, stats in concept_stats.items():
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
