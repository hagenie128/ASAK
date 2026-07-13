#!/usr/bin/env python3
"""Add reusable option policy tables and populate them from ASAK seed JSON.

The original MVP schema keeps every menu-option relation in menu_option. This
script preserves those compatibility tables and adds reusable option policies
deduplicated at the menu option-group level.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import pymysql


ROOT = Path(__file__).resolve().parents[2]
SEED_DIR = ROOT / "asak-data" / "seed"

DDL = [
    """
    CREATE TABLE IF NOT EXISTS option_policy (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        policy_key CHAR(64) NOT NULL UNIQUE,
        name VARCHAR(120) NOT NULL,
        option_group_id BIGINT NOT NULL,
        sort_order INT NOT NULL DEFAULT 0,
        is_required BOOLEAN NOT NULL DEFAULT FALSE,
        min_select INT NOT NULL DEFAULT 0,
        max_select INT NOT NULL DEFAULT 1,
        item_count INT NOT NULL DEFAULT 0,
        menu_count INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_option_policy_group
            FOREIGN KEY (option_group_id) REFERENCES option_group(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS option_policy_item (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        policy_id BIGINT NOT NULL,
        option_item_id BIGINT NOT NULL,
        is_recommended BOOLEAN NOT NULL DEFAULT FALSE,
        is_default BOOLEAN NOT NULL DEFAULT FALSE,
        sort_order INT NOT NULL DEFAULT 0,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        UNIQUE KEY uq_option_policy_item (policy_id, option_item_id),
        CONSTRAINT fk_option_policy_item_policy
            FOREIGN KEY (policy_id) REFERENCES option_policy(id),
        CONSTRAINT fk_option_policy_item_item
            FOREIGN KEY (option_item_id) REFERENCES option_item(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_option_policy (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL,
        policy_id BIGINT NOT NULL,
        sort_order INT NOT NULL DEFAULT 0,
        is_required BOOLEAN NOT NULL DEFAULT FALSE,
        priority INT NOT NULL DEFAULT 0,
        UNIQUE KEY uq_menu_option_policy (menu_id, policy_id),
        CONSTRAINT fk_menu_option_policy_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_option_policy_policy
            FOREIGN KEY (policy_id) REFERENCES option_policy(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS menu_option_override (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        menu_id BIGINT NOT NULL,
        option_item_id BIGINT NOT NULL,
        is_recommended BOOLEAN,
        is_default BOOLEAN,
        sort_order INT,
        is_active BOOLEAN,
        note VARCHAR(255),
        UNIQUE KEY uq_menu_option_override (menu_id, option_item_id),
        CONSTRAINT fk_menu_option_override_menu
            FOREIGN KEY (menu_id) REFERENCES menu(id),
        CONSTRAINT fk_menu_option_override_item
            FOREIGN KEY (option_item_id) REFERENCES option_item(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply ASAK option policy tables.")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--seed-dir", type=Path, default=SEED_DIR)
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing policy rows before rebuilding policies.",
    )
    return parser.parse_args()


def read_seed(seed_dir: Path, table: str) -> list[dict[str, Any]]:
    path = seed_dir / f"{table}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"{path} must contain a JSON array")
    return rows


def build_policies(seed_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    option_groups = {row["id"]: row for row in read_seed(seed_dir, "option_group")}
    option_items = {row["id"]: row for row in read_seed(seed_dir, "option_item")}
    menu_option_groups = read_seed(seed_dir, "menu_option_group")
    menu_options = read_seed(seed_dir, "menu_option")

    items_by_menu_group: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in menu_options:
        group_id = option_items[row["option_item_id"]]["option_group_id"]
        items_by_menu_group[(row["menu_id"], group_id)].append(row)

    signatures: dict[str, dict[str, Any]] = {}
    menu_policy_links: list[dict[str, Any]] = []

    for link in menu_option_groups:
        group_id = link["option_group_id"]
        items = sorted(
            items_by_menu_group[(link["menu_id"], group_id)],
            key=lambda row: (row["sort_order"], row["option_item_id"]),
        )
        payload = {
            "option_group_id": group_id,
            "sort_order": link["sort_order"],
            "is_required": bool(link["is_required"]),
            "min_select": option_groups[group_id]["min_select"],
            "max_select": option_groups[group_id]["max_select"],
            "items": [
                {
                    "option_item_id": item["option_item_id"],
                    "is_recommended": bool(item["is_recommended"]),
                    "is_default": bool(item["is_default"]),
                    "sort_order": item["sort_order"],
                    "is_active": bool(item["is_active"]),
                }
                for item in items
            ],
        }
        policy_key = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        policy = signatures.setdefault(
            policy_key,
            {
                "policy_key": policy_key,
                "option_group_id": group_id,
                "sort_order": link["sort_order"],
                "is_required": bool(link["is_required"]),
                "min_select": option_groups[group_id]["min_select"],
                "max_select": option_groups[group_id]["max_select"],
                "items": payload["items"],
                "menu_ids": set(),
            },
        )
        policy["menu_ids"].add(link["menu_id"])
        menu_policy_links.append(
            {
                "menu_id": link["menu_id"],
                "policy_key": policy_key,
                "sort_order": link["sort_order"],
                "is_required": bool(link["is_required"]),
            }
        )

    policies: list[dict[str, Any]] = []
    policy_items: list[dict[str, Any]] = []
    policy_id_by_key: dict[str, int] = {}
    for policy_id, policy in enumerate(
        sorted(signatures.values(), key=lambda row: (row["option_group_id"], row["sort_order"], row["policy_key"])),
        start=1,
    ):
        policy_id_by_key[policy["policy_key"]] = policy_id
        group_name = option_groups[policy["option_group_id"]]["name"]
        policies.append(
            {
                "id": policy_id,
                "policy_key": policy["policy_key"],
                "name": f"{group_name} policy {policy_id}",
                "option_group_id": policy["option_group_id"],
                "sort_order": policy["sort_order"],
                "is_required": policy["is_required"],
                "min_select": policy["min_select"],
                "max_select": policy["max_select"],
                "item_count": len(policy["items"]),
                "menu_count": len(policy["menu_ids"]),
                "is_active": True,
            }
        )
        for item in policy["items"]:
            policy_items.append({"policy_id": policy_id, **item})

    menu_policies = [
        {
            "menu_id": row["menu_id"],
            "policy_id": policy_id_by_key[row["policy_key"]],
            "sort_order": row["sort_order"],
            "is_required": row["is_required"],
            "priority": 0,
        }
        for row in menu_policy_links
    ]

    return policies, policy_items, menu_policies


def insert_rows(cur: pymysql.cursors.Cursor, table: str, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
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
    cur.executemany(sql, [tuple(row.get(column) for column in columns) for row in rows])
    return len(rows)


def main() -> None:
    args = parse_args()
    policies, policy_items, menu_policies = build_policies(args.seed_dir)

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
            # This script targets the pre-short-name option tables.  Refuse to
            # recreate that schema beside the canonical opt_* tables.
            cur.execute("SHOW TABLES LIKE 'opt_group'")
            if cur.fetchone():
                raise RuntimeError(
                    "Short-name schema detected. This legacy option-policy loader "
                    "cannot be used; update it for the canonical schema first."
                )
            for ddl in DDL:
                cur.execute(ddl)

            if args.replace:
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                for table in [
                    "menu_option_override",
                    "menu_option_policy",
                    "option_policy_item",
                    "option_policy",
                ]:
                    cur.execute(f"DELETE FROM `{table}`")
                    cur.execute(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1")
                cur.execute("SET FOREIGN_KEY_CHECKS = 1")

            counts = {
                "option_policy": insert_rows(cur, "option_policy", policies),
                "option_policy_item": insert_rows(cur, "option_policy_item", policy_items),
                "menu_option_policy": insert_rows(cur, "menu_option_policy", menu_policies),
                "menu_option_override": 0,
            }
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print("Option policy load complete")
    for table, count in counts.items():
        print(f"  {table}: {count}")


if __name__ == "__main__":
    main()
