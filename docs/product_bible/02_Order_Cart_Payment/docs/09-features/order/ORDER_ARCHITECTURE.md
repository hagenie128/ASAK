# Order Architecture

> Status: Current  
> Domain: Order

## 1. 목적

Order 도메인은 고객이 선택한 메뉴와 옵션을 서버 기준의 주문 단위로 확정하고, 이후 결제·조리·완료 흐름을 연결한다.

Order는 단순히 Cart 데이터를 복사하는 객체가 아니다.

Order는 다음 책임을 가진다.

- 주문 유형 저장
- 주문 항목 확정
- 서버 가격 재계산
- 주문번호 생성
- 주문 상태 관리
- 결제 연결
- 주방 처리 연결
- 매출 집계의 기준 제공

---

## 2. Order와 Cart의 차이

### Cart

- 클라이언트 중심
- 사용자가 자유롭게 수정 가능
- 서버에 아직 확정되지 않을 수 있음
- 로컬 임시 식별자 사용 가능

### Order

- 서버 중심
- 주문번호 보유
- 상태 전이 존재
- 서버 가격 검증 완료
- 결제 및 조리 흐름과 연결

---

## 3. Order Lifecycle

```text
CART_READY
    ↓
ORDER_CREATING
    ↓
RECEIVED
    ↓
PREPARING
    ↓
COMPLETED
```

결제 실패 시 Order 자체를 즉시 삭제하지 않는다.

권장:

```text
RECEIVED + Payment READY/FAILED
```

또는 주문 생성과 결제 승인 순서를 분리해:

```text
DRAFT
→ PAYMENT_PENDING
→ RECEIVED
```

현재 ASAK scaffold의 상태값과 단순성을 고려하면 첫 번째 방식이 적합하다.

---

## 4. Canonical Status

### OrderStatus

```text
RECEIVED
PREPARING
COMPLETED
```

추가 검토 상태:

```text
CANCELED
```

`CANCELED`는 실제 취소 기능을 구현할 때 공식 enum으로 추가한다. 영국식 표기
`CANCELLED`는 legacy mock 외의 API 계약과 신규 구현에 사용하지 않는다.

### PaymentStatus

```text
READY
APPROVED
FAILED
```

---

## 5. Figma Mapping

| Screen | Role |
|---|---|
| SCR-005 Cart | 주문 생성 전 최종 검토 |
| SCR-007 Payment | Order에 대한 결제 |
| SCR-008 Complete | Order 접수 결과 |
| SCR-009 Live Order Board | 진행 주문 운영 |
| SCR-010 Order Management | 검색·조회·상세·상태 변경 |

---

## 6. React Responsibility

### Kiosk

- `CartPage.jsx`
- `PaymentPage.jsx`
- `CompletePage.jsx`
- `orderSessionStore.js`

### Admin

- `LiveOrderBoardPage.jsx`
- `OrderManagementPage.jsx`
- `OrderDetailPanel.jsx`

### Store Draft

```js
{
  orderId: null,
  orderNo: null,
  orderType: null,
  orderStatus: null,
  paymentStatus: null,
  waitingOrderCount: null
}
```

---

## 7. Backend Responsibility

### Controller

- 주문 생성
- 주문 조회
- 주문 상태 변경

### Service

- 메뉴/옵션 유효성 검증
- 서버 가격 계산
- 주문번호 생성
- 상태 전이 검증
- 결제 상태 연결
- 완료 주문 수 계산

### Repository

- Order
- OrderItem
- OrderItemOption

---

## 8. DB Relation

```text
orders
 ├─ order_item
 │   └─ order_item_option
 └─ payment
```

권장 주요 컬럼:

```text
orders
- id
- order_no
- order_type
- order_status
- total_amount
- created_at
- updated_at
```

---

## 9. Server Price Authority

Order 생성 시 서버는 반드시 재계산한다.

```text
menu base price
+ selected option price
× quantity
= line total
```

전체:

```text
sum(line total) = total amount
```

클라이언트 금액과 다르면:

- 주문 생성 중단
- 최신 가격 반환
- Cart에 변경 안내

---

## 10. Completion Data

SCR-008에 필요한 최소 응답:

```json
{
  "orderId": 128,
  "orderNo": "1225",
  "orderStatus": "RECEIVED",
  "paymentStatus": "APPROVED",
  "totalAmount": 16800,
  "waitingOrderCount": 3
}
```

---

## 11. Implementation Checklist

- [ ] OrderStatus 공식 상수
- [ ] Order 생성 request/response
- [ ] 서버 가격 재계산
- [ ] OrderItem 저장
- [ ] OrderItemOption 저장
- [ ] orderNo 생성
- [ ] waitingOrderCount
- [ ] Admin 상태 변경
- [ ] 상태 전이 검증
- [ ] Order 조회 API
- [ ] Figma/API/DB naming 일치
