# 2026-08-24 오늘의 작업 계획 (Admin 전용, 고객화면 제외)

기준 시점: 2026-08-24. 오늘은 **고객 화면(ASAK-Kiosk)은 손대지 않는다.** 관리자 결제수단 API와 주문/환불만
진행한다. 키오스크 결제 훅·품절 재검증·장바구니 옵션 수정은 이 문서 범위 밖 — 별도 세션에서 처리.

RTOS 이벤트 DB 추가는 오늘 범위 아님 — 현재 작업사항 진행 상황에 따라 차후 처리.

> **2026-08-25 업데이트** (teacher 협의 결과 반영)
>
> 1. **로그인 방식 변경**: 계정(아이디/비밀번호) 인증 대신 **매장 번호 '0001' 고정값 하드코드 승인**으로
>    확정. DB 조회·매장별 로그인 확장 없음. 세션도 **JWT 미사용, 단순 승인 플래그**로 확정 — TODO-028
>    (JwtTokenProvider)은 불필요해짐. 기존 TODO-027(username/password + AuthenticationManager) 설계를
>    이 방향에 맞게 다시 써야 함 — 아래 신규 **우선순위 2** 참고.
> 2. **환불 결제수단 범위**: **카드/신용카드**는 이번 프로젝트에 반영한다. **토스페이**는 API를 확인한 상태이며,
>    실제 연동과 결제 과정 통합 테스트가 성공할 때만 프로젝트 범위에 포함한다.
> 3. **TODO-001 승인 결제 취소 정책 확정** — order_status는 기존 `CANCELED` 재사용(payment_status만
>    `REFUNDED`로 구분), 외부 결제사 API 먼저 호출 후 성공 시 DB 트랜잭션 원자 처리, 중복 환불 방지는
>    별도 멱등키 없이 `payment_status` 상태 체크만으로 처리. 아래 **우선순위 3** TODO-001 참고 — 이제
>    TODO-039 → TODO-038 → TODO-040 → TODO-042 순서로 구현 착수 가능.
> 4. 위 결정에 맞춰 관련 설계 문서도 함께 갱신할 것.

---

## 우선순위 1 — 관리자 결제수단 API (의존성 없음, 바로 착수)

실행 순서가 곧 TODO 체인이다. 순서를 건너뛰면 다음 단계가 계약 불일치로 막힌다.

- [~] **TODO-011** `AdminPaymentMethodController` (ASAK-back) — 매핑 골격 존재, 런타임 미검증
  `src/main/java/com/asak/admin/controller/AdminPaymentMethodController.java`
  `GET /api/admin/paymentMethods`, `PATCH /{paymentMethodId}`가 있으며 식별자는 path variable만 쓴다.
  현재 요청 DTO는 `active`, `sortNo`만 가진다. `receiptMessage`는 API·DB 계약이 없어 이번 연결 범위에서 제외한다.
  Screen Bible과 Controller의 정본 경로는 camelCase `/api/admin/paymentMethods`로 일치한다.
- [~] **TODO-012** `AdminPaymentMethodService` / Mapper / DTO (ASAK-back) — 골격 존재, 구현 보완 필요
  `src/main/java/com/asak/admin/service/AdminPaymentMethodService.java`
  `getPaymentMethods()` / `updatePaymentMethod()` 호출 골격은 있다. Mapper SQL의 `onF` 오타와 map 바인딩,
  요청 검증, 존재하지 않는 id·0건 갱신 구분, DTO 경계를 보완한 뒤 API를 검증한다.
  현재는 한 행의 `sort_no`를 수정하므로 정렬 충돌(409)을 두지 않는다. 목록은 `sort_no ASC, id ASC`로
  동점 순서를 고정한다. 여러 행 재정렬은 endpoint·동시 변경 정책·transaction을 별도 TODO로 분리한다.

- [x] **TODO-013** `paymentMethodsApi.js` (ASAK-Admin)
      `src/api/paymentMethodsApi.js`
      GET 목록 + `PATCH /{paymentMethodId}`를 `API_ENDPOINTS.paymentMethods` 기반으로 추가. PATCH body와
      성공 data shape를 TODO-012 DTO에 맞춘다. mock의 `isActive`/`sortOrder`와 API의 `active`/`sortNo`는
      adapter 또는 계약 통일 후 연결한다.
- [x] **TODO-014** `usePaymentMethodDraft.js` 훅 연결 (ASAK-Admin)
      `src/hooks/usePaymentMethodDraft.js`
      초기 load를 mock → `paymentMethodsApi.listPaymentMethods`로, `save()`를 mock →
      `paymentMethodsApi.patchPaymentMethod`로 교체한다. 현재 화면의 순서 이동은 여러 행을 바꾸므로, 개별 PATCH
      순차 호출과 일괄 저장 endpoint 중 하나를 계약으로 먼저 확정한다. 실패 시 baselineRows 롤백 규칙은 유지한다.
