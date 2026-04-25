"""Single source of truth for determinism and volume knobs.

Every tunable parameter for the generator lives here. If you want to change
volume, cadence, or distribution shape, adjust values in this module — do not
sprinkle magic numbers through the generators.
"""
from __future__ import annotations

from datetime import date

SEED: int = 20260425

ARTICLES_START: date = date(2024, 1, 1)
ARTICLES_END: date = date(2025, 12, 31)
AUDIENCE_START: date = ARTICLES_START
AUDIENCE_END: date = ARTICLES_END
NEWSLETTER_START: date = ARTICLES_START
NEWSLETTER_END: date = ARTICLES_END
CAMPAIGNS_START: date = date(2022, 1, 1)
CAMPAIGNS_END: date = date(2025, 12, 31)

ARTICLE_COUNT_TARGET: int = 5500
SUBSCRIBER_COUNT: int = 45_000
CAMPAIGN_COUNT: int = 72
VIRAL_OUTLIER_COUNT: int = 8

# Cadence: spec says 8-14 weekday, 3-5 weekend. Modeled as a mixture so
# most weekdays sit in a normal band; ~15% are news-heavy.
WEEKDAY_NORMAL_RANGE: tuple[int, int] = (8, 11)
WEEKDAY_BUSY_RANGE: tuple[int, int] = (12, 14)
WEEKDAY_BUSY_SHARE: float = 0.15
WEEKEND_ARTICLES_RANGE: tuple[int, int] = (3, 5)

# Section weight in editorial output. city_hall and housing carry the
# heaviest editorial weight per the outlet's stated coverage priorities.
SECTION_WEIGHTS: dict[str, float] = {
    "city_hall":      0.22,
    "housing":        0.16,
    "climate":        0.14,
    "transportation": 0.12,
    "business":       0.11,
    "culture":        0.09,
    "food_drink":     0.08,
    "opinion":        0.08,
}

# Audience country distribution. The Cascade Tribune is English-only,
# Portland-metro-centric, with diaspora readership in PNW + Bay Area + NYC
# accounted for via cities, not separate countries.
COUNTRY_WEIGHTS: dict[str, float] = {
    "US":    0.88,
    "CA":    0.04,
    "UK":    0.02,
    "other": 0.06,
}

# Within US: Oregon dominates, then Washington, California, NY, others.
US_STATE_WEIGHTS: dict[str, float] = {
    "OR":           0.62,
    "WA":           0.14,
    "CA":           0.10,
    "NY":           0.03,
    "other_state":  0.11,
}

# Tail-length ranges in days by section. Investigations-heavy sections
# (city_hall, housing) have longer tails; opinion decays fastest.
TAIL_DAYS_BY_SECTION: dict[str, tuple[int, int]] = {
    "city_hall":      (40, 80),
    "housing":        (40, 80),
    "climate":        (30, 60),
    "transportation": (20, 40),
    "business":       (15, 30),
    "culture":        (20, 40),
    "food_drink":     (20, 45),
    "opinion":        (5, 12),
}

VIRAL_MULTIPLIER_RANGE: tuple[float, float] = (10.0, 30.0)

# Typical day-1 peak pageviews per section. The flagship beats
# (city_hall, housing) drive the most traffic.
PEAK_PAGEVIEWS_BY_SECTION: dict[str, int] = {
    "city_hall":      4000,
    "housing":        3500,
    "climate":        3200,
    "transportation": 2400,
    "business":       2200,
    "culture":        1800,
    "food_drink":     2400,
    "opinion":        2400,
}
PEAK_LOGNORMAL_SIGMA: float = 0.55

HALF_LIFE_BY_SECTION: dict[str, float] = {
    "city_hall":      5.0,
    "housing":        5.0,
    "climate":        4.0,
    "transportation": 3.0,
    "business":       2.5,
    "culture":        3.0,
    "food_drink":     3.5,
    "opinion":        1.0,
}

MIN_PAGEVIEW_THRESHOLD: int = 6

# Climate pieces sometimes get a republishing bump (heat wave, fire
# season, atmospheric river coverage resurfaces with the next event).
CLIMATE_BUMP_PROB: float = 0.30
CLIMATE_BUMP_DAYS: tuple[int, int] = (14, 45)
CLIMATE_BUMP_MAGNITUDE: tuple[float, float] = (0.3, 0.8)

VIRAL_TAIL_EXTENSION: tuple[float, float] = (1.5, 2.5)
VIRAL_SECONDARY_BUMP_COUNT: tuple[int, int] = (2, 3)
VIRAL_SECONDARY_BUMP_MAGNITUDE: tuple[float, float] = (0.5, 1.2)

# ---- Audience -------------------------------------------------------------
SESSION_PAGEVIEW_RATIO: float = 1.42
MIN_AUDIENCE_SESSIONS: int = 360

LANGUAGE_ES_SHARE: float = 0.02  # small Spanish share, mostly East Portland

# ---- Newsletters: two only --------------------------------------------------
# Spec: The Daily Cascade (weekday morning) + Plate & Place (Friday food/culture).
NEWSLETTER_LIST_SIZES: dict[str, int] = {
    "daily_cascade": 38_000,
    "plate_place":   22_000,
}

