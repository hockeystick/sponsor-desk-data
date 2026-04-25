"""Controlled vocabularies. The Portland voice of the dataset lives here.

All lists must stay in deterministic order — they are iterated by position
and any reorder will shift article assignments across a regenerated dataset.
"""
from __future__ import annotations

SECTIONS: list[str] = [
    "city_hall",
    "housing",
    "climate",
    "transportation",
    "business",
    "culture",
    "food_drink",
    "opinion",
]

# 52 topic tags spanning Portland-specific civics, regional issues,
# US-civic-life beats, climate/environment, transit, and culture/food.
# Tags are deliberately specific — generic "politics" / "environment" tags
# would be useless for the brief tool's audience-matching.
TOPIC_TAGS: list[str] = [
    # city government & accountability (12)
    "city_council", "mayors_office", "multnomah_county", "washington_county",
    "clackamas_county", "ranked_choice_voting", "charter_reform", "city_audit",
    "public_records", "ethics_commission", "police_oversight", "ppb_reform",
    # housing & homelessness (10)
    "zoning", "adu", "rent_stabilization", "evictions",
    "homelessness", "supportive_housing", "encampments", "joint_office",
    "housing_authority", "tenant_protections",
    # climate & environment (10)
    "wildfires", "fire_season", "atmospheric_river", "heat_dome",
    "salmon", "columbia_river", "decarbonization", "gas_phaseout",
    "climate_resilience", "oregon_climate_action_plan",
    # transportation (8)
    "trimet", "max_light_rail", "bike_infrastructure", "vision_zero",
    "freight", "ev_charging", "parking_reform", "bridge_replacement",
    # business & economy (5)
    "small_business", "layoffs", "openings_closings", "downtown",
    "port_of_portland",
    # culture & food (10)
    "indie_music", "performing_arts", "museums",
    "lit_scene", "k12_arts",
    "new_restaurants", "craft_beer", "wine_country",
    "coffee_culture", "farmers_markets",
    # cross-cutting Oregon civic life (5)
    "measure_110", "fentanyl_crisis", "oregon_legislature",
    "ballot_measures", "public_safety",
]

# Tags that plausibly co-occur within a given section.
SECTION_TAG_AFFINITY: dict[str, list[str]] = {
    "city_hall": [
        "city_council", "mayors_office", "multnomah_county", "washington_county",
        "clackamas_county", "ranked_choice_voting", "charter_reform",
        "city_audit", "public_records", "ethics_commission",
        "police_oversight", "ppb_reform", "ballot_measures",
        "oregon_legislature", "public_safety",
    ],
    "housing": [
        "zoning", "adu", "rent_stabilization", "evictions",
        "homelessness", "supportive_housing", "encampments", "joint_office",
        "housing_authority", "tenant_protections", "city_council",
        "multnomah_county",
    ],
    "climate": [
        "wildfires", "fire_season", "atmospheric_river", "heat_dome",
        "salmon", "columbia_river", "decarbonization", "gas_phaseout",
        "climate_resilience", "oregon_climate_action_plan",
        "oregon_legislature",
    ],
    "transportation": [
        "trimet", "max_light_rail", "bike_infrastructure", "vision_zero",
        "freight", "ev_charging", "parking_reform", "bridge_replacement",
        "city_council", "downtown",
    ],
    "business": [
        "small_business", "layoffs", "openings_closings", "downtown",
        "port_of_portland", "homelessness", "public_safety",
    ],
    "culture": [
        "indie_music", "performing_arts", "museums",
        "lit_scene", "k12_arts",
    ],
    "food_drink": [
        "new_restaurants", "craft_beer", "wine_country",
        "coffee_culture", "farmers_markets", "openings_closings",
    ],
    "opinion": [
        "homelessness", "rent_stabilization", "trimet", "city_council",
        "decarbonization", "fentanyl_crisis", "measure_110",
        "ranked_choice_voting", "public_safety", "police_oversight",
    ],
}

# Beats held by authors, used as the author↔section routing key.
BEATS: list[str] = [
    "editorial", "city_hall", "housing", "climate",
    "transportation", "business", "culture", "food",
    "opinion", "investigations",
]

