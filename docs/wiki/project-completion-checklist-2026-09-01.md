# ASAK 프로젝트 전체 완료 체크리스트

> 기준일: **2026-09-01**  
> 정본: [WBS](wbs.md) · [QA 테스트 케이스](qa-test-cases.md) · [릴리스/데모 운영 기준](../product_bible/09_QA_Bible/RELEASE_AND_DEMO_OPERATIONS.md)  
> **2026-09-02 종강 전:** [문서·코드 대조](admin-doc-code-verification-2026-09-02.md) · [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) · [Admin QA](qa-execution-report-2026-09-02.md) · [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md) · [발표 대본](graduation-presentation-script-2026-09-02.md)  
> **QA 요약 (9/2):** Admin API 22/24 · Kiosk API 17/18 · build Admin/Kiosk ✅ · **UI 브라우저 클릭·팀 검토 미완** → 완료 선언 불가
> **검증 스냅샷:** [§9 2026-09-02 항목별 검증](#9-2026-09-02-항목별-검증-스냅샷) — 아래 `- [ ]`는 **미완료 유지**. `△`/`✅`는 코드·문서 대조 결과이며 **완료 선언 아님**.  
> 원칙: 체크는 코드 존재가 아니라 **팀 검토 + 실행 근거 + 문서 기록**이 모두 있을 때만 한다. MVP 범위에서 제외할 항목은 `DONE`으로 바꾸지 말고, 근거와 함께 `EXCLUDED` 또는 범위 변경으로 남긴다.

## 0. 완료 선언 전 공통 조건

> **2026-09-02:** [§9.0](#90-완료-선언-전-공통-조건) — 전항 `❌` 또는 `△`. 체크박스 미체크 유지.

- [ ] 모든 활성 WBS가 `DONE`이거나 팀이 승인한 제외/보류 사유를 갖는다. — `❌`
- [ ] `TODO`, `IN_PROGRESS`, `IN_REVIEW`, `DELAYED` 항목을 WBS별로 재확인하고 상태·근거·담당자를 갱신한다. — `△`
- [ ] 변경한 코드/문서의 담당 팀원이 검토하고, 테스트 근거를 남긴다. — `△` [Admin QA](qa-execution-report-2026-09-02.md) · [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md) · [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) · 팀 검토 미완
- [ ] 각 저장소의 `git diff --check`, 빌드, 핵심 테스트를 다시 실행한다. — `△` Admin·Kiosk build ✅ · Backend `compileJava` ✅ · Admin API 22/24 · Kiosk API 17/18 · UI 클릭 미완
- [ ] 커밋·푸시·배포는 팀 승인 후 담당자가 직접 수행한다. — `❌`

## 1. 기획·범위·저장소 정리

> **2026-09-02:** [§9.1](#91-기획범위저장소-wbs-002013)

- [ ] **WBS-002** 브랜치·커밋·PR·작업 티켓 규칙을 팀 문서에 확정한다. — `△`
- [ ] **WBS-003** 메뉴·옵션 트리와 가격/선택 규칙을 팀 리뷰로 확정한다. — `△`
- [ ] **WBS-004** 사용자·관리자 화면 흐름과 기능을 최신 문서에 반영한다. — `△`
- [ ] **WBS-005** ERD와 API 목록을 실제 구현/미구현 상태와 비교해 확정한다. — `△`
- [ ] **WBS-008~009** 키오스크 정본 저장소와 미커밋/브랜치 이관 계획을 결정한다. — `△` 로컬 정본 · 클라우드 머지 금지
- [ ] **WBS-010** 요구사항·시나리오·Screen ID·API ID의 추적성 누락/중복을 정리한다. — `△`
- [ ] **WBS-011** MVP 포함 범위와 발표 이후 범위를 분리해 승인받는다. — `△` [종강 MVP](graduation-demo-mvp-2026-09-02.md)
- [ ] **WBS-012** 과거 API와 현재 API의 차이표를 실제 요청·응답 기준으로 갱신한다. — `△`
- [ ] **WBS-013** 운영 DB를 훼손하지 않는 점검/복구 절차를 확정한다. — `△`

## 2. Figma·화면 설계·접근성 기준

> **2026-09-02:** [§9.2](#92-figma화면접근성-wbs-014022)

- [ ] **WBS-014** 와이어프레임과 공통 컴포넌트 구조를 Figma/코드와 맞춘다. — `△`
- [ ] **WBS-016** Loading, Empty, Error, Disabled 상태를 화면별로 정의하고 문서·코드와 대조한다. — `△`
- [ ] **WBS-017~018** 키오스크·관리자 Screen ID별 Figma Frame/Node, 문구, 데이터 필드, 이동 경로를 매핑한다. — `△`
- [ ] **WBS-019~020** 디자인 누락과 담당자 작업 경계를 정리한다. — `△`
- [ ] **WBS-021** 글자 크기·색 대비·터치 대상 기준을 체크리스트화한다. — `❌`
- [ ] **WBS-022** 프로토타입 교체 보류 여부와 이유를 기록한다. — `△`

## 3. 키오스크 기능 완료

> **2026-09-02:** [Kiosk QA 보고](qa-kiosk-execution-report-2026-09-02.md) — API E2E **17/18 PASS** · UI 클릭 미검증

### 메뉴·장바구니

- [ ] **WBS-024** 메뉴 목록을 실제 API로 조회하고 Loading/Empty/Error/품절 상태를 확인한다. — `△` API **PASS** (`categories` 8 · `menuList` 72) · UI Loading/Empty 미검증
- [ ] **WBS-025~026** 메뉴 상세, 필수·선택 옵션, 담기 가능/불가 조건, 가격 합계를 확인한다. — `△` `menuDetail`·`cart/validate` **PASS** (menu 768 필수옵션·합계 11,400) · UI 미검증
- [ ] **WBS-027** 알레르기 정보의 조건부 표시를 실제 데이터로 검증한다. — `❌` API·UI 미검증
- [ ] **WBS-030** 수량 초과 안내가 4초간 정확히 노출되는지 확인한다. — `❌` UI 미검증
- [ ] **WBS-031** 수량 변경·삭제·비우기와 서버 장바구니 검증 결과를 확인한다. — `△` `cart/validate`·`CART_EMPTY` **PASS** · UI 조작 미검증

### 결제·완료·예외

- [ ] **WBS-032** 관리자 결제수단 활성 상태/정렬이 키오스크 결제수단 선택에 반영되는지 확인한다. — `❌` Kiosk 4종 조회 OK · **Admin CARD OFF → Kiosk 미반영 FAIL**
- [ ] **WBS-033** 결제 실패 시 장바구니와 사용자가 선택한 옵션이 유지되는지 확인한다. — `❌` UI·실패 시나리오 미검증
- [ ] **WBS-034** 결제 성공 뒤 주문번호·금액·대기정보가 승인 응답과 일치하는지 확인한다. — `△` API **PASS** (`orderNo`·`approvedAmount`·`waitingOrderNo`) · UI 미검증
- [ ] **WBS-035~036** 일반 화면 타임아웃과 결제 진행 중 타임아웃 제외를 확인한다. — `❌` UI 미검증
- [ ] **WBS-037** 키오스크 모든 핵심 화면의 Loading/Empty/Error/Disabled 상태를 점검한다. — `❌` UI 미검증
- [ ] **WBS-038** 실제 목표 화면 크기·터치 환경에서 48px 이상 터치 대상, 잘림, 스크롤, 재진입을 QA한다. — `❌` 실기기 QA 미기록

## 4. 관리자 기능 완료

> **2026-09-02:** Admin `npm run build` ✅ · 상세는 [§9.4](#94-관리자-wbs-039051) · 시연은 [발표 대본](graduation-presentation-script-2026-09-02.md).

- [ ] **WBS-039** 사이드바·라우트·화면 목록이 일치하는지 확인한다. — `△` 코드: `AdminApp.jsx`↔`AdminSidebar` 일치
- [ ] **WBS-040** 대시보드 위젯·최근 주문·부분 오류 상태와 DB 합계를 브라우저에서 확인한다. — `△` API **PASS** · UI 클릭 미검증
- [ ] **WBS-041** 실시간 주문 목록, 상세, 상태 표시, 페이지네이션을 확인한다. — `△` Live·상태변경 API **PASS** · TTS·UI 미검증
- [ ] **WBS-042~043** 주문 상태 전이, `READY` 주문 취소 성공, 승인 결제 직접 취소 차단, 환불 사유/중복/OTHER 오류, 관리자 화면 E2E를 확인한다. — `△` 전이·APPROVED취소409 **PASS** · **READY취소 500 FAIL** · 환불 스킵
- [ ] **WBS-044** 메뉴·재료·옵션 품절 저장/복구, 유효/무효 변경 혼합 시 전체 롤백, 화면 재조회와 고객 화면 반영을 확인한다. — `△` Admin PATCH **PASS** · Kiosk **MENU/OPTION PASS** · **INGREDIENT ing125 FAIL**
- [ ] **WBS-045** 메뉴 등록·수정·삭제를 실제 API/DB 흐름으로 확인한다(이미지 업로드는 MVP 제외). — `△` 목록·상세 API **PASS** · **Cloudinary `.env` 로컬 설정됨(9/2)** · Admin=미리보기만 · 서버 업로드 E2E 미검증
- [ ] **WBS-046** 결제수단 활성화·비활성화·`sortNo` 저장/재조회/실패 롤백과 키오스크 노출을 확인한다. — `△` Admin PATCH **PASS** · **Kiosk 반영 FAIL**
- [ ] **WBS-047~049** 매출 기간·월·일 필터, 차트/순위/시간대 데이터, Loading/Empty/Error 상태를 실제 API로 확인한다. — `△` API **PASS** (8/28=890300) · UI 클릭 미검증
- [ ] **WBS-050** Admin 전 화면에서 Loading, Empty, Error, Disabled, Confirm 동작을 QA한다. — `△` `AdminAsyncState` 주요 페이지 · 전 화면 QA 기록 없음
- [ ] **WBS-051** 날짜 필터·합계·메뉴 강조의 회귀 QA와 결과 기록을 완료한다. — `❌` 실행 기록 없음

## 5. 백엔드·DB·API 완료

> **2026-09-02:** `compileJava` ✅ · [§9.5](#95-백엔드dbapi-wbs-052066)

- [ ] **WBS-052** 추천 드레싱 데이터 정책을 확정하고 옵션 시드/API 응답을 검증한다. — `△`
- [ ] **WBS-053** 핵심 DB 제약조건·인덱스·외래키를 설계서와 실제 DB에서 대조한다. — `△`
- [ ] **WBS-054** 메뉴·재료·옵션 샘플 데이터의 정합성·재현 가능한 적재 절차를 검수한다. — `△`
- [ ] **WBS-055** 장바구니 주문 가능 검증 API의 재고·품절·필수 옵션·수량 한계 테스트를 완료한다. — `△` `cart/validate` **PASS** (품절·필수옵션·빈cart) · 수량 한계 미검증
- [ ] **WBS-056~057** 저장소/DB·migration·seed 운영 방식을 팀이 결정하고 문서화한다. — `△`
- [ ] **WBS-058~060** 메뉴 목록/상세, 주문 생성 API의 성공·빈값·오류·DB 반영을 확인한다. — `△` Kiosk menuList/detail/orders **PASS** · EAT_IN/TAKE_OUT DB 반영
- [ ] **WBS-061** 결제 승인·실패 API의 요청, 응답, 주문/결제 상태, idempotency, 실패 복구를 확인한다. — `△` CARD 승인·idempotency·중복409 **PASS** · 실패·PG 실연동 미검증
- [ ] **WBS-062** 품절 API의 MENU/INGREDIENT/OPTION_ITEM, 복수 변경 트랜잭션, 없는 ID 오류를 확인한다. — `△` MENU/OPTION Kiosk 반영 **PASS** · INGREDIENT ing125 **FAIL**
- [ ] **WBS-063** 관리자 주문 목록/상세/상태 변경 API를 실서버·DB에서 확인한다. — `△` Live·상태변경 API **PASS**
- [ ] **WBS-064** 일별·월별·시간대·순위 매출 View/API가 같은 계산 규칙을 사용하는지 확인한다. — `△` API **PASS** (8/28=890300) · UI 미검증
- [ ] **WBS-065** 모든 주요 API가 실제 HTTP 상태와 공통 `ApiResponse` 오류 코드/메시지를 일치시켜 반환하는지 확인한다. — `△` 주요 오류코드 검증(400/404/409) · 전수 미완
- [ ] **WBS-066** ERD·migration·실제 테이블·View·seed의 drift 보고서와 정정 계획을 확정한다. — `❌`

## 6. 시스템 연동·RTOS·합계

> **2026-09-02:** [§9.6](#96-연동rtos-wbs-067071)

- [ ] **WBS-067** 키오스크 → Spring API → DB의 최소 스모크 흐름을 기록한다. — `△` Kiosk menu→order→pay **PASS** · [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md)
- [ ] **WBS-068** `totalAmount`, `APPROVED`, `CANCELED`, `REFUNDED`, 주문 유형 등 공통 필드명이 Kiosk/Admin/backend에서 일치하는지 확인한다. — `△` `orderType`·`totalAmount`·`paymentStatus` API 확인
- [ ] **WBS-069** 키오스크 메뉴→옵션→장바구니→결제→완료의 실제 서버 E2E를 성공·실패 모두 실행한다. — `△` 성공 흐름 API **PASS** (TC-001~002) · 실패·UI 미검증
- [ ] **WBS-070** 관리자 로그인→주문→품절→결제수단→환불→매출의 실제 서버 E2E를 실행하고 mock 잔존 여부를 제거/기록한다. — `△` Admin API 대부분 **PASS** · 환불·UI 미검증
- [ ] **WBS-071** 주문·결제·취소·환불 후 `총매출 - 취소/환불액 = 순매출`을 일별/요약/월별/시간대에서 대조한다. — `△` 8/28=890300 API **PASS**
- [ ] RTOS가 MVP 범위라면 React 출력 요청 → Spring device event → Gateway → Console RTOS 결과 로그까지 시연한다. — `❌` **시연 제외**

## 7. 전체 QA·사용성·접근성

> **2026-09-02:** [§9.7](#97-전체-qa접근성-wbs-072079) · [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) 시연 당일

- [ ] **WBS-072** 키오스크 결제 실패, 네트워크 오류, 연속 터치, 뒤로가기, 타임아웃 예외를 QA한다. — `❌`
- [ ] **WBS-073** 사용자·관리자 핵심 시나리오를 처음부터 끝까지 수행하고 결과/버그/재현 절차를 남긴다. — `△` API E2E 기록 · **UI·브라우저 미검증**
- [ ] **WBS-074** 느린 화면, 혼동되는 문구/버튼, 중복 입력을 개선하고 전후 근거를 기록한다. — `❌`
- [ ] **WBS-075~076** 글자 크기·대비·키보드·터치 접근성 및 설정 화면 MVP 포함 여부를 확정한다. — `❌`
- [ ] **WBS-077** 요구사항별 테스트 결과를 PASS/FAIL/BLOCKED와 근거로 기록한다. — `△` [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) · P0 대부분 기록 · 접근성·UI 남음
- [ ] **WBS-078** 고대비, 키보드 탐색, 터치 사용성을 실제 환경에서 검증한다. — `❌`
- [ ] **WBS-079** Kiosk와 Admin을 함께 재시작해 전체 회귀 QA를 완료한다. — `❌`

## 8. 운영·발표·릴리스

> **2026-09-02:** [§9.8](#98-운영발표wbs-080085)

- [ ] **WBS-080** 주간 데모/회고와 남은 위험을 WBS에 반영한다. — `△` 9/1·9/2 문서화 · 주간 회고 기록 불완전
- [ ] **WBS-081** 발표 자료와 시연 순서를 실제 구현 범위로 작성한다. — `△` [발표 대본](graduation-presentation-script-2026-09-02.md) · [종강 MVP](graduation-demo-mvp-2026-09-02.md)
- [ ] **WBS-082** 팀원별 발표·질의응답·실패 시 대체 시연을 포함한 최종 리허설을 기록한다. — `❌` 리허설 기록 없음
- [ ] **WBS-083** README, Product Bible, Screen Bible, API 명세, WBS, QA 결과, 인수인계 자료의 내용이 일치하는지 확인한다. — `△` wiki·검증 문서 갱신 · 팀 최종 검토 남음
- [ ] **WBS-084** 모든 저장소 build/test, 환경변수·시크릿 점검, 롤백 기준, 배포 후보와 담당자를 확인한다. — `△` Admin·Kiosk build ✅ · API QA · **Backend Cloudinary `.env` 로컬 채움(9/2)** · 재시작·업로드 동작 검증·배포 근거 없음
- [ ] **WBS-085** 슬라이드·대본·데모 1~5 순서·비상 계획·최종 리허설을 팀 검토로 확정한다. — `△` 대본·TC 실행표·Plan B 문서화 · 슬라이드·팀 검토 남음

## 9. 2026-09-02 항목별 검증 스냅샷

> **검증일:** 2026-09-02 · **정본:** 로컬 `c:\ASAK-workspace`  
> **상세 대조:** [admin-doc-code-verification-2026-09-02.md](admin-doc-code-verification-2026-09-02.md) · **QA 실행:** [Admin](qa-execution-report-2026-09-02.md) · [Kiosk](qa-kiosk-execution-report-2026-09-02.md)
> **기호:** `✅` 코드·문서 일치·빌드 통과 · `△` 부분 충족·E2E·팀 검토 미완 · `❌` 미충족·미기록 · 체크박스 `- [ ]`는 **의도적으로 미체크 유지**

### 9.0 완료 선언 전 공통 조건

| # | 항목 | 판정 | 근거 |
| --- | --- | --- | --- |
| 0-1 | WBS 전부 DONE/EXCLUDED | ❌ | [wbs.md](wbs.md) IN_PROGRESS·IN_REVIEW 다수 |
| 0-2 | 상태·근거·담당자 갱신 | △ | 9/2 wiki 블록 추가 · 팀 승인 미완 |
| 0-3 | 담당자 검토·테스트 근거 | △ | [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) P0 기록 · 팀 승인 미완 |
| 0-4 | 빌드·핵심 테스트 재실행 | △ | Admin·Kiosk build ✅ · Backend compileJava ✅ · Admin API 22/24 · Kiosk API 17/18 · UI 클릭 미완 |
| 0-5 | 커밋·배포 팀 승인 | ❌ | 미실행 |

### 9.1 기획·범위·저장소 (WBS-002~013)

| WBS | 판정 | 비고 |
| --- | --- | --- |
| 002~004 | △ | Product Bible·wiki 존재 · **최종 팀 리뷰 기록 없음** |
| 005 ERD·API | △ | bible·backend 대체로 일치 · drift 미정리 |
| 008~009 저장소 | △ | 로컬 3저장소 운영 · **클라우드 Agent 중복=머지 금지** |
| 010~012 추적성·MVP | △ | [종강 MVP](graduation-demo-mvp-2026-09-02.md) · 범위 승인 문서화 불완전 |
| 013 운영 DB 절차 | △ | 실DB QA 기록(9/1) · 절차서 팀 확정 없음 |

### 9.2 Figma·화면·접근성 (WBS-014~022)

| WBS | 판정 | 비고 |
| --- | --- | --- |
| 014~018 | △ | Screen Bible·Figma 링크 존재 · **화면별 매핑 QA 미기록** |
| 019~020 | △ | WBS에 보류·담당 기록 일부 |
| 021~022 접근성·프로토타입 | ❌ | 체크리스트·실측 기록 없음 |

### 9.3 키오스크 (WBS-024~038)

| WBS | 판정 | 비고 |
| --- | --- | --- |
| 024 메뉴 목록 | △ | `categories` 8 · `menuList` 72 **PASS** · UI Loading/Empty 미검증 |
| 025~026 상세·옵션·합계 | △ | `menuDetail`·`cart/validate` **PASS** · UI 미검증 |
| 027 알레르기 | ❌ | 미검증 |
| 030~031 수량·장바구니 | △ | `CART_EMPTY`·검증 합계 **PASS** · UI 미검증 |
| 032 결제수단 Admin 반영 | ❌ | Kiosk 4종 조회 OK · **Admin OFF 미반영 FAIL** |
| 033 결제 실패 유지 | ❌ | UI·실패 시나리오 미검증 |
| 034 결제 성공 정보 | △ | `orderNo`·`approvedAmount`·`waitingOrderNo` **PASS** |
| 035~037 타임아웃·상태 | ❌ | UI 미검증 |
| 038 터치·해상도 | ❌ | 실기기 QA 없음 |
| **build** | ✅ | `npm install` 후 `npm run build` **PASS** |
| **API E2E** | △ | TC-001~003 **PASS** · [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md) |

### 9.4 관리자 (WBS-039~051)

§4 인라인 주석과 동일. **시연 권장 순서:** [발표 대본](graduation-presentation-script-2026-09-02.md).

| 핵심 | 판정 | 시연 고정값 |
| --- | --- | --- |
| 로그인 | △ | PIN `0001` · 빈값·오류 토스트(9/2) |
| Live 주문 | △ | 5초 폴링 · TTS · 취소 Confirm |
| 품절 | △ | MENU/OPTION Kiosk **PASS** · INGREDIENT ing125 **FAIL** · 시연은 **MENU 단위** 권장 |
| 결제수단 | △ | CARD on/off · 정책 문구=localStorage |
| 매출 | △ | 검증일 `2026-08-28` · `951,100 - 60,800 = 890,300` |
| 메뉴 편집 | △ | 이미지 **미리보기만** · Cloudinary env 로컬 설정 · 업로드 API E2E 미검증 |

### 9.5 백엔드·DB·API (WBS-052~066)

| WBS | 판정 | 비고 |
| --- | --- | --- |
| 052 드레싱 | △ | Admin Live **가짜 드레싱 제거(9/2)** · 시드 정책 미확정 |
| 053~057 DB·migration | △ | 실DB 운영 · 설계서 대조 보고서 없음 |
| 055 cart 검증 | △ | 품절·필수옵션·빈cart **PASS** |
| 058~060 메뉴·주문 | △ | Kiosk API **PASS** |
| 061 결제 | △ | CARD·idempotency·409 **PASS** |
| 062 품절 | △ | MENU/OPTION Kiosk OK · INGREDIENT FAIL |
| 063~064 주문·매출 | △ | Admin 연동 · 새 매출 UI **브라우저 재검증 필요** |
| 065 ApiResponse | △ | 주요 API 일치 · 전수 HTTP 테스트 없음 |
| 066 drift | ❌ | 보고서·정정 계획 없음 |
| **compile** | ✅ | `gradlew compileJava` (2026-09-02) |

### 9.6 연동·RTOS (WBS-067~071)

| WBS | 판정 | 비고 |
| --- | --- | --- |
| 067 스모크 | △ | Kiosk menu→order→pay **PASS** |
| 068 필드명 | △ | `orderType`·금액·결제상태 API 확인 |
| 069 Kiosk E2E | △ | 성공 API **PASS** (TC-001~002) · 실패·UI 미완 |
| 070 Admin E2E | △ | Admin API 대부분 **PASS** · 환불·UI 미완 |
| 071 매출 합계 | △ | 8/28=890300 **PASS** |
| RTOS | ❌ | **시연 제외** 권장 |

### 9.7 전체 QA·접근성 (WBS-072~079)

| WBS | 판정 | 비고 |
| --- | --- | --- |
| 072~074 예외·시나리오 | △ | API 오류코드 일부 **PASS** · UI·네트워크 예외 미완 |
| 077 TC 기록 | △ | [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) P0 기록 |
| 075~078 접근성 | ❌ | 실환경 검증 없음 |
| 079 회귀 QA | ❌ | Kiosk+Admin 동시 재시작 미기록 |

### 9.8 운영·발표 (WBS-080~085)

§8 인라인 주석과 동일. **종강 시연 문서:** [graduation-demo-mvp-2026-09-02.md](graduation-demo-mvp-2026-09-02.md).

| 항목 | 판정 |
| --- | --- |
| 대본·TC 실행표 | △ 작성·API PASS 기록 · UI 클릭·리허설 시연 당일 |
| 리허설·슬라이드 | ❌ |
| 배포·롤백 | ❌ |

### 9.9 시연 제외·Plan B · 알려진 FAIL

| 항목 | 처리 |
| --- | --- |
| RTOS·영수증 | 시연에서 언급만 · `receipt-print` API는 **PASS** |
| KAKAO/NAVER 환불 | CARD만 시연 |
| 메뉴 이미지 서버 업로드 | Cloudinary `.env` 로컬 설정(9/2) · 시연은 **미리보기** 또는 업로드 성공 시에만 데모 |
| 결제 정책 문구 | Admin localStorage · Kiosk 미반영 |
| **Admin CARD OFF → Kiosk** | **FAIL** — Admin만 시연 |
| **INGREDIENT ing125 품절** | **FAIL** — **MENU 품절**로 시연 대체 |
| **READY 주문 취소** | **FAIL** (500) — 시연 제외 |
| QA 테스트 주문 | `ASAK2609020001~` 등 DB 생성됨 · 시연 전 정리 여부 팀 판단 |
| UI 브라우저 클릭 | 시연 당일 · API PASS ≠ UI PASS |

## 완료 판정 기록

프로젝트 완료 선언 전 아래를 이 문서 끝에 남긴다.

| 항목 | 결과 | 근거 링크/명령 | 확인자 | 일자 |
| --- | --- | --- | --- | --- |
| WBS 최종 상태 | △ IN_REVIEW 다수 | [wbs.md](wbs.md#2026-09-02-로컬-코드-대조-종강-전) | | 2026-09-02 |
| Admin build/E2E | △ API QA ✅ UI △ | [QA 보고](qa-execution-report-2026-09-02.md) 22/24 PASS | Agent | 2026-09-02 |
| Backend test/API/DB | △ compileJava ✅ | API QA 동일 세션 · 9/1 실DB | Agent | 2026-09-02 |
| Kiosk build/E2E | △ API E2E ✅ UI △ | [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md) TC-001~003 PASS | Agent | 2026-09-02 |
| 통합 QA·접근성 | △ | [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) P0 API 기록 · UI·접근성·환불 남음 | Agent | 2026-09-02 |
| 발표 리허설 | △ | [발표 대본](graduation-presentation-script-2026-09-02.md) · [§9.8](#98-운영발표wbs-080085) | | 2026-09-02 |
| 배포 후보/롤백 | △ | Cloudinary env 로컬만 · WBS-084 미충족 | | 2026-09-02 |

> **2026-09-02 QA 근거:** Admin·Kiosk **API E2E**는 [TC 실행표](demo-tc-execution-sheet-2026-09-02.md)에 PASS/FAIL 기록됨. 체크박스 `- [ ]`는 **팀 검토·UI 클릭·완료 선언 전까지 미체크 유지**.  
> 알려진 FAIL: Admin 결제수단→Kiosk 미반영 · INGREDIENT ing125 품절 · READY 취소 500 · PG 실연동·환불 UI 미검증.
