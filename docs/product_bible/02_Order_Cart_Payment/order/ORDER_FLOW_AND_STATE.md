# Order Flow and State Machine

> Status: Current

## 1. Main Sequence

```text
Home
→ orderType 선택
→ Menu List
→ Menu Detail
→ Cart
→ 주문 생성
→ Payment
→ Complete
```

---

## 2. Order Creation Sequence

```text
Customer
  ↓
CartPage
  ↓
validateCart()
  ↓
POST order
  ↓
Backend validates menu/options/sold-out
  ↓
Backend recalculates price
  ↓
Order saved
  ↓
orderId/orderNo returned
  ↓
PaymentPage
```

---

## 3. Validation Order

서버 검증 순서:

1. Cart item 존재
2. quantity 1 이상
3. menu active
4. menu sold-out 여부
5. option group 존재
6. required/min/max selection
7. option item sold-out 여부
8. ingredient sold-out 영향
9. price recalculation
10. order save

---

## 4. State Machine

```text
[No Order]
   ↓ create
[RECEIVED]
   ↓ admin accept/start
[PREPARING]
   ↓ complete
[COMPLETED]
```

### Invalid Transition

```text
RECEIVED → COMPLETED
```

허용 여부는 운영 정책으로 정해야 한다.

MVP 권장:

```text
RECEIVED → PREPARING → COMPLETED
```

---

## 5. Idempotency

동일 주문의 완료 요청이 중복되어도 중복 TTS나 중복 매출 반영이 발생하면 안 된다.

권장:

- 상태가 이미 COMPLETED이면 현재 상태 반환
- 새로운 완료 이벤트 생성 금지
- frontend는 동일 orderNo 10초 중복 발화 차단

---

## 6. Back Navigation

### Before Order Creation

Cart 상태 유지.

### After Order Creation / Before Payment

권장 정책:

- Cart 수정으로 돌아가면 기존 Order draft 무효 처리 또는 재생성
- MVP에서는 Payment 화면에서 Cart로 복귀 시 기존 orderId를 폐기하고 재생성하는 방식이 단순

문서화 없는 상태에서 기존 Order를 수정하지 않는다.

---

## 7. Order Failure States

### ORDER_CREATE_FAILED

UI:

- 장바구니 유지
- 다시 시도
- 메뉴 화면 복귀 선택 가능

### PRICE_CHANGED

UI:

- 변경 전 금액
- 변경 후 금액
- 확인 후 다시 주문

### ITEM_SOLD_OUT

UI:

- 품절된 항목 표시
- 삭제 또는 옵션 수정

---

## 8. Admin State Change

```text
Order Card action
→ PATCH status
→ Backend validates transition
→ Success Toast
→ UI state update
→ if COMPLETED: TTS
```

TTS는 PATCH 성공 후만 실행한다.
