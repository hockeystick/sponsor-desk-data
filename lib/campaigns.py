"""Past sponsorship campaigns + campaign↔article bridge + pricing doc.

Generators wired together:
1. `build_campaigns` reserves a minimum number of slots for each
   headline sponsor (Portland General Energy, Powell's Community Foundation,
   Cascadia Credit Union, Stumptown Roasters Co-op), then fills the rest
   with random draws across 12 sectors weighted to a US local-news pipeline.
2. `build_campaign_articles_and_summaries` links applicable campaigns to
   the articles that ran under them and writes an outcome-aware
   English summary per campaign.
3. Articles receive a `sponsor_tag` update so the articles table
   self-links to the sponsor name.
4. `write_pricing_reference` emits `data/pricing_reference.md` — a
   static USD rate-card doc anchored to the new outlet.

Outcome modeling: 22% of campaigns land in a non-completed outcome
state (`underdelivered`, `did_not_renew`, `ended_early`) per the
CAMPAIGN_OUTCOME_WEIGHTS distribution. Summaries reflect the outcome
honestly so the brief tool can show real history, not success-theatre.
"""
from __future__ import annotations

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

from lib import config

CAMPAIGNS_DDL = """
CREATE TABLE past_campaigns (
    campaign_id              INTEGER PRIMARY KEY,
    sponsor_name             TEXT NOT NULL,
    sponsor_sector           TEXT NOT NULL,
    start_date               TEXT NOT NULL,
    end_date                 TEXT NOT NULL,
    format                   TEXT NOT NULL,
    fee_usd                  INTEGER NOT NULL,
    impressions_delivered    INTEGER NOT NULL,
    engagement_rate          REAL NOT NULL,
    outcome_status           TEXT NOT NULL,
    post_campaign_summary    TEXT NOT NULL
);
CREATE INDEX idx_camp_sector ON past_campaigns(sponsor_sector);
CREATE INDEX idx_camp_format ON past_campaigns(format);
CREATE INDEX idx_camp_sponsor ON past_campaigns(sponsor_name);
CREATE INDEX idx_camp_outcome ON past_campaigns(outcome_status);

CREATE TABLE campaign_articles (
    campaign_id INTEGER NOT NULL REFERENCES past_campaigns(campaign_id),
    article_id  INTEGER NOT NULL REFERENCES articles(article_id),
    PRIMARY KEY (campaign_id, article_id)
);
CREATE INDEX idx_ca_article ON campaign_articles(article_id);
"""

# Fictional sponsor pools per sector. The four headline sponsors
# (PGE, Powell's CF, Cascadia CU, Stumptown) are included in their
# sector pools — they get random draws on top of their reserved
# minimums. All names are fictional analogues; profile.md files in
# /sponsors include the disclaimer.
_SPONSORS_BY_SECTOR: dict[str, list[str]] = {
    "regional_food_beverage": [
        "Stumptown Roasters Co-op",
        "Cascade Market Co-op",
        "Willamette Brewers Co-op",
        "Salt & Cedar Collective",
        "Pacific Pinot Collective",
        "Bull Run Cider",
        "Bonny Slope Bakehouse",
        "Tualatin Valley Wines",
    ],
    "regional_finance": [
        "Cascadia Credit Union",
        "Onpoint Cooperative",
        "Willamette Mutual Bank",
        "Albina Trust Mutual",
        "First Tech Federal Mutual",
        "Columbia Pacific Bank",
    ],
    "regional_healthcare": [
        "Pacific Northwest Health",
        "Providence Cascadia Health",
        "Kaiser Cascade Network",
        "Legacy West Health",
        "Adventist Cascade Medical",
    ],
    "regional_culture_arts": [
        "Portland Museum of Art",
        "Cascade Center Stage",
        "Cascade Symphony",
        "Literary Arts Cascade",
        "Northwest Film Center",
        "Japanese Garden of Portland",
    ],
    "regional_education": [
        "Portland State Foundation",
        "Reed College Press",
        "Lewis & Clark Foundation",
        "University of Portland Foundation",
        "OHSU Cascade Foundation",
    ],
    "regional_business_services": [
        "Cascadia Realty Group",
        "Pacific Tower Development",
        "Stoel Rivers Law",
        "Holland & Knight Cascade",
        "Schwabe Williams",
    ],
    "regional_utility": [
        "Portland General Energy",
        "NW Natural Gas",
        "Northwest Natural Energy",
        "Bonneville Pacific Power",
    ],
    "national_outdoor_lifestyle": [
        "Cascadia Outfitters Co-op",
        "Patagonia Pacific Northwest",
        "Columbia Mountain Apparel",
        "Filson Northwest",
        "Black Diamond Cascade",
        "KEEN Pacific",
    ],
    "national_consumer": [
        "Subaru Pacific",
        "Toyota Northwest",
        "Whole Earth Foods",
        "Allbirds Pacific",
        "Seventh Generation Pacific",
        "Charles Schwab Pacific",
        "US Bank Pacific Northwest",
    ],
    "pnw_community_foundation": [
        "Powell's Community Foundation",
        "Meyer Northwest Trust",
        "Oregon Community Foundation Cascade",
        "Collins Family Foundation",
        "Spirit Mountain Cascade Fund",
        "Pacific Northwest Foundation",
    ],
    "national_journalism_funder": [
        "Knight Pacific Initiative",
        "Lenfest Foundation Cascade",
        "Lever Cascade",
        "NewsMatch Cascade",
        "Local Media Association",
    ],
    "state_local_govt": [
        "City of Portland Office of Sustainability",
        "Oregon Department of Transportation",
        "Multnomah County Library",
        "Travel Oregon",
        "Oregon Health Authority",
    ],
}

