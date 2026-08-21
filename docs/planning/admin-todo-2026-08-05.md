# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-043)

> Status: **CURRENT IMPLEMENTATION ROADMAP**
>
> 갱신: **2026-08-21**. 이 문서는 `ASAK-Admin`과 `ASAK-backend`의 원격 `main` 코드, 현재 Product/Screen Bible을 대조한 결과다.
>
> 정본 우선순위는 **실제 코드와 Git 상태 → 이 문서 → Product/Screen Bible → Figma**다. 문서의 완료 표시는 브라우저·실DB E2E 성공을 뜻하지 않는다. 별도 표기가 없으면 컴파일 또는 프론트 빌드까지만 확인된 상태다.
>
> 인라인 태그 `TODO-NNN`은 번호를 재사용하거나 재정렬하지 않는다. 이미 구현된 코드에 과거 TODO가 남은 경우에는 **주석 정합화 대기**로 기록한다.

## 1. 현재 상황 요약

| 상태 | TODO | 현재 근거 | 남은 확인 |
| --- | --- | --- | --- |
| ✅ 코드 구현·빌드 확인 | 003~004 | 메뉴 CRUD API와 Admin 연결 존재 | 실제 DB/브라우저 E2E, Figma 상태 대조 |
| ✅ 코드 구현·빌드 확인 | 007~010 | 품절 GET/PATCH, DB Mapper, draft 훅 연결 존재 | 실제 DB 요청 1건, 실패·롤백 API 확인 |
| ⬜ 미구현·Mock 유지 | 011~014 | 결제수단 Controller/API는 빈 껍데기, draft는 mock 사용 | API 경로·DTO·저장 정책 결정 후 구현 |
| ✅ 코드 구현·빌드 확인 | 015~025 | sales summary/monthly/daily/time-slots, dashboard API·FE 호출 존재 | DB View 배포 및 Bruno/브라우저 E2E |
| ⬜ 미구현 | 027~037 | 로그인/JWT/보호 경로는 TODO 주석과 stub 상태 | 인증 계약·보안 정책 결정 후 구현 |
| ⬜ 정책 선행 | 001, 038~043 | 취소와 승인 결제 환불을 분리하는 계약만 존재 | 환불 상태 전이·SQL·UI·영수증 책임 확정 |

### 검증 상태 표기

- **코드 구현·빌드 확인**: 소스 연결을 확인했고, `ASAK-backend` `compileJava`, `ASAK-Admin` `npm run build`가 과거 실행에서 통과했다. 서버 기동·실제 DB·브라우저 E2E는 별도다.
- **Mock 유지**: 화면은 보이지만 저장·조회가 실제 API/DB와 연결되지 않았다.
- **정책 선행**: API를 먼저 만들면 주문/결제 데이터 의미가 달라질 수 있어 팀 결정이 필요하다.

## 2. 화면·정본 계약 대조

| Screen ID | Figma 기준 | 실행 경로 | 구현 상태 | 결정/검증 필요 |
| --- | --- | --- | --- | --- |
| SCR-011 품절 관리 | Default `39:8577`, Loading `51:13887`, Empty `51:14020`, Error `51:14181`, Save `39:8653` | `/sold-out` | 메뉴·재료 탭은 DB 연동. 옵션 항목은 API에는 포함하지만 탭은 숨김 | 화면 경로는 Bible의 `/soldOut`과 다름. 메뉴/재료만 노출한다는 UX 결정을 문서 정본에 반영할지 결정 |
| SCR-018 결제수단 | `39:8203` | `/payment-methods` | mock 화면 | Bible의 `/paymentMethods`, Controller의 `/api/admin/paymentMethods` 표기 불일치 결정 필요 |
| SCR-019 매출 요약 | Default `39:7405` 등 | `/sales` | API·adapter·query 연결 | 실제 View 데이터와 KPI/차트 합계 E2E |
| SCR-020 월별 매출 | `39:7701` | `/sales/monthly` | API·adapter·query 연결 | 연도 경계·빈 월·실DB 확인 |
| SCR-021 일별 매출 | `39:7894` | `/sales/daily` | daily + 별도 time-slots API 연결 | 10:00~22:00 30/60분 0-fill 실DB 확인 |
| SCR-022 대시보드 | Figma 상세 노드 미기록 | `/dashboard` | API·adapter·hook 연결 | 위젯별 partial error와 실DB 확인 |

