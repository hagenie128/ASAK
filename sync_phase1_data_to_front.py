#!/usr/bin/env python3
"""phase1 output JSON을 frontend/data로 복사."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "data-pipeline" / "phase1" / "output"
DST = ROOT / "frontend" / "data"
FILES = (
    "menus.json",
    "dressings.json",
    "store_menus.json",
    "dressing_nutrition_supplements.json",
)

def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    copied = []
    for name in FILES:
        src = SRC / name
        if src.exists():
            shutil.copy2(src, DST / name)
            copied.append(name)
    print(f"복사 완료: {DST}")
    print("  " + ", ".join(copied) if copied else "  (복사된 파일 없음)")

if __name__ == "__main__":
    main()
