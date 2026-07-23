# DevCopilot API 정리 기준 (2026-07-23)

## 목적

DevCopilot API 명세를 현재 ASAK 정본 경로와 요구사항 ID로 통일한다. 이 문서는 외부 도구에서 레거시 항목을 갱신하거나 제거할 때의 추적표이며, 구현 코드나 DB 스키마를 변경하지 않는다.

## 유지·갱신할 API 레코드

| DevCopilot 레코드 | 정본 API | 요구사항 ID |
| --- | --- | --- |
| 208 | `GET /api/kiosk/menuList` | FWD-MENU-001 |
| 209 | `GET /api/kiosk/menuDetail/{menuId}` | DEV-MENU-001 |
| 83 | `POST /api/kiosk/cart/validate` | DEV-CART-001 |
| 210 | `POST /api/kiosk/orders` | DEV-ORDER-001 |
| 211 | `POST /api/kiosk/payments` | DEV-PAY-001 |
| 80 | `GET /api/kiosk/payment-methods` | FWD-PAY-001 |
| 71, 72, 74, 75 | 관리자 활성 주문·상세·목록·상태 변경 | LMIS-ORDER-001/002/003 |
| 77, 212 | 관리자 품절 목록·변경 | LMIS-MENU-001 |
| 69, 76, 78, 79 | 관리자 메뉴 상세·수정·목록·등록 | LMIS-MENU-004 |
| 68, 81 | 관리자 결제수단 조회·설정 변경 | LMIS-PAY-001 |
| 82, 84, 213, 214 | 관리자 일별·대시보드·요약·월별 매출 | LMIS-ORDER-005, LMIS-DASH-001 |

## 제거 대상

다음은 이전 `/api/menus`, `/api/orders`, `/api/payments`, `/api/v1/**` 또는 제외 범위 API이므로 DevCopilot에서 제거한다. 정본에서 필요할 경우 위 유지 목록의 경로로만 다시 정의한다.

`70`, `73`, `85`, `86`, `87`, `120`–`138`

## 공통 규칙

- 제목 형식: `API-번호 기능명 (요구사항-ID)`
- 응답: `{ success, status, code, message, data }`
- Java/JSON: `categoryId`, `totalAmount`, `approvedAmount`, `approvedAt`, `isSoldOut`
- DB 매핑: `menu.cat_id`, `orders.total_price`, `payment.amount`, `payment.paid_at`을 사용한다.
- 카테고리 코드는 현재 DB에 없으므로 API 계약에 `categoryCode`를 쓰지 않는다.
