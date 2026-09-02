#!/usr/bin/env python3
import pymysql
from pathlib import Path

sql = Path(r"c:/ASAK-workspace/ASAK-back/docs/migrations/2026-09-02_vw_soldout_catalog_ingredient_scope.sql")
conn = pymysql.connect(
    host="nam3324.synology.me",
    port=33338,
    user="asakasak",
    password="dktkrdktkr486",
    database="asak_db",
    connect_timeout=20,
    charset="utf8mb4",
)
cur = conn.cursor()
cur.execute(sql.read_text(encoding="utf-8"))
conn.commit()
cur.execute("SELECT target_type, COUNT(*) FROM vw_soldout_catalog GROUP BY target_type")
print("catalog counts", cur.fetchall())
cur.execute(
    "SELECT category, COUNT(*) FROM vw_soldout_catalog WHERE target_type='INGREDIENT' GROUP BY category ORDER BY category"
)
print("ing by category", cur.fetchall())
conn.close()
