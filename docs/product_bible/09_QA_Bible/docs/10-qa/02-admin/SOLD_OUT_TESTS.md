# Sold-out Tests

## SOLD-001 — Menu direct sold-out

Expected:
- Kiosk card disabled

## SOLD-002 — CORE ingredient

Expected:
- 연결 메뉴 derived sold-out

## SOLD-003 — BASE 일부 품절

Expected:
- 대체 base가 있으면 메뉴 유지

## SOLD-004 — BASE 전체 품절

Expected:
- 메뉴 품절

## SOLD-005 — STANDARD ingredient

Expected:
- 제거 가능 시 메뉴 유지 + 안내

## SOLD-006 — OPTIONAL

Expected:
- 해당 옵션만 disabled

## SOLD-007 — Required group 전체 품절

Expected:
- 메뉴 품절

## SOLD-008 — 저장 취소

Expected:
- dirty draft 폐기

## SOLD-009 — 일부 저장 실패

Expected:
- 전체 rollback

## SOLD-010 — 해제

Expected:
- derived 원인 해소 시 복구
- direct sold-out이면 유지
