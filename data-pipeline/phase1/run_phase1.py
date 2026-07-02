#!/usr/bin/env python3
"""ASAK 1차 크롤링 파이프라인."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STEPS = [
    ("매장 메뉴 수집", "run_store_menus.py"),
    ("드레싱 영양 보조 수집", "run_dressing_nutrition.py"),
    ("드레싱 병합", "run_dressings.py"),
    ("이벤트 수집", "run_events.py"),
]


def main() -> None:
    python = Path(sys.executable)
    for title, script_name in STEPS:
        script = ROOT / script_name
        print(f"\n== {title} ==")
        print(f"$ {python} {script}")
        subprocess.check_call([str(python), str(script)], cwd=ROOT)

    print("\nASAK 1차 크롤링 완료")
    print(f"- 산출물: {ROOT / 'output'}")


if __name__ == "__main__":
    main()
