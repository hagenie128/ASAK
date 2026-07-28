# 2026-07-27 Admin 운영 조회 API·메뉴 adapter

> **일일:** [2026-07-27.md](../../daily/이하진/2026-07-27.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-07-27
- 담당자: 이하진
- 저장소: ASAK-back / ASAK-Admin
- 브랜치: `main` (ASAK-back) / Admin 작업 브랜치 이력
- 관련 이슈/PR: WBS2-035·036·039·053 / API-011
- 작업 유형: `feature` / `fix`

## 2. 작업 목적

- Admin Live 주문, 주문 목록, 메뉴 관리 화면이 실제 DB 조회 결과를 사용할 수 있도록 백엔드 조회 세로 슬라이스를 확장한다.
- 메뉴 상세 응답은 raw JSON을 그대로 넘기지 않고 화면 표시·편집에 필요한 요약 필드만 제공한다.

## 3. 직접 구현 영역

- `vw_order_live`와 `LiveOrderResponse`·`LiveOrderListResponse`를 추가해 `GET /api/admin/orders/active` 조회 경로를 만들었다.
- 활성 주문은 `RECEIVED`, `PREPARING` 상태를 대상으로 생성 시각 오름차순으로 조회하고, Live 카드용 `menus[]` 표시 정보를 반환하도록 구성했다.
- Admin 메뉴 목록·상세 DTO, Controller·Service·Mapper XML을 보강하고, 재료·옵션 그룹·영양·알레르겐·태그 등 표시/편집용 요약을 분리했다.
- 주문 목록·상세의 오류 처리를 정리해 없는 주문 상세에만 `ORDER_NOT_FOUND`를 반환하고, 빈 목록은 정상 200 응답으로 처리했다.
- Admin 프론트에 `toMenuEditModel` 변환 함수와 메뉴 관리 레이아웃 보완을 반영했다.

## 4. 구현 로직 / 적용한 방식

- Live 주문과 주문 목록/상세는 목적이 달라 DTO 형태를 분리했다. Live 화면은 `menus[]` 중심의 빠른 운영 표시, 주문 목록/상세는 `items[]`·`optionItems[]` 중심의 상세 표시를 사용한다.
- Controller는 `ApiResponse` 한 겹만 만들고, Service는 `LiveOrderListResponse`를 반환해 최종 응답이 `data.content` 형태가 되도록 했다.
- 메뉴 상세는 `JSON_TABLE`과 메뉴 관련 뷰를 이용해 화면에서 필요한 옵션 권장 라벨·영양·알레르겐·태그를 요약하는 방향으로 구성했다.
- Admin 프론트 변환 함수는 API 응답과 메뉴 편집 화면 모델 사이의 차이를 adapter 경계에서 처리하도록 두었다.

## 5. AI 도움 영역

- 사용한 AI 도구: Codex
- 어떤 질문/요청을 했는지: 실제 DB 상태와 MyBatis Mapper·DTO 경로를 기준으로 Live 주문 조회가 화면 계약에 맞는지, 메뉴 상세가 과도한 DB JSON을 노출하지 않는지 검토해 달라고 요청했다.
- AI가 도움 준 내용: Live 주문 DB seed/조회 검증 항목, response envelope 중첩 방지, 메뉴 상세 결과 범위와 Mapper XML resultMap 순서 문제를 점검했다.
- 그대로 사용한 부분: Live와 목록/상세 DTO 분리, 빈 목록을 성공 응답으로 처리하는 규칙.
- 수정해서 사용한 부분: 메뉴 상세는 초기의 넓은 응답 범위를 줄여 표시/편집에 필요한 요약 DTO로 정리했다.

## 6. 발생 이슈

- 이슈 1:
  - 증상: 메뉴 상세 Mapper를 포함한 Spring context 시작 시 SAXParseException이 발생할 수 있다.
  - 원인: MyBatis resultMap에서 `<collection>`보다 `<association>`이 앞에 와야 하는 DTD 순서를 지키지 않은 부분이 있다.
  - 해결: `menuDetailMap`에서 `<association>`을 `<collection>`보다 먼저 배치한 뒤 Spring 기동으로 재검증해야 한다. 이 날짜에는 컴파일 통과까지만 확인했다.

## 7. 디버깅 기록

- 확인한 로그/에러 메시지: Menu Mapper의 `SAXParseException`과 resultMap 요소 순서 문제를 확인했다.
- 의심했던 지점: Live 조회가 빈 결과를 오류로 처리하거나, Service가 `data`를 다시 감싸는 응답 구조.
- 실제 원인: 빈 활성 주문은 정상 업무 상태이며, 공통 `ApiResponse`가 이미 최상위 envelope를 담당한다.
- 다시 같은 문제가 생기면 먼저 볼 파일/명령어: `AdminMenuMapper.xml`, `AdminOrderMapper.xml`, `ApiResponse.java`를 확인한 뒤 `gradlew.bat compileJava --no-daemon` 및 Spring context 기동을 실행한다.

## 8. 이번 작업에서 배운 점

- Java 컴파일 성공은 Mapper XML DTD 순서와 Spring context 시작 성공을 보장하지 않는다.
- 운영 보드용 요약 DTO와 주문 상세 DTO는 화면이 다르면 같은 구조로 억지로 통합하지 않는 편이 안전하다.

## 9. 개선사항 / TODO

- `AdminMenuMapper.xml` resultMap 순서를 정리하고 Spring context 기동을 확인한다.
- Admin/Kiosk의 실제 API adapter 연결과 mock fallback 정책을 확정한다.
- Bruno로 활성 주문, 빈 활성 주문, 메뉴 목록/상세, 없는 주문 상세를 회귀 검증한다.
- 메뉴 등록·수정·삭제와 품절 API는 별도 세로 슬라이스로 이어 간다.

## 10. 검증 내용

- 실행한 명령어: `ASAK-back\\gradlew.bat -p ASAK-back compileJava --no-daemon`, `git diff --check`.
- 테스트한 시나리오: 실제 DB에 `RECEIVED`·`PREPARING` 테스트 주문을 만들고 활성 주문 조회 결과를 확인했다. `84606f6` 커밋 전 컴파일 및 diff 검사를 통과했다.
- 확인 결과: Live 주문 조회와 주문 목록 관련 Java 컴파일은 통과했고 main 반영 이력도 확인했다. 메뉴 상세 Mapper의 Spring 기동 검증과 프론트 통합은 미완료다.

## 11. 포트폴리오용 요약

- Admin 운영 화면의 Live 주문·주문 목록·메뉴 조회를 실제 DB 뷰와 MyBatis DTO로 연결하고, 화면 목적에 맞게 응답 모델을 분리했다.

## 12. 첨부하면 좋은 자료

- 커밋: `94a9589`, `9e827fd`, `84606f6`, `638eb44`, `e700203`
- `ASAK-back/docs/view.sql`
- `AdminOrderMapper.xml`, `AdminMenuMapper.xml`
- Bruno: `api/admin/Admin Menu List total.bru`
