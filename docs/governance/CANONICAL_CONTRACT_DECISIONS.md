# 정본(Canonical) 계약 결정

> 상태: 현재 — 2026-07-16 사람 결정 확정. 이 문서는 문서 계약만 선언하며, 이 단계에서 소스 변경을 승인하지 않습니다.

## 저장소 소유권

- `ASAK-Admin`이 관리자 구현의 정본(Canonical) 저장소입니다.
- `ASAK-Kiosk` 내부의 관리자 페이지/컴포넌트/API 스캐폴드는 **레거시 참조(Legacy Reference)** 및 중복 검토 자산입니다. 삭제·이동하거나 관리자 구현의 단일 진실 소스(Single Source of Truth)로 사용하지 마세요.
- Product Bible은 `ASAK/docs/product_bible`에 유지합니다. `product-bible`로 이름을 바꾸지 마세요.

## 정본(Canonical) API 경로

```text
GET   /api/kiosk/menuList
GET   /api/kiosk/menuDetail/{menuId}
POST  /api/kiosk/orders
POST  /api/kiosk/payments
PATCH /api/admin/soldOut
```

URL 및 API 경로는 camelCase를 사용합니다. 이 문서화 단계에서는 기존 상수를 변경하지 않습니다.

## 정본(Canonical) Admin 라우트

```text
/
/orders/live
/orders
/soldOut
/menus
/paymentMethods
/sales
/sales/monthly
/sales/daily
```

## 정본(Canonical) 응답 필드 및 어댑터 규칙

정본 API 필드는 `totalAmount`, `approvedAmount`, `approvedAt`, `waitingOrderCount`입니다.

기존 Kiosk 스토어 필드 `totalPrice`, `amount`, `paidAt`은 지금 이름을 바꾸지 않습니다. 향후 API 어댑터가 경계(boundary)에서 정본 응답 필드를 매핑하여, 기존 import 및 스토어 소비자를 보존합니다.

## Mock 데이터

다음은 MVP 데모 데이터(MVP Demo Data) 소스 자산이며, 향후 형태/무결성 업데이트 전까지 그대로 둡니다.

- `ASAK-Kiosk/public/mocks/kiosk.json`
- `ASAK-Admin/public/mocks/asak-admin-data.json`

향후 mock 수정 시 정본 API 응답 형태와 일치해야 하며, 매출 KPI/차트/테이블 합계 및 비율을 일관되게 유지해야 합니다.
