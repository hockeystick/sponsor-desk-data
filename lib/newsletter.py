"""Newsletter subscribers and sends.

Subscribers model: 45,000 IDs with hashed identifiers, growth-curve
subscribed_at dates across the outlet's history (Jan 2018 to Dec 2025),
country/language/engagement metadata, and 1-3 newsletter opt-ins
weighted so aggregate opt-ins roughly match target list sizes.

Sends model: one row per (newsletter, send_date). Diario Mon-Fri,
Verde Thursdays, Sobremesa Saturdays — within the 24-month window.
Recipients at send time = opted-in subscribers whose subscribed_at
predates the send. Natural growth over the window (the Jan 2024
Diario send reaches ~23k; the Dec 2025 Diario send reaches ~30k).
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
    subject_line_es   TEXT NOT NULL,
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

_FOUNDING_DATE = date(2018, 1, 15)

_SEND_WEEKDAYS: dict[str, set[int]] = {
    "diario":    {0, 1, 2, 3, 4},     # Mon-Fri
    "verde":     {3},                 # Thursday
    "sobremesa": {5},                 # Saturday
}

_DIARIO_SUBJECTS: list[str] = [
    "Hoy en La Brújula: {topic}",
    "El resumen del día",
    "Diario: {topic}",
    "Lo que debes leer hoy en Colombia",
    "Un vistazo al país — {topic}",
    "Buenas tardes desde Medellín",
    "Tu resumen del {weekday}",
    "Cinco historias para hoy",
    "La mañana en Colombia: {topic}",
    "Hoy en portada — {topic}",
]

_VERDE_SUBJECTS: list[str] = [
    "Verde: {topic}",
    "La semana del clima: {topic}",
    "Alerta verde — {topic}",
    "Lo urgente en clima: {topic}",
    "Esta semana en biodiversidad",
    "Verde · {topic}",
    "El balance ambiental de la semana",
    "Una semana en la crisis climática",
]

_SOBREMESA_SUBJECTS: list[str] = [
    "Sobremesa: {topic}",
    "Esta semana probamos: {topic}",
    "Café, comida y cultura: {topic}",
    "La mesa de Sobremesa",
    "Para el fin de semana: {topic}",
    "Sobremesa · {topic}",
    "Entre tazas y fogones",
    "Lo que está pasando en la cocina colombiana",
]

_DIARIO_TOPICS: list[str] = [
    "reforma a la salud", "paro camionero", "elecciones locales",
    "Hidroituango", "POT de Medellín", "paz total",
    "reforma pensional", "tarifas de EPM", "la consulta popular",
    "el metro ligero", "migración venezolana", "presupuesto nacional",
    "Corte Constitucional", "la agenda del Congreso",
]

_VERDE_TOPICS: list[str] = [
    "deforestación en la Amazonía", "los páramos de Santurbán",
    "minería ilegal en el Chocó", "sequía en La Guajira",
    "transición energética", "la COP de Medellín",
    "consulta previa", "biodiversidad en el Pacífico",
    "contaminación del río Medellín", "proyecto Quebradona",
    "ríos contaminados de Antioquia", "la crisis del agua en Bogotá",
]

_SOBREMESA_TOPICS: list[str] = [
    "Gesha del Huila", "Tabi de Nariño", "Caturra del Tolima",
    "la bandeja paisa", "el sancocho trifásico",
    "los festivales de diciembre", "cocina indígena del Cauca",
    "Bourbon Rosado", "las arepas del Valle de Aburrá",
    "el aguardiente antioqueño", "la lechona tolimense",
    "nuevos baristas de Medellín", "mercados campesinos",
]

_WEEKDAY_ES: dict[int, str] = {
    0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
    4: "viernes", 5: "sábado", 6: "domingo",
}


def _subscriber_id(idx: int) -> str:
    h = hashlib.sha256(f"labrujula-subscriber-{idx}".encode()).hexdigest()
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
    if year == 2018:
        day_of_year = rng.randint(14, 364)  # after founding
    elif year == 2025:
        day_of_year = rng.randint(0, 364)
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
        en_share = config.SUBSCRIBER_EN_SHARE_BY_COUNTRY[country]
        language = "en" if rng.random() < en_share else "es"
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
    if newsletter == "diario":
        templates, topics = _DIARIO_SUBJECTS, _DIARIO_TOPICS
    elif newsletter == "verde":
        templates, topics = _VERDE_SUBJECTS, _VERDE_TOPICS
    else:
        templates, topics = _SOBREMESA_SUBJECTS, _SOBREMESA_TOPICS
    template = rng.choice(templates)
    return template.format(
        topic=rng.choice(topics),
        weekday=_WEEKDAY_ES[send_date.weekday()],
    )


def build_sends(rng: random.Random, subscribers: list[dict]) -> list[dict]:
    """Sorted subscribed-at indices per newsletter, then bisect per send."""
    opted_dates_by_nl: dict[str, list[date]] = {
        nl: [] for nl in config.NEWSLETTER_LIST_SIZES
    }
    for s in subscribers:
        subscribed_at = date.fromisoformat(s["subscribed_at"])
        for nl in json.loads(s["newsletters_opted_in"]):
            opted_dates_by_nl[nl].append(subscribed_at)
    for nl in opted_dates_by_nl:
        opted_dates_by_nl[nl].sort()

    sends: list[dict] = []
    for nl in ["diario", "verde", "sobremesa"]:
        sorted_dates = opted_dates_by_nl[nl]
        lo_open, hi_open = config.OPEN_RATE_RANGES[nl]
        lo_click, hi_click = config.CLICK_RATE_RANGES[nl]
        lo_unsub, hi_unsub = config.UNSUB_RATE_RANGES[nl]
        for send_date in _iterate_send_dates(nl):
            recipients = bisect.bisect_right(sorted_dates, send_date)
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
                    "subject_line_es": _subject_line(rng, nl, send_date),
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
        "subject_line_es, recipients, opens, unique_opens, clicks, "
        "unique_clicks, unsubscribes) VALUES (:send_id, :newsletter, "
        ":send_date, :subject_line_es, :recipients, :opens, :unique_opens, "
        ":clicks, :unique_clicks, :unsubscribes)",
        sends,
    )
