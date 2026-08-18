# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-076)

> Status: **HISTORY**
> 인라인 주석 태그: `TODO-NNN`
> **번호 순 = 교사 우선순위** (주문 → 메뉴 → 품절 → 결제수단 → 매출 → 대시보드)
> 파일 상단에 모아 두지 않고, **해당 코드 위치**에만 달아 두었다.
> 검색: `TODO-00` / `TODO-0` / `TODO-`
> 진행 갱신: 2026-08-06 (오늘 작업 순서 재정렬: 메뉴 조회 먼저)
> 2026-08-18 overlay: 기존 8/5~8/6 TODO 기록은 보존하고, 아래에 **현재 코드 기준 후속 순서**만 덧붙인다.
> 작업 원칙: **기능별로 화면–API–DB 결과를 함께 확인**하며 진행한다.
> 상세 검증: [`admin-feature-verify-todos-2026-08-06.md`](admin-feature-verify-todos-2026-08-06.md)

## 2026-08-18 현재 후속 순서 오버레이

> 아래 표는 기존 TODO 번호를 **지우지 않고**, 현재 남아 있는 인라인 TODO와 최근 반영 사항을 기준으로 다시 읽기 쉽게 정리한 것이다.

| 순위 | 구간 | 관련 TODO | 현재 상태 | 다음 행동 |
|---|---|---|---|---|
| **1** | 품절 줄기 | **040~043** | 미착수 | `040→041` 백엔드 뒤 `042→043` 프런트 연결 |
| **2** | 결제수단 줄기 | **044~047** | 미착수 | `044→045` 백엔드 뒤 `046→047` 프런트 연결 |
| **3** | 매출 API | **048~055** | 미착수 | `048~051` 백엔드 집계·DTO를 먼저 확정하고 `052~055` 프런트 연결 |
| **4** | 대시보드 API | **056~058** | 미착수 | summary/monthly/daily 이후 `056→057→058` 순서로 연결 |
| **5** | Live 보드 구조 정리 | **059** | 보류 | 기능 급한 줄기(품절/결제수단/매출) 이후 가로 스크롤 구조 정리 |
| **6** | 로그인/JWT/보호 라우트 | **060~070** | 미착수 묶음 | `060→061→062→063` 백엔드 인증 줄기 뒤 `064→067`, `065→066→068`, `069→070` 순으로 연결 |
| **7** | 환불/영수증 Future | **071~076** | Future | 현재 계약 정리 후 별도 범위로 진행 |

### 2026-08-18 반영 완료 메모

- 주문/결제 상태 계약 정리:
  - `API-005` 응답은 `status=READY`
  - `API-006` 요청은 `orderStatus=READY` 포함
  - `API-006` 응답은 `paymentStatus` 유지
- 관리자 Live 보드:
  - `READY` 주문은 `대기중`으로 표시
  - `준비 시작` 버튼은 비활성화
- 관련 반영 저장소:
  - `ASAK-back` 반영 완료
  - `ASAK-Admin` 반영 완료
  - `ASAK` 문서 동기화 및 반영 완료

### 이번 주 권장 일정 (8/19~8/22)

| 날짜 | 권장 작업 |
|---|---|
| **8/19** | `040~045` 품절·결제수단 백엔드 (`WBS-044`, `WBS-046`, `WBS-063`) |
| **8/20** | `042~047` 품절·결제수단 프런트 연결 |
| **8/20~8/21** | `048~051` 매출 백엔드 집계 (`WBS-064`) |
| **8/21** | `052~058` 매출/대시보드 프런트 연결 (`WBS-040`, `WBS-047~049`, `WBS-051`) |
| **8/22** | `059`, `060~070` 로그인/JWT/경로 canonical 재정리 |
| **후순위** | `059`, `071~076` |

### WBS 기준 해석 메모 (2026-08-18)

- 정본 일정 기준:
  - `WBS-040~051`은 **관리자 화면 연동/QA** 줄기다.
  - `WBS-063~066`은 **관리자 주문·매출·오류응답·DB 점검** 백엔드 줄기다.
  - `WBS-070~071`은 **관리자 실서버 연동과 매출 검증** 줄기다.
- 실제 코드 기준:
  - `ASAK-Admin`은 주문/라이브/대시보드/매출/결제수단/품절 화면 뼈대와 mock 흐름이 이미 있다.
  - `ASAK-back`은 주문 조회/상태 변경은 일부 구현됐지만, 로그인(`060~063`), 매출/대시보드(`048~056`), 품절/결제수단(`040~047`)은 아직 TODO 주석 단계가 많다.
