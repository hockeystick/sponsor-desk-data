"""Single source of truth for determinism and volume knobs.

Every tunable parameter for the generator lives here. If you want to change
volume, cadence, or distribution shape, adjust values in this module — do not
sprinkle magic numbers through the generators.
"""
from __future__ import annotations

from datetime import date

SEED: int = 20260424

ARTICLES_START: date = date(2024, 1, 1)
ARTICLES_END: date = date(2025, 12, 31)
AUDIENCE_START: date = ARTICLES_START
AUDIENCE_END: date = ARTICLES_END
NEWSLETTER_START: date = ARTICLES_START
NEWSLETTER_END: date = ARTICLES_END
CAMPAIGNS_START: date = date(2022, 1, 1)
CAMPAIGNS_END: date = date(2025, 12, 31)

ARTICLE_COUNT_TARGET: int = 4500
SUBSCRIBER_COUNT: int = 45_000
CAMPAIGN_COUNT: int = 72
VIRAL_OUTLIER_COUNT: int = 8

# News cadence isn't uniform. Most weekdays sit in a normal band; a minority
# of weekdays are news-heavy and reach the upper end of the spec's 6-12 range.
WEEKDAY_NORMAL_RANGE: tuple[int, int] = (6, 9)
WEEKDAY_BUSY_RANGE: tuple[int, int] = (10, 12)
WEEKDAY_BUSY_SHARE: float = 0.15
WEEKEND_ARTICLES_RANGE: tuple[int, int] = (2, 4)

SECTION_WEIGHTS: dict[str, float] = {
    "actualidad": 0.20,
    "politica": 0.14,
    "clima": 0.22,
    "ciudades": 0.18,
    "investigacion": 0.10,
    "cultura": 0.06,
    "cafe_y_comida": 0.05,
    "opinion": 0.05,
}

# Share of articles that get an English translation headline populated.
TRANSLATION_FLAG_SHARE: float = 0.12

# Audience mix across countries.
COUNTRY_WEIGHTS: dict[str, float] = {
    "CO": 0.68,
    "US": 0.14,
    "ES": 0.08,
    "MX": 0.04,
    "other": 0.06,
}

# Share of sessions that are English (via site translation feature).
LANGUAGE_EN_SHARE: float = 0.12

# Tail-length ranges in days by section. Drives pageviews_daily row-count.
# Investigations have the longest tails; commodity news decays fastest.
TAIL_DAYS_BY_SECTION: dict[str, tuple[int, int]] = {
    "actualidad": (7, 14),
    "politica": (8, 16),
    "clima": (30, 60),
    "ciudades": (20, 40),
    "investigacion": (60, 120),
    "cultura": (20, 40),
    "cafe_y_comida": (20, 40),
    "opinion": (5, 10),
}

VIRAL_MULTIPLIER_RANGE: tuple[float, float] = (10.0, 30.0)

# Newsletter sizing + engagement.
NEWSLETTER_LIST_SIZES: dict[str, int] = {
    "diario": 30_000,
    "verde": 9_000,
    "sobremesa": 18_000,
}

OPEN_RATE_RANGES: dict[str, tuple[float, float]] = {
    "diario": (0.28, 0.35),
    "verde": (0.42, 0.48),
    "sobremesa": (0.34, 0.40),
}

CLICK_RATE_RANGES: dict[str, tuple[float, float]] = {
    "diario": (0.045, 0.075),
    "verde": (0.09, 0.14),
    "sobremesa": (0.055, 0.090),
}

UNSUB_RATE_RANGES: dict[str, tuple[float, float]] = {
    "diario": (0.0010, 0.0025),
    "verde": (0.0004, 0.0012),
    "sobremesa": (0.0008, 0.0020),
}

ENGAGEMENT_BUCKET_SPLIT: dict[str, float] = {
    "cold": 0.50,
    "warm": 0.35,
    "hot": 0.15,
}

# Share of subscribers on exactly 1, 2, or 3 of the newsletters.
LIST_OVERLAP_SPLIT: dict[int, float] = {1: 0.55, 2: 0.30, 3: 0.15}

# Campaign format distribution (sums to 1.0). sponsored_section most common.
CAMPAIGN_FORMAT_WEIGHTS: dict[str, float] = {
    "sponsored_section": 0.35,
    "branded_newsletter": 0.22,
    "longform_series": 0.12,
    "event_partnership": 0.18,
    "podcast_sponsorship": 0.13,
}

CAMPAIGN_SECTOR_WEIGHTS: dict[str, float] = {
    "financial_services": 0.22,
    "ngo_foundation": 0.20,
    "consumer_brands": 0.18,
    "health": 0.12,
    "tech": 0.14,
    "government_eu": 0.14,
}

# Fee ranges in EUR by format.
CAMPAIGN_FEE_RANGES: dict[str, tuple[int, int]] = {
    "sponsored_section": (12_000, 45_000),
    "branded_newsletter": (3_000, 9_000),
    "longform_series": (18_000, 42_000),
    "event_partnership": (8_000, 22_000),
    "podcast_sponsorship": (4_000, 11_000),
}

# Articles linked to a campaign by format.
CAMPAIGN_ARTICLE_COUNTS: dict[str, tuple[int, int]] = {
    "sponsored_section": (6, 12),
    "longform_series": (3, 6),
    "branded_newsletter": (0, 3),  # occasional companion pieces
    "event_partnership": (0, 0),
    "podcast_sponsorship": (0, 0),
}
