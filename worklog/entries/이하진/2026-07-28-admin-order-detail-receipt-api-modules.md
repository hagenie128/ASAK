# 2026-07-28 관리자 주문 상세 금액 내역 및 API 모듈 정리

> 일일 기록: [2026-07-28.md](../../daily/이하진/2026-07-28.md)
> 기준 화면: [SCR-010 Admin Order Management](../../../docs/product_bible/07_Screen_Bible/docs/07-screens/SCR-010-ADMIN-ORDER-MANAGEMENT.md) · Figma 0718 화면 `134:10630` · 구현 컴포넌트 주석의 상세 패널 `150:5418`
> 관련 확장 화면: [SCR-023 Receipt Output](../../../docs/product_bible/07_Screen_Bible/docs/07-screens/SCR-023-RECEIPT-OUTPUT.md) — 이 날짜에는 미구현

---

## 1. 기본 정보

- 작업 일자: 2026-07-28
- 담당자: 이하진
- 저장소: ASAK-Admin / ASAK-back
- 반영 이력: `aecf6f8`(API 모듈 명명 통일), `96352d9`(주문 상세 금액 내역), `05d6351`(주문 조회·판매 뷰 정비), `c5538f9`(Bruno 계약 용어 정렬)
- 관련 화면/계약: SCR-010, API-007 `GET /api/admin/orders`, `GET /api/admin/orders/{orderId}`, `GET /api/admin/orders/active`
- 작업 유형: `feature` / `refactor` / `docs`
- 완료 판정: 정적 검사와 Java 컴파일은 완료. Spring 기동, Bruno, 실제 DB·브라우저 통합 검증은 미완료이므로 기능 전체 완료로 판정하지 않는다.

## 2. 작업 목적

- 관리자 주문 상세에서 메뉴 이름과 단가만 보이던 정보를 금액 근거 단위로 나눈다. 관리자가 기본 메뉴 금액, 옵션 추가금, 제외 재료, 메뉴별 합계를 구분해 주문·환불 판단을 할 수 있어야 한다.
- API 모듈 파일명과 import를 역할이 드러나는 형태로 정리하되, 요청 경로와 응답 계약은 바꾸지 않는다.
- 주문 목록의 행 조회와 개수 집계가 같은 검색 조건을 해석하도록 정비하고, 활성 주문 응답 모델이 프론트 계약과 어떻게 다른지 남긴다.

## 3. 화면·상태·재사용 범위

| 구분 | 기준 | 이 날짜의 범위 | 남은 확인 |
|---|---|---|---|
| SCR-010 주문 관리 | Figma 0718 Default `134:10630`, Loading `235:15447`, Empty `235:15866`, Error `235:16269` | 주문 상세 패널의 선택 없음 상태와 금액 항목 UI를 보강 | 목록/상세 실제 응답, 상세 loading/error, 브라우저 접근성 |
| 상세 패널 | Figma 컴포넌트 주석 `150:5418` | 옵션·제외·메뉴 합계 렌더링 | 옵션 가격 누락, 취소/환불 표시, 버튼 동작 |
| SCR-023 영수증 출력 | Extension / 신규, `choice/printing/success/error` | 금액 표시 구조를 재사용 후보로만 검토 | API, 프린터 연동, 실패·재출력 UX, Figma 확정 |

`OrderManagementPreview`가 주문 목록을 조회하고, 행 선택 시 `ordersApi.getOrder(orderId)`를 호출한다. 응답은 `OrderDetailResponse`의 `items[]`으로 전달되어 `OrderDetailPanel`이 표시한다. 이 흐름은 구현 파일을 기준으로 확인했으며, 실제 네트워크 응답을 캡처해 검증한 기록은 없다.

## 4. 직접 구현 영역

### ASAK-Admin

