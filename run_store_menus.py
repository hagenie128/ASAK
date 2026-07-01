#!/usr/bin/env python3
"""매장 메뉴판만 수집해 기존 menus.json에 병합합니다."""

from __future__ import annotations

import json
from pathlib import Path

from salady_scraper import (
    SaladyScraper,
    backfill_store_categories,
    build_dressings_catalog,
    enrich_menu_dressings,
    load_dressing_nutrition_supplements,
    write_menus_csv,
)


def main() -> None:
    output_dir = Path("output")
    scraper = SaladyScraper(output_dir=output_dir, delay=0.2)
    store_menus = scraper.scrape_store_menus()
    (output_dir / "store_menus.json").write_text(
        json.dumps(store_menus, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    menus_path = output_dir / "menus.json"
    if menus_path.exists():
        menus = json.loads(menus_path.read_text(encoding="utf-8"))
        backfill_store_categories(store_menus, menus)
        (output_dir / "store_menus.json").write_text(
            json.dumps(store_menus, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        merged = scraper.merge_store_menus(menus, store_menus)

        extra_toppings = None
        extra_path = output_dir / "extra_toppings.json"
        if extra_path.exists():
            extra_toppings = json.loads(extra_path.read_text(encoding="utf-8"))
        calorie_data = None
        calorie_path = output_dir / "calorie_calculator.json"
        if calorie_path.exists():
            calorie_data = json.loads(calorie_path.read_text(encoding="utf-8"))
        allergy_rows = None
        allergy_path = output_dir / "allergy_pdf.json"
        if allergy_path.exists():
            allergy_rows = json.loads(allergy_path.read_text(encoding="utf-8"))

        dressings_catalog = build_dressings_catalog(
            extra_toppings,
            calorie_data,
            allergy_rows=allergy_rows,
            menus=merged,
            nutrition_supplements=load_dressing_nutrition_supplements(output_dir),
        )
        merged = enrich_menu_dressings(merged, dressings_catalog)
        (output_dir / "dressings.json").write_text(
            json.dumps(dressings_catalog, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        menus_path.write_text(
            json.dumps(merged, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        write_menus_csv(merged, output_dir)
        print(f"menus.json 업데이트: {len(menus)} → {len(merged)}개")
    print(f"완료: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
