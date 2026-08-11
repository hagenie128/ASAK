#!/usr/bin/env python3
"""Apply view DDL that depends on ing_nutr split."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pymysql

DDL_PATH = Path(__file__).resolve().parent / "migrations" / "20260811_update_views_ing_nutr.sql"


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


def main() -> int:
    url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    if not url or not user:
        print("DB_URL / DB_USERNAME env required", file=sys.stderr)
        return 1

    sql = DDL_PATH.read_text(encoding="utf-8")
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
            cur.execute(sql)
            print("applied vw_menu_opt_policy_json")
            cur.execute(
                """
                SELECT menu_id, option_group_id,
                       JSON_EXTRACT(items, '$[0].extraKcal') AS extra_kcal,
                       JSON_EXTRACT(items, '$[0].proteinG') AS protein_g
                FROM vw_menu_opt_policy_json
                WHERE JSON_EXTRACT(items, '$[0].extraKcal') IS NOT NULL
                LIMIT 3
                """
            )
            rows = cur.fetchall()
            print(f"sample_rows={len(rows)}")
            for row in rows:
                print(row)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
