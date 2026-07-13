#!/usr/bin/env python3
"""Rename ASAK MySQL tables and columns to the short-name convention.

The migration only renames identifiers; it never deletes or rewrites rows.
Before applying, it writes SHOW CREATE TABLE snapshots to ``--backup-dir``.
Use --rollback to apply the exact inverse mapping.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pymysql


ROOT = Path(__file__).resolve().parents[2]

TABLE_RENAMES = {
    "menu_nutrition": "menu_nutr",
    "ingredient": "ing",
    "ingredient_allergen": "ing_allergen",
    "menu_ingredient": "menu_ing",
    "option_group": "opt_group",
    "option_item": "opt_item",
    "option_item_component": "opt_item_comp",
    "option_policy": "opt_policy",
    "option_policy_item": "opt_policy_item",
    "menu_option_policy": "menu_opt_policy",
    "menu_option_override": "menu_opt_override",
    "payment_method_config": "pay_method_cfg",
    "menu_option_group_legacy_20260710": "menu_opt_grp_legacy_20260710",
    "menu_option_legacy_20260710": "menu_opt_legacy_20260710",
}

# Keys are source table names before TABLE_RENAMES.  Each rename is safe to
# rerun: it is applied only when the old name still exists.
COLUMN_RENAMES = {
    "category": {"is_active": "active", "sort_order": "sort_no"},
    "code_group": {},
    "common_code": {
        "code_group_id": "code_grp_id",
        "is_active": "active",
        "sort_order": "sort_no",
    },
    "tag": {"is_active": "active"},
    "menu": {"category_id": "cat_id", "is_sold_out": "sold_out"},
    "menu_tag": {},
    "menu_nutrition": {},
    "ingredient": {"is_sold_out": "sold_out"},
    "allergen": {},
    "ingredient_allergen": {"ingredient_id": "ing_id"},
    "menu_ingredient": {
        "ingredient_id": "ing_id",
        "sort_order": "sort_no",
    },
    "option_group": {},
    "option_item": {
        "option_group_id": "opt_group_id",
        "ingredient_id": "ing_id",
        "extra_price": "add_price",
        "original_price": "list_price",
        "is_sold_out": "sold_out",
    },
    "option_item_component": {
        "option_item_id": "opt_item_id",
        "ingredient_id": "ing_id",
        "sort_order": "sort_no",
    },
    "option_policy": {
        "option_group_id": "opt_group_id",
        "sort_order": "sort_no",
        "is_required": "required",
        "is_active": "active",
    },
    "option_policy_item": {
        "option_item_id": "opt_item_id",
        "is_recommended": "recommended",
        "sort_order": "sort_no",
        "is_active": "active",
    },
    "menu_option_policy": {
        "sort_order": "sort_no",
        "is_required": "required",
    },
    "menu_option_override": {
        "option_item_id": "opt_item_id",
        "is_recommended": "recommended",
        "sort_order": "sort_no",
        "is_active": "active",
    },
    "payment_method_config": {"is_active": "active", "sort_order": "sort_no"},
    "orders": {},
    "order_item": {},
    "order_item_option": {"option_item_id": "opt_item_id"},
    "item_exclusion": {"ingredient_id": "ing_id"},
    "payment": {},
    "menu_option_group_legacy_20260710": {
        "option_group_id": "opt_group_id",
        "sort_order": "sort_no",
        "is_required": "required",
    },
    "menu_option_legacy_20260710": {
        "option_item_id": "opt_item_id",
        "is_recommended": "recommended",
        "sort_order": "sort_no",
        "is_active": "active",
    },
}


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--backup-dir", type=Path, default=ROOT / "asak-data" / "schema-backups")
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Perform changes; omit for a dry run.")
    return parser.parse_args()


def quote(name: str) -> str:
    return "`" + name.replace("`", "``") + "`"


def tables(cur: pymysql.cursors.Cursor) -> set[str]:
    cur.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
    return {row[0] for row in cur.fetchall()}


def columns(cur: pymysql.cursors.Cursor, table: str) -> set[str]:
    cur.execute(f"SHOW COLUMNS FROM {quote(table)}")
    return {row[0] for row in cur.fetchall()}


def snapshot(cur: pymysql.cursors.Cursor, backup_dir: Path, db_tables: set[str]) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = backup_dir / f"short-name-before-{stamp}.sql"
    target.parent.mkdir(parents=True, exist_ok=True)
    chunks = ["-- ASAK schema snapshot before short-name migration\n"]
    for table in sorted(db_tables):
        cur.execute(f"SHOW CREATE TABLE {quote(table)}")
        _, ddl = cur.fetchone()
        chunks.append(f"DROP TABLE IF EXISTS {quote(table)};\n{ddl};\n")
    target.write_text("\n".join(chunks), encoding="utf-8")
    return target


def inverse(mapping: dict[str, str]) -> dict[str, str]:
    return {new: old for old, new in mapping.items()}


def main() -> None:
    config = args()
    table_map = inverse(TABLE_RENAMES) if config.rollback else TABLE_RENAMES
    column_map = {
        # In a dry run, inspect the current (pre-migration) table name.  In an
        # applied migration, inspect the name after the table rename step.
        (
            table
            if config.apply == config.rollback
            else TABLE_RENAMES.get(table, table)
        ): inverse(mapping) if config.rollback else mapping
        for table, mapping in COLUMN_RENAMES.items()
    }

    conn = pymysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database,
        charset="utf8mb4",
        autocommit=False,
    )
    try:
        with conn.cursor() as cur:
            db_tables = tables(cur)
            if config.apply:
                backup = snapshot(cur, config.backup_dir, db_tables)
                print(f"Schema snapshot: {backup}")

            for old, new in table_map.items():
                if old in db_tables and new not in db_tables:
                    print(f"TABLE {old} -> {new}")
                    if config.apply:
                        cur.execute(f"RENAME TABLE {quote(old)} TO {quote(new)}")
                    if config.apply:
                        db_tables.remove(old)
                        db_tables.add(new)

            for table, mapping in column_map.items():
                if table not in db_tables:
                    continue
                table_columns = columns(cur, table)
                for old, new in mapping.items():
                    if old in table_columns and new not in table_columns:
                        print(f"COLUMN {table}.{old} -> {new}")
                        if config.apply:
                            cur.execute(
                                f"ALTER TABLE {quote(table)} RENAME COLUMN {quote(old)} TO {quote(new)}"
                            )
                        table_columns.remove(old)
                        table_columns.add(new)

            if config.apply:
                conn.commit()
                print("Short-name migration complete")
            else:
                print("Dry run only. Re-run with --apply to change the database.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
