#!/usr/bin/env python3
"""Apply allergy_260715.csv / nutrition_260715.csv into seed-v3 and optionally MySQL.

Rules (ASAK 2026-08-12 plan):
  - Prefer 적용범위 == SALADY when duplicate names conflict.
  - Update ALL menu ids that share a normalized name.
  - Ingredient nutrition/allergens for matched ings; menu allergens are report-only.
  - Do not create new menus/ingredients for unmatched names.
  - Do not expand allergen master for unused CSV columns (땅콩/잣/게/오징어/복숭아).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed-v3"
INPUT = Path(__file__).resolve().parent / "input"
OUTPUT = Path(__file__).resolve().parent / "output"

DEFAULT_NUTRITION = INPUT / "nutrition_260715.csv"
DEFAULT_ALLERGY = INPUT / "allergy_260715.csv"
REPORT_PATH = OUTPUT / "csv_260715_report.json"

NUTR_KEYS = (
    "serving_g",
    "kcal",
    "carb_g",
    "sugar_g",
    "protein_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
)
CSV_NUTR_COLS = (
    "제공량(g)",
    "열량(Kcal)",
    "탄수화물(g)",
    "당류(g)",
    "단백질(g)",
    "지방(g)",
    "포화지방(g)",
    "나트륨(mg)",
)

# Categories that typically map to ingredients (and sometimes also menus, e.g. BASE).
ING_CATS = {
    "BASE",
    "PROTEIN",
    "VEGGIES",
    "CRISPY",
    "DRESSING",
    "SAUCE & MOUSSE",
    "SIDE",
    "DRINK",
}

ALIASES = {
    "(베이스)파스타면": "파스타면",
    "(베이스)곡물밥": "곡물밥",
    "(토핑)닭가슴살": "닭가슴살",
    "(토핑)베이컨": "베이컨",
    "로스트닭다리살마덮요밥": "로스트닭다리살마요덮밥",
}


def strip_name(name: str) -> str:
    """Whitespace/punctuation normalize only — used to index seed names."""
    s = (name or "").strip()
    s = s.replace("（", "(").replace("）", ")")
    return re.sub(r"\s+", "", s)


def resolve_name(name: str, available: set[str] | dict[str, Any]) -> str:
    """CSV lookup key: exact strip match first, then alias if target exists."""
    key = strip_name(name)
    if key in available:
        return key
    aliased = ALIASES.get(key)
    if aliased and aliased in available:
        return aliased
    return key


def normalize(name: str) -> str:
    """Backward-compatible helper; prefer resolve_name with an index."""
    key = strip_name(name)
    return ALIASES.get(key, key)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def is_primary_scope(scope: str) -> bool:
    return (scope or "").strip() == "SALADY"


def dedupe_by_name(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep one row per stripped name; prefer 적용범위=SALADY."""
    chosen: dict[str, dict[str, str]] = {}
    for row in rows:
        key = strip_name(row.get("메뉴명", ""))
        if not key:
            continue
        prev = chosen.get(key)
        if prev is None:
            chosen[key] = row
            continue
        prev_primary = is_primary_scope(prev.get("적용범위", ""))
        cur_primary = is_primary_scope(row.get("적용범위", ""))
        if cur_primary and not prev_primary:
            chosen[key] = row
        # if both primary or both non-primary, keep the earlier (first) row
    return list(chosen.values())


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return float(text)


def csv_nutrition_fields(row: dict[str, str]) -> dict[str, float | None]:
    return {
        key: parse_float(row.get(col))
        for key, col in zip(NUTR_KEYS, CSV_NUTR_COLS, strict=True)
    }


def fields_equal(a: dict[str, Any], b: dict[str, float | None]) -> bool:
    for key in NUTR_KEYS:
        left = a.get(key)
        right = b.get(key)
        if left is None and right is None:
            continue
        if left is None or right is None:
            return False
        if round(float(left), 1) != round(float(right), 1):
            return False
    return True


