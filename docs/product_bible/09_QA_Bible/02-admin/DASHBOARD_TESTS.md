# Dashboard Tests

## DASH-001 — KPI

- 순매출
- 주문 수
- 평균 객단가
- 진행 중 주문

Expected:
- 계산 기준 일치

## DASH-002 — Empty

Expected:
- 0값
- 정상 Empty copy

## DASH-003 — Partial Error

Expected:
- 실패 widget만 Error
- 전체 Dashboard 유지

## DASH-004 — Refresh

Expected:
- duplicate fetch 없음
- lastUpdatedAt 갱신

## DASH-005 — Navigation

Expected:
- Home active
- 주문관리와 역할 분리
