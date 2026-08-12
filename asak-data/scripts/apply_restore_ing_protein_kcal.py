#!/usr/bin/env python3
"""Restore protein_g, kcal columns onto ing from ing_nutr (idempotent)."""

from __future__ import annotations

import os
import sys

import pymysql

RESTORE_COLS = ["kcal", "protein_g"]


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


def existing_columns(cur, table: str) -> set[str]:
    cur.execute(
        """
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
        """,
        (table,),
    )
    return {row[0] for row in cur.fetchall()}


def table_exists(cur, table: str) -> bool:
    cur.execute(
        """
        SELECT 1
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
        """,
        (table,),
    )
    return cur.fetchone() is not None


def add_missing_columns(cur, present: set[str]) -> list[str]:
    added = []
    for col in RESTORE_COLS:
        if col in present:
            continue
        comment = "칼로리" if col == "kcal" else "단백질 g"
        cur.execute(
            f"ALTER TABLE `ing` ADD COLUMN `{col}` DECIMAL(8,2) NULL COMMENT '{comment}'"
        )
        added.append(col)
    return added


def backfill_from_ing_nutr(cur) -> int:
    sql = """
        UPDATE `ing` i
        JOIN `ing_nutr` n ON n.`ing_id` = i.`id`
        SET i.`kcal` = n.`kcal`,
            i.`protein_g` = n.`protein_g`
    """
    cur.execute(sql)
    return cur.rowcount


def main() -> int:
    url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    if not url or not user:
        print("DB_URL / DB_USERNAME env required", file=sys.stderr)
        return 1

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
    try:
        with conn.cursor() as cur:
            if not table_exists(cur, "ing"):
                print("missing table: ing", file=sys.stderr)
                return 1
            if not table_exists(cur, "ing_nutr"):
                print("missing table: ing_nutr", file=sys.stderr)
                return 1

            present = existing_columns(cur, "ing")
            added = add_missing_columns(cur, present)
            print(f"added columns: {added or 'none (already present)'}")

            affected = backfill_from_ing_nutr(cur)
            print(f"backfilled rows affected={affected}")

            print("ing cols=", sorted(existing_columns(cur, "ing")))
        conn.commit()
        print("done")
        return 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
