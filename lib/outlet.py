"""Authors, articles, and pageviews_daily generators.

Split across three `build_*` functions that each take a seeded RNG and
return plain Python structures; `write_*` helpers own the SQLite inserts.
The generators have no side effects so they're easy to re-run for
consistency checks.
"""
from __future__ import annotations

import json
import math
import random
import re
import sqlite3
from datetime import date, datetime, time, timedelta

from lib import config, vocab

AUTHORS_DDL = """
CREATE TABLE authors (
    author_id     INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    role          TEXT NOT NULL,
    primary_beat  TEXT NOT NULL,
    joined_at     TEXT NOT NULL,
    is_active     INTEGER NOT NULL
);
"""

ARTICLES_DDL = """
CREATE TABLE articles (
    article_id    INTEGER PRIMARY KEY,
    url           TEXT NOT NULL,
    headline      TEXT NOT NULL,
    section       TEXT NOT NULL,
    topic_tags    TEXT NOT NULL,
    published_at  TEXT NOT NULL,
    author_id     INTEGER NOT NULL REFERENCES authors(author_id),
    word_count    INTEGER NOT NULL,
    language      TEXT NOT NULL DEFAULT 'en',
    sponsor_tag   TEXT
);
CREATE INDEX idx_articles_section ON articles(section);
CREATE INDEX idx_articles_published_at ON articles(published_at);
CREATE INDEX idx_articles_author ON articles(author_id);
"""

PAGEVIEWS_DDL = """
CREATE TABLE pageviews_daily (
    date                    TEXT NOT NULL,
    article_id              INTEGER NOT NULL REFERENCES articles(article_id),
    pageviews               INTEGER NOT NULL,
    unique_visitors         INTEGER NOT NULL,
    avg_time_on_page_sec    REAL NOT NULL,
    scroll_depth_pct        REAL NOT NULL,
    PRIMARY KEY (date, article_id)
);
CREATE INDEX idx_pv_date ON pageviews_daily(date);
"""

# Article length bands by section. City-hall and housing accountability
# pieces run longer; food/drink coverage stays tight.
WORD_COUNT_RANGES: dict[str, tuple[int, int]] = {
    "city_hall":      (700, 1700),
    "housing":        (700, 1600),
    "climate":        (700, 1500),
    "transportation": (550, 1100),
    "business":       (500,  900),
    "culture":        (500, 1000),
    "food_drink":     (450,  900),
    "opinion":        (700, 1300),
}


def _slugify(text: str) -> str:
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug[:60]


def _weighted_choice(rng: random.Random, mapping: dict[str, float]) -> str:
    items = list(mapping.items())
    total = sum(w for _, w in items)
    r = rng.random() * total
    cum = 0.0
    for key, w in items:
        cum += w
        if r <= cum:
            return key
    return items[-1][0]


def build_authors(rng: random.Random) -> list[dict]:
    del rng
    return [
        {
            "author_id": i + 1,
            "name": name,
            "role": role,
            "primary_beat": beat,
            "joined_at": joined,
            "is_active": 1 if active else 0,
        }
        for i, (name, role, beat, joined, active) in enumerate(vocab.AUTHORS)
    ]


def _build_author_weights_by_section(
    authors: list[dict],
) -> dict[str, list[tuple[int, float]]]:
    result: dict[str, list[tuple[int, float]]] = {s: [] for s in vocab.SECTIONS}
    for a in authors:
        affinity = vocab.BEAT_SECTION_AFFINITY.get(a["primary_beat"], {})
        for section, w in affinity.items():
            if w > 0:
                result[section].append((a["author_id"], w))
    for section, candidates in result.items():
        if not candidates:
            raise RuntimeError(f"No author candidates for section {section!r}")
    return result


def _pick_author_for_section(
    rng: random.Random, candidates: list[tuple[int, float]]
) -> int:
    total = sum(w for _, w in candidates)
    r = rng.random() * total
    cum = 0.0
    for aid, w in candidates:
        cum += w
        if r <= cum:
            return aid
    return candidates[-1][0]


def _pick_tags(rng: random.Random, section: str) -> list[str]:
    pool = list(vocab.SECTION_TAG_AFFINITY[section])
    k = rng.choices([2, 3, 4], weights=[0.35, 0.45, 0.20])[0]
    k = min(k, len(pool))
    return sorted(rng.sample(pool, k))


