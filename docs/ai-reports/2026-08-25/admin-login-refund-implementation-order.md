# 관리자 로그인·환불 정책 확정 및 구현 순서 (2026-08-25)

> 오늘 teacher와 협의로 확정된 결정 요약 + 구현 순서.
> 상세 TODO 원본: [`../../planning/admin-todo-2026-08-24.md`](../../planning/admin-todo-2026-08-24.md)
> (원본 문서가 실제 코드 재검증으로 이후 갱신됨 — 이 요약본도 그 내용에 맞춰 다시 동기화함)

## 오늘 확정된 결정

| 항목 | 결정 |
|---|---|
| 로그인 방식 | 매장 번호 '0001' 고정값 하드코드 승인 |
| 로그인 세션 | JWT 미사용, 단순 승인 플래그 |
| 환불 결제수단 | 카드/신용카드 확정. 토스페이는 연동+통합 테스트 성공 시 포함 |
| 환불 후 order_status | 기존 `CANCELED` 재사용 |
| 환불 후 payment_status | `REFUNDED`로 구분 |
| 환불 트랜잭션 순서 | 외부 결제사 API 먼저 → 성공 시 DB 처리 |
| 중복 환불 방지 | `payment_status` 상태 체크만 사용 |

문서 반영 완료:
- `docs/planning/admin-todo-2026-08-24.md`
- `docs/planning/README.md`
- `docs/wiki/rest-api-spec.md`
- `docs/product_bible/07_Screen_Bible/SCR-015-ADMIN-LOGIN.md`
- `docs/wiki/qa-test-cases.md` (TC-009)

코드 변경은 아직 없음. 아래 순서대로 구현하면 된다.

---

## 1단계 — 결제수단 mock → API 연결

의존성 없음, 바로 시작 가능.

**현재 실제 상태** (`admin-todo-2026-08-24.md` 재검증 반영)
- `AdminPaymentMethodController`(ASAK-back): GET/PATCH 매핑 골격 존재, 런타임 미검증
- 요청 DTO는 `active`, `sortNo`만 있음 — `receiptMessage`는 API·DB 계약 자체가 없어 이번 범위에서 제외
- `AdminPaymentMethodService`/Mapper: 골격은 있으나 Mapper SQL에 `onF` 오타, 바인딩·검증 보완 필요
- 정렬은 한 행의 `sort_no`만 수정 — 여러 행 재정렬(409 충돌)은 이번 범위 아님

**`ASAK-Admin/src/api/paymentMethodsApi.js`**
- GET 목록 + `PATCH /{paymentMethodId}` 구현
- mock의 `isActive`/`sortOrder`와 API의 `active`/`sortNo` 필드명 차이는 adapter로 맞추거나 계약 통일 후 연결

**`ASAK-Admin/src/hooks/usePaymentMethodDraft.js`**
- 초기 load를 mock → `paymentMethodsApi.listPaymentMethods`로 교체
- 저장을 mock → `paymentMethodsApi.patchPaymentMethod`로 교체
- 화면의 순서 이동은 여러 행을 바꾸므로, 개별 PATCH 순차 호출 vs 일괄 저장 endpoint 중 하나를 먼저 계약으로 정할 것
- 실패 시 baselineRows 롤백 규칙은 그대로 유지

**검증**
- 토글/정렬 저장 후 재조회
- 존재하지 않는 id, 유효하지 않은 요청, 0건 갱신

---

## 2단계 — 로그인 (매장 번호 '0001')

**`ASAK-back/.../AdminAuthController.java`**
- `POST /api/admin/login`, body `{ storeNumber }`
- `storeNumber == "0001"` 하드코드 비교만 수행
- AuthenticationManager·DB 조회·JWT 발급 없음
- 불일치 시 401(또는 ErrorCode)
- 일치 시 `{ approved: true }` 형태 응답
- 기존 TODO-028(JwtTokenProvider)은 폐기

**`ASAK-Admin/src/api/adminApi.js`**
- `login()`을 위 API에 맞게 구현

**`ASAK-Admin/src/pages/admin/LoginPage.jsx`**
- 아이디/비밀번호 입력 폼 → 매장 번호 입력 하나로 교체
- `loginAdmin` mock 호출 → 실제 API 연결로 교체

**`ASAK-Admin/src/auth/adminSession.js`, `src/api/apiClient.js`**
- 토큰 저장·만료 판정 로직 추가 불필요
- 기존 `loggedIn` boolean 플래그 구조 그대로 재사용
- mock 호출 자리만 실제 API 응답으로 교체

**검증**
- 정상 '0001' 승인
- 잘못된 매장 번호
- 빈 입력

---

## 3단계 — 환불

정책은 위 표대로 확정됨. 순서를 반드시 지킬 것 —
순서를 건너뛰면 다음 단계가 계약 불일치로 막힌다.

**① `ASAK-back/.../mappers/AdminOrderMapper.xml`**
- cancel SQL과 분리한 UPDATE 2개 추가 (한 쿼리로 묶지 않음)
  - orders 취소: `status_id` → `CANCELED`
  - payment 환불: `payment_status` → `REFUNDED`
- 각 update는 의미 있는 행 수를 반환해야 함

**② `ASAK-back/.../AdminOrderController.java`**
- `PATCH /api/admin/orders/{orderId}/refund` 추가 (cancel과 분리된 엔드포인트)
- 실행 전 `payment_status != "APPROVED"`면 즉시 409 `ORDER_REFUND_NOT_ALLOWED`
- 외부 결제사(카드/토스페이) API 호출
- 성공 시에만 ①의 UPDATE 2개를 `@Transactional`로 원자 실행
- 실패 시 DB 미변경, 즉시 에러 응답
- 외부 성공 + DB 실패 극단 케이스: 오늘은 로그만, 자동 보정은 별도 TODO

**③ `ASAK-Admin/src/api/ordersApi.js`**
- 이미 `API_ENDPOINTS.orderRefund` + `orderRefund` 래퍼가 선언돼 있음 (구현 상태 재검증됨)
- TODO-038/039 검증 완료 후 화면의 mock 환불 호출을 이 래퍼로 교체
- cancel API 재사용 금지

**④ `ASAK-Admin/src/pages/admin/OrderManagePage.jsx`**
- `handleRefund`를 `ordersApi.orderRefund` + `ConfirmDialog`에 연결
- 승인 결제만 환불 가능 여부 확인
- 409/이미 환불됨 응답 구분 처리
- 성공 후 `refetch()`로 목록 갱신

**검증**
- 승인 결제 환불 성공
- 미승인 주문 환불 시도(차단)
- 중복 환불 시도(409)
- cancel과 refund 동시 미충돌

---

## 작업 횡단 (admin-todo에 추가된 항목)

- **Admin → Backend → RTOS 콘솔 통합 테스트**: Admin 화면 요청 → Spring API →
  `DeviceGateway` → `ConsoleRtosGateway` → RTOS 콘솔 출력까지 한 경로를 실제로 확인.
  Admin 화면만, DB row만, 콘솔 로그만 확인한 결과는 통과로 기록하지 않는다.
- **DevCopilot 최신화**: 확정되거나 실제로 검증된 API·화면·QA 근거만 반영한다.
  계획·mock·미검증 통합 테스트는 구현 완료로 동기화하지 않는다.

## 오늘 범위 밖 (참고만)

- 키오스크 결제 훅, 품절 재검증, 장바구니 옵션 수정 — 고객화면, 오늘 범위 아님
- 환불 트랜잭션/타임스탬프 이슈: `docs/ai-reports/2026-08-21/order-refund-timestamp-gap.md` 참고
