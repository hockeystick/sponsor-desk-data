"""Post-generation consistency checks.

Runs after every generate.py pass. Enforces cross-table invariants the
downstream brief tool will rely on. Raises RuntimeError on any
violation so the generator can't quietly ship broken data.
"""
from __future__ import annotations

import bisect
import json
import sqlite3

from lib import config


def _row_count(conn: sqlite3.Connection, table: str) -> int:
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def _count_check(
    conn: sqlite3.Connection, table: str, lo: int, hi: int,
    out: list[tuple[str, bool, str]],
) -> None:
    n = _row_count(conn, table)
    ok = lo <= n <= hi
    out.append((f"rows({table}) in [{lo}, {hi}]", ok, f"actual={n:,}"))


def _check_send_eligibility(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    subs = conn.execute(
        "SELECT subscribed_at, newsletters_opted_in FROM newsletter_subscribers"
    ).fetchall()
    opted_dates: dict[str, list[str]] = {nl: [] for nl in config.NEWSLETTER_LIST_SIZES}
    for sa, opts_json in subs:
        for nl in json.loads(opts_json):
            opted_dates[nl].append(sa)
    for nl in opted_dates:
        opted_dates[nl].sort()

    sends = conn.execute(
        "SELECT newsletter, send_date, recipients FROM newsletter_sends"
    ).fetchall()
    violations = 0
    for nl, sd, recipients in sends:
        eligible = bisect.bisect_right(opted_dates[nl], sd)
        if recipients > eligible:
            violations += 1
    out.append(
        (
            "recipients <= eligible subscribers at send date",
            violations == 0,
            f"{violations} send(s) violated (of {len(sends)})",
        )
    )


def _check_send_rates(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    for nl, (open_lo, open_hi) in config.OPEN_RATE_RANGES.items():
        rows = conn.execute(
            "SELECT opens * 1.0 / recipients FROM newsletter_sends WHERE newsletter = ?",
            (nl,),
        ).fetchall()
        rates = [r[0] for r in rows if r[0] is not None]
        if not rates:
            out.append((f"{nl} open rate range", False, "no sends"))
            continue
        min_r, max_r = min(rates), max(rates)
        ok = min_r >= open_lo - 0.01 and max_r <= open_hi + 0.01
        out.append(
            (
                f"{nl} open rates within [{open_lo:.2f}, {open_hi:.2f}]",
                ok,
                f"observed min={min_r:.3f} max={max_r:.3f}",
            )
        )


def _check_pv_sess_ratio(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    pv = conn.execute("SELECT SUM(pageviews) FROM pageviews_daily").fetchone()[0] or 0
    ss = conn.execute("SELECT SUM(sessions) FROM audience_daily").fetchone()[0] or 0
    ratio = pv / ss if ss else 0
    out.append(
        (
            "pv/sess ratio in [0.80, 0.95]",
            0.80 <= ratio <= 0.95,
            f"pv={pv:,} sess={ss:,} ratio={ratio:.3f}",
        )
    )


def _check_bridge_windows(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    n = conn.execute(
        """
        SELECT COUNT(*)
        FROM campaign_articles ca
        JOIN past_campaigns c ON c.campaign_id = ca.campaign_id
        JOIN articles a ON a.article_id = ca.article_id
        WHERE substr(a.published_at, 1, 10) < c.start_date
           OR substr(a.published_at, 1, 10) > c.end_date
        """
    ).fetchone()[0]
    out.append(("campaign_articles within campaign window", n == 0, f"{n} violation(s)"))


def _check_sponsor_tag_propagation(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    mismatched = conn.execute(
        """
        SELECT COUNT(*)
        FROM campaign_articles ca
        JOIN past_campaigns c ON c.campaign_id = ca.campaign_id
        JOIN articles a ON a.article_id = ca.article_id
        WHERE a.sponsor_tag IS NULL OR a.sponsor_tag != c.sponsor_name
        """
    ).fetchone()[0]
    out.append(
        (
            "sponsor_tag propagated to every linked article",
            mismatched == 0,
            f"{mismatched} mismatch(es)",
        )
    )


def _check_headline_sponsor_minimums(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    """The four headline sponsors must each have at least N campaigns
    on record so the brief tool has real history to cite."""
    for sponsor, (sector, min_n) in config.HEADLINE_SPONSORS.items():
        actual = conn.execute(
            "SELECT COUNT(*) FROM past_campaigns WHERE sponsor_name = ?",
            (sponsor,),
        ).fetchone()[0]
        out.append(
            (
                f"{sponsor}: >= {min_n} campaigns",
                actual >= min_n,
                f"actual={actual}",
            )
        )


def _check_outcome_distribution(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    """At least 10% of campaigns should land in a non-completed outcome
    so the brief tool sees honest history, not success-theatre."""
    total = conn.execute("SELECT COUNT(*) FROM past_campaigns").fetchone()[0]
    non_completed = conn.execute(
        "SELECT COUNT(*) FROM past_campaigns WHERE outcome_status != 'completed'"
    ).fetchone()[0]
    pct = (non_completed / total) if total else 0
    out.append(
        (
            "non-completed outcomes share >= 10%",
            pct >= 0.10,
            f"{non_completed}/{total} = {pct*100:.1f}%",
        )
    )


def _check_fk_integrity(
    conn: sqlite3.Connection, out: list[tuple[str, bool, str]]
) -> None:
    orphans_articles = conn.execute(
        "SELECT COUNT(*) FROM articles a LEFT JOIN authors au "
        "ON au.author_id = a.author_id WHERE au.author_id IS NULL"
    ).fetchone()[0]
    out.append(
        ("articles.author_id FK valid", orphans_articles == 0, f"{orphans_articles} orphan(s)")
    )

    orphan_pv = conn.execute(
        "SELECT COUNT(*) FROM pageviews_daily p LEFT JOIN articles a "
        "ON a.article_id = p.article_id WHERE a.article_id IS NULL"
    ).fetchone()[0]
    out.append(
        (
            "pageviews_daily.article_id FK valid",
            orphan_pv == 0,
            f"{orphan_pv} orphan(s)",
        )
    )


def run(conn: sqlite3.Connection) -> None:
    results: list[tuple[str, bool, str]] = []

    _count_check(conn, "authors", 22, 22, results)
    _count_check(conn, "articles", 4_800, 6_500, results)
    _count_check(conn, "pageviews_daily", 130_000, 230_000, results)
    _count_check(conn, "audience_daily", 80_000, 160_000, results)
    _count_check(conn, "newsletter_subscribers", 44_500, 45_500, results)
    _count_check(conn, "newsletter_sends", 580, 640, results)
    _count_check(conn, "past_campaigns", 68, 76, results)
    _count_check(conn, "campaign_articles", 80, 360, results)

    _check_pv_sess_ratio(conn, results)
    _check_bridge_windows(conn, results)
    _check_sponsor_tag_propagation(conn, results)
    _check_headline_sponsor_minimums(conn, results)
    _check_outcome_distribution(conn, results)
    _check_fk_integrity(conn, results)
    _check_send_eligibility(conn, results)
    _check_send_rates(conn, results)

    failed = [(n, d) for n, ok, d in results if not ok]

    print("\n=== Verification ===")
    for name, ok, detail in results:
        mark = "OK  " if ok else "FAIL"
        print(f"  [{mark}] {name:64}  {detail}")

    if failed:
        print(f"\n{len(failed)} check(s) FAILED. Aborting.")
        raise RuntimeError(f"verifier: {len(failed)} check(s) failed: "
                           + "; ".join(n for n, _ in failed))
    print(f"  all {len(results)} checks passed")
