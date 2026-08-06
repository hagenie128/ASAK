#!/usr/bin/env python3
"""dedupe_menus_report.json 기준 실DB(asak_db) 중복 메뉴 제거."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pymysql

OUT = Path(__file__).resolve().parent / "output"
REPORT = OUT / "dedupe_menus_report.json"

DB_CHILD_TABLES = [
    ("menu_opt_override", "menu_id"),
    ("menu_opt_policy", "menu_id"),
    ("menu_ing", "menu_id"),
    ("menu_nutr", "menu_id"),
    ("menu_tag", "menu_id"),
]


def connect():
    url = os.environ.get("DB_URL", "jdbc:mysql://nam3324.synology.me:33338/asak_db")
    # jdbc:mysql://host:port/db
    body = url.split("://", 1)[1]
    host_port, database = body.split("/", 1)
    host, port = host_port.split(":")
    return pymysql.connect(
        host=host,
        port=int(port),
        user=os.environ.get("DB_USERNAME", "asakasak"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=database.split("?", 1)[0],
        charset="utf8mb4",
        autocommit=False,
    )


def main() -> None:
    pairs = json.loads(REPORT.read_text(encoding="utf-8"))["pairs"]
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM menu")
    before = cur.fetchone()[0]
    print(f"before: {before} menus")

    try:
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        for row in pairs:
            remove_id = row["remove_id"]
            keep_id = row["keep_id"]
            name = row["name"]
            print(f"  remove {remove_id} -> keep {keep_id} ({name})")
            cur.execute(
                "UPDATE order_item SET menu_id = %s WHERE menu_id = %s",
                (keep_id, remove_id),
            )
            for table, col in DB_CHILD_TABLES:
                cur.execute(f"DELETE FROM `{table}` WHERE `{col}` = %s", (remove_id,))
            cur.execute("DELETE FROM menu WHERE id = %s", (remove_id,))

        cur.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    conn2 = connect()
    cur2 = conn2.cursor()
    cur2.execute("SELECT COUNT(*) FROM menu")
    after = cur2.fetchone()[0]
    cur2.execute(
        "SELECT name, COUNT(*) c FROM menu GROUP BY name HAVING c > 1"
    )
    dups = cur2.fetchall()
    conn2.close()

    print(f"after: {after} menus, duplicate names: {len(dups)}")


if __name__ == "__main__":
    main()
