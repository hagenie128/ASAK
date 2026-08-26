# 환불 구현 및 가상 카드 승인 검토

> 작성일: 2026-08-26
> 범위: 환불 정적 코드 검토와 실제 PG 미연동 상태의 가상 카드 승인 검증 계획
> 판정: **환불은 구현 진행 중이며, 가상 카드 승인을 포함한 실제 흐름 검증 전에는 완료로 표시할 수 없다.**

## 1. 확인한 기준과 범위

| 구분 | 확인 근거 | 확인 결과 |
|---|---|---|
| Product Bible | `02_Order_Cart_Payment/PAYMENT_BIBLE.md`, `ORDER_BIBLE.md` | MVP는 실제 PG 대신 가상 결제를 허용한다. 주문과 결제 상태는 분리하고, 승인 금액은 서버가 주문 금액으로 결정해야 한다. |
| Screen Bible | `SCR-007-KIOSK-PAYMENT.md`, `SCR-010-ADMIN-ORDER-MANAGEMENT.md` | SCR-007은 결제 선택/처리/실패 상태와 `POST /api/kiosk/payments`를 정의한다. SCR-010은 주문 조회·상세 화면이며 기본 Figma Frame만 `134:10630`으로 기록되어 있다. |
| Kiosk 현재 코드 | `ASAK-Kiosk/src/pages/kiosk/PaymentProcessingPage.jsx` | 주문 생성 후 `testResult=true`와 타이머로 성공 화면을 표시한다. `approvePayment()` API는 호출하지 않는다. |
| Admin 현재 코드 | `ASAK-Admin/src/pages/admin/OrderManagePage.jsx`, `ordersApi.js` | 환불 버튼/확인창은 있으나 `refundAdminOrder()`이라는 mock 호출을 사용한다. `ordersApi.orderRefund`는 선언만 되어 있으며 body 없이 PATCH한다. |
| Backend 현재 코드 | `ASAK-back`의 미커밋 변경 및 `AdminOrderMapper.xml` | `/refund` Controller와 Service 초안이 추가되었지만, Mapper SQL/인터페이스와 맞지 않아 현재 상태로는 신뢰 가능한 실행 경로가 아니다. |

Figma 원본과 노드에는 이번 검토에서 직접 접근하지 못했다. 따라서 색상·간격·컴포넌트 variant는 판정하지 않았고, 문서에 기록된 화면 상태와 현재 React 상태만 비교했다.

## 2. 상태 규칙: 취소와 환불을 분리해야 한다

```text
결제 전 (Payment READY/FAILED)
  └─ 관리자 취소 → Order CANCELED

결제 승인 후 (Payment APPROVED)
  └─ 관리자 환불 → Payment REFUNDED + Order CANCELED
```

`OrderStatus`와 `PaymentStatus`는 별도다. 특히 환불을 `OrderStatus.REFUNDED`로 표현하면 주문 상태와 결제 상태가 섞인다. 화면의 “환불” 표시는 `paymentStatus === REFUNDED`를 기준으로 하고, 주문은 `CANCELED`인지 함께 표시해야 한다.

## 3. 현재 환불 구현 검토 결과

### 가능한 방향

- Admin 상세 패널은 `paymentStatus === APPROVED`인 주문에만 환불 버튼을 보이도록 하고, 이미 취소·환불된 주문은 버튼을 숨긴다.
- Admin API 상수와 `ordersApi.orderRefund` 경로는 `/api/admin/orders/{orderId}/refund` 방향으로 준비되어 있다.
- Backend는 카드만 이번 범위로 제한하려는 의도가 주석에 명시되어 있다.
- 환불 사유와 환불 시각을 보존하려는 DTO/서비스 방향은 맞다.

### 반드시 보완할 문제

#### 2026-08-26 현재 코드 기준 진행 체크

- [~] **Admin 화면 API 연결**: `OrderManagePage.jsx`의 확인창은 `ordersApi.orderRefund(orderId)`를 호출한다. 다만 백엔드 요청 DTO가 받는 `refundReason` 등을 보내지 않고, 처리 중 disabled 및 409/이미 환불됨 분기가 없어 완료가 아니다.
- [x] **DB 트랜잭션 어노테이션 존재**: `AdminOrderService.refundOrder()`에 `@Transactional`이 선언되어 있고 `CustomException`은 `RuntimeException`이다.
- [ ] **외부 결제사 호출을 DB 트랜잭션 밖에서 먼저 실행**: `refundCardOrder()`는 현재 `@Transactional` 메서드 내부에서 호출되며 실제 PG/가상 카드 취소 호출도 구현되어 있지 않다.
- [ ] **PG 성공 뒤 payment/order를 각각 1건씩 원자 갱신**: Mapper에는 payment `REFUNDED` UPDATE만 있다. 현재 Service는 일반 `cancelOrder()`를 재사용하고, `COMPLETED` 주문은 order `CANCELED` 갱신을 건너뛴다.
- [ ] **외부 성공 후 DB 실패 시 로그와 수동 확인 경로**: DB 실패를 위한 로그가 없고 Controller가 모든 예외를 `ORDER_REFUND_NOT_ALLOWED`로 통일한다.
- [ ] **브라우저·HTTP·DB 통합 검증**: 실행하지 않았다.

