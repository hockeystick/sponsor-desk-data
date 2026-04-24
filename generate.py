"""Entrypoint for the synthetic-data generator.

Running `uv run generate.py` recreates every artefact from a single seed:
- data/labrujula.sqlite  (eight tables)
- data/csv/*.csv         (one CSV per table)
- data/pricing_reference.md
- data/CHECKSUMS.txt
- sponsors/<slug>/ ...

Determinism contract: two consecutive runs produce byte-identical output.
No datetime.now() in data paths. No network calls. Single seed per run.
"""
from __future__ import annotations

import random
from pathlib import Path

from faker import Faker

from lib.config import SEED

ROOT: Path = Path(__file__).parent
DATA_DIR: Path = ROOT / "data"
CSV_DIR: Path = DATA_DIR / "csv"
SPONSORS_DIR: Path = ROOT / "sponsors"
SQLITE_PATH: Path = DATA_DIR / "labrujula.sqlite"


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    CSV_DIR.mkdir(exist_ok=True)
    SPONSORS_DIR.mkdir(exist_ok=True)


def main() -> None:
    _ensure_dirs()

    rng = random.Random(SEED)
    fake = Faker("es_CO")
    fake.seed_instance(SEED)

    # Phase 2+ generators will plug in here, each taking `rng` and `fake`
    # and writing into SQLITE_PATH and SPONSORS_DIR respectively.
    print(f"[scaffold] seed={SEED}")
    print(f"[scaffold] data dir  : {DATA_DIR}")
    print(f"[scaffold] sponsors  : {SPONSORS_DIR}")
    print("[scaffold] Phase 1 complete — vocabularies and config loaded, "
          "no data written yet.")


if __name__ == "__main__":
    main()
