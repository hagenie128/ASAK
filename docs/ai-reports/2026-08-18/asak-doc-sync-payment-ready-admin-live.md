## 대상 저장소와 기준

- 문서 저장소: `ASAK`
- 구현 근거 저장소: `ASAK-back`, `ASAK-Admin`
- 기준 커밋:
  - `ASAK-back`: `1f2d886`
  - `ASAK-Admin`: 작업 트리 기준 미커밋 변경 포함

## 확인한 근거

- Backend
  - `ASAK-back/src/main/java/com/asak/common/enums/OrderStatus.java`
  - `ASAK-back/src/main/java/com/asak/user/dto/order/response/CreateOrderResponse.java`
  - `ASAK-back/src/main/java/com/asak/user/dto/payment/ApprovePaymentRequest.java`
  - `ASAK-back/src/main/java/com/asak/user/dto/payment/ApprovePaymentResponse.java`
  - `ASAK-back/src/main/java/com/asak/user/service/UserOrderService.java`
  - `ASAK-back/src/main/java/com/asak/user/service/UserPayService.java`
  - `ASAK-back/src/main/resources/mappers/UserPayMapper.xml`
  - `ASAK-back/api/kiosk/04-create-order.bru`
  - `ASAK-back/api/kiosk/06-start-payment.bru`
- Admin UI
  - `ASAK-Admin/src/components/admin/LiveOrderBoard.jsx`
  - `ASAK-Admin/src/components/admin/orders/OrderStatusBadge.jsx`
  - `ASAK-Admin/src/components/admin/DashboardPanels.jsx`
  - `ASAK-Admin/src/constants/orderLabels.js`

## 갱신한 문서

- `docs/wiki/rest-api-spec.md`
- `docs/wiki/screen-design-figma.md`
- `docs/screens/screens.md`
- `docs/implementation_guide/02-kiosk-implementation.md`
- `docs/ai-reports/2026-08-18/asak-doc-sync-payment-ready-admin-live.md`

## 반영 내용

1. `API-005`는 성공 응답에 `paymentStatus`를 두지 않고 `status=READY`를 사용하도록 유지했다.
2. `API-006` 요청은 `orderId`, `orderStatus(=READY)`, `paymentMethodCode`, `idempotencyKey`이고, 성공 응답은 `paymentStatus`, `approvedAmount`, `approvedAt`, `waitingOrderCount`를 포함하도록 정리했다.
3. 주문 상태 코드 표에 `READY`를 포함한 현재 구현 상태를 유지했다.
4. 관리자 라이브 보드(SCR-009)는 `READY` 주문을 `대기중`으로 표시하고 준비 시작 버튼을 비활성화하는 현재 UI 동작을 문서에 반영했다.

## 검증 결과

- Backend: `ASAK-back`에서 `.\gradlew.bat test` 성공
- Admin UI: 수정 파일 대상 lint 확인 성공
- 문서: 코드 근거 기준으로 필드명과 상태값 수기 대조

## 남은 불일치 / 결정 필요

- `READY`가 주문 상태와 결제 상태에 모두 존재한다. 의미 분리를 유지할지 용어를 재정리할지 결정 필요.
- `API-005` 응답 필드명이 `status`이고 목록/상세는 `orderStatus`다. 생성 응답도 `orderStatus`로 통일할지 결정 필요.
- Admin 상태 전이 규칙은 여전히 `RECEIVED → PREPARING → COMPLETED` 기준 문서가 여러 곳에 남아 있다. 이번 범위에서는 관련 화면/위키만 최소 수정했다.

## 수정하지 않은 범위

- Product Bible 전반
- QA 시나리오 상세 절차
- DevCopilot/Notion 원격 데이터
