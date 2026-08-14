# API·DB 공통 규칙

> 화면별 URL·request·response는 이미 [Kiosk 기능 가이드](02-kiosk-implementation.md), [Admin 기능 가이드](03-admin-implementation.md)에 붙어 있다.
> 이 문서는 **여러 화면에서 공통으로 쓰는 처리 규칙만** 찾는 곳이다.

## 현재 연결 상태

| 사실 | 구현할 때의 처리 |
| --- | --- |
| Backend 실제 원격은 `nayeon0828/ASAK-backend`이며, Kiosk 메뉴/카테고리 조회·장바구니 검증과 Admin 메뉴/주문 조회는 코드 경로가 있다 | 각 endpoint는 Controller→Service→MyBatis Mapper까지 존재하지만, 실DB·Bruno 응답은 별도 검증 전이다. |
| 주문 생성은 validation 뒤 `null`을 반환하고, 결제·상태변경/취소·품절·결제수단·매출/대시보드 mapping은 없다 | Front는 이를 완료 API로 연결하지 않는다. 저장·응답 DTO·오류 응답·Bruno 검증까지 같은 세로 슬라이스에서 끝낸다. |
| API 계약은 `SPEC_ONLY`/Draft가 포함됨 | Backend 구현 시 원본 계약을 확정하고 Front adapter를 연결한다. |
| 기존 frontend mock 필드가 다름 | 기존 store를 한꺼번에 바꾸지 않고 API 경계에서 변환한다. |

## 모든 API에서 공통으로 처리할 것

### 응답을 화면에 넘기는 방식

```json
{"success": true, "status": 200, "code": "OK", "message": "OK", "data": {}}
```

- API client가 envelope를 한 번만 벗기고, 화면은 필요한 `data`만 받는다.
- 실패 때도 `status`, `code`, `message`, `data`를 버리지 않는다.
- Entity를 그대로 JSON으로 반환하지 않는다. Controller는 DTO validation, Service는 가격·품절·상태 전이·멱등성을 맡는다.

### 오류별 공통 행동

| 상황 | 화면 행동 |
| --- | --- |
| `401` | 로그인/세션 만료를 안내한다. |
| `403` | 권한 없음을 알리고 무의미한 재시도는 숨긴다. |
| `409` | 최신 데이터를 다시 받고 충돌·가격 변경을 안내한다. |
| network / `5xx` | 입력값·필터·장바구니를 남기고 재시도한다. |
| `MENU_SOLD_OUT`, `OPTION_ITEM_SOLD_OUT` | 해당 항목만 표시하고 수정·삭제로 복구한다. |
| `PAYMENT_IN_PROGRESS`, `PAYMENT_ALREADY_APPROVED` | 결제를 다시 만들지 말고 현재 결과를 조회한다. |

### 기존 mock과 목표 API를 연결하는 이름

| 목표 API | 기존 mock/store에서 보일 수 있는 값 | 경계에서 맞출 이름 |
| --- | --- | --- |
| `menuName` | `name` | `menuName` |
| `basePrice` | `price` | `basePrice` |
| `calories` | `baseKcal` | `calories` |
| `additionalAmount` | `extraPrice` | `additionalAmount` |
| `totalAmount` | `totalPrice` | 기존 store에는 `totalPrice` 유지 가능 |
| `approvedAmount` | `amount` | 기존 결제 상태에는 `amount` 유지 가능 |
| `approvedAt` | `paidAt` | 기존 결제 상태에는 `paidAt` 유지 가능 |

<details>
<summary>원본 API 계약이 필요할 때만 열기</summary>

- [Canonical Contract Decisions](../governance/canonical-contract-decisions-2026-07-16.md)
- [Kiosk Frontend Data Contract](../../../ASAK-Kiosk/src/contracts/api-data-contract.md)
- [Menu API Contract](../product_bible/03_Menu_Inventory_SoldOut/MENU_BIBLE.md)
- [Order API Contract](../product_bible/02_Order_Cart_Payment/ORDER_BIBLE.md)
- [Payment API Contract](../product_bible/02_Order_Cart_Payment/PAYMENT_BIBLE.md)
- [Menu Management API Contract](../product_bible/03_Menu_Inventory_SoldOut/MENU_MANAGEMENT_BIBLE.md)
- [Sales API Contract](../product_bible/04_Dashboard_Sales_Kitchen_TTS/SALES_BIBLE.md)
</details>