## 3. 인라인 TODO 현황과 구현 단위

아래의 **권장 인라인 TODO**는 소스에 새로 넣었다는 뜻이 아니다. 현재 소스의 TODO 문구가 구현 상태와 어긋나는 곳을 팀원이 정리할 때, 해당 함수/파일 위치에 한 항목씩 붙일 내용이다. 코드 수정은 별도 `코드 수정 승인` 범위에서만 한다.

### P1 · 주문 취소·환불·영수증 (TODO-001, 002, 038~043)

| TODO | 현재 상태 | 실제 위치 | 다음 구현 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 001 | ⬜ 정책 선행 | `AdminOrderService.cancelOrder` | 승인 결제 취소와 미승인 주문 취소의 상태표 확정 | `TODO-001: APPROVED 결제는 cancel이 아닌 refund 계약으로 분리하고, 주문/결제 상태·멱등성·409 기준을 확정한다.` |
| 002 | ✅ 코드 존재 | `useOrdersQuery.js` | 필터·empty·error를 실 API로 회귀 확인 | `TODO-002: status/date/page 쿼리가 API 계약과 같은지, 빈 목록·재시도·오래된 응답 무시를 브라우저에서 확인한다.` |
| 038 | ⬜ | `AdminOrderController` | `PATCH /api/admin/orders/{orderId}/refund` 계약 확정 | `TODO-038: COMPLETED + APPROVED만 환불 가능하도록 요청/응답/ErrorCode를 TODO-001 정책에 맞춰 구현한다.` |
| 039 | ⬜ | `AdminOrderMapper.xml` | refund SQL과 조회 SQL 분리 | `TODO-039: payment.refunded_at을 기록하고 paid_at은 보존하며, 0건 update와 중복 환불을 409로 구분한다.` |
| 040 | ⬜ | `ordersApi.js` | refund API 메서드 추가 | `TODO-040: refundOrder는 확정된 path/body를 그대로 호출하고 ApiResponse 오류를 화면으로 전달한다.` |
| 041 | ⬜ | `ordersApi.js` | 영수증 출력 책임 확정 | `TODO-041: 브라우저 인쇄·서버 PDF·RTOS 출력 중 책임을 정한 뒤 printReceipt API를 추가한다.` |
| 042 | ⬜ | `OrderManagePage.jsx` | 환불 확인 UI | `TODO-042: 환불 가능 상태만 버튼을 열고, 확인 대화상자·중복 클릭 방지·성공 후 목록 재조회 흐름을 연결한다.` |
| 043 | ⬜ | `OrderManagePage.jsx` | 영수증 UI | `TODO-043: 출력 요청 중 상태와 실패 메시지를 표시하고, 주문번호 기준으로 재시도 가능하게 한다.` |

### P2 · 메뉴 관리 (TODO-003~006, SCR-016)

| TODO | 현재 상태 | 실제 위치 | 다음 구현 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 003 | ✅ 코드 구현 | `AdminMenuController`, `menusApi` | POST/PATCH/DELETE 실 DB E2E | `TODO-003: CreateMenuRequest 검증 실패·이미지 없는 메뉴·soft delete 후 조회 제외를 API와 화면에서 확인한다.` |
| 004 | ✅ 코드 구현 | `MenuManagePage.jsx` | 삭제 후 선택/페이지 상태 QA | `TODO-004: 삭제된 메뉴가 선택 상태·상세 패널·현재 페이지에 남지 않는지 회귀 확인한다.` |
| 005 | 🟡 QA 잔여 | `MenuEditPanel.jsx` | 재료 검색/페이지 결과 확인 | `TODO-005: 재료 서버 검색의 query/page/empty/error와 선택 결과가 저장 body에 반영되는지 확인한다.` |
| 006 | 🟡 QA 잔여 | `MenuEditPanel.jsx` | 재료 추가·저장 수동 QA | `TODO-006: 재료 추가·삭제·중복 방지·저장 후 재진입을 실제 DB로 확인한다.` |

