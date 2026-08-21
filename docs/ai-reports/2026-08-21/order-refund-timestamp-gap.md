# 발견: Admin 주문 상세에 취소/환불 시각이 절대 채워지지 않음

- 날짜: 2026-08-21
- 계기: `OrderDetailPanel.jsx`에서 "환불시간 기록 컬럼이 없다"는 문제 제기로 확인.

## 결론

DB 원본 컬럼은 **존재**하지만, Admin 주문 상세 API로 오는 경로 중간(View)에서 빠져 있어서
프론트가 절대 값을 받을 수 없다. `OrderDetailPanel.jsx`의 "취소/환불일시" 표시는 현재 죽은 코드다.

## 근거

DB 컬럼 존재 확인 (`ASAK-back/docs/schema-doc-drift-2026-08-19.md` — 운영 DB에 직접 접속해
`SHOW CREATE TABLE`로 검증한 문서):

- `payment.refunded_at` TIMESTAMP NULL — **있음** (`아삭_mysql.sql` 372행)
- `orders.canceled_at` TIMESTAMP NULL — **있음** (`아삭_mysql.sql`, drift 문서 263~268행)

그런데 아래 체인에서 둘 다 중간에 빠진다:

```text
payment.refunded_at, orders.canceled_at   (DB 컬럼 — 존재)
        │
        ▼
vw_order_summary (View)
  실제 컬럼(drift 문서 2-3절, 검증됨):
  order_id, order_no, total_price, created_at, order_type_code, order_type_name,
  status_code, status_name, payment_id, paid_amount, paid_at,
  payment_status_code, payment_status_name, payment_method_name
  → canceled_at, refunded_at 둘 다 없음
        │
        ▼
AdminOrderMapper.xml #getOrderDetail (18~23행)
  SELECT order_id, order_no, order_type_code, status_code, payment_status_code,
         payment_method_name, total_price, created_at
  FROM vw_order_summary WHERE order_id = #{orderId}
  → vw_order_summary만 조회하니 애초에 선택할 컬럼이 없음
        │
        ▼
OrderDetailResponse.java
  필드: orderId, orderNo, orderType, orderStatus, paymentStatus, paymentMethod,
        totalAmount, createdAt, items
  → cancelledAt/refundedAt 필드 자체가 없음
        │
        ▼
ASAK-Admin/OrderDetailPanel.jsx 88~93행
  selectedOrder.cancelledAt ?? selectedOrder.refundedAt
  → 응답에 그 필드가 아예 없으므로 항상 undefined
```

## 왜 이렇게 됐는지 (연결된 기존 TODO)

환불 기능 자체가 백엔드에 아직 없다. 이미 알려진 미완성 지점과 정확히 같은 원인이다.

- `AdminOrderMapper.xml` 152행 TODO-039: "환불 SQL을 cancel SQL과 분리한다 ... payment/refund
  update와 조회 SQL을 추가한다" — 아직 미착수.
- `ASAK-Admin/src/api/ordersApi.js` TODO-040/042: backend TODO-038/039 완료 후
  `refundOrder`/`API_ENDPOINTS.refundOrder` 추가 예정 — 아직 미착수.
- `cancelOrder` (AdminOrderMapper.xml 146~151행)는 `orders.canceled_at`만 `NOW()`로 채우고,
  `payment.refunded_at`을 채우는 SQL은 아직 없다.

## 고치려면 (참고 — 지금은 미착수, 기록만)

1. `vw_order_summary`(또는 상세 전용 별도 쿼리)에 `orders.canceled_at`, `payment.refunded_at` 노출.
2. `AdminOrderMapper.xml` `getOrderDetail`의 SELECT·`orderDetailMap`에 두 컬럼 추가.
3. `OrderDetailResponse.java`에 `cancelledAt`/`refundedAt` 필드 추가.
4. 환불 처리 SQL(TODO-039)이 실제로 `payment.refunded_at`을 채우도록 구현 — 아래 절에 구체화.

## 다음 작업: 환불 처리 SQL (TODO-038/039/001 구체화)

기존 `cancelOrder`는 **미승인 주문만** 취소한다 (`AdminOrderService.java` 144~146행:
`paymentStatus == APPROVED`면 바로 `return 0`으로 막음). 승인 결제 건은 별도의 환불 흐름이
필요하고, 이게 바로 TODO-038/039/001이 가리키는 미구현 지점이다. `ErrorCode.java` 40행에
`ORDER_REFUND_NOT_ALLOWED`가 이미 정의돼 있지만 아직 어디서도 쓰이지 않는다.

### 확인한 값

- `orders.status_id` 코드 그룹 `ORDER_STATUS`에 `REFUNDED` 존재 (`orderLabels.js` — `ORDER_STATUS.REFUNDED`).
- `payment.status_id` 코드 그룹 `PAYMENT_STATUS`에도 `REFUNDED` 존재 (`orderLabels.js`,
  `AdminSalesMapper.xml` 114/121행의 `payment_status_code NOT IN ('CANCELED', 'REFUNDED')`로 재확인).
- `payment` 테이블 실제 컬럼(`schema-doc-drift-2026-08-19.md`): `id, order_id, method_id, status_id,
  amount, paid_at, refunded_at, idempotency_key`.

### Mapper — `AdminOrderMapper.xml`에 추가

`cancelOrder`처럼 orders 하나만 건드리지 않고, **orders와 payment를 각각 별도 update로 분리**
(TODO-039의 1번 요구사항 그대로).

