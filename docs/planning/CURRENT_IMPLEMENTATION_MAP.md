# Current Implementation Map

> 사람 결정, 2026-07-16: canonical API/route/response 필드는 [Canonical Contract Decisions](../governance/CANONICAL_CONTRACT_DECISIONS.md)에 있습니다. 코드는 변경하지 않았습니다. `DECIDED_PENDING_CODE_CHANGE`는 목표가 확정됐으나 소스 변경은 연기됨을 뜻하고, `DECIDED_NOT_IMPLEMENTED`는 adapter 결정은 확정됐으나 의도적으로 미구현임을 뜻합니다.

## Decision status overlay

| Prior conflict | Updated status | Decided canonical target |
|---|---|---|
| Kiosk menu/order/payment paths | DECIDED_PENDING_CODE_CHANGE | `/api/kiosk/menuList`, `/api/kiosk/menuDetail/{menuId}`, `/api/kiosk/orders`, `/api/kiosk/payments` |
| Admin Dashboard/Live Order/Sold-out/Payment routes | DECIDED_PENDING_CODE_CHANGE | `/`, `/orders/live`, `/soldOut`, `/paymentMethods` |
| Store field versus API fields | DECIDED_NOT_IMPLEMENTED | adapter가 canonical field 매핑; `totalPrice`, `amount`, `paidAt` 유지 |
| Admin implementation ownership | DECIDED_NOT_IMPLEMENTED | ASAK-Admin; Kiosk Admin scaffold는 Legacy Reference |

> 2026-07-16 코드 정적 조사 및 Kiosk/Admin production build 기준. 상태: `IMPLEMENTED`, `PARTIAL`, `MOCK_ONLY`, `MISSING`, `CONFLICT`, `FUTURE_SCOPE`.

## 화면과 라우트

| 문서 화면 | 실제 경로/파일 | 상태 | 근거 |
|---|---|---|---|
| SCR-001 Home | Kiosk `HomePage`, `/` | PARTIAL | 주문 유형 선택과 `/menu` 이동만 연결 |
| SCR-003 Menu List | `MenuListPage`, `/menu` | MOCK_ONLY | `public/mocks/kiosk.json`으로 카테고리/메뉴 표시 |
| SCR-004 Menu Detail | `MenuDetailPage`, `/menu/:menuId` | PARTIAL | 라우트·파라미터·store import만 있고 UI/검증/추가 미완성 |
| SCR-005 Cart | `CartPage.jsx` | MISSING | 파일은 빈 스캐폴드, 라우트 없음 |
| SCR-007 Payment | `PaymentPage.jsx` | MISSING | 파일은 빈 스캐폴드, 라우트 없음 |
| SCR-008 Complete | `OrderCompletePage.jsx` | MISSING | 파일은 빈 스캐폴드, 라우트 없음 |
| SCR-012 Payment Error | 없음 | MISSING | paymentError state만 존재 |
| SCR-013 Timeout | `useKioskTimeout.js` 자리만 존재 | PARTIAL | 앱 연결·overlay·reset 흐름 없음 |
| SCR-014 Accessibility | `AccessibilityPage.jsx` | MISSING | 빈 스캐폴드, 라우트 없음 |
| SCR-015 Admin Login | `LoginPage.jsx` | MISSING | 빈 스캐폴드, 라우트 없음 |
| SCR-022 Dashboard | Admin `/` | CONFLICT | `AdminApp`이 SCR-009 라벨/placeholder를 `/`에 사용 |
| SCR-009 Live Order | Admin `/` | CONFLICT | 문서는 `/orders/live`; 실제는 `/` placeholder |
| SCR-010 Order Management | `OrderList/DetailPage` | MISSING | 페이지 파일은 placeholder, 라우트 없음 |
| SCR-011 Sold-out | Admin `/sold-out` | CONFLICT | 문서 canonical route는 `/soldOut`; 컴포넌트/페이지는 placeholder |
| SCR-016 Menu Management | Admin `/menus` | PARTIAL | route placeholder만 존재; 관리 페이지 파일은 미연결 |
| SCR-018 Payment Settings | Admin `/payment-methods` | CONFLICT | 문서는 `/paymentMethods`; 실제 placeholder route는 kebab-case |
| SCR-019 Sales Summary | Admin `/sales` | PARTIAL | route placeholder, SalesChart/page 파일은 placeholder |
| SCR-020/021 Monthly/Daily | 없음 | MISSING | 문서 route 미구현 |

