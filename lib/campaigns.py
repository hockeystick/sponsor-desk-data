"""Past sponsorship campaigns + campaign↔article bridge + pricing doc.

Four generators, wired together:
1. `build_campaigns` draws ~72 campaigns across 2022-2025 with
   format/sector/fee/duration/impression distributions.
2. `build_campaign_articles` links each applicable campaign to the
   articles La Brújula actually ran under it — constrained by the
   campaign's date window and sector-preferred sections.
3. Articles receive a `sponsor_tag` update so the articles table is
   self-linking to the sponsor name.
4. `write_pricing_reference` emits `data/pricing_reference.md` — a
   static rate-card doc for the downstream brief tool to anchor to.

The four folder sponsors (Bancolombia Verde, Fundación Andes, MoviMed,
Grupo Éxito Café) are *not* in past_campaigns: they're the prospective
clients the brief tool will be pitching. The campaigns here are a
different cast of named companies that serves as precedent analogues.
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
    fee_eur                  INTEGER NOT NULL,
    impressions_delivered    INTEGER NOT NULL,
    engagement_rate          REAL NOT NULL,
    post_campaign_summary_es TEXT NOT NULL
);
CREATE INDEX idx_camp_sector ON past_campaigns(sponsor_sector);
CREATE INDEX idx_camp_format ON past_campaigns(format);

CREATE TABLE campaign_articles (
    campaign_id INTEGER NOT NULL REFERENCES past_campaigns(campaign_id),
    article_id  INTEGER NOT NULL REFERENCES articles(article_id),
    PRIMARY KEY (campaign_id, article_id)
);
CREATE INDEX idx_ca_article ON campaign_articles(article_id);
"""

# Sponsor name pools per sector. Real Colombian/international names are
# used here because the campaigns are *fictional* events — the names
# provide realism without claiming any real company actually ran these.
# The four folder sponsors are deliberately excluded; they're the
# prospective clients for the downstream brief tool.
_SPONSORS_BY_SECTOR: dict[str, list[str]] = {
    "financial_services": [
        "Bancolombia", "Grupo Sura", "Davivienda", "BBVA Colombia",
        "Banco de Bogotá", "Banco Popular", "Itaú Colombia",
        "Banco Caja Social", "AV Villas",
    ],
    "ngo_foundation": [
        "Fundación Corona", "Fundación Santo Domingo",
        "Fundación Bolívar Davivienda", "Fundación Aurelio Llano Posada",
        "Open Society Foundations", "Ford Foundation",
        "Fundación Carvajal", "National Endowment for Democracy",
        "Fundación WWB Colombia",
    ],
    "consumer_brands": [
        "Nutresa", "Alpina", "Postobón", "Colombina",
        "Crepes & Waffles", "Juan Valdez Café", "Avianca",
        "Totto", "Claro Móvil",
    ],
    "health": [
        "Compensar", "Colsubsidio", "EPS Sura", "EPS Sanitas",
        "Clínica Las Américas", "Hospital Pablo Tobón Uribe",
        "Cafesalud", "Coomeva",
    ],
    "tech": [
        "Rappi", "Platzi", "Lulo Bank", "Bold", "Habi",
        "Tpaga", "Tul", "Mercado Libre Colombia", "Habi Colombia",
    ],
    "government_eu": [
        "Unión Europea en Colombia", "Embajada de Suecia",
        "Embajada de Francia", "Ministerio de Ambiente",
        "Alcaldía de Medellín", "Gobernación de Antioquia",
        "USAID Colombia", "Programa de las Naciones Unidas para el Desarrollo",
        "Cancillería de Colombia",
    ],
}

# Sector ↔ preferred article sections for bridge linking.
_SECTOR_PREFERRED_SECTIONS: dict[str, list[str]] = {
    "financial_services": ["ciudades", "politica", "actualidad", "cafe_y_comida"],
    "ngo_foundation":     ["investigacion", "politica", "clima", "actualidad"],
    "consumer_brands":    ["cultura", "cafe_y_comida", "ciudades"],
    "health":             ["actualidad", "ciudades", "politica"],
    "tech":               ["ciudades", "actualidad", "politica"],
    "government_eu":      ["politica", "clima", "investigacion", "actualidad"],
}