```xml
<!-- code_group 'PAYMENT_STATUS'에서 코드로 status_id 조회 — findOrderStatusId와 동일 패턴 -->
<select id="findPaymentStatusId" resultType="java.lang.Long">
  SELECT cc.id
  FROM common_code cc
  JOIN code_group cg ON cc.code_grp_id = cg.id
  WHERE cg.group_code = 'PAYMENT_STATUS'
    AND cc.code = #{code}
</select>

<update id="refundOrderStatus">
UPDATE orders
SET status_id = #{refundedOrderStatusId}
WHERE id = #{orderId}
  AND status_id = #{expectedOrderStatusId}
</update>

<update id="refundPayment">
UPDATE payment
SET status_id = #{refundedPaymentStatusId},
    refunded_at = NOW()
WHERE order_id = #{orderId}
  AND status_id = #{expectedPaymentStatusId}
</update>
```

`cancelOrder`와 마찬가지로 `WHERE ... AND status_id = #{expected...}`로 낙관적 동시성을 건다 —
행 수 0이면 "그새 다른 요청이 먼저 바꿨다"는 뜻이므로 Service가 이 값을 그대로 반환해서
Controller가 409로 구분해야 한다 (TODO-039의 3번).

### Service — `AdminOrderService.refundOrder(orderId)`

```java
@Transactional // orders/payment 두 update를 하나의 트랜잭션 경계로 묶는다 (TODO-039의 3번)
public int refundOrder(Long orderId) {
  OrderDetailResponse response = adminOrderMapper.getOrderDetail(orderId);
  if (response == null) return 0;

  // cancelOrder와 반대 조건: APPROVED 결제만 환불 가능
  if (!"APPROVED".equals(response.getPaymentStatus())) return 0;

  Long refundedOrderStatusId = adminOrderMapper.findOrderStatusId("REFUNDED");
  Long approvedPaymentStatusId = adminOrderMapper.findPaymentStatusId("APPROVED");
  Long refundedPaymentStatusId = adminOrderMapper.findPaymentStatusId("REFUNDED");
  if (refundedOrderStatusId == null || approvedPaymentStatusId == null || refundedPaymentStatusId == null) {
    return 0;
  }

  int orderRows = adminOrderMapper.refundOrderStatus(Map.of(
      "orderId", orderId,
      "refundedOrderStatusId", refundedOrderStatusId,
      "expectedOrderStatusId", /* 현재 orders.status_id — getOrderDetail 응답의 orderStatus로 조회한 id */ null));

  int paymentRows = adminOrderMapper.refundPayment(Map.of(
      "orderId", orderId,
      "refundedPaymentStatusId", refundedPaymentStatusId,
      "expectedPaymentStatusId", approvedPaymentStatusId));

  return (orderRows > 0 && paymentRows > 0) ? 1 : 0;
}
```

`expectedOrderStatusId`는 `response.getOrderStatus()` 문자열을 `findOrderStatusId(...)`로 다시
id 변환해야 한다 — `cancelOrder`에는 이 값이 없었는데(취소는 상태 무관하게 진행), 환불은
"현재 orders 상태가 그대로일 때만" 갱신해야 하므로 새로 필요해진 부분이다.

### Controller — `PATCH /api/admin/orders/{orderId}/refund` (TODO-038)

```java
@PatchMapping("/{orderId}/refund")
public ApiResponse<Void> refundOrder(@PathVariable Long orderId) {
  OrderDetailResponse response = adminOrderService.getOrderDetail(orderId);
  if (response == null) return ApiResponse.error(ErrorCode.ORDER_NOT_FOUND);
  if (!"APPROVED".equals(response.getPaymentStatus())) {
    return ApiResponse.error(ErrorCode.ORDER_REFUND_NOT_ALLOWED);
  }
  if (adminOrderService.refundOrder(orderId) == 0) {
    return ApiResponse.error(ErrorCode.ORDER_REFUND_NOT_ALLOWED);
  }
  return ApiResponse.success("ADMIN_ORDER_REFUND_SUCCESS", "관리자 주문 환불 성공", null);
}
```

### 아직 결정 안 된 것 (구현 전에 확정 필요)

- **"이미 환불됨" 409를 어떻게 구분할지**: 지금 설계는 `ORDER_REFUND_NOT_ALLOWED` 하나로
  "환불 불가 상태"와 "이미 환불됨"을 뭉뚱그린다. TODO-039의 3번은 이 둘을 ErrorCode로
  나누라고 명시하므로, `ORDER_ALREADY_REFUNDED` 같은 별도 코드 추가가 필요할 수 있음
  (기존 `ErrorCode.java`엔 아직 없음).
- **멱등키**: `payment.idempotency_key`가 이미 있는 컬럼인데, 환불 API 재시도 시 이 값을
  어떻게 검증/재사용할지 TODO-001/038에서 아직 정하지 않음.
- **취소(cancel)와의 관계**: `cancelOrder`는 미승인 건 전용으로 남기고 환불(refund)을 승인 건
  전용으로 완전히 분리할지, 프론트 버튼(`canRefund`/`canPrintReceipt`) 조건도 이 결정에
  맞춰 다시 봐야 함.
- 이 문서는 SQL/코드 초안만 정리한 것이고 **아직 실행·컴파일 검증하지 않았다.**
  실제 작업 시 `compileJava`뿐 아니라 Spring 기동 후 실제 row 반영까지 확인할 것
  (TODO-039의 4번, `schema-doc-drift-2026-08-19.md` 검증 방식과 동일하게).

## 참고 문서

- [schema-doc-drift-2026-08-19.md](../../../../ASAK-back/docs/schema-doc-drift-2026-08-19.md) — DB 컬럼 존재 검증 근거