1. **프런트 API 연결은 시작됐지만 요청 계약과 상태 처리가 미완성이다.**
   `OrderManagePage.jsx`는 `ordersApi.orderRefund(orderId)`를 호출한다. 그러나 현재 백엔드 DTO가 요구하는 결제수단·금액·사유와 호출 body가 일치하지 않으며, 처리 중 disabled와 409/이미 환불됨 응답 구분도 없다.

2. **환불 요청의 신뢰 경계가 잘못되어 있다.**
   Controller/Service가 요청 body의 `paymentStatus`, `orderStatus`, `paymentMethod`, `totalAmount`를 기준으로 환불 가능 여부를 판단한다. 클라이언트가 이 값을 바꿔 보낼 수 있으므로, 서버는 `orderId`로 DB의 주문·결제 정보를 다시 조회한 뒤 상태/수단/승인 금액을 판정해야 한다. 클라이언트는 최소한 `refundReason`만 보낸다.

3. **Backend 연결 초안은 추가됐지만 환불 처리 완료가 아니다.**
   `AdminOrderMapper.refundOrder`와 payment `REFUNDED` UPDATE는 추가됐다. 그러나 실제 PG/가상 카드 취소 호출이 없고, 주문 `CANCELED` 전용 UPDATE와 API·DB 실행 검증도 없다. 따라서 빌드·DB 검증을 통과한 환불 구현으로 표시할 수 없다.

4. **트랜잭션 경계가 요구사항과 다르다.**
   `@Transactional`은 존재하지만 외부 환불 함수가 그 안에서 호출된다. 또한 `COMPLETED` 주문에서는 payment UPDATE 1건만 성공해도 성공 응답을 낸다. 외부 호출은 트랜잭션 밖에서 먼저 수행하고, 성공 후 별도 트랜잭션에서 payment/order UPDATE가 각각 정확히 1건인지 확인해야 한다.

5. **외부 승인 취소 결과를 대체하는 명시적 가상 승인/취소 규칙이 없다.**
   카드 환불 메서드는 TODO만 있고 성공/거절/timeout을 어떤 값으로 재현할지 정의되어 있지 않다. 이 규칙 없이는 환불 성공이라고 DB만 바꾸어 실제 PG 환불처럼 보이게 된다.

6. **환불 화면 상태가 Figma 기준으로 확정되지 않았다.**
   SCR-010은 기본 Frame만 기록되어 있다. 다음 상태의 Frame/Node, 문구, 버튼 disabled 기준이 필요하다: `환불 확인`, `환불 처리 중`, `환불 성공`, `환불 거절/네트워크 실패`, `이미 환불됨(409)`.

## 4. 권장 계약: 실제 PG 전의 가상 카드 승인

가상 결제는 화면 타이머가 아니라 **백엔드가 승인 결과를 저장하고 돌려주는 시연용 결제 어댑터**여야 한다. 그래야 Admin 환불이 같은 승인 데이터를 대상으로 검증된다.

### 승인 요청·응답

```http
POST /api/kiosk/payments
Content-Type: application/json

{
  "orderId": 128,
  "paymentMethodCode": "CARD",
  "idempotencyKey": "UUID"
}
```

서버는 `orderId`로 주문을 조회해 현재 주문 상태와 `total_price`를 확인하고, 가상 승인 결과를 만들고 저장한다. 금액과 `paymentStatus`를 프런트에서 받거나 신뢰하지 않는다.

성공 응답의 최소 데이터:

```json
{
  "paymentId": 900,
  "orderId": 128,
  "orderNo": "1225",
  "paymentStatus": "APPROVED",
  "approvedAmount": 16800,
  "approvedAt": "2026-08-26T14:00:00",
  "waitingOrderCount": 3
}
```

### 시연 전용 결과 선택 방식

- 기본값은 `APPROVED`로 고정한다.
- 실패/timeout 재현은 화면에 노출하지 않는 개발용 설정(예: local profile의 `payment.simulator.result`)으로만 선택한다.
- 가능한 값은 `APPROVED`, `DECLINED`, `TIMEOUT`으로 제한한다.
- 응답에 `provider=VIRTUAL_CARD`, `providerTransactionId`, `simulated=true`를 남긴다.
- 운영 profile에서는 이 어댑터를 비활성화하거나 실제 PG 어댑터로 교체한다. 가상 승인 정보를 실제 카드 승인번호처럼 표기하지 않는다.

