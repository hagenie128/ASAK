# Kiosk Order Flow Tests

## KSK-ORDER-001 — 주문 유형 유지

Priority: P0

1. Home에서 EAT_IN 선택
2. Menu → Detail → Cart → Payment 이동

Expected:

- 모든 단계에서 orderType 유지
- Order request에 EAT_IN 포함

---

## KSK-ORDER-002 — 필수 옵션 미선택

Priority: P0

Expected:

- Cart 추가 차단
- 필수 옵션 위치에 오류
- 기존 선택 유지

---

## KSK-ORDER-003 — 최대 선택 초과

Expected:

- 추가 선택 차단 또는 validation
- 최대 개수 안내

---

## KSK-ORDER-004 — 옵션 품절

Expected:

- 품절 옵션 disabled
- 기존 선택이 품절되면 수정 안내

---

## KSK-ORDER-005 — 뒤로가기 선택 유지

Expected:

- Detail draft 유지
- Cart item과 draft 혼동 없음

---

## KSK-ORDER-006 — 주문 생성 실패

Expected:

- Cart 유지
- 다시 시도
- Home 강제 이동 없음
