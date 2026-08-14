# 2026-07-27 Admin 운영 조회 API·메뉴 adapter

> 일일 기록: [2026-07-27.md](../../daily/이하진/2026-07-27.md)
> 화면 기준: [SCR-009](../../../docs/product_bible/07_Screen_Bible/SCR-009-ADMIN-LIVE-ORDER-BOARD.md), [SCR-010](../../../docs/product_bible/07_Screen_Bible/SCR-010-ADMIN-ORDER-MANAGEMENT.md), [SCR-016](../../../docs/product_bible/07_Screen_Bible/SCR-016-ADMIN-MENU-MANAGEMENT.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-27
- 담당자: 이하진
- 저장소: ASAK-back / ASAK-Admin
- 관련 화면: SCR-009 Live Order Board, SCR-010 Order Management, SCR-016 Menu Management
- 관련 WBS/계약: WBS2-035·036·039·053 / API-011
- 구현 근거: `94a9589`(실시간 보드 조회), `9e827fd`(메뉴 목록 조회), `84606f6`(주문 목록·메뉴 상세)
- 작업 유형: `feature` / `fix`
- 완료 판정: Java 컴파일과 일부 Live DB 조회는 확인했지만, Spring context·Bruno·Admin 프론트 통합이 남아 있어 전체 기능 완료가 아니다.

## 2. 작업 목적

- 운영 중인 주문을 빠르게 보여 주는 Live 보드, 검색·상세 확인용 주문 관리, 메뉴 편집용 메뉴 관리의 목적을 분리한 조회 모델을 만든다.
- DB JSON을 화면에 그대로 넘기지 않고, 메뉴 관리 화면에서 실제로 표시·편집할 수 있는 요약 응답과 adapter 경계를 만든다.
- 빈 결과를 오류로 만들지 않고, 없는 주문 상세만 명확한 오류로 구분한다.

## 3. 화면 기준과 작업 범위

| 화면 | Figma/상태 기준 | 이 날짜의 작업 | 미완료 |
|---|---|---|---|
| SCR-009 Live 보드 | default `134:10607`, loading `134:11447`, empty `134:11452`, error `134:11468` | `vw_order_live`·Live DTO·`/active` 조회 기반 | polling, stale response, 상태 변경/TTS, 프론트 상태 UI |
| SCR-010 주문 관리 | default `134:10630`, loading `235:15447`, empty `235:15866`, error `235:16269` | 목록·상세 데이터 경로 보강 | 필터/상세 API 회귀, 화면 상태, 브라우저 |
| SCR-016 메뉴 관리 | default `134:12137`, add `134:12328`, edit `134:12668` | 목록/상세 요약 DTO와 편집 model 변환 | 저장·검증·error·실 API adapter |

## 4. 직접 구현 영역

### Live 주문 — `94a9589`

- `docs/view.sql`에 `vw_order_live`를 추가·보강하고, 활성 주문을 `RECEIVED`, `PREPARING` 상태와 생성 시각 오름차순 기준으로 조회하는 경로를 만들었다.
- `LiveOrderResponse`, `LiveOrderListResponse`를 추가하고, Live 카드가 쓸 `orderId`, `orderNo`, 주문 유형 라벨, 상태, `totalAmount`, 생성 시각, 경과 초, `menus` 정보를 다루는 모델을 구성했다.
- 이 구현은 Live 화면의 빠른 표시를 위한 모델이었다. 7/28 후속 변경에서 public `/api/admin/orders/active`가 `OrderListResponse`로 전환됐으므로, 현재 코드를 기준으로는 이 전용 모델이 그대로 응답된다고 단정할 수 없다.

### 메뉴 목록·상세 — `9e827fd`, `84606f6`

- `MenuListRequest`, `MenuListResponse`, `MenuDetailResponse`와 Controller·Service·Mapper 경로를 추가했다.
- 메뉴 상세는 재료, 옵션 그룹, 영양, 알레르겐, 태그를 표시/편집 목적의 요약 응답으로 나눴다. 프론트의 `toMenuEditModel`은 이 응답과 편집 화면 모델의 차이를 adapter에서 흡수하도록 두었다.
- 메뉴 CRUD·품절 변경을 이 조회 작업과 섞지 않았다. SCR-016의 `detailAdd`, `detailEdit`, `saving`, `error`는 별도 구현·검증 대상이다.

### 주문 목록·상세 — `84606f6`

- 주문 목록의 Controller·Service·Mapper 경로를 보강하고, 상세 응답의 메뉴 항목과 관련 정보를 정리했다.
- 목록이 비어 있으면 성공 200의 빈 결과로 다루고, 없는 주문 상세만 `ORDER_NOT_FOUND`로 구분하는 API 원칙을 유지했다.

## 5. 구현 로직 / 적용한 방식

### 화면 목적별 DTO 분리

- Live 보드는 빠른 처리 판단을 위해 주문 카드·경과 시간·메뉴 요약이 중심이다.
- 주문 관리는 검색·필터·페이지·상세의 `items[]`, `optionItems[]` 중심이다.
- 메뉴 관리는 원본 메뉴와 편집 draft를 만들 수 있는 재료·옵션·영양·알레르겐 요약이 중심이다.

따라서 세 응답을 같은 DTO로 강제로 합치지 않았다. Controller가 `ApiResponse`를 한 번만 만들고 Service는 화면 DTO를 반환하도록 해 `data.data` 중첩도 피하는 구조를 유지했다.

### 메뉴 상세의 DB/응답 경계

- Mapper는 메뉴 관련 뷰와 `JSON_TABLE`을 사용해 필요한 값을 조합하려 했다.
- 화면에는 DB JSON 전체가 아니라 옵션 권장 라벨, 영양, 알레르겐, 태그처럼 표시·편집에 필요한 요약을 제공하는 방향을 잡았다.
- 이 방향 자체는 정했지만 Mapper XML의 resultMap이 Spring에서 파싱되는지 확인하지 못했으므로, 응답이 실제로 끝까지 생성된다고 기록하지 않는다.

## 6. AI 도움 영역

- 사용한 AI 도구: Codex
- 요청 범위: 실DB 상태와 Mapper·DTO 경로, API envelope, 화면별 데이터 범위를 대조하는 보조.
- 도움 내용: Live/주문 관리/메뉴 관리 DTO를 분리할 근거, 빈 목록의 성공 처리, 화면에 불필요한 raw JSON을 줄이는 기준, MyBatis resultMap DTD 순서 확인 항목.
- 사람이 결정·검증한 부분: 조회 범위, DB seed 확인, 코드 반영, 커밋·main 반영 여부.
- 적용 방식: AI 제안은 검토 자료로만 쓰고, Spring/Bruno 증거가 없는 항목은 미완료로 유지했다.

## 7. 발생 이슈

### 이슈 1 — MyBatis resultMap 요소 순서

- 증상: `AdminMenuMapper.xml`을 포함한 Spring context 시작 시 `SAXParseException`이 발생할 수 있다.
- 원인: MyBatis DTD의 resultMap 요소 순서를 어겨 `<collection>`보다 `<association>`을 뒤에 배치한 부분이 있었다.
- 해결 상태: `menuDetailMap`에서 `<association>`을 먼저 배치해야 한다는 원인은 확인했다. 이 날짜에는 Java 컴파일까지만 확인했으며 Spring 기동 성공은 남아 있다.

### 이슈 2 — 컴파일과 Mapper 실행의 차이

- 증상: `compileJava`는 성공했지만 XML DTD와 실제 SQL·DB 매핑은 컴파일로 검증되지 않는다.
- 대응: 메뉴 상세를 완료라고 쓰지 않고, Spring context·Bruno·실DB 조회를 TODO에 남겼다.

### 이슈 3 — Live API 계약의 후속 변경

- 증상: 다음 날 공개 `/active` 반환 타입이 Live 전용 DTO에서 `OrderListResponse`로 바뀌었다.
- 영향: 7/27의 `menus[]` 기준 Live 카드와 현재 `menuSummary` 기준 공개 API 사이에 adapter/계약 결정을 해야 한다.
- 대응: 이 항목은 7/28 상세 워크로그에 후속 이력으로 기록하고, SCR-009 실제 연동 전에는 완료로 처리하지 않는다.

## 8. 디버깅 기록

- 확인한 오류: `AdminMenuMapper.xml` resultMap DTD 순서 관련 `SAXParseException` 가능성.
- 먼저 볼 파일: `AdminMenuMapper.xml`, `AdminOrderMapper.xml`, `AdminMenuService.java`, `AdminOrderService.java`, `ApiResponse.java`.
- 먼저 실행할 검증: `gradlew.bat -p ASAK-back compileJava --no-daemon` 다음 Spring context 기동, Bruno 메뉴 목록·상세, 활성 주문·빈 활성 주문, 없는 주문 상세.
- 데이터 확인 기준: 빈 목록은 정상 200, 없는 상세만 `ORDER_NOT_FOUND`, `ApiResponse`는 최상위 envelope를 한 번만 생성.

## 9. 이번 작업에서 배운 점

- Java 컴파일은 MyBatis XML DTD, Spring bean 등록, SQL 실행을 보장하지 않는다.
- 같은 “주문” 데이터라도 화면의 행동과 판단이 다르면 전용 DTO 또는 명확한 adapter가 필요하다.
- 화면에 쓰지 않는 DB JSON을 그대로 노출하면 프론트가 DB 구조에 묶이므로 표시/편집 요약 DTO가 더 안전하다.

## 10. 검증 내용

| 구분 | 실행/확인 | 결과 | 남은 범위 |
|---|---|---|---|
| Java 컴파일 | `ASAK-back\\gradlew.bat -p ASAK-back compileJava --no-daemon` | 통과 | Mapper XML/DB 실행 |
| Git 형식 | `git diff --check` | 통과 | PR/CI |
| Live 데이터 | `RECEIVED`, `PREPARING` 테스트 주문의 조회 결과 확인 | Live 조회 기반 확인 | 빈 결과·HTTP 응답·프론트 카드 |
| 메뉴 상세 | DTO·Mapper 변경 파일 대조 | 구조 확인 | Spring context, SQL 결과, 브라우저 |
| 프론트 | `toMenuEditModel`과 레이아웃 변경 반영 | 코드 반영 확인 | 실제 API, fallback, 화면 상태 |

## 11. 개선사항 / TODO

- [ ] `menuDetailMap` DTD 순서를 정리하고 Spring context를 실행한다.
- [ ] Bruno로 메뉴 목록/상세, 활성/빈 활성 주문, 주문 상세 없음과 필터 조합을 실행한다.
- [ ] SCR-009의 Live 전용 DTO와 현재 `/active` 목록 DTO 중 하나를 확정하고 adapter를 문서화한다.
- [ ] SCR-009·010·016의 loading/empty/error와 메뉴 저장/에러 상태를 브라우저에서 확인한다.
- [ ] 메뉴 등록·수정·삭제, 품절 변경은 별도 세로 슬라이스와 테스트로 이어 간다.

## 12. 포트폴리오용 요약

- Admin의 Live 주문, 주문 관리, 메뉴 관리가 서로 다른 화면 목적을 갖는다는 점을 기준으로 DB 조회·DTO·Mapper 경로를 분리했다. MyBatis 실행 및 프론트 통합 검증은 완료 조건에서 분리해 후속 체크리스트로 관리했다.

## 13. 참고 자료

- Backend: `docs/view.sql`, `AdminOrderController.java`, `AdminOrderService.java`, `AdminOrderMapper.xml`, `AdminMenuController.java`, `AdminMenuService.java`, `AdminMenuMapper.xml`
- Frontend: 메뉴 편집 model 변환과 메뉴 관리 레이아웃 관련 Admin 변경
- Bruno: `api/admin/Admin Menu List total.bru`
