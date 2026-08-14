# Sales Tests

## 공식 정의

```text
고객 수 = 결제 승인 건수
평균 객단가 = 총매출 / 고객 수
```

## SALES-001 — KPI 정합성

- 총매출
- 고객 수
- 평균 객단가

## SALES-002 — 차트 합계

Expected:
- 일별/월별 합계 = KPI

## SALES-003 — 시간대별 고객 수

Expected:
- 합계 = 전체 고객 수

## SALES-004 — 결제수단 비율

Expected:
- 합계 100%

## SALES-005 — 주문유형 비율

Expected:
- 합계 100%

## SALES-006 — 비교율

Expected:
- 표시값과 계산값 일치

## SALES-007 — previous 0

Expected:
- 비교 데이터 없음

## SALES-008 — Mock Data

Expected:
- 날짜 중복 없음
- KPI·표·차트 모두 일치
