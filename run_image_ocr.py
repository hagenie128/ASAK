#!/usr/bin/env python3
"""세트메뉴 배너·멤버십 등급표 이미지 OCR만 실행합니다."""

from __future__ import annotations

import json
from pathlib import Path

from salady_scraper import SaladyScraper


def main() -> None:
    output_dir = Path("output")
    scraper = SaladyScraper(output_dir=output_dir, delay=0.2)

    print("단체주문 세트메뉴 배너 OCR...")
    group_order_path = output_dir / "group_order.json"
    if group_order_path.exists():
        group_order = json.loads(group_order_path.read_text(encoding="utf-8"))
    else:
        group_order = scraper.scrape_group_order()
    group_order = scraper._enrich_group_order_ocr(group_order)
    group_order_path.write_text(
        json.dumps(group_order, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  → 세트메뉴 {len(group_order.get('set_menus', []))}개")

    print("멤버십 등급표 OCR...")
    app_path = output_dir / "app_services.json"
    if app_path.exists():
        app_services = json.loads(app_path.read_text(encoding="utf-8"))
    else:
        app_services = scraper.scrape_app_services()
    app_services = scraper._enrich_membership_ocr(app_services)
    app_path.write_text(
        json.dumps(app_services, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    grades = app_services.get("membership", {}).get("grade_table", {}).get("grades", [])
    print(f"  → 등급 {len(grades)}단계")
    print(f"완료: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
