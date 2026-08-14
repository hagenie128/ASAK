# Error Recovery Architecture

> Status: Current

## 원칙
오류는 기술 메시지가 아니라 다음 행동을 선택할 수 있는 제품 상태다.

## 오류 분류
```text
VALIDATION
NETWORK
SERVER
BUSINESS
PAYMENT
SESSION
UNSUPPORTED
```

## Kiosk
- Menu Load Error: 다시 시도 / 처음으로
- Menu Detail Validation: 선택 유지 + 해당 옵션 안내
- Cart Validation: 품절 항목 강조 + 수정/삭제
- Order Create Error: Cart 유지 + 다시 시도
- Payment Error: 다시 결제 / 다른 수단 / Cart
- Timeout: 계속 주문 / 처음으로

## Admin
- page retry
- widget partial error
- save rollback
- Toast
- unsaved draft 유지

## Error Response Draft
```json
{
  "success": false,
  "message": "OPTION_ITEM_SOLD_OUT",
  "data": {
    "field": "selectedOptionItemIds",
    "targetId": 101,
    "canRetry": true
  }
}
```

## 공통 React 구조
```text
ErrorState
InlineError
Toast
ConfirmDialog
useApiError
errorMessageMap
```

## 금지
- alert() 남용
- 서버 원문 노출
- 오류 후 무조건 Home 이동
- 사용자 입력 즉시 초기화