- [ ] **검증**: 토글/정렬 저장 후 재조회, 없는 id, 유효하지 않은 요청, 0건 갱신을 API·DB row로 확인한다.

---

## 우선순위 2 — 로그인: 매장 번호 승인 방식 (2026-08-25 결정, 설계 재정의 먼저)

기존 `AdminAuthController`(ASAK-back)는 TODO-027로 username/password + `AuthenticationManager` 설계가,
TODO-028로 `JwtTokenProvider` 기반 세션 설계가 잡혀 있었으나, **매장 번호 '0001'로 승인 + 단순 승인
플래그 세션**으로 방향이 바뀌었다. 계정 인증도 JWT도 아니므로 기존 TODO-027/028 설계를 그대로 구현하면
안 되고, 먼저 계약을 다시 정의해야 한다.

- [x] **설계 확정 (2026-08-25)** — 매장 번호는 **고정값 '0001' 하드코드 승인**으로, 세션은 \*\*JWT 없이
  ```
  단순 승인 플래그**로 결정. DB 매장 테이블 조회·매장별 로그인 확장·토큰 발급/만료 관리 없음.
  `AdminAuthController`의 TODO-027(username/password)과 TODO-028(`JwtTokenProvider`) 주석은 이
  결정과 어긋나므로 아래 내용으로 다시 쓴다 — TODO-028은 더 이상 필요 없다.
  ```
- [x] **TODO-027 재정의** `AdminAuthController` (ASAK-back)
  ```
  `POST /api/admin/login` request body를 `{ storeNumber }` 기준으로 재정의하고, 입력값이 하드코드
  '0001'과 일치하는지만 검사한다 — `AuthenticationManager`/DB 조회/JWT 발급 제거. 불일치 시 401(또는
  별도 ErrorCode), 일치 시 단순 승인 플래그(예: `{ approved: true }`) 응답을 확정한다.
  ```
- [x] **TODO-031~034 연쇄 갱신** (ASAK-Admin)
  ```
  `src/api/adminApi.js`(TODO-031) → `src/pages/admin/LoginPage.jsx`(TODO-034) 순서로, 아이디/비밀번호
  입력 폼을 매장 번호 입력으로 교체하고 `loginAdmin` mock을 실제 API 응답 연결로 바꾼다. `apiClient.js`
  (TODO-033)·`adminSession.js`(TODO-032)는 토큰 저장/만료 판정 로직이 필요 없어짐 — 기존
  `adminSession.js`의 단순 `loggedIn` 플래그 저장 구조를 그대로 유지하고, mock 호출 자리만 실제 API
  승인 응답으로 교체한다.
  ```
- [ ] **검증**: 정상 매장 번호('0001') 승인, 잘못된 매장 번호, 빈 입력이 각각 성공/실패 계약을 지키는지
  ```
  확인.
  ```

---

## 우선순위 3 — 주문/환불 (설계 결정 먼저, 그다음 구현)

환불은 코드에 명시적으로 "먼저 결정 3개 확정 전까지 손대지 말 것"이라고 박혀 있다. 순서를 지키지 않으면
cancel과 refund SQL이 뒤섞여 감사 추적이 깨진다. **2026-08-25 정책 확정 완료** — 아래 TODO-001 참고.

- [x] **TODO-001** 승인 결제 취소 정책 확정 (ASAK-back) — **2026-08-25 확정**
  ```
  `src/main/java/com/asak/admin/service/AdminOrderService.java` (`cancelOrder` 근처 주석)
  1) **미승인 cancel / 승인 refund 분리** — 이미 코드에 구현됨: `cancelOrder()`가
     `paymentStatus == "APPROVED"`면 `ORDER_PAYMENT_APPROVED_CANCEL_NOT_ALLOWED`로 차단하고 있어,
     승인 결제는 cancel로 못 건드리고 반드시 TODO-038 refund만 처리한다. 이 동작을 그대로 유지·확정.
  2) **환불 성공 후 order_status**: 기존 **`CANCELED` 값을 재사용**한다. order_status에 별도
     `REFUNDED` 값을 새로 만들지 않는다 — payment_status만 `REFUNDED`(기존 `PaymentStatus` enum에
     이미 존재)로 바꿔서 "취소"와 "환불"을 payment 레벨에서 구분한다. DB에 새 common_code row를
     추가하지 않아도 되므로 리스크가 적다.
  3) **트랜잭션 경계**: 외부 결제사(카드/토스페이) 취소·환불 API를 **DB 트랜잭션 밖에서 먼저** 호출하고,
     성공한 경우에만 TODO-039의 payment UPDATE + order UPDATE를 하나의 `@Transactional` 메서드로
     묶어 원자적으로 실행한다(`cancelOrder()`와 동일 패턴). 외부 API 실패 시 DB는 건드리지 않고 즉시
     실패 응답. 외부 API는 성공했는데 DB 업데이트만 실패하는 극단 케이스는 오늘 범위에서 자동 보정 없이
     로그만 남기고 수동 확인 — 자동 보정(재시도/보상 트랜잭션)은 별도 TODO로 분리한다.
  4) **중복 환불 방지**: 별도 Idempotency-Key 인프라를 두지 않고, `payment_status` 상태 체크만으로
     막는다 — 환불 실행 전 `payment_status`가 `APPROVED`가 아니면(이미 `REFUNDED` 등) 즉시
     `ORDER_REFUND_NOT_ALLOWED`(409). 상태 자체가 멱등성을 보장하므로 키오스크 결제(TODO-211)의
     별도 idempotency key 테이블과는 다른 방식으로 간다.
  5) 0건 반환을 성공으로 감추지 말 것 — 행 수 0 / 허용 안 되는 상태 / 동시 변경을 ErrorCode로 구분.
  6) **(2026-08-25 결정)** 환불 대상 결제수단 범위: **카드/신용카드**는 반영한다. **토스페이**는 API를
     확인한 상태이며, 실제 연동과 결제 과정 통합 테스트가 성공할 때만 프로젝트 범위에 포함한다.
  ```