### P3 · 품절 관리 (TODO-007~010, SCR-011)

**현재 구현 사실**

- `GET /api/admin/soldOut`은 `menu`, `ingredient`, `opt_item`의 `sold_out`을 하나의 카탈로그 row로 조회해 `available`과 `soldOut` 배열로 나눈다.
- `PATCH /api/admin/soldOut` body는 `{ changes: [{ targetType: "MENU" | "INGREDIENT" | "OPTION_ITEM", targetId, isSoldOut }] }`이다.
- Service는 빈 요청·중복 target·잘못된 targetId를 거절하고 `@Transactional` 안에서 전체 변경을 처리한다. 하나라도 대상이 없으면 예외로 전체 롤백된다.
- Admin `useSoldOutDraft`는 최초 GET, 화면 내 이동, 변경분만 PATCH, 실패 시 baseline 복원을 수행한다.
- 화면 탭은 사용자 결정대로 `MENU`, `INGREDIENT`만 보인다. `OPTION_ITEM`은 DB/API에 포함되지만 UI 탭은 숨김이다.

| TODO | 현재 상태 | 실제 위치 | 남은 구현/검증 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 007 | ✅ 코드 구현·주석 정리 필요 | `AdminSoldOutController.java` | 200/검증 실패/없는 대상 요청을 Bruno로 확인 | `TODO-007: 구현 완료. GET/PATCH의 성공·빈 changes·중복 target·없는 target 응답 코드와 message를 Bruno로 고정한다.` |
| 008 | ✅ 코드 구현·주석 정리 필요 | `AdminSoldOutService`, `AdminSoldOutMapper`, XML | 실제 DB 1건 저장 및 롤백 확인 | `TODO-008: 구현 완료. menu/ingredient/opt_item별 sold_out 저장, 복수 changes 전체 롤백, 오류 코드 의미를 실DB로 검증한다.` |
| 009 | ✅ 코드 구현·주석 정리 필요 | `soldOutApi.js` | API 오류 형식과 endpoint 상수 점검 | `TODO-009: 구현 완료. ApiResponse unwrap 뒤 available/soldOut shape와 4xx 오류 전달을 네트워크 탭에서 확인한다.` |
| 010 | ✅ 코드 구현·주석 정리 필요 | `useSoldOutDraft.js` | loading/empty/error/dirty/saveConfirm 브라우저 QA | `TODO-010: 구현 완료. 저장 성공 baseline 갱신, 실패 롤백, 빠른 재시도와 화면 이탈 후 재진입을 확인한다.` |

**품절 데이터/표시 주의점**

- DB 컬럼은 `menu.sold_out`, `ingredient.sold_out`, `opt_item.sold_out`이다. 재료 이미지는 `ingredient.photo_asset_id → media_asset.url`이 없을 수 있으므로 화면은 fallback 이미지를 사용한다.
- Product Bible은 재료/옵션 품절에서 메뉴에 미치는 파생 품절과 영향 메뉴 표시를 권장한다. 현재 구현은 각 테이블의 직접 `sold_out` 토글만 저장하며, `effectiveSoldOut` 계산·영향 메뉴 목록은 **미구현**이다.
- 현재 오류에 `INVALID_ORDER_REQUEST` 등 주문 중심 ErrorCode가 재사용된다. 품절 전용 ErrorCode 도입은 계약 변경이므로 팀 결정 후 별도 작업으로 분리한다.

### P4A · 결제수단 설정 (TODO-011~014, SCR-018)

