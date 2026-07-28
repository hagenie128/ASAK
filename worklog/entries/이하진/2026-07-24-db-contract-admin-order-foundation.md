# 2026-07-24 DB 뷰·API 계약·Admin 주문 조회 기반

> 일일 기록: [2026-07-24.md](../../daily/이하진/2026-07-24.md)
> 기준 화면: [SCR-010 Admin Order Management](../../../docs/product_bible/07_Screen_Bible/docs/07-screens/SCR-010-ADMIN-ORDER-MANAGEMENT.md) · Figma 0718 `134:10630`

---

## 1. 기본 정보

- 작업 날짜: 2026-07-24
- 담당자: 이하진
- 저장소: ASAK / ASAK-back
- 관련 작업: WBS2-048~055, WBS2-064, SCR-010
- 구현 근거: `72e2c78`(목록 조회·응답 정리), `a300060`(필터/목록 DTO), `4d455a9`(상세 조회)
- 작업 유형: `feature` / `docs`
- 완료 판정: 코드·문서 변경 경로는 확인했으나, 이 날짜에 보관된 Gradle·Spring·Bruno 실행 증거가 없어 `IN_PROGRESS`다.

## 2. 작업 목적

- Admin 주문 관리 화면이 검색·필터·상세를 사용할 수 있도록 목록과 상세 조회의 최소 세로 슬라이스를 만든다.
- DB 뷰·API 예시·DTO·WBS가 서로 다른 필드명을 말해 프론트 adapter가 흔들리는 문제를 줄인다.
- “커밋이 있다”와 “기능을 실제로 검증했다”를 구분해 WBS 상태를 정직하게 남긴다.

## 3. 직접 구현 영역

- 목록 요청 조건을 담는 `OrderListFilter`와 목록 행 응답 `OrderListResponse`를 추가했다.
- `AdminOrderController` → `AdminOrderService` → `AdminOrderMapper`/`AdminOrderMapper.xml` 경로에서 목록과 상세 조회를 연결했다.
- 상세 조회는 주문이 없을 때 일반 빈 객체가 아니라 `ORDER_NOT_FOUND`를 반환하도록 분기했다.
- 뷰 설명과 API 예시에서 `optionItemId`, `unitPrice`, `ingredientId`, `waitingOrderCount` 같은 계약 필드를 정리했고, 메뉴/주문/결제와 매출·대시보드 예시를 보강했다.
- DevCopilot 허브에 실DB 뷰 정보를 동기화하고, 허브 ERD의 잔여 중복·유령 구조를 감사 문서로 남겼다.

## 4. 구현 로직 / 적용한 방식

### 조회 흐름

1. 화면은 페이지, 크기, 주문 상태, 결제 상태, 주문 유형, 날짜, 키워드를 요청한다.
2. Controller가 이를 Service로 전달하고, Service는 `OrderListFilter`에 조건과 pagination 값을 만든다.
3. Mapper XML은 목록 행을 `OrderListResponse`로 조회하고, Service는 `PageResult`로 목록·현재 페이지·총 건수를 묶는다.
4. Controller만 `ApiResponse`를 만들어 최상위 `{ success, status, code, message, data }` envelope를 제공한다. Service에서 `data`를 한 번 더 감싸지 않는 것이 규칙이다.
5. 상세는 `orderId`로 조회하며 결과가 없을 때만 `ORDER_NOT_FOUND`로 구분한다. 목록이 비어 있는 것은 정상 업무 상태라 성공 빈 목록으로 처리하는 것이 목표다.

### 화면·Figma 범위

SCR-010의 Figma 0718 기준은 Default `134:10630`, Loading `235:15447`, Empty `235:15866`, Error `235:16269`이며 필수 상태는 `default`, `loading`, `empty`, `error`다. 이 날짜에는 목록/상세 API 기반을 만든 범위이며, React의 상태 UI·필터 URL 보존·접근성·브라우저 검증까지 완료한 기록은 아니다.

## 5. AI 도움 영역

- 사용한 AI 도구: Codex / Cursor
- 요청 범위: 현재 Git 이력·WBS·API 계약을 대조해 구현 경로와 필드 불일치 후보를 찾는 보조.
- AI가 도움 준 내용: Controller/Service/Mapper/DTO 경계, `ApiResponse` envelope 중첩 방지, WBS 증거와 실행 검증을 분리하는 체크 항목.
- 사람이 판단한 부분: 구현 파일 반영, WBS 최종 상태, DB/플랫폼 동기화 범위.
- 적용 원칙: AI가 제안한 구조를 그대로 완료 판정에 쓰지 않고, 실행 근거가 없으면 상태를 `IN_PROGRESS`로 유지했다.

