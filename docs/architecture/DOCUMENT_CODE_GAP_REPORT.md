# Document–Code Gap Report

## 핵심 충돌 (사람 확인 전 수정 금지)

| ID | 문서 기준 | 실제 코드 | 분류 | 필요한 결정 |
|---|---|---|---|---|
| API-01 | `POST /api/kiosk/orders`, `POST /api/kiosk/payments` | Kiosk constants: `/orders`, `/payments` | CONFLICT | canonical `/api/kiosk` prefix 채택 여부 |
| API-02 | menu list/detail: `/api/kiosk/menuList`, `/api/kiosk/menuDetail/{menuId}` | `/menus`, `/menus/{id}`, `/menus/{id}/options` | CONFLICT | Backend contract를 확정하고 adapter 일괄 정렬 |
| API-03 | sold-out: `PATCH /api/admin/soldOut` | `/admin/sold-out-items` | CONFLICT | draft 중 하나를 canonical로 결정 |
| API-04 | sales summary/monthly/daily API | `/admin/sales/daily` 상수만 존재 | PARTIAL | 화면별 contract 확정 |
| SCR-01 | SCR-022 Dashboard=`/`, SCR-009=`/orders/live` | Admin `/`가 SCR-009 | CONFLICT | registry대로 Dashboard를 `/`로 복원 |
| SCR-02 | `/soldOut`, `/paymentMethods` camelCase | `/sold-out`, `/payment-methods` | CONFLICT | URL naming rule 적용 범위 확인 |
| DATA-01 | 주문 response: `totalAmount`, 결제: `approvedAmount`, `approvedAt` | store: `totalPrice`, `amount`, `paidAt` | CONFLICT | DTO adapter 또는 store field 명명 결정 |
| UI-01 | Screen Bible은 SCR-003 | `MenuListPage` 주석은 SCR-002 | CONFLICT | Screen Registry의 SCR-003을 기준으로 주석/표시 정정 |

## 문서 대비 누락

- Kiosk: Cart, order create, payment method 조회/승인, complete, payment error, timeout overlay, accessibility, server-side 가격·품절 재검증 연결.
- Admin: login guard, Dashboard, Live Board polling, order list/detail/status, sold-out draft/save, menu CRUD, payment settings, sales KPI/chart, browser TTS.
- Backend: JPA/MySQL 의존성 및 설정, Entity/Repository/Service/Controller, validation/exception/error envelope, migration/seed 연결, contract/business tests.
- QA: 현재 자동화는 Backend context test뿐이며 Product Bible의 smoke/contract/regression 체크리스트를 실행하는 테스트가 없다.

## 반드시 보존할 기존 코드

1. Kiosk `MenuListPage`, `MenuCard`, `CategoryTabs`, `OrderTypeSelector`, menu detail/option UI의 도메인 모델과 mock 연결 방식.
2. 단일 주문 세션인 `orderSessionStore` 및 `orderStore`/`cartStore` 호환 export.
3. Axios client와 `{ success, status, code, message, data }` unwrap 구조.
4. Kiosk의 JavaScript, Vite, Zustand, CSS 토큰/스타일 구조와 Backend의 Spring Boot 4.1.0/Java 25/Gradle.

## 수정만 필요한 부분

- 이미 존재하는 Kiosk page/component의 route, props, option validation, loading/empty/error/disabled/processing 상태, API adapter 연결.
- Admin `AdminApp` route metadata를 Screen Registry와 일치시키고 placeholder를 기존 page/component에 연결.
- API constants/store DTO 이름을 확정 계약에 맞춰 adapter 경계에서 정렬.

## 신규 구현이 필요한 부분

- 위 누락 목록의 Backend 도메인 계층과 DB 연결.
- Cart/Payment/Complete/timeout/error의 실제 화면 동작.
- Admin의 실사용 페이지·store·API modules·auth guard 및 Dashboard/Live Order 기능.

## 지금 구현하지 않을 확장 기능

- SCR-023 영수증 출력, SCR-024 멤버십/쿠폰, 외부 AI TTS, WebSocket, 고급 접근성, 고급 매출 차트, 이미지 업로드·영양 재계산, 주문 취소 Live Board action.

## 문서 정리 판단

- `_archive/**`: ARCHIVE이며 현재 정본에서 제외.
- `docs/product_bible/**`: KEEP (각 문서 status가 Draft여도 현재 Product Bible 기준).
- Kiosk/Admin의 `README`, `STRUCTURE_GUIDE`, `IMPLEMENTATION_PLAN`, `contracts`: UPDATE 후보. Product Bible과 endpoint/route를 대조한 뒤 유지한다.
- `ASAK-Kiosk` 내부의 Admin page/component/API: MOVE 후보가 아니라 **중복 자산 검토 대상**. 팀원 코드 보존 원칙상 승인 전 이동/삭제하지 않는다.

## 확인이 필요한 결정사항

1. Product Bible의 canonical API 경로·응답 필드로 Backend와 두 프런트를 맞출지.
2. Admin camelCase URL을 유지할지, 현재 kebab-case URL을 허용할지.
3. Kiosk 안 Admin 스캐폴드를 재사용할지, ASAK-Admin에서 기능을 완성할지 및 소유자.
4. 기존 `kiosk.json` 및 `asak-admin-data.json`을 MVP demo 정본 mock으로 채택할지.
5. DB schema/seed 중 ASAK-back에 연결할 기준 파일과 migration 도구(Flyway 등) 채택 여부.

## Human decision status overlay

다음 이전 충돌은 사람 방향으로 결정됐으며 코드에는 의도적으로 미반영입니다: `API-01`, `API-02`, `API-03`, `SCR-01`, `SCR-02`는 `DECIDED_PENDING_CODE_CHANGE`; `DATA-01`은 `DECIDED_NOT_IMPLEMENTED`이며 현재 store 필드 이름 변경 없이 API adapter로 처리합니다. [Canonical Contract Decisions](../governance/CANONICAL_CONTRACT_DECISIONS.md)를 참고하세요. `UI-01`과 DB migration/seed 선택은 아직 열려 있습니다.