| TODO | 현재 상태 | 실제 위치 | 다음 구현 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 011 | ⬜ | `AdminPaymentMethodController` | API 경로를 `/api/admin/payment-methods` 또는 기존 camelCase 중 하나로 결정 | `TODO-011: 경로와 GET/PATCH 단위를 정한 뒤, path id만 받고 active/sortOrder 검증을 Controller에 구현한다.` |
| 012 | ⬜ | `AdminPaymentMethodService`, Mapper, DTO | `pay_method_cfg` row/DTO 확정 | `TODO-012: DTO 직렬화 필드를 active로 통일하고, 정렬 충돌·없는 id·0건 update의 오류 규칙을 Service transaction에 구현한다.` |
| 013 | ⬜ | `paymentMethodsApi.js` | GET/PATCH 실제 호출 | `TODO-013: 확정된 endpoint와 DTO로 list/patch 메서드를 만들고, 409·검증 오류를 throw하여 훅이 처리하게 한다.` |
| 014 | ⬜ Mock 유지 | `usePaymentMethodDraft.js` | mock load/save 교체 | `TODO-014: mock repository를 API로 교체하고, 성공 시 서버 응답으로 baseline 갱신·실패 시 이전 baseline 복원을 유지한다.` |

### P4B · 매출 분석 (TODO-015~022, SCR-019~021)

**현재 구현 사실**

- Backend: `GET /api/admin/sales/summary`, `/monthly`, `/daily`, `/daily/time-slots`가 `AdminSalesController → Service → Mapper` 구조로 존재한다.
- time-slots 계약은 `date=YYYY-MM-DD`, `intervalMinutes=30|60`이며 Service가 10:00~22:00 영업시간 구간을 0-fill 한다. 당일은 미래 슬롯을 포함하지 않는다.
- Frontend: `salesApi.js`, `useSalesQuery.js`, `salesAdapter.js`, 매출 페이지가 API 결과를 view model로 변환한다.
- DB 집계 View와 실제 API/Bruno 응답은 이 문서 갱신 시점에 재실행하지 않았다. **구현/빌드 확인과 DB E2E를 구분한다.**

| TODO | 현재 상태 | 실제 위치 | 남은 구현/검증 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 015 | ✅ 코드 구현 | `AdminSalesController` summary | today/week/month/custom 및 잘못된 날짜 Bruno 확인 | `TODO-015: 구현 완료. period와 startDate/endDate 상호 배타 규칙, 미래 날짜·역전 범위 오류를 API로 고정한다.` |
| 016 | ✅ 코드 구현 | `AdminSalesController` monthly | 연도 범위·빈 월 실DB 확인 | `TODO-016: 구현 완료. year 범위 오류와 0매출 월의 반환 shape를 Bruno/브라우저로 확인한다.` |
| 017 | ✅ 코드 구현 | `AdminSalesController` daily/time-slots | date/range/30·60분 슬롯 E2E | `TODO-017: 구현 완료. daily 범위와 time-slots 단일일 계약을 혼용하지 않고, 10:00~22:00 0-fill을 실DB로 확인한다.` |
| 018 | ✅ 코드 구현·DB 검증 대기 | `AdminSalesService`, `AdminSalesMapper.xml` | 집계 View 배포 여부·합계 대조 | `TODO-018: 구현 완료. vw_sales_daily와 30분 View가 배포됐는지 확인하고, DB 실매출만 집계한 뒤 Service가 0을 채우는지 검증한다.` |
| 019 | ✅ 코드 구현 | `salesApi.js` | summary query/오류 전달 확인 | `TODO-019: 구현 완료. summary 요청에 period/startDate/endDate를 누락 없이 전달하고 ApiResponse data만 사용한다.` |
| 020 | ✅ 코드 구현 | `salesApi.js` | monthly query/empty 확인 | `TODO-020: 구현 완료. year가 없는 요청과 빈 월 목록의 화면 처리 기준을 확인한다.` |
| 021 | ✅ 코드 구현 | `salesApi.js` | daily와 time-slots 책임 구분 확인 | `TODO-021: 구현 완료. daily(from/to)와 time-slots(date/intervalMinutes)를 별도 메서드로 유지하고 응답 배열을 혼용하지 않는다.` |
| 022 | ✅ 코드 구현 | `useSalesQuery.js` | 요청 경합·loading/error QA | `TODO-022: 구현 완료. 기간을 빠르게 바꿀 때 이전 응답을 무시하고 loading/error/empty가 화면별로 분리되는지 확인한다.` |

