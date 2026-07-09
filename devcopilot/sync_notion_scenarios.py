#!/usr/bin/env python3
"""Sync Notion-updated scenarios to DevCopilot API (workspace 2). Uses stdlib only."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}

# Notion 정본 (2026-07-06) — SCR ID 반영 mermaid + 흐름
UPDATES: dict[str, dict] = {
    "SC-001": {
        "pre_condition": "ASAK 키오스크 화면 진입(처음 방문 고객)",
        "post_condition": "결제 완료 후 주문번호가 화면에 표시됨",
        "normal_flow": "홈(SCR-001)·매장/포장 선택 → 카테고리·메뉴 선택(SCR-003) → 옵션 선택(SCR-004) → 장바구니·주문확인 컨펌 팝업(SCR-005) → 결제(SCR-007) → 주문 완료(SCR-008)",
        "alternative_flow": "옵션이 헷갈려 이전 단계로 돌아가도 선택 내용이 유지됨 (사용자가 지적한 키오스크 취소 시 초기화 문제 개선)",
        "mermaid_script": (
            "flowchart TD\n"
            "    A[홈·매장/포장 SCR-001] --> C[메뉴 선택 SCR-003]\n"
            "    C --> D[옵션 선택 SCR-004]\n"
            "    D --> E[장바구니·주문확인 SCR-005]\n"
            "    E --> F[컨펌 팝업 확인]\n"
            "    F --> G[결제 SCR-007]\n"
            "    G --> H[주문 완료 SCR-008]"
        ),
    },
    "SC-003": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[관리자 품절 처리 SCR-011] --> B[메뉴/옵션 SOLD OUT 표시 SCR-003, SCR-004]\n"
            "    B --> C[고객 선택 불가 SCR-003, SCR-004]\n"
            "    C --> D[다른 항목으로 대체 선택 SCR-003, SCR-004]"
        ),
    },
    "SC-002": {
        "normal_flow": "메뉴 선택 → 추천조합 기본값 → 장바구니(SCR-005) 컨펌 팝업 확인 → 결제(SCR-007) → 완료(SCR-008)",
        "post_condition": "결제 완료 및 주문번호 표시, 화면 전환 4회 이내 목표 (2026-07-06: SCR-002·006 병합, 주문확인은 SCR-005 컨펌 팝업)",
        "mermaid_script": (
            "flowchart TD\n"
            "    A[메뉴 선택 SCR-003] --> B[추천조합 기본값 SCR-004]\n"
            "    B --> C[장바구니·주문확인 팝업 SCR-005]\n"
            "    C --> D[결제 SCR-007]\n"
            "    D --> E[완료 SCR-008]\n"
            "    E --> F[화면 전환 4회 이내]"
        ),
    },
    "SC-004": {
        "normal_flow": "장바구니·주문확인 컨펌 팝업(SCR-005) → API-005 주문 생성 → 결제(SCR-007) → 승인 → 주문 완료(SCR-008)",
        "mermaid_script": (
            "flowchart TD\n"
            "    A[장바구니·주문확인 SCR-005] --> B[컨펌 팝업 확인]\n"
            "    B --> C[API-005 주문 생성]\n"
            "    C --> D[결제 SCR-007]\n"
            "    D --> E{결제 승인?}\n"
            "    E -->|성공| F[주문 완료 SCR-008]"
        ),
    },
    "SC-006": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[결제 SCR-007] --> B[적립 확인 SCR-021 1회 노출]\n"
            "    B --> C[결제 완료 SCR-008]\n"
            "    C --> D[적립 결과 자동 표시]"
        ),
    },
    "SC-005": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[결제 SCR-007] --> B{결제 승인?}\n"
            "    B -->|실패| C[결제 실패 SCR-012]\n"
            "    C --> D[장바구니 유지 SCR-005]\n"
            "    D --> E[결제 재시도 SCR-007]\n"
            "    E --> A"
        ),
    },
    "SC-007": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[품절 관리 SCR-011 토글 ON] --> B[메뉴/옵션 표시 갱신 SCR-003, SCR-004]\n"
            "    B --> C[고객 화면 즉시 반영]"
        ),
    },
    "SC-008": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[고객 결제 완료 SCR-008] --> B[관리자 주문 목록 SCR-009]\n"
            "    B --> C[주문 상세 SCR-010]\n"
            "    C --> D[준비중으로 변경 API-008]\n"
            "    D --> E[완료로 변경 API-008]\n"
            "    E --> F[매장/포장 구분 표시 SCR-010]"
        ),
    },
    "SC-009": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[장바구니 진입 SCR-005] --> B[수량 -/+ 조정 SCR-005]\n"
            "    B --> C[개별 항목 삭제 SCR-005]\n"
            "    C --> D[총금액 자동 재계산 SCR-005]\n"
            "    C -->|마지막 1개 삭제| E[메뉴선택 유도 SCR-003]"
        ),
    },
    "SC-010": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[메뉴/옵션 선택 SCR-003, SCR-004] --> B[알레르기/비건 태그 확인]\n"
            "    B --> C{해당 재료 포함?}\n"
            "    C -->|예| D[메뉴 회피 또는 옵션 조정]\n"
            "    C -->|아니오| E[정상 진행]"
        ),
    },
    "SC-011": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[기본 포함 재료 확인 SCR-004] --> B[특정 재료 '빼기' 선택 SCR-004]\n"
            "    B --> C[가격 변동 없이 반영]\n"
            "    C --> D[장바구니/주문서 제외 항목 표시 SCR-005]"
        ),
    },
    "SC-012": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[주문 진행 중 입력 없음] --> B{일정시간 경과?}\n"
            "    B -->|예| C[초기화면 자동 복귀 SCR-001]\n"
            "    B -->|아니오| D[대기 지속]\n"
            "    C --> E[장바구니 초기화 SCR-005]"
        ),
    },
    "SC-013": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[저시력 고객 진입 SCR-001] --> B[접근성 설정 SCR-014]\n"
            "    B --> C[큰 글자/고대비 메뉴 탐색 SCR-003~SCR-008]\n"
            "    C --> D[안내 없이 주문 완료 SCR-008]"
        ),
    },
    "SC-014": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[홈 매장·포장 SCR-001] --> B[orderType 선택]\n"
            "    B --> C[orderType 유지 SCR-003~005]\n"
            "    C --> D[주문 생성 시 orderType 반영]"
        ),
    },
    "SC-015": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[주문 완료 SCR-008] --> B{영수증 출력? SCR-020}\n"
            "    B -->|예| C[API-019 모의 프린터 요청]\n"
            "    B -->|아니오| D[화면 주문번호 표시]\n"
            "    C --> E[출력 결과 확인]\n"
            "    E --> D"
        ),
    },
    "SC-016": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[결제 단계 SCR-007] --> B[모바일 쿠폰 QR/바코드 스캔 SCR-021]\n"
            "    B --> C{유효 코드?}\n"
            "    C -->|예| D[할인 자동 적용]\n"
            "    C -->|아니오| E[오류 안내 후 일반결제 진행]\n"
            "    D --> F[잔액 결제]"
        ),
    },
    "SC-017": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[관리자 로그인 SCR-015] --> B[메뉴 관리 SCR-016]\n"
            "    B --> C[신규 메뉴 등록 SCR-017: 이름/가격/이미지/카테고리]\n"
            "    C --> D[옵션그룹 연결]\n"
            "    D --> E[저장 → 키오스크 메뉴 SCR-003 즉시 노출]"
        ),
    },
    "SC-018": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[관리자 로그인 SCR-015] --> B[기간 선택 SCR-019]\n"
            "    B --> C[일별 매출/메뉴별 판매량 조회 SCR-019]\n"
            "    C --> D{데이터 존재?}\n"
            "    D -->|없음| E[공백 상태 안내 SCR-019]\n"
            "    D -->|있음| F[표/그래프 표시 SCR-019]"
        ),
    },
    # SC-019~024: Notion Mermaid (확장 시나리오, SCR ID 미정리 구간은 Notion 원문 유지)
    "SC-019": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[점심시간 다수 고객 동시 접속] --> B[메뉴조회/주문 동시 요청]\n"
            "    B --> C{응답 목표시간 이내?}\n"
            "    C -->|예| D[정상 처리]\n"
            "    C -->|아니오| E[로깅 및 지연 안내]"
        ),
    },
    "SC-020": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[기본 드레싱 선택 SCR-004] --> B[별도포장 드레싱 추가 선택 SCR-004]\n"
            "    B --> C[장바구니에 드레싱 2개 표시 SCR-005]\n"
            "    C --> D[주문서에 별도포장 안내 SCR-005]"
        ),
    },
    "SC-021": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[토핑 선택 SCR-004] --> B[+ 버튼으로 수량 증가 SCR-004]\n"
            "    B --> C[가격 수량만큼 자동 재계산 SCR-005]\n"
            "    C --> D{최대 5개 도달?}\n"
            "    D -->|예| E[버튼 비활성화 안내 SCR-004]\n"
            "    D -->|아니오| F[계속 담기 가능 SCR-005]"
        ),
    },
    "SC-022": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[커스텀 옵션 포함 주문 접수 SCR-008] --> B[관리자 주문목록 SCR-009]\n"
            "    B --> C[추가 재료 강조 SCR-010]\n"
            "    C --> D[제외 재료 강조 SCR-010]\n"
            "    D --> E[조리 준비]"
        ),
    },
    "SC-023": {
        "mermaid_script": (
            "flowchart TD\n"
            "    A[개발 완료 후 부하테스트] --> B[메뉴목록 API-001 - 목표 2초]\n"
            "    B --> C[옵션조회 API-004 - 목표 1초]\n"
            "    C --> D[결제 API-006 - 목표 3초]\n"
            "    D --> E{목표시간 내 응답?}\n"
            "    E -->|아니오| F[병목 구간 점검]"
        ),
    },
    "SC-024": {
        "normal_flow": (
            "1. 홈(SCR-001)에서 매장/포장 선택 → 2. 메뉴·옵션(SCR-003/004) "
            "→ 3. 장바구니·주문확인 컨펌 팝업(SCR-005) → 4. 결제(SCR-007) → 5. 완료(SCR-008) "
            "→ 6. 관리자 주문 확인·상태변경(SCR-009/010)"
        ),
        "mermaid_script": (
            "flowchart TD\n"
            "    A[홈 매장·포장 SCR-001] --> B[메뉴·옵션 SCR-003/004]\n"
            "    B --> C[장바구니·주문확인 팝업 SCR-005]\n"
            "    C --> D[결제 로딩 SCR-007]\n"
            "    D --> E[완료 SCR-008]\n"
            "    E --> F[관리자 확인 SCR-009/010]"
        ),
    },
}


def api(method: str, path: str, body: dict | None = None) -> tuple[int, str]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        headers=HEADERS,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def main() -> int:
    status, raw = api("GET", f"/api/workspaces/{WS}/scenarios")
    if status != 200:
        print(f"FAIL list scenarios: {status} {raw[:300]}", file=sys.stderr)
        return 1
    existing = {s["id"]: s for s in json.loads(raw)}
    ok = 0
    for sid, patch in sorted(UPDATES.items()):
        cur = existing.get(sid)
        if not cur:
            print(f"SKIP {sid}: not in DevCopilot")
            continue
        body = {
            "id": sid,
            "title": cur.get("title") or sid,
            "pre_condition": patch.get("pre_condition") or cur.get("pre_condition") or "",
            "post_condition": patch.get("post_condition") or cur.get("post_condition") or "",
            "normal_flow": patch.get("normal_flow") or cur.get("normal_flow") or "",
            "alternative_flow": patch.get("alternative_flow") or cur.get("alternative_flow") or "",
            "mermaid_script": patch.get("mermaid_script") or cur.get("mermaid_script") or "",
            "status": cur.get("status") or "DRAFT",
        }
        code, text = api("PUT", f"/api/workspaces/{WS}/scenarios/{sid}", body)
        has_scr = "SCR-" in body["mermaid_script"]
        if code in (200, 201):
            ok += 1
            print(f"OK  {sid} SCR_in_mermaid={has_scr}")
        else:
            print(f"FAIL {sid}: {code} {text[:200]}", file=sys.stderr)
    print(f"Synced {ok}/{len(UPDATES)} scenarios")
    return 0 if ok == len(UPDATES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