# Topic-phrase pool per sector — threaded into the post-campaign summary.
_SECTOR_TOPICS: dict[str, list[str]] = {
    "financial_services": [
        "inclusión financiera rural", "educación financiera",
        "microcrédito para pymes", "banca sostenible",
        "hipotecas verdes", "movilidad eléctrica",
    ],
    "ngo_foundation": [
        "violencia basada en género", "periodismo local",
        "democracia participativa", "acuerdo de paz",
        "derechos humanos", "liderazgos juveniles",
        "reporteo investigativo",
    ],
    "consumer_brands": [
        "café de origen colombiano", "gastronomía regional",
        "turismo responsable", "marca país",
        "emprendimiento cultural", "economía creativa",
    ],
    "health": [
        "salud rural", "salud mental", "atención primaria",
        "maternidad adolescente", "vacunación",
        "enfermedades crónicas no transmisibles",
    ],
    "tech": [
        "innovación digital", "ecosistema de startups",
        "educación digital", "inclusión tecnológica",
        "economía digital", "fintech en Colombia",
    ],
    "government_eu": [
        "cooperación internacional", "reforma rural integral",
        "transición energética justa", "postconflicto",
        "equidad de género", "protección de líderes sociales",
    ],
}

_FORMAT_DURATION_WEEKS: dict[str, tuple[int, int]] = {
    "sponsored_section":   (4, 12),
    "branded_newsletter":  (1, 3),
    "longform_series":     (8, 24),
    "event_partnership":   (1, 4),
    "podcast_sponsorship": (4, 8),
}

_FORMAT_IMPRESSIONS_RANGE: dict[str, tuple[int, int]] = {
    "sponsored_section":   (180_000, 1_100_000),
    "branded_newsletter":  (16_000,     55_000),
    "longform_series":     (320_000, 2_000_000),
    "event_partnership":   (22_000,     90_000),
    "podcast_sponsorship": (35_000,    210_000),
}

