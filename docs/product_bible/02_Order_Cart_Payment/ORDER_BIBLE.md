# Order Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ORDER_API_CONTRACT.md`
- `ORDER_ARCHITECTURE.md`
- `ORDER_EDGE_CASE_AND_QA.md`
- `ORDER_FLOW_AND_STATE.md`

---

## 원문: `ORDER_API_CONTRACT.md`

### Order API Contract

> Status: Draft
> URL naming follows project camelCase rule.

#### 1. Create Order

```http
POST /api/kiosk/orders
```

##### Request

```json
{
  "orderType": "EAT_IN",
  "items": [
    {
      "menuId": 1,
      "quantity": 2,
      "selectedOptionItemIds": [101, 104],
      "excludedIngredientIds": [33]
    }
  ]
}
```

##### Response

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "orderId": 128,
    "orderNo": "1225",
    "orderStatus": "RECEIVED",
    "paymentStatus": "READY",
    "totalAmount": 16800,
    "items": [
      {
        "orderItemId": 500,
        "menuId": 1,
        "menuName": "멕시칸 랩",
        "quantity": 2,
        "unitAmount": 8400,
        "lineAmount": 16800
      }
    ]
  }
}
```

---

#### 2. Get Order

```http
GET /api/admin/orders/{orderId}
```

##### Response

```json
{
  "success": true,
  "data": {
    "orderId": 128,
    "orderNo": "1225",
    "orderType": "EAT_IN",
    "orderStatus": "PREPARING",
    "paymentStatus": "APPROVED",
    "totalAmount": 16800,
    "createdAt": "2026-07-16T03:15:00",
    "items": []
  }
}
```

---

#### 3. Change Order Status

```http
PATCH /api/admin/orders/{orderId}/{status}
```

##### Request

Path parameters: `orderId`, `status` (`PREPARING` 또는 `COMPLETED`)

Request body는 없다.

##### Response

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_ORDER_STATUS_CHANGE_SUCCESS",
  "message": "관리자 주문 상태 변경 성공",
  "data": null
}
```

---

#### 4. Error Codes

```text
ORDER_NOT_FOUND
ORDER_ITEM_REQUIRED
INVALID_ORDER_TYPE
INVALID_ORDER_STATUS
INVALID_ORDER_STATUS_TRANSITION
MENU_NOT_FOUND
MENU_SOLD_OUT
OPTION_ITEM_SOLD_OUT
INVALID_OPTION_SELECTION
ORDER_PRICE_CHANGED
```

---

#### 5. Important Rules

- Client totalAmount를 request 기준으로 신뢰하지 않는다.
- orderNo와 orderId는 분리한다.
- API JSON은 camelCase.
- DB는 snake_case.
- completed 상태 재요청은 idempotent 처리 권장.

---

## 원문: `ORDER_ARCHITECTURE.md`

### Order Architecture

> Status: Current
> Domain: Order

#### 1. 목적

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

#### 2. Order와 Cart의 차이

##### Cart

- 클라이언트 중심
- 사용자가 자유롭게 수정 가능
- 서버에 아직 확정되지 않을 수 있음
- 로컬 임시 식별자 사용 가능

##### Order

- 서버 중심
- 주문번호 보유
- 상태 전이 존재
- 서버 가격 검증 완료
- 결제 및 조리 흐름과 연결

---

#### 3. Order Lifecycle

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

#### 4. Canonical Status

##### OrderStatus

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

##### PaymentStatus

```text
READY
APPROVED
FAILED
```

---

#### 5. Figma Mapping

| Screen | Role |
|---|---|
| SCR-005 Cart | 주문 생성 전 최종 검토 |
| SCR-007 Payment | Order에 대한 결제 |
| SCR-008 Complete | Order 접수 결과 |
| SCR-009 Live Order Board | 진행 주문 운영 |
| SCR-010 Order Management | 검색·조회·상세·상태 변경 |

---

#### 6. React Responsibility

##### Kiosk

- `CartPage.jsx`
- `PaymentPage.jsx`
- `CompletePage.jsx`
- `orderSessionStore.js`

##### Admin

- `LiveOrderBoardPage.jsx`
- `OrderManagementPage.jsx`
- `OrderDetailPanel.jsx`

##### Store Draft

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

#### 7. Backend Responsibility

##### Controller

