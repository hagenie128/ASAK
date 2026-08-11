#!/usr/bin/env python3
"""Generate diverse multi-item recent orders (+ payments) into live ASAK MySQL."""

from __future__ import annotations

import os
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pymysql

# ORDER_STATUS
ST_RECEIVED, ST_PREPARING, ST_COMPLETED, ST_CANCELED = 11, 12, 13, 43
# ORDER_TYPE
TYPE_EAT_IN, TYPE_TAKE_OUT = 17, 18
# PAYMENT
PAY_CARD, PAY_KAKAO, PAY_NAVER = 19, 46, 47
PAY_READY, PAY_APPROVED, PAY_FAILED, PAY_CANCELED, PAY_REFUNDED = 14, 15, 16, 44, 45

SKIP_NAME_SUBSTR = (
    "bruno",
    "sample",
    "write tables",
    "recommended override",
    "123",
)


def connect() -> pymysql.Connection:
    url = os.environ.get("DB_URL", "")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD", "")
    if not url or not user:
        raise SystemExit("DB_URL / DB_USERNAME required")
    raw = url.replace("jdbc:mysql://", "")
    host_port, _, rest = raw.partition("/")
    db = rest.split("?", 1)[0]
    if ":" in host_port:
        host, port_s = host_port.split(":", 1)
        port = int(port_s)
    else:
        host, port = host_port, 3306
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db,
        charset="utf8mb4",
        autocommit=False,
    )


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def fetch_menus(cur) -> list[dict]:
    cur.execute(
        """
        SELECT id, name, price, cat_id
        FROM menu
        WHERE sold_out = 0 AND price > 0
        ORDER BY id
        """
    )
    rows = []
    for mid, name, price, cat_id in cur.fetchall():
        low = (name or "").lower()
        if any(s in low for s in SKIP_NAME_SUBSTR):
            continue
        rows.append({"id": mid, "name": name, "price": int(price), "cat_id": cat_id})
    return rows


def fetch_options_by_menu(cur, menu_ids: list[int]) -> dict[int, list[tuple[int, int]]]:
    if not menu_ids:
        return {}
    placeholders = ",".join(["%s"] * len(menu_ids))
    cur.execute(
        f"""
        SELECT mop.menu_id, oi.id, COALESCE(oi.add_price, 0)
        FROM menu_opt_policy mop
        JOIN opt_policy_item opi ON opi.policy_id = mop.policy_id AND opi.active = 1
        JOIN opt_item oi ON oi.id = opi.opt_item_id AND oi.sold_out = 0
        WHERE mop.menu_id IN ({placeholders})
        """,
        menu_ids,
    )
    by_menu: dict[int, list[tuple[int, int]]] = {}
    for menu_id, opt_id, add_price in cur.fetchall():
        by_menu.setdefault(menu_id, []).append((opt_id, int(add_price or 0)))
    return by_menu


def next_order_seq(cur, day: datetime) -> int:
    prefix = f"ASAK{day.strftime('%y%m%d')}"
    cur.execute(
        "SELECT order_no FROM orders WHERE order_no LIKE %s ORDER BY order_no DESC LIMIT 1",
        (prefix + "%",),
    )
    row = cur.fetchone()
    if not row:
        return 1
    try:
        return int(row[0][-4:]) + 1
    except ValueError:
        return 1


def pick_status_and_payment(rng: random.Random):
    roll = rng.random()
    if roll < 0.08:
        return ST_CANCELED, PAY_CANCELED, False
    if roll < 0.18:
        return ST_RECEIVED, PAY_APPROVED, True
    if roll < 0.35:
        return ST_PREPARING, PAY_APPROVED, True
    return ST_COMPLETED, PAY_APPROVED, True


def build_cart(rng: random.Random, menus: list[dict], opts_by_menu: dict) -> list[dict]:
    """2~5 distinct menus, some qty>1, some with options."""
    n_items = rng.choices([2, 3, 4, 5], weights=[35, 35, 20, 10], k=1)[0]
    # prefer mixing categories when possible
    by_cat: dict[int, list[dict]] = {}
    for m in menus:
        by_cat.setdefault(m["cat_id"], []).append(m)

    picked: list[dict] = []
    cats = list(by_cat.keys())
    rng.shuffle(cats)
    used_ids: set[int] = set()

    for cat in cats:
        if len(picked) >= n_items:
            break
        candidates = [m for m in by_cat[cat] if m["id"] not in used_ids]
        if not candidates:
            continue
        m = rng.choice(candidates)
        used_ids.add(m["id"])
        picked.append(m)

    while len(picked) < n_items:
        m = rng.choice(menus)
        if m["id"] in used_ids:
            continue
        used_ids.add(m["id"])
        picked.append(m)

    cart = []
    for m in picked:
        qty = rng.choices([1, 2, 3], weights=[75, 20, 5], k=1)[0]
        unit = m["price"]
        options = []
        available = opts_by_menu.get(m["id"], [])
        if available and rng.random() < 0.65:
            k = min(len(available), rng.randint(1, 3))
            for opt_id, add_price in rng.sample(available, k):
                options.append({"opt_item_id": opt_id, "quantity": 1, "price": add_price})
                unit += add_price
        cart.append(
            {
                "menu_id": m["id"],
                "quantity": qty,
                "price": unit,  # unit line price (menu+opts), same as existing sample
                "options": options,
            }
        )
    return cart