# Preferred section for an article given its author's beat.
BEAT_SECTION_AFFINITY: dict[str, dict[str, float]] = {
    "editorial":      {"opinion": 0.40, "city_hall": 0.20, "housing": 0.15,
                       "climate": 0.10, "transportation": 0.08, "business": 0.07},
    "city_hall":      {"city_hall": 0.78, "housing": 0.10, "transportation": 0.06,
                       "business": 0.04, "opinion": 0.02},
    "housing":        {"housing": 0.80, "city_hall": 0.12, "business": 0.04,
                       "opinion": 0.04},
    "climate":        {"climate": 0.82, "transportation": 0.06, "business": 0.04,
                       "city_hall": 0.04, "opinion": 0.04},
    "transportation": {"transportation": 0.78, "city_hall": 0.10, "climate": 0.06,
                       "business": 0.04, "opinion": 0.02},
    "business":       {"business": 0.74, "city_hall": 0.10, "housing": 0.06,
                       "food_drink": 0.04, "transportation": 0.04, "opinion": 0.02},
    "culture":        {"culture": 0.82, "food_drink": 0.10, "opinion": 0.04,
                       "city_hall": 0.04},
    "food":           {"food_drink": 0.78, "culture": 0.14, "business": 0.06,
                       "opinion": 0.02},
    "opinion":        {"opinion": 0.80, "city_hall": 0.06, "housing": 0.05,
                       "climate": 0.05, "culture": 0.04},
    "investigations": {"city_hall": 0.45, "housing": 0.20, "business": 0.15,
                       "climate": 0.10, "transportation": 0.06, "opinion": 0.04},
}

# 22 fictional staff. Fields: (name, role, primary_beat, joined_at, is_active).
# Spread across founding (Jan 2019) and recent hires.
AUTHORS: list[tuple[str, str, str, str, bool]] = [
    ("Maya Chen",            "editor_in_chief",          "editorial",      "2019-01-15", True),
    ("Daniel Vasquez",       "city_hall_editor",         "city_hall",      "2019-02-20", True),
    ("Tomas Rivera",         "climate_editor",           "climate",        "2019-03-10", True),
    ("James Okafor",         "housing_editor",           "housing",        "2019-06-15", True),
    ("Olivia Gallagher",     "transportation_editor",    "transportation", "2020-02-08", True),
    ("Lily Anderson",        "culture_editor",           "culture",        "2020-09-12", True),
    ("Rebecca Kim",          "city_hall_reporter",       "city_hall",      "2021-01-18", True),
    ("Naomi Brennan",        "opinion_columnist",        "opinion",        "2021-04-22", True),
    ("Alex Park",            "climate_reporter",         "climate",        "2021-07-30", True),
    ("Marcus Johnson",       "city_hall_reporter",       "city_hall",      "2021-11-05", True),
    ("Sophie Tran",          "business_editor",          "business",       "2022-02-14", True),
    ("Elena Petrov",         "housing_reporter",         "housing",        "2022-06-09", True),
    ("Henry Brooks",         "transportation_reporter",  "transportation", "2022-09-19", True),
    ("David Nakamura",       "culture_reporter",         "culture",        "2023-01-10", True),
    ("Tyler Knox",           "opinion_columnist",        "opinion",        "2023-03-22", True),
    ("Liam O'Sullivan",      "climate_reporter",         "climate",        "2023-08-08", True),
    ("Priya Iyer",           "food_reporter",            "food",           "2023-11-04", True),
    ("Aisha Williams",       "housing_reporter",         "housing",        "2024-02-19", True),
    ("Jordan Mitchell",      "food_editor",              "food",           "2024-05-13", True),
    ("Pavel Becker",         "business_reporter",        "business",       "2024-08-26", True),
    ("Rachel Goldberg",      "investigations_reporter",  "investigations", "2024-11-12", True),
    ("Theo Walsh",           "investigations_reporter",  "investigations", "2025-03-04", True),
]

# Portland metro neighborhoods + Oregon cities + Pacific Northwest geography.
PORTLAND_NEIGHBORHOODS: list[str] = [
    "Pearl District", "Old Town", "Downtown", "Goose Hollow",
    "Northwest", "Slabtown", "Hawthorne", "Belmont", "Sellwood",
    "Foster-Powell", "Montavilla", "Lents", "St Johns", "Kenton",
    "Alberta Arts", "Mississippi", "Boise", "Eliot",
    "Hollywood", "Concordia", "Cully", "East Portland", "Centennial",
]

