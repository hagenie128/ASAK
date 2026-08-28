# 2026-08-24 Admin 작업 계획 (고객화면 제외)

> **최종 재점검: 2026-08-28** — `ASAK-back` **main**, `ASAK-Admin` **main** 기준.
> 원본 계획일(2026-08-24)과 2026-08-25 teacher 협의 결정은 유지한다. 아래 `[x]`는 **코드 연결 완료**, `[ ]`는 **런타임·Bruno·브라우저·DB 검증 미완**을 뜻한다.

기준 시점: 2026-08-24. 당일 범위는 **고객 화면(ASAK-Kiosk) 제외**, 관리자 결제수단·로그인·주문/환불.
키오스크 결제 훅·품절 재검증·장바구니 옵션 수정은 이 문서 범위 밖 — 별도 세션.

RTOS 이벤트 DB 추가는 당일 범위 아님 — 현재 작업 진행 상황에 따라 차후 처리.

---

## 2026-08-28 코드 재점검 요약

| 영역 | 코드(main) | 검증 | 비고 |
|---|---|---|---|
| 결제수단 API·FE | **연결됨** | 미완 | Mapper `ORDER BY sort_no, id` **누락** |
| 로그인 API·FE | **연결됨** | 미완 | JWT/계정 인증 없음(의도). `LoginPage` 파일 헤더 주석 구식 |
| 환불 API | **main 미구현** | — | `feat/admin-refund-history`에만 초안 |
| 환불 FE | **호출 연결됨** | 미완 | `refundReason` body·사유 입력 UI 없음 → **계약 불일치** |
| 주문/Live/취소 | **연결됨** | 미완 | todo 범위 밖이나 main에 존재 |
| 품절 | **연결됨** | 미완 | `soldOutApi` + `AdminSoldOutController` |
| 매출/대시보드 | **연결됨** | 미완 | `AdminSalesController` + `salesApi`/`useDashboard` |
| 영수증/device-events | **연결됨** | 미완 | `AdminDeviceEventController`, FE `printReceipt` |

**경로 정렬:** `VITE_API_BASE_URL=/api` + `API_BASE_PATH=/admin` → 실제 호출 `/api/admin/...`로 Backend와 일치. 문서·주석의 “경로 불일치” 표기는 **구식** — 런타임 검증만 남음.

**환불 브랜치:** `ASAK-back` `feat/admin-refund-history`에 `PATCH .../refund`, `OrderRefundRequest(refundReason)`, Service/SQL 초안 존재. **main 미머지.** 리뷰 이슈는 `docs/ai-reports/2026-08-26/refund-virtual-card-approval-review.md` 참고.

---

## 2026-08-25 업데이트 (teacher 협의 결과, 유효)

1. **로그인 방식 변경**: 계정(아이디/비밀번호) 인증 대신 **매장 번호 '0001' 고정값 하드코드 승인**으로 확정. DB 조회·매장별 로그인 확장 없음. 세션도 **JWT 미사용, 단순 승인 플래그** — TODO-028(JwtTokenProvider) 불필요.
2. **환불 결제수단 범위**: **카드/신용카드**는 이번 프로젝트에 반영. **토스페이**는 API 확인 후 실제 연동·통합 테스트 성공 시만 포함.
3. **TODO-001 승인 결제 취소 정책 확정** — order_status는 `CANCELED` 재사용, payment_status만 `REFUNDED`로 구분. 외부 결제사 API 먼저 → 성공 시 DB 트랜잭션. 중복 환불은 `payment_status` 상태 체크.
4. 위 결정에 맞춰 관련 설계 문서도 함께 갱신할 것.

---

## 우선순위 1 — 관리자 결제수단 API

실행 순서가 곧 TODO 체인이다. 순서를 건너뛰면 다음 단계가 계약 불일치로 막힌다.

- [x] **TODO-011** `AdminPaymentMethodController` (ASAK-back) — **구현 완료 · 검증 대기**
  - `src/main/java/com/asak/admin/controller/AdminPaymentMethodController.java`
  - `GET /api/admin/paymentMethods`, `PATCH /{paymentMethodId}` — path variable만 사용.
  - 요청 DTO: `active`, `sortNo`만. `receiptMessage`는 API·DB 계약 없어 제외.
