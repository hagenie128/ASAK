#!/usr/bin/env python3
"""Save live Notion MCP fetch payloads into notion_raw/."""
from __future__ import annotations

import json
from pathlib import Path

RAW = Path(__file__).parent / "notion_raw"

# (page_id, title, full MCP text field)
PAGES: list[tuple[str, str, str]] = [
    (
        "39151ef04f0b81f5892ce9384de4f834",
        "QR/바코드로 쿠폰 인식 후 결제",
        'Here is the result of "view" for the Page with URL https://app.notion.com/p/39151ef04f0b81f5892ce9384de4f834 as of 2026-07-06T01:33:03.602Z:\n<page url="https://app.notion.com/p/39151ef04f0b81f5892ce9384de4f834">\n<properties>\n{"url":"https://app.notion.com/p/39151ef04f0b81f5892ce9384de4f834","관련 API":"POST /api/device/scan","관련 요구사항":"RTOS-DEVICE-004, RTOS-DEVICE-005, RTOS-DEVICE-006, LMIS-ORDER-005","관련 화면":"SCR-007, SCR-021","시나리오 ID":"SC-016","시나리오명":"QR/바코드로 쿠폰 인식 후 결제","시작 조건":"고객이 모바일 쿠폰을 보유하고 있음","종료 조건":"할인 적용된 금액으로 결제 완료","기본 흐름":"결제 단계 진입 → 모바일 쿠폰/멤버십 바코드 스캔 → 할인 자동 적용 → 잔액 결제 진행","예외 흐름":"스캔 실패/만료된 쿠폰 시 오류 메시지 안내 후 일반결제로 진행","상태":"초안"}\n</properties>\n<content>\n```mermaid\nflowchart TD\n    A[결제 단계 SCR-007] --> B[모바일 쿠폰 QR/바코드 스캔 SCR-021]\n    B --> C{유효 코드?}\n    C -->|예| D[할인 자동 적용]\n    C -->|아니오| E[오류 안내 후 일반결제 진행]\n    D --> F[잔액 결제]\n```\n</content>\n</page>',
    ),
    (
        "39251ef04f0b81b99b6fc38923f826c0",
        "최종 통합 리허설에서 주문-결제-관리자 확인",
        'Here is the result of "view" for the Page with URL https://app.notion.com/p/39251ef04f0b81b99b6fc38923f826c0 as of 2026-07-06T02:44:39.614Z:\n<page url="https://app.notion.com/p/39251ef04f0b81b99b6fc38923f826c0">\n<properties>\n{"url":"https://app.notion.com/p/39251ef04f0b81b99b6fc38923f826c0","관련 API":"API-001~API-009","관련 요구사항":"FWD-ORDER-001, FWD-CART-001, FWD-PAY-002, DEV-ORDER-001, KSD-PAY-001, LMIS-ORDER-001, LMIS-ORDER-002","관련 테스트":"TC-001, TC-002, TC-003, TC-004, TC-014","관련 화면":"SCR-001~SCR-011","시나리오 ID":"SC-024","시나리오명":"최종 통합 리허설에서 주문-결제-관리자 확인","시작 조건":"Week 5 MVP(8/1) 또는 최종 발표(9/2) 전 전체 데모 환경이 준비되어 있음","종료 조건":"고객 주문 완료와 관리자 주문 확인/상태 변경까지 한 번에 시연 가능","기본 흐름":"1. 고객이 홈에서 주문을 시작한다. 2. 먹고가기/포장을 선택한다. 3. 메뉴를 선택하고 옵션을 구성한다. 4. 장바구니와 주문 확인을 거쳐 결제한다. 5. 주문 완료 화면을 확인한다. 6. 관리자가 주문 목록/상세에서 주문 상태와 선택 옵션/제외 재료를 확인한다.","예외 흐름":"결제 실패, 품절 항목 포함, 필수 옵션 미선택, 관리자 상태 변경 실패 시 해당 화면과 API 오류 응답을 기준으로 재시도 또는 오류 안내를 확인한다.","상태":"확정"}\n</properties>\n<content>\n```mermaid\nflowchart TD\n    A[홈 SCR-001] --> B[먹고가기/포장 SCR-002]\n    B --> C[메뉴·옵션 SCR-003/004]\n    C --> D[장바구니·주문확인 SCR-005/006]\n    D --> E[결제 SCR-007]\n    E --> F[완료 SCR-008]\n    F --> G[관리자 확인 SCR-009/010]\n```\n</content>\n</page>',
    ),
    (
        "39151ef04f0b816dac73e50493047aac",
        "일정시간 미입력 시 자동 초기화 (FWD-SYS-001)",
        'Here is the result of "view" for the Page with URL https://app.notion.com/p/39151ef04f0b816dac73e50493047aac.\n<page url="https://app.notion.com/p/39151ef04f0b816dac73e50493047aac">\n<properties>\n{"url":"https://app.notion.com/p/39151ef04f0b816dac73e50493047aac","관련 API":"없음(프론트 로컬 타이머)","관련 요구사항":"FWD-SYS-001","관련 화면":"SCR-013, SCR-005","시나리오 ID":"SC-012","시나리오명":"일정시간 미입력 시 자동 초기화 (FWD-SYS-001)","시작 조건":"주문 진행 중 고객이 자리를 비움","종료 조건":"초기화면으로 전환되고 다음 고객이 깨끗한 상태로 이용 가능","기본 흐름":"고객이 주문 진행 중 자리를 뜨 → 일정시간(예 30초) 동안 입력 없음 → 경고 없이 초기화면으로 자동 복귀 → 장바구니 초기화","예외 흐름":"타임아웃 직전 다시 터치하면 타이머 리셋","상태":"초안"}\n</properties>\n<content>\n```mermaid\nflowchart TD\n    A[주문 진행 중 입력 없음] --> B{일정시간 경과?}\n    B -->|예| C[초기화면 자동 복귀 SCR-001]\n    B -->|아니오| D[대기 지속]\n    C --> E[장바구니 초기화 SCR-005]\n```\n</content>\n</page>',
    ),
    (
        "39151ef04f0b8110a97ed0e2593fe40b",
        "접근성 옵션으로 저시력 고객 주문 (FWD-UI-001)",
        'Here is the result of "view" for the Page with URL https://app.notion.com/p/39151ef04f0b8110a97ed0e2593fe40b.\n<page url="https://app.notion.com/p/39151ef04f0b8110a97ed0e2593fe40b">\n<properties>\n{"url":"https://app.notion.com/p/39151ef04f0b8110a97ed0e2593fe40b","관련 API":"API-017","관련 요구사항":"FWD-UI-004","관련 화면":"SCR-014","시나리오 ID":"SC-013","시나리오명":"접근성 옵션으로 저시력 고객 주문 (FWD-UI-001)","시작 조건":"저시력 고객이 키오스크 이용 시작","종료 조건":"안내 없이 주문 완료","기본 흐름":"저시력 고객이 초기화면 진입 → 글자크기 확대 옵션 인지 → 큰 글자/높은 대비로 메뉴 탐색 → 주문 완료","예외 흐름":"없음","상태":"초안"}\n</properties>\n<content>\n```mermaid\nflowchart TD\n    A[저시력 고객 진입 SCR-001] --> B[접근성 설정 SCR-014]\n    B --> C[큰 글자/고대비 메뉴 탐색 SCR-003~SCR-008]\n    C --> D[안내 없이 주문 완료 SCR-008]\n```\n</content>\n</page>',
    ),
]


def main() -> None:
    RAW.mkdir(exist_ok=True)
    for pid, title, text in PAGES:
        url = f"https://app.notion.com/p/{pid}"
        out = {"title": title, "url": url, "text": text}
        (RAW / f"{pid}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved {pid}")
    print(f"Wrote {len(PAGES)} scenario pages")


if __name__ == "__main__":
    main()