OREGON_CITIES: list[tuple[str, str]] = [
    # (city, state)
    ("Portland", "OR"),
    ("Beaverton", "OR"),
    ("Hillsboro", "OR"),
    ("Gresham", "OR"),
    ("Tigard", "OR"),
    ("Lake Oswego", "OR"),
    ("Oregon City", "OR"),
    ("Milwaukie", "OR"),
    ("Salem", "OR"),
    ("Eugene", "OR"),
    ("Bend", "OR"),
    ("Corvallis", "OR"),
    ("Hood River", "OR"),
    ("Astoria", "OR"),
    ("Vancouver", "WA"),
    ("Seattle", "WA"),
    ("Tacoma", "WA"),
    ("San Francisco", "CA"),
    ("Oakland", "CA"),
    ("Los Angeles", "CA"),
    ("New York", "NY"),
    ("Brooklyn", "NY"),
]

# Weighted distribution of US sessions by city. Calibrated so per-state
# rollups land at: OR 62%, WA 14%, CA 10%, NY 3%, other states 10.4%.
# Portland metro core (Portland + Beaverton + Hillsboro + Gresham +
# Tigard + Lake Oswego + Oregon City + Milwaukie) accounts for ~52%.
US_CITY_WEIGHTS: dict[str, float] = {
    "Portland": 0.38,
    "Beaverton": 0.04, "Hillsboro": 0.035, "Gresham": 0.035,
    "Tigard": 0.02, "Lake Oswego": 0.018, "Oregon City": 0.012,
    "Milwaukie": 0.012, "Salem": 0.022, "Eugene": 0.018,
    "Bend": 0.018, "Corvallis": 0.008, "Hood River": 0.004, "Astoria": 0.004,
    "Vancouver": 0.05, "Seattle": 0.075, "Tacoma": 0.015,
    "San Francisco": 0.05, "Oakland": 0.025, "Los Angeles": 0.025,
    "New York": 0.02, "Brooklyn": 0.01,
}
# US sessions where state is one of the long-tail "other" states (not OR,
# WA, CA, or NY). Sum of US_CITY_WEIGHTS + this share = 1.0.
US_OTHER_STATE_SHARE: float = 0.104

US_STATE_FOR_CITY: dict[str, str] = {city: state for city, state in OREGON_CITIES}

# Diaspora cities for non-US countries.
DIASPORA_CITIES_BY_COUNTRY: dict[str, list[str]] = {
    "CA": ["Vancouver BC", "Toronto", "Montreal"],
    "UK": ["London", "Manchester"],
}

DEVICE_WEIGHTS: dict[str, float] = {
    "mobile": 0.66, "desktop": 0.28, "tablet": 0.06,
}

REFERRER_WEIGHTS: dict[str, float] = {
    "search": 0.34, "social": 0.22, "direct": 0.24,
    "newsletter": 0.16, "external": 0.04,
}

# ---- Headline assembly ------------------------------------------------------
# US local-news register: declarative, factual, specific. No clickbait
# patterns ("how X is changing Y"), no breathless launches, no LinkedIn
# voice. Closer to the Texas Tribune / Baltimore Banner cadence.

