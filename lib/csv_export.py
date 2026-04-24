"""Emit one CSV per SQLite table under data/csv/.

Uses pandas for JSON column handling: topic_tags and
newsletters_opted_in stay as JSON-encoded strings in the CSV, which is
the most portable form for downstream consumers.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

TABLES: list[str] = [
    "authors",
    "articles",
    "pageviews_daily",
    "audience_daily",
    "newsletter_subscribers",
    "newsletter_sends",
    "past_campaigns",
    "campaign_articles",
]


def export_all(conn: sqlite3.Connection, csv_dir: Path) -> dict[str, int]:
    """Write one CSV per table. Returns row counts per table."""
    counts: dict[str, int] = {}
    for table in TABLES:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        # Stable sort order for determinism.
        if "article_id" in df.columns and table != "articles":
            if "date" in df.columns:
                df = df.sort_values(["date", "article_id"]).reset_index(drop=True)
            elif "campaign_id" in df.columns:
                df = df.sort_values(["campaign_id", "article_id"]).reset_index(drop=True)
            else:
                df = df.sort_values("article_id").reset_index(drop=True)
        path = csv_dir / f"{table}.csv"
        df.to_csv(path, index=False, encoding="utf-8", lineterminator="\n")
        counts[table] = len(df)
    return counts
