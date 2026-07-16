# SCR-019: Admin Sales Summary

> Status: Current Draft  
> Route: `/sales`  
> Purpose: 기간 성과 요약


## 1. Domain

`Admin`

## 2. Figma Reference

Default 39:7405 / Loading 39:8307 / Empty 39:8537 / Error 39:8557

## 3. Main Data

```text
kpis, customerCount, trend, popularMenus
```

## 4. Required States

- `default`
- `loading`
- `empty`
- `error`

## 5. Product Rules

- 고객 수는 `결제 승인 건수`로 정의해 유지할 수 있다.
- 평균 객단가는 `총매출 / 고객 수`로 계산한다.
- 고객 수는 고유 고객 수가 아님을 데이터 사전에 명시한다.
- 비교 문구는 preset에 따라 동적으로 바꾼다.
- 지원되지 않는 지표는 mock/연결예정으로 표시한다.

## 6. React Component Map

- `SalesSummaryPage`
- `SalesMetricCard`
- `SalesTrendChart`
- `DateRangePicker`

## 7. API Contract

- `GET /api/admin/sales/summary`

## 8. User Actions

- 화면의 단일 핵심 행동을 유지한다.
- destructive action은 확인 단계를 둔다.
- 실패 시 이전 입력과 선택 상태를 가능한 한 유지한다.

## 9. Edge Cases

- 네트워크 실패
- 중복 클릭
- 오래된 응답
- 품절 또는 상태 변경
- 데이터 없음
- 화면 이탈과 복귀
- 접근성 모드 적용

## 10. Accessibility

- 핵심 터치 타겟 80×80px 이상
- 색상만으로 상태를 표현하지 않음
- focus/label/aria 속성 제공
- 글자 확대 시 overflow 방지

## 11. QA Checklist

- [ ] Figma state와 React state가 일치한다.
- [ ] API 필드와 화면 표시값이 일치한다.
- [ ] Empty·Loading·Error가 누락되지 않는다.
- [ ] 접근성 기준을 충족한다.
- [ ] 잘못된 더미데이터와 개발 메모가 노출되지 않는다.

## 12. Definition of Done

- [ ] Figma 완료
- [ ] React skeleton 또는 구현
- [ ] API 계약 확인
- [ ] DB source 확인
- [ ] PrototypeMap 반영
- [ ] P0 이슈 0건
