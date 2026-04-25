# sponsor-desk-data

Synthetic data generator for **The Cascade Tribune** — a fictional
English-language local news outlet based in Portland, Oregon — plus
public-footprint materials for four fictional sponsors. Built to feed
a sponsorship-brief tool without touching real data or live APIs.

## What this produces

- `data/cascade_tribune.sqlite` — eight tables: `authors`, `articles`,
  `pageviews_daily`, `audience_daily`, `newsletter_subscribers`,
  `newsletter_sends`, `past_campaigns`, `campaign_articles`.
- `data/csv/*.csv` — one CSV mirror per table, for inspection.
- `data/pricing_reference.md` — static USD rate-card doc the brief tool
  can anchor pricing suggestions to.
- `data/CHECKSUMS.txt` — SHA256 of every generated artefact; two
  consecutive runs must produce identical checksums.
- `sponsors/<slug>/` — four sponsor folders, each with `profile.md`,
  `press_releases/*.md`, `past_media_partnerships.md`, and
  `brand_priorities_2026.md`.

## Regenerate

```
uv sync
uv run generate.py
```

All output is driven by a single `SEED` in `lib/config.py`. No
`datetime.now()`, no network calls — every run is byte-identical to
the last.

### Determinism proof

```
uv run generate.py
cp data/CHECKSUMS.txt /tmp/c1
uv run generate.py
diff /tmp/c1 data/CHECKSUMS.txt   # must be empty → "FULLY DETERMINISTIC"
```

A non-empty diff means some generator introduced non-determinism —
usually via dict iteration order, unseeded randomness, or a
datetime.now() call that crept in.

### Verification

The generator runs 21 consistency checks after every pass and aborts
on any failure. The checks cover:

- Row-count ranges per table
- `sum(pageviews) / sum(sessions)` ratio in [0.80, 0.95]
- Foreign-key integrity (articles→authors, pageviews_daily→articles)
- Every `campaign_articles` row falls within its campaign's date window
- `sponsor_tag` propagated consistently from campaign to linked articles
- Every newsletter send's `recipients` ≤ eligible-subscriber count at send date
- Per-newsletter open rates remain inside the configured band
- Each headline sponsor has at least the configured minimum of campaigns
- Non-completed-outcomes share is at least 10% (so the brief tool sees
  honest history, not success-theatre)

## Tuning

Every volume/cadence knob lives in `lib/config.py`. Controlled
vocabularies (sections, topic tags, Portland places, authors,
headline templates) live in `lib/vocab.py`. Don't sprinkle magic
numbers through the generators.

## Project layout

```
lib/
  config.py      — SEED and all tunable knobs
  vocab.py       — controlled vocabularies; the Portland voice of the dataset
  outlet.py      — authors, articles, pageviews_daily
  audience.py    — audience_daily rollups
  newsletter.py  — newsletter_subscribers, newsletter_sends
  campaigns.py   — past_campaigns + campaign_articles + pricing reference
  sponsors.py    — sponsor markdown folders
  csv_export.py  — pandas-based CSV mirror
  verify.py      — 21 post-generation consistency checks
generate.py      — single entrypoint; idempotent
```

## The outlet, in one paragraph

The Cascade Tribune is a Portland-based independent news outlet
founded in January 2019. 24 staff (22 named bylines + 2 ops). Covers
the Portland metro area in English, with diaspora readership in
Seattle, the Bay Area, and New York. Editorial strengths in order:
city government and accountability, housing and homelessness, climate
and environment, transportation and urban planning, food and culture,
regional business. Revenue mix approximately 25% reader revenue
(digital subs + donations), 45% sponsorship and branded content, 30%
foundation grants. Two newsletters: *The Daily Cascade* (weekday
morning roundup) and *Plate & Place* (Friday food and culture).

## The four sponsor folders

Each is a fictional analogue of a real Portland-metro or national
company. Profiles include a disclosure note. The four span fit
profiles deliberately so the brief tool can demonstrate honest
matching:

| Sponsor                              | Sector                  | Fit profile                         |
|--------------------------------------|-------------------------|-------------------------------------|
| Portland General Energy              | regional_utility        | Strong topical fit + editorial conflict (rate filings, reliability) |
| Powell's Community Foundation        | pnw_community_foundation| Strong, clean fit (literacy, journalism, culture) |
| Cascadia Credit Union                | regional_finance        | Partial fit (demographic-strong, weaker topical) |
| Stumptown Roasters Co-op             | regional_food_beverage  | Thin fit (Plate & Place only) |

These four sponsors also appear in `past_campaigns` with at least the
configured minimum of historical campaigns each (4, 4, 3, 3
respectively), so the brief tool has real proof points to cite.
