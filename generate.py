"""Entrypoint for the synthetic-data generator.

Running `uv run generate.py` recreates every artefact from a single seed:
- data/cascade_tribune.sqlite  (eight tables)
- data/csv/*.csv               (one CSV per table)
- data/pricing_reference.md
- data/CHECKSUMS.txt
- sponsors/<slug>/ ...

Determinism contract: two consecutive runs produce byte-identical output.
No datetime.now() in data paths. No network calls. Single seed per run.
"""
from __future__ import annotations

import hashlib
import random
import sqlite3
from pathlib import Path

from lib import audience, campaigns, csv_export, newsletter, outlet, sponsors, verify
from lib.config import SEED

ROOT: Path = Path(__file__).parent
DATA_DIR: Path = ROOT / "data"
CSV_DIR: Path = DATA_DIR / "csv"
SPONSORS_DIR: Path = ROOT / "sponsors"
SQLITE_PATH: Path = DATA_DIR / "cascade_tribune.sqlite"


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

    # Clean up prior artefacts so we never mix a half-regenerated run.
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()
    for csv_file in CSV_DIR.glob("*.csv"):
        csv_file.unlink()
    for md in SPONSORS_DIR.rglob("*.md"):
        md.unlink()
    checksums_path = DATA_DIR / "CHECKSUMS.txt"
    if checksums_path.exists():
        checksums_path.unlink()

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

        campaign_rows = campaigns.build_campaigns(rng)
        bridge_rows, campaign_rows = campaigns.build_campaign_articles_and_summaries(
            rng, campaign_rows, articles
        )
        campaigns.write_campaigns(conn, campaign_rows, bridge_rows)
        print(
            f"[campaigns] campaigns: {len(campaign_rows)}  "
            f"bridge rows: {len(bridge_rows)}"
        )

        campaigns.write_pricing_reference(DATA_DIR / "pricing_reference.md")
        print(f"[campaigns] pricing_reference.md written")

        conn.commit()

        # Post-generation verification. Fails loud if any invariant broke.
        verify.run(conn)

        # CSV export mirrors each table to data/csv/.
        csv_counts = csv_export.export_all(conn, CSV_DIR)
        print(f"\n[csv] wrote {sum(csv_counts.values()):,} rows across "
              f"{len(csv_counts)} files")
    finally:
        conn.close()

    n_sponsor_files = sponsors.write_all_sponsors(rng, SPONSORS_DIR)
    print(f"[sponsors] files written: {n_sponsor_files}")

    _write_checksums()
    print(f"[checksums] wrote {checksums_path.name}")


def _write_checksums() -> None:
    """SHA256 every generated artefact into data/CHECKSUMS.txt.

    Two consecutive `uv run generate.py` invocations must produce an
    identical CHECKSUMS.txt. Covers: labrujula.sqlite, every CSV,
    pricing_reference.md, every sponsor markdown.
    """
    targets: list[Path] = [SQLITE_PATH]
    targets.extend(sorted(CSV_DIR.glob("*.csv")))
    targets.append(DATA_DIR / "pricing_reference.md")
    targets.extend(sorted(SPONSORS_DIR.rglob("*.md")))

    lines: list[str] = []
    for p in targets:
        if not p.exists():
            continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        rel = p.relative_to(ROOT)
        lines.append(f"{digest}  {rel}")

    (DATA_DIR / "CHECKSUMS.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
