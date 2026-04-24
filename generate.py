"""Entrypoint for the synthetic-data generator.

Running `uv run generate.py` recreates every artefact from a single seed:
- data/labrujula.sqlite  (eight tables)
- data/csv/*.csv         (one CSV per table)
- data/pricing_reference.md
- data/CHECKSUMS.txt
- sponsors/<slug>/ ...

Determinism contract: two consecutive runs produce byte-identical output.
No datetime.now() in data paths. No network calls. Single seed per run.
"""
from __future__ import annotations

import random
import sqlite3
from pathlib import Path

from faker import Faker

from lib import audience, newsletter, outlet
from lib.config import SEED

ROOT: Path = Path(__file__).parent
DATA_DIR: Path = ROOT / "data"
CSV_DIR: Path = DATA_DIR / "csv"
SPONSORS_DIR: Path = ROOT / "sponsors"
SQLITE_PATH: Path = DATA_DIR / "labrujula.sqlite"


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    CSV_DIR.mkdir(exist_ok=True)
    SPONSORS_DIR.mkdir(exist_ok=True)


def _fresh_sqlite() -> sqlite3.Connection:
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()
    conn = sqlite3.connect(SQLITE_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def main() -> None:
    _ensure_dirs()

    rng = random.Random(SEED)
    fake = Faker("es_CO")
    fake.seed_instance(SEED)

    conn = _fresh_sqlite()
    try:
        authors = outlet.build_authors(rng)
        outlet.write_authors(conn, authors)
        print(f"[outlet] authors written: {len(authors)}")

        articles = outlet.build_articles(rng, authors)
        outlet.write_articles(conn, articles)
        print(f"[outlet] articles written: {len(articles)}")

        pageview_rows, viral_ids = outlet.build_pageviews(rng, articles)
        outlet.write_pageviews(conn, pageview_rows)
        print(f"[outlet] pageview rows: {len(pageview_rows)}")
        print(f"[outlet] viral articles: {sorted(viral_ids)}")

        conn.commit()  # commit outlet tables so audience can read aggregates

        audience_rows = audience.build_audience_daily(rng, conn)
        audience.write_audience_daily(conn, audience_rows)
        print(f"[audience] rows: {len(audience_rows)}")

        subscribers = newsletter.build_subscribers(rng)
        newsletter.write_subscribers(conn, subscribers)
        print(f"[newsletter] subscribers: {len(subscribers)}")

        sends = newsletter.build_sends(rng, subscribers)
        newsletter.write_sends(conn, sends)
        print(f"[newsletter] sends: {len(sends)}")

        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