OPEN_RATE_RANGES: dict[str, tuple[float, float]] = {
    "daily_cascade": (0.30, 0.40),
    "plate_place":   (0.36, 0.46),
}

CLICK_RATE_RANGES: dict[str, tuple[float, float]] = {
    "daily_cascade": (0.045, 0.090),
    "plate_place":   (0.060, 0.120),
}

UNSUB_RATE_RANGES: dict[str, tuple[float, float]] = {
    "daily_cascade": (0.0010, 0.0025),
    "plate_place":   (0.0006, 0.0016),
}

ENGAGEMENT_BUCKET_SPLIT: dict[str, float] = {
    "cold": 0.50,
    "warm": 0.35,
    "hot":  0.15,
}

# Two-list overlap: 67/33 split between subs on 1 list vs both lists.
# Calibrated so total opt-ins land near 60k (38k + 22k = 60k target).
LIST_OVERLAP_SPLIT: dict[int, float] = {1: 0.67, 2: 0.33}

SUBSCRIBER_COUNTRY_WEIGHTS: dict[str, float] = {
    "US": 0.92, "CA": 0.03, "UK": 0.02, "other": 0.03,
}

LAST_ACTIVE_DAYS_BY_BUCKET: dict[str, tuple[int, int]] = {
    "hot":  (0, 7),
    "warm": (7, 60),
    "cold": (60, 540),
}

SUBSCRIBER_YEAR_GROWTH: dict[int, float] = {
    2019: 0.10, 2020: 0.12, 2021: 0.14, 2022: 0.18,
    2023: 0.20, 2024: 0.16, 2025: 0.10,
}

# ---- Campaigns: USD instead of EUR -----------------------------------------
# Sectors structured to reflect a US local outlet's real sponsorship pipeline:
# ~50% regional businesses, ~25% national brands seeking PNW reach,
# ~20% institutional/civic funders, plus small state/local share.
CAMPAIGN_SECTOR_WEIGHTS: dict[str, float] = {
    "regional_food_beverage":         0.10,  # breweries, food brands, coffee
    "regional_finance":               0.08,  # credit unions, community banks
    "regional_healthcare":            0.07,  # health systems
    "regional_culture_arts":          0.07,  # museums, performing arts
    "regional_education":             0.05,  # universities
    "regional_business_services":     0.05,  # real estate, professional
    "regional_utility":               0.05,  # PGE, water, broadband
    "national_outdoor_lifestyle":     0.13,  # Patagonia/REI archetypes
    "national_consumer":              0.13,  # CPG, EV, national banks
    "pnw_community_foundation":       0.13,  # Meyer/OCF/Powell's CF archetypes
    "national_journalism_funder":     0.07,  # Knight/Lenfest
    "state_local_govt":               0.07,  # Oregon agencies, City of Portland
}

CAMPAIGN_FORMAT_WEIGHTS: dict[str, float] = {
    "sponsored_section":    0.32,
    "branded_newsletter":   0.22,
    "longform_series":      0.10,
    "event_partnership":    0.18,
    "podcast_sponsorship":  0.08,
    "underwriting":         0.10,  # NPR-style year-long underwriting (US-specific)
}

CAMPAIGN_FEE_RANGES: dict[str, tuple[int, int]] = {
    "sponsored_section":    (15_000, 60_000),
    "branded_newsletter":   ( 5_000, 12_000),
    "longform_series":      (20_000, 60_000),
    "event_partnership":    (10_000, 28_000),
    "podcast_sponsorship":  ( 6_000, 14_000),
    "underwriting":         (40_000, 200_000),  # six-figure anchor commitments
}

CAMPAIGN_ARTICLE_COUNTS: dict[str, tuple[int, int]] = {
    "sponsored_section":    (6, 12),
    "longform_series":      (3, 6),
    "branded_newsletter":   (0, 3),
    "event_partnership":    (0, 0),
    "podcast_sponsorship":  (0, 0),
    "underwriting":         (0, 0),
}

# Share of campaigns that didn't go to plan. Drives the outcome_status
# field. The brief tool needs to see honest history, not success-theatre.
CAMPAIGN_OUTCOME_WEIGHTS: dict[str, float] = {
    "completed":       0.78,
    "underdelivered":  0.10,  # delivered fewer impressions or below-band engagement
    "did_not_renew":   0.08,  # finished as planned, sponsor walked
    "ended_early":     0.04,  # cut short by either side
}

# Headline sponsors that must each receive at least N campaigns in the
# past_campaigns generation. These are the prospects/partners the
# downstream brief tool will be working with — they need a track record
# the tool can cite.
HEADLINE_SPONSORS: dict[str, tuple[str, int]] = {
    # sponsor_name → (sector, min campaigns)
    "Portland General Energy":         ("regional_utility",          4),
    "Powell's Community Foundation":   ("pnw_community_foundation",  4),
    "Cascadia Credit Union":           ("regional_finance",          3),
    "Stumptown Roasters Co-op":        ("regional_food_beverage",    3),
}
