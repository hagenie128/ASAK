# API-008 상태 변경 경로 문서 동기화

- 일자: 2026-07-30
- 범위: 로컬 문서와 Bruno 컬렉션만 수정. Java/React 소스, DevCopilot 웹 기록, Git 작업은 제외.

## 확정 계약

```http
PATCH /api/admin/orders/{orderId}/{status}
```

- Path: `orderId`, `status`
- 현재 구현이 허용하는 목표 `status`: `PREPARING`, `COMPLETED`
- Request body: 없음
- 성공 응답: `ADMIN_ORDER_STATUS_CHANGE_SUCCESS`, `data: null`

## 코드 근거

- `ASAK-back/src/main/java/com/asak/admin/controller/AdminOrderController.java`의 `@PatchMapping("/{orderId}/{status}")`
- `AdminOrderService.changeOrderStatus(...)`는 `PREPARING`, `COMPLETED`만 처리한다.
- `ApiResponse.success(...)` 호출은 성공 code/message와 `null` data를 반환한다.

## 반영 파일

- ASAK 정본/API/화면 문서: API-008 경로, 요청 위치, 성공 응답
- ASAK-Admin API 연동 문서: path parameter 표기
- ASAK-back 구현 계획/가이드/참조 HTML: API-008 경로와 구현 상태
- `ASAK-back/api/admin/04-order-status.bru`: path variable `status`, body 없음, 구현 상태

## 남은 확인 사항

- 일부 문서는 `RECEIVED → PREPARING → COMPLETED`만 허용한다고 서술하지만, 현재 서비스 구현은 이전 상태를 별도로 검증하지 않아 `RECEIVED → COMPLETED`도 통과할 수 있다. 정책 확정 뒤 서비스 로직 또는 문서를 별도 정합화해야 한다.
- `AdminOrderController`의 소스 주석에는 이전 `/status` 경로가 남아 있다. 이번 범위는 문서·Bruno만이므로 소스 주석은 수정하지 않았다.
- Bruno 실서버 호출 및 Spring 통합 테스트는 실행하지 않았다.