- 따라서 이번 문서의 우선순위는 **현재 WBS 이번 주 우선(08/17~08/21)** 중에서, 담당 범위인 관리자/백엔드만 추린 실행 순서다.
- 로그인(`060~070`)은 현재 코드상 큰 미착수 묶음이지만, `wbs.md`의 이번 주 최우선 축에는 직접 올라와 있지 않으므로 **품절/결제수단/매출/대시보드 뒤**로 둔다.

### 이미 반영된 진행 기준

- `WBS-041` 관련:
  - 라이브 보드에서 `READY` 주문은 `대기중`으로 보이고 버튼이 비활성화되도록 반영됨.
- `WBS-070` 관련:
  - 관리자 실서버 연동은 주문 일부/메뉴 일부는 진행됐지만, 로그인·매출·품절·결제수단은 아직 mock/API TODO가 남아 있음.
- `WBS-064` 관련:
  - 매출/대시보드 API는 Controller/Service/Mapper와 프런트 hook/api에 TODO가 그대로 남아 있어 이번 주 실작업 축으로 보는 것이 맞다.

### 인라인 TODO 기준 해석 메모

- 번호 정본은 이 문서보다 **코드 인라인 `TODO-NNN`** 이다.
- 이 문서는 "지금 무엇부터 할지"를 읽기 쉽게 정리한 인덱스다.
- 기존 표의 상세 설명은 유지하고, 실제 착수 순서는 이 오버레이를 우선 참고한다.

## 오늘 작업 우선순위 (8/5 + 8/6 합본)

| 순위 | 작업 | 인라인 TODO | 비고 |
|---|---|---|---|
| **1** | 메뉴 **목록·상세 조회** FE 실연동 + 검증 | **015·016** | BE GET 있음. 목록 0건=`MENU_NOT_FOUND` 제거. **등록보다 조회 먼저** |
| **2** | 메뉴 **등록·수정** BE → FE | **017~025** | 기본 필드만. Create/Update Request 정리됨 |
| **3** | 메뉴 **삭제** BE → FE | **026~028·030·031** | 8/6. 스키마 제약 확인 |
| **4** | 품절 C→S→M | **032~039** | 8/6 |
| **5** | 결제수단 C→S→M | **040~047** | 8/6 |
| 병행 | 주문 통합 테스트 | **008·010·012** + 검증 | 8/5. 메뉴 조회 줄기 후·여유 시 |
| 후순위 | 매출 → 대시보드 | **048~058** | 오늘 필수 아님 |
| 보류 | TTS·Live스크롤·로그인·키오스크·문서 | **059**, 013a~d, 060~ | 8/6 키오스크·문서는 관리자 메뉴 줄기 이후 |

## 번호 재매핑 (2026-08-06)

| 구간 | 구 번호 | 신 번호 |
|---|---|---|
| 메뉴 CRUD | 032~048 | **015~031** |
| 품절 | 015~022 | **032~039** |
| 결제수단 | 024~031 | **040~047** |
| 매출 | 049~056 | **048~055** |
| 대시보드 | 057~059 | **056~058** |
| Live 가로스크롤 | 023 | **059** |
| 주문 잔여·인증·Future | 008·010·012, 060~076 | 유지 |
| 완료 주석 제거 | 007, 013(기본 TTS) | IDE TODO에서 제거 |

## 진행 요약

| 상태 | 번호 |
|---|---|
| 완료(주석 제거) | **001~007**, **009**, **011**, **013**(기본 TTS), **014** |
| 완료 | **015**, **016** |
| 부분/잔여 | **008**, **010**(코드테이블화 진행), **012**(hook 수정·화면확인) |
| 진행 중 | **017~025** (메뉴 등록·수정 설계/연결), **032~039**, **040~047** |
| 미착수 | **026~031**, **048~076** |

다음 착수: **① 메뉴 등록·수정(T-3~T-6)** → **② 메뉴 삭제(T-7)** → **③ 품절·결제수단 C→S→M** → (여유) 주문 검증 · 매출·대시보드

### 진행 로그

| 날짜 | 내용 |
|---|---|
| 2026-08-06 | 오늘 순서를 메뉴 **조회 먼저**로 재정렬. Request DTO MVP 정리. Empty/Error·Live 빈목록 수정. |
| 2026-08-06 | 메뉴 조회 실연동 반영: `useMenusQuery`가 `PageResult` 기준으로 목록/필터/페이지네이션 연동, `AdminMenuController.getMenus`는 빈 목록도 200으로 응답. |
| 2026-08-06 | 문서·DevCopilot 동기화(코드 기준). 주문 BE/FE 연동은 구현됨·**미검증**. 메뉴 POST/PATCH/DELETE는 미구현. |

