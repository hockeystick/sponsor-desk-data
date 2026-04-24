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
# Overall target ~12%; per-country split differs because diaspora readers
# skew bilingual and rest-of-world traffic is mostly English.
LANGUAGE_EN_SHARE: float = 0.12

LANGUAGE_EN_SHARE_BY_COUNTRY: dict[str, float] = {
    "CO":    0.10,
    "US":    0.15,
    "ES":    0.04,
    "MX":    0.03,
    "other": 0.40,
}

# Sessions are slightly larger than article pageviews because sessions
# include homepage/nav traffic. Spec's consistency rule: sum(pageviews)
# = 80-95% of sum(sessions) → sessions ≈ 1.15 × pageviews on average.
SESSION_PAGEVIEW_RATIO: float = 1.42

# Minimum session count to emit an audience_daily row. Keeps low-share
# dimension combos out of the table.
MIN_AUDIENCE_SESSIONS: int = 265

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

# Typical day-1 peak pageviews per section. Per-article variation applied
# via a log-normal multiplier with sigma PEAK_LOGNORMAL_SIGMA.
PEAK_PAGEVIEWS_BY_SECTION: dict[str, int] = {
    "actualidad":    1800,
    "politica":      2800,
    "clima":         3500,
    "ciudades":      2400,
    "investigacion": 5000,
    "cultura":       1400,
    "cafe_y_comida": 1500,
    "opinion":       2000,
}
PEAK_LOGNORMAL_SIGMA: float = 0.55

# Exponential decay half-life in days past day 1. Calibrated so the
# section's typical tail length lands around the MIN_PAGEVIEW_THRESHOLD
# cutoff given the peak size.
HALF_LIFE_BY_SECTION: dict[str, float] = {
    "actualidad":    1.0,
    "politica":      1.5,
    "clima":         4.5,
    "ciudades":      3.5,
    "investigacion": 8.0,
    "cultura":       3.0,
    "cafe_y_comida": 3.0,
    "opinion":       1.0,
}

# Minimum pageviews to record a row. Below this, the article is effectively
# dead for the day and we emit no row (matches the spec's "every day an
# article got traffic").
MIN_PAGEVIEW_THRESHOLD: int = 6

# Climate pieces get republished around news events. This triggers a
# secondary bump at a random day within CLIMATE_BUMP_DAYS for the share
# of climate articles controlled by CLIMATE_BUMP_PROB.
CLIMATE_BUMP_PROB: float = 0.30
CLIMATE_BUMP_DAYS: tuple[int, int] = (14, 45)
CLIMATE_BUMP_MAGNITUDE: tuple[float, float] = (0.3, 0.8)

# Viral outliers get a longer tail plus 2-3 secondary bumps.
VIRAL_TAIL_EXTENSION: tuple[float, float] = (1.5, 2.5)
VIRAL_SECONDARY_BUMP_COUNT: tuple[int, int] = (2, 3)
VIRAL_SECONDARY_BUMP_MAGNITUDE: tuple[float, float] = (0.5, 1.2)

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
# Calibrated so total opt-ins (~57,100) matches the sum of list target
# sizes Diario+Verde+Sobremesa = 57,000. A more aggressive 55/30/15 split
# would overshoot target list sizes by ~25%.
LIST_OVERLAP_SPLIT: dict[int, float] = {1: 0.76, 2: 0.21, 3: 0.03}

SUBSCRIBER_COUNTRY_WEIGHTS: dict[str, float] = {
    "CO": 0.75, "US": 0.10, "ES": 0.06, "MX": 0.03, "other": 0.06,
}

SUBSCRIBER_EN_SHARE_BY_COUNTRY: dict[str, float] = {
    "CO": 0.08, "US": 0.15, "ES": 0.04, "MX": 0.03, "other": 0.35,
}

# Year-on-year new-subscriber share. Outlet founded Jan 2018; gradual
# growth with COVID bump and post-pandemic plateau.
SUBSCRIBER_YEAR_GROWTH: dict[int, float] = {
    2018: 0.11, 2019: 0.09, 2020: 0.11, 2021: 0.13,
    2022: 0.16, 2023: 0.18, 2024: 0.13, 2025: 0.09,
}

# Days-since-reference-date that last_active_at falls into, per bucket.
# Reference date is ARTICLES_END.
LAST_ACTIVE_DAYS_BY_BUCKET: dict[str, tuple[int, int]] = {
    "hot":  (0, 7),
    "warm": (7, 60),
    "cold": (60, 540),
}

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
