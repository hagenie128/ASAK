#!/usr/bin/env python3
"""Split nutrition fields from seed-v3/ing.json into seed-v3/ing_nutr.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed-v3"
ING_PATH = SEED / "ing.json"
NUTR_PATH = SEED / "ing_nutr.json"
MANIFEST_PATH = SEED / "manifest.json"

NUTR_KEYS = [
    "serving_g",
    "kcal",
    "carb_g",
    "sugar_g",
    "protein_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
]


def main() -> None:
    rows = json.loads(ING_PATH.read_text(encoding="utf-8"))
    nutr_rows = []
    cleaned = []
    for row in rows:
        nutr = {k: row.get(k) for k in NUTR_KEYS}
        if any(v is not None for v in nutr.values()):
            nutr_rows.append(
                {
                    "id": row["id"],
                    "ing_id": row["id"],
                    **nutr,
                    "source_id": None,
                }
            )
        cleaned.append({k: v for k, v in row.items() if k not in NUTR_KEYS})

    NUTR_PATH.write_text(
        json.dumps(nutr_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    ING_PATH.write_text(
        json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        counts = manifest.setdefault("counts", {})
        counts["ing"] = len(cleaned)
        counts["ing_nutr"] = len(nutr_rows)
        paths = manifest.setdefault("paths", {})
        paths["ing_nutr"] = "seed-v3/ing_nutr.json"
        MANIFEST_PATH.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"ing={len(cleaned)} ing_nutr={len(nutr_rows)}")


if __name__ == "__main__":
    main()
