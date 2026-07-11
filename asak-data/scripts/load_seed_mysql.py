#!/usr/bin/env python3
"""Create the ASAK MySQL schema and load seed JSON data.

This loader targets the 22-table ASAK MVP schema documented in the ERD notes.
It loads the current 17 seed tables from asak-data/seed and creates the 5 order
tables empty.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pymysql


ROOT = Path(__file__).resolve().parents[2]
SEED_DIR = ROOT / "asak-data" / "seed"

SEED_TABLE_ORDER = [
    "category",
    "code_group",
    "common_code",
    "tag",
    "menu",
    "menu_nutrition",
    "ingredient",
    "allergen",
    "ingredient_allergen",
    "menu_ingredient",
    "option_group",
    "option_item",
    "option_item_component",
    "menu_option_group",
    "menu_option",
    "menu_tag",
    "payment_method_config",
]

REPLACE_DELETE_ORDER = [
    "payment",
    "item_exclusion",
    "order_item_option",
    "order_item",
    "orders",
    "payment_method_config",
    "menu_option",
    "menu_option_group",
    "option_item_component",
    "option_item",
    "option_group",
    "menu_ingredient",
    "ingredient_allergen",
    "allergen",
    "ingredient",
    "menu_nutrition",
    "menu_tag",
    "menu",
    "tag",
    "common_code",
    "code_group",
    "category",
]

DDL = [
    """
    CREATE TABLE IF NOT EXISTS category (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        sort_order INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT TRUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS code_group (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        group_code VARCHAR(50) NOT NULL UNIQUE,
        name VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS common_code (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        code_group_id BIGINT NOT NULL,
        code VARCHAR(50) NOT NULL,
        name VARCHAR(50) NOT NULL,
        sort_order INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        UNIQUE KEY uq_common_code_group_code (code_group_id, code),
        CONSTRAINT fk_common_code_group
            FOREIGN KEY (code_group_id) REFERENCES code_group(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS tag (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        code VARCHAR(50) NOT NULL UNIQUE,
        name VARCHAR(50) NOT NULL,
        color_hex VARCHAR(20),
        is_active BOOLEAN NOT NULL DEFAULT TRUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        category_id BIGINT NOT NULL,
        name VARCHAR(100) NOT NULL,
        price INT NOT NULL DEFAULT 0,
        image_url TEXT,
        description TEXT,
        is_sold_out BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_menu_category
            FOREIGN KEY (category_id) REFERENCES category(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_tag (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL,
        tag_id BIGINT NOT NULL,
        UNIQUE KEY uq_menu_tag (menu_id, tag_id),
        CONSTRAINT fk_menu_tag_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_tag_tag
            FOREIGN KEY (tag_id) REFERENCES tag(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_nutrition (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL UNIQUE,
        kcal DECIMAL(8,2),
        protein_g DECIMAL(8,2),
        carb_g DECIMAL(8,2),
        fat_g DECIMAL(8,2),
        sodium_mg DECIMAL(8,2),
        source_id BIGINT,
        CONSTRAINT fk_menu_nutrition_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_nutrition_source
            FOREIGN KEY (source_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS ingredient (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL UNIQUE,
        type_id BIGINT NOT NULL,
        kcal DECIMAL(8,2),
        protein_g DECIMAL(8,2),
        is_sold_out BOOLEAN NOT NULL DEFAULT FALSE,
        CONSTRAINT fk_ingredient_type
            FOREIGN KEY (type_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS allergen (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS ingredient_allergen (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        ingredient_id BIGINT NOT NULL,
        allergen_id BIGINT NOT NULL,
        UNIQUE KEY uq_ingredient_allergen (ingredient_id, allergen_id),
        CONSTRAINT fk_ingredient_allergen_ingredient
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id),
        CONSTRAINT fk_ingredient_allergen_allergen
            FOREIGN KEY (allergen_id) REFERENCES allergen(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_ingredient (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL,
        ingredient_id BIGINT NOT NULL,
        role_id BIGINT NOT NULL,
        quantity DECIMAL(8,2),
        unit_id BIGINT,
        is_default BOOLEAN NOT NULL DEFAULT TRUE,
        can_remove BOOLEAN NOT NULL DEFAULT TRUE,
        sort_order INT NOT NULL DEFAULT 0,
        UNIQUE KEY uq_menu_ingredient_role (menu_id, ingredient_id, role_id),
        CONSTRAINT fk_menu_ingredient_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_ingredient_ingredient
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id),
        CONSTRAINT fk_menu_ingredient_role
            FOREIGN KEY (role_id) REFERENCES common_code(id),
        CONSTRAINT fk_menu_ingredient_unit
            FOREIGN KEY (unit_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS option_group (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        group_type_id BIGINT NOT NULL,
        min_select INT NOT NULL DEFAULT 0,
        max_select INT NOT NULL DEFAULT 1,
        CONSTRAINT fk_option_group_type
            FOREIGN KEY (group_type_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_option_group (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL,
        option_group_id BIGINT NOT NULL,
        sort_order INT NOT NULL DEFAULT 0,
        is_required BOOLEAN NOT NULL DEFAULT FALSE,
        UNIQUE KEY uq_menu_option_group (menu_id, option_group_id),
        CONSTRAINT fk_menu_option_group_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_option_group_group
            FOREIGN KEY (option_group_id) REFERENCES option_group(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS option_item (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        option_group_id BIGINT NOT NULL,
        ingredient_id BIGINT,
        name VARCHAR(100) NOT NULL,
        extra_price INT NOT NULL DEFAULT 0,
        original_price INT,
        amount DECIMAL(8,2),
        unit_id BIGINT,
        icon_url TEXT,
        color_hex VARCHAR(20),
        is_sold_out BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_option_item_group
            FOREIGN KEY (option_group_id) REFERENCES option_group(id),
        CONSTRAINT fk_option_item_ingredient
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id),
        CONSTRAINT fk_option_item_unit
            FOREIGN KEY (unit_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_option (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL,
        option_item_id BIGINT NOT NULL,
        is_recommended BOOLEAN NOT NULL DEFAULT FALSE,
        is_default BOOLEAN NOT NULL DEFAULT FALSE,
        sort_order INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        UNIQUE KEY uq_menu_option (menu_id, option_item_id),
        CONSTRAINT fk_menu_option_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_option_item
            FOREIGN KEY (option_item_id) REFERENCES option_item(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS option_item_component (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        option_item_id BIGINT NOT NULL,
        ingredient_id BIGINT,
        name VARCHAR(100) NOT NULL,
        quantity DECIMAL(8,2),
        unit_id BIGINT,
        sort_order INT NOT NULL DEFAULT 0,
        CONSTRAINT fk_option_item_component_item
            FOREIGN KEY (option_item_id) REFERENCES option_item(id),
        CONSTRAINT fk_option_item_component_ingredient
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id),
        CONSTRAINT fk_option_item_component_unit
            FOREIGN KEY (unit_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS payment_method_config (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        method_id BIGINT NOT NULL UNIQUE,
        name VARCHAR(50) NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        sort_order INT NOT NULL DEFAULT 0,
        CONSTRAINT fk_payment_method_config_method
            FOREIGN KEY (method_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_no VARCHAR(50) NOT NULL UNIQUE,
        order_type_id BIGINT NOT NULL,
        status_id BIGINT NOT NULL,
        total_price INT NOT NULL DEFAULT 0,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_orders_type
            FOREIGN KEY (order_type_id) REFERENCES common_code(id),
        CONSTRAINT fk_orders_status
            FOREIGN KEY (status_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS order_item (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_id BIGINT NOT NULL,
        menu_id BIGINT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        price INT NOT NULL DEFAULT 0,
        CONSTRAINT fk_order_item_order
            FOREIGN KEY (order_id) REFERENCES orders(id),
        CONSTRAINT fk_order_item_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS order_item_option (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_item_id BIGINT NOT NULL,
        option_item_id BIGINT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        price INT NOT NULL DEFAULT 0,
        UNIQUE KEY uq_order_item_option (order_item_id, option_item_id),
        CONSTRAINT fk_order_item_option_item
            FOREIGN KEY (order_item_id) REFERENCES order_item(id),
        CONSTRAINT fk_order_item_option_option
            FOREIGN KEY (option_item_id) REFERENCES option_item(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS item_exclusion (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_item_id BIGINT NOT NULL,
        ingredient_id BIGINT NOT NULL,
        UNIQUE KEY uq_item_exclusion (order_item_id, ingredient_id),
        CONSTRAINT fk_item_exclusion_order_item
            FOREIGN KEY (order_item_id) REFERENCES order_item(id),
        CONSTRAINT fk_item_exclusion_ingredient
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS payment (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_id BIGINT NOT NULL UNIQUE,
        method_id BIGINT NOT NULL,
        status_id BIGINT NOT NULL,
        amount INT NOT NULL DEFAULT 0,
        paid_at TIMESTAMP NULL,
        CONSTRAINT fk_payment_order
            FOREIGN KEY (order_id) REFERENCES orders(id),
        CONSTRAINT fk_payment_method
            FOREIGN KEY (method_id) REFERENCES common_code(id),
        CONSTRAINT fk_payment_status
            FOREIGN KEY (status_id) REFERENCES common_code(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load ASAK seed JSON into MySQL.")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--seed-dir", type=Path, default=SEED_DIR)
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete data from ASAK tables before loading seed rows.",
    )
    return parser.parse_args()


def load_rows(seed_dir: Path, table: str) -> list[dict[str, Any]]:
    path = seed_dir / f"{table}.json"
    if not path.exists():
        return []
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"{path} must contain a JSON array")
    return rows


def normalize_value(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def insert_rows(cur: pymysql.cursors.Cursor, table: str, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0

    rows = [{k: v for k, v in row.items() if not k.startswith("_")} for row in rows]
    columns = list(rows[0].keys())
    column_sql = ", ".join(f"`{column}`" for column in columns)
    placeholder_sql = ", ".join(["%s"] * len(columns))
    update_sql = ", ".join(
        f"`{column}` = VALUES(`{column}`)" for column in columns if column != "id"
    )
    sql = (
        f"INSERT INTO `{table}` ({column_sql}) VALUES ({placeholder_sql}) "
        f"ON DUPLICATE KEY UPDATE {update_sql or '`id` = VALUES(`id`)'}"
    )
    values = [
        tuple(normalize_value(row.get(column)) for column in columns)
        for row in rows
    ]
    cur.executemany(sql, values)
    return len(rows)


def main() -> None:
    args = parse_args()
    conn = pymysql.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
        charset="utf8mb4",
        autocommit=False,
    )
    try:
        with conn.cursor() as cur:
            for ddl in DDL:
                cur.execute(ddl)

            if args.replace:
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                for table in REPLACE_DELETE_ORDER:
                    cur.execute(f"DELETE FROM `{table}`")
                    cur.execute(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1")
                cur.execute("SET FOREIGN_KEY_CHECKS = 1")

            counts: dict[str, int] = {}
            for table in SEED_TABLE_ORDER:
                rows = load_rows(args.seed_dir, table)
                counts[table] = insert_rows(cur, table, rows)

            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print("MySQL seed load complete")
    for table in SEED_TABLE_ORDER:
        print(f"  {table}: {counts[table]}")
    for table in ["orders", "order_item", "order_item_option", "item_exclusion", "payment"]:
        print(f"  {table}: 0")


if __name__ == "__main__":
    main()
