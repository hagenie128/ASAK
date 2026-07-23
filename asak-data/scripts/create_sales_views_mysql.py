import pymysql


DB_CONFIG = {
    "host": "nam3324.synology.me",
    "port": 33338,
    "user": "asakasak",
    "password": "dktkrdktkr486",
    "database": "asak_db",
    "charset": "utf8mb4",
    "autocommit": True,
}


VIEWS = {
    "vw_sales_daily": """
CREATE OR REPLACE VIEW vw_sales_daily AS
SELECT
  DATE(COALESCE(p.paid_at, o.created_at)) AS sales_date,
  COUNT(DISTINCT CASE WHEN p.paid_at IS NOT NULL AND os.code <> 'CANCELED' AND ps.code NOT IN ('CANCELED', 'REFUNDED') THEN o.id END) AS order_count,
  COUNT(DISTINCT CASE WHEN p.paid_at IS NOT NULL AND os.code <> 'CANCELED' AND ps.code NOT IN ('CANCELED', 'REFUNDED') THEN o.id END) AS customer_count,
  COUNT(DISTINCT CASE WHEN os.code = 'CANCELED' OR ps.code IN ('CANCELED', 'REFUNDED') THEN o.id END) AS canceled_order_count,
  COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL THEN p.amount ELSE 0 END), 0) AS gross_sales_amount,
  COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL AND (os.code = 'CANCELED' OR ps.code IN ('CANCELED', 'REFUNDED')) THEN p.amount ELSE 0 END), 0) AS canceled_amount,
  COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL THEN p.amount ELSE 0 END), 0)
    - COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL AND (os.code = 'CANCELED' OR ps.code IN ('CANCELED', 'REFUNDED')) THEN p.amount ELSE 0 END), 0) AS net_sales_amount
FROM orders o
LEFT JOIN payment p ON p.order_id = o.id
LEFT JOIN common_code ps ON ps.id = p.status_id
LEFT JOIN common_code os ON os.id = o.status_id
GROUP BY DATE(COALESCE(p.paid_at, o.created_at))
""",
    "vw_sales_hourly": """
CREATE OR REPLACE VIEW vw_sales_hourly AS
SELECT
  DATE(COALESCE(p.paid_at, o.created_at)) AS sales_date,
  HOUR(COALESCE(p.paid_at, o.created_at)) AS sales_hour,
  COUNT(DISTINCT CASE WHEN p.paid_at IS NOT NULL AND os.code <> 'CANCELED' AND ps.code NOT IN ('CANCELED', 'REFUNDED') THEN o.id END) AS order_count,
  COUNT(DISTINCT CASE WHEN p.paid_at IS NOT NULL AND os.code <> 'CANCELED' AND ps.code NOT IN ('CANCELED', 'REFUNDED') THEN o.id END) AS customer_count,
  COUNT(DISTINCT CASE WHEN os.code = 'CANCELED' OR ps.code IN ('CANCELED', 'REFUNDED') THEN o.id END) AS canceled_order_count,
  COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL THEN p.amount ELSE 0 END), 0) AS gross_sales_amount,
  COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL AND (os.code = 'CANCELED' OR ps.code IN ('CANCELED', 'REFUNDED')) THEN p.amount ELSE 0 END), 0) AS canceled_amount,
  COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL THEN p.amount ELSE 0 END), 0)
    - COALESCE(SUM(CASE WHEN p.paid_at IS NOT NULL AND (os.code = 'CANCELED' OR ps.code IN ('CANCELED', 'REFUNDED')) THEN p.amount ELSE 0 END), 0) AS net_sales_amount
FROM orders o
LEFT JOIN payment p ON p.order_id = o.id
LEFT JOIN common_code ps ON ps.id = p.status_id
LEFT JOIN common_code os ON os.id = o.status_id
GROUP BY
  DATE(COALESCE(p.paid_at, o.created_at)),
  HOUR(COALESCE(p.paid_at, o.created_at))
""",
    "vw_top_menu_daily": """
CREATE OR REPLACE VIEW vw_top_menu_daily AS
SELECT
  DATE(COALESCE(p.paid_at, o.created_at)) AS sales_date,
  m.id AS menu_id,
  m.name AS menu_name,
  SUM(oi.quantity) AS quantity,
  COUNT(DISTINCT o.id) AS order_count,
  SUM(oi.price * oi.quantity) AS sales_amount
FROM orders o
JOIN order_item oi ON oi.order_id = o.id
JOIN menu m ON m.id = oi.menu_id
LEFT JOIN payment p ON p.order_id = o.id
LEFT JOIN common_code ps ON ps.id = p.status_id
LEFT JOIN common_code os ON os.id = o.status_id
WHERE p.paid_at IS NOT NULL
  AND os.code <> 'CANCELED'
  AND ps.code NOT IN ('CANCELED', 'REFUNDED')
GROUP BY
  DATE(COALESCE(p.paid_at, o.created_at)),
  m.id,
  m.name
""",
    "vw_top_menu_hourly": """
CREATE OR REPLACE VIEW vw_top_menu_hourly AS
SELECT
  DATE(COALESCE(p.paid_at, o.created_at)) AS sales_date,
  HOUR(COALESCE(p.paid_at, o.created_at)) AS sales_hour,
  m.id AS menu_id,
  m.name AS menu_name,
  SUM(oi.quantity) AS quantity,
  COUNT(DISTINCT o.id) AS order_count,
  SUM(oi.price * oi.quantity) AS sales_amount
FROM orders o
JOIN order_item oi ON oi.order_id = o.id
JOIN menu m ON m.id = oi.menu_id
LEFT JOIN payment p ON p.order_id = o.id
LEFT JOIN common_code ps ON ps.id = p.status_id
LEFT JOIN common_code os ON os.id = o.status_id
WHERE p.paid_at IS NOT NULL
  AND os.code <> 'CANCELED'
  AND ps.code NOT IN ('CANCELED', 'REFUNDED')
GROUP BY
  DATE(COALESCE(p.paid_at, o.created_at)),
  HOUR(COALESCE(p.paid_at, o.created_at)),
  m.id,
  m.name
""",
}


def main():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            for name, sql in VIEWS.items():
                cur.execute(sql)
                print(f"created {name}")

            print("verify")
            for name in VIEWS:
                cur.execute(f"SHOW COLUMNS FROM `{name}`")
                columns = [row[0] for row in cur.fetchall()]
                cur.execute(f"SELECT COUNT(*) FROM `{name}`")
                row_count = cur.fetchone()[0]
                print(f"{name}: columns={columns}, rows={row_count}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