def august_2026_day_plan(now: datetime) -> list[tuple]:
    """2026-08 only: fill each day up to today with multi-item orders."""
    plan = []
    for day_num in range(1, 32):
        try:
            day = datetime(2026, 8, day_num).date()
        except ValueError:
            break
        if day > now.date():
            break
        # weekday busier; weekend lighter; today denser for live board
        weekday = day.weekday()  # Mon=0
        if day == now.date():
            target = 28
        elif weekday >= 5:
            target = 14
        else:
            target = 20
        plan.append((day, target))
    return plan


def main() -> int:
    load_env_file(Path(r"c:\ASAK-workspace\ASAK-back\.env"))
    rng = random.Random(20260811)
    now = datetime(2026, 8, 11, 15, 10, 0)

    # 2026년 8월만 생성 (오늘까지)
    day_plan = august_2026_day_plan(now)

    conn = connect()
    try:
        with conn.cursor() as cur:
            menus = fetch_menus(cur)
            if len(menus) < 5:
                raise SystemExit(f"not enough menus: {len(menus)}")
            opts_by_menu = fetch_options_by_menu(cur, [m["id"] for m in menus])

            created = 0
            multi_item = 0
            pay_count = 0

            for day, target in day_plan:
                cur.execute(
                    """
                    SELECT COUNT(*) FROM orders
                    WHERE created_at >= %s AND created_at < %s
                    """,
                    (
                        datetime.combine(day, datetime.min.time()),
                        datetime.combine(day, datetime.min.time()) + timedelta(days=1),
                    ),
                )
                existing = cur.fetchone()[0]
                count = max(0, target - existing)
                if count == 0:
                    print(f"skip {day} already={existing} target={target}")
                    continue

                seq = next_order_seq(cur, datetime.combine(day, datetime.min.time()))
                for _ in range(count):
                    cart = build_cart(rng, menus, opts_by_menu)
                    if len(cart) >= 2:
                        multi_item += 1
                    total = sum(line["price"] * line["quantity"] for line in cart)
                    order_type = rng.choice([TYPE_EAT_IN, TYPE_TAKE_OUT])
                    status_id, pay_status, has_payment = pick_status_and_payment(rng)

                    hour = rng.randint(10, 20)
                    minute = rng.randint(0, 59)
                    second = rng.randint(0, 59)
                    created_at = datetime(day.year, day.month, day.day, hour, minute, second)
                    if day == now.date() and created_at > now:
                        created_at = now - timedelta(minutes=rng.randint(1, 120))

                    order_no = f"ASAK{day.strftime('%y%m%d')}{seq:04d}"
                    seq += 1

                    canceled_at = created_at + timedelta(minutes=rng.randint(2, 20)) if status_id == ST_CANCELED else None

                    cur.execute(
                        """
                        INSERT INTO orders
                          (order_no, order_type_id, status_id, total_price, created_at, canceled_at)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        """,
                        (order_no, order_type, status_id, total, created_at, canceled_at),
                    )
                    order_id = cur.lastrowid

                    for line in cart:
                        cur.execute(
                            """
                            INSERT INTO order_item (order_id, menu_id, quantity, price)
                            VALUES (%s,%s,%s,%s)
                            """,
                            (order_id, line["menu_id"], line["quantity"], line["price"]),
                        )
                        order_item_id = cur.lastrowid
                        for opt in line["options"]:
                            cur.execute(
                                """
                                INSERT INTO order_item_option
                                  (order_item_id, opt_item_id, quantity, price)
                                VALUES (%s,%s,%s,%s)
                                """,
                                (
                                    order_item_id,
                                    opt["opt_item_id"],
                                    opt["quantity"],
                                    opt["price"],
                                ),
                            )

                    if has_payment:
                        method = rng.choices(
                            [PAY_CARD, PAY_KAKAO, PAY_NAVER],
                            weights=[70, 18, 12],
                            k=1,
                        )[0]
                        paid_at = created_at + timedelta(seconds=rng.randint(20, 180))
                        refunded_at = None
                        if status_id == ST_CANCELED and pay_status == PAY_APPROVED:
                            pay_status = PAY_REFUNDED
                            refunded_at = canceled_at
                        cur.execute(
                            """
                            INSERT INTO payment
                              (order_id, method_id, status_id, amount, paid_at, refunded_at, idempotency_key)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """,
                            (
                                order_id,
                                method,
                                pay_status,
                                total,
                                paid_at,
                                refunded_at,
                                f"demo-{order_id}-{uuid.uuid4().hex[:12]}",
                            ),
                        )
                        pay_count += 1

                    created += 1

                print(f"day {day} added={count} existing_was={existing} target={target}")
            conn.commit()
            print(
                f"created_orders={created} multi_item_orders={multi_item} payments={pay_count}"
            )

            cur.execute(
                """
                SELECT DATE(created_at) d, COUNT(*) c,
                       ROUND(AVG(item_cnt),2) avg_items
                FROM (
                  SELECT o.id, o.created_at, COUNT(oi.id) item_cnt
                  FROM orders o
                  JOIN order_item oi ON oi.order_id = o.id
                  WHERE o.created_at >= %s
                  GROUP BY o.id, o.created_at
                ) t
                GROUP BY DATE(created_at)
                ORDER BY d
                """,
                (now.date() - timedelta(days=3),),
            )
            print("by_day", cur.fetchall())
            cur.execute(
                """
                SELECT o.order_no, o.total_price, COUNT(oi.id) items, SUM(oi.quantity) qty, o.created_at
                FROM orders o
                JOIN order_item oi ON oi.order_id=o.id
                WHERE o.created_at >= %s
                GROUP BY o.id
                HAVING COUNT(oi.id) >= 2
                ORDER BY o.created_at DESC
                LIMIT 8
                """,
                (now.date() - timedelta(days=1),),
            )
            print("sample_multi", cur.fetchall())
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