def _pick_published_at(rng: random.Random, day: date) -> datetime:
    r = rng.random()
    if r < 0.32:      # morning brief slot, 7-11
        hour = rng.randint(7, 10)
    elif r < 0.55:    # midday, 11-14
        hour = rng.randint(11, 13)
    elif r < 0.82:    # afternoon push, 15-18
        hour = rng.randint(15, 17)
    else:             # late, evening
        hour = rng.choice([6, 14, 18, 19, 20])
    return datetime.combine(day, time(hour, rng.randint(0, 59), rng.randint(0, 59)))


def _post_process_headline(text: str) -> str:
    # US headlines capitalize first letter; templates may start with a
    # lowercase filler so normalize after rendering.
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def _render_headline(rng: random.Random, section: str) -> str:
    template = rng.choice(vocab.HEADLINE_TEMPLATES_BY_SECTION[section])
    placeholders = re.findall(r"\{(\w+)\}", template)
    subs: dict[str, str] = {}
    for p in placeholders:
        if p in subs:
            continue
        pool = vocab.HEADLINE_FILLERS.get(p)
        if not pool:
            raise RuntimeError(f"Missing filler vocabulary for placeholder {p!r}")
        subs[p] = rng.choice(pool)
    return _post_process_headline(template.format(**subs))


def _articles_per_day(rng: random.Random, d: date) -> int:
    if d.weekday() >= 5:
        return rng.randint(*config.WEEKEND_ARTICLES_RANGE)
    if rng.random() < config.WEEKDAY_BUSY_SHARE:
        return rng.randint(*config.WEEKDAY_BUSY_RANGE)
    return rng.randint(*config.WEEKDAY_NORMAL_RANGE)


def build_articles(rng: random.Random, authors: list[dict]) -> list[dict]:
    author_weights = _build_author_weights_by_section(authors)
    articles: list[dict] = []
    aid = 0
    d = config.ARTICLES_START
    while d <= config.ARTICLES_END:
        n = _articles_per_day(rng, d)
        for _ in range(n):
            aid += 1
            section = _weighted_choice(rng, config.SECTION_WEIGHTS)
            author_id = _pick_author_for_section(rng, author_weights[section])
            tags = _pick_tags(rng, section)
            headline = _render_headline(rng, section)
            published_at = _pick_published_at(rng, d)
            wc_lo, wc_hi = WORD_COUNT_RANGES[section]
            word_count = rng.randint(wc_lo, wc_hi)
            slug = _slugify(headline) or section
            url = (
                f"https://cascadetribune.com/{section}/{d.year:04d}/{d.month:02d}/"
                f"{slug}-{aid}"
            )
            articles.append(
                {
                    "article_id": aid,
                    "url": url,
                    "headline": headline,
                    "section": section,
                    "topic_tags": json.dumps(tags),
                    "published_at": published_at.isoformat(timespec="seconds"),
                    "author_id": author_id,
                    "word_count": word_count,
                    "language": "en",
                    "sponsor_tag": None,
                }
            )
        d += timedelta(days=1)
    return articles


def write_authors(conn: sqlite3.Connection, authors: list[dict]) -> None:
    conn.executescript(AUTHORS_DDL)
    conn.executemany(
        "INSERT INTO authors (author_id, name, role, primary_beat, joined_at, is_active) "
        "VALUES (:author_id, :name, :role, :primary_beat, :joined_at, :is_active)",
        authors,
    )


def write_articles(conn: sqlite3.Connection, articles: list[dict]) -> None:
    conn.executescript(ARTICLES_DDL)
    conn.executemany(
        "INSERT INTO articles (article_id, url, headline, section, "
        "topic_tags, published_at, author_id, word_count, language, sponsor_tag) "
        "VALUES (:article_id, :url, :headline, :section, "
        ":topic_tags, :published_at, :author_id, :word_count, :language, :sponsor_tag)",
        articles,
    )


# ---- pageviews_daily --------------------------------------------------------

# Long-form / accountability / opinion pieces tend to go viral.
_VIRAL_PREFERRED_SECTIONS: set[str] = {
    "city_hall", "housing", "climate", "opinion",
}


