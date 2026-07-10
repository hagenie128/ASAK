#!/usr/bin/env python3
"""Reflect current option cleanup and sales views in DevCopilot workspace 2."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any


BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "x-user-username": "hagenie128",
}
if token := os.environ.get("DEVCOPILOT_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {token}"


def col(
    name: str,
    data_type: str,
    description: str,
    *,
    is_pk: bool = False,
    is_fk: bool = False,
    fk_target: str | None = None,
    is_nullable: bool = False,
) -> dict[str, Any]:
    return {
        "name": name,
        "data_type": data_type,
        "is_pk": is_pk,
        "is_fk": is_fk,
        "fk_target": fk_target,
        "is_nullable": is_nullable,
        "description": description,
    }


OBJECTS = [
    {
        "name": "menu_option_group_legacy_20260710",
        "description": "기존 menu_option_group 원본 백업 테이블. 정규 운영 조회에서는 사용하지 않고 복구/검증 용도로만 보관한다.",
        "columns": [
            col("id", "BIGINT", "백업된 연결 ID", is_pk=True),
            col("menu_id", "BIGINT", "백업된 메뉴 ID"),
            col("option_group_id", "BIGINT", "백업된 옵션 그룹 ID"),
            col("sort_order", "INT", "백업된 표시 순서"),
            col("is_required", "BOOLEAN", "백업된 필수 여부"),
        ],
    },
    {
        "name": "menu_option_legacy_20260710",
        "description": "기존 menu_option 원본 백업 테이블. 정규 운영 조회에서는 사용하지 않고 복구/검증 용도로만 보관한다.",
        "columns": [
            col("id", "BIGINT", "백업된 설정 ID", is_pk=True),
            col("menu_id", "BIGINT", "백업된 메뉴 ID"),
            col("option_item_id", "BIGINT", "백업된 옵션 항목 ID"),
            col("is_recommended", "BOOLEAN", "백업된 추천 옵션 여부"),
            col("is_default", "BOOLEAN", "백업된 기본 선택 여부"),
            col("sort_order", "INT", "백업된 표시 순서"),
            col("is_active", "BOOLEAN", "백업된 노출 여부"),
        ],
    },
    {
        "name": "vw_sales_daily",
        "description": "관리자 일별 매출 조회 View. 승인 결제, 주문 취소, 결제 취소/환불을 반영해 일자별 매출을 집계한다.",
        "columns": [
            col("sales_date", "DATE", "매출 일자"),
            col("order_count", "BIGINT", "승인 주문 수"),
            col("customer_count", "BIGINT", "고객 수. MVP 기준 주문 수와 동일"),
            col("canceled_order_count", "BIGINT", "취소/환불 주문 수"),
            col("gross_sales_amount", "INT", "승인 결제 금액"),
            col("canceled_amount", "INT", "취소/환불 금액"),
            col("net_sales_amount", "INT", "순매출. 승인 결제 금액에서 취소/환불 금액을 차감"),
        ],
    },
    {
        "name": "vw_sales_hourly",
        "description": "관리자 시간대별 매출 조회 View. 승인 결제, 주문 취소, 결제 취소/환불을 반영해 일자/시간대별 매출을 집계한다.",
        "columns": [
            col("sales_date", "DATE", "매출 일자"),
            col("sales_hour", "INT", "매출 시간대. 0~23"),
            col("order_count", "BIGINT", "승인 주문 수"),
            col("customer_count", "BIGINT", "고객 수. MVP 기준 주문 수와 동일"),
            col("canceled_order_count", "BIGINT", "취소/환불 주문 수"),
            col("gross_sales_amount", "INT", "승인 결제 금액"),
            col("canceled_amount", "INT", "취소/환불 금액"),
            col("net_sales_amount", "INT", "순매출. 승인 결제 금액에서 취소/환불 금액을 차감"),
        ],
    },
    {
        "name": "vw_top_menu_daily",
        "description": "관리자 일별 인기 메뉴 조회 View. 승인 결제 주문만 대상으로 메뉴별 판매 수량과 매출을 집계한다.",
        "columns": [
            col("sales_date", "DATE", "매출 일자"),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("menu_name", "VARCHAR(100)", "메뉴명"),
            col("quantity", "BIGINT", "판매 수량"),
            col("order_count", "BIGINT", "해당 메뉴가 포함된 주문 수"),
            col("sales_amount", "INT", "메뉴 판매 금액"),
        ],
    },
    {
        "name": "vw_top_menu_hourly",
        "description": "관리자 시간대별 인기 메뉴 조회 View. 승인 결제 주문만 대상으로 시간대/메뉴별 판매 수량과 매출을 집계한다.",
        "columns": [
            col("sales_date", "DATE", "매출 일자"),
            col("sales_hour", "INT", "매출 시간대. 0~23"),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("menu_name", "VARCHAR(100)", "메뉴명"),
            col("quantity", "BIGINT", "판매 수량"),
            col("order_count", "BIGINT", "해당 메뉴가 포함된 주문 수"),
            col("sales_amount", "INT", "메뉴 판매 금액"),
        ],
    },
]


def request_json(method: str, path: str, body: dict[str, Any] | None = None) -> Any:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=HEADERS, method=method)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                text = resp.read().decode("utf-8")
                return json.loads(text) if text else None
        except urllib.error.HTTPError as exc:
            text = exc.read().decode("utf-8", errors="replace")
            if exc.code >= 500 and attempt < 2:
                time.sleep(3 * (attempt + 1))
                continue
            raise RuntimeError(f"{method} {path} failed: {exc.code} {text}") from exc
    raise RuntimeError("unreachable")


def get_tables() -> list[dict[str, Any]]:
    return request_json("GET", f"/api/workspaces/{WS}/tables")


def upsert_object(obj: dict[str, Any], existing_by_name: dict[str, Any]) -> str:
    body = {"name": obj["name"], "description": obj["description"]}
    if obj["name"] in existing_by_name:
        table_id = existing_by_name[obj["name"]]["id"]
        request_json("PUT", f"/api/workspaces/{WS}/tables/{table_id}", body)
        action = "updated"
    else:
        created = request_json("POST", f"/api/workspaces/{WS}/tables", body)
        table_id = created["id"]
        action = "created"

    refreshed = get_tables()
    current = next(row for row in refreshed if row["name"] == obj["name"])
    existing_columns = {column["name"]: column for column in current.get("columns", [])}
    for column in obj["columns"]:
        if column["name"] in existing_columns:
            request_json("PUT", f"/api/workspaces/{WS}/columns/{existing_columns[column['name']]['id']}", column)
        else:
            request_json("POST", f"/api/workspaces/{WS}/tables/{table_id}/columns", column)
    return action


def main() -> None:
    tables = get_tables()
    existing_by_name = {table["name"]: table for table in tables}

    for old_name in ["menu_option", "menu_option_group"]:
        old = existing_by_name.get(old_name)
        if old:
            request_json("DELETE", f"/api/workspaces/{WS}/tables/{old['id']}")
            print(f"deleted {old_name}")

    existing_by_name = {table["name"]: table for table in get_tables()}
    for obj in OBJECTS:
        action = upsert_object(obj, existing_by_name)
        print(f"{action} {obj['name']}")
        existing_by_name = {table["name"]: table for table in get_tables()}

    final = get_tables()
    watched = [
        table["name"]
        for table in final
        if "menu_option" in table["name"] or table["name"].startswith("vw_sales") or table["name"].startswith("vw_top")
    ]
    print("watched:", ", ".join(sorted(watched)))


if __name__ == "__main__":
    main()
