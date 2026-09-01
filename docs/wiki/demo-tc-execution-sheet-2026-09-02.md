# 종강 시연 TC 실행표 (2026-09-02)

> Status: **CURRENT** — **2026-09-02 Agent API QA** (Admin+Kiosk) · UI 클릭은 시연 당일  
> 실행 보고: [Admin](qa-execution-report-2026-09-02.md) · [Kiosk](qa-kiosk-execution-report-2026-09-02.md)  
> 정본: [qa-test-cases.md](qa-test-cases.md) · [종강 MVP](graduation-demo-mvp-2026-09-02.md)  
> 사전 판정: [admin-doc-code-verification](admin-doc-code-verification-2026-09-02.md)

**원칙:** 코드만으로 PASS 금지. 실패 시 `FAIL` + Plan B 열에 기록.

## 시연 전 (3분)

- [x] Backend `8080` · Admin/Kiosk dev 동일 API — **2026-09-02 확인**
- [x] 고정 데이터: 로그인 `0001` · 품절 `ing_id=125` · CARD — **API 확인** (ing125 영향메뉴 0)
- [x] 품절·결제수단 **시연 후 원복** — **스크립트 자동 원복**
- [ ] 백업: Kiosk 녹화 · 9/1 환불·매출 캡처

---

## P0 — 반드시 실행

| ☑ | TC | 시나리오 | 실행 요약 | 기대 결과 | 결과 | Plan B / 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| ☑ | **TC-009** | SC-008 | `0001` / 빈값 / `9999` | 성공·400 | **PASS** | API 2026-09-02 |
| ☑ | **TC-014** | SC-008 | Live + RECEIVED→PREPARING→COMPLETED | 200 | **PASS** | TTS는 UI 미검증 |
| ☑ | **TC-006** | SC-007 | ing125 ON/OFF PATCH | 저장·원복 | **PASS** △ | affected=0, Kiosk 변화 없음 |
| ☑ | **TC-012** | SC-017 | CARD OFF→ON Admin | PATCH 200 | **PASS** Admin / **FAIL** Kiosk | Kiosk에 CARD 계속 노출 |
| ☑ | **TC-013** | SC-018 | summary today/week/month, 8/28 | KPI·890300 | **PASS** | UI 클릭 미검증 |
| ☑ | TC-001 | SC-014 | Kiosk EAT_IN/TAKE_OUT 주문 | orderType DB 일치 | **PASS** | API 2026-09-02 |
| ☑ | TC-002 | SC-002 | orders→payments CARD | APPROVED·orderNo | **PASS** | UI 클릭 미검증 |
| ☑ | **TC-003** | SC-003 | MENU·OPTION 품절 Kiosk | soldOut·cart 차단 | **PASS** | INGREDIENT ing125 FAIL |

---

## P1 — 시간 있을 때

| ☑ | TC | 실행 요약 | 기대 결과 | 결과 | 비고 |
| --- | --- | --- | --- | --- | --- |
| ☑ | **TC-010** | 메뉴 목록 | content≥1 | **PASS** | |
| ☑ | **TC-011** | 메뉴 상세 | name 필드 | **PASS** | 이미지=미리보기만 |
| ☐ | **TC-017** | CARD 환불 | CANCELED | **BLOCKED** | 실주문 스킵 |
| ☑ | SC-022 | 주문 상세 items | items[] | **PASS** | |
| ☑ | WBS-040 | 대시보드 KPI·delta | 200 | **PASS** | |
| ☑ | TC-015 | — | BLOCKED | **BLOCKED** | RTOS Q&A만 |

---

## 시연 순서 (체크용)

| 순서 | 화면 | TC/SC |
| --- | --- | --- |
| 1 | 로그인 SCR-015 | TC-009 |
| 2 | 주문 현황 SCR-009 | TC-014 |
| 3 | 품절 SCR-011 | TC-006 |
| 4 | 결제수단 SCR-018 | TC-012 |
| 5 | 매출 요약·일별 SCR-019/021 | TC-013 |
| 6 | 메뉴 SCR-016 | TC-010~011 |
| 7 | 주문 상세 SCR-010 | SC-022 |

---

## 시연 결과 요약 (2026-09-02 API QA)

| 항목 | PASS / FAIL / BLOCKED | 담당 | 캡처·로그 |
| --- | --- | --- | --- |
| Admin 로그인 | **PASS** | Agent | [report](qa-execution-report-2026-09-02.md) |
| 주문 상태 변경 | **PASS** | Agent | TC-014b/c |
| 품절 (Admin) | **PASS** △ | Agent | affectedMenuCount=0 |
| 품절 (Kiosk) | **PASS** △ | Agent | MENU/OPTION OK · INGREDIENT FAIL |
| 결제수단 (Admin) | **PASS** | Agent | |
| 결제수단 (Kiosk) | **FAIL** | Agent | Admin OFF 무시 |
| 매출 화면 | **PASS** API | Agent | 8/28=890300 |
| 메뉴 편집 | **PASS** 조회 | Agent | 저장 UI 미클릭 |
| 환불 | **BLOCKED** | — | |
| Kiosk 주문·결제 | **PASS** | Agent | [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md) |
