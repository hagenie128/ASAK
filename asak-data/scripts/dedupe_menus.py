#!/usr/bin/env python3
"""menu.json 및 menu_id FK 시드에서 중복 메뉴 제거.

정책:
1. (name, category_id) 동일 → id 작은 쪽 유지
2. 이름만 동일, 카테고리 다름 → 신메뉴(231)·기타(232) 쪽 제거, 실카테고리 유지
3. 그 외 → id 작은 쪽 유지

출력: seed/*.json 갱신, scripts/output/dedupe_menus.sql, dedupe_menus_report.json
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed"
OUT = Path(__file__).resolve().parent / "output"

LOW_PRIORITY_CATEGORIES = {231, 232}  # 신메뉴, 기타

MENU_CHILD_TABLES = [
    ("menu_tag", "menu_id"),
    ("menu_nutrition", "menu_id"),
    ("menu_ingredient", "menu_id"),
    ("menu_option_group", "menu_id"),
    ("menu_option", "menu_id"),
]

# 실DB(asak_db) 테이블명 — seed JSON과 다름
DB_CHILD_TABLES = [
    ("menu_opt_override", "menu_id"),
    ("menu_opt_policy", "menu_id"),
    ("menu_ing", "menu_id"),
    ("menu_nutr", "menu_id"),
    ("menu_tag", "menu_id"),
]


def load(name: str) -> list[dict]:
    return json.loads((SEED / f"{name}.json").read_text(encoding="utf-8"))


def save(name: str, rows: list[dict]) -> None:
    (SEED / f"{name}.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def menu_priority(menu: dict) -> tuple[int, int, int]:
    cat = menu["category_id"]
    if cat not in LOW_PRIORITY_CATEGORIES:
        return (0, 0, menu["id"])
    # 신메뉴(231)가 기타(232)보다 우선 제거 대상
    sub = 0 if cat == 231 else 1
    return (1, sub, menu["id"])


def build_remove_map(menus: list[dict]) -> dict[int, int]:
    """remove_id -> keep_id"""
    by_name: dict[str, list[dict]] = defaultdict(list)
    for menu in menus:
        by_name[menu["name"]].append(menu)

    remove_map: dict[int, int] = {}
    for group in by_name.values():
        if len(group) < 2:
            continue
        ordered = sorted(group, key=menu_priority)
        keep = ordered[0]
        for remove in ordered[1:]:
            remove_map[remove["id"]] = keep["id"]

    return remove_map


def filter_child(table: str, field: str, rows: list[dict], remove_ids: set[int]) -> list[dict]:
    return [row for row in rows if row[field] not in remove_ids]


def sql_delete_menu_db(menu_id: int, keep_id: int) -> list[str]:
    lines = [
        f"-- menu_id {menu_id} -> keep {keep_id}",
        f"UPDATE order_item SET menu_id = {keep_id} WHERE menu_id = {menu_id};",
    ]
    for table, col in DB_CHILD_TABLES:
        lines.append(f"DELETE FROM {table} WHERE {col} = {menu_id};")
    lines.append(f"DELETE FROM menu WHERE id = {menu_id};")
    return lines


def main() -> None:
    menus = load("menu")
    remove_map = build_remove_map(menus)
    remove_ids = set(remove_map)

    kept_menus = [m for m in menus if m["id"] not in remove_ids]
    assert len(kept_menus) + len(remove_ids) == len(menus)

    save("menu", kept_menus)

    for table, field in MENU_CHILD_TABLES:
        rows = load(table)
        filtered = filter_child(table, field, rows, remove_ids)
        save(table, filtered)

    manifest = json.loads((SEED / "manifest.json").read_text(encoding="utf-8"))
    manifest["counts"]["menu"] = len(kept_menus)
    for table, field in MENU_CHILD_TABLES:
        manifest["counts"][table] = len(load(table))
    manifest["deduped_at"] = datetime.now(timezone.utc).isoformat()
    manifest["deduped_removed"] = len(remove_ids)
    (SEED / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "removed_count": len(remove_ids),
        "kept_count": len(kept_menus),
        "pairs": [
            {"remove_id": rid, "keep_id": kid, "name": next(m["name"] for m in menus if m["id"] == rid)}
            for rid, kid in sorted(remove_map.items())
        ],
    }
    (OUT / "dedupe_menus_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    sql_lines = [
        "-- ASAK menu dedupe",
        f"-- removed: {len(remove_ids)}, kept: {len(kept_menus)}",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
    ]
    for rid, kid in sorted(remove_map.items()):
        sql_lines.extend(sql_delete_menu_db(rid, kid))
        sql_lines.append("")
    sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;")
    (OUT / "dedupe_menus.sql").write_text("\n".join(sql_lines), encoding="utf-8")

    print(f"menus: {len(menus)} -> {len(kept_menus)} (removed {len(remove_ids)})")
    print(f"report: {OUT / 'dedupe_menus_report.json'}")
    print(f"sql:    {OUT / 'dedupe_menus.sql'}")


if __name__ == "__main__":
    main()
