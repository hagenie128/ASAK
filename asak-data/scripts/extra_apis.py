"""API-018~020 definitions merged into notion_data when absent from Notion raw."""
from __future__ import annotations

from api_format import format_api_fields
from req_link_maps import api_req_ids, title_with_req

EXTRA_APIS: list[dict] = [
    {
        "api_id": "API-018",
        "title": "멤버십 스탬프 적립",
        "method": "POST",
        "endpoint": "/api/membership/stamps",
        "request_body": "orderId, memberId, confirmStamp",
        "response_success": "MEMBERSHIP_STAMP_SUCCESS",
        "description": "결제 후 스탬프 1회 확인·적립 (SC-006, KSD-MEMBER-001)",
    },
    {
        "api_id": "API-019",
        "title": "영수증 출력 요청",
        "method": "POST",
        "endpoint": "/api/orders/{orderId}/receipt-print",
        "request_body": "orderId",
        "response_success": "RECEIPT_PRINT_REQUESTED",
        "description": "모의 프린터 출력 요청 (SC-015, Week 5 MVP 제외)",
    },
    {
        "api_id": "API-020",
        "title": "QR/바코드 스캔",
        "method": "POST",
        "endpoint": "/api/device/scan",
        "request_body": "scanType, code",
        "response_success": "SCAN_SUCCESS",
        "description": "쿠폰/멤버십 인식 (SC-016, RTOS-DEVICE-004/005/006)",
    },
]


def merge_extra_apis(data: dict) -> int:
    """Append EXTRA_APIS rows not already present in data['apis']. Returns count added."""
    existing = {a["api_id"] for a in data.get("apis", [])}
    added = 0
    for item in EXTRA_APIS:
        api_id = item["api_id"]
        if api_id in existing:
            continue
        req_ids = api_req_ids(api_id)
        base_title = item["title"]
        fmt = format_api_fields(
            api_id,
            item["method"],
            item["endpoint"],
            item.get("request_body", ""),
            item.get("response_success", ""),
            "",
            "",
        )
        data.setdefault("apis", []).append(
            {
                "api_id": api_id,
                "title": title_with_req(f"{api_id} {base_title}", req_ids, primary_only=True),
                "base_title": base_title,
                "req_ids": req_ids,
                "method": item["method"],
                "endpoint": item["endpoint"],
                "request_params": fmt["request_params"],
                "request_body": fmt["request_body"],
                "response_success": fmt["response_success"],
                "response_error": fmt["response_error"],
                "description": item.get("description", ""),
            }
        )
        added += 1
    return added