## 6. 발생 이슈

### 이슈 1 — 계약 필드의 다중 이름

- 증상: SQL 뷰, API 예시, mock이 같은 값을 서로 다른 이름으로 표현하면 화면 adapter가 변환 규칙을 중복으로 갖게 된다.
- 원인: 기능별 문서와 구현이 독립적으로 갱신된 이력이 있었다.
- 대응: canonical 필드는 `optionItemId`, `unitPrice` 등으로 문서·뷰 설명을 보강하고, legacy 이름은 adapter 경계에서만 흡수하는 방향을 남겼다.

### 이슈 2 — 구현 근거와 실행 근거의 차이

- 증상: 목록·상세 파일이 존재해도 Mapper XML 파싱, DB 데이터, 실제 HTTP 응답은 실패할 수 있다.
- 대응: 이 날짜의 상세 워크로그에는 저장된 Gradle/Bruno 로그가 없음을 명시하고 완료로 쓰지 않았다.

### 이슈 3 — DevCopilot ERD 잔여 데이터

- 증상: 실DB 뷰 동기화 후에도 주문·매출 영역에 유령 테이블/컬럼 중복이 남았다.
- 원인: 플랫폼의 삭제 반영 한계와 기존 데이터 잔존.
- 대응: 동기화 성공과 ERD 완전 정리를 분리해 기록하고, 플랫폼 정리는 외부 블로커로 남겼다.

## 7. 디버깅 기록

- 이 날짜 범위에는 저장된 런타임 오류 로그가 없다.
- 다음에 먼저 확인할 파일: `ApiResponse.java`, `AdminOrderController.java`, `AdminOrderService.java`, `AdminOrderMapper.java`, `AdminOrderMapper.xml`, Bruno의 Admin 주문 요청.
- 다음에 먼저 확인할 시나리오: 빈 목록은 200인지, 없는 상세만 `ORDER_NOT_FOUND`인지, 필터와 total count의 조건이 같은지, `ApiResponse.data`가 중첩되지 않는지.

## 8. 이번 작업에서 배운 점

- DB 뷰의 컬럼 이름과 설명도 화면 API 계약의 일부다.
- 단위 파일 추가는 세로 슬라이스의 시작일 뿐이다. 실제 DB·Mapper·HTTP·프론트 화면까지 한 번에 통과해야 기능 완료라고 쓸 수 있다.

## 9. 개선사항 / TODO

- [ ] Spring context와 `./gradlew test` 또는 범위 테스트를 실행한다.
- [ ] Bruno로 목록 정상/빈 결과/모든 필터/없는 상세를 확인한다.
- [ ] 실제 DB 결과와 `OrderListResponse`·`OrderDetailResponse` 필드를 대조한다.
- [ ] SCR-010의 loading/empty/error 및 프론트 adapter/mock fallback을 확정한다.

## 10. 검증 내용

- 확인한 근거: 세 커밋의 변경 파일에서 DTO → Controller/Service → Mapper XML → 오류 코드 연결을 대조했다.
- 확인 결과: 목록 필터/행 DTO와 상세 조회 경로가 추가된 사실은 확인했다.
- 미확인 범위: 이 날짜의 Gradle, Spring context, Bruno, 실제 DB, 브라우저 상태 결과는 남아 있지 않다.

## 11. 포트폴리오용 요약

- Admin 주문 관리의 목록·상세 조회를 DTO, Mapper XML, 공통 응답 규칙까지 연결하고, DB/API/문서 필드 계약을 함께 정리했다. 실제 실행 검증은 완료 조건에서 분리해 후속 과제로 관리했다.

## 12. 참고 자료

- `ASAK-back/docs/view.sql`
- `docs/wiki/wbs-v2-2026-07-16.md`, `docs/wiki/rest-api-spec.md`, `docs/wiki/devcopilot-hub-audit-2026-07-24.md`
- `OrderListFilter.java`, `OrderListResponse.java`, `AdminOrderController.java`, `AdminOrderService.java`, `AdminOrderMapper.xml`