def _pick_viral_article_ids(
    rng: random.Random, articles: list[dict]
) -> set[int]:
    by_quarter: dict[tuple[int, int], list[dict]] = {}
    for a in articles:
        d = date.fromisoformat(a["published_at"][:10])
        q = (d.year, (d.month - 1) // 3 + 1)
        by_quarter.setdefault(q, []).append(a)
    chosen: set[int] = set()
    for q in sorted(by_quarter):
        bucket = by_quarter[q]
        preferred = [a for a in bucket if a["section"] in _VIRAL_PREFERRED_SECTIONS]
        pool = preferred if preferred else bucket
        chosen.add(rng.choice(pool)["article_id"])
    return chosen


def _expected_day_views(peak: int, day: int, half_life: float, publish_hour: int) -> float:
    if day == 0:
        hours_remaining = max(1, 24 - publish_hour)
        return peak * 0.55 * (hours_remaining / 24)
    if day == 1:
        return float(peak)
    return peak * math.pow(0.5, (day - 1) / half_life)


def build_pageviews(
    rng: random.Random, articles: list[dict]
) -> tuple[list[dict], set[int]]:
    viral_ids = _pick_viral_article_ids(rng, articles)
    rows: list[dict] = []

    for article in articles:
        section = article["section"]
        published_dt = datetime.fromisoformat(article["published_at"])
        publish_date = published_dt.date()
        publish_hour = published_dt.hour
        word_count = article["word_count"]
        aid = article["article_id"]

        is_viral = aid in viral_ids
        viral_mult = (
            rng.uniform(*config.VIRAL_MULTIPLIER_RANGE) if is_viral else 1.0
        )

        base = config.PEAK_PAGEVIEWS_BY_SECTION[section]
        variance = math.exp(rng.gauss(0.0, config.PEAK_LOGNORMAL_SIGMA))
        peak = max(120, int(base * variance * viral_mult))

        half_life = config.HALF_LIFE_BY_SECTION[section]
        tail_lo, tail_hi = config.TAIL_DAYS_BY_SECTION[section]
        tail_days = rng.randint(tail_lo, tail_hi)
        if is_viral:
            tail_days = int(tail_days * rng.uniform(*config.VIRAL_TAIL_EXTENSION))

        climate_bump_day = -1
        climate_bump_mag = 0.0
        if section == "climate" and rng.random() < config.CLIMATE_BUMP_PROB:
            lo, hi = config.CLIMATE_BUMP_DAYS
            hi = min(hi, max(lo, tail_days - 1))
            climate_bump_day = rng.randint(lo, hi)
            climate_bump_mag = rng.uniform(*config.CLIMATE_BUMP_MAGNITUDE)

        viral_bumps: dict[int, float] = {}
        if is_viral and tail_days >= 5:
            n_bumps = rng.randint(*config.VIRAL_SECONDARY_BUMP_COUNT)
            for _ in range(n_bumps):
                bump_day = rng.randint(3, tail_days - 1)
                viral_bumps[bump_day] = rng.uniform(
                    *config.VIRAL_SECONDARY_BUMP_MAGNITUDE
                )

        reading_time_sec = word_count / 200.0 * 60.0  # ~200 wpm for English news

        for d in range(tail_days + 1):
            noise = 0.80 + 0.40 * rng.random()
            expected = _expected_day_views(peak, d, half_life, publish_hour)
            views = int(expected * noise)
            if d == climate_bump_day:
                views += int(peak * climate_bump_mag * noise)
            if d in viral_bumps:
                views += int(peak * viral_bumps[d] * noise)
            if views < config.MIN_PAGEVIEW_THRESHOLD:
                continue

            uniq_fraction = (
                (0.70 + 0.15 * rng.random())
                if d <= 3
                else (0.80 + 0.15 * rng.random())
            )
            unique_visitors = max(1, int(views * uniq_fraction))

            finish_rate = 0.30 + 0.40 * rng.random()
            avg_time = reading_time_sec * finish_rate
            scroll_depth = 40.0 + 50.0 * rng.random()

            rows.append(
                {
                    "date": (publish_date + timedelta(days=d)).isoformat(),
                    "article_id": aid,
                    "pageviews": views,
                    "unique_visitors": unique_visitors,
                    "avg_time_on_page_sec": round(avg_time, 1),
                    "scroll_depth_pct": round(scroll_depth, 1),
                }
            )

    rows.sort(key=lambda r: (r["date"], r["article_id"]))
    return rows, viral_ids


def write_pageviews(conn: sqlite3.Connection, rows: list[dict]) -> None:
    conn.executescript(PAGEVIEWS_DDL)
    conn.executemany(
        "INSERT INTO pageviews_daily (date, article_id, pageviews, "
        "unique_visitors, avg_time_on_page_sec, scroll_depth_pct) "
        "VALUES (:date, :article_id, :pageviews, :unique_visitors, "
        ":avg_time_on_page_sec, :scroll_depth_pct)",
        rows,
    )
