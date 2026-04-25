"""Newsletter subscribers and sends.

Two newsletters:
- The Daily Cascade — weekday morning roundup, largest list (~38k)
- Plate & Place — weekly Friday food and culture letter, smaller (~22k)

Subscribers: 45,000 IDs with hashed identifiers, growth-curve subscribed_at
dates 2019-2025, US-heavy country mix, 50/35/15 cold/warm/hot engagement,
1-2 newsletter opt-ins weighted so total opt-ins approximate the sum of
list size targets.

Sends: one row per (newsletter, send_date). Daily Cascade Mon-Fri,
Plate & Place Fridays. Recipients at send time = opted-in subscribers
whose subscribed_at predates the send.
"""
from __future__ import annotations

import bisect
import hashlib
import json
import random
import sqlite3
from datetime import date, timedelta

from lib import config

SUBSCRIBERS_DDL = """
CREATE TABLE newsletter_subscribers (
    subscriber_id         TEXT PRIMARY KEY,
    subscribed_at         TEXT NOT NULL,
    country               TEXT NOT NULL,
    language              TEXT NOT NULL,
    engagement_bucket     TEXT NOT NULL,
    newsletters_opted_in  TEXT NOT NULL,
    last_active_at        TEXT NOT NULL
);
CREATE INDEX idx_sub_country ON newsletter_subscribers(country);
CREATE INDEX idx_sub_subscribed ON newsletter_subscribers(subscribed_at);
"""

SENDS_DDL = """
CREATE TABLE newsletter_sends (
    send_id           INTEGER PRIMARY KEY,
    newsletter        TEXT NOT NULL,
    send_date         TEXT NOT NULL,
    subject_line      TEXT NOT NULL,
    recipients        INTEGER NOT NULL,
    opens             INTEGER NOT NULL,
    unique_opens      INTEGER NOT NULL,
    clicks            INTEGER NOT NULL,
    unique_clicks     INTEGER NOT NULL,
    unsubscribes      INTEGER NOT NULL
);
CREATE INDEX idx_send_newsletter ON newsletter_sends(newsletter);
CREATE INDEX idx_send_date ON newsletter_sends(send_date);
"""

_FOUNDING_DATE = date(2019, 1, 15)

_SEND_WEEKDAYS: dict[str, set[int]] = {
    "daily_cascade": {0, 1, 2, 3, 4},  # Mon-Fri
    "plate_place":   {4},              # Friday
}

_DAILY_CASCADE_SUBJECTS: list[str] = [
    "The Daily Cascade — {topic}",
    "Today in Portland: {topic}",
    "Your morning briefing on {topic}",
    "What we're watching at City Hall today",
    "Five stories to start your day",
    "Daily Cascade: {topic}",
    "The Cascade — {weekday} morning edition",
    "Inside today's news: {topic}",
    "Portland this morning: {topic}",
    "The brief: {topic}",
]

_PLATE_PLACE_SUBJECTS: list[str] = [
    "Plate & Place: {topic}",
    "This weekend in Portland's food scene",
    "Plate & Place — where to eat this weekend",
    "Where we're eating, drinking, and going",
    "Plate & Place: {topic}",
    "The Friday food letter",
    "Pour-over picks and weekend plans",
    "Where Portland eats this week",
]

_DAILY_TOPICS: list[str] = [
    "the camping ordinance vote",
    "the Joint Office shake-up",
    "the rent stabilization fight",
    "PGE's rate hike filing",
    "Multnomah County's audit findings",
    "the Burnside Bridge plan",
    "the FX bus rollout",
    "ranked-choice tabulation",
    "downtown's slow comeback",
    "Powell Boulevard pedestrian deaths",
    "the Joint Office contract",
    "salmon runs on the Sandy",
    "wildfire smoke advisories",
    "the climate plan rewrite",
]

_PLATE_TOPICS: list[str] = [
    "a new Sichuan pop-up in St Johns",
    "the cooperative bakery on Alberta",
    "Sumatran roasts to seek out",
    "weekend wine bar picks",
    "the natural-wine list everyone's talking about",
    "where chefs are eating right now",
    "a Burundian café opens in Foster-Powell",
    "single-origin pour-overs in Sellwood",
    "Detroit-style pizza in the Pearl",
    "weekend brunch in Hawthorne",
    "a craft beer crawl through Slabtown",
    "Portland's queer food scene",
    "winter farmers' market roundup",
]

_WEEKDAY_EN: dict[int, str] = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
    4: "Friday", 5: "Saturday", 6: "Sunday",
}


def _subscriber_id(idx: int) -> str:
    h = hashlib.sha256(f"cascade-tribune-subscriber-{idx}".encode()).hexdigest()
    return f"sub_{h[:16]}"


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


def _pick_year(rng: random.Random) -> int:
    items = list(config.SUBSCRIBER_YEAR_GROWTH.items())
    total = sum(w for _, w in items)
    r = rng.random() * total
    cum = 0.0
    for y, w in items:
        cum += w
        if r <= cum:
            return y
    return items[-1][0]


def _pick_subscribed_at(rng: random.Random) -> date:
    year = _pick_year(rng)
    if year == 2019:
        day_of_year = rng.randint(14, 364)  # after founding
    else:
        day_of_year = rng.randint(0, 364)
    d = date(year, 1, 1) + timedelta(days=day_of_year)
    return max(d, _FOUNDING_DATE)


def _pick_last_active(
    rng: random.Random, subscribed_at: date, bucket: str
) -> date:
    lo, hi = config.LAST_ACTIVE_DAYS_BY_BUCKET[bucket]
    days_ago = rng.randint(lo, hi)
    candidate = config.ARTICLES_END - timedelta(days=days_ago)
    return max(candidate, subscribed_at)