- `src/api/`의 `admin.js`, `client.js`, `menus.js`, `orders.js`, `paymentMethods.js`, `sales.js`, `soldOut.js`를 각각 `*Api.js` 이름으로 변경하고, `useOrdersQuery.js`와 `OrderManagementPreview.jsx`의 import를 갱신했다. 경로는 `ordersApi.listOrders`, `ordersApi.getOrder`, `ordersApi.listActiveOrders`로 유지했다.
- `OrderDetailPanel.jsx`에 `getPositiveQuantity`, `getOptionLineAmount`, `getItemTotalAmount`를 추가했다. 수량이 숫자가 아니거나 0 이하이면 표시/계산상 1개로 보정한다.
- 옵션 행은 `option.price × item.quantity × option.quantity`로 계산하고, 메뉴 합계는 `item.unitPrice × item.quantity + 옵션 행 합계`로 계산한다. 취소/환불 상태에서는 기존 `formatItemPrice`의 음수 표시 규칙을 그대로 사용한다.
- 옵션과 제외 재료를 단일 문자열로 합치지 않고 별도 섹션으로 렌더링했다. 각 항목이 없으면 해당 섹션에 `없음`을 표시한다. CSS에는 행 정렬, 메뉴 합계 구분선, 긴 이름 대응을 위한 flex/min-width 규칙을 추가했다.

### ASAK-back

- `/api/admin/orders/active`의 Controller·Service·Mapper 반환 타입을 `LiveOrderListResponse`에서 `OrderListResponse`로 통일했다. 현재 응답 행은 `orderId`, `orderNo`, `orderType`, `orderStatus`, `paymentStatus`, `totalAmount`, `createdAt`, `itemCount`, `menuSummary`를 가진다.
- 주문 목록 행 조회는 `vw_order_list_summary`를 유지하고, 개수 집계는 `orders`·`payment`·`common_code` 및 메뉴명 검색용 `order_item`·`menu` 조건을 사용하도록 바꿨다. 필터는 주문 상태, 결제 상태, 주문 유형, 날짜 범위, 주문번호/메뉴명 키워드다.
- `docs/view.sql`에 주문 옵션·제외 재료와 일/시간별 판매·상위 메뉴 집계 뷰 정의를 반영했다. 이 문서 변경만으로 DB에 뷰가 적용됐다는 뜻은 아니다.

## 5. 구현 로직 / 적용한 방식

### 주문 상세 데이터 흐름

1. `OrderManagementPreview`가 목록에서 선택한 `orderId`를 `ordersApi.getOrder`에 전달한다.
2. 백엔드 `GET /api/admin/orders/{orderId}`는 `OrderDetailResponse`를 반환하고, 없으면 `ORDER_NOT_FOUND`를 반환하도록 되어 있다.
3. 상세 응답의 `items[]` 각 행은 `menuName`, `quantity`, `unitPrice`, `optionItems`, `excludedIngredients`를 가진다.
4. 패널은 기본 단가를 먼저 표시한 뒤 옵션·제외 목록과 메뉴 합계를 렌더링하고, 주문 전체 금액은 서버의 `totalAmount`를 별도로 표시한다.

서버 전체 금액을 클라이언트에서 다시 합산한 메뉴 합계로 대체하지 않은 이유는 결제 확정 금액의 정본을 임의로 바꾸지 않기 위해서다. 화면 계산값은 항목별 설명용이며, 서버 `totalAmount`와 불일치할 때는 데이터 계약 또는 표시 정책을 별도로 확인해야 한다.

### 활성 주문·목록 집계

- 활성 주문 API는 현재 `vw_order_list_summary`에서 `RECEIVED`, `PREPARING` 상태를 생성 시각 오름차순으로 조회한다.
- 이 응답은 7/27에 기록한 `vw_order_live`/`menus[]` 중심의 Live 전용 모델과 다르다. `vw_order_live` 쿼리와 `LiveOrderResponse`는 코드에 남아 있으나, 이 날짜의 public `/active` 경로는 `OrderListResponse`를 반환한다.
- 따라서 SCR-009 Live 보드가 필요로 하는 경과 시간·`menus[]`와 현재 공개 API의 `menuSummary` 사이의 adapter 또는 계약 결정은 남은 일이다. 둘을 이미 통합했다고 기록하지 않는다.

## 6. AI 도움 영역