def index_by_norm_name(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        out.setdefault(strip_name(str(row.get("name", ""))), []).append(row)
    return out


def lookup_by_name(
    index: dict[str, list[dict[str, Any]]], name: str
) -> list[dict[str, Any]]:
    key = resolve_name(name, index)
    return index.get(key, [])


def next_id(rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 1
    return max(int(r["id"]) for r in rows) + 1


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    raw = url.replace("jdbc:mysql://", "")
    host_port, _, rest = raw.partition("/")
    db = rest.split("?", 1)[0]
    if ":" in host_port:
        host, port_s = host_port.split(":", 1)
        port = int(port_s)
    else:
        host, port = host_port, 3306
    return host, port, db


def load_backend_env() -> None:
    """Load ASAK-back/.env into os.environ if vars are missing."""
    here = Path(__file__).resolve()
    candidates = [
        here.parents[3] / "ASAK-back" / ".env",  # workspace/ASAK-back
        here.parents[2] / "ASAK-back" / ".env",
        here.parents[1] / "ASAK-back" / ".env",
    ]
    env_path = next((p for p in candidates if p.exists()), None)
    if env_path is None:
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def update_nutrition(
    menus: list[dict[str, Any]],
    ings: list[dict[str, Any]],
    menu_nutr: list[dict[str, Any]],
    ing_nutr: list[dict[str, Any]],
    nutrition_rows: list[dict[str, str]],
) -> dict[str, Any]:
    menu_by_name = index_by_norm_name(menus)
    ing_by_name = index_by_norm_name(ings)
    menu_nutr_by_menu = {int(r["menu_id"]): r for r in menu_nutr}
    ing_nutr_by_ing = {int(r["ing_id"]): r for r in ing_nutr}

    report: dict[str, Any] = {
        "menu_matched": [],
        "menu_updated": [],
        "menu_unchanged": [],
        "ing_matched": [],
        "ing_updated": [],
        "ing_unchanged": [],
        "unmatched": [],
    }

    for row in nutrition_rows:
        raw_name = (row.get("메뉴명") or "").strip()
        cat = (row.get("구분") or "").strip()
        fields = csv_nutrition_fields(row)
        menu_hits = lookup_by_name(menu_by_name, raw_name)
        ing_hits = lookup_by_name(ing_by_name, raw_name)

        if not menu_hits and not ing_hits:
            report["unmatched"].append(
                {"name": raw_name, "category": cat, "scope": row.get("적용범위")}
            )
            continue

        if menu_hits:
            report["menu_matched"].append(
                {"name": raw_name, "menu_ids": [m["id"] for m in menu_hits]}
            )
            for menu in menu_hits:
                menu_id = int(menu["id"])
                existing = menu_nutr_by_menu.get(menu_id)
                if existing is None:
                    existing = {
                        "id": menu_id,
                        "menu_id": menu_id,
                        "source_id": 41,
                    }
                    for k in NUTR_KEYS:
                        existing[k] = None
                    menu_nutr.append(existing)
                    menu_nutr_by_menu[menu_id] = existing
                before = {k: existing.get(k) for k in NUTR_KEYS}
                if fields_equal(existing, fields):
                    report["menu_unchanged"].append({"menu_id": menu_id, "name": raw_name})
                else:
                    existing.update(fields)
                    if existing.get("source_id") is None:
                        existing["source_id"] = 41
                    report["menu_updated"].append(
                        {
                            "menu_id": menu_id,
                            "name": raw_name,
                            "before": before,
                            "after": {k: existing.get(k) for k in NUTR_KEYS},
                        }
                    )

        if ing_hits:
            report["ing_matched"].append(
                {"name": raw_name, "ing_ids": [i["id"] for i in ing_hits]}
            )
            for ing in ing_hits:
                ing_id = int(ing["id"])
                existing = ing_nutr_by_ing.get(ing_id)
                if existing is None:
                    existing = {
                        "id": ing_id,
                        "ing_id": ing_id,
                        "source_id": None,
                    }
                    for k in NUTR_KEYS:
                        existing[k] = None
                    ing_nutr.append(existing)
                    ing_nutr_by_ing[ing_id] = existing
                before = {k: existing.get(k) for k in NUTR_KEYS}
                if fields_equal(existing, fields):
                    report["ing_unchanged"].append({"ing_id": ing_id, "name": raw_name})
                else:
                    existing.update(fields)
                    report["ing_updated"].append(
                        {
                            "ing_id": ing_id,
                            "name": raw_name,
                            "before": before,
                            "after": {k: existing.get(k) for k in NUTR_KEYS},
                        }
                    )

    return report


def allergen_cols(allergy_rows: list[dict[str, str]]) -> list[str]:
    if not allergy_rows:
        return []
    keys = list(allergy_rows[0].keys())
    return keys[3:]


def update_ing_allergens(
    ings: list[dict[str, Any]],
    allergens: list[dict[str, Any]],
    ing_allergen: list[dict[str, Any]],
    allergy_rows: list[dict[str, str]],
) -> dict[str, Any]:
    ing_by_name = index_by_norm_name(ings)
    allergen_id_by_name = {a["name"]: int(a["id"]) for a in allergens}
    known_cols = allergen_cols(allergy_rows)

    by_ing: dict[int, set[int]] = {}
    for link in ing_allergen:
        by_ing.setdefault(int(link["ing_id"]), set()).add(int(link["allergen_id"]))

    report: dict[str, Any] = {
        "ing_matched": [],
        "ing_updated": [],
        "ing_unchanged": [],
        "unmatched": [],
        "skipped_unknown_allergen_cols": [],
        "unknown_col_hits": {},
    }

    touched_ing_ids: set[int] = set()
    desired_by_ing: dict[int, set[int]] = {}

    for row in allergy_rows:
        raw_name = (row.get("메뉴명") or "").strip()
        cat = (row.get("구분") or "").strip()
        ing_hits = lookup_by_name(ing_by_name, raw_name)
        if not ing_hits:
            # menu-only or unknown — handled in menu allergy report
            if cat in ING_CATS:
                report["unmatched"].append(
                    {"name": raw_name, "category": cat, "scope": row.get("적용범위")}
                )
            continue

        marks = [c for c in known_cols if (row.get(c) or "").strip() == "●"]
        mapped: set[int] = set()
        for col in marks:
            aid = allergen_id_by_name.get(col)
            if aid is None:
                report["unknown_col_hits"][col] = report["unknown_col_hits"].get(col, 0) + 1
                if col not in report["skipped_unknown_allergen_cols"]:
                    report["skipped_unknown_allergen_cols"].append(col)
                continue
            mapped.add(aid)

        report["ing_matched"].append(
            {"name": raw_name, "ing_ids": [i["id"] for i in ing_hits], "allergens": marks}
        )
        for ing in ing_hits:
            ing_id = int(ing["id"])
            touched_ing_ids.add(ing_id)
            desired_by_ing[ing_id] = set(mapped)

    # rebuild links for touched ingredients only
    kept = [link for link in ing_allergen if int(link["ing_id"]) not in touched_ing_ids]
    nid = next_id(ing_allergen)
    for ing_id in sorted(touched_ing_ids):
        current = by_ing.get(ing_id, set())
        desired = desired_by_ing.get(ing_id, set())
        name = next(
            (i["name"] for i in ings if int(i["id"]) == ing_id),
            str(ing_id),
        )
        if current == desired:
            report["ing_unchanged"].append({"ing_id": ing_id, "name": name})
        else:
            cur_names = sorted(
                a["name"] for a in allergens if int(a["id"]) in current
            )
            new_names = sorted(
                a["name"] for a in allergens if int(a["id"]) in desired
            )
            report["ing_updated"].append(
                {
                    "ing_id": ing_id,
                    "name": name,
                    "before": cur_names,
                    "after": new_names,
                }
            )
        for aid in sorted(desired):
            kept.append({"id": nid, "ing_id": ing_id, "allergen_id": aid})
            nid += 1

    ing_allergen[:] = kept
    return report


def menu_allergy_validation(
    menus: list[dict[str, Any]],
    allergens: list[dict[str, Any]],
    menu_ing: list[dict[str, Any]],
    ing_allergen: list[dict[str, Any]],
    allergy_rows: list[dict[str, str]],
) -> dict[str, Any]:
    menu_by_name = index_by_norm_name(menus)
    allergen_id_by_name = {a["name"]: int(a["id"]) for a in allergens}
    allergen_name_by_id = {int(a["id"]): a["name"] for a in allergens}
    known_cols = allergen_cols(allergy_rows)

    ings_by_menu: dict[int, list[int]] = {}
    for mi in menu_ing:
        ings_by_menu.setdefault(int(mi["menu_id"]), []).append(int(mi["ing_id"]))

    allergens_by_ing: dict[int, set[int]] = {}
    for link in ing_allergen:
        allergens_by_ing.setdefault(int(link["ing_id"]), set()).add(
            int(link["allergen_id"])
        )

    mismatches = []
    matched = 0
    unmatched_menu = []

    for row in allergy_rows:
        raw_name = (row.get("메뉴명") or "").strip()
        menu_hits = lookup_by_name(menu_by_name, raw_name)
        if not menu_hits:
            continue
        matched += 1
        csv_marks = {
            c
            for c in known_cols
            if (row.get(c) or "").strip() == "●" and c in allergen_id_by_name
        }
        for menu in menu_hits:
            menu_id = int(menu["id"])
            derived_ids: set[int] = set()
            for ing_id in ings_by_menu.get(menu_id, []):
                derived_ids |= allergens_by_ing.get(ing_id, set())
            derived_names = {allergen_name_by_id[i] for i in derived_ids if i in allergen_name_by_id}
            if derived_names != csv_marks:
                mismatches.append(
                    {
                        "menu_id": menu_id,
                        "name": raw_name,
                        "csv": sorted(csv_marks),
                        "derived": sorted(derived_names),
                        "only_csv": sorted(csv_marks - derived_names),
                        "only_derived": sorted(derived_names - csv_marks),
                    }
                )

    # names that look like menus but missing from seed
    for row in allergy_rows:
        raw_name = (row.get("메뉴명") or "").strip()
        cat = (row.get("구분") or "").strip()
        if cat in ING_CATS:
            continue
        if not lookup_by_name(menu_by_name, raw_name):
            unmatched_menu.append(
                {"name": raw_name, "category": cat, "scope": row.get("적용범위")}
            )

    return {
        "menus_checked": matched,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "unmatched_menu_rows": unmatched_menu,
    }


def apply_to_mysql(
    menu_nutr: list[dict[str, Any]],
    ing_nutr: list[dict[str, Any]],
    ing_allergen: list[dict[str, Any]],
) -> dict[str, int]:
    import pymysql

    load_backend_env()
    url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    if not url or not user:
        raise RuntimeError("DB_URL / DB_USERNAME required (ASAK-back/.env or env)")

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
    stats = {
        "menu_nutr": 0,
        "menu_nutr_skipped": 0,
        "ing_nutr": 0,
        "ing_nutr_skipped": 0,
        "ing_allergen_deleted": 0,
        "ing_allergen_inserted": 0,
    }
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT `id` FROM `menu`")
            existing_menus = {int(r[0]) for r in cur.fetchall()}
            cur.execute("SELECT `id` FROM `ing`")
            existing_ings = {int(r[0]) for r in cur.fetchall()}
            cur.execute("SELECT `id` FROM `allergen`")
            existing_allergens = {int(r[0]) for r in cur.fetchall()}

            # menu_nutr upsert (only for menus present in DB)
            sql_menu = """
                INSERT INTO `menu_nutr`
                  (`id`, `menu_id`, `kcal`, `protein_g`, `carb_g`, `fat_g`, `sodium_mg`,
                   `source_id`, `serving_g`, `sugar_g`, `saturated_fat_g`)
                VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  `kcal`=VALUES(`kcal`),
                  `protein_g`=VALUES(`protein_g`),
                  `carb_g`=VALUES(`carb_g`),
                  `fat_g`=VALUES(`fat_g`),
                  `sodium_mg`=VALUES(`sodium_mg`),
                  `source_id`=VALUES(`source_id`),
                  `serving_g`=VALUES(`serving_g`),
                  `sugar_g`=VALUES(`sugar_g`),
                  `saturated_fat_g`=VALUES(`saturated_fat_g`)
            """
            menu_params = [
                (
                    r.get("id"),
                    r.get("menu_id"),
                    r.get("kcal"),
                    r.get("protein_g"),
                    r.get("carb_g"),
                    r.get("fat_g"),
                    r.get("sodium_mg"),
                    r.get("source_id"),
                    r.get("serving_g"),
                    r.get("sugar_g"),
                    r.get("saturated_fat_g"),
                )
                for r in menu_nutr
                if int(r["menu_id"]) in existing_menus
            ]
            skipped_menu = [
                int(r["menu_id"])
                for r in menu_nutr
                if int(r["menu_id"]) not in existing_menus
            ]
            if menu_params:
                cur.executemany(sql_menu, menu_params)
            stats["menu_nutr"] = len(menu_params)
            stats["menu_nutr_skipped"] = len(skipped_menu)

            sql_ing = """
                INSERT INTO `ing_nutr`
                  (`id`, `ing_id`, `serving_g`, `kcal`, `carb_g`, `sugar_g`, `protein_g`,
                   `fat_g`, `saturated_fat_g`, `sodium_mg`, `source_id`)
                VALUES
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  `serving_g`=VALUES(`serving_g`),
                  `kcal`=VALUES(`kcal`),
                  `carb_g`=VALUES(`carb_g`),
                  `sugar_g`=VALUES(`sugar_g`),
                  `protein_g`=VALUES(`protein_g`),
                  `fat_g`=VALUES(`fat_g`),
                  `saturated_fat_g`=VALUES(`saturated_fat_g`),
                  `sodium_mg`=VALUES(`sodium_mg`),
                  `source_id`=VALUES(`source_id`)
            """
            ing_params = [
                (
                    r.get("id"),
                    r.get("ing_id"),
                    r.get("serving_g"),
                    r.get("kcal"),
                    r.get("carb_g"),
                    r.get("sugar_g"),
                    r.get("protein_g"),
                    r.get("fat_g"),
                    r.get("saturated_fat_g"),
                    r.get("sodium_mg"),
                    r.get("source_id"),
                )
                for r in ing_nutr
                if int(r["ing_id"]) in existing_ings
            ]
            if ing_params:
                cur.executemany(sql_ing, ing_params)
            stats["ing_nutr"] = len(ing_params)
            stats["ing_nutr_skipped"] = sum(
                1 for r in ing_nutr if int(r["ing_id"]) not in existing_ings
            )

            # Replace entire ing_allergen from seed (filter to existing FKs)
            cur.execute("SELECT COUNT(*) FROM `ing_allergen`")
            before = cur.fetchone()[0]
            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            cur.execute("DELETE FROM `ing_allergen`")
            stats["ing_allergen_deleted"] = before
            sql_ia = (
                "INSERT INTO `ing_allergen` (`id`, `ing_id`, `allergen_id`) VALUES (%s, %s, %s)"
            )
            ia_params = [
                (r.get("id"), r.get("ing_id"), r.get("allergen_id"))
                for r in ing_allergen
                if int(r["ing_id"]) in existing_ings
                and int(r["allergen_id"]) in existing_allergens
            ]
            if ia_params:
                cur.executemany(sql_ia, ia_params)
            stats["ing_allergen_inserted"] = len(ia_params)
            cur.execute("SET FOREIGN_KEY_CHECKS=1")

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return stats


def verify_mysql_sample() -> dict[str, Any]:
    import pymysql

    load_backend_env()
    url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    host, port, db = parse_jdbc_url(url)
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password or "",
        database=db,
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT m.id, m.name, n.kcal, n.serving_g, n.sugar_g, n.saturated_fat_g
                FROM menu m
                JOIN menu_nutr n ON n.menu_id = m.id
                WHERE m.name LIKE %s
                ORDER BY m.id
                """,
                ("%로스트닭다리살%샐러%",),
            )
            roast = cur.fetchall()
            cur.execute(
                """
                SELECT COUNT(*) FROM menu_nutr
                WHERE serving_g IS NOT NULL AND sugar_g IS NOT NULL AND saturated_fat_g IS NOT NULL
                """
            )
            filled = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM menu_nutr")
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM ing_allergen")
            ia = cur.fetchone()[0]
        return {
            "roast_chicken_salad": [
                {
                    "id": r[0],
                    "name": r[1],
                    "kcal": float(r[2]) if r[2] is not None else None,
                    "serving_g": float(r[3]) if r[3] is not None else None,
                    "sugar_g": float(r[4]) if r[4] is not None else None,
                    "saturated_fat_g": float(r[5]) if r[5] is not None else None,
                }
                for r in roast
            ],
            "menu_nutr_filled": filled,
            "menu_nutr_total": total,
            "ing_allergen_count": ia,
        }
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nutrition-csv", type=Path, default=DEFAULT_NUTRITION)
    parser.add_argument("--allergy-csv", type=Path, default=DEFAULT_ALLERGY)
    parser.add_argument(
        "--apply-db",
        action="store_true",
        help="Upsert updated seed rows into MySQL (ASAK-back/.env)",
    )
    parser.add_argument(
        "--skip-seed-write",
        action="store_true",
        help="Compute report only; do not rewrite seed JSON",
    )
    args = parser.parse_args()

    if not args.nutrition_csv.exists():
        print(f"missing nutrition csv: {args.nutrition_csv}", file=sys.stderr)
        return 1
    if not args.allergy_csv.exists():
        print(f"missing allergy csv: {args.allergy_csv}", file=sys.stderr)
        return 1

    menus = load_json(SEED / "menu.json")
    ings = load_json(SEED / "ing.json")
    allergens = load_json(SEED / "allergen.json")
    menu_nutr = load_json(SEED / "menu_nutr.json")
    ing_nutr = load_json(SEED / "ing_nutr.json")
    ing_allergen = load_json(SEED / "ing_allergen.json")
    menu_ing = load_json(SEED / "menu_ing.json")

    nutrition_raw = load_csv(args.nutrition_csv)
    allergy_raw = load_csv(args.allergy_csv)
    nutrition_rows = dedupe_by_name(nutrition_raw)
    allergy_rows = dedupe_by_name(allergy_raw)

    nutr_report = update_nutrition(menus, ings, menu_nutr, ing_nutr, nutrition_rows)
    allergy_report = update_ing_allergens(ings, allergens, ing_allergen, allergy_rows)
    menu_allergy_report = menu_allergy_validation(
        menus, allergens, menu_ing, ing_allergen, allergy_rows
    )

    if not args.skip_seed_write:
        dump_json(SEED / "menu_nutr.json", menu_nutr)
        dump_json(SEED / "ing_nutr.json", ing_nutr)
        dump_json(SEED / "ing_allergen.json", ing_allergen)

    db_stats = None
    verify = None
    if args.apply_db:
        db_stats = apply_to_mysql(menu_nutr, ing_nutr, ing_allergen)
        verify = verify_mysql_sample()

    report = {
        "source": {
            "nutrition_csv": str(args.nutrition_csv),
            "allergy_csv": str(args.allergy_csv),
            "nutrition_rows_raw": len(nutrition_raw),
            "nutrition_rows_deduped": len(nutrition_rows),
            "allergy_rows_raw": len(allergy_raw),
            "allergy_rows_deduped": len(allergy_rows),
            "prefer_scope": "SALADY",
        },
        "nutrition": {
            "menu_matched": len(nutr_report["menu_matched"]),
            "menu_updated": len(nutr_report["menu_updated"]),
            "menu_unchanged": len(nutr_report["menu_unchanged"]),
            "ing_matched": len(nutr_report["ing_matched"]),
            "ing_updated": len(nutr_report["ing_updated"]),
            "ing_unchanged": len(nutr_report["ing_unchanged"]),
            "unmatched": nutr_report["unmatched"],
            "menu_updated_sample": nutr_report["menu_updated"][:20],
            "ing_updated_sample": nutr_report["ing_updated"][:20],
        },
        "allergy_ingredients": {
            "ing_matched": len(allergy_report["ing_matched"]),
            "ing_updated": len(allergy_report["ing_updated"]),
            "ing_unchanged": len(allergy_report["ing_unchanged"]),
            "unmatched": allergy_report["unmatched"],
            "skipped_unknown_allergen_cols": allergy_report["skipped_unknown_allergen_cols"],
            "unknown_col_hits": allergy_report["unknown_col_hits"],
            "ing_updated_sample": allergy_report["ing_updated"][:20],
        },
        "allergy_menu_validation": menu_allergy_report,
        "db_apply": db_stats,
        "db_verify": verify,
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    dump_json(REPORT_PATH, report)

    print(f"report -> {REPORT_PATH}")
    print(
        "nutrition: menu_updated=%s ing_updated=%s unmatched=%s"
        % (
            report["nutrition"]["menu_updated"],
            report["nutrition"]["ing_updated"],
            len(report["nutrition"]["unmatched"]),
        )
    )
    print(
        "allergy ing: updated=%s unchanged=%s"
        % (
            report["allergy_ingredients"]["ing_updated"],
            report["allergy_ingredients"]["ing_unchanged"],
        )
    )
    print(
        "menu allergy mismatches=%s"
        % report["allergy_menu_validation"]["mismatch_count"]
    )
    if db_stats:
        print("db_apply:", db_stats)
    if verify:
        print("db_verify:", json.dumps(verify, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
