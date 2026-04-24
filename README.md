# sponsor-desk-data

Synthetic data generator for **La Brújula** — a fictional Spanish-language independent news outlet based in Medellín, Colombia — plus public-footprint materials for four fictional sponsors. Built to feed a sponsorship-brief tool without touching real data or live APIs.

## What this produces

- `data/labrujula.sqlite` — eight tables: `authors`, `articles`, `pageviews_daily`, `audience_daily`, `newsletter_subscribers`, `newsletter_sends`, `past_campaigns`, `campaign_articles`.
- `data/csv/*.csv` — one CSV mirror per table, for inspection.
- `data/pricing_reference.md` — static rate-card doc the brief tool can anchor pricing suggestions to.
- `data/CHECKSUMS.txt` — SHA256 of every generated artefact; two consecutive runs must produce identical checksums.
- `sponsors/<slug>/` — four sponsor folders, each with `profile.md`, `press_releases/*.md`, `past_media_partnerships.md`, and `brand_priorities_2026.md`.

## Regenerate

```
uv sync
uv run generate.py
```

All output is driven by a single `SEED` in `lib/config.py`. No `datetime.now()`, no network calls — every run is byte-identical to the last.

### Determinism proof

```
uv run generate.py && cp data/CHECKSUMS.txt /tmp/c1
uv run generate.py
diff /tmp/c1 data/CHECKSUMS.txt   # must be empty
```

## Tuning

Every volume/cadence knob lives in `lib/config.py`. Controlled vocabularies (sections, topic tags, Colombian places, authors, coffee varietals) live in `lib/vocab.py`. Don't sprinkle magic numbers through the generators.

## Project layout

```
lib/
  config.py      — SEED and all tunable knobs
  vocab.py       — controlled vocabularies; the Colombian voice of the dataset
  outlet.py      — authors, articles, pageviews_daily
  audience.py    — audience_daily rollups
  newsletter.py  — newsletter_subscribers, newsletter_sends
  campaigns.py   — past_campaigns + campaign_articles + pricing reference
  sponsors.py    — sponsor markdown folders
generate.py      — single entrypoint; idempotent
```

## The outlet, in one paragraph

La Brújula is a Medellín-based independent news outlet founded in January 2018. 22 staff. Covers Colombia and the Andean region in Spanish, with English translations of roughly 12% of pieces. Editorial strengths in order: climate and environment, urban issues, local investigative reporting, Colombian coffee and food culture. Revenue mix approximately 30% reader revenue, 40% sponsorship and branded content, 30% grants and institutional funding. Three newsletters: *Diario* (daily roundup), *Verde* (weekly climate), *Sobremesa* (weekly culture and food).
