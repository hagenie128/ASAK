# 종강 전 문서 동기화 — Admin 검증·대본·TC 실행표 (2026-09-02)

## 작성·갱신 문서

| 문서 | 작업 |
| --- | --- |
| `wiki/admin-doc-code-verification-2026-09-02.md` | **신규** — 4개 wiki + 로컬 코드 대조 전문 |
| `wiki/demo-tc-execution-sheet-2026-09-02.md` | **신규** — 시연 당일 TC 체크표 |
| `wiki/graduation-presentation-script-2026-09-02.md` | **갱신** — 상세 멘트·타임라인·클릭 체크리스트·WBS-081/085 연계 |
| `wiki/graduation-demo-mvp-2026-09-02.md` | 링크·매출 UI·검증 상태 갱신 |
| `wiki/wbs.md` | 2026-09-02 블록, WBS-041/045/047~049 정정 |
| `wiki/qa-test-cases.md` | TC-009·013 종강 메모, 실행표 링크 |
| `wiki/project-completion-checklist-2026-09-01.md` | 종강 링크·완료 판정 표 사전 기록 |
| `wiki/user-scenarios.md` | HISTORY + 검증 문서 §3 링크 |
| `wiki/index.md` | 종강 시연 섹션 추가 |

| `wiki/qa-execution-report-2026-09-02.md` | Admin API QA |
| `wiki/qa-kiosk-execution-report-2026-09-02.md` | Kiosk API E2E QA |
| `scripts/qa-admin-api-2026-09-02.ps1` | Admin QA 재실행 스크립트 |
| `scripts/qa-kiosk-api-2026-09-02.ps1` | Kiosk QA 재실행 스크립트 |

## 핵심 결론 (QA 후)

- Admin·Kiosk **API E2E 대부분 PASS** — TC-001~003, 009, 012(Admin), 013, 014 등.
- **FAIL:** Admin 결제수단→Kiosk 미반영, INGREDIENT ing125 Kiosk 미반영. READY 취소 500 → **409 불가** (Admin 코드 수정).
- UI 브라우저 클릭·리허설은 시연 당일.

---

## 2026-09-02 추가 동기화 (REST API·계약)

### 갱신 문서

| 문서 | 작업 |
| --- | --- |
| `wiki/rest-api-spec.md` | **갱신** — 커밋·QA 상태·품절/로그인 구현·영수증 path·`waitingOrderNo` 계약 불일치 |
| `wiki/current-status-baseline.md` | **갱신** — 2026-09-02 overlay |
| `governance/contract-decisions-2026-07-16.md` | **갱신** — `waitingOrderNo` vs `waitingOrderCount` 결정 필요 |
| `wiki/qa-execution-report-2026-09-02.md` | **갱신** — TC-013-daily 스크립트 필드명 불일치 |
| `wiki/wbs.md` | **갱신** — QA 요약·rest-api 링크 |

### 기준 커밋

| 저장소 | 커밋 |
| --- | --- |
| ASAK (docs) | `2fd0c0a` |
| ASAK-back | `b0718b3` |
| ASAK-Admin | `6071c68` |
| ASAK-Kiosk | `e1994e4` |

### 확인한 근거

- Controller: `AdminSoldOutController`, `AdminAuthController`, `UserReceiptController`, `AdminDeviceEventController`
- DTO: `ApprovePaymentResponse.waitingOrderNo`, `DailySalesResponse.rows`
- QA JSON: `qa-admin-api-results-2026-09-02.json`, `qa-kiosk-api-results-2026-09-02.json`
- DevCopilot workspace 2 (비교용, 원격 수정 없음)

### 남은 결정 필요

| 상태 | 항목 |
| --- | --- |
| `계약 불일치` | API-006 `waitingOrderNo` vs 정본 `waitingOrderCount` |
| `구현 불일치` | Admin 결제수단 methodId ↔ Kiosk `pay_method_cfg` 동기화 |
| `구현 불일치` | INGREDIENT 품절 → Kiosk (`affectedMenuCount=0`) |
| `구현 불일치` | READY 주문 취소 500 | **해소(코드)** → 409 `ORDER_CANCEL_NOT_ALLOWED`. HTTP 재검증 미실행 |
| `미검증` | UI 브라우저 E2E · RTOS 실기기 |

---

## 2026-09-02 오후 — Hub·Notion·READY 취소 정책

### 기준

| 저장소 | 커밋/상태 |
| --- | --- |
| ASAK (docs) | `2fd0c0a` + 로컬 수정 |
| ASAK-back | `b0718b3` + **미커밋** Admin READY 취소 409 (`AdminOrderController`·`AdminOrderService`) |

### 갱신한 로컬 문서

`rest-api-spec.md`, `qa-execution-report`, `qa-test-cases.md`, `wbs.md`, `current-status-baseline.md`, `admin-doc-code-verification`, `project-completion-checklist`, `graduation-demo-mvp`