# Sector ↔ preferred article sections for bridge linking.
_SECTOR_PREFERRED_SECTIONS: dict[str, list[str]] = {
    "regional_food_beverage":     ["food_drink", "culture", "business"],
    "regional_finance":           ["business", "housing", "city_hall"],
    "regional_healthcare":        ["city_hall", "housing", "business"],
    "regional_culture_arts":      ["culture", "food_drink"],
    "regional_education":         ["city_hall", "culture", "business"],
    "regional_business_services": ["business", "housing", "transportation"],
    "regional_utility":           ["climate", "city_hall", "business"],
    "national_outdoor_lifestyle": ["climate", "culture", "transportation"],
    "national_consumer":          ["business", "culture", "food_drink"],
    "pnw_community_foundation":   ["culture", "city_hall", "housing"],
    "national_journalism_funder": ["city_hall", "housing", "climate"],
    "state_local_govt":           ["city_hall", "transportation", "climate"],
}

# Topic-phrase pool per sector — threaded into the post-campaign summary.
_SECTOR_TOPICS: dict[str, list[str]] = {
    "regional_food_beverage": [
        "Portland's specialty-coffee scene",
        "the cooperative-bakery renaissance",
        "small-format breweries in Slabtown",
        "Oregon pinot country",
        "the Friday-night neighborhood guide",
    ],
    "regional_finance": [
        "first-time homebuyer programs",
        "financial literacy for renters",
        "small-business banking after the SBA shift",
        "credit-union savings products",
        "sustainable lending in Oregon",
    ],
    "regional_healthcare": [
        "behavioral-health access in East Portland",
        "maternal-health outcomes in the Tri-County",
        "rural medicine in the Willamette Valley",
        "vaccine equity programs",
        "pediatric urgent care",
    ],
    "regional_culture_arts": [
        "K-12 arts education funding",
        "the independent literary scene",
        "performing arts post-pandemic recovery",
        "regional artist residencies",
        "Title I free-day programs",
    ],
    "regional_education": [
        "civic education in PPS",
        "first-gen college pathways",
        "community-college transfer rates",
        "research at Portland State",
        "K-16 mathematics initiatives",
    ],
    "regional_business_services": [
        "zoning reform",
        "transit-oriented development",
        "the downtown vacancy puzzle",
        "co-op ownership models",
        "the Pearl District after the office downturn",
    ],
    "regional_utility": [
        "the Climate Protection Program rollout",
        "summer grid reliability",
        "EV adoption curves",
        "gas-to-electric residential conversion",
        "wildfire season mitigation",
    ],
    "national_outdoor_lifestyle": [
        "public-lands access",
        "outdoor-recreation equity",
        "sustainable apparel sourcing",
        "Cascade and Coast Range trail networks",
        "Oregon's adaptive recreation movement",
    ],
    "national_consumer": [
        "regional manufacturing",
        "B-corp profiles",
        "climate-conscious consumption",
        "EV market expansion",
        "small-batch brand growth",
    ],
    "pnw_community_foundation": [
        "Black-led nonprofits in Portland",
        "civic-infrastructure resilience",
        "journalism sustainability",
        "Indigenous-led environmental programs",
        "community-driven climate adaptation",
    ],
    "national_journalism_funder": [
        "investigative journalism on housing",
        "local news experiments",
        "cross-border reporting on climate",
        "civic-information ecosystems",
        "newsroom sustainability",
    ],
    "state_local_govt": [
        "the Climate Protection Program rollout",
        "Vision Zero implementation",
        "the public-records modernization push",
        "Travel Oregon's regional partnerships",
        "Oregon Health Authority's behavioral-health build-out",
    ],
}

