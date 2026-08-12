#!/usr/bin/env python3
"""seed-v3 + live DB 중복 메뉴 제거.

정책 (dedupe_menus.py 와 동일 + 옵션정책 우선):
1. 실카테고리(233~236) > 신메뉴(231) > 기타(232)
2. 동일 카테고리면 menu_opt_policy 많은 쪽 유지
3. 그래도 같으면 id 작은 쪽 유지

출력: seed-v3/*.json 갱신, output/dedupe_menus_seed_v3_report.json, dedupe_menus_seed_v3.sql
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed-v3"
OUT = Path(__file__).resolve().parent / "output"

LOW_PRIORITY_CATEGORIES = {231, 232}

CHILD_JSON = [
    ("menu_tag.json", "menu_id"),
    ("menu_nutr.json", "menu_id"),
    ("menu_ing.json", "menu_id"),
    ("menu_opt_policy.json", "menu_id"),
]

DB_CHILD_TABLES = [
    ("menu_opt_override", "menu_id"),
    ("menu_opt_policy", "menu_id"),
    ("menu_ing", "menu_id"),
    ("menu_nutr", "menu_id"),
    ("menu_tag", "menu_id"),
]


def strip_name(name: str) -> str:
    s = (name or "").strip().lower()
    s = s.replace("[프로틴]", "")
    return re.sub(r"\s+", "", s)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def menu_priority(menu: dict, policy_count: int, ing_count: int) -> tuple[int, int, int, int]:
    cat = int(menu.get("cat_id") or 0)
    if cat not in LOW_PRIORITY_CATEGORIES:
        cat_rank = 0
    elif cat == 231:
        cat_rank = 1
    else:
        cat_rank = 2
    return (cat_rank, -policy_count, -ing_count, int(menu["id"]))


def build_remove_map(
    menus: list[dict],
    policy_by_menu: dict[int, int],
    ing_by_menu: dict[int, int],
) -> dict[int, int]:
    by_name: dict[str, list[dict]] = defaultdict(list)
    for menu in menus:
        by_name[strip_name(menu["name"])].append(menu)

    remove_map: dict[int, int] = {}
    for group in by_name.values():
        if len(group) < 2:
            continue
        ordered = sorted(
            group,
            key=lambda m: menu_priority(
                m,
                policy_by_menu.get(int(m["id"]), 0),
                ing_by_menu.get(int(m["id"]), 0),
            ),
        )
        keep = ordered[0]
        for remove in ordered[1:]:
            remove_map[int(remove["id"])] = int(keep["id"])
    return remove_map


def load_backend_env() -> None:
    for env_path in (
        Path(__file__).resolve().parents[3] / "ASAK-back" / ".env",
        Path(__file__).resolve().parents[2] / "ASAK-back" / ".env",
    ):
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() and k.strip() not in os.environ:
                os.environ[k.strip()] = v.strip()
        break


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    raw = url.replace("jdbc:mysql://", "")
    host_port, _, rest = raw.partition("/")
    db = rest.split("?", 1)[0]
    host, port = host_port.split(":") if ":" in host_port else (host_port, "3306")
    return host, int(port), db


def apply_seed_dedupe() -> dict[str, Any]:
    menus = load_json(SEED / "menu.json")
    policies = load_json(SEED / "menu_opt_policy.json")
    menu_ing = load_json(SEED / "menu_ing.json")
    policy_by_menu: dict[int, int] = defaultdict(int)
    for p in policies:
        policy_by_menu[int(p["menu_id"])] += 1
    ing_by_menu: dict[int, int] = defaultdict(int)
    for mi in menu_ing:
        ing_by_menu[int(mi["menu_id"])] += 1

    remove_map = build_remove_map(menus, policy_by_menu, ing_by_menu)
    remove_ids = set(remove_map)

    kept_menus = [m for m in menus if int(m["id"]) not in remove_ids]
    dump_json(SEED / "menu.json", kept_menus)

    for fname, field in CHILD_JSON:
        path = SEED / fname
        if not path.exists():
            continue
        rows = load_json(path)
        filtered = [r for r in rows if int(r[field]) not in remove_ids]
        dump_json(path, filtered)

    manifest_path = SEED / "manifest.json"
    if manifest_path.exists():
        manifest = load_json(manifest_path)
        manifest["counts"]["menu"] = len(kept_menus)
        for fname, _ in CHILD_JSON:
            key = fname.replace(".json", "")
            if key in manifest.get("counts", {}):
                manifest["counts"][key] = len(load_json(SEED / fname))
        manifest["deduped_at"] = datetime.now(timezone.utc).isoformat()
        manifest["deduped_removed"] = len(remove_ids)
        dump_json(manifest_path, manifest)

    pairs = []
    for rid, kid in sorted(remove_map.items()):
        name = next(m["name"] for m in menus if int(m["id"]) == rid)
        pairs.append(
            {
                "remove_id": rid,
                "keep_id": kid,
                "name": name,
                "remove_cat": next(int(m["cat_id"]) for m in menus if int(m["id"]) == rid),
                "keep_cat": next(int(m["cat_id"]) for m in menus if int(m["id"]) == kid),
            }
        )

    report = {
        "removed_count": len(remove_ids),
        "kept_count": len(kept_menus),
        "before_count": len(menus),
        "pairs": pairs,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    dump_json(OUT / "dedupe_menus_seed_v3_report.json", report)

    sql_lines = [
        "-- ASAK seed-v3 menu dedupe",
        f"-- removed: {len(remove_ids)}, kept: {len(kept_menus)}",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
    ]
    for row in pairs:
        rid, kid = row["remove_id"], row["keep_id"]
        sql_lines.append(f"-- {row['name']}: {rid} (cat {row['remove_cat']}) -> {kid} (cat {row['keep_cat']})")
        sql_lines.append(f"UPDATE order_item SET menu_id = {kid} WHERE menu_id = {rid};")
        for table, col in DB_CHILD_TABLES:
            sql_lines.append(f"DELETE FROM `{table}` WHERE `{col}` = {rid};")
        sql_lines.append(f"DELETE FROM menu WHERE id = {rid};")
        sql_lines.append("")
    sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;")
    (OUT / "dedupe_menus_seed_v3.sql").write_text("\n".join(sql_lines), encoding="utf-8")

    print(f"seed menus: {len(menus)} -> {len(kept_menus)} (removed {len(remove_ids)})")
    return report


def apply_db_dedupe(report: dict[str, Any]) -> dict[str, int]:
    import pymysql

    load_backend_env()
    url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    if not url or not user:
        raise RuntimeError("DB_URL / DB_USERNAME required")

    host, port, db = parse_jdbc_url(url)
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password or "",
        database=db,
        charset="utf8mb4",
        autocommit=False,
    )
    stats = {"removed": 0, "order_item_updated": 0}
    try:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            for row in report["pairs"]:
                remove_id = int(row["remove_id"])
                keep_id = int(row["keep_id"])
                cur.execute(
                    "SELECT COUNT(*) FROM menu WHERE id=%s", (remove_id,)
                )
                if cur.fetchone()[0] == 0:
                    continue
                cur.execute(
                    "UPDATE order_item SET menu_id = %s WHERE menu_id = %s",
                    (keep_id, remove_id),
                )
                stats["order_item_updated"] += cur.rowcount
                for table, col in DB_CHILD_TABLES:
                    cur.execute(f"DELETE FROM `{table}` WHERE `{col}` = %s", (remove_id,))
                cur.execute("DELETE FROM menu WHERE id = %s", (remove_id,))
                stats["removed"] += 1
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply-db", action="store_true")
    parser.add_argument("--skip-seed", action="store_true")
    args = parser.parse_args()

    if args.skip_seed:
        report = load_json(OUT / "dedupe_menus_seed_v3_report.json")
    else:
        report = apply_seed_dedupe()

    if args.apply_db:
        stats = apply_db_dedupe(report)
        print("db:", stats)

    print(f"report -> {OUT / 'dedupe_menus_seed_v3_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