### DevCopilot Hub (workspace 2)

| id | 결과 |
| --- | --- |
| **291** API-024 cancel | **갱신** — READY → 409 `ORDER_CANCEL_NOT_ALLOWED`, NPE 500 수정 메모 |
| API-006 (id 확인됨) | 변경 없음 — 이미 `waitingOrderNo` |

재조회: id 291 description·response_error 반영 확인.

### Notion

| 페이지 | 결과 |
| --- | --- |
| [06. API 명세](https://app.notion.com/p/34651ef04f0b838ca3a481e55eebfb2b) | `## 2026-09-02` 섹션 **prepend** |
| [07. WBS](https://app.notion.com/p/1ab51ef04f0b8330afca012a4e8d14fa) | `## 2026-09-02` 섹션 **prepend** |

### Hub Wiki REST

`GET /api/workspaces/2/wikis` — 빈 응답 또는 wiki id 12 미조회. **wiki/12 본문 push 미실행** (MCP API 카드만 갱신).

### 수정하지 않은 범위

- 소스코드 커밋/push (Admin 수정은 로컬 미커밋)
- Kiosk·User 코드
- QA 스크립트 재실행

---

## 2026-09-02 저녁 — DevCopilot Hub 전수 점검

### 조회 범위

| 범위 | 개수 | pagination | 판정 |
| --- | --- | --- | --- |
| Wiki | — | MCP 미지원 | **MCP 미지원** (REST wiki 목록 빈 응답) |
| 요구사항 | 45 | 단일 페이지 전체 | 변경 없음 40 · 사람 결정 5 |
| WBS | 85 | 단일 페이지 전체 | 변경 없음 85 |
| API 명세 | 30 | 단일 페이지 전체 | **갱신 4** · 변경 없음 24 · 사람 결정 2 |
| 시나리오 | 25 | 단일 페이지 전체 | 변경 없음 25 |
| QA TC | 17 | 단일 페이지 전체 | **갱신 2** · 변경 없음 15 |
| 화면 | 24 | 단일 페이지 전체 | **갱신 3** · 변경 없음 21 |
| DB 테이블/뷰 | 49 | 단일 페이지 전체 | **갱신 3** · 변경 없음 46 |
| 버그 | 0 | — | 해당 없음 |

### HTTP 재검증 (READY 취소)

- `PATCH /api/admin/orders/51984/cancel` → **409** `ORDER_CANCEL_NOT_ALLOWED` (실DB, 2026-09-02)

### Hub 갱신 (재조회 확인)

| 원격 ID | 범위 | 변경 전 → 후 |
| --- | --- | --- |
| **291** | API-024 | HTTP 재검증 pending → **verified 409** (orderId=51984) |
| **212** | API-009 | "스텁·메서드 없음" → **구현·TC-006 PASS** |
| **80** | API-014 | "active만 UI" → **구현 불일치** (Admin OFF→Kiosk CARD 노출) |
| **82** | API-017 | 미검증 → **data.rows[]** (QA 스크립트 `dailySales` 불일치) |
| **TC-014** | QA | READY 취소 409 기대결과 추가 |
| **TC-012** | QA | Kiosk 연동 구현 불일치 주석 |
| **SCR-007/008/022** | 화면 | `waitingOrderCount` → **`waitingOrderNo`** |
| **1223/1224** | DB orders | `waiting_date`, `waiting_order_no` 컬럼 **신규** |
| **1058** | DB vw_payment_result | `waiting_order_count` → 레거시 뷰 컬럼 명시 |

### 사람 결정 필요 (미갱신)

| 상태 | 항목 |
| --- | --- |
| `구현 불일치` | Admin 결제수단 OFF → Kiosk CARD 노출 (키오스크 코드 수정 범위 외) |
| `구현 불일치` | INGREDIENT ing125 품절 → Kiosk 미반영 |
| `MCP 미지원` | Hub Wiki 본문 (id 12) push |
| `보류` | 요구사항 상태 일괄 갱신 (FWD-MENU-001 등 DESIGNED vs 구현 DONE) |
| `보류` | API 30건 description "HTTP E2E 미검증" → QA PASS 일괄 반영 (범위 큼, 개별 근거 필요) |
| `보류` | Admin login API Hub 미등록 (`POST /api/admin/login`) |
| `보류` | `daily_waiting_sequence` 테이블 Hub DB 미등록 |
| `보류` | WBS Evidence 필드 (MCP 미지원) |

### 로컬 문서 동기화

- `wiki/rest-api-spec.md` — API-024 HTTP PASS
- `wiki/qa-execution-report-2026-09-02.md` — READY 취소 HTTP 검증
- `wiki/current-status-baseline.md` — overlay 갱신

### Git

자동 branch/commit/push **수행하지 않음**.
