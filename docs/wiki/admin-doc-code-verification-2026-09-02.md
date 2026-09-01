# 관리자 문서·코드 대조 검증 (2026-09-02)

> Status: **CURRENT** (종강 시연 전 검증)  
> 대상: 로컬 `ASAK-Admin` + `ASAK-backend` + `ASAK-Kiosk` (API QA)  
> 정본 링크: [WBS](wbs.md) · [QA TC](qa-test-cases.md) · [완료 체크리스트](project-completion-checklist-2026-09-01.md) · [종강 MVP](graduation-demo-mvp-2026-09-02.md)  
> QA 실행: [Admin](qa-execution-report-2026-09-02.md) · [Kiosk](qa-kiosk-execution-report-2026-09-02.md) · [TC 실행표](demo-tc-execution-sheet-2026-09-02.md)

## 결론

**종강 시연은 가능**하지만 **완료 선언·UI E2E PASS·체크리스트 전항목 완료**까지는 아직 아니다.  
WBS·QA 원칙: **「코드 연결 ≠ DONE」** · 로컬 `c:\ASAK-workspace` 정본(클라우드 Agent 머지 금지).

| 구분 | 판정 |
| --- | --- |
| Admin API QA | ✅ 22/24 PASS — [보고](qa-execution-report-2026-09-02.md) |
| Kiosk API QA | ✅ 17/18 PASS — [보고](qa-kiosk-execution-report-2026-09-02.md) |
| Admin·Kiosk build | ✅ |
| UI 브라우저 클릭 | △ 미실행 |
| 프로젝트 완료 선언 | ❌ §0 공통 조건 미충족 |

**알려진 FAIL:** Admin CARD OFF→Kiosk 미반영 · INGREDIENT ing125 품절 Kiosk 미반영 · READY 취소 500

---

## 1. `project-completion-checklist-2026-09-01.md` 검증

### §0 완료 선언 전 공통 조건 — **미충족**

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| WBS 전부 DONE/EXCLUDED | ❌ | IN_PROGRESS·IN_REVIEW 다수 |
| 빌드·테스트 재실행 | △ | Admin·Kiosk build ✅ · Admin API 22/24 · Kiosk API 17/18 · **UI 클릭 미완** |
| 팀 검토·실행 근거 | △ | [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) P0 기록 · 팀 승인 미완 |

### §4 관리자 기능 — **시연 가능 / 문서 완료는 아님**

| 체크리스트 | WBS | 코드 | 시연 | 비고 |
| --- | --- | --- | --- | --- |
| 사이드바·라우트 일치 | 039 | ✅ | △ | `AdminApp.jsx` ↔ `AdminSidebar` |
| 대시보드·최근주문·합계 | 040 | ✅ | △ | `useDashboard` + 전주 대비. **실DB 브라우저 QA 미기록** |
| 실시간 주문·5초 폴링 | 041 | ✅ | △ | `LiveOrderBoard` `setInterval(5000)` |
| 주문 상태·취소·환불 | 042~043 | △ | △ | RECEIVED→PREPARING→COMPLETED ✅. **CARD 환불만**. READY 취소·중복409 **미검증** |
| 품절 저장·영향 메뉴 | 044 | △ | △ | 재료·메뉴 탭 ✅, `affectedMenuCount` ✅. 옵션 탭 숨김. Kiosk E2E 없음 |
| 메뉴 등록·수정 | 045 | △ | △ | `menusApi.create/update` ✅. **이미지 미리보기만** |
| 결제수단 on/off·정렬 | 046 | △ | △ | PATCH·LEFT JOIN ✅. Kiosk 노출 E2E 없음. 정책 문구 **localStorage만** |
| 매출 기간·차트 | 047~049 | ✅ | △ | 오늘/이번주/이번달·달 전체 그래프·더미 채움. **화면 E2E 미기록** |
| Loading/Empty/Error | 050 | △ | △ | `AdminAsyncState` 주요 페이지. **전 화면 QA 기록 없음** |
| 날짜·합계 회귀 | 051 | ❌ | ❌ | 실행 기록 없음 |

### §6 연동 (관리자 시연 관련)

| 항목 | 상태 |
| --- | --- |
| WBS-070 Admin E2E | △ 코드 연결 완료, mock 잔존 거의 없음, E2E 기록 없음 |
| WBS-071 매출·환불 합계 | △ 8/28 실DB 대조 기록 있음. **새 매출 UI 재검증 필요** |
| RTOS 영수증 | ❌ 시연 제외 권장 |

### §3·§5·§7 (키오스크·기획·전체 QA)

이번 관리자 시연 범위 밖. `EXCLUDED`가 아니라 **「미검증·IN_REVIEW」**로 둔다.

---

## 2. `wbs.md` 검증 (관리자·백엔드)

