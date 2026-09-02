#!/usr/bin/env python3
"""Fill empty sales dates with realistic kiosk-scale dummy orders (Admin makeDummyDay parity)."""
from __future__ import annotations

import argparse
import os
import random
import secrets
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Iterable

import pymysql

KST = timedelta(hours=9)
HOUR_WEIGHTS_FULL = [4, 8, 18, 16, 10, 6, 5, 8, 12, 8, 4, 1]  # 10:00-21:00
HOUR_START = 10

ORDER_STATUS_COMPLETED = 13
PAYMENT_STATUS_APPROVED = 15
ORDER_TYPE_EAT_IN = 17
ORDER_TYPE_TAKE_OUT = 18
PAYMENT_METHODS = [(19, 0.70), (46, 0.15), (47, 0.10), (49, 0.05)]


def hash_seed(value: str) -> int:
    h = 2166136261
    for ch in str(value):
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


def make_dummy_day(ymd: str) -> tuple[int, int, int]:
    y, m, d = map(int, ymd.split("-"))
    weekend = date(y, m, d).weekday() >= 5
    seed = hash_seed(f"asak-day-{ymd}")
    order_count = max(8, (26 if weekend else 16) + (seed % 9) - 4)
    avg_amount = 15000 + (seed % 8) * 500
    total_amount = order_count * avg_amount
    return order_count, total_amount, avg_amount


def each_ymd(from_ymd: str, to_ymd: str) -> list[str]:
    start = date.fromisoformat(from_ymd)
    end = date.fromisoformat(to_ymd)
    out: list[str] = []
    cur = start
    while cur <= end:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


def hour_weights_until(max_hour: int) -> list[tuple[int, int]]:
    weights: list[tuple[int, int]] = []
    for idx, w in enumerate(HOUR_WEIGHTS_FULL):
        hour = HOUR_START + idx
        if hour > max_hour:
            break
        weights.append((hour, w))
    return weights


def assign_hours(order_count: int, ymd: str, max_hour: int = 21) -> list[int]:
    pairs = hour_weights_until(max_hour)
    total_w = sum(w for _, w in pairs)
    rng = random.Random(hash_seed(f"asak-hours-{ymd}"))
    counts: dict[int, int] = {h: 0 for h, _ in pairs}
    for i in range(order_count):
        hour = rng.choices([h for h, _ in pairs], weights=[w for _, w in pairs], k=1)[0]
        counts[hour] += 1
    hours: list[int] = []
    for hour, _ in pairs:
        hours.extend([hour] * counts[hour])
    rng.shuffle(hours)
    while len(hours) < order_count:
        hours.append(rng.choice([h for h, _ in pairs]))
    return hours[:order_count]


@dataclass
class Menu:
    id: int
    price: int


def connect() -> pymysql.connections.Connection:
    url = os.getenv("DB_URL", "")
    if url.startswith("jdbc:mysql://"):
        host_port_db = url.removeprefix("jdbc:mysql://")
        host_port, _, database = host_port_db.partition("/")
        host, _, port = host_port.partition(":")
        return pymysql.connect(
            host=host,
            port=int(port or 3306),
            user=os.getenv("DB_USERNAME", "asakasak"),
            password=os.getenv("DB_PASSWORD", ""),
            database=database.split("?")[0],
            charset="utf8mb4",
            autocommit=False,
            connect_timeout=20,
        )
    return pymysql.connect(
        host=os.getenv("DB_HOST", "nam3324.synology.me"),
        port=int(os.getenv("DB_PORT", "33338")),
        user=os.getenv("DB_USERNAME", "asakasak"),
        password=os.getenv("DB_PASSWORD", "dktkrdktkr486"),
        database=os.getenv("DB_NAME", "asak_db"),
        charset="utf8mb4",
        autocommit=False,
        connect_timeout=20,
    )


def load_menus(cur) -> list[Menu]:
    cur.execute(
        """
        SELECT id, price
        FROM menu
        WHERE deleted_at IS NULL AND price BETWEEN 5000 AND 14000
        ORDER BY id
        """
    )
    return [Menu(int(r[0]), int(r[1])) for r in cur.fetchall()]


def dates_with_sales(cur, from_ymd: str, to_ymd: str) -> set[str]:
    cur.execute(
        """
        SELECT DISTINCT DATE(COALESCE(p.paid_at, o.created_at)) AS d
        FROM orders o
        JOIN payment p ON p.order_id = o.id
        JOIN common_code ps ON ps.id = p.status_id AND ps.code = 'APPROVED'
        WHERE DATE(COALESCE(p.paid_at, o.created_at)) BETWEEN %s AND %s
        """,
        (from_ymd, to_ymd),
    )
    return {r[0].isoformat() for r in cur.fetchall()}


def count_orders_on_date(cur, ymd: str) -> int:
    cur.execute(
        """
        SELECT COUNT(DISTINCT o.id)
        FROM orders o
        JOIN payment p ON p.order_id = o.id
        JOIN common_code ps ON ps.id = p.status_id AND ps.code = 'APPROVED'
        WHERE DATE(COALESCE(p.paid_at, o.created_at)) = %s
        """,
        (ymd,),
    )
    return int(cur.fetchone()[0])