_FORMAT_DURATION_WEEKS: dict[str, tuple[int, int]] = {
    "sponsored_section":   (4, 12),
    "branded_newsletter":  (1, 3),
    "longform_series":     (8, 24),
    "event_partnership":   (1, 4),
    "podcast_sponsorship": (4, 8),
    "underwriting":        (26, 52),  # 6-12 months
}

_FORMAT_IMPRESSIONS_RANGE: dict[str, tuple[int, int]] = {
    "sponsored_section":   (180_000, 1_100_000),
    "branded_newsletter":  ( 28_000,    140_000),
    "longform_series":     (320_000, 2_000_000),
    "event_partnership":   ( 22_000,     90_000),
    "podcast_sponsorship": ( 35_000,    210_000),
    "underwriting":        (800_000,  4_500_000),  # year-long high-frequency
}

_FORMAT_ENGAGEMENT_RANGE: dict[str, tuple[float, float]] = {
    "sponsored_section":   (0.025, 0.080),
    "branded_newsletter":  (0.040, 0.130),
    "longform_series":     (0.050, 0.150),
    "event_partnership":   (0.150, 0.350),
    "podcast_sponsorship": (0.060, 0.180),
    "underwriting":        (0.012, 0.040),  # low engagement, broad reach
}


def _weighted_choice(rng: random.Random, mapping: dict[str, float]) -> str:
    items = list(mapping.items())
    total = sum(w for _, w in items)
    r = rng.random() * total
    cum = 0.0
    for k, w in items:
        cum += w
        if r <= cum:
            return k
    return items[-1][0]


def _pick_start_date(rng: random.Random) -> date:
    span_days = (config.CAMPAIGNS_END - config.CAMPAIGNS_START).days
    offset = rng.randint(0, max(1, span_days - 30))
    return config.CAMPAIGNS_START + timedelta(days=offset)


def _fee(rng: random.Random, fmt: str, weeks: int) -> int:
    lo, hi = config.CAMPAIGN_FEE_RANGES[fmt]
    dur_lo, dur_hi = _FORMAT_DURATION_WEEKS[fmt]
    dur_span = max(1, dur_hi - dur_lo)
    duration_factor = 0.6 + 0.8 * ((weeks - dur_lo) / dur_span)
    base = lo + (hi - lo) * rng.random()
    fee = base * duration_factor
    return max(lo, min(hi, int(fee / 100) * 100))


