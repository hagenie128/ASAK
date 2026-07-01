#!/usr/bin/env python3
"""기존 store_menus.json 카테고리 보완 후 menus.json store_pricing 반영."""

from __future__ import annotations

import json
from pathlib import Path

from salady_scraper import SaladyScraper, backfill_store_categories, write_menus_csv


def main() -> None:
    output_dir = Path("output")
    store_path = output_dir / "store_menus.json"
    menus_path = output_dir / "menus.json"
    if not store_path.exists() or not menus_path.exists():
        raise SystemExit("store_menus.json 과 menus.json 이 필요합니다.")

    store_menus = json.loads(store_path.read_text(encoding="utf-8"))
    menus = json.loads(menus_path.read_text(encoding="utf-8"))
    meta = backfill_store_categories(store_menus, menus)
    store_path.write_text(
        json.dumps(store_menus, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    scraper = SaladyScraper(output_dir=output_dir)
    merged = scraper.merge_store_menus(menus, store_menus)
    menus_path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_menus_csv(merged, output_dir)

    naver = next(
        (s for s in store_menus["stores"] if s["id"] == "naver_mapo"),
        None,
    )
    empty = 0
    if naver:
        empty = sum(1 for i in naver["items"] if not i.get("category"))
    print(
        f"카테고리 보완: {meta.get('category_backfill', {}).get('filled', 0)}건, "
        f"naver_mapo 미분류 {empty}/{len(naver['items']) if naver else 0}"
    )


if __name__ == "__main__":
    main()
