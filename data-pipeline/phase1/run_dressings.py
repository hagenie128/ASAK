#!/usr/bin/env python3
"""기존 menus.json에 드레싱 필드를 백필하고 dressings.json을 생성합니다."""

from __future__ import annotations

import json
from pathlib import Path

from salady_scraper import (
    build_dressings_catalog,
    enrich_menu_dressings,
    load_dressing_nutrition_supplements,
    write_menus_csv,
)


def main() -> None:
    output_dir = Path("output")
    menus_path = output_dir / "menus.json"
    if not menus_path.exists():
        raise SystemExit("output/menus.json 이 없습니다. 먼저 크롤러를 실행하세요.")

    extra_toppings: dict | None = None
    extra_path = output_dir / "extra_toppings.json"
    if extra_path.exists():
        extra_toppings = json.loads(extra_path.read_text(encoding="utf-8"))

    calorie_data: dict | None = None
    calorie_path = output_dir / "calorie_calculator.json"
    if calorie_path.exists():
        calorie_data = json.loads(calorie_path.read_text(encoding="utf-8"))

    allergy_rows: list | None = None
    allergy_path = output_dir / "allergy_pdf.json"
    if allergy_path.exists():
        allergy_rows = json.loads(allergy_path.read_text(encoding="utf-8"))

    menus = json.loads(menus_path.read_text(encoding="utf-8"))
    dressings_catalog = build_dressings_catalog(
        extra_toppings,
        calorie_data,
        allergy_rows=allergy_rows,
        menus=menus,
        nutrition_supplements=load_dressing_nutrition_supplements(output_dir),
    )
    enriched = enrich_menu_dressings(menus, dressings_catalog)

    menus_path.write_text(
        json.dumps(enriched, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "dressings.json").write_text(
        json.dumps(dressings_catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_menus_csv(enriched, output_dir)

    rec = sum(1 for m in enriched if m.get("recommended_dressing"))
    inc = sum(1 for m in enriched if m.get("included_dressing"))
    print(
        f"완료: 드레싱 카탈로그 {dressings_catalog['count']}개, "
        f"추천 {rec}개 / 포함 {inc}개"
    )


if __name__ == "__main__":
    main()
