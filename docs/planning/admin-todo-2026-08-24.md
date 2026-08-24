# 2026-08-24 오늘의 작업 계획 (Admin 전용, 고객화면 제외)

기준 시점: 2026-08-24. 오늘은 **고객 화면(ASAK-Kiosk)은 손대지 않는다.** 관리자 결제수단 API와 주문/환불만
진행한다. 키오스크 결제 훅·품절 재검증·장바구니 옵션 수정은 이 문서 범위 밖 — 별도 세션에서 처리.

RTOS 이벤트 DB 추가는 오늘 범위 아님 — 현재 작업사항 진행 상황에 따라 차후 처리.

---

## 우선순위 1 — 관리자 결제수단 API (의존성 없음, 바로 착수)

실행 순서가 곧 TODO 체인이다. 순서를 건너뛰면 다음 단계가 계약 불일치로 막힌다.

- [ ] **TODO-011** `AdminPaymentMethodController` (ASAK-back)
      `src/main/java/com/asak/admin/controller/AdminPaymentMethodController.java`
      GET 목록 + `PATCH /{paymentMethodId}` 추가. PATCH body: `active`, `sortOrder?`, `receiptMessage?` —
      id는 path에서만 받고 body id와 혼용 금지.
      **먼저 확정**: 현재 경로가 `/api/admin/paymentMethods`(camelCase)인데 Product Bible이 kebab-case면
      TODO-013 시작 전에 정본 경로부터 하나로 맞춘다.
- [ ] **TODO-012** `AdminPaymentMethodService` / Mapper / DTO (ASAK-back)
      `src/main/java/com/asak/admin/service/AdminPaymentMethodService.java`
      `getPaymentMethods()` / `patchPaymentMethod()` 구현. 활성/정렬/영수증문구 validation, 존재하지 않는
      id, 0건 update, 정렬 충돌 규칙을 Controller ErrorCode와 맞춘다. 정렬 변경이 여러 행을 건드리면
      트랜잭션 범위·동시 변경 정책을 먼저 정한다.
- [ ] **TODO-013** `paymentMethodsApi.js` (ASAK-Admin)
      `src/api/paymentMethodsApi.js`
      GET 목록 + `PATCH /{paymentMethodId}`를 `API_ENDPOINTS.paymentMethods` 기반으로 추가. PATCH body와
      성공 data shape를 TODO-012 DTO에 맞춘다.
- [ ] **TODO-014** `usePaymentMethodDraft.js` 훅 연결 (ASAK-Admin)
      `src/hooks/usePaymentMethodDraft.js`
      초기 load를 mock → `paymentMethodsApi.listPaymentMethods`로, `save()`를 mock →
      `paymentMethodsApi.patchPaymentMethod`로 교체. 실패 시 baselineRows 롤백, 성공 시 서버 반환값으로
      baseline 갱신 규칙 유지.
- [ ] **검증**: 토글/정렬 저장 후 재조회, 존재하지 않는 id, 정렬 충돌(409), 유효성 실패를 API로 직접 확인.

---

## 우선순위 2 — 주문/환불 (설계 결정 먼저, 그다음 구현)

환불은 코드에 명시적으로 "먼저 결정 3개 확정 전까지 손대지 말 것"이라고 박혀 있다. 순서를 지키지 않으면
cancel과 refund SQL이 뒤섞여 감사 추적이 깨진다.

- [ ] **TODO-001** 승인 결제 취소 정책 확정 (ASAK-back)
      `src/main/java/com/asak/admin/service/AdminOrderService.java` (`cancelOrder` 근처 주석)
      1) 미승인 주문 cancel과 승인 결제 refund를 분리 — TODO-038 환불 endpoint는 승인 결제만 담당하도록
         상태표 확정.
      2) 결제 상태·주문 상태·외부 결제 취소가 필요하면 TODO-039 SQL과 하나의 트랜잭션 경계로 연결.
      3) 0건 반환을 성공으로 감추지 말 것 — 행 수 0 / 허용 안 되는 상태 / 동시 변경을 ErrorCode로 구분.
- [ ] **TODO-039** 환불 SQL 분리 (ASAK-back)
      `src/main/resources/mappers/AdminOrderMapper.xml`
      cancel SQL과 분리한 orders 취소 / payment 환불 상태 변경 쿼리 각각 추가 (한 쿼리로 묶지 않음). 각
      update는 의미 있는 행 수를 반환. TODO-001/038 정책 확정 후 착수.
- [ ] **TODO-038** `PATCH /api/admin/orders/{orderId}/refund` Controller (ASAK-back)
      `src/main/java/com/asak/admin/controller/AdminOrderController.java` 맨 아래 주석
      cancel과 분리한 계약으로 확정. request body·멱등키·허용 상태·이미 환불됨(409) ErrorCode
      (`ORDER_REFUND_NOT_ALLOWED`는 이미 존재) 문서화. 상태 전이와 결제 변경은 하나의 트랜잭션으로 검증.
- [ ] **TODO-040** `ordersApi.refundOrder` 추가 (ASAK-Admin)
      `src/api/ordersApi.js`
      TODO-038/039에서 refund 경로·요청 body·결제 상태 전이·ErrorCode가 확정된 뒤 `API_ENDPOINTS.refundOrder`
      와 `refundOrder`를 추가. **cancel API를 환불에 재사용하지 않는다.**
- [ ] **TODO-042** `OrderManagePage.jsx`의 `handleRefund` 연결 (ASAK-Admin)
      `src/pages/admin/OrderManagePage.jsx`
      TODO-040 완료 후 `ordersApi.refundOrder` + `ConfirmDialog` 연결. 승인 결제만 환불 가능한지, 409/이미
      환불됨 응답 구분. 성공 뒤 훅의 `refetch()`로 목록 갱신.
- [ ] **검증**: 승인 결제 환불 성공, 미승인 주문 환불 시도(차단), 중복 환불 시도(409), cancel과 refund가
      같은 주문에 동시에 안 걸리는지 확인.

---

## 오늘 범위 밖 (참고만)

- 키오스크 결제 훅(`usePayment.js`, WBS2-026) + 주문생성/결제 통합 — 백엔드(`UserPayController`/
  `UserPayService`)는 이미 완성돼 있어 프런트 배선만 남음. 고객화면이라 오늘 제외.
- 품절 재검증/결제 차단(`soldOutPolicy.js`) — 고객화면이라 오늘 제외.
- 장바구니 항목 옵션 수정(`CartItem.jsx`) — 고객화면이라 오늘 제외.
- 환불 관련 백엔드 트랜잭션/타임스탬프 이슈는 `docs/ai-reports/2026-08-21/order-refund-timestamp-gap.md`
  참고.
- RTOS 이벤트 DB 추가 — 오늘 범위 아님, 현재 작업 진행 상황 따라 차후 결정.