- [~] **TODO-039** 환불 SQL 분리 (ASAK-back) — `AdminPaymentMapper`에 `markPaymentRefunded` / `insertPaymentRefund` / `cancelOrderForRefund` 초안 존재. COMPLETED는 주문 유지·그 외만 CANCELED. **미검증** · INSERT 파라미터명 불일치 가능(`구현 불일치`)
  ```
  `src/main/resources/mappers/AdminPaymentMapper.xml`
  ```
- [~] **TODO-038** `PATCH /api/admin/orders/{orderId}/refund` Controller (ASAK-back) — Controller·`OrderRefundRequest`·Service·가상 cardRefund 초안 존재. 실PG·HTTP 검증 대기. `providerPaymentKey` SELECT 누락(`구현 불일치`)
  ```
  `AdminOrderController.refundOrder` → `AdminOrderService.refundOrder` → `PaymentService.cardRefund` → `AdminRefundTransactionService.applyRefund`
  body `{ refundReason }`. CARD만. 성공 data = `OrderDetailResponse` 재조회.
  ```

- [~] **TODO-040** `ordersApi.orderRefund` (ASAK-Admin) — path만 PATCH·**body 없음** → 백엔드 `@NotBlank refundReason`과 **계약 불일치**. 응답/ErrorCode 검증 대기
  `src/api/ordersApi.js` — **cancel API를 환불에 재사용하지 않는다.**

- [~] **TODO-042** `OrderManagePage.jsx`의 `handleRefund` 연결 (ASAK-Admin) — ConfirmDialog → `ordersApi.orderRefund(orderId)` 연결됨. refundReason 입력·409 구분·통합 검증 대기
      `src/pages/admin/OrderManagePage.jsx`
- [ ] **검증**: 승인 결제 환불 성공, 미승인 주문 환불 시도(차단), 중복 환불 시도(409), cancel과 refund가
      같은 주문에 동시에 안 걸리는지 확인.

---

## 작업 횡단 — Admin·Backend·RTOS 콘솔 통합 테스트와 DevCopilot 최신화

- [ ] **통합 테스트**: Admin 화면 요청 → Spring API → `DeviceGateway` → `ConsoleRtosGateway` → RTOS 콘솔 출력의
  ```
  한 경로를 실제로 확인한다. Admin 화면만, DB row만, 콘솔 로그만 확인한 결과는 통합 테스트 통과로 기록하지 않는다.
  ```
- [ ] **DevCopilot 최신화**: 위에서 확정되거나 실제로 검증된 API·화면·QA 근거만 DevCopilot workspace에 반영한다.
  ```
  계획·mock·미검증 통합 테스트는 구현 완료로 동기화하지 않는다.
  ```

---

## 오늘 범위 밖 (참고만)

- 키오스크 결제 훅(`usePayment.js`, WBS2-026) + 주문생성/결제 통합 — 백엔드(`UserPayController`/
  `UserPayService`)는 이미 완성돼 있어 프런트 배선만 남음. 고객화면이라 오늘 제외.
- 품절 재검증/결제 차단(`soldOutPolicy.js`) — 고객화면이라 오늘 제외.
- 장바구니 항목 옵션 수정(`CartItem.jsx`) — 고객화면이라 오늘 제외.
- 환불 관련 백엔드 트랜잭션/타임스탬프 이슈는 `docs/ai-reports/2026-08-21/order-refund-timestamp-gap.md`
  참고.
- RTOS 이벤트 DB 추가 — 오늘 범위 아님, 현재 작업 진행 상황 따라 차후 결정.
