"""audience_daily rollups.

Emits one row per (date, country, region, city, language, device,
referrer_type) combo where sessions clear MIN_AUDIENCE_SESSIONS.

Colombia is the only country with city/region breakdown; diaspora
traffic (US/ES/MX) is split across top diaspora cities but left at
region=NULL; the `other` bucket is country-level only.

The day's total sessions is derived from that day's article pageviews
× SESSION_PAGEVIEW_RATIO, so the audience table is internally
consistent with `pageviews_daily` — the phase 8 verifier enforces this
relationship.
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


def _city_to_region() -> dict[str, str]:
    return {city: region for city, region in vocab.COLOMBIA_CITIES}


def _daily_pageview_totals(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        "SELECT date, SUM(pageviews) FROM pageviews_daily GROUP BY date"
    ).fetchall()
    return {date: total for date, total in rows}


def _emit_combos(
    rng: random.Random,
    rows: list[dict],
    date: str,
    country: str,
    region: str | None,
    city: str | None,
    sessions_pool: float,
) -> None:
    en_share = config.LANGUAGE_EN_SHARE_BY_COUNTRY[country]
    lang_shares = [("es", 1.0 - en_share), ("en", en_share)]
    for lang, lw in lang_shares:
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


_DIASPORA_CITY_WEIGHTS: dict[str, list[tuple[str, float]]] = {
    # For US/ES/MX, top diaspora cities take fixed shares; rest falls to
    # a single "rest-of-country" row with city=None.
    "US": [("Miami", 0.45), ("New York", 0.22), ("Houston", 0.15)],
    "ES": [("Madrid", 0.55), ("Barcelona", 0.25)],
    "MX": [("Ciudad de México", 0.60), ("Guadalajara", 0.20)],
}


def build_audience_daily(
    rng: random.Random, conn: sqlite3.Connection
) -> list[dict]:
    pv_by_date = _daily_pageview_totals(conn)
    city_region = _city_to_region()
    rows: list[dict] = []

    for date in sorted(pv_by_date.keys()):
        pv = pv_by_date[date]
        daily_sessions = pv * config.SESSION_PAGEVIEW_RATIO * (
            0.95 + 0.10 * rng.random()
        )

        for country, cw in config.COUNTRY_WEIGHTS.items():
            pool = daily_sessions * cw

            if country == "CO":
                for city, city_w in vocab.COLOMBIA_CITY_WEIGHTS.items():
                    _emit_combos(
                        rng, rows, date, country,
                        city_region[city], city, pool * city_w,
                    )
            elif country == "other":
                _emit_combos(rng, rows, date, country, None, None, pool)
            else:
                diaspora = _DIASPORA_CITY_WEIGHTS[country]
                named_share = sum(w for _, w in diaspora)
                for city, w in diaspora:
                    _emit_combos(rng, rows, date, country, None, city, pool * w)
                # Remainder goes to country-level rest-of-country bucket.
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
