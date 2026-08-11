#!/usr/bin/env python3
"""Add missing nutrition columns to live MySQL (ing_nutr / menu_nutr) if absent."""

from __future__ import annotations

import os
import sys

import pymysql

COLUMNS = {
    "ing_nutr": [
        ("serving_g", "DECIMAL(8,2) NULL COMMENT '표준 제공량 g'"),
        ("kcal", "DECIMAL(8,2) NULL COMMENT '칼로리'"),
        ("carb_g", "DECIMAL(8,2) NULL COMMENT '탄수화물 g'"),
        ("sugar_g", "DECIMAL(8,2) NULL COMMENT '당류 g'"),
        ("protein_g", "DECIMAL(8,2) NULL COMMENT '단백질 g'"),
        ("fat_g", "DECIMAL(8,2) NULL COMMENT '지방 g'"),
        ("saturated_fat_g", "DECIMAL(8,2) NULL COMMENT '포화지방 g'"),
        ("sodium_mg", "DECIMAL(8,2) NULL COMMENT '나트륨 mg'"),
        ("source_id", "BIGINT NULL COMMENT '데이터 출처 코드 ID'"),
    ],
    "menu_nutr": [
        ("serving_g", "DECIMAL(8,2) NULL COMMENT '표준 제공량 g'"),
        ("sugar_g", "DECIMAL(8,2) NULL COMMENT '당류 g'"),
        ("saturated_fat_g", "DECIMAL(8,2) NULL COMMENT '포화지방 g'"),
    ],
}


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    # jdbc:mysql://host:port/db?...
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
        autocommit=True,
    )
    try:
        with conn.cursor() as cur:
            for table, cols in COLUMNS.items():
                present = existing_columns(cur, table)
                if not present:
                    print(f"skip missing table: {table}")
                    continue
                for name, ddl in cols:
                    if name in present:
                        print(f"ok exists {table}.{name}")
                        continue
                    sql = f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"
                    cur.execute(sql)
                    print(f"added {table}.{name}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