- 사용한 AI 도구: Codex
- 요청 범위: 금액 계산 기준, 현재 코드·Git 이력·Screen Bible 사이의 차이, 검증 범위를 대조하는 보조.
- AI가 제공한 내용: 옵션별 가격 계산과 수량 보정의 검토 항목, `totalAmount`를 최상위 응답과 정본 금액으로 유지하는 기준, 활성 주문 DTO 변경에 따른 문서 불일치 후보.
- 사람이 결정·확인한 부분: 어떤 파일을 기능별로 분리할지, 커밋/병합 범위, 실제 코드 반영과 결과 확인.
- 그대로 사용한 부분: 금액 표시를 기본/옵션/제외/메뉴 합계로 분리하는 구조와 검증 체크리스트.
- 수정해서 사용한 부분: 영수증 기능은 구현 완료가 아니라 데이터 표시 재사용 후보로만 남기고, DTO 차이는 실제 코드 기준으로 재기록했다.

## 7. 발생 이슈 및 미완료 상태

### 이슈 1 — UI 버튼과 실제 기능 연결 상태

- 증상: `OrderManagementPreview`의 `handleRefund`, `handlePrintReceipt`는 주석 처리되어 있으나, `OrderDetailPanel`은 승인 결제 또는 취소 상태에서 해당 버튼을 렌더링할 수 있다.
- 영향: 실제 주문 데이터를 연결하면 클릭 시 전달받지 않은 핸들러를 호출할 위험이 있다. 따라서 환불·영수증을 완료 기능으로 기록할 수 없다.
- 필요한 해결: API와 오류/확인 다이얼로그를 연결하기 전에는 버튼을 숨기거나 비활성화할지 결정하고, 연결 후 정상·실패·중복 클릭을 검증한다.

### 이슈 2 — 금액 데이터의 예외값

- 증상: 옵션의 `price`가 `undefined`이면 `Number(option.price)` 계산 결과가 `NaN`이 될 수 있다.
- 영향: 메뉴 합계와 옵션 표시가 깨질 수 있다.
- 필요한 해결: API 계약에서 옵션 가격의 필수/기본값을 확정하고, `0원`, 누락, 문자열 숫자, 옵션 수량 2 이상을 실제 응답으로 테스트한다.

### 이슈 3 — 메뉴 합계의 표시 조건

- 증상: 현재 메뉴 합계는 옵션 또는 제외 재료가 하나 이상일 때만 렌더링된다.
- 영향: 기본 메뉴만 있는 주문에는 메뉴 합계 행이 보이지 않는다.
- 필요한 해결: 모든 메뉴에 합계를 보여 줄지 Figma와 UX 의도를 확인한 뒤 조정한다. 이 워크로그에서는 코드 수정하지 않았다.

### 이슈 4 — 활성 주문 계약 전환

- 증상: 7/27의 Live 전용 `menus[]` 기록과 7/28 공개 API의 `menuSummary` DTO가 다르다.
- 영향: SCR-009 프론트가 기대하는 카드 데이터와 API가 맞지 않을 수 있다.
- 필요한 해결: Live 보드용 DTO/API를 유지할지, 목록 DTO에 adapter를 둘지 팀 기준을 확정하고 Bruno·브라우저로 확인한다.

## 8. 디버깅 기록

- 확인한 결과: `gh auth status`에서 GitHub CLI 토큰 만료 상태를 확인했다. GitHub CLI 인증은 HTTPS Git push 인증과 별도라서 Git 원격 push 자체는 가능했다.
- 확인한 결과: 첫 Gradle 실행은 샌드박스 환경의 배포본 다운로드 제한에 막혔고, 권한이 있는 환경에서 재실행해 `compileJava` 성공을 확인했다.
- 확인해야 할 우선순위:
  1. `OrderManagementPreview.jsx`의 상세 요청 결과와 API client의 응답 unwrap 규칙
  2. `OrderDetailPanel.jsx`의 옵션 가격·수량·취소 상태 표시
  3. `AdminOrderMapper.xml`의 목록 행/개수 필터 결과와 Spring context 기동
  4. `ordersApi.js`의 `/active` 응답이 SCR-009 adapter와 맞는지