- [x] **TODO-012** `AdminPaymentMethodService` / Mapper / DTO (ASAK-back) — **구현 완료 · SQL/실 DB 검증 대기**
  - `AdminPaymentMethodService.java`, `AdminPaymentMethodMapper.xml`
  - 없는 id·null 필드·0건 갱신 → ErrorCode 구분 구현됨.
  - **갭:** `getPaymentMethods` SELECT에 `ORDER BY sort_no ASC, id ASC` **없음** — Service 주석과 불일치. 추가 후 Bruno/DB 확인.
- [x] **TODO-013** `paymentMethodsApi.js` (ASAK-Admin)
  - `src/api/paymentMethodsApi.js` — GET + PATCH, body `{ active, sortNo }`.
- [x] **TODO-014** `usePaymentMethodDraft.js` 훅 연결 (ASAK-Admin)
  - mock → `paymentMethodsApi` 교체 완료. 순서 변경은 **개별 PATCH 순차 호출**. 실패 시 `baselineRows` 롤백 유지.
- [ ] **검증**: 토글/정렬 저장 후 재조회, 없는 id, 유효하지 않은 요청, 0건 갱신, ORDER BY 정렬을 API·DB row로 확인.

---

## 우선순위 2 — 로그인: 매장 번호 승인 방식

기존 username/password + JWT 설계는 **2026-08-25 결정으로 폐기**. main 코드는 새 계약으로 구현됨.

- [x] **설계 확정 (2026-08-25)** — 매장 번호 **'0001' 하드코드**, 세션 **단순 승인 플래그**. JWT·DB 매장 조회 없음.
- [x] **TODO-027** `AdminAuthController` (ASAK-back) — **구현 완료 · 검증 대기**
  - `POST /api/admin/login` — body `{ storeNumber }`.
  - `"0001"` → `{ approved: true }`. 빈 값·불일치 → `INVALID_STORE_NUMBER` / `NOT_APPROVED_STORE_NUMBER`.
- [x] **TODO-031~034** (ASAK-Admin) — **코드 연결 완료 · 검증 대기**
  - `adminApi.login` → `LoginPage.jsx` → `loginAdmin({ remember })`.
  - `adminSession.js` — `loggedIn` 플래그 유지, JWT 저장 없음.
  - **갭:** `LoginPage.jsx` 파일 헤더가 여전히 “인증 API 없음” — 주석 갱신 필요.
  - **갭:** `apiClient.js` TODO-033(JWT Authorization) 주석 잔존 — 이번 범위 불필요.
- [ ] **검증**: 정상 `'0001'` 승인, 잘못된 매장 번호, 빈 입력, 네트워크 오류를 실제 API 응답으로 확인.

---

## 우선순위 3 — 주문/환불

환불은 설계 결정(TODO-001) 후 구현. **2026-08-25 정책 확정 완료.**

- [x] **TODO-001** 승인 결제 취소 정책 확정 (ASAK-back)
  - `AdminOrderService.cancelOrder` — `paymentStatus == APPROVED`면 cancel 차단, refund만 허용.
  - 환불 성공 후 order_status `CANCELED` 재사용, payment_status `REFUNDED`.
  - 외부 결제 API → 성공 시 DB `@Transactional`. 중복 환불은 `payment_status` 체크(409).
  - 카드/신용카드 반영. 토스페이는 통합 테스트 성공 시만.
- [ ] **TODO-039** 환불 SQL (ASAK-back) — **main 없음 · branch 초안**
  - `feat/admin-refund-history`: `AdminPaymentMapper` — `markPaymentRefunded` / `insertPaymentRefund` / `cancelOrderForRefund`.
  - INSERT 파라미터명·컬럼 불일치 가능. **main 머지 전 SQL 대조 필수.**
- [ ] **TODO-038** `PATCH /api/admin/orders/{orderId}/refund` (ASAK-back) — **main 없음 · branch 초안**
  - main `AdminOrderController`: TODO-038 **주석만** (endpoint 미구현).
  - branch: `@Valid OrderRefundRequest` — `@NotBlank refundReason`.
  - 가상 `cardRefund` 초안. 실PG·HTTP·DB 통합 검증 대기.
- [~] **TODO-040** `ordersApi.orderRefund` (ASAK-Admin) — **경로 연결 · body 계약 불일치**
  - `src/api/ordersApi.js` — `PATCH` **body 없음**.
  - Backend(branch)는 `{ refundReason }` 필수 → **400 예상**. body 추가 + ErrorCode 매핑 필요.
