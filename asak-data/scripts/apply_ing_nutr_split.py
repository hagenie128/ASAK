#!/usr/bin/env python3
"""Split ingredient nutrition columns from ing into ing_nutr (idempotent)."""

from __future__ import annotations

import os
import sys

import pymysql

NUTR_COLS = [
    "serving_g",
    "kcal",
    "carb_g",
    "sugar_g",
    "protein_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
]


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


def ensure_ing_nutr(cur) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS `ing_nutr` (
            `id` BIGINT NOT NULL PRIMARY KEY,
            `ing_id` BIGINT NOT NULL,
            `serving_g` DECIMAL(8,2) NULL COMMENT '표준 제공량 g',
            `kcal` DECIMAL(8,2) NULL COMMENT '칼로리',
            `carb_g` DECIMAL(8,2) NULL COMMENT '탄수화물 g',
            `sugar_g` DECIMAL(8,2) NULL COMMENT '당류 g',
            `protein_g` DECIMAL(8,2) NULL COMMENT '단백질 g',
            `fat_g` DECIMAL(8,2) NULL COMMENT '지방 g',
            `saturated_fat_g` DECIMAL(8,2) NULL COMMENT '포화지방 g',
            `sodium_mg` DECIMAL(8,2) NULL COMMENT '나트륨 mg',
            `source_id` BIGINT NULL COMMENT '데이터 출처 코드 ID',
            UNIQUE KEY `uq_ing_nutr_ing_id` (`ing_id`),
            CONSTRAINT `fk_ing_nutr_ing_id`
                FOREIGN KEY (`ing_id`) REFERENCES `ing` (`id`),
            CONSTRAINT `fk_ing_nutr_source_id`
                FOREIGN KEY (`source_id`) REFERENCES `common_code` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    print("ok table ing_nutr")


def copy_nutrition(cur, present: set[str]) -> int:
    selectable = [c for c in NUTR_COLS if c in present]
    if not selectable:
        print("skip copy: no nutrition columns on ing")
        return 0

    select_list = ", ".join(f"`{c}`" for c in selectable)
    insert_list = ", ".join(f"`{c}`" for c in selectable)
    update_list = ", ".join(f"`{c}`=VALUES(`{c}`)" for c in selectable)
    where = " OR ".join(f"`{c}` IS NOT NULL" for c in selectable)

    sql = f"""
        INSERT INTO `ing_nutr` (`id`, `ing_id`, {insert_list})
        SELECT `id`, `id`, {select_list}
        FROM `ing`
        WHERE {where}
        ON DUPLICATE KEY UPDATE {update_list}
    """
    cur.execute(sql)
    print(f"copied rows affected={cur.rowcount}")
    return cur.rowcount


def drop_ing_nutrition_columns(cur, present: set[str]) -> None:
    to_drop = [c for c in NUTR_COLS if c in present]
    if not to_drop:
        print("skip drop: nutrition columns already removed from ing")
        return
    drops = ", ".join(f"DROP COLUMN `{c}`" for c in to_drop)
    cur.execute(f"ALTER TABLE `ing` {drops}")
    print(f"dropped from ing: {', '.join(to_drop)}")


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
            ensure_ing_nutr(cur)
            present = existing_columns(cur, "ing")
            copy_nutrition(cur, present)
            drop_ing_nutrition_columns(cur, present)
            cur.execute("SELECT COUNT(*) FROM ing_nutr")
            print(f"ing_nutr count={cur.fetchone()[0]}")
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
