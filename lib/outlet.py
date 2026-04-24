"""Authors, articles, and pageviews_daily generators.

Split across three `build_*` functions that each take a seeded RNG and
return plain Python structures; `write_*` helpers own the SQLite inserts.
The generators have no side effects so they're easy to re-run for
consistency checks.
"""
from __future__ import annotations

import json
import random
import re
import sqlite3
import unicodedata
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
    headline_es   TEXT NOT NULL,
    headline_en   TEXT,
    section       TEXT NOT NULL,
    topic_tags    TEXT NOT NULL,
    published_at  TEXT NOT NULL,
    author_id     INTEGER NOT NULL REFERENCES authors(author_id),
    word_count    INTEGER NOT NULL,
    language      TEXT NOT NULL DEFAULT 'es',
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

# Article length bands by section. Investigations are long-form;
# opinion and actualidad stay tight.
WORD_COUNT_RANGES: dict[str, tuple[int, int]] = {
    "actualidad":    (400, 800),
    "politica":      (500, 1100),
    "clima":         (900, 1800),
    "ciudades":      (700, 1500),
    "investigacion": (1800, 3500),
    "cultura":       (600, 1200),
    "cafe_y_comida": (700, 1300),
    "opinion":       (800, 1400),
}

_EN_SECTION_LABEL: dict[str, str] = {
    "actualidad":    "Colombia News",
    "politica":      "Politics",
    "clima":         "Climate Coverage",
    "ciudades":      "Cities",
    "investigacion": "Investigation",
    "cultura":       "Culture",
    "cafe_y_comida": "Coffee & Food",
    "opinion":       "Opinion",
}


def _slugify(text: str) -> str:
    stripped = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    lowered = stripped.lower()
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
    # Seeded RNG intentionally unused — author list is fully specified in
    # vocab. Kept in the signature for parity with other generators.
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
    """For each section, candidate authors with per-author weight.

    Weight derives from the author's beat via `BEAT_SECTION_AFFINITY`.
    Sections with no beat pointing at them would be unreachable — all
    eight sections are covered by design.
    """
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
    if r < 0.30:      # morning roundup
        hour = rng.randint(7, 11)
    elif r < 0.55:    # lunch slot
        hour = rng.randint(12, 13)
    elif r < 0.80:    # evening push
        hour = rng.randint(17, 19)
    else:
        hour = rng.choice([6, 14, 15, 16, 20, 21])
    return datetime.combine(day, time(hour, rng.randint(0, 59), rng.randint(0, 59)))


_CONTRACTION_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\ba\s+el\b"),  "al"),
    (re.compile(r"\bde\s+el\b"), "del"),
]


def _post_process_headline(text: str) -> str:
    for pattern, replacement in _CONTRACTION_RULES:
        text = pattern.sub(replacement, text)
    # Capitalize the first letter — templates can start with a lowercase
    # filler token (e.g. {project} pulling "la ampliación…").
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
    if subs.get("region") and subs.get("region_b") == subs.get("region"):
        alts = [r for r in vocab.HEADLINE_FILLERS["region_b"] if r != subs["region"]]
        if alts:
            subs["region_b"] = rng.choice(alts)
    return _post_process_headline(template.format(**subs))


def _english_headline(section: str, tags: list[str]) -> str:
    label = _EN_SECTION_LABEL[section]
    topic = tags[0].replace("_", " ").title() if tags else label
    return f"{label}: {topic}"


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
            headline_es = _render_headline(rng, section)
            if rng.random() < config.TRANSLATION_FLAG_SHARE:
                headline_en: str | None = _english_headline(section, tags)
            else:
                headline_en = None
            published_at = _pick_published_at(rng, d)
            wc_lo, wc_hi = WORD_COUNT_RANGES[section]
            word_count = rng.randint(wc_lo, wc_hi)
            slug = _slugify(headline_es) or section
            url = (
                f"https://labrujula.co/{section}/{d.year:04d}/{d.month:02d}/"
                f"{slug}-{aid}"
            )
            articles.append(
                {
                    "article_id": aid,
                    "url": url,
                    "headline_es": headline_es,
                    "headline_en": headline_en,
                    "section": section,
                    "topic_tags": json.dumps(tags, ensure_ascii=False),
                    "published_at": published_at.isoformat(timespec="seconds"),
                    "author_id": author_id,
                    "word_count": word_count,
                    "language": "es",
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
        "INSERT INTO articles (article_id, url, headline_es, headline_en, section, "
        "topic_tags, published_at, author_id, word_count, language, sponsor_tag) "
        "VALUES (:article_id, :url, :headline_es, :headline_en, :section, "
        ":topic_tags, :published_at, :author_id, :word_count, :language, :sponsor_tag)",
        articles,
    )