---

### P1 · 주문 잔여 (통합 테스트와 함께)

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **008** | 🟡 부분 | `AdminOrderService.cancelOrder` | ① APPROVED 취소 정책 확정 ② 환불 흐름 분리 여부 결정 ③ Controller/ErrorCode 기준 정리 |
| **010** | ✅ 완료 | `AdminOrderMapper.xml` cancel | `status_id=43` 제거, `findOrderStatusId("CANCELED")` 사용 |
| **012** | 🟡 부분 | `useOrdersQuery.js` | ① Empty/Error 분리 반영 ② 필터 쿼리 정합 확인 ③ OrderManagement 화면 수동 검증 |

상세 검증 ID: `P1-1`~`P1-9` → 검증 투두 문서

### P2 · 메뉴 (015~031) — SCR-016 · 조회→등록·수정→삭제

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **015** | ✅ 완료 | `useMenusQuery.js` | mock 제거, `menusApi.listMenus` / `getMenu` + `PageResult` 페이지네이션 연동 |
| **016** | ✅ 완료 | `AdminMenuController.getMenus` | 목록 0건 → 200+빈 `PageResult` (`MENU_NOT_FOUND` 제거) |
| **017** | ⬜ 진행 중 | `AdminMenuMapper.java` | `insertMenu` 선언 → XML INSERT → generated key 반환 |
| **018** | ⬜ 진행 중 | `AdminMenuService.createMenu` | 이미지 저장 → request + imageUrl로 INSERT → 요약 응답 연결 |
| **019** | ⬜ 진행 중 | `AdminMenuController` | POST 바인딩 방식 결정(JSON/multipart) → service 호출 → 성공 응답 |
| **020** | ⬜ 진행 중 | `AdminMenuMapper.java` | `updateMenu` 선언 → XML UPDATE → 수정 건수 반환 |
| **021** | ⬜ 진행 중 | `AdminMenuService` | menuId 기준 update 호출 → 존재하지 않음/성공 기준 정리 |
| **022** | ⬜ 진행 중 | `AdminMenuController` | PATCH 바인딩 → service 호출 → `MENU_NOT_FOUND`/성공 응답 |
| **023** | ⬜ 진행 중 | `menusApi.js` | `createMenu(payload)` 추가 → 백엔드 POST 규격 연결 |
| **024** | ⬜ 진행 중 | `menusApi.js` | `updateMenu(menuId, payload)` 추가 → 백엔드 PATCH 규격 연결 |
| **025** | ⬜ 진행 중 | `MenuManagePage.jsx` | create/edit 분기 호출 → 성공 refetch/optimistic update → 실패 toast 처리 |
| **026** | ⬜ 오늘③ | `AdminMenuMapper.java` | 삭제 정책 확정 후 `deleteMenu`/`updateMenuActive` 선언·XML 구현 |
| **027** | ⬜ 오늘③ | `AdminMenuService` | 삭제 service 구현 → 정책(soft/hard) 반영 |
| **028** | ⬜ 오늘③ | `AdminMenuController` | DELETE endpoint → 성공/실패 응답 규격 정리 |
| **029** | ⬜ 후순위 | Mapper + Controller | ingredients |
| **030** | ⬜ 오늘③ | `menusApi.js` | `deleteMenu(menuId)` 추가 |
| **031** | ⬜ 오늘③ | `MenuManagePage.jsx` | 삭제 확인 → API 호출 → refetch/선택 메뉴 이동/view 복귀 |

> CreateMenuRequest / UpdateMenuRequest 기본 필드 DTO는 정리 완료(별도 TODO 번호 없음).

상세 검증: `T-1`~`T-7` ([검증 투두](admin-feature-verify-todos-2026-08-06.md))

### P3 · 품절 (032~039) — SCR-011

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **032** | ✅ 완료 | `SoldOutPatchRequest.java` | DTO 필드(`targetType`, `targetId`, `isSoldOut`) |
| **033** | ⬜ | `AdminSoldOutMapper` + XML | ① 대상별 SELECT ② 공통 row shape 정리 ③ XML 추가 |
| **034** | ⬜ | 동상 | ① targetType 분기 ② `is_sold_out` 토글 UPDATE ③ 변경 건수 반환 |
| **035** | ⬜ | `AdminSoldOutService.java` | ① 조회 메서드 ② patch 메서드 ③ 실패/롤백 기준 정리 |
| **036** | ⬜ | `AdminSoldOutController.java` | ① GET 응답 ② PATCH 바인딩 ③ ErrorCode 규격 정리 |
| **037** | ⬜ | `soldOutApi.js` | ① `listSoldOutCatalog()` 추가 ② 초기 load 연결 |
| **038** | ⬜ | `soldOutApi.js` | ① `patchSoldOut(body)` 추가 ② body 규격 정리 |
| **039** | ⬜ | `useSoldOutDraft.js` | ① mock load 교체 ② mock save 교체 ③ baseline 롤백 유지 |

