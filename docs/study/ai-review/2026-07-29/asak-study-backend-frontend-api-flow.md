# 백엔드·프론트 API 연동 학습 기록

- 날짜: 2026-07-29
- 스킬: `asak-study`
- 범위: ASAK-Admin 주문 조회, ASAK-Kiosk 메뉴·주문 API 준비 상태, ASAK-backend 주문 API

## 결론

실제 백엔드 DB 조회까지 연결된 화면은 Admin 주문 목록이다. 키오스크 메뉴 화면은 현재 `kiosk.json` 목업을 직접 사용하며, 주문 생성과 결제는 API 골격 또는 서버 검증 일부만 있는 미완성 상태다.

## 확인한 흐름

```text
Admin 주문 관리 화면
OrderManagementPreview
  -> useOrdersQuery
  -> ordersApi / apiClient
  -> GET /api/admin/orders
  -> Vite 5174 프록시
  -> AdminOrderController
  -> AdminOrderService
  -> AdminOrderMapper
  -> orders, payment, order_item, common_code
  -> ApiResponse<PageResult<OrderListResponse>>
  -> OrderTable
```

## 확인한 파일

- `ASAK-Admin/src/api/apiClient.js`: `/api` 기본 경로와 공통 응답 envelope 해제
- `ASAK-Admin/src/hooks/useOrdersQuery.js`: 필터·페이지 요청과 loading/empty/error 상태 관리
- `ASAK-Admin/src/components/admin/OrderTable.jsx`: 주문 목록과 오류·빈 상태 표시
- `ASAK-backend/src/main/java/com/asak/admin/controller/AdminOrderController.java`: 관리자 주문 목록·상세·활성 주문 API
- `ASAK-backend/src/main/java/com/asak/admin/service/AdminOrderService.java`: 빈 필터를 `null`로 변환하고 페이징 범위 제한
- `ASAK-backend/src/main/resources/mappers/AdminOrderMapper.xml`: DB snake_case를 API camelCase로 별칭 처리

## 계약과 상태

- Admin 목록의 DB `total_price`는 응답 `totalAmount`로 변환된다.
- Admin 프론트의 빈 필터값은 백엔드 Service에서 `null`로 처리된다.
- 키오스크 실제 화면은 `MenuListPage`, `MenuDetailPage`에서 `public/mocks/kiosk.json`을 직접 import한다.
- 키오스크 API 상수의 `/api/categories`, `/api/menus`, `/api/orders`는 백엔드의 `/api/kiosk/categories`, `/api/kiosk/menuList`, `/api/kiosk/orders`와 아직 일치하지 않는다.
- 키오스크 Vite 서버에는 `/api` 프록시가 없다.
- `UserOrderService.createOrder()`은 검증 후 현재 `null`을 반환하며 DB 주문 생성이 완성되지 않았다.
- `UserPayController`에는 결제 endpoint 메서드가 없다.

## 검증 근거

프론트 API 모듈·Vite 설정·Page/Hook/Component와 백엔드 Controller/Service/Mapper/DTO를 읽어 정적 호출 흐름을 대조했다. 소스코드, DB 데이터, 실행 중 서버 설정은 수정하지 않았다.

## 남은 위험과 다음 작업

- Admin 주문 목록의 500은 프론트 필터보다 실행 DB 조회 단계에서 확인해야 한다.
- 백엔드 `AdminOrderController.java`에는 이 학습 시점에 Git 미반영 변경이 있었으므로, 반영 전 담당자 확인이 필요하다.
- 키오스크 실제 API 연결은 경로·프록시·응답 필드를 함께 합의한 뒤 별도 승인 범위에서 진행한다.
