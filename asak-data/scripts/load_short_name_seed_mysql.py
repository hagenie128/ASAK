#!/usr/bin/env python3
"""Load seed-v3 JSON into an already-migrated short-name ASAK MySQL schema."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pymysql

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SEED = ROOT / "asak-data" / "seed-v3"
ORDER = ["category", "code_group", "common_code", "tag", "menu", "menu_nutr", "ing", "allergen", "ing_allergen", "menu_ing", "opt_group", "opt_item", "opt_item_comp", "menu_opt_grp_legacy_20260710", "menu_opt_legacy_20260710", "menu_tag", "pay_method_cfg", "opt_policy", "opt_policy_item", "menu_opt_policy", "menu_opt_override"]

def parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--host", required=True); p.add_argument("--port", type=int, default=3306)
    p.add_argument("--user", required=True); p.add_argument("--password", required=True); p.add_argument("--database", required=True)
    p.add_argument("--seed-dir", type=Path, default=DEFAULT_SEED); p.add_argument("--replace", action="store_true")
    return p.parse_args()

def q(name: str) -> str: return "`" + name + "`"

def main() -> None:
    a = parse(); seed = a.seed_dir.resolve()
    conn = pymysql.connect(host=a.host, port=a.port, user=a.user, password=a.password, database=a.database, charset="utf8mb4", autocommit=False)
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES LIKE 'opt_item'")
            if not cur.fetchone(): raise RuntimeError("Short-name schema not found. Run migrate_short_names_mysql.py first.")
            if a.replace:
                cur.execute("SET FOREIGN_KEY_CHECKS=0")
                for table in reversed(ORDER): cur.execute(f"DELETE FROM {q(table)}")
                cur.execute("SET FOREIGN_KEY_CHECKS=1")
            for table in ORDER:
                path = seed / f"{table}.json"
                rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
                if not rows: continue
                cols = list(rows[0]); sql = f"INSERT INTO {q(table)} ({', '.join(q(c) for c in cols)}) VALUES ({', '.join(['%s']*len(cols))}) ON DUPLICATE KEY UPDATE " + ", ".join(f"{q(c)}=VALUES({q(c)})" for c in cols if c != "id")
                cur.executemany(sql, [tuple(row.get(c) for c in cols) for row in rows])
            conn.commit()
    except Exception:
        conn.rollback(); raise
    finally: conn.close()
    print("Short-name seed load complete")

if __name__ == "__main__": main()
