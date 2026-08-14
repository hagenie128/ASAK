# Sales Data Integrity and QA

## 현재 Figma 즉시 수정 대상

- SCR-019 반복 날짜 `2025.02.22`
- SCR-021 반복 날짜
- 고객 수 정의 누락
- 동일 패턴의 고객수/매출 차트
- 고정 비교 문구
- 지원되지 않는 성장률·환불 지표
- 카테고리 명칭 불일치

## 차트와 표 정합성

```text
sum(chart sales) = KPI netSales
sum(table sales) = KPI netSales
```

## Empty

주문이 없으면:
- KPI 0
- chart empty
- table empty
- `선택한 기간에 주문 데이터가 없습니다.`

## 비교율

```text
(current - previous) / previous
```

previous가 0이면 ratio는 null, 문구는 `비교 데이터 없음`.

## QA

- [ ] 승인 결제만 포함
- [ ] timezone 경계
- [ ] previous 0 처리
- [ ] dynamic comparison label
- [ ] duplicate dummy 제거
- [ ] chart/table 합계
- [ ] filter reset
- [ ] API date validation
