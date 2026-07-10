#!/usr/bin/env python3
"""Sync the current ASAK DB schema to DevCopilot workspace 2.

This updates descriptions for the existing 22 tables and creates the 4 option
policy tables added after menu_option deduplication.
"""

from __future__ import annotations

import json
import os
import sys
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


TABLES: list[dict[str, Any]] = [
    {
        "name": "category",
        "description": "메뉴 카테고리 마스터. 메뉴 목록의 상위 분류와 노출 순서를 관리한다.",
        "columns": [
            col("id", "BIGINT", "카테고리 ID", is_pk=True),
            col("name", "VARCHAR(50)", "카테고리명. 신메뉴, 샐러디·볼, 랩, 샌드위치 등"),
            col("sort_order", "INT", "노출 순서. 작을수록 먼저 표시"),
            col("is_active", "BOOLEAN", "카테고리 사용 여부"),
        ],
    },
    {
        "name": "code_group",
        "description": "공통 코드 그룹. 주문 상태, 결제 상태, 옵션 유형처럼 확장 가능한 코드 묶음.",
        "columns": [
            col("id", "BIGINT", "코드 그룹 ID", is_pk=True),
            col("group_code", "VARCHAR(50)", "코드 그룹 코드. 예: ORDER_STATUS, PAYMENT_METHOD"),
            col("name", "VARCHAR(50)", "코드 그룹 표시명"),
        ],
    },
    {
        "name": "common_code",
        "description": "공통 코드 상세. 상태, 유형, 단위, 결제수단 등의 실제 코드값.",
        "columns": [
            col("id", "BIGINT", "코드 ID", is_pk=True),
            col("code_group_id", "BIGINT", "소속 코드 그룹 ID", is_fk=True, fk_target="code_group.id"),
            col("code", "VARCHAR(50)", "API와 화면에서 사용하는 코드값"),
            col("name", "VARCHAR(50)", "코드 표시명"),
            col("sort_order", "INT", "정렬 순서"),
            col("is_active", "BOOLEAN", "코드 사용 여부"),
        ],
    },
    {
        "name": "tag",
        "description": "메뉴 태그 마스터. BEST, NEW, LOW_SUGAR 같은 메뉴 배지.",
        "columns": [
            col("id", "BIGINT", "태그 ID", is_pk=True),
            col("code", "VARCHAR(50)", "태그 코드"),
            col("name", "VARCHAR(50)", "태그 표시명"),
            col("color_hex", "VARCHAR(20)", "태그 색상 HEX", is_nullable=True),
            col("is_active", "BOOLEAN", "태그 사용 여부"),
        ],
    },
    {
        "name": "menu",
        "description": "판매 메뉴 마스터. 카테고리, 가격, 이미지, 설명, 품절 상태를 가진다.",
        "columns": [
            col("id", "BIGINT", "메뉴 ID", is_pk=True),
            col("category_id", "BIGINT", "메뉴 카테고리 ID", is_fk=True, fk_target="category.id"),
            col("name", "VARCHAR(100)", "메뉴명"),
            col("price", "INT", "기본 판매가. 단위 KRW"),
            col("image_url", "TEXT", "메뉴 이미지 URL", is_nullable=True),
            col("description", "TEXT", "메뉴 설명", is_nullable=True),
            col("is_sold_out", "BOOLEAN", "메뉴 품절 여부"),
            col("created_at", "TIMESTAMP", "생성일시"),
            col("updated_at", "TIMESTAMP", "수정일시"),
        ],
    },
    {
        "name": "menu_tag",
        "description": "메뉴와 태그의 N:M 연결 테이블.",
        "columns": [
            col("id", "BIGINT", "연결 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("tag_id", "BIGINT", "태그 ID", is_fk=True, fk_target="tag.id"),
        ],
    },
    {
        "name": "menu_nutrition",
        "description": "메뉴별 영양 정보 요약. 칼로리와 주요 영양성분을 저장한다.",
        "columns": [
            col("id", "BIGINT", "영양 정보 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("kcal", "DECIMAL(8,2)", "칼로리", is_nullable=True),
            col("protein_g", "DECIMAL(8,2)", "단백질 g", is_nullable=True),
            col("carb_g", "DECIMAL(8,2)", "탄수화물 g", is_nullable=True),
            col("fat_g", "DECIMAL(8,2)", "지방 g", is_nullable=True),
            col("sodium_mg", "DECIMAL(8,2)", "나트륨 mg", is_nullable=True),
            col("source_id", "BIGINT", "데이터 출처 코드 ID", is_fk=True, fk_target="common_code.id", is_nullable=True),
        ],
    },
    {
        "name": "ingredient",
        "description": "재료 마스터. 채소, 단백질, 드레싱, 베이스, 사이드, 음료 재료를 관리한다.",
        "columns": [
            col("id", "BIGINT", "재료 ID", is_pk=True),
            col("name", "VARCHAR(100)", "재료명"),
            col("type_id", "BIGINT", "재료 유형 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("kcal", "DECIMAL(8,2)", "기준 칼로리", is_nullable=True),
            col("protein_g", "DECIMAL(8,2)", "기준 단백질 g", is_nullable=True),
            col("is_sold_out", "BOOLEAN", "재료 품절 여부"),
        ],
    },
    {
        "name": "allergen",
        "description": "알레르기 마스터.",
        "columns": [
            col("id", "BIGINT", "알레르기 ID", is_pk=True),
            col("name", "VARCHAR(50)", "알레르기명"),
        ],
    },
    {
        "name": "ingredient_allergen",
        "description": "재료와 알레르기의 N:M 연결 테이블.",
        "columns": [
            col("id", "BIGINT", "연결 ID", is_pk=True),
            col("ingredient_id", "BIGINT", "재료 ID", is_fk=True, fk_target="ingredient.id"),
            col("allergen_id", "BIGINT", "알레르기 ID", is_fk=True, fk_target="allergen.id"),
        ],
    },
    {
        "name": "menu_ingredient",
        "description": "메뉴 기본 재료 연결. 기본 포함, 제외 가능 여부, 역할과 표시 순서를 관리한다.",
        "columns": [
            col("id", "BIGINT", "연결 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("ingredient_id", "BIGINT", "재료 ID", is_fk=True, fk_target="ingredient.id"),
            col("role_id", "BIGINT", "재료 역할 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("quantity", "DECIMAL(8,2)", "기본 제공량", is_nullable=True),
            col("unit_id", "BIGINT", "단위 코드 ID", is_fk=True, fk_target="common_code.id", is_nullable=True),
            col("is_default", "BOOLEAN", "기본 포함 여부"),
            col("can_remove", "BOOLEAN", "고객 제외 가능 여부"),
            col("sort_order", "INT", "표시 순서"),
        ],
    },
    {
        "name": "option_group",
        "description": "옵션 그룹 마스터. 드레싱 선택, 토핑 추가, 베이스 선택 등.",
        "columns": [
            col("id", "BIGINT", "옵션 그룹 ID", is_pk=True),
            col("name", "VARCHAR(100)", "옵션 그룹명"),
            col("group_type_id", "BIGINT", "옵션 그룹 유형 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("min_select", "INT", "최소 선택 수"),
            col("max_select", "INT", "최대 선택 수"),
        ],
    },
    {
        "name": "menu_option_group",
        "description": "기존 호환용 메뉴-옵션그룹 연결. 신규 구현은 menu_option_policy를 우선 사용한다.",
        "columns": [
            col("id", "BIGINT", "연결 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("option_group_id", "BIGINT", "옵션 그룹 ID", is_fk=True, fk_target="option_group.id"),
            col("sort_order", "INT", "표시 순서"),
            col("is_required", "BOOLEAN", "필수 여부"),
        ],
    },
    {
        "name": "menu_option",
        "description": "기존 호환용 메뉴별 옵션 항목 설정. 신규 구현은 option_policy 계열을 우선 사용한다.",
        "columns": [
            col("id", "BIGINT", "설정 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("option_item_id", "BIGINT", "옵션 항목 ID", is_fk=True, fk_target="option_item.id"),
            col("is_recommended", "BOOLEAN", "추천 옵션 여부"),
            col("is_default", "BOOLEAN", "기본 선택 여부"),
            col("sort_order", "INT", "표시 순서"),
            col("is_active", "BOOLEAN", "노출 여부"),
        ],
    },
    {
        "name": "option_item",
        "description": "옵션 선택 항목 마스터. 가격, 수량, 재료 연결, 품절 상태를 가진다.",
        "columns": [
            col("id", "BIGINT", "옵션 항목 ID", is_pk=True),
            col("option_group_id", "BIGINT", "옵션 그룹 ID", is_fk=True, fk_target="option_group.id"),
            col("ingredient_id", "BIGINT", "재료 기반 옵션일 때 재료 ID", is_fk=True, fk_target="ingredient.id", is_nullable=True),
            col("name", "VARCHAR(100)", "옵션 항목명"),
            col("extra_price", "INT", "추가 금액. 단위 KRW"),
            col("original_price", "INT", "할인 전 금액", is_nullable=True),
            col("amount", "DECIMAL(8,2)", "제공량", is_nullable=True),
            col("unit_id", "BIGINT", "단위 코드 ID", is_fk=True, fk_target="common_code.id", is_nullable=True),
            col("icon_url", "TEXT", "아이콘 URL", is_nullable=True),
            col("color_hex", "VARCHAR(20)", "표시 색상 HEX", is_nullable=True),
            col("is_sold_out", "BOOLEAN", "옵션 항목 품절 여부"),
            col("created_at", "TIMESTAMP", "생성일시"),
            col("updated_at", "TIMESTAMP", "수정일시"),
        ],
    },
    {
        "name": "option_item_component",
        "description": "세트/복합 옵션 구성 테이블.",
        "columns": [
            col("id", "BIGINT", "구성 ID", is_pk=True),
            col("option_item_id", "BIGINT", "상위 옵션 항목 ID", is_fk=True, fk_target="option_item.id"),
            col("ingredient_id", "BIGINT", "구성 재료 ID", is_fk=True, fk_target="ingredient.id", is_nullable=True),
            col("name", "VARCHAR(100)", "구성명"),
            col("quantity", "DECIMAL(8,2)", "구성 수량", is_nullable=True),
            col("unit_id", "BIGINT", "단위 코드 ID", is_fk=True, fk_target="common_code.id", is_nullable=True),
            col("sort_order", "INT", "표시 순서"),
        ],
    },
    {
        "name": "payment_method_config",
        "description": "결제 수단 노출 설정.",
        "columns": [
            col("id", "BIGINT", "설정 ID", is_pk=True),
            col("method_id", "BIGINT", "결제수단 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("name", "VARCHAR(50)", "표시명"),
            col("is_active", "BOOLEAN", "노출 여부"),
            col("sort_order", "INT", "노출 순서"),
        ],
    },
    {
        "name": "orders",
        "description": "주문 헤더. 주문 번호, 주문 유형, 상태, 총액을 가진다.",
        "columns": [
            col("id", "BIGINT", "주문 ID", is_pk=True),
            col("order_no", "VARCHAR(50)", "주문 번호"),
            col("order_type_id", "BIGINT", "주문 유형 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("status_id", "BIGINT", "주문 상태 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("total_price", "INT", "주문 총액. 단위 KRW"),
            col("created_at", "TIMESTAMP", "주문 생성일시"),
        ],
    },
    {
        "name": "order_item",
        "description": "주문 메뉴 단위. 주문 시점의 메뉴, 수량, 단가를 저장한다.",
        "columns": [
            col("id", "BIGINT", "주문 상세 ID", is_pk=True),
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id"),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("quantity", "INT", "메뉴 수량"),
            col("price", "INT", "주문 시점 메뉴 단가. 단위 KRW"),
        ],
    },
    {
        "name": "order_item_option",
        "description": "주문 메뉴별 선택 옵션. 주문 시점의 옵션, 수량, 단가를 저장한다.",
        "columns": [
            col("id", "BIGINT", "주문 옵션 ID", is_pk=True),
            col("order_item_id", "BIGINT", "주문 상세 ID", is_fk=True, fk_target="order_item.id"),
            col("option_item_id", "BIGINT", "옵션 항목 ID", is_fk=True, fk_target="option_item.id"),
            col("quantity", "INT", "옵션 수량"),
            col("price", "INT", "주문 시점 옵션 단가. 단위 KRW"),
        ],
    },
    {
        "name": "item_exclusion",
        "description": "주문 메뉴에서 제외한 기본 재료.",
        "columns": [
            col("id", "BIGINT", "제외 ID", is_pk=True),
            col("order_item_id", "BIGINT", "주문 상세 ID", is_fk=True, fk_target="order_item.id"),
            col("ingredient_id", "BIGINT", "제외한 재료 ID", is_fk=True, fk_target="ingredient.id"),
        ],
    },
    {
        "name": "payment",
        "description": "결제 내역. 주문별 결제수단, 상태, 금액, 승인 시각을 저장한다.",
        "columns": [
            col("id", "BIGINT", "결제 ID", is_pk=True),
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id"),
            col("method_id", "BIGINT", "결제수단 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("status_id", "BIGINT", "결제 상태 코드 ID", is_fk=True, fk_target="common_code.id"),
            col("amount", "INT", "결제 금액. 단위 KRW"),
            col("paid_at", "TIMESTAMP", "결제 승인 시각", is_nullable=True),
        ],
    },
    {
        "name": "option_policy",
        "description": "재사용 가능한 옵션 정책 마스터. 옵션 그룹 단위로 공통 옵션 노출/기본/추천 정책을 정의한다.",
        "columns": [
            col("id", "BIGINT", "정책 ID", is_pk=True),
            col("policy_key", "CHAR(64)", "정책 구성 해시. 동일 정책 중복 생성을 방지한다."),
            col("name", "VARCHAR(120)", "정책명"),
            col("option_group_id", "BIGINT", "옵션 그룹 ID", is_fk=True, fk_target="option_group.id"),
            col("sort_order", "INT", "정책 표시 순서"),
            col("is_required", "BOOLEAN", "필수 선택 여부"),
            col("min_select", "INT", "최소 선택 수"),
            col("max_select", "INT", "최대 선택 수"),
            col("item_count", "INT", "정책에 포함된 옵션 항목 수"),
            col("menu_count", "INT", "이 정책을 사용하는 메뉴 수"),
            col("is_active", "BOOLEAN", "정책 사용 여부"),
            col("created_at", "TIMESTAMP", "생성일시"),
            col("updated_at", "TIMESTAMP", "수정일시"),
        ],
    },
    {
        "name": "option_policy_item",
        "description": "옵션 정책 안의 옵션 항목 설정. 추천/기본/정렬/노출 값을 정책 단위로 저장한다.",
        "columns": [
            col("id", "BIGINT", "정책 항목 ID", is_pk=True),
            col("policy_id", "BIGINT", "옵션 정책 ID", is_fk=True, fk_target="option_policy.id"),
            col("option_item_id", "BIGINT", "옵션 항목 ID", is_fk=True, fk_target="option_item.id"),
            col("is_recommended", "BOOLEAN", "추천 옵션 여부"),
            col("is_default", "BOOLEAN", "기본 선택 여부"),
            col("sort_order", "INT", "표시 순서"),
            col("is_active", "BOOLEAN", "노출 여부"),
        ],
    },
    {
        "name": "menu_option_policy",
        "description": "메뉴와 옵션 정책의 연결 테이블. 메뉴가 재사용 옵션 정책을 사용하도록 연결한다.",
        "columns": [
            col("id", "BIGINT", "연결 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("policy_id", "BIGINT", "옵션 정책 ID", is_fk=True, fk_target="option_policy.id"),
            col("sort_order", "INT", "메뉴 내 정책 표시 순서"),
            col("is_required", "BOOLEAN", "해당 메뉴에서 필수 여부"),
            col("priority", "INT", "정책 적용 우선순위"),
        ],
    },
    {
        "name": "menu_option_override",
        "description": "메뉴별 옵션 예외 설정. 공통 정책과 다르게 적용할 값만 저장한다.",
        "columns": [
            col("id", "BIGINT", "예외 ID", is_pk=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id"),
            col("option_item_id", "BIGINT", "옵션 항목 ID", is_fk=True, fk_target="option_item.id"),
            col("is_recommended", "BOOLEAN", "추천 여부 override", is_nullable=True),
            col("is_default", "BOOLEAN", "기본 선택 여부 override", is_nullable=True),
            col("sort_order", "INT", "정렬 override", is_nullable=True),
            col("is_active", "BOOLEAN", "노출 여부 override", is_nullable=True),
            col("note", "VARCHAR(255)", "예외 사유", is_nullable=True),
        ],
    },
]


def request_json(method: str, path: str, body: dict[str, Any] | None = None) -> Any:
    data = None
    headers = dict(HEADERS)
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
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
        except urllib.error.URLError:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


def upsert_table(table: dict[str, Any], existing: dict[str, Any]) -> tuple[int, str]:
    name = table["name"]
    body = {"name": name, "description": table["description"]}
    if name in existing:
        table_id = existing[name]["id"]
        request_json("PUT", f"/api/workspaces/{WS}/tables/{table_id}", body)
        return table_id, "updated"
    created = request_json("POST", f"/api/workspaces/{WS}/tables", body)
    return int(created["id"]), "created"


def upsert_column(table_id: int, column: dict[str, Any], existing_columns: dict[str, Any]) -> str:
    if column["name"] in existing_columns:
        current = existing_columns[column["name"]]
        body = {
            "name": column["name"],
            "data_type": column["data_type"],
            "is_pk": column["is_pk"],
            "is_fk": column["is_fk"],
            "fk_target": column.get("fk_target"),
            "is_nullable": column["is_nullable"],
            "description": column["description"],
        }
        request_json("PUT", f"/api/workspaces/{WS}/columns/{current['id']}", body)
        return "updated"
    request_json("POST", f"/api/workspaces/{WS}/tables/{table_id}/columns", column)
    return "created"


def main() -> None:
    existing_tables = request_json("GET", f"/api/workspaces/{WS}/tables")
    existing_by_name = {table["name"]: table for table in existing_tables}
    summary = {"tables_created": 0, "tables_updated": 0, "columns_created": 0, "columns_updated": 0}

    for table in TABLES:
        table_id, table_action = upsert_table(table, existing_by_name)
        summary[f"tables_{table_action}"] += 1

        refreshed = request_json("GET", f"/api/workspaces/{WS}/tables")
        refreshed_table = next(row for row in refreshed if row["name"] == table["name"])
        existing_columns = {column["name"]: column for column in refreshed_table.get("columns", [])}

        for column in table["columns"]:
            col_action = upsert_column(table_id, column, existing_columns)
            summary[f"columns_{col_action}"] += 1

        print(f"{table_action.upper()} table {table['name']} id={table_id} columns={len(table['columns'])}")

    final_tables = request_json("GET", f"/api/workspaces/{WS}/tables")
    names = sorted(table["name"] for table in final_tables)
    print("\nSummary")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print(f"  total_tables_on_server: {len(final_tables)}")
    print("  option policy tables:", ", ".join(name for name in names if "policy" in name or "override" in name))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