## 9. 이번 작업에서 배운 점

- `unitPrice`와 `totalAmount`는 같은 의미가 아니다. 전자는 항목 기본 단가, 후자는 서버가 확정한 주문 전체 금액이므로 화면에서 서로 대체하면 안 된다.
- 컴포넌트가 UI를 렌더링한다는 것과 사용자 행동이 끝까지 작동한다는 것은 다르다. 특히 버튼 핸들러, API 실패, 상세 요청 중 상태를 따로 확인해야 한다.
- API DTO를 통일하면 파일 수는 줄지만 화면 목적까지 자동으로 같아지지는 않는다. Live 보드와 주문 관리의 필요한 데이터가 다르면 adapter 또는 별도 DTO가 필요하다.

## 10. 검증 내용

| 구분 | 실행/확인 | 결과 | 검증하지 못한 범위 |
|---|---|---|---|
| Admin lint | `npm.cmd run lint` | 오류 0건. 기존 미사용 변수 경고 2건 | 런타임 동작 |
| Admin build | `npm.cmd run build` | Vite 프로덕션 빌드 성공. 기존 번들 크기 경고 | 브라우저 렌더링/상호작용 |
| Git 형식 | 기능별 staged diff check 및 main 동기화 확인 | 기록상 통과 | PR 리뷰/CI |
| Back compile | `gradlew.bat -p C:\ASAK-workspace\ASAK-back compileJava --no-daemon` | `BUILD SUCCESSFUL` | Mapper XML 파싱, Spring context, DB 쿼리 |
| API/DB | 코드·DTO·SQL 변경 파일 대조 | 요청 경로와 필드 변경을 확인 | Bruno, 실DB 정상/빈/필터/오류 응답 |

## 11. 다음 작업 / 검증 체크리스트

- [ ] 실제 주문 4종(옵션 없음, 옵션 0원, 옵션 수량 2 이상, 제외 재료만 있음)으로 메뉴 행과 서버 `totalAmount`를 대조한다.
- [ ] SCR-010의 목록 `loading/empty/error`와 상세 선택 없음/상세 요청 실패 상태를 브라우저에서 확인한다.
- [ ] 환불·영수증 버튼의 노출 정책을 정하고, 연결 전에는 클릭 불가능 상태인지 확인한다.
- [ ] Spring context와 Bruno로 `/api/admin/orders`, `/{orderId}`, `/active`의 정상·빈 결과·없는 주문·각 필터 조합을 확인한다.
- [ ] SCR-009가 `menuSummary`를 쓸지 Live 전용 `menus[]` 계약을 복구할지 결정한다.
- [ ] SCR-023의 프린터 실패·용지 없음·재출력 상태와 API 계약을 별도 화면 작업으로 정의한다.

## 12. 포트폴리오용 요약

- 관리자 주문 상세에 기본 단가, 옵션별 추가금, 제외 재료, 메뉴 합계를 분리해 표시하고, 서버 확정 주문 금액(`totalAmount`)과 항목별 설명 금액을 구분했다.
- API 모듈 import를 정리하고 주문 조회·판매 뷰의 DTO/집계 조건을 보강했다. 다만 실제 API·DB·브라우저 통합 검증 및 영수증 기능은 다음 작업으로 남겼다.

## 13. 첨부 / 참고 자료

- Admin: `src/components/admin/OrderDetailPanel.jsx`, `src/styles/admin/orders.css`, `src/api/ordersApi.js`, `src/hooks/useOrdersQuery.js`, `src/pages/admin/OrderManagementPreview.jsx`
- Backend: `AdminOrderController.java`, `AdminOrderService.java`, `AdminOrderMapper.java`, `AdminOrderMapper.xml`, `docs/view.sql`
- 문서: SCR-010, SCR-023, Bruno `api/admin/04-order-status.bru`, `api/kiosk/03-cart-validate.bru`, `api/kiosk/04-create-order.bru`