[2026-09-01 Admin 실DB QA 정정](wbs.md#2026-09-01-admin-실db-qa-상태-정정) 블록과 로컬 코드는 **대체로 일치**한다.

| WBS | 문서 상태 | 코드 대조 | 보정 (2026-09-02) |
| --- | --- | --- | --- |
| 040 대시보드 | IN_REVIEW | `AdminSalesController` → adapter → `DashboardPanels` | 일치 |
| 041 실시간 주문 | IN_PROGRESS | 5초 폴링·TTS·취소 Confirm | **IN_REVIEW 권장** |
| 042~043 주문·환불 | IN_REVIEW | `OrderManagePage` + `PATCH .../refund` | E2E만 남음 |
| 044 품절 | IN_REVIEW | `PATCH soldOut`, `affectedMenuCount` | 일치 |
| 045 메뉴 | IN_PROGRESS | **실 API 저장** 연결 | 문서 「가짜 저장」은 **구식** |
| 046 결제수단 | IN_REVIEW | LEFT JOIN·빈목록 200 | 일치 |
| 047~049 매출 | IN_PROGRESS | `fillDailyRows`·기간 버튼 반영 | E2E 후 IN_REVIEW |
| 062 품절 API | DONE | Mapper·Controller | 일치 |
| 070 Admin 실연동 | IN_REVIEW | 대부분 실 API | 일치 |

**문서·코드 불일치 1건:** WBS-045 「가짜 저장」→ 현재 `createMenu`/`updateMenu` 실 호출. **이미지 파일 업로드 API는 미연결.**

---

## 3. `user-scenarios.md` 검증 (시연 SC)

문서 Status: **HISTORY**. Pack 02·07·Screen Bible 우선.

| SC | 시나리오 | 판정 | 코드·문서 갭 |
| --- | --- | --- | --- |
| **SC-007** | 관리자 품절 | PARTIAL | Admin 저장·영향 메뉴 ✅. 문서 「인증 없이」→ **SCR-015 로그인 필요** |
| **SC-008** | 주문 상태 관리 | PARTIAL | Live + 주문관리 ✅. E2E 기록 없음 |
| **SC-017** | 신규 메뉴 등록 | PARTIAL | API 저장·옵션그룹 ✅. 이미지·Kiosk 미검증 |
| **SC-018** | 일별 매출 조회 | PARTIAL | 3매출 화면 + API ✅. 더미·미래 비활성 시연 보강 |
| **SC-022** | 제외 재료 확인 | PASS(코드) | `OrderDetailPanel.excludedIngredients` ✅ |
| **SC-024** | 통합 리허설 | PARTIAL | 관리자 구간만. Kiosk 1~4 미검증 |
| SC-001~006, 009~016, 019~021, 023 | Kiosk·멤버십·RTOS | 미검증/EXCLUDED | SC-016·SC-015 MVP 제외 |

---

## 4. `qa-test-cases.md` 검증 (관리자 TC)

**실행 기록 없으면 PASS 금지.** 아래는 코드·WBS 기준 **사전 판정**.

| TC | 이름 | 사전 판정 | 시연 당일 확인 |
| --- | --- | --- | --- |
| **TC-009** | 관리자 로그인 | READY | `0001` 성공, 빈/오류 번호 토스트. **시연 필수**(문서 EXCLUDED 표기와 별개) |
| **TC-010** | 메뉴 목록·품절 | PARTIAL | 목록·품절 배지. Kiosk는 TC-006과 함께 |
| **TC-011** | 메뉴 등록/수정 | PARTIAL | 저장 API ✅. 이미지·Kiosk 미검증 |
| **TC-012** | 결제수단 | PARTIAL | Admin PATCH ✅(9/1). Kiosk 미검증 |
| **TC-013** | 매출 요약 | PARTIAL | API 합계 ✅. **오늘/주/월·달 전체 차트 새 QA** |
| **TC-014** | 주문·상태 | PARTIAL | API 전이 ✅. 화면 E2E 미기록 |
| **TC-017** | 환불·사유 | PARTIAL | CARD 1건 ✅. 409·OTHER·화면 E2E 미기록 |
| TC-001~008, 015~016 | Kiosk·장치 | 미실행 | Kiosk 시연 시 별도 |

**문서 오류 (시연 시 주의)**

- TC-015의 API-019 = 월별 매출 API이지 영수증 아님 → **시연 스킵**
- TC-009 `EXCLUDED` vs 실제 로그인 시연 필요 → **[TC 실행표](demo-tc-execution-sheet-2026-09-02.md)에 포함**

---

## 5. 시연 권장 순서 (SC-024 관리자 구간)

1. **TC-009** 로그인 `0001`
2. **SC-008 / TC-014** 주문 현황 → 상태 변경 (환불·영수증은 리허설에서만)
3. **SC-007 / TC-006** 품절(재료) → 영향 메뉴 N개 → 저장 → **원복**
4. **TC-012** 결제수단 토글·저장 → **원복**
5. **SC-018 / TC-013** 매출 요약(오늘/이번주/이번달) → 일별·월별
6. **SC-017 / TC-010~011** 메뉴 상세·수정 — **이미지는 미리보기만**이라고 말하기
7. **SC-022** 주문 상세 제외 재료 확인

**시연에서 빼기:** 영수증 재출력(RTS), KAKAO/NAVER 환불, 품절 옵션 탭, 결제 정책 문구(키오스크 미반영)

---

## 6. 시연 후 문서에 남길 것

[project-completion-checklist](project-completion-checklist-2026-09-01.md#완료-판정-기록) 하단 표 + [demo-tc-execution-sheet](demo-tc-execution-sheet-2026-09-02.md) 결과 열.

| 항목 | 시연 후 기록 예시 |
| --- | --- |
| Admin build | `npm run build` 성공 일시 |
| Admin E2E | TC-009, 010~014, 017 PASS/FAIL |
| Backend | `gradlew compileJava` + 환불/품절 수동 API |
| BLOCKED | 이미지 업로드, Kiosk↔품절 E2E, TC-015 RTOS |

---

## 7. 관련 문서

- [종강 MVP 실행본](graduation-demo-mvp-2026-09-02.md)
- [발표 대본 (정본)](graduation-presentation-script-2026-09-02.md)
- [TC 실행표 (1페이지)](demo-tc-execution-sheet-2026-09-02.md)
- [ai-reports 기록](../ai-reports/2026-09-02/asak-doc-sync-admin-verification-2026-09-02.md)

## 변경 이력

| 일자 | 내용 |
| --- | --- |
| 2026-09-02 | 최초 작성 — 4개 wiki + 로컬 코드 대조, 시연 전 사전 판정 |
