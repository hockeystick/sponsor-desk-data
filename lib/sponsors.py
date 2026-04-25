"""Sponsor folders: profile, press releases, past partnerships, 2026 priorities.

Content is written by hand as static English strings — not templated —
because the four sponsors are a fixed cast and scale-of-one realism
beats scale-of-N generation. A banned-phrase filter runs before every
write; if anything smells like corporate boilerplate or LLM-generic
output, the run aborts.
"""
from __future__ import annotations

import random
from pathlib import Path

# English LLM-sludge tells. Hits abort the run.
_BANNED_PHRASES: tuple[str, ...] = (
    # Generic corporate-boilerplate
    "at the intersection of",
    "in today's rapidly evolving",
    "in an ever-changing world",
    "ever-changing landscape",
    "rapidly evolving landscape",
    # Verb tics
    "leverage", "leveraging",
    "synergy", "synergies",
    # Lazy intensifiers
    "best-in-class",
    "world-class",
    "cutting-edge",
    "game-changing",
    "paradigm shift",
    "revolutionize",
    "revolutionizing",
    "seamless", "seamlessly",
    # Bumper-sticker mission claims
    "we're committed to",
    "we are committed to",
    "our mission is to",
    "passionate about",
    "thought leader",
    "thought leadership",
    # Generic feel-good
    "robust ecosystem",
    "vibrant ecosystem",
    "unlock the potential",
    "unlocking the potential",
)


def _check_banned(text: str, source_label: str) -> None:
    lowered = text.lower()
    hits = [p for p in _BANNED_PHRASES if p in lowered]
    if hits:
        raise RuntimeError(
            f"banned phrase in {source_label}: {hits!r}. "
            "fix the copy — don't weaken the filter."
        )


SPONSORS: dict[str, dict[str, str]] = {
    # Filled in by the dedicated content modules below.
}


def write_all_sponsors(rng: random.Random, sponsors_dir: Path) -> int:
    del rng
    count = 0
    for slug in sorted(SPONSORS.keys()):
        files = SPONSORS[slug]
        base = sponsors_dir / slug
        for rel_path in sorted(files.keys()):
            content = files[rel_path]
            _check_banned(content, f"{slug}/{rel_path}")
            if "press_releases/" in rel_path and '"' not in content and "said" not in content.lower():
                raise RuntimeError(
                    f"press release {slug}/{rel_path} is missing a quoted speaker"
                )
            target = base / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            count += 1
    return count
