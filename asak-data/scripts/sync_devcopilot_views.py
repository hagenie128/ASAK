#!/usr/bin/env python3
"""Sync ASAK DB views into DevCopilot workspace 2 (ERD tables).

Uses DevCopilot MCP HTTP transport.
  DEVCOPILOT_MCP_URL  — full MCP URL including ?token=...
  DEVCOPILOT_WS_ID    — workspace id (default 2)

Example:
  set DEVCOPILOT_MCP_URL=https://devcopilot.ai.kr/api/mcp/mcp?token=...
  python asak-data/scripts/sync_devcopilot_views.py
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from typing import Any


WS = int(os.environ.get("DEVCOPILOT_WS_ID", "2"))
MCP_URL = os.environ.get("DEVCOPILOT_MCP_URL", "").strip()


def col(
    name: str,
    data_type: str,
    description: str,
    *,
    is_pk: bool = False,
    is_fk: bool = False,
    fk_target: str | None = None,
    is_nullable: bool = True,
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


# Live asak_db views (2026-07-24) + Korean descriptions for DevCopilot ERD.
VIEWS: list[dict[str, Any]] = [
    {
        "name": "vw_menu_opt_resolved",
        "description": "[View] 메뉴–옵션정책–옵션항목을 행 단위로 펼침. menu_opt_override가 있으면 정책 기본값보다 메뉴 오버라이드 우선(COALESCE).",
        "columns": [
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("policy_id", "BIGINT", "옵션 정책 ID", is_fk=True, fk_target="opt_policy.id", is_nullable=False),
            col("policy_name", "VARCHAR(120)", "정책명", is_nullable=False),
            col("min_select", "INT", "최소 선택 수", is_nullable=False),
            col("max_select", "INT", "최대 선택 수", is_nullable=False),
            col("policy_required", "TINYINT", "정책 필수 여부", is_nullable=False),
            col("opt_item_id", "BIGINT", "옵션 항목 ID", is_fk=True, fk_target="opt_item.id", is_nullable=False),
            col("opt_item_name", "VARCHAR(100)", "옵션 항목명", is_nullable=False),
            col("add_price", "INT", "추가 금액(KRW)", is_nullable=False),
            col("opt_item_sold_out", "TINYINT", "옵션 품절 여부", is_nullable=False),
            col("recommended", "INT", "추천 여부(오버라이드 병합)", is_nullable=False),
            col("is_default", "INT", "기본 선택 여부(오버라이드 병합)", is_nullable=False),
            col("sort_no", "BIGINT", "표시 순서(오버라이드 병합)", is_nullable=False),
            col("active", "INT", "활성 여부(오버라이드 병합)", is_nullable=False),
        ],
    },
    {
        "name": "vw_menu_opt_policy_json",
        "description": "[View] 옵션 정책당 1행. items JSON(JSON_ARRAYAGG). 키오스크 optionGroups 필드명 맞춤(option_group_id/extraPrice/servingUnit 등). 2026-07-24.",
        "columns": [
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("option_group_id", "BIGINT", "옵션 그룹(정책) ID", is_fk=True, fk_target="opt_policy.id", is_nullable=False),
            col("name", "VARCHAR(120)", "옵션 그룹명", is_nullable=False),
            col("group_type", "VARCHAR(50)", "그룹 유형 코드(BASE/DRESSING 등)", is_nullable=False),
            col("select_type", "VARCHAR(6)", "SINGLE 또는 MULTI", is_nullable=False),
            col("min_select", "INT", "최소 선택 수", is_nullable=False),
            col("max_select", "INT", "최대 선택 수", is_nullable=False),
            col("sort_order", "INT", "메뉴 내 그룹 표시 순서", is_nullable=False),
            col("is_required", "INT", "필수 여부", is_nullable=False),
            col("items", "JSON", "옵션 항목 JSON 배열(optionItemId, extraPrice, servingUnit 등)", is_nullable=True),
        ],
    },
    {
        "name": "vw_menu_ing_detail",
        "description": "[View] 메뉴 재료 상세 + 알레르기. 알레르기 N개면 재료 행이 N줄로 늘어날 수 있음.",
        "columns": [
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("ing_id", "BIGINT", "재료 ID", is_fk=True, fk_target="ing.id", is_nullable=False),
            col("ing_name", "VARCHAR(100)", "재료명", is_nullable=False),
            col("ing_sold_out", "TINYINT", "재료 품절", is_nullable=False),
            col("role_id", "BIGINT", "재료 역할 코드(CORE/BASE/DEFAULT 등)", is_fk=True, fk_target="common_code.id", is_nullable=False),
            col("quantity", "DECIMAL(8,2)", "수량", is_nullable=True),
            col("unit_id", "BIGINT", "단위 코드", is_fk=True, fk_target="common_code.id", is_nullable=True),
            col("is_default", "TINYINT", "기본 포함 여부", is_nullable=False),
            col("can_remove", "TINYINT", "제외(빼기) 가능 여부", is_nullable=False),
            col("sort_no", "INT", "표시 순서", is_nullable=False),
            col("allergen_id", "BIGINT", "알레르기 ID", is_fk=True, fk_target="allergen.id", is_nullable=True),
            col("allergen_name", "VARCHAR(50)", "알레르기명", is_nullable=True),
        ],
    },
    {
        "name": "vw_menu_ing_json",
        "description": "[View] 메뉴 재료당 1행. allergens JSON. 프론트 필드명 맞춤(ingredient_id, role/unit 문자 코드). 2026-07-24.",
        "columns": [
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("ingredient_id", "BIGINT", "재료 ID", is_fk=True, fk_target="ing.id", is_nullable=False),
            col("ing_name", "VARCHAR(100)", "재료명", is_nullable=True),
            col("ing_sold_out", "TINYINT", "재료 품절", is_nullable=True),
            col("role", "VARCHAR(50)", "재료 역할 코드(소문자, 예: core/base/default)", is_nullable=False),
            col("quantity", "DECIMAL(8,2)", "수량", is_nullable=True),
            col("unit", "VARCHAR(50)", "단위 표시 코드", is_nullable=True),
            col("is_default", "TINYINT", "기본 포함 여부", is_nullable=False),
            col("can_remove", "TINYINT", "제외 가능 여부", is_nullable=False),
            col("sort_no", "INT", "표시 순서", is_nullable=False),
            col("allergens", "JSON", "알레르기 JSON 배열. 없으면 []", is_nullable=True),
        ],
    },
    {
        "name": "vw_menu_availability",
        "description": "[View] 메뉴 주문가능/품절 판정 플래그. CORE·BASE·DEFAULT·필수옵션그룹 규칙을 각각 계산.",
        "columns": [
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=True),
            col("direct_sold_out", "TINYINT", "메뉴 자체 품절(menu.sold_out)", is_nullable=True),
            col("has_core_sold_out", "INT", "CORE 재료 품절 → 무조건 품절", is_nullable=False),
            col("base_ing_exhausted", "INT", "BASE 재료(고정형) 전부 품절", is_nullable=False),
            col("base_opt_exhausted", "INT", "BASE 옵션그룹 선택가능 옵션 0", is_nullable=False),
            col("has_blocking_standard", "INT", "DEFAULT 재료 품절 + 제거 불가", is_nullable=False),
            col("has_exhausted_required_group", "INT", "필수 옵션그룹 min_select 미충족", is_nullable=False),
        ],
    },
    {
        "name": "vw_menu_list",
        "description": "[View] 메뉴 목록용. is_orderable / has_sold_out_ingredient. category_id(API categoryId). 2026-07-24.",
        "columns": [
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("category_id", "BIGINT", "카테고리 ID", is_fk=True, fk_target="category.id", is_nullable=False),
            col("name", "VARCHAR(100)", "메뉴명", is_nullable=False),
            col("price", "INT", "기본 가격", is_nullable=False),
            col("image_url", "TEXT", "이미지 URL", is_nullable=True),
            col("base_kcal", "DECIMAL(8,2)", "기본 칼로리(menu_nutr)", is_nullable=True),
            col("is_sold_out", "TINYINT", "메뉴 직접 품절", is_nullable=False),
            col("has_sold_out_ingredient", "INT", "재료/베이스 관련 품절 플래그 OR", is_nullable=False),
            col("is_orderable", "INT", "주문 가능 여부(모든 품절 조건 NOT)", is_nullable=True),
        ],
    },
    {
        "name": "vw_soldout_catalog",
        "description": "[View] 품절 관리 카탈로그. 메뉴/재료/옵션아이템 UNION (target_type=MENU|INGREDIENT|OPTION_ITEM).",
        "columns": [
            col("target_type", "VARCHAR(11)", "대상 유형", is_nullable=False),
            col("target_id", "BIGINT", "대상 ID", is_nullable=False),
            col("name", "VARCHAR(100)", "표시명", is_nullable=False),
            col("category", "VARCHAR(100)", "분류명(카테고리/타입/옵션그룹)", is_nullable=False),
            col("is_sold_out", "TINYINT", "품절 여부", is_nullable=False),
            col("price", "INT", "가격(재료는 NULL)", is_nullable=True),
        ],
    },
    {
        "name": "vw_order_item_detail",
        "description": "[View] 주문 라인 기본 상세. 주문번호 + 메뉴명 + 수량/가격.",
        "columns": [
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id", is_nullable=False),
            col("order_no", "VARCHAR(50)", "주문번호", is_nullable=False),
            col("order_item_id", "BIGINT", "주문 라인 ID", is_fk=True, fk_target="order_item.id", is_nullable=False),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("menu_name", "VARCHAR(100)", "메뉴명", is_nullable=False),
            col("quantity", "INT", "수량", is_nullable=False),
            col("price", "INT", "라인 가격", is_nullable=False),
        ],
    },
    {
        "name": "vw_order_item_option",
        "description": "[View] 주문 라인에 선택된 옵션(정규화 행).",
        "columns": [
            col("order_item_id", "BIGINT", "주문 라인 ID", is_fk=True, fk_target="order_item.id", is_nullable=False),
            col("opt_item_id", "BIGINT", "옵션 항목 ID", is_fk=True, fk_target="opt_item.id", is_nullable=False),
            col("opt_item_name", "VARCHAR(100)", "옵션명", is_nullable=False),
            col("quantity", "INT", "옵션 수량", is_nullable=False),
            col("price", "INT", "옵션 가격", is_nullable=False),
        ],
    },
    {
        "name": "vw_order_item_exclusion",
        "description": "[View] 주문 라인에서 제외한 재료 목록.",
        "columns": [
            col("order_item_id", "BIGINT", "주문 라인 ID", is_fk=True, fk_target="order_item.id", is_nullable=False),
            col("ing_id", "BIGINT", "제외 재료 ID", is_fk=True, fk_target="ing.id", is_nullable=False),
            col("ing_name", "VARCHAR(100)", "재료명", is_nullable=False),
        ],
    },
    {
        "name": "vw_order_item_full",
        "description": "[View] 주문 라인 1행 + option_items/excluded_ingredients JSON. Admin/API-007 필드명 맞춤. order_item_id 없음. 2026-07-24.",
        "columns": [
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id", is_nullable=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=True),
            col("menu_name", "VARCHAR(100)", "메뉴명", is_nullable=False),
            col("quantity", "INT", "수량", is_nullable=True),
            col("unit_price", "INT", "품목 단가", is_nullable=True),
            col("option_items", "JSON", "선택 옵션 JSON(optionItemId 키)", is_nullable=True),
            col("excluded_ingredients", "JSON", "제외 재료 JSON(ingredientId 키)", is_nullable=True),
        ],
    },
    {
        "name": "vw_order_item_base_dressing",
        "description": "[View] 주문 라인의 BASE/DRESSING 옵션을 컬럼으로 pivot.",
        "columns": [
            col("order_item_id", "BIGINT", "주문 라인 ID", is_fk=True, fk_target="order_item.id", is_nullable=False),
            col("base_name", "VARCHAR(100)", "베이스 옵션명", is_nullable=True),
            col("dressing_name", "VARCHAR(100)", "드레싱 옵션명", is_nullable=True),
        ],
    },
    {
        "name": "vw_order_item_tag",
        "description": "[View] BASE/DRESSING 제외 옵션 + 제외재료. tone=side|drink|plus|exclude (UI 태그).",
        "columns": [
            col("order_item_id", "BIGINT", "주문 라인 ID", is_fk=True, fk_target="order_item.id", is_nullable=False),
            col("tone", "VARCHAR(7)", "태그 톤(side/drink/plus/exclude)", is_nullable=False),
            col("label", "VARCHAR(100)", "표시 라벨", is_nullable=False),
        ],
    },
    {
        "name": "vw_order_summary",
        "description": "[View] 주문 요약. 유형/상태/결제상태/결제수단을 코드명으로 해석.",
        "columns": [
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id", is_nullable=False),
            col("order_no", "VARCHAR(50)", "주문번호", is_nullable=False),
            col("total_price", "INT", "주문 총액", is_nullable=False),
            col("created_at", "TIMESTAMP", "주문 생성 시각", is_nullable=False),
            col("order_type_code", "VARCHAR(50)", "주문 유형 코드", is_nullable=False),
            col("order_type_name", "VARCHAR(50)", "주문 유형명", is_nullable=False),
            col("status_code", "VARCHAR(50)", "주문 상태 코드", is_nullable=False),
            col("status_name", "VARCHAR(50)", "주문 상태명", is_nullable=False),
            col("payment_id", "BIGINT", "결제 ID", is_fk=True, fk_target="payment.id", is_nullable=True),
            col("paid_amount", "INT", "결제 금액", is_nullable=True),
            col("paid_at", "TIMESTAMP", "결제 시각", is_nullable=True),
            col("payment_status_code", "VARCHAR(50)", "결제 상태 코드", is_nullable=True),
            col("payment_status_name", "VARCHAR(50)", "결제 상태명", is_nullable=True),
            col("payment_method_name", "VARCHAR(50)", "결제 수단명", is_nullable=True),
        ],
    },
    {
        "name": "vw_order_list_summary",
        "description": "[View] 주문 목록 한 줄 요약. menu_summary는 '메뉴명' 또는 '메뉴명 외 N'.",
        "columns": [
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id", is_nullable=False),
            col("order_no", "VARCHAR(50)", "주문번호", is_nullable=False),
            col("created_at", "TIMESTAMP", "주문 생성 시각", is_nullable=False),
            col("total_price", "INT", "주문 총액", is_nullable=False),
            col("order_type_code", "VARCHAR(50)", "주문 유형 코드", is_nullable=False),
            col("order_type_name", "VARCHAR(50)", "주문 유형명", is_nullable=False),
            col("status_code", "VARCHAR(50)", "주문 상태 코드", is_nullable=False),
            col("status_name", "VARCHAR(50)", "주문 상태명", is_nullable=False),
            col("payment_status_code", "VARCHAR(50)", "결제 상태 코드", is_nullable=True),
            col("payment_status_name", "VARCHAR(50)", "결제 상태명", is_nullable=True),
            col("line_count", "BIGINT", "주문 라인 수", is_nullable=False),
            col("item_count", "DECIMAL(32,0)", "총 수량(라인 quantity 합)", is_nullable=True),
            col("menu_summary", "MEDIUMTEXT", "메뉴 한 줄 요약", is_nullable=True),
        ],
    },
    {
        "name": "vw_order_live",
        "description": "[View] 실시간 주문 보드. elapsed_sec=생성 후 경과 초.",
        "columns": [
            col("order_id", "BIGINT", "주문 ID", is_fk=True, fk_target="orders.id", is_nullable=False),
            col("order_no", "VARCHAR(50)", "주문번호", is_nullable=False),
            col("order_type_label", "VARCHAR(50)", "주문 유형 표시명", is_nullable=False),
            col("status_code", "VARCHAR(50)", "주문 상태 코드", is_nullable=False),
            col("total_price", "INT", "주문 총액", is_nullable=False),
            col("created_at", "TIMESTAMP", "주문 생성 시각", is_nullable=False),
            col("elapsed_sec", "BIGINT", "경과 초", is_nullable=True),
        ],
    },
    {
        "name": "vw_order_status_summary",
        "description": "[View] 일자×주문유형×상태별 주문 건수 집계.",
        "columns": [
            col("order_date", "DATE", "주문 일자", is_nullable=True),
            col("order_type_code", "VARCHAR(50)", "주문 유형 코드", is_nullable=False),
            col("order_type_name", "VARCHAR(50)", "주문 유형명", is_nullable=False),
            col("status_code", "VARCHAR(50)", "상태 코드", is_nullable=False),
            col("status_name", "VARCHAR(50)", "상태명", is_nullable=False),
            col("order_count", "BIGINT", "건수", is_nullable=False),
        ],
    },
    {
        "name": "vw_sales_daily",
        "description": "[View] 관리자 일별 매출. 승인/취소·환불을 반영한 일자별 집계.",
        "columns": [
            col("sales_date", "DATE", "매출 일자", is_nullable=True),
            col("order_count", "BIGINT", "승인 주문 수", is_nullable=False),
            col("canceled_order_count", "BIGINT", "취소/환불 주문 수", is_nullable=False),
            col("gross_sales_amount", "DECIMAL(32,0)", "총매출(승인)", is_nullable=False),
            col("canceled_amount", "DECIMAL(32,0)", "취소/환불 금액", is_nullable=False),
            col("net_sales_amount", "DECIMAL(33,0)", "순매출", is_nullable=False),
        ],
    },
    {
        "name": "vw_sales_hourly",
        "description": "[View] 관리자 시간대별 매출. 일자/시간대별 집계.",
        "columns": [
            col("sales_date", "DATE", "매출 일자", is_nullable=True),
            col("sales_hour", "INT", "시간대 0~23", is_nullable=True),
            col("order_count", "BIGINT", "승인 주문 수", is_nullable=False),
            col("canceled_order_count", "BIGINT", "취소/환불 주문 수", is_nullable=False),
            col("gross_sales_amount", "DECIMAL(32,0)", "총매출(승인)", is_nullable=False),
            col("canceled_amount", "DECIMAL(32,0)", "취소/환불 금액", is_nullable=False),
            col("net_sales_amount", "DECIMAL(33,0)", "순매출", is_nullable=False),
        ],
    },
    {
        "name": "vw_top_menu_daily",
        "description": "[View] 일별 인기 메뉴. 승인 결제 주문 기준 수량·매출.",
        "columns": [
            col("sales_date", "DATE", "매출 일자", is_nullable=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("menu_name", "VARCHAR(100)", "메뉴명", is_nullable=False),
            col("quantity", "DECIMAL(32,0)", "판매 수량", is_nullable=True),
            col("order_count", "BIGINT", "포함 주문 수", is_nullable=False),
            col("sales_amount", "DECIMAL(42,0)", "판매 금액", is_nullable=True),
        ],
    },
    {
        "name": "vw_top_menu_hourly",
        "description": "[View] 시간대별 인기 메뉴. 승인 결제 주문 기준.",
        "columns": [
            col("sales_date", "DATE", "매출 일자", is_nullable=True),
            col("sales_hour", "INT", "시간대 0~23", is_nullable=True),
            col("menu_id", "BIGINT", "메뉴 ID", is_fk=True, fk_target="menu.id", is_nullable=False),
            col("menu_name", "VARCHAR(100)", "메뉴명", is_nullable=False),
            col("quantity", "DECIMAL(32,0)", "판매 수량", is_nullable=True),
            col("order_count", "BIGINT", "포함 주문 수", is_nullable=False),
            col("sales_amount", "DECIMAL(42,0)", "판매 금액", is_nullable=True),
        ],
    },
]


class McpClient:
    def __init__(self, url: str) -> None:
        self.url = url
        self.session_id: str | None = None
        self._opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def _post(self, body: dict[str, Any], *, notification: bool = False) -> Any:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
        for attempt in range(3):
            try:
                with self._opener.open(req, timeout=120) as resp:
                    sid = resp.headers.get("Mcp-Session-Id") or resp.headers.get("mcp-session-id")
                    if sid:
                        self.session_id = sid
                    text = resp.read().decode("utf-8")
                    if notification:
                        return None
                    for line in text.splitlines():
                        if line.startswith("data: "):
                            return json.loads(line[6:])
                    if text.strip():
                        return json.loads(text)
                    return None
            except urllib.error.HTTPError as exc:
                err = exc.read().decode("utf-8", errors="replace")
                if exc.code >= 500 and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(f"MCP HTTP {exc.code}: {err}") from exc
        raise RuntimeError("unreachable")

    def initialize(self) -> None:
        self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "asak-sync-views", "version": "1.0"},
                },
            }
        )
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"}, notification=True)

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        payload = self._post(
            {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            }
        )
        if not payload or "error" in payload:
            raise RuntimeError(f"tools/call {name} failed: {payload}")
        result = payload.get("result", {})
        if result.get("isError"):
            raise RuntimeError(f"tools/call {name} isError: {result}")
        # prefer structuredContent.result, else content[0].text
        structured = result.get("structuredContent") or {}
        if "result" in structured:
            raw = structured["result"]
            if isinstance(raw, str):
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return raw
            return raw
        texts = [c.get("text", "") for c in result.get("content", []) if c.get("type") == "text"]
        joined = "\n".join(texts)
        try:
            return json.loads(joined)
        except json.JSONDecodeError:
            return joined


def index_schema(schema: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in schema:
        name = row.get("table_name") or row.get("name")
        if not name:
            continue
        cols = {c["name"]: c for c in row.get("columns", [])}
        out[name] = {"table_id": row.get("table_id") or row.get("id"), "columns": cols, "raw": row}
    return out


def refresh(client: McpClient) -> dict[str, dict[str, Any]]:
    schema = client.call("get_db_schema", {"workspace_id": WS})
    if not isinstance(schema, list):
        raise RuntimeError(f"unexpected schema type: {type(schema)}")
    return index_schema(schema)


def upsert_view(client: McpClient, view: dict[str, Any], existing: dict[str, dict[str, Any]]) -> tuple[str, dict[str, dict[str, Any]]]:
    name = view["name"]
    if name in existing:
        client.call(
            "update_db_table",
            {
                "workspace_id": WS,
                "table_id": existing[name]["table_id"],
                "description": view["description"],
            },
        )
        action = "updated"
        existing_cols = existing[name]["columns"]
    else:
        client.call(
            "create_db_table",
            {
                "workspace_id": WS,
                "name": name,
                "description": view["description"],
            },
        )
        action = "created"
        existing = refresh(client)
        existing_cols = existing[name]["columns"]

    created_any = False
    for column in view["columns"]:
        if column["name"] in existing_cols:
            client.call(
                "update_db_column",
                {
                    "workspace_id": WS,
                    "column_id": existing_cols[column["name"]]["id"],
                    "data_type": column["data_type"],
                    "is_pk": column["is_pk"],
                    "is_fk": column["is_fk"],
                    "fk_target": column["fk_target"],
                    "is_nullable": column["is_nullable"],
                    "description": column["description"],
                },
            )
        else:
            client.call(
                "create_db_column",
                {
                    "workspace_id": WS,
                    "table_name": name,
                    "name": column["name"],
                    "data_type": column["data_type"],
                    "is_pk": column["is_pk"],
                    "is_fk": column["is_fk"],
                    "fk_target": column["fk_target"],
                    "is_nullable": column["is_nullable"],
                    "description": column["description"],
                },
            )
            created_any = True

    if created_any or action == "created":
        existing = refresh(client)
    return action, existing


def main() -> None:
    if not MCP_URL:
        print("DEVCOPILOT_MCP_URL 환경변수가 필요합니다.", file=sys.stderr)
        sys.exit(1)

    client = McpClient(MCP_URL)
    print("initialize…", flush=True)
    client.initialize()
    print("load schema…", flush=True)
    existing = refresh(client)
    print(f"tables={len(existing)}", flush=True)

    for i, view in enumerate(VIEWS, 1):
        action, existing = upsert_view(client, view, existing)
        print(f"[{i}/{len(VIEWS)}] {action} {view['name']}", flush=True)

    view_names = sorted(n for n in existing if str(n).startswith("vw_"))
    print("views in DevCopilot:", ", ".join(view_names), flush=True)
    print(f"count={len(view_names)}", flush=True)


if __name__ == "__main__":
    main()