_FORMAT_ENGAGEMENT_RANGE: dict[str, tuple[float, float]] = {
    "sponsored_section":   (0.025, 0.080),
    "branded_newsletter":  (0.040, 0.130),
    "longform_series":     (0.050, 0.150),
    "event_partnership":   (0.150, 0.350),
    "podcast_sponsorship": (0.060, 0.180),
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


def build_campaigns(rng: random.Random) -> list[dict]:
    campaigns: list[dict] = []
    for campaign_id in range(1, config.CAMPAIGN_COUNT + 1):
        sector = _weighted_choice(rng, config.CAMPAIGN_SECTOR_WEIGHTS)
        fmt = _weighted_choice(rng, config.CAMPAIGN_FORMAT_WEIGHTS)
        sponsor = rng.choice(_SPONSORS_BY_SECTOR[sector])
        start = _pick_start_date(rng)
        dur_lo, dur_hi = _FORMAT_DURATION_WEEKS[fmt]
        weeks = rng.randint(dur_lo, dur_hi)
        end = start + timedelta(weeks=weeks)
        if end > config.CAMPAIGNS_END:
            end = config.CAMPAIGNS_END
            weeks = max(1, (end - start).days // 7)
        imp_lo, imp_hi = _FORMAT_IMPRESSIONS_RANGE[fmt]
        impressions = rng.randint(imp_lo, imp_hi)
        eng_lo, eng_hi = _FORMAT_ENGAGEMENT_RANGE[fmt]
        engagement = round(rng.uniform(eng_lo, eng_hi), 4)
        campaigns.append(
            {
                "campaign_id": campaign_id,
                "sponsor_name": sponsor,
                "sponsor_sector": sector,
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "format": fmt,
                "fee_eur": _fee(rng, fmt, weeks),
                "impressions_delivered": impressions,
                "engagement_rate": engagement,
                "weeks": weeks,  # scratch, not persisted
            }
        )
    campaigns.sort(key=lambda c: c["start_date"])
    for i, c in enumerate(campaigns, 1):
        c["campaign_id"] = i
    return campaigns


def _es_num(n: int) -> str:
    """Format a number Spanish-style: 1.234.567 (thousand separators = '.')."""
    return f"{n:,}".replace(",", ".")


def _summary_sponsored_section(rng, c, topic, n_pieces):
    return (
        f"Durante {c['weeks']} semanas, La Brújula produjo junto con "
        f"{c['sponsor_name']} una sección patrocinada sobre {topic} que "
        f"publicó {n_pieces} artículos originales. La sección acumuló "
        f"{_es_num(c['impressions_delivered'])} impresiones y una tasa de "
        f"engagement del {c['engagement_rate']*100:.1f}%."
    )


def _summary_longform(rng, c, topic, n_pieces):
    return (
        f"Una serie de reporteo en {n_pieces} entregas sobre {topic}, "
        f"cofinanciada por {c['sponsor_name']}, exploró el tema desde "
        f"ángulos regionales y nacionales a lo largo de {c['weeks']} "
        f"semanas. La serie sumó {_es_num(c['impressions_delivered'])} "
        f"lecturas con engagement del {c['engagement_rate']*100:.1f}%."
    )


def _summary_branded_newsletter(rng, c, topic, n_pieces):
    nl = rng.choice(["Diario", "Verde", "Sobremesa"])
    return (
        f"Una edición especial del newsletter {nl} dedicada a {topic}, "
        f"patrocinada por {c['sponsor_name']}, alcanzó "
        f"{_es_num(c['impressions_delivered'])} suscriptores con una tasa de "
        f"apertura del {c['engagement_rate']*100:.1f}%."
    )


def _summary_event(rng, c, topic, n_pieces):
    city = rng.choice(["Medellín", "Bogotá", "Cali", "Cartagena"])
    return (
        f"{c['sponsor_name']} copatrocinó el panel de La Brújula sobre "
        f"{topic} realizado en {city}, con asistencia presencial y "
        f"transmisión online que sumaron {_es_num(c['impressions_delivered'])} "
        f"impresiones. La interacción medida fue del "
        f"{c['engagement_rate']*100:.1f}%."
    )


def _summary_podcast(rng, c, topic, n_pieces):
    eps = max(4, c["weeks"])
    return (
        f"Patrocinio de {c['weeks']} semanas ({eps} episodios) del "
        f"podcast semanal de La Brújula con {c['sponsor_name']}, "
        f"centrado en {topic}. Los episodios acumularon "
        f"{_es_num(c['impressions_delivered'])} escuchas con tasa de clic del "
        f"{c['engagement_rate']*100:.1f}%."
    )


_SUMMARY_BUILDERS = {
    "sponsored_section":   _summary_sponsored_section,
    "longform_series":     _summary_longform,
    "branded_newsletter":  _summary_branded_newsletter,
    "event_partnership":   _summary_event,
    "podcast_sponsorship": _summary_podcast,
}


def _outcome_and_followup(rng, c, n_pieces):
    sector = c["sponsor_sector"]
    outcomes = {
        "financial_services": [
            f"El sponsor reportó un aumento del {rng.randint(6, 18)}% en búsquedas de marca durante el periodo.",
            f"La serie generó {_es_num(rng.randint(280, 1200))} clics hacia la microsite del sponsor.",
            "Se produjo un informe final distribuido a la red de corresponsales del sponsor.",
        ],
        "ngo_foundation": [
            f"La campaña motivó una audiencia pública en el Congreso de la República.",
            f"Los resultados alimentaron el informe anual del {c['sponsor_name']}.",
            f"Tres de las piezas fueron replicadas por aliados del sponsor en el territorio.",
        ],
        "consumer_brands": [
            f"La marca reportó un aumento del {rng.randint(8, 22)}% en afinidad medida por encuestas internas.",
            f"Las piezas vincularon tráfico directo a los puntos de venta destacados.",
            f"La colaboración derivó en una segunda temporada acordada el trimestre siguiente.",
        ],
        "health": [
            f"La cobertura contribuyó a {rng.randint(2, 6)} mesas técnicas entre secretarías de salud y operadores.",
            f"Los datos del informe fueron citados por la Defensoría del Pueblo en su reporte semestral.",
            f"El sponsor distribuyó las piezas a su red asistencial.",
        ],
        "tech": [
            f"El sponsor reportó {_es_num(rng.randint(150, 900))} descargas directamente atribuibles a la serie.",
            f"La campaña impulsó dos paneles adicionales en festivales tech del semestre.",
            f"Se registraron {_es_num(rng.randint(20, 120))} leads calificados para el equipo comercial del sponsor.",
        ],
        "government_eu": [
            f"El material fue incorporado al repositorio público de la delegación.",
            f"La serie fue presentada en un evento en Bruselas con representantes de la región.",
            f"Los hallazgos alimentaron la agenda de cooperación del siguiente ciclo.",
        ],
    }
    followups = [
        f"La colaboración con {c['sponsor_name']} continúa en conversaciones para un posible formato de podcast.",
        f"El equipo comercial reporta satisfacción con entregables y resultados.",
        f"La relación sentó base para una renovación anual del acuerdo marco.",
        "El informe interno del sponsor cita esta pieza como caso de referencia.",
    ]
    return rng.choice(outcomes[sector]) + " " + rng.choice(followups)


def build_campaign_articles_and_summaries(
    rng: random.Random,
    campaigns: list[dict],
    articles: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Return (bridge_rows, updated_campaigns).

    `updated_campaigns` gets post_campaign_summary_es populated and
    `weeks` scratch field removed. `articles` is mutated in place to
    set sponsor_tag where applicable.
    """
    # Index articles by date for fast windowed lookup.
    articles_by_date: dict[str, list[dict]] = {}
    for a in articles:
        d = a["published_at"][:10]
        articles_by_date.setdefault(d, []).append(a)

    bridge: list[dict] = []

    for c in campaigns:
        fmt = c["format"]
        n_lo, n_hi = config.CAMPAIGN_ARTICLE_COUNTS[fmt]
        n_target = rng.randint(n_lo, n_hi) if n_hi > 0 else 0

        linked_ids: list[int] = []
        if n_target > 0:
            start = c["start_date"]
            end = c["end_date"]
            preferred = set(_SECTOR_PREFERRED_SECTIONS[c["sponsor_sector"]])
            # Gather candidates in window.
            candidates: list[dict] = []
            for day_str in sorted(articles_by_date.keys()):
                if start <= day_str <= end:
                    for a in articles_by_date[day_str]:
                        if a["sponsor_tag"] is None and a["section"] in preferred:
                            candidates.append(a)
            if len(candidates) < n_target:
                # Relax to all sections in the window.
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
        outcome_followup = _outcome_and_followup(rng, c, len(linked_ids))
        c["post_campaign_summary_es"] = f"{base_summary} {outcome_followup}"

    # Remove the scratch field.
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
        "start_date, end_date, format, fee_eur, impressions_delivered, "
        "engagement_rate, post_campaign_summary_es) VALUES (:campaign_id, "
        ":sponsor_name, :sponsor_sector, :start_date, :end_date, :format, "
        ":fee_eur, :impressions_delivered, :engagement_rate, "
        ":post_campaign_summary_es)",
        campaigns,
    )
    conn.executemany(
        "INSERT INTO campaign_articles (campaign_id, article_id) "
        "VALUES (:campaign_id, :article_id)",
        bridge,
    )
    # Propagate sponsor_tag back to articles table.
    tag_updates = [
        (a_id, s_name)
        for s_name, a_id in _collect_sponsor_tag_updates(campaigns, bridge)
    ]
    conn.executemany(
        "UPDATE articles SET sponsor_tag = ? WHERE article_id = ?",
        [(s, a) for (a, s) in tag_updates],
    )


def _collect_sponsor_tag_updates(campaigns, bridge):
    sponsor_by_campaign = {c["campaign_id"]: c["sponsor_name"] for c in campaigns}
    return [
        (sponsor_by_campaign[r["campaign_id"]], r["article_id"])
        for r in bridge
    ]


PRICING_REFERENCE_MD = """\
# La Brújula — Rate Card 2026

_Prices in EUR. Valid for contracts signed Q1–Q3 2026. Regional
distribution add-ons available on request. COP and USD quoted on
demand._

## Editorial sponsorship formats

### Sponsored Section

A disclosure-labelled branded-content hub of 6–12 original articles
produced by La Brújula's editorial team. Sponsor defines topic scope
in advance; editorial retains full control over reporting and
selection. Best for long-arc commitments on a clearly delimited
subject (e.g., *inclusión financiera rural*, *transición energética*).

- Duration: 4–12 weeks
- Base fee: €12,000–€45,000
- Median delivered impressions: ~450,000
- Includes: hero piece, 5–11 follow-ups, one newsletter feature, social push
- Strongest sector fit: financial services, philanthropy, public sector

### Longform Series

A 3–6 piece investigative or reportage series, usually produced under
an editorial grant from a foundation or institutional funder. Longer
production cycle; heavier per-piece lift.

- Duration: 8–24 weeks
- Base fee: €18,000–€42,000
- Median impressions: ~800,000
- Includes: 3–6 longform pieces, editorial launch event, translation
  into English on request
- Strongest sector fit: philanthropy, government/EU, health

### Branded Newsletter

A single sponsored edition or 2–3 edition arc inside Diario, Verde, or
Sobremesa. Highest direct engagement per impression thanks to the
opt-in list.

- Duration: 1–3 weeks (per arc)
- Base fee: €3,000–€9,000 per send
- Median impressions: ~35,000
- Includes: custom subject line, one creative slot, link tracking
- Strongest sector fit: any — especially consumer brands, tech, health

### Event Partnership

Co-produced panel or in-person event with livestream and recap
coverage. Variable format (breakfast panel, evening discussion,
festival partnership).

- Duration: 1–4 weeks incl. promotion
- Base fee: €8,000–€22,000
- Median in-room + stream attendance: ~50,000
- Includes: venue coordination, moderation, recorded panel, recap
  newsletter, social clips
- Strongest sector fit: philanthropy, government/EU, financial services

### Podcast Sponsorship

Full or partial sponsorship of a 4–8 week run of La Brújula's podcast,
with host-read placements and optional episode co-production.

- Duration: 4–8 weeks
- Base fee: €4,000–€11,000
- Median listens over run: ~100,000
- Includes: pre-roll + mid-roll host reads, show-notes placement, one
  social teaser per episode
- Strongest sector fit: tech, consumer brands, financial services

## Add-ons

| Add-on                                  | Uplift      |
| --------------------------------------- | ----------- |
| English translation of all pieces       | +15% of base fee |
| Regional distribution push (LatAm partners) | +€2,000     |
| Post-campaign report + engagement audit | +€1,500     |
| Spanish→Portuguese translation          | +12%        |
| Extended social campaign (6 weeks)      | +€1,800     |

## Notes

- All formats carry disclosure labelling per IAB Colombia standards.
- Minimum booking: €3,000.
- Editorial independence is non-negotiable: sponsors have no pre-publication
  review or takedown rights. All sponsored work is marked as such and
  archived with the original disclosure.
- Grant-funded reportage (common in the NGO/foundation sector) is
  priced separately from sponsorship formats and follows a project
  budget model rather than the rate card above.
"""


def write_pricing_reference(path: Path) -> None:
    path.write_text(PRICING_REFERENCE_MD, encoding="utf-8")
