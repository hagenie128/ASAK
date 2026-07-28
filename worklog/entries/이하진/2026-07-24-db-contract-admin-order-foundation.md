# 2026-07-24 DB 뷰·API 계약·Admin 주문 조회 기반

> **일일:** [2026-07-24.md](../../daily/이하진/2026-07-24.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-24
- 담당자: 이하진
- 저장소: ASAK / ASAK-back
- 브랜치: `main` 및 문서 작업 브랜치 이력
- 관련 이슈/PR: WBS2-053~055
- 작업 유형: `feature` / `docs`

## 2. 작업 목적

- DB 뷰·API 계약·WBS의 필드명을 같은 기준으로 맞추고, Admin 주문 관리 화면이 사용할 목록·상세 조회 API의 첫 세로 슬라이스를 만든다.
- 구현 근거가 있어도 API 테스트 증거가 없으면 DONE으로 처리하지 않는 기준을 문서에 유지한다.

## 3. 직접 구현 영역

- `ASAK-back/docs/view.sql`의 뷰 설명과 중복 정의를 정리하고, `optionItemId`, `unitPrice`, `ingredientId`, `waitingOrderCount` 등 계약 필드명을 맞췄다.
- API 메뉴/주문/결제와 매출·대시보드 응답 예시를 보강하고, DevCopilot 허브의 DB 뷰 정보를 동기화·감사했다.
- `OrderListFilter`, `OrderListResponse`를 추가하고 Admin 주문 목록 조회를 Controller → Service → Mapper XML 흐름으로 연결했다.
- Admin 주문 상세 조회에 Mapper·Service·Controller 경로를 연결하고, 주문·결제 상태를 응답에 포함했다.

## 4. 구현 로직 / 적용한 방식

- 목록 조회는 요청 필터 DTO에서 조건을 받고, Service가 Mapper 결과를 응답 DTO로 반환하도록 역할을 나눴다.
- 상세 조회는 없는 주문을 일반 빈 응답으로 숨기지 않고 `ORDER_NOT_FOUND` 오류로 구분했다.
- 공통 응답은 `ApiResponse`가 최상위 `{ success, status, code, message, data }`를 만들도록 두고, Service에서 `data`를 한 번 더 감싸지 않는 계약을 유지했다.
- WBS2-048~051·053~055는 코드/계약 증거만 반영해 IN_PROGRESS로 두고, 046·047·052는 TODO, 프론트 실연동 058~060은 BLOCKED로 유지했다.

## 5. AI 도움 영역

- 사용한 AI 도구: Codex / Cursor
- 어떤 질문/요청을 했는지: Git 이력·현재 문서·WBS를 대조해 실제 구현과 계약 문서의 차이를 찾고, 응답 envelope와 상태 표기를 검토해 달라고 요청했다.
- AI가 도움 준 내용: 누락된 문서·WBS Evidence 후보와 API 응답 필드 불일치 후보를 정리했다.
- 그대로 사용한 부분: Controller → Service → Mapper → DTO 경계와 공통 응답 확인 목록.
- 수정해서 사용한 부분: 구현·테스트 완료 여부는 커밋 존재만으로 판정하지 않고, 실제 실행 증거가 없는 항목은 IN_PROGRESS로 다시 조정했다.

## 6. 발생 이슈

- 이슈 1:
  - 증상: 코드와 계약 문서의 필드명이 달라지면 프론트 adapter와 매출 화면의 값이 달라질 수 있다.
  - 원인: DB 뷰, API 예시, mock에서 각각 다른 이름을 사용한 이력이 있었다.
  - 해결: 문서와 뷰 설명을 `optionItemId`, `unitPrice` 등 계약 필드 기준으로 보강하고, canonical/legacy 차이는 adapter 경계에 남겼다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: 이 날짜의 워크로그 범위에는 저장된 런타임 오류 로그가 없다.
- 의심했던 지점: 목록/상세 응답을 Service에서 다시 감싸 `data.data` 형태가 되는지 여부.
- 실제 원인: 공통 `ApiResponse`의 역할과 Service 반환 책임을 분리하지 않으면 응답 envelope가 중첩될 수 있다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: `ApiResponse.java`, `AdminOrderController.java`, `AdminOrderService.java`, `AdminOrderMapper.xml`과 Bruno 요청 경로를 함께 확인한다.

## 8. 이번 작업에서 배운 점

- DB 뷰 주석도 API 계약의 일부다. 화면에서 쓰는 필드명은 SQL·DTO·문서에서 같은 의미로 유지해야 한다.
- Controller/Service/Mapper 파일이 생겼다는 사실과 요청을 실제로 통과시킨 테스트 증거는 별개다.

## 9. 개선사항 / TODO

- Bruno로 Admin 주문 목록·상세의 정상/없는 주문/필터 조합을 실행해 증거를 남긴다.
- `./gradlew test`와 DB 조회로 목록·상세 데이터 매핑을 검증한다.
- Admin 프론트 adapter의 실제 API 연결 범위와 mock fallback 유지 기준을 확정한다.

## 10. 검증 내용

- 실행한 명령어: Git 커밋과 변경 파일을 기준으로 구현 경로를 대조했다.
- 테스트한 시나리오: 주문 목록 요청 필터·상태 응답 및 없는 주문 상세의 오류 처리 구조를 코드/계약 문서에서 확인했다.
- 확인 결과: 목록·상세 조회 구현과 WBS2-053 Evidence는 확인했지만, 이 날짜에 보관된 Gradle·Bruno 실행 결과는 없어 상태를 IN_PROGRESS로 기록했다.

## 11. 포트폴리오용 요약

- Admin 주문 관리 기능의 조회 API를 DTO·Mapper XML·공통 응답 규칙까지 연결하고, DB/API/문서의 필드 계약을 함께 정리했다.

## 12. 첨부하면 좋은 자료

- 7/24 커밋: `4d455a9`, `a300060`, `72e2c78`
- `ASAK-back/docs/view.sql`
- `docs/wiki/wbs-v2-2026-07-16.md`, `docs/wiki/rest-api-spec.md`