def _build_one_campaign(
    rng: random.Random, sector: str, sponsor: str | None = None
) -> dict:
    """Build a single campaign dict (without campaign_id, summary, outcome_status —
    those are set later)."""
    fmt = _weighted_choice(rng, config.CAMPAIGN_FORMAT_WEIGHTS)
    start = _pick_start_date(rng)
    dur_lo, dur_hi = _FORMAT_DURATION_WEEKS[fmt]
    weeks = rng.randint(dur_lo, dur_hi)
    end = start + timedelta(weeks=weeks)
    if end > config.CAMPAIGNS_END:
        end = config.CAMPAIGNS_END
        weeks = max(1, (end - start).days // 7)
    if sponsor is None:
        sponsor = rng.choice(_SPONSORS_BY_SECTOR[sector])
    imp_lo, imp_hi = _FORMAT_IMPRESSIONS_RANGE[fmt]
    impressions = rng.randint(imp_lo, imp_hi)
    eng_lo, eng_hi = _FORMAT_ENGAGEMENT_RANGE[fmt]
    engagement = round(rng.uniform(eng_lo, eng_hi), 4)
    return {
        "sponsor_name": sponsor,
        "sponsor_sector": sector,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "format": fmt,
        "fee_usd": _fee(rng, fmt, weeks),
        "impressions_delivered": impressions,
        "engagement_rate": engagement,
        "weeks": weeks,
    }


def _apply_outcome(rng: random.Random, c: dict) -> None:
    """Set outcome_status and adjust impressions/engagement/end_date in
    place to reflect honest history. Mutates c."""
    outcome = _weighted_choice(rng, config.CAMPAIGN_OUTCOME_WEIGHTS)
    c["outcome_status"] = outcome

    if outcome == "underdelivered":
        # Delivered fewer impressions, engagement at the low end of the band.
        c["impressions_delivered"] = int(c["impressions_delivered"] * rng.uniform(0.55, 0.78))
        eng_lo, _ = _FORMAT_ENGAGEMENT_RANGE[c["format"]]
        c["engagement_rate"] = round(eng_lo * rng.uniform(0.85, 1.05), 4)
    elif outcome == "ended_early":
        # Cut short — recompute end_date and scale impressions down.
        actual_weeks = max(1, int(c["weeks"] * rng.uniform(0.30, 0.60)))
        new_end = date.fromisoformat(c["start_date"]) + timedelta(weeks=actual_weeks)
        c["end_date"] = new_end.isoformat()
        c["impressions_delivered"] = int(
            c["impressions_delivered"] * actual_weeks / max(1, c["weeks"])
        )
        c["weeks"] = actual_weeks
    # `did_not_renew` and `completed` keep numbers as drawn.


def build_campaigns(rng: random.Random) -> list[dict]:
    """72 campaigns with the four headline sponsors guaranteed minimum
    representation, then random fills."""
    campaigns: list[dict] = []

    # Reserved slots for each headline sponsor.
    for sponsor, (sector, min_n) in config.HEADLINE_SPONSORS.items():
        for _ in range(min_n):
            campaigns.append(_build_one_campaign(rng, sector, sponsor=sponsor))

    # Random fill for the rest.
    reserved = sum(n for _, n in config.HEADLINE_SPONSORS.values())
    for _ in range(config.CAMPAIGN_COUNT - reserved):
        sector = _weighted_choice(rng, config.CAMPAIGN_SECTOR_WEIGHTS)
        campaigns.append(_build_one_campaign(rng, sector))

    # Apply outcome status (mutates in place).
    for c in campaigns:
        _apply_outcome(rng, c)

    campaigns.sort(key=lambda c: c["start_date"])
    for i, c in enumerate(campaigns, 1):
        c["campaign_id"] = i
    return campaigns


# ---- summaries --------------------------------------------------------------

def _us_num(n: int) -> str:
    return f"{n:,}"  # US-style: 1,234,567


def _summary_sponsored_section(rng, c, topic, n_pieces):
    return (
        f"Across {c['weeks']} weeks, The Cascade Tribune produced a "
        f"sponsored section with {c['sponsor_name']} on {topic}, publishing "
        f"{n_pieces} original articles. The series accumulated "
        f"{_us_num(c['impressions_delivered'])} impressions with a "
        f"{c['engagement_rate']*100:.1f}% engagement rate."
    )


def _summary_longform(rng, c, topic, n_pieces):
    return (
        f"A {n_pieces}-part longform series on {topic}, co-funded by "
        f"{c['sponsor_name']}, ran across {c['weeks']} weeks. The series "
        f"reached {_us_num(c['impressions_delivered'])} readers with a "
        f"{c['engagement_rate']*100:.1f}% engagement rate."
    )


def _summary_branded_newsletter(rng, c, topic, n_pieces):
    nl = rng.choice(["The Daily Cascade", "Plate & Place"])
    return (
        f"A sponsored edition of {nl} dedicated to {topic}, underwritten by "
        f"{c['sponsor_name']}, reached {_us_num(c['impressions_delivered'])} "
        f"subscribers with a {c['engagement_rate']*100:.1f}% open rate."
    )


def _summary_event(rng, c, topic, n_pieces):
    venue = rng.choice([
        "the Alberta Rose Theatre", "Revolution Hall", "Holocene",
        "the Old Church Concert Hall", "the Portland Art Museum auditorium",
    ])
    return (
        f"{c['sponsor_name']} co-presented The Cascade Tribune's panel "
        f"on {topic} at {venue}, with in-room and livestreamed reach "
        f"of {_us_num(c['impressions_delivered'])}. Measured engagement "
        f"was {c['engagement_rate']*100:.1f}%."
    )


def _summary_podcast(rng, c, topic, n_pieces):
    eps = max(4, c["weeks"])
    return (
        f"A {c['weeks']}-week podcast sponsorship ({eps} episodes) with "
        f"{c['sponsor_name']}, focused on {topic}. Episodes accumulated "
        f"{_us_num(c['impressions_delivered'])} listens with a "
        f"{c['engagement_rate']*100:.1f}% click-through rate on host-read placements."
    )


def _summary_underwriting(rng, c, topic, n_pieces):
    return (
        f"A {c['weeks']}-week underwriting partnership with {c['sponsor_name']}, "
        f"providing low-frequency sponsor recognition across The Cascade "
        f"Tribune's flagship pages, daily newsletter, and event programming. "
        f"Total estimated impression reach: {_us_num(c['impressions_delivered'])}; "
        f"average click-through {c['engagement_rate']*100:.1f}%."
    )


_SUMMARY_BUILDERS = {
    "sponsored_section":   _summary_sponsored_section,
    "longform_series":     _summary_longform,
    "branded_newsletter":  _summary_branded_newsletter,
    "event_partnership":   _summary_event,
    "podcast_sponsorship": _summary_podcast,
    "underwriting":        _summary_underwriting,
}


def _outcome_clause(rng: random.Random, c: dict, n_pieces: int) -> str:
    sector = c["sponsor_sector"]
    outcome = c["outcome_status"]

    if outcome == "completed":
        return _completed_outcome(rng, c, sector)
    if outcome == "underdelivered":
        return _underdelivered_outcome(rng, c)
    if outcome == "ended_early":
        return _ended_early_outcome(rng, c)
    if outcome == "did_not_renew":
        return _did_not_renew_outcome(rng, c)
    return ""


def _completed_outcome(rng: random.Random, c: dict, sector: str) -> str:
    pool = {
        "regional_food_beverage": [
            f"{c['sponsor_name']} reported a {rng.randint(8, 22)}% lift in foot-traffic "
            f"to participating locations during the campaign window.",
            f"The series drove {_us_num(rng.randint(280, 1400))} clicks to the sponsor's storefront finder.",
            "Three pieces from the series were syndicated by Eater Portland and PDX Monthly.",
        ],
        "regional_finance": [
            f"{c['sponsor_name']} reported {_us_num(rng.randint(180, 900))} new "
            "membership applications attributable to the series.",
            "The campaign supported the sponsor's first-time homebuyer outreach in East Portland.",
            "The sponsor cited the series in its 2025 community reinvestment filing.",
        ],
        "regional_healthcare": [
            f"The campaign supported the sponsor's outreach to {_us_num(rng.randint(2_000, 9_000))} "
            "previously unenrolled patients.",
            "The series was distributed across the sponsor's network of community partners.",
            "Outcomes data from the series fed into the sponsor's annual community health needs assessment.",
        ],
        "regional_culture_arts": [
            f"The series drove {_us_num(rng.randint(400, 1_800))} ticket inquiries during its run.",
            "Two pieces won regional arts journalism awards and were reprinted by the sponsor.",
            "The campaign accompanied the launch of the sponsor's expanded K-12 programming.",
        ],
        "regional_education": [
            f"{c['sponsor_name']} reported {_us_num(rng.randint(120, 600))} prospective-student "
            "inquiries tied to the campaign window.",
            "The series was incorporated into freshman seminar materials at the sponsor institution.",
            "Coverage informed the sponsor's regional outreach strategy for fall 2026.",
        ],
        "regional_business_services": [
            f"The sponsor reported {_us_num(rng.randint(40, 200))} "
            "qualified leads attributable to the campaign.",
            "The series accompanied the sponsor's office expansion into Beaverton.",
            "Two pieces were repurposed for the sponsor's industry-association presentations.",
        ],
        "regional_utility": [
            "The sponsor cited the series in its rate-case filing as evidence of customer education investment.",
            f"{_us_num(rng.randint(800, 3_500))} customers signed up for the sponsor's "
            "energy-efficiency rebate program during the campaign.",
            "Coverage was distributed to the sponsor's residential customer base via bill insert.",
        ],
        "national_outdoor_lifestyle": [
            f"The sponsor reported {_us_num(rng.randint(2_000, 12_000))} engagements "
            "with their PNW campaign hub during the run.",
            "Two pieces were syndicated by REI Outdoor Journal and Outside.",
            "The campaign supported the sponsor's launch of its Cascade-region storytelling hub.",
        ],
        "national_consumer": [
            f"The sponsor reported a {rng.randint(6, 16)}% lift in PNW brand affinity scores.",
            f"The series generated {_us_num(rng.randint(800, 4_500))} qualified leads.",
            "Coverage accompanied the sponsor's regional product launch.",
        ],
        "pnw_community_foundation": [
            "The series was incorporated into the foundation's annual report.",
            "Two pieces were cited by Multnomah County in subsequent budget testimony.",
            "The campaign supported the launch of the foundation's regional grantee portfolio.",
        ],
        "national_journalism_funder": [
            "Three pieces were re-published in the funder's national best-of digest.",
            "The campaign satisfied the funder's matching-gift program requirements.",
            "Coverage was used in the funder's annual conference proceedings.",
        ],
        "state_local_govt": [
            "The campaign satisfied the agency's public-information mandate for the program.",
            f"Coverage reached approximately {_us_num(rng.randint(15_000, 80_000))} "
            "Oregon households through cross-channel distribution.",
            "The series informed an expanded second-year budget request.",
        ],
    }
    return rng.choice(pool[sector])


def _underdelivered_outcome(rng: random.Random, c: dict) -> str:
    return rng.choice([
        "Delivered impressions came in below the contracted target; the sponsor and editorial "
        "agreed on a partial credit toward a future activation.",
        "Engagement landed at the bottom of the format's typical band, attributed to a mid-run "
        "competing news cycle. The sponsor accepted the result and elected not to renew at the "
        "same volume.",
        "The campaign delivered against its impression target but engagement fell short. Post-mortem "
        "identified topic-fit drift between the original brief and what editorial actually produced.",
        "Performance fell short of projections; both parties signed off on a make-good event in Q1 of the following year.",
    ])


def _ended_early_outcome(rng: random.Random, c: dict) -> str:
    return rng.choice([
        f"The sponsor pulled the campaign in week {max(2, c['weeks'])} citing internal budget revisions; "
        "remaining commitments were settled at pro-rated terms.",
        "The campaign ended ahead of schedule by mutual agreement after a topical conflict surfaced "
        "with editorial coverage outside the sponsored series.",
        f"The sponsor concluded the campaign early after a strategic priority shift. "
        f"Pro-rated impressions were credited.",
        "Editorial flagged a conflict-of-interest concern partway through the run; both parties "
        "concluded the campaign at the natural break point.",
    ])


def _did_not_renew_outcome(rng: random.Random, c: dict) -> str:
    return rng.choice([
        "The campaign delivered against its targets, but the sponsor opted not to renew, citing "
        "a planned shift to a different audience strategy.",
        "Strong delivery, no renewal — the sponsor moved its 2026 budget to a national platform partner.",
        "Met all delivery targets. The sponsor did not renew in the following budget cycle; "
        "the relationship remains warm.",
        "Campaign closed on plan; sponsor walked. Internal post-mortem flagged a mismatch between "
        "the sponsor's brand-building goals and our direct-response measurement framework.",
    ])


def build_campaign_articles_and_summaries(
    rng: random.Random,
    campaigns: list[dict],
    articles: list[dict],
) -> tuple[list[dict], list[dict]]:
    articles_by_date: dict[str, list[dict]] = {}
    for a in articles:
        d = a["published_at"][:10]
        articles_by_date.setdefault(d, []).append(a)

    bridge: list[dict] = []

    for c in campaigns:
        fmt = c["format"]
        n_lo, n_hi = config.CAMPAIGN_ARTICLE_COUNTS[fmt]
        n_target = rng.randint(n_lo, n_hi) if n_hi > 0 else 0
        # ended_early campaigns produce fewer articles.
        if c["outcome_status"] == "ended_early" and n_target > 0:
            n_target = max(1, int(n_target * 0.5))

        linked_ids: list[int] = []
        if n_target > 0:
            start = c["start_date"]
            end = c["end_date"]
            preferred = set(_SECTOR_PREFERRED_SECTIONS[c["sponsor_sector"]])
            candidates: list[dict] = []
            for day_str in sorted(articles_by_date.keys()):
                if start <= day_str <= end:
                    for a in articles_by_date[day_str]:
                        if a["sponsor_tag"] is None and a["section"] in preferred:
                            candidates.append(a)
            if len(candidates) < n_target:
                extras = []
                for day_str in sorted(articles_by_date.keys()):
                    if start <= day_str <= end:
                        for a in articles_by_date[day_str]:
                            if a["sponsor_tag"] is None and a["section"] not in preferred:
                                extras.append(a)
                candidates.extend(extras)

            to_pick = min(n_target, len(candidates))
            if to_pick > 0:
                chosen = rng.sample(candidates, to_pick)
                for a in chosen:
                    a["sponsor_tag"] = c["sponsor_name"]
                    linked_ids.append(a["article_id"])
                    bridge.append(
                        {"campaign_id": c["campaign_id"], "article_id": a["article_id"]}
                    )

        topic = rng.choice(_SECTOR_TOPICS[c["sponsor_sector"]])
        base_summary = _SUMMARY_BUILDERS[fmt](rng, c, topic, len(linked_ids) or n_target)
        outcome_text = _outcome_clause(rng, c, len(linked_ids))
        c["post_campaign_summary"] = f"{base_summary} {outcome_text}".strip()

    for c in campaigns:
        c.pop("weeks", None)

    bridge.sort(key=lambda r: (r["campaign_id"], r["article_id"]))
    return bridge, campaigns


def write_campaigns(
    conn: sqlite3.Connection, campaigns: list[dict], bridge: list[dict]
) -> None:
    conn.executescript(CAMPAIGNS_DDL)
    conn.executemany(
        "INSERT INTO past_campaigns (campaign_id, sponsor_name, sponsor_sector, "
        "start_date, end_date, format, fee_usd, impressions_delivered, "
        "engagement_rate, outcome_status, post_campaign_summary) VALUES "
        "(:campaign_id, :sponsor_name, :sponsor_sector, :start_date, :end_date, "
        ":format, :fee_usd, :impressions_delivered, :engagement_rate, "
        ":outcome_status, :post_campaign_summary)",
        campaigns,
    )
    conn.executemany(
        "INSERT INTO campaign_articles (campaign_id, article_id) "
        "VALUES (:campaign_id, :article_id)",
        bridge,
    )
    sponsor_by_campaign = {c["campaign_id"]: c["sponsor_name"] for c in campaigns}
    conn.executemany(
        "UPDATE articles SET sponsor_tag = ? WHERE article_id = ?",
        [(sponsor_by_campaign[r["campaign_id"]], r["article_id"]) for r in bridge],
    )


PRICING_REFERENCE_MD = """\
# The Cascade Tribune — Sponsorship Rate Card 2026

_Prices in USD. Valid for contracts signed Q1–Q3 2026. Regional add-ons
available on request. All sponsored work carries disclosure labelling
per IAB standards. Editorial control sits with the newsroom; sponsors
receive no pre-publication review or takedown rights._

## Editorial sponsorship formats

### Sponsored Section

A disclosure-labelled branded-content hub of 6–12 original articles
produced by The Cascade Tribune's editorial team. Sponsor defines the
scope of subject matter in advance; editorial retains full control
over reporting and selection. Best for medium-arc commitments on a
clearly delimited topic.

- Duration: 4–12 weeks
- Base fee: $15,000–$60,000
- Median delivered impressions: ~520,000
- Includes: anchor piece, 5–11 follow-ups, one newsletter feature, one social campaign
- Strongest sector fit: utilities, financial services, philanthropy, healthcare

### Longform Series

A 3–6 piece investigative or reportage series, typically produced
under an editorial grant from a foundation, civic funder, or
public-interest sponsor. Longer production timeline; heavier per-piece lift.

- Duration: 8–24 weeks
- Base fee: $20,000–$60,000
- Median impressions: ~900,000
- Includes: 3–6 longform pieces, editorial launch event, one accompanying podcast episode
- Strongest sector fit: community foundations, journalism funders, healthcare

### Branded Newsletter

A single sponsored edition or 2–3 edition arc inside The Daily Cascade
or Plate & Place. Highest direct engagement per impression thanks to
the opt-in list.

- Duration: 1–3 weeks (per arc)
- Base fee: $5,000–$12,000 per send
- Median impressions: ~50,000
- Includes: custom subject line, one creative slot, one promoted link with click tracking
- Strongest sector fit: any — particularly consumer brands, food & drink, finance

### Event Partnership

Co-produced panel or in-person event with livestream and recap
coverage. Format flexible (breakfast panel, evening discussion,
festival co-presentation, member meetup).

- Duration: 1–4 weeks including promotion
- Base fee: $10,000–$28,000
- Median in-room + stream attendance: ~55,000 impressions
- Includes: venue coordination, moderation, recorded panel, recap newsletter, social clips
- Strongest sector fit: community foundations, arts institutions, healthcare, regional banks

### Podcast Sponsorship

Full or partial sponsorship of a 4–8 episode podcast run, with
host-read placements and optional episode co-production. Cascade
Tribune's podcast cadence is bi-weekly during sponsor windows.

- Duration: 4–8 weeks
- Base fee: $6,000–$14,000
- Median listens over run: ~110,000
- Includes: pre-roll + mid-roll host reads, show-notes placement, social teasers
- Strongest sector fit: outdoor/lifestyle, financial services, food & drink

### Underwriting

A year-long brand-building partnership through low-frequency,
high-trust placement: weekly sponsor banner on flagship pages,
monthly recognition in The Daily Cascade, named acknowledgment at
all live events. No created content; this is brand presence, not
sponsored journalism.

- Duration: 26–52 weeks
- Base fee: $40,000–$200,000 (tiered)
- Median annualized impressions: ~2.2M
- Strongest sector fit: anchor sponsors — utilities, foundations, large regional employers

## Add-ons

| Add-on                                    | Uplift             |
| ----------------------------------------- | ------------------ |
| Newsletter cross-promotion (other list)   | +$2,500            |
| Post-campaign engagement audit & report   | +$1,800            |
| Spanish-language translation of pieces    | +12% of base fee   |
| Extended social campaign (8 weeks)        | +$3,200            |
| In-person sponsor recognition at one event| +$1,500            |

## Notes

- All formats include disclosure labelling per IAB standards.
- Minimum booking: $5,000.
- Editorial independence is non-negotiable: no pre-publication review, no takedown rights, no veto.
- Foundation-funded reportage (common in our community-foundation and
  journalism-funder partnerships) is priced separately from the rate
  card above and follows a project-budget model.
- Six-figure commitments ($100k+) trigger an annual partnership review
  with both the publisher and the editor in chief; the goal is honest
  alignment over time, not perpetual renewal.
"""


def write_pricing_reference(path: Path) -> None:
    path.write_text(PRICING_REFERENCE_MD, encoding="utf-8")