def next_order_seq(cur, ymd: str) -> int:
    y, m, d = map(int, ymd.split("-"))
    prefix = f"ASAK{y % 100:02d}{m:02d}{d:02d}"
    cur.execute(
        "SELECT order_no FROM orders WHERE order_no LIKE %s ORDER BY order_no DESC LIMIT 1",
        (prefix + "%",),
    )
    row = cur.fetchone()
    if not row:
        return 1
    last = row[0]
    try:
        return int(last[-4:]) + 1
    except ValueError:
        return 1


def pick_payment_method(rng: random.Random) -> int:
    roll = rng.random()
    acc = 0.0
    for method_id, weight in PAYMENT_METHODS:
        acc += weight
        if roll <= acc:
            return method_id
    return PAYMENT_METHODS[0][0]


def build_order_lines(
    rng: random.Random, menus: list[Menu], target_amount: int
) -> list[tuple[int, int, int]]:
    if not menus:
        raise RuntimeError("no menus available")
    menu = rng.choice(menus)
    qty = max(1, min(3, round(target_amount / menu.price)))
    total = menu.price * qty
    return [(menu.id, qty, total)]


def insert_order_bundle(
    cur,
    *,
    ymd: str,
    seq: int,
    hour: int,
    menus: list[Menu],
    target_amount: int,
    rng: random.Random,
) -> None:
    y, m, d = map(int, ymd.split("-"))
    prefix = f"ASAK{y % 100:02d}{m:02d}{d:02d}"
    order_no = f"{prefix}{seq:04d}"
    minute = rng.randint(3, 57)
    second = rng.randint(0, 59)
    created_at = datetime(y, m, d, hour, minute, second)
    paid_at = created_at + timedelta(minutes=rng.randint(1, 4), seconds=rng.randint(0, 59))

    lines = build_order_lines(rng, menus, target_amount)
    total_price = sum(price for _, _, price in lines)
    order_type_id = ORDER_TYPE_EAT_IN if rng.random() < 0.55 else ORDER_TYPE_TAKE_OUT
    method_id = pick_payment_method(rng)
    idempotency_key = f"backfill-{ymd}-{seq:04d}"

    cur.execute(
        """
        INSERT INTO orders (order_no, order_type_id, status_id, total_price, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (order_no, order_type_id, ORDER_STATUS_COMPLETED, total_price, created_at),
    )
    order_id = cur.lastrowid
    for menu_id, qty, price in lines:
        cur.execute(
            """
            INSERT INTO order_item (order_id, menu_id, quantity, price)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, menu_id, qty, price),
        )
    cur.execute(
        """
        INSERT INTO payment (order_id, method_id, status_id, amount, paid_at, idempotency_key)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (order_id, method_id, PAYMENT_STATUS_APPROVED, total_price, paid_at, idempotency_key),
    )


def fill_date(
    cur,
    ymd: str,
    menus: list[Menu],
    *,
    max_hour: int,
    dry_run: bool,
    mode: str,
) -> int:
    target_count, _, avg_amount = make_dummy_day(ymd)
    existing = count_orders_on_date(cur, ymd)

    if mode == "empty_only" and existing > 0:
        print(f"SKIP {ymd}: not empty ({existing} orders)")
        return 0
    if mode == "top_up":
        need = max(0, target_count - existing)
    else:
        need = target_count if existing == 0 else 0

    if need == 0:
        print(f"SKIP {ymd}: already {existing}/{target_count}")
        return 0

    seq = next_order_seq(cur, ymd)
    hours = assign_hours(need, ymd, max_hour=max_hour)
    rng = random.Random(hash_seed(f"asak-orders-{ymd}-{existing}"))
    print(
        f"FILL {ymd}: +{need} orders (existing {existing} -> {existing + need}, "
        f"avg~{avg_amount}, hours<={max_hour}:00)"
    )
    if dry_run:
        return need

    for i in range(need):
        amount = avg_amount + rng.randint(-1500, 1500)
        amount = max(5000, amount)
        insert_order_bundle(
            cur,
            ymd=ymd,
            seq=seq + i,
            hour=hours[i],
            menus=menus,
            target_amount=amount,
            rng=rng,
        )
    return need


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="from_ymd", default="2026-07-20")
    parser.add_argument("--to", dest="to_ymd", default=date.today().isoformat())
    parser.add_argument("--today-max-hour", type=int, default=18)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    conn = connect()
    try:
        cur = conn.cursor()
        menus = load_menus(cur)
        if not menus:
            print("No menus found", file=sys.stderr)
            sys.exit(1)

        targets = each_ymd(args.from_ymd, args.to_ymd)
        total_inserted = 0

        for ymd in targets:
            if ymd > args.to_ymd:
                continue
            if ymd == args.to_ymd:
                mode = "top_up"
                max_hour = args.today_max_hour
            else:
                mode = "empty_only"
                max_hour = 21
            inserted = fill_date(
                cur, ymd, menus, max_hour=max_hour, dry_run=args.dry_run, mode=mode
            )
            total_inserted += inserted

        if args.dry_run:
            conn.rollback()
            print(f"DRY RUN complete. would insert ~{total_inserted} orders")
        else:
            conn.commit()
            print(f"DONE inserted {total_inserted} orders")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