- 주문 생성
- 주문 조회
- 주문 상태 변경

##### Service

- 메뉴/옵션 유효성 검증
- 서버 가격 계산
- 주문번호 생성
- 상태 전이 검증
- 결제 상태 연결
- 완료 주문 수 계산

##### Repository

- Order
- OrderItem
- OrderItemOption

---

#### 8. DB Relation

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

#### 9. Server Price Authority

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

#### 10. Completion Data

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

#### 11. Implementation Checklist

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

---

## 원문: `ORDER_EDGE_CASE_AND_QA.md`

### Order Edge Cases and QA

#### P0 Edge Cases

##### 1. 메뉴 가격 변경

- Cart 이후 서버 가격 변경
- 주문 생성 시 최신 가격 재계산
- 결제 전 사용자 확인

##### 2. 메뉴 품절

- Menu Detail에서 담은 뒤 품절
- Order 생성 시 차단
- Cart에서 해당 항목 강조

##### 3. 옵션 품절

- 선택 옵션만 품절된 경우
- 옵션 수정 유도

##### 4. 중복 주문 생성

- 결제 버튼 연타
- isSubmitting
- server idempotency key 검토

##### 5. 주문 생성 후 결제 실패

- Order와 Cart 유지
- 재결제 가능
- 중복 Order 생성 방지 정책 필요

##### 6. Admin 중복 상태 변경

- 동일 주문 완료 버튼 연타
- idempotent response
- TTS 중복 차단

---

#### QA Checklist

##### Kiosk

- [ ] orderType 유지
- [ ] Cart item 누락 없음
- [ ] selected option 저장
- [ ] excluded ingredient 저장
- [ ] totalAmount 16,800원 일치
- [ ] sold-out 차단
- [ ] price changed UI
- [ ] create loading
- [ ] create error

##### Admin

- [ ] 최신 주문 우선
- [ ] 상태 badge
- [ ] 상태 전이
- [ ] 완료 성공 후 TTS
- [ ] 완료 중복 요청 방지
- [ ] 상세 item/option 표시

##### Backend

- [ ] transaction
- [ ] price recalculation
- [ ] validation order
- [ ] DTO only
- [ ] status transition
- [ ] idempotency

---

## 원문: `ORDER_FLOW_AND_STATE.md`

### Order Flow and State Machine

> Status: Current

#### 1. Main Sequence

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

#### 2. Order Creation Sequence

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

#### 3. Validation Order

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

#### 4. State Machine

```text
[No Order]
   ↓ create
[RECEIVED]
   ↓ admin accept/start
[PREPARING]
   ↓ complete
[COMPLETED]
```

##### Invalid Transition

```text
RECEIVED → COMPLETED
```

허용 여부는 운영 정책으로 정해야 한다.

MVP 권장:

```text
RECEIVED → PREPARING → COMPLETED
```

---

#### 5. Idempotency

동일 주문의 완료 요청이 중복되어도 중복 TTS나 중복 매출 반영이 발생하면 안 된다.

권장:

- 상태가 이미 COMPLETED이면 현재 상태 반환
- 새로운 완료 이벤트 생성 금지
- frontend는 동일 orderNo 10초 중복 발화 차단

---

#### 6. Back Navigation

##### Before Order Creation

Cart 상태 유지.

##### After Order Creation / Before Payment

권장 정책:

- Cart 수정으로 돌아가면 기존 Order draft 무효 처리 또는 재생성
- MVP에서는 Payment 화면에서 Cart로 복귀 시 기존 orderId를 폐기하고 재생성하는 방식이 단순

문서화 없는 상태에서 기존 Order를 수정하지 않는다.

---

#### 7. Order Failure States

##### ORDER_CREATE_FAILED

UI:

- 장바구니 유지
- 다시 시도
- 메뉴 화면 복귀 선택 가능

##### PRICE_CHANGED

UI:

- 변경 전 금액
- 변경 후 금액
- 확인 후 다시 주문

##### ITEM_SOLD_OUT

UI:

- 품절된 항목 표시
- 삭제 또는 옵션 수정

---

#### 8. Admin State Change

```text
Order Card action
→ PATCH status
→ Backend validates transition
→ Success Toast
→ UI state update
→ if COMPLETED: TTS
```

TTS는 PATCH 성공 후만 실행한다.
