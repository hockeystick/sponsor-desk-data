"""audience_daily rollups.

Emits one row per (date, country, region, city, language, device,
referrer_type) combo where sessions clear MIN_AUDIENCE_SESSIONS.

For US sessions:
- Top cities (Portland metro, Salem, Eugene, Bend, plus diaspora hubs in
  WA/CA/NY) get city-level granularity with state in the `region` column.
- Long-tail US states roll up to a single (region='other_state', city=NULL)
  bucket.

Non-US (CA, UK, other) is country-level — region=NULL — with optional
top diaspora cities for CA and UK.

Daily totals derive from the day's article pageviews × SESSION_PAGEVIEW_RATIO,
keeping the audience table consistent with `pageviews_daily`.
"""
from __future__ import annotations

import random
import sqlite3

from lib import config, vocab

AUDIENCE_DDL = """
CREATE TABLE audience_daily (
    date             TEXT NOT NULL,
    country          TEXT NOT NULL,
    region           TEXT,
    city             TEXT,
    language         TEXT NOT NULL,
    device           TEXT NOT NULL,
    referrer_type    TEXT NOT NULL,
    sessions         INTEGER NOT NULL,
    new_users        INTEGER NOT NULL,
    returning_users  INTEGER NOT NULL
);
CREATE INDEX idx_aud_date ON audience_daily(date);
CREATE INDEX idx_aud_country ON audience_daily(country);
"""


def _daily_pageview_totals(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        "SELECT date, SUM(pageviews) FROM pageviews_daily GROUP BY date"
    ).fetchall()
    return {date: total for date, total in rows}


# Spanish share by country. Mostly English; a small Latino segment in
# East Portland reads in Spanish.
_ES_SHARE_BY_COUNTRY: dict[str, float] = {
    "US":    0.025,
    "CA":    0.005,
    "UK":    0.000,
    "other": 0.10,
}


def _emit_combos(
    rng: random.Random,
    rows: list[dict],
    date: str,
    country: str,
    region: str | None,
    city: str | None,
    sessions_pool: float,
) -> None:
    es_share = _ES_SHARE_BY_COUNTRY[country]
    lang_shares = [("en", 1.0 - es_share), ("es", es_share)]
    for lang, lw in lang_shares:
        if lw <= 0:
            continue
        for device, dw in vocab.DEVICE_WEIGHTS.items():
            for referrer, rw in vocab.REFERRER_WEIGHTS.items():
                expected = sessions_pool * lw * dw * rw
                noise = 0.80 + 0.40 * rng.random()
                sessions = int(expected * noise)
                if sessions < config.MIN_AUDIENCE_SESSIONS:
                    continue
                new_users_share = 0.28 + 0.22 * rng.random()
                new_users = max(1, int(sessions * new_users_share))
                returning_users = sessions - new_users
                rows.append(
                    {
                        "date": date,
                        "country": country,
                        "region": region,
                        "city": city,
                        "language": lang,
                        "device": device,
                        "referrer_type": referrer,
                        "sessions": sessions,
                        "new_users": new_users,
                        "returning_users": returning_users,
                    }
                )


# Top diaspora cities for non-US countries. Rest of country rolls up
# to a country-level row with city=NULL.
_DIASPORA_CITY_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    "CA": [("Vancouver BC", 0.42), ("Toronto", 0.20)],
    "UK": [("London", 0.55)],
}


def build_audience_daily(
    rng: random.Random, conn: sqlite3.Connection
) -> list[dict]:
    pv_by_date = _daily_pageview_totals(conn)
    rows: list[dict] = []

    for date in sorted(pv_by_date.keys()):
        pv = pv_by_date[date]
        daily_sessions = pv * config.SESSION_PAGEVIEW_RATIO * (
            0.95 + 0.10 * rng.random()
        )

        for country, cw in config.COUNTRY_WEIGHTS.items():
            pool = daily_sessions * cw

            if country == "US":
                # Iterate named cities; their state lives in `region`.
                for city, city_w in vocab.US_CITY_WEIGHTS.items():
                    state = vocab.US_STATE_FOR_CITY[city]
                    _emit_combos(
                        rng, rows, date, country, state, city, pool * city_w,
                    )
                # Remainder = the long tail of other US states.
                _emit_combos(
                    rng, rows, date, country,
                    "other_state", None,
                    pool * vocab.US_OTHER_STATE_SHARE,
                )
            elif country == "other":
                _emit_combos(rng, rows, date, country, None, None, pool)
            else:
                diaspora = _DIASPORA_CITY_WEIGHTS.get(country, [])
                named_share = sum(w for _, w in diaspora)
                for city, w in diaspora:
                    _emit_combos(
                        rng, rows, date, country, None, city, pool * w,
                    )
                _emit_combos(
                    rng, rows, date, country, None, None,
                    pool * (1.0 - named_share),
                )

    rows.sort(
        key=lambda r: (
            r["date"], r["country"], r["region"] or "",
            r["city"] or "", r["language"], r["device"], r["referrer_type"],
        )
    )
    return rows


def write_audience_daily(conn: sqlite3.Connection, rows: list[dict]) -> None:
    conn.executescript(AUDIENCE_DDL)
    conn.executemany(
        "INSERT INTO audience_daily (date, country, region, city, language, "
        "device, referrer_type, sessions, new_users, returning_users) "
        "VALUES (:date, :country, :region, :city, :language, :device, "
        ":referrer_type, :sessions, :new_users, :returning_users)",
        rows,
    )