## Kiosk 보존·재사용 자산

| 분류 | 파일/역할 | 상태 | 처리 |
|---|---|---|---|
| 앱/라우터 | `apps/kiosk/KioskApp.jsx`, `entries/kiosk.jsx` | PARTIAL | 기존 세 route를 확장 |
| 메뉴 UI | `MenuCard`, `CategoryTabs`, `Header` | PARTIAL | 메뉴 조회 adapter와 상태만 보강 |
| 상세 UI | `MenuDetailSummary`, `OptionItem`, `OptionGroup` | PARTIAL | props/렌더링 결함 보정 후 재사용 |
| 주문 상태 | `orderSessionStore.js` | PARTIAL | 단일 session 방향은 유지, cart item identity/총액/검증 추가 |
| 호환 exports | `cartStore.js`, `orderStore.js` | IMPLEMENTED | 기존 import 호환성 보존 |
| API client | `api/client.js`, `unwrapResponse` | PARTIAL | envelope 처리 재사용, canonical endpoint로 통일 필요 |
| API modules | menu/category/order/payment | PARTIAL | 함수 골격은 있으나 현재 API와 미연결 |
| Mock | `public/mocks/kiosk.json` | MOCK_ONLY | 메뉴 목록 데모 자산으로 유지 |
| styles | `styles/*.css` | IMPLEMENTED | CSS 방식 유지 |

## Admin 인벤토리

| 분류 | 파일/역할 | 상태 |
|---|---|---|
| 앱 | `apps/AdminApp.jsx` | PARTIAL/CONFLICT |
| shell | `layouts/AdminLayout.jsx`, `components/admin/AdminSidebar.jsx` | MISSING |
| pages | Login, Menu, Order, SoldOut, PaymentMethod, Sales | MISSING (placeholder) |
| components | OrderTable, OrderStatusBadge, SoldOutToggle, SalesChart | MISSING (placeholder) |
| store/hook | `adminSessionStore.js`, `useAdminAuth.js` | MISSING (placeholder) |
| API | `api/client.js` | PARTIAL; `admin.js`, `sales.js`, constants | MISSING (placeholder) |
| mock | `public/mocks/asak-admin-data.json` | MOCK_ONLY; 실제 화면 미사용 |

## Backend 및 DB

| 계층 | 실제 파일 | 상태 | 비고 |
|---|---|---|---|
| Bootstrap | `AsakBackendApplication` | IMPLEMENTED | Spring Boot 4.1.0 / Java 25 |
| Controller | `HealthController` (`GET /api/health`) | IMPLEMENTED | 유일한 business endpoint |
| DTO | `ApiResponse` | PARTIAL | 성공 factory만 있고 오류/validation/exception 정책 미구현 |
| Service/Repository/Entity | 없음 | MISSING | 메뉴·주문·결제·관리자 도메인 미구현 |
| DB/JPA/Flyway | build/application 설정에 없음 | MISSING | schema·seed가 ASAK에 있으나 앱 연결 없음 |
| Test | context test 1개 | PARTIAL | business/API contract test 없음 |

## 중복 및 명명 관찰

- `ASAK-Kiosk`에 Admin pages/components/API가 함께 존재하지만 `ASAK-Admin`의 동명 역할은 placeholder다. Admin의 정본 구현 위치는 `ASAK-Admin`으로 확정해야 한다.
- Kiosk의 `orderStore`와 `cartStore`는 중복 store가 아니라 `orderSessionStore`를 re-export하는 의도적 호환 계층이므로 유지한다.
- `Header`가 `components/kiosk`와 `components/common`에 공존한다. 역할을 검증한 뒤 Kiosk Header는 보존하고 공통 Header를 성급히 통합하지 않는다.