HEADLINE_TEMPLATES_BY_SECTION: dict[str, list[str]] = {
    "city_hall": [
        "City Council {council_action} {city_topic}",
        "{official} {gov_verb} {city_topic} amid {context}",
        "Multnomah County {county_action} after {trigger}",
        "Audit finds {audit_finding} in {agency}",
        "Portland's {city_topic} faces {hurdle}",
        "Records show {records_finding} at {agency}",
        "{official} clashes with {actor} over {city_topic}",
        "{agency} budget would {budget_action} {budget_target}",
    ],
    "housing": [
        "Portland's {housing_topic} hits {milestone}",
        "Why {neighborhood} is seeing {housing_trend}",
        "{housing_policy} clears another hurdle at {body}",
        "Eviction filings {direction} in {area} as {context}",
        "Inside the {project_type} planned for {area}",
        "{housing_topic} report flags gap in {area}",
        "Rent in {neighborhood}: {rent_finding}",
        "Joint Office of Homeless Services {joint_action}",
    ],
    "climate": [
        "Heat wave {heat_action} four records as forecast tightens",
        "Wildfire season {fire_trend} earlier than expected",
        "Atmospheric river dumps {rain_amount} on Portland metro",
        "{utility} {utility_action} amid {pressure}",
        "Salmon counts on the {river} tell {salmon_story}",
        "Oregon's {climate_policy} hits {policy_milestone}",
        "Why {region} is {climate_change_pattern}",
        "Climate scientists revise {forecast_target} after {context}",
    ],
    "transportation": [
        "TriMet {transit_action} {transit_target}",
        "Why {neighborhood} riders {transit_complaint}",
        "{bike_project} clears {bike_milestone}",
        "{bridge} replacement {bridge_status}",
        "Pedestrian deaths on {road_corridor} up as {context}",
        "Vision Zero report flags {vision_finding}",
        "{transit_action} could {transit_consequence} in {area}",
    ],
    "business": [
        "{biz_subject} {biz_verb} {biz_object} amid {context}",
        "Why {sector} is {biz_trend} in Portland",
        "{biz_subject} cuts {n_jobs} jobs as {context}",
        "Inside the {biz_type} reshaping {area}",
        "{biz_subject} expands into {expansion_area}",
        "{downtown_topic} returns as {context}",
    ],
    "culture": [
        "{artist} returns to {venue} with {work_descriptor}",
        "Inside {neighborhood}'s {culture_scene}",
        "{institution} announces {culture_announcement}",
        "{festival} brings {festival_feature} to {area}",
        "Why {institution} is {culture_action}",
        "Local {culture_form}: {curator_take}",
    ],
    "food_drink": [
        "Inside the {food_type} reshaping {neighborhood}'s food scene",
        "{restaurant_name} closes in {neighborhood} after {context}",
        "{brewery_or_food_spot} opens in {area}",
        "Why {origin} {beverage} is {beverage_trend}",
        "{food_topic} guide: {food_finding}",
        "The {meal_or_format} taking over {neighborhood}",
    ],
    "opinion": [
        "Why {opinion_position}",
        "Portland needs {opinion_call}",
        "{opinion_topic}: a reckoning",
        "Column: {opinion_argument}",
        "What we're getting wrong about {opinion_topic}",
        "{opinion_call} — and the politics making it harder",
    ],
}

