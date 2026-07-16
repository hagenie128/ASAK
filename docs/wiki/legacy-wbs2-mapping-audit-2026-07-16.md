# Legacy WBS to WBS2 Mapping Audit

> Audit date: 2026-07-16. Scope: the 37 non-EXCLUDED Legacy WBS records in DevCopilot, compared with the 64 active `WBS2-*` records. Internal ID means DevCopilot's immutable numeric record ID; it is not the Task ID.

## Method and limitation

- The audit compared requirement tags, title scope, repository target, deliverable, and concrete local evidence. A similar word alone was not treated as duplication.
- `SUPERSEDED` records are preserved in DevCopilot with the `[SUPERSEDED]` title prefix and `EXCLUDED` status. Their replacement mapping is authoritative in this table.
- The DevCopilot WBS MCP schema has no Description field and `update_wbs_task` cannot write one. Therefore the requested `Replaced by WBS2-XXX` text is retained here, rather than falsely claiming it was written to DevCopilot.
- A `DONE` result is accepted only for a completed document/data artifact. It never asserts React implementation, executed QA, or a working backend API.

| Legacy Internal ID | Legacy Task ID | Legacy Title | Related WBS2 | Relationship | Recommended Status | Evidence |
|---:|---|---|---|---|---|---|
| 10 | WBS-001 | 메뉴 구조 · 옵션 트리 설계 | — | COMPLETED_WITH_EVIDENCE | DONE 유지 | Product Bible/Notion menu-option definition is present; design/data structure only. |
| 11 | WBS-010 | 프론트: 결제 화면 구현 | WBS2-026, WBS2-027 | SUPERSEDED | EXCLUDED | Payment route and failure work are separately scoped in WBS2; no implementation completion claim. |
| 12 | WBS-021 | 프론트: 타임아웃 정책/카운트다운 기준 확정 | WBS2-029, WBS2-030 | SUPERSEDED | EXCLUDED | WBS2 separates warning/countdown and payment-processing disable rules. |
| 14 | WBS-002 | 화면 흐름도 · 기능 정의서 | WBS2-005, WBS2-064 | SUPERSEDED | EXCLUDED | WBS2 owns current requirement/scenario/screen audit and handoff traceability. |
| 15 | WBS-003 | 기술스택 확정 · 역할분담 | WBS2-002 | COMPLETED_WITH_EVIDENCE | DONE 유지 | Repository baseline and role/stack records exist; this is documentation, not code delivery. |
| 16 | WBS-004 | ERD · API 명세서 작성 | WBS2-007, WBS2-008, WBS2-056 | COMPLETED_WITH_EVIDENCE | DONE 유지 | Legacy API/DB artifacts exist; WBS2 audits unresolved target-contract and migration gaps. |
| 17 | WBS-005 | 와이어프레임 · 컴포넌트 구조 | WBS2-009 to WBS2-016 | SUPERSEDED | EXCLUDED | WBS2 separates design evidence, mappings, accessibility, prototype, and conflict boundary. |
| 18 | WBS-008 | 프론트: 옵션선택 화면 구현 | WBS2-019, WBS2-020, WBS2-021 | SUPERSEDED | EXCLUDED | Detail, validation, and allergy disclosure are independent WBS2 work packages. |
| 19 | WBS-011 | 백엔드: 메뉴/옵션 API | WBS2-048, WBS2-049 | SUPERSEDED | EXCLUDED | WBS2 names the two backend vertical slices; backend API evidence is absent. |
| 20 | WBS-012 | 백엔드: 주문 생성 API | WBS2-050 | SUPERSEDED | EXCLUDED | WBS2 owns order validation/transaction/API-test evidence. |
| 21 | WBS-013 | 백엔드: 판매 항목 품절 상태 변경 API | WBS2-052 | SUPERSEDED | EXCLUDED | WBS2 owns the sold-out backend slice and API evidence. |
| 22 | WBS-015 | 프론트-백엔드 연동 테스트 | WBS2-057 to WBS2-060 | SUPERSEDED | EXCLUDED | Contract mapping and Kiosk/Admin/Sales integration are split in WBS2. |
| 23 | WBS-016 | 키오스크 예외처리(결제/터치/타임아웃) | WBS2-027, WBS2-029 to WBS2-032 | SUPERSEDED | EXCLUDED | Failure, timeout, states, and touch QA are separately testable WBS2 work. |
| 24 | WBS-019 | 배포 · 발표자료 · 시연 시나리오 | WBS2-064 | NEEDS_CONFIRMATION | BLOCKED | WBS2-064 covers documentation/demo handoff, but deployment ownership/scope is not evidenced. |
| 25 | WBS-022 | 프론트: 접근성 UI 적용 | WBS2-015, WBS2-032, WBS2-044, WBS2-062 | SUPERSEDED | EXCLUDED | Checklist, Kiosk/Admin states, and execution QA are distinct in WBS2. |
| 27 | WBS-024 | DB: ASAK 샘플 메뉴/재료/옵션 데이터 구성 | WBS2-047 | COMPLETED_WITH_EVIDENCE | DONE 유지 | `asak-data/seed/asak_seed_bundle.json` contains menu/ingredient/option data; application migration remains separate. |
| 28 | WBS-025 | 백엔드: 장바구니 검증 API | WBS2-050 | SUPERSEDED | EXCLUDED | Cart/order validation is part of the WBS2 transaction slice; no backend implementation proof. |
| 29 | WBS-026 | 백엔드: 추천 드레싱 menu_option 반영 | WBS2-049 | SUPERSEDED | EXCLUDED | Legacy source says planned and no backend slice exists; WBS2-049 owns target detail API. |
| 30 | WBS-027 | 프론트: 결제 실패/재시도 화면 구현 | WBS2-027 | SUPERSEDED | EXCLUDED | Exact payment failure/cart-retention scope is WBS2-027. |
| 31 | WBS-028 | 프론트: 타임아웃 안내/자동 초기화 구현 | WBS2-029, WBS2-030 | SUPERSEDED | EXCLUDED | WBS2 separates countdown and PROCESSING-state behavior. |
| 32 | WBS-029 | 관리자: 메뉴 관리 화면/API 설계 | WBS2-039, WBS2-052 | SUPERSEDED | EXCLUDED | Admin UI and backend sold-out/menu work are separately owned in WBS2. |
| 33 | WBS-030 | 관리자: 결제수단 설정 화면/API 설계 | WBS2-040 | SUPERSEDED | EXCLUDED | Current active scope is the Admin payment-method screen; backend contract is not claimed done. |
| 34 | WBS-031 | 테스트: 요구사항-시나리오-화면-API 추적성 점검 | WBS2-005, WBS2-061, WBS2-064 | SUPERSEDED | EXCLUDED | Traceability audit, actual QA execution, and handoff are separated in WBS2. |
| 35 | WBS-032 | 프론트: 접근성 설정 화면 초안 | WBS2-015, WBS2-044, WBS2-062 | SUPERSEDED | EXCLUDED | Design checklist, Admin states, and executed accessibility QA are WBS2 scope. |
| 36 | WBS-034 | 장치: 영수증 출력 모의 구현 | — | UNIQUE_LEGACY | EXCLUDED | Receipt/device work is explicit Future Scope; no active WBS2 implementation maps to it. |
| 37 | WBS-035 | 백엔드: 관리자 주문 목록/상태변경 API | WBS2-053 | SUPERSEDED | EXCLUDED | WBS2-053 owns admin order/status slice and API evidence. |
| 38 | WBS-036 | 프론트: 관리자 주문 관리/상세 화면 구현 | WBS2-035, WBS2-036, WBS2-037 | SUPERSEDED | EXCLUDED | Live order, list, and status/TTS policy are separately scoped in WBS2. |
| 39 | WBS-EXT-001 | [삭제요망] 장바구니 서버 검증 | WBS2-050 | SUPERSEDED | EXCLUDED | Legacy replacement/deletion marker is superseded by WBS2 transaction validation. |
| 40 | WBS-EXT-002 | [삭제요망] 관리자 결제수단 설정 | WBS2-040 | SUPERSEDED | EXCLUDED | Legacy replacement/deletion marker is superseded by WBS2 Admin payment work. |
| 41 | WBS-006 | Git 전략 · 백로그 티켓화 | WBS2-002, WBS2-064 | SUPERSEDED | EXCLUDED | Current repository baseline and documentation handoff replace the generic legacy task. |
| 42 | WBS-007 | 프론트: 메뉴선택 화면 구현 | WBS2-017, WBS2-018 | SUPERSEDED | EXCLUDED | Route assessment and menu-list contract are independently tracked. |
| 43 | WBS-009 | 프론트: 장바구니 화면 구현 | WBS2-022 to WBS2-025 | SUPERSEDED | EXCLUDED | Quantity limits, toast, and cart edit/delete are separately scoped. |
| 44 | WBS-014 | 주간 데모 & 회고 | — | UNIQUE_LEGACY | TODO 유지 | Ongoing team coordination has no duplicate WBS2 implementation scope. |
| 45 | WBS-017 | 시나리오 기반 QA | WBS2-061 to WBS2-063 | SUPERSEDED | EXCLUDED | Requirement, accessibility, and regression execution are distinct WBS2 QA records. |
| 46 | WBS-018 | 성능 · UX 개선 | WBS2-032, WBS2-045 | SUPERSEDED | EXCLUDED | Kiosk touch/responsive and Admin date/totals QA are current bounded scope. |
| 47 | WBS-020 | 최종 리허설 | WBS2-061 to WBS2-064 | SUPERSEDED | EXCLUDED | Final integration QA and documentation/demo handoff are represented by WBS2. |

## Resulting operational counts

| Metric | Count | Calculation |
|---|---:|---|
| Legacy active | 7 | 5 `COMPLETED_WITH_EVIDENCE` + 1 `UNIQUE_LEGACY` + 1 `NEEDS_CONFIRMATION` |
| Active WBS2 | 64 | No WBS2 scope/status change in this audit |
| Active total | 71 | `7 + 64` |
| Newly superseded Legacy | 30 | 29 `SUPERSEDED` + 1 Future Scope `UNIQUE_LEGACY` |
| Legacy `UNIQUE_LEGACY` retained | 1 | Internal ID 44 |
| `NEEDS_CONFIRMATION` | 1 | Internal ID 24, moved to `BLOCKED` |
| DONE | 8 | 5 evidence-backed Legacy + 3 evidence-backed WBS2 |
| EXCLUDED | 97 | Previous 67 duplicate records + 30 Legacy records excluded here |
| Total WBS | 168 | No deletion or creation |

The remaining human decision is Internal ID 24 (deployment/presentation ownership). It remains `BLOCKED`, not falsely complete and not silently excluded.