def _pick_opt_ins(rng: random.Random) -> list[str]:
    overlap_items = list(config.LIST_OVERLAP_SPLIT.items())
    n_counts = [c for c, _ in overlap_items]
    n_weights = [w for _, w in overlap_items]
    n = rng.choices(n_counts, weights=n_weights)[0]

    available = list(config.NEWSLETTER_LIST_SIZES.items())
    picked: list[str] = []
    for _ in range(n):
        total = sum(w for _, w in available)
        r = rng.random() * total
        cum = 0.0
        for i, (nl, w) in enumerate(available):
            cum += w
            if r <= cum:
                picked.append(nl)
                available.pop(i)
                break
    return sorted(picked)


def build_subscribers(rng: random.Random) -> list[dict]:
    subs: list[dict] = []
    for idx in range(config.SUBSCRIBER_COUNT):
        subscribed_at = _pick_subscribed_at(rng)
        country = _weighted_choice(rng, config.SUBSCRIBER_COUNTRY_WEIGHTS)
        # Subscriber language: most English, small Spanish share for US subs.
        es_chance = 0.04 if country == "US" else 0.01
        language = "es" if rng.random() < es_chance else "en"
        bucket = _weighted_choice(rng, config.ENGAGEMENT_BUCKET_SPLIT)
        opt_ins = _pick_opt_ins(rng)
        last_active = _pick_last_active(rng, subscribed_at, bucket)
        subs.append(
            {
                "subscriber_id": _subscriber_id(idx),
                "subscribed_at": subscribed_at.isoformat(),
                "country": country,
                "language": language,
                "engagement_bucket": bucket,
                "newsletters_opted_in": json.dumps(opt_ins),
                "last_active_at": last_active.isoformat(),
            }
        )
    subs.sort(key=lambda s: s["subscriber_id"])
    return subs


def _iterate_send_dates(newsletter: str):
    weekdays = _SEND_WEEKDAYS[newsletter]
    d = config.NEWSLETTER_START
    while d <= config.NEWSLETTER_END:
        if d.weekday() in weekdays:
            yield d
        d += timedelta(days=1)


def _subject_line(rng: random.Random, newsletter: str, send_date: date) -> str:
    if newsletter == "daily_cascade":
        templates, topics = _DAILY_CASCADE_SUBJECTS, _DAILY_TOPICS
    else:
        templates, topics = _PLATE_PLACE_SUBJECTS, _PLATE_TOPICS
    template = rng.choice(templates)
    return template.format(
        topic=rng.choice(topics),
        weekday=_WEEKDAY_EN[send_date.weekday()],
    )


def build_sends(rng: random.Random, subscribers: list[dict]) -> list[dict]:
    opted_dates_by_nl: dict[str, list[str]] = {
        nl: [] for nl in config.NEWSLETTER_LIST_SIZES
    }
    for s in subscribers:
        subscribed_at = s["subscribed_at"]
        for nl in json.loads(s["newsletters_opted_in"]):
            opted_dates_by_nl[nl].append(subscribed_at)
    for nl in opted_dates_by_nl:
        opted_dates_by_nl[nl].sort()

    sends: list[dict] = []
    for nl in ["daily_cascade", "plate_place"]:
        sorted_dates = opted_dates_by_nl[nl]
        lo_open, hi_open = config.OPEN_RATE_RANGES[nl]
        lo_click, hi_click = config.CLICK_RATE_RANGES[nl]
        lo_unsub, hi_unsub = config.UNSUB_RATE_RANGES[nl]
        for send_date in _iterate_send_dates(nl):
            recipients = bisect.bisect_right(sorted_dates, send_date.isoformat())
            if recipients == 0:
                continue
            open_rate = rng.uniform(lo_open, hi_open)
            click_rate = rng.uniform(lo_click, hi_click)
            unsub_rate = rng.uniform(lo_unsub, hi_unsub)
            opens = int(recipients * open_rate)
            unique_opens = int(opens * (0.90 + 0.06 * rng.random()))
            clicks = int(recipients * click_rate)
            unique_clicks = int(clicks * (0.86 + 0.06 * rng.random()))
            unsubscribes = int(recipients * unsub_rate)
            sends.append(
                {
                    "newsletter": nl,
                    "send_date": send_date.isoformat(),
                    "subject_line": _subject_line(rng, nl, send_date),
                    "recipients": recipients,
                    "opens": opens,
                    "unique_opens": unique_opens,
                    "clicks": clicks,
                    "unique_clicks": unique_clicks,
                    "unsubscribes": unsubscribes,
                }
            )
    sends.sort(key=lambda s: (s["send_date"], s["newsletter"]))
    for i, s in enumerate(sends, start=1):
        s["send_id"] = i
    return sends


def write_subscribers(conn: sqlite3.Connection, subs: list[dict]) -> None:
    conn.executescript(SUBSCRIBERS_DDL)
    conn.executemany(
        "INSERT INTO newsletter_subscribers (subscriber_id, subscribed_at, "
        "country, language, engagement_bucket, newsletters_opted_in, "
        "last_active_at) VALUES (:subscriber_id, :subscribed_at, :country, "
        ":language, :engagement_bucket, :newsletters_opted_in, :last_active_at)",
        subs,
    )


def write_sends(conn: sqlite3.Connection, sends: list[dict]) -> None:
    conn.executescript(SENDS_DDL)
    conn.executemany(
        "INSERT INTO newsletter_sends (send_id, newsletter, send_date, "
        "subject_line, recipients, opens, unique_opens, clicks, "
        "unique_clicks, unsubscribes) VALUES (:send_id, :newsletter, "
        ":send_date, :subject_line, :recipients, :opens, :unique_opens, "
        ":clicks, :unique_clicks, :unsubscribes)",
        sends,
    )
