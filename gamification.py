"""
gamification.py
---------------
Feature 5: XP & Streak System.
Tracks student experience points and daily learning streaks in SQLite.
"""

import sqlite3
import os
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "concept_traces.db")

# XP values per event
XP_REWARDS = {
    "chat":          5,
    "code_pass":     15,
    "code_partial":  7,
    "quiz_complete": 20,
    "duel_win":      30,
    "duel_complete": 10,
    "notes_gen":     5,
}

# Level thresholds: (min_xp, level_name)
LEVELS = [
    (0,    "Novice"),
    (100,  "Apprentice"),
    (300,  "Junior Dev"),
    (700,  "Developer"),
    (1500, "Senior Dev"),
    (3000, "Principal Engineer"),
    (6000, "Distinguished Engineer"),
]


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_gamification_tables():
    """Create XP and streak tables if they don't exist."""
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS xp_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            event     TEXT NOT NULL,
            xp_earned INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS streak_log (
            date TEXT PRIMARY KEY
        );
    """)
    conn.commit()
    conn.close()


def award_xp(event: str) -> dict:
    """
    Award XP for an event and record the day in streak_log.
    Returns updated XP summary.
    """
    xp = XP_REWARDS.get(event, 0)
    if xp == 0:
        return get_xp_summary()

    now = datetime.utcnow().isoformat()
    today = date.today().isoformat()

    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO xp_log (event, xp_earned, timestamp) VALUES (?, ?, ?)",
            (event, xp, now)
        )
        # Record today for streak (INSERT OR IGNORE handles duplicates)
        conn.execute(
            "INSERT OR IGNORE INTO streak_log (date) VALUES (?)",
            (today,)
        )
        conn.commit()
    finally:
        conn.close()

    return get_xp_summary()


def get_xp_summary() -> dict:
    """
    Return current XP summary:
    {
        "total_xp": int,
        "level": int (1-based),
        "level_name": str,
        "xp_in_level": int,
        "xp_to_next": int,
        "streak": int,
        "progress_pct": float (0-100)
    }
    """
    conn = _get_conn()
    try:
        row = conn.execute("SELECT COALESCE(SUM(xp_earned), 0) FROM xp_log").fetchone()
        total_xp = int(row[0]) if row else 0

        # Calculate current streak (consecutive days ending today or yesterday)
        dates = [r[0] for r in conn.execute("SELECT date FROM streak_log ORDER BY date DESC").fetchall()]
    finally:
        conn.close()

    # Determine current level
    current_level_idx = 0
    for i, (threshold, _) in enumerate(LEVELS):
        if total_xp >= threshold:
            current_level_idx = i

    level_num = current_level_idx + 1
    level_name = LEVELS[current_level_idx][1]
    level_xp_start = LEVELS[current_level_idx][0]

    if current_level_idx + 1 < len(LEVELS):
        next_threshold = LEVELS[current_level_idx + 1][0]
        xp_in_level = total_xp - level_xp_start
        xp_to_next = next_threshold - level_xp_start
        progress_pct = min(100.0, (xp_in_level / xp_to_next) * 100)
    else:
        # Max level
        xp_in_level = total_xp - level_xp_start
        xp_to_next = 0
        progress_pct = 100.0

    # Calculate streak
    streak = _calculate_streak(dates)

    return {
        "total_xp":     total_xp,
        "level":        level_num,
        "level_name":   level_name,
        "xp_in_level":  xp_in_level,
        "xp_to_next":   xp_to_next if xp_to_next > 0 else None,
        "streak":       streak,
        "progress_pct": round(progress_pct, 1)
    }


def _calculate_streak(dates: list[str]) -> int:
    """Count consecutive dates ending at today or yesterday."""
    if not dates:
        return 0

    from datetime import timedelta
    today = date.today()
    date_set = set(dates)

    streak = 0
    check = today
    # Allow streak to count if last activity was today or yesterday
    if today.isoformat() not in date_set:
        yesterday = today - timedelta(days=1)
        if yesterday.isoformat() not in date_set:
            return 0
        check = yesterday

    while check.isoformat() in date_set:
        streak += 1
        check -= timedelta(days=1)

    return streak