# Filler vocabulary the templates pull from.
HEADLINE_FILLERS: dict[str, list[str]] = {
    # ---- city_hall ----
    "council_action": [
        "narrowly advances", "tables", "amends", "rejects",
        "fast-tracks", "delays vote on", "approves",
    ],
    "official": [
        "Mayor Wheeler's office", "Mayor's office", "Commissioner Rubio",
        "Commissioner Gonzalez", "Multnomah County Chair", "Council President",
        "City Auditor", "City Attorney's office",
    ],
    "gov_verb": [
        "pushes back on", "signs off on", "questions",
        "stalls", "fast-tracks", "calls for review of",
    ],
    "city_topic": [
        "the short-term rental fee hike", "the police accountability ordinance",
        "the homelessness response budget", "the downtown revitalization plan",
        "the camping ordinance", "the public records request backlog",
        "the climate resilience plan", "the parking reform package",
        "ranked-choice ballot design", "the lobbying disclosure rule",
    ],
    "context": [
        "an audit", "court ruling", "ballot pressure",
        "a public records release", "growing council split",
        "rising service costs", "a state preemption fight",
        "fall budget hearings",
    ],
    "county_action": [
        "moves to take over the homeless services contract",
        "shelves a behavioral health expansion",
        "expands deflection court capacity",
        "tightens rules on homelessness contracting",
        "approves a jail diversion pilot",
    ],
    "trigger": [
        "an audit", "a damning state report", "court ruling",
        "a leaked memo", "rising overdose figures",
        "a federal compliance deadline",
    ],
    "audit_finding": [
        "missing payroll records", "millions in unspent funds",
        "no oversight of vendor billings", "compliance gaps",
        "inconsistent contract enforcement",
    ],
    "agency": [
        "Portland Bureau of Transportation", "Bureau of Planning",
        "Joint Office of Homeless Services", "Bureau of Environmental Services",
        "Multnomah County Health Department", "Portland Bureau of Emergency Management",
        "Bureau of Development Services", "Portland Parks & Recreation",
    ],
    "hurdle": [
        "a council split", "PUC pushback",
        "a county standoff", "a state preemption",
        "an unresolved lawsuit",
    ],
    "records_finding": [
        "the contract was awarded without bids",
        "internal emails warned of the cost overrun",
        "the bureau missed reporting deadlines twice",
        "officials knew about the leak in March",
    ],
    "actor": [
        "the county", "the state", "the police union",
        "the firefighters' union", "transit advocates",
        "neighborhood associations",
    ],
    "budget_action": ["cut", "freeze", "shift", "expand"],
    "budget_target": [
        "outreach contracts", "park maintenance", "shelter beds",
        "transit subsidies", "office leases", "code enforcement staffing",
    ],
    # ---- housing ----
    "housing_topic": [
        "permitting backlog", "ADU pipeline", "shelter capacity",
        "supportive housing waitlist", "rent assistance pipeline",
        "vacancy rate", "tenant protection caseload",
    ],
    "milestone": [
        "a new low", "the highest level on record",
        "a six-year high", "the worst quarter since 2020",
        "an all-time backlog", "a record streak",
    ],
    "neighborhood": [
        "the Pearl", "Sellwood", "St Johns", "Hawthorne",
        "Alberta Arts", "Foster-Powell", "Lents", "Cully",
        "Hollywood", "East Portland", "Belmont", "Mississippi",
    ],
    "housing_trend": [
        "a wave of new ADUs",
        "a surge in eviction filings",
        "more vacant storefronts than tenants",
        "rents flatten for the first time in three years",
        "a new wave of redevelopment",
    ],
    "housing_policy": [
        "the inclusionary housing rule", "the relocation assistance ordinance",
        "the camping enforcement ordinance", "the no-cause eviction ban",
        "the tenant screening reform",
    ],
    "body": [
        "the council", "Multnomah County", "the state legislature",
        "the city auditor's review",
    ],
    "direction": ["climb", "fall", "level off"],
    "area": [
        "East Portland", "the Pearl", "Inner Southeast",
        "North Portland", "Northeast Portland", "outer Southwest",
        "the central city", "the eastside",
    ],
    "project_type": [
        "200-unit affordable project", "transit-oriented development",
        "shelter conversion", "modular supportive housing project",
        "mixed-use complex",
    ],
    "rent_finding": [
        "a five-year squeeze finally easing",
        "the asking-rent gap has tripled",
        "studios outpacing two-bedrooms for the first time",
        "what concessions are now standard",
    ],
    "joint_action": [
        "shifts $14 million to outreach contracts",
        "hits a contracting wall with the county",
        "reports first quarter under new leadership",
        "drops a long-running shelter operator",
    ],
    # ---- climate ----
    "heat_action": ["breaks", "ties", "approaches"],
    "fire_trend": [
        "starts five weeks earlier than the 30-year average",
        "stretches deeper into October",
        "is the longest of the decade so far",
        "follows the third-driest spring on record",
    ],
    "rain_amount": [
        "3.7 inches",
        "more rain in 36 hours than September averages",
        "a half-summer's rainfall",
        "1.2 inches an hour at the peak",
    ],
    "utility": [
        "Portland General Energy", "PacifiCorp", "NW Natural",
        "Bonneville Power Administration", "Pacific Northwest grid operator",
    ],
    "utility_action": [
        "files a 7.4% rate hike",
        "warns of summer reliability gaps",
        "cuts gas hookups in new construction",
        "loses a key climate benchmark",
        "delays a transmission build",
    ],
    "pressure": [
        "PUC scrutiny", "ratepayer pushback",
        "wildfire liability questions", "a coalition of environmental groups",
        "a federal review",
    ],
    "river": [
        "Columbia", "Willamette", "Sandy", "Clackamas",
        "Tualatin", "Deschutes",
    ],
    "salmon_story": [
        "a mixed recovery story",
        "the worst run since 2018",
        "what restoration is — and isn't — doing",
        "habitat work is finally showing up",
    ],
    "climate_policy": [
        "Climate Protection Program", "100% clean electricity rule",
        "diesel idling reduction rule", "tribal co-management framework",
    ],
    "policy_milestone": [
        "first compliance deadline",
        "halfway mark on its emissions target",
        "a court challenge",
        "a stakeholder rewrite",
    ],
    "region": [
        "Oregon", "the Willamette Valley", "Eastern Oregon",
        "the Coast Range", "the Cascades", "the Columbia Gorge",
        "Multnomah County", "the Hood River Valley",
    ],
    "climate_change_pattern": [
        "warming faster than the rest of the state",
        "losing snowpack two weeks earlier each decade",
        "experiencing more 90-degree days each year",
        "drying earlier in summer",
    ],
    "forecast_target": [
        "the summer outlook", "fire-season risk",
        "salmon return projections", "ozone forecasts",
    ],
    # ---- transportation ----
    "transit_action": [
        "raises", "restructures", "freezes",
        "extends", "cuts", "suspends",
    ],
    "transit_target": [
        "the base fare to $2.95",
        "weekend MAX service",
        "the FX bus rollout",
        "low-income fare passes",
        "downtown transfer rules",
    ],
    "transit_complaint": [
        "are paying the most under the new fare structure",
        "wait longer for FX buses than promised",
        "lost two stops in last month's restructure",
        "say weekend cuts gut access to jobs",
    ],
    "bike_project": [
        "The 70s Greenway",
        "The Naito Parkway protected lane",
        "The Lloyd cycle track",
        "The Outer Powell bike network",
        "The Tilikum spine improvements",
    ],
    "bike_milestone": [
        "a key council vote",
        "design review",
        "the first round of construction",
        "a ribbon cutting",
    ],
    "bridge": [
        "Burnside Bridge", "Hawthorne Bridge",
        "I-5 bridge", "Sellwood Bridge",
    ],
    "bridge_status": [
        "moves to environmental review",
        "hits its second cost overrun",
        "could finally start in 2027",
        "stalls amid funding gap",
    ],
    "road_corridor": [
        "82nd Avenue", "Powell Boulevard", "Sandy Boulevard",
        "Outer Division", "MLK", "TV Highway",
    ],
    "vision_finding": [
        "the deadliest year for pedestrians since 2017",
        "speeding tickets are down despite enforcement push",
        "high-injury network unchanged after five years",
    ],
    "transit_consequence": [
        "save the agency $12 million",
        "kill the East Portland night service",
        "force a new round of route changes",
    ],
    # ---- business ----
    "biz_subject": [
        "Daimler Trucks NA", "Tektronix", "Adidas North America",
        "Nike", "Lam Research", "Vacasa",
        "On Semiconductor", "Stoel Rives",
    ],
    "biz_verb": [
        "lays off", "expands", "moves",
        "consolidates", "spins off", "buys",
    ],
    "biz_object": [
        "its Beaverton operations", "headquarters staff",
        "its DEI office", "its digital team",
        "a regional office", "a logistics arm",
    ],
    "sector": [
        "outdoor apparel", "semiconductors", "craft distilling",
        "cannabis retail", "hospitality", "biotech",
    ],
    "biz_trend": [
        "leaving the central city", "consolidating",
        "raising wages faster than the metro average",
        "betting on co-op ownership", "rebounding more slowly than expected",
    ],
    "n_jobs": ["120", "240", "60", "350", "90"],
    "biz_type": [
        "co-op grocery", "credit union", "worker-owned bakery",
        "indie publisher", "mutual-aid hardware store",
    ],
    "expansion_area": [
        "Beaverton", "Hillsboro", "Bend", "Eugene",
        "the Tualatin Valley", "the Gorge",
    ],
    "downtown_topic": [
        "Office occupancy", "weekend foot traffic",
        "small business openings", "after-hours retail",
    ],
    # ---- culture ----
    "artist": [
        "M. Ward", "Karl Blau", "Stephen Malkmus",
        "The Decemberists", "Sleater-Kinney",
        "Lael Neale", "Y La Bamba",
    ],
    "venue": [
        "the Crystal Ballroom", "Doug Fir", "Mississippi Studios",
        "Revolution Hall", "Polaris Hall", "Aladdin Theater",
    ],
    "work_descriptor": [
        "a stripped-down new record",
        "a four-night residency",
        "a career-spanning retrospective",
        "a return to chamber-pop form",
    ],
    "culture_scene": [
        "indie literary scene",
        "experimental theater scene",
        "queer punk scene",
        "wood-and-clay craft revival",
    ],
    "institution": [
        "Portland Art Museum", "Portland Center Stage",
        "Powell's Books", "Oregon Symphony",
        "the Portland Japanese Garden", "Literary Arts",
    ],
    "culture_announcement": [
        "a new artistic director",
        "a 30% expansion of K-12 programming",
        "a free-day pilot for Title I schools",
        "a strategic plan focused on regional artists",
    ],
    "festival": [
        "Pickathon", "Wordstock", "PDX Jazz Festival",
        "the Time-Based Art Festival", "Soul'd Out",
    ],
    "festival_feature": [
        "an all-Oregon main stage",
        "a two-day Japanese-American storytelling thread",
        "a rare Karl Blau set",
        "a dedicated kids' programming track",
    ],
    "culture_action": [
        "rethinking its membership model",
        "splitting from its longtime presenting partner",
        "doubling down on regional artists",
        "running a sliding-scale ticket pilot",
    ],
    "culture_form": [
        "letterpress publishing", "experimental cinema",
        "performance art", "small-press poetry",
    ],
    "curator_take": [
        "what this year is doing differently",
        "five works to watch",
        "the curator's own picks",
        "a quiet shift in the field",
    ],
    # ---- food_drink ----
    "food_type": [
        "cooperative bakery", "natural-wine bar",
        "Sichuan night-market pop-up", "izakaya",
        "Oaxacan tortillería", "pan-African café",
    ],
    "restaurant_name": [
        "Le Pigeon", "Pok Pok", "Holdfast Dining",
        "Beast", "Castagna", "Ava Gene's",
        "Coquine", "Clyde Common",
    ],
    "brewery_or_food_spot": [
        "Block 15 taproom", "Breakside satellite",
        "Heater Allen tasting room", "Migration Brewing pop-up",
        "a Detroit-style pizza joint", "a sandwich shop",
    ],
    "origin": [
        "Yirgacheffe", "Sumatran", "Honduran",
        "Burundian", "Ethiopian", "Guatemalan Antigua",
    ],
    "beverage": ["coffee", "espresso", "single-origin"],
    "beverage_trend": [
        "showing up everywhere this fall",
        "back on Portland's roasters' menus",
        "the cup of the season",
        "rewriting the seasonal menu",
    ],
    "food_topic": [
        "Friday-night neighborhood",
        "winter farmers' market",
        "Inner Eastside lunch",
        "weekend brunch", "natural-wine",
    ],
    "food_finding": [
        "five spots, all under $20",
        "what's actually new", "what's worth the wait",
        "where chefs are eating",
    ],
    "meal_or_format": [
        "happy hour", "single-origin pour-over",
        "two-stop bar crawl", "weekday lunch counter",
    ],
    # ---- opinion ----
    "opinion_position": [
        "the camping ordinance won't fix what it was built for",
        "ranked-choice voting needs a real public-education investment",
        "the Joint Office can't be both a shelter operator and a contracting authority",
        "Portland's bike network needs to stop pretending the eastside doesn't exist",
        "Powell's Books is a civic institution and we should fund it like one",
    ],
    "opinion_call": [
        "an honest conversation about deflection",
        "a property-tax reform that holds up",
        "a transit funding model that doesn't break with every recession",
        "a climate plan with teeth",
    ],
    "opinion_topic": [
        "homelessness", "Measure 110",
        "Portland's downtown", "ranked-choice voting",
        "school closures",
    ],
    "opinion_argument": [
        "the camping ordinance is doing the opposite of what its supporters claim",
        "Measure 110's repeal didn't fix what it was meant to fix",
        "the city's outreach contracts are a structural conflict of interest",
        "we keep mistaking visibility for success in homeless services",
    ],
}