- [~] **TODO-042** `OrderManagePage.handleRefund` (ASAK-Admin) — **ConfirmDialog 연결 · 사유 입력 없음**
  - `ordersApi.orderRefund(orderId)` 호출됨. refundReason 입력 UI·409/이미 환불됨 분기·처리 중 disabled 미완.
  - 성공 후 `printReceipt` + `refund` — 영수증 출력과 환불 흐름 분리 검토 필요.
- [ ] **검증**: 승인 결제 환불 성공, 미승인 차단, 중복 환불(409), cancel/refund 동시 불가, `refundReason` body, 브라우저 E2E.

**환불 착수 순서 (main 기준):**

1. `feat/admin-refund-history` 리뷰·머지 (또는 main에 동일 계약 재구현)
2. FE `orderRefund(orderId, { refundReason })` + 사유 입력 UI
3. 가상 카드 취소 규칙 확정 → Bruno → 브라우저

---

## 작업 횡단 — 통합 테스트와 DevCopilot

- [ ] **통합 테스트**: Admin 화면 → Spring API → (환불 시) 가상 PG → DB row. Admin만·콘솔만 확인은 통과로 기록하지 않음.
- [ ] **DevCopilot 최신화**: 위에서 **실제 검증된** API·화면·QA 근거만 반영. mock·미검증·branch-only는 DONE 동기화 금지.

---

## 범위 밖이지만 main 코드 연결됨 (2026-08-28)

이 문서 작성 당시 “오늘 범위 밖”이었으나, 이후 main에 FE↔BE 연결까지 진행된 항목. **검증은 별도.**

| 기능 | Backend | Frontend | 상태 |
|---|---|---|---|
| 주문 목록/상세/상태/취소 | `AdminOrderController` | `ordersApi`, `OrderManagePage` | 코드 연결 · E2E 미완 |
| Live 주문 | `GET .../orders/live` | `LiveOrderBoard` | 동일 |
| 품절 | `AdminSoldOutController` | `soldOutApi`, `useSoldOutDraft` | 동일 |
| 매출 summary/monthly/daily/time-slots | `AdminSalesController` | `salesApi`, `useSalesQuery` | 동일 · `DailySalesPage` mock hourly 폴백 잔존 가능 |
| 대시보드 | `GET /api/admin/dashboard` | `adminApi.getDashboard`, `useDashboard` | 동일 · 성능 실측 별도 |
| 영수증 재출력 | `AdminDeviceEventController` | `ordersApi.printReceipt` | 동일 · RTOS 장치 검증 별도 |
| 메뉴 CRUD | `AdminMenuController` | `menusApi`, `useMenusQuery` | 재료 모달 stub 잔존 가능 |

---

## 오늘 범위 밖 (참고만, 2026-08-24 기준 유지)

- 키오스크 결제 훅(`usePayment.js`, WBS2-026) + 주문생성/결제 통합 — 고객화면.
- 품절 재검증/결제 차단(`soldOutPolicy.js`) — 고객화면.
- 장바구니 항목 옵션 수정(`CartItem.jsx`) — 고객화면.
- 환불 트랜잭션/타임스탬프 — `docs/ai-reports/2026-08-21/order-refund-timestamp-gap.md`.
- RTOS 이벤트 DB 추가 — 차후.

---

## 알려진 갭 · 후속 TODO

1. **결제수단 Mapper** — `ORDER BY sort_no ASC, id ASC` 추가.
2. **환불** — main 머지, FE `refundReason`, 사유 UI, 트랜잭션 경계(외부 API 밖) 재검토.
3. **주석 정리** — `LoginPage` 헤더, `api.js`/`paymentMethodsApi.js` 경로 불일치 문구, `STRUCTURE_GUIDE.md` mock 표.
4. **문서 vs 코드** — `admin-api-contract.md`, Bruno, Hub/WBS를 “코드 연결 / 검증 완료” 2단계로 구분.

---

## 관련 문서

- 환불 검토: `docs/ai-reports/2026-08-26/refund-virtual-card-approval-review.md`
- 환불 Hub: `docs/ai-reports/2026-08-26/asak-doc-sync-payment-refund-hub.md`
- 로그인·환불 착수 순서: `docs/ai-reports/2026-08-25/admin-login-refund-implementation-order.md`
- 영수증 아키텍처: `docs/planning/receipt-digital-delivery-architecture-2026-08-24.md`
