# SCR-018: Admin Payment Method Settings

> Status: Current Draft  
> Route: `/paymentMethods`  
> Purpose: 결제수단·정책 관리


## 1. Domain

`Admin`

## 2. Figma Reference

Figma node 39:8203

## 3. Main Data

```text
paymentMethods, policies
```

## 4. Required States

- `default`
- `dirty`
- `saving`
- `success`
- `error`

## 5. Product Rules

- enabled/disabled/maintenance를 구분한다.
- 전체 비활성화는 ConfirmDialog를 사용한다.
- Kiosk가 활성 수단만 조회하도록 한다.

## 6. React Component Map

- `PaymentMethodSettingsPage`
- `PaymentMethodCard`
- `KioskPreview`
- `SaveBar`

## 7. API Contract

- `GET/PATCH /api/admin/paymentMethods`

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