상세 검증: `P3-1`~`P3-4`

### P4A · 결제수단 (040~047) — SCR-018

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **040** | ✅ 완료 | `PatchPaymentMethodRequest.java` | DTO 필드(`status`, `sortOrder`, `receiptMessage`) |
| **041** | ⬜ | `AdminPaymentMethodMapper` + XML | ① 목록 SELECT ② row shape 정리 ③ XML 추가 |
| **042** | ⬜ | 동상 | ① methodId 기준 UPDATE ② 변경 건수 반환 |
| **043** | ⬜ | `AdminPaymentMethodService.java` | ① 목록 메서드 ② patch 메서드 ③ 0건 처리 기준 정리 |
| **044** | ⬜ | `AdminPaymentMethodController.java` | ① GET 목록 ② PATCH 바인딩 ③ 응답/ErrorCode 규격 |
| **045** | ⬜ | `paymentMethodsApi.js` | ① `listPaymentMethods()` 추가 ② 초기 load 연결 |
| **046** | ⬜ | `paymentMethodsApi.js` | ① `patchPaymentMethod()` 추가 ② 저장 방식(순차/일괄) 확정 |
| **047** | ⬜ | `usePaymentMethodDraft.js` | ① mock load 교체 ② mock save 교체 ③ baseline 롤백 유지 |

상세 검증: `P4A-1`~`P4A-2`

### P4B · 매출 (048~055) — SCR-019/020/021

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **048** | ⬜ | `AdminStatsController` | sales/summary |
| **049** | ⬜ | 동상 | sales/monthly |
| **050** | ⬜ | 동상 | sales/daily |
| **051** | ⬜ | Stats Service/Mapper | 집계 |
| **052** | ⬜ | `salesApi.js` | getSummary |
| **053** | ⬜ | `salesApi.js` | getMonthly |
| **054** | ⬜ | `salesApi.js` | getDaily |
| **055** | ⬜ | `useSalesQuery.js` | mock → API |

상세 검증: `P4B-1`~`P4B-3`

### P4C · 대시보드 (056~058) — SCR-022

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **056** | ⬜ | `AdminStatsController` | dashboard |
| **057** | ⬜ | `adminApi.js` | getDashboard |
| **058** | ⬜ | `useDashboard.js` | mock → API |

상세 검증: `P4C-1`

### 보류 · Live UX · TTS 명세 · 인증 · Future

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **059** | ⬜ 보류 | `LiveOrderPreview.jsx` | 가로 스크롤 (구 023) |
| **013a~d** | ⬜ 보류 | TTS | 중복방지·Queue·Mute·localStorage |
| **060** | ⬜ | `AdminAuthController` | POST /login |
| **061** | ⬜ | `JwtTokenProvider.java` | JWT |
| **062** | ⬜ | `JwtAuthenticationFilter.java` | 필터 |
| **063** | ⬜ | `SecurityConfig.java` | authorize |
| **064** | ⬜ | `adminApi.js` | login |
| **065** | ⬜ | `adminSession.js` | token |
| **066** | ⬜ | `apiClient.js` | Bearer + 401 |
| **067** | ⬜ | `LoginPage.jsx` | 실로그인 |
| **068** | ⬜ | `useAdminAuth.js` | 401 가드 |
| **069** | ⬜ | `AdminApp.jsx` | 정본 경로 |
| **070** | ⬜ | `apiClient.js` | 403 매핑 |
| **071** | ⬜ Future | `AdminOrderController` | refund |
| **072** | ⬜ Future | `AdminOrderMapper.xml` | payments 환불 |
| **073** | ⬜ Future | `ordersApi.js` | refundOrder |
| **074** | ⬜ Future | `ordersApi.js` | printReceipt |
| **075** | ⬜ Future | `OrderManagementPreview.jsx` | 환불 UI |
| **076** | ⬜ Future | `OrderManagementPreview.jsx` | 영수증 UI |

## 사용법

1. IDE TODO 패널을 번호순으로 보면 **교사 우선순위**와 같다.
2. 각 기능은 **화면–API–DB**를 함께 확인한 뒤 다음 번호로 넘어간다.
3. 완료한 항목은 인라인 주석을 지우고, 이 표 상태를 ✅로 갱신한다.
4. 이 표와 코드 주석이 어긋나면 **코드 인라인을 정본**으로 맞춘다.