### P4C · 관리자 대시보드 (TODO-023~025, SCR-022)

| TODO | 현재 상태 | 실제 위치 | 남은 구현/검증 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 023 | ✅ 코드 구현 | `AdminSalesController#getDashboard`, Service/Mapper | 각 위젯의 실제 DB 값 대조 | `TODO-023: 구현 완료. dashboard DTO의 매출·주문·품절 요약 필드와 각 원본 조회의 합계를 실DB로 대조한다.` |
| 024 | ✅ 코드 구현 | `adminApi.js` | endpoint/ApiResponse 오류 확인 | `TODO-024: 구현 완료. getDashboard는 dashboard endpoint 하나만 호출하고 오류를 hook으로 그대로 전달한다.` |
| 025 | ✅ 코드 구현 | `useDashboard.js` | loading/refresh/error/partial error UI QA | `TODO-025: 구현 완료. 재조회 중 기존 데이터 유지, 전체 실패와 위젯별 partial error 표시 여부를 화면 기준으로 확정한다.` |

### P5 · Live UX, 인증, 보안 (TODO-026~037)

| TODO | 현재 상태 | 실제 위치 | 다음 구현 1단위 | 권장 인라인 TODO |
| --- | --- | --- | --- | --- |
| 026 | ⬜ 보류 | `LiveOrderBoard.jsx` | 가로 스크롤 UX 결정 | `TODO-026: 카드 보드를 useRef + scrollBy로 전환하기 전 키보드·터치·상태 변경 시 포커스 보존 기준을 정한다.` |
| 027 | ⬜ | `AdminAuthController` | POST login 요청/응답 계약 | `TODO-027: 관리자 식별자/비밀번호 검증과 실패 ErrorCode를 정하고 password·원문 예외는 응답에 노출하지 않는다.` |
| 028 | ⬜ | `JwtTokenProvider.java` | token 생성/검증/claims | `TODO-028: access token의 issuer/subject/role/expiry와 서명 키 관리 방식을 정해 create/validate/getClaims를 구현한다.` |
| 029 | ⬜ | `JwtAuthenticationFilter.java` | Bearer 필터 | `TODO-029: Bearer 누락·만료·위조를 500이 아닌 인증 실패로 처리하고 kiosk 경로에는 적용하지 않는다.` |
| 030 | ⬜ | `SecurityConfig.java` | 보호 경로 정책 | `TODO-030: login만 permitAll로 두고 /api/admin/** 권한 정책과 CORS/CSRF 기준을 명시한다.` |
| 031 | ⬜ | `adminApi.js` | login 호출 | `TODO-031: 로그인 응답 token/expiresAt 필드를 고정한 뒤 adminSession 저장으로 연결한다.` |
| 032 | ⬜ | `adminSession.js`, store | 세션 저장/만료 | `TODO-032: remember 옵션별 저장소와 만료·파싱 실패 시 세션 제거 규칙을 단일 함수로 정리한다.` |
| 033 | ⬜ | `apiClient.js` | Bearer/401 공통 처리 | `TODO-033: 요청마다 최신 token을 주입하고 401에서 한 번만 세션을 지운 뒤 로그인으로 이동한다.` |
| 034 | ⬜ | `LoginPage.jsx` | 실제 로그인 UI | `TODO-034: submitting/invalid credentials/network error 상태를 분리하고 token을 화면 state에 남기지 않는다.` |
| 035 | ⬜ | `useAdminAuth.js` | 보호 라우트 가드 | `TODO-035: 세션 검증 전 loading, 만료 시 redirect, 권한 없음 403 안내 흐름을 구현한다.` |
| 036 | ⬜ | `AdminApp.jsx` | canonical URL 정리 | `TODO-036: 실행 kebab-case 경로와 Bible camelCase 표기 중 하나를 정하고 alias/redirect 정책을 문서와 코드에 같이 반영한다.` |
| 037 | ⬜ | `apiClient.js` | 403/409/검증 오류 매핑 | `TODO-037: ApiResponse code/message를 보존해 403·409·field validation을 화면별 메시지로 매핑한다.` |

