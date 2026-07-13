#!/usr/bin/env python3
"""Build canonical short-name ASAK seed JSON from the preserved v2 seed."""
from __future__ import annotations

import json
from pathlib import Path

from apply_option_policy_mysql import build_policies

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "asak-data" / "seed"
TARGET = ROOT / "asak-data" / "seed-v3"

TABLES = {
    "menu_nutrition": "menu_nutr", "ingredient": "ing", "ingredient_allergen": "ing_allergen",
    "menu_ingredient": "menu_ing", "option_group": "opt_group", "option_item": "opt_item",
    "option_item_component": "opt_item_comp", "option_policy": "opt_policy",
    "option_policy_item": "opt_policy_item", "menu_option_policy": "menu_opt_policy",
    "menu_option_override": "menu_opt_override", "payment_method_config": "pay_method_cfg",
    "menu_option_group": "menu_opt_grp_legacy_20260710", "menu_option": "menu_opt_legacy_20260710",
}
COLUMNS = {
    "category_id": "cat_id", "ingredient_id": "ing_id", "option_group_id": "opt_group_id",
    "option_item_id": "opt_item_id", "code_group_id": "code_grp_id", "is_active": "active",
    "is_sold_out": "sold_out", "is_required": "required", "is_recommended": "recommended",
    "sort_order": "sort_no", "original_price": "list_price", "extra_price": "add_price",
}

def renamed(row: dict) -> dict:
    return {COLUMNS.get(k, k): v for k, v in row.items() if k != "_source_ref"}

def read(name: str) -> list[dict]:
    return json.loads((SOURCE / f"{name}.json").read_text(encoding="utf-8"))

def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    output: dict[str, list[dict]] = {}
    for old in manifest["paths"]:
        new = TABLES.get(old, old)
        output[new] = [renamed(row) for row in read(old)]
    policies, policy_items, menu_policies = build_policies(SOURCE)
    output["opt_policy"] = [renamed(row) for row in policies]
    output["opt_policy_item"] = [renamed(row) for row in policy_items]
    output["menu_opt_policy"] = [renamed(row) for row in menu_policies]
    output["menu_opt_override"] = []
    for table, rows in output.items():
        (TARGET / f"{table}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    new_manifest = {**manifest, "schema_version": 3, "note": "ASAK short-name canonical seed", "counts": {k: len(v) for k, v in output.items()}, "paths": {k: f"seed-v3/{k}.json" for k in output}}
    (TARGET / "manifest.json").write_text(json.dumps(new_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(output)} tables to {TARGET}")

if __name__ == "__main__":
    main()