### 가상 환불 규칙

`PATCH /api/admin/orders/{orderId}/refund`의 body는 아래처럼 환불 사유만 받는다.

```json
{ "refundReason": "고객 요청" }
```

서버 순서:

1. `orderId`로 주문과 가장 최근 결제를 조회한다.
2. 결제가 `APPROVED`이고 수단이 `CARD`, provider가 `VIRTUAL_CARD`인지 확인한다.
3. 가상 취소 결과가 성공일 때만 한 트랜잭션에서 payment를 `REFUNDED` 및 `refunded_at`으로, order를 `CANCELED` 및 `canceled_at`으로 변경한다.
4. 두 변경이 각각 1건인지 확인한다. 아니면 rollback 및 409/500을 구분해 반환한다.
5. 성공 응답에는 DB에서 재조회한 주문/결제 상태와 시각을 반환한다.

## 5. 팀원이 구현할 권장 순서

1. **Figma 상태 확정**: SCR-010 환불 확인/처리/성공/실패/이미 환불됨 Frame과 문구를 확정한다. SCR-007 Processing/Success/Error와도 문구·버튼 상태를 맞춘다.
2. **Backend 결제 승인 경로 연결**: Kiosk가 `approvePayment()`를 실제로 호출하도록 하기 전에 Controller–Service–Mapper–XML의 주문 상태 기준(`READY` 또는 `RECEIVED`)을 하나로 정한다. 현재 Service 내부에서도 두 기준이 충돌한다.
3. **가상 카드 승인 저장**: 서버 계산 금액, idempotency key, `APPROVED/FAILED`, provider 식별값과 승인 시각을 payment에 저장한다.
4. **환불 Mapper/트랜잭션 완성**: DB 재조회 기반 검증, payment/order 각각의 UPDATE, 1건 검증, rollback을 구현한다.
5. **Admin 연결**: mock 호출을 제거하고 `ordersApi.orderRefund(orderId, { refundReason })`로 연결한다. 처리 중에는 확인 버튼과 환불 버튼을 disabled하고, 성공 시 상세·목록을 재조회한다.
6. **통합 검증 후만 완료 표시**: 아래 시나리오를 브라우저·API·DB에서 모두 확인한다.

## 6. 검증 시나리오와 합격 기준

| 번호 | 시나리오 | 확인 위치 | 합격 기준 |
|---|---|---|---|
| P-01 | 카드 가상 승인 성공 | Kiosk, HTTP 응답, payment DB | `APPROVED`, 서버 계산 금액, 승인 시각, provider 식별값이 저장된다. |
| P-02 | 승인 버튼 연타/동일 idempotency key 재전송 | HTTP, DB | payment가 한 건만 생성되고 기존 결과를 반환하거나 명확한 충돌을 반환한다. |
| P-03 | 가상 승인 거절 | Kiosk, DB | 완료 화면으로 가지 않고 cart/선택 수단을 유지하며 `FAILED` 이력이 남는다. |
| P-04 | 승인 성공 응답 유실 후 재시도 | HTTP, DB | 중복 승인·중복 주문 없이 기존 승인 결과를 확인한다. |
| R-01 | 승인된 가상 카드 환불 | Admin, HTTP, orders/payment DB | `payment=REFUNDED`, `order=CANCELED`, 두 시각·사유가 함께 저장된다. |
| R-02 | 환불 버튼 연타/동시 요청 | HTTP, DB | 한 요청만 성공하고 나머지는 이미 환불/상태 충돌로 처리되며 이중 환불이 없다. |
| R-03 | 결제 전 주문 취소 | Admin, orders DB | payment 환불 없이 `order=CANCELED`만 변경된다. |
| R-04 | 비카드 또는 미승인 결제 환불 | HTTP, DB | 409을 반환하고 DB 상태가 바뀌지 않는다. |
| R-05 | 환불 DB 업데이트 중 실패 | DB/로그 | payment와 order가 한쪽만 바뀌지 않고 모두 rollback된다. |

## 7. 이번 검토에서 확인하지 못한 항목

- Backend 빌드, Spring 기동, 실제 HTTP 요청, MyBatis SQL 실행, DB 행 변경은 실행하지 않았다.
- 실제 PG/카드 단말 연동은 범위 밖이며, 이 문서의 `VIRTUAL_CARD`는 시연용이다.
- Figma 원본의 환불 관련 Frame/Node와 시각 디자인은 접근 권한이 없어 확인하지 못했다.

따라서 현재 확인 가능한 결론은 다음과 같다. **화면에 환불 UI와 API 초안은 있으나, 실제 결제 모듈이 붙지 않은 상태에서는 가상 승인을 서버에 저장하는 흐름부터 연결하고, 그 승인 데이터를 대상으로 환불을 통합 검증해야 한다.**