## 4. 다음 구현 순서

1. **품절 런타임 QA**: 실제 DB에서 메뉴 1건과 재료 1건을 품절/복구하고, 복수 변경 중 실패 1건의 전체 롤백을 확인한다. 옵션 탭은 숨김을 유지한다.
2. **매출 DB 계약 QA**: 집계 View 배포 여부를 확인하고 Bruno에서 summary/monthly/daily/time-slots/dashboard 응답과 화면 합계를 대조한다.
3. **결제수단 계약 결정 후 011→014 순서 구현**: 경로와 `active` DTO를 먼저 고정한 뒤 Controller → Service/Mapper → API → draft 순서를 지킨다.
4. **환불 정책 결정 후 001→038→039→040→042 순서 구현**: 승인 결제 환불을 주문 취소와 섞지 않는다.
5. **인증은 027→037 순서**: login/JWT/filter/security를 먼저 끝낸 뒤 프런트 세션과 보호 라우트를 연결한다.

## 5. 문서와 코드의 불일치/결정 필요

| 항목 | 현재 코드 | 기존 문서/Figma | 필요한 결정 |
| --- | --- | --- | --- |
| 품절 옵션 탭 | API에 `OPTION_ITEM` 포함, UI 탭 숨김 | Product Bible은 옵션 품절을 범위에 포함 | 옵션은 관리 API만 유지할지, 별도 화면/탭을 만들지 결정 |
| 품절 파생 상태 | 직접 `sold_out` 토글만 구현 | Bible은 ingredient/option 영향 메뉴와 effectiveSoldOut 권장 | MVP에서 파생 품절을 구현할지, 현재 직접 토글만 명시할지 결정 |
| 결제수단 URL | 코드 camelCase 표기 존재 | 실행 URL/Bible 표기가 서로 다름 | kebab-case 정본 및 alias 여부 결정 |
| Screen URL | 실행은 `/sold-out`, `/payment-methods` | 일부 Bible은 camelCase | 기존 링크 호환을 포함한 URL 정규화 결정 |
| 매출 DB 검증 | 코드와 빌드 근거 있음 | 실제 View/Bruno/브라우저 증거 없음 | 배포 DB에서 검증한 뒤 구현 완료 기준을 확정 |

---

## 이력

### 번호 재매핑 (2026-08-06 → 2026-08-19)

8/6에 TODO 번호를 재배치(032~048 → 015~031 등)한 뒤, 8/19에 인라인 주석을 구현 순서대로 001~043으로 재정리했다. 구 번호와 신 번호의 대응은 소스 커밋 `6f4201f`(ASAK-back)·`c08190f`(ASAK-Admin) 참조.

### 진행 로그

| 날짜 | 내용 |
| --- | --- |
| 2026-08-06 | 메뉴 조회와 주문 목록의 Empty/Error 처리 정리. |
| 2026-08-11 | 관리자 메뉴 상세·영양·재료·soft delete API와 Admin 연결. |
| 2026-08-18 | 결제수단 `active` 필드 정합화 방향 합의. 실제 API 구현은 미완료. |
| 2026-08-19~20 | 매출·대시보드 API/프런트 연결과 시간대 30분 조회 구현·빌드 확인. |
| 2026-08-21 | 메뉴·재료·옵션 항목을 포함하는 품절 DB GET/PATCH 및 Admin draft 연결·빌드 확인. 옵션 탭은 숨김 유지. 이 문서를 실제 구현 상태 기준으로 전면 갱신. |

## 사용법

1. IDE TODO 패널에서는 번호순으로 구현한다. 완료된 과거 TODO를 다음 기능으로 재사용하지 않는다.
2. 기능은 **화면 상태 → API 계약 → DB 저장/집계 → 실패 처리 → 브라우저/Bruno 검증** 순서로 닫는다.
3. 코드 구현 사실, mock, DB 반영, 런타임 검증을 같은 완료 표시로 섞지 않는다.
4. 이 문서와 소스 인라인 주석이 어긋나면 실제 코드부터 다시 확인하고, 주석 수정은 별도 코드 수정 승인으로 진행한다.
