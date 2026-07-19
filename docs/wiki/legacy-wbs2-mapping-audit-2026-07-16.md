# Legacy WBS to WBS2 Mapping Audit

> 감사일: 2026-07-16. 범위: DevCopilot의 EXCLUDED가 아닌 Legacy WBS 37건, 초기에는 활성 `WBS2-*` 64건과 비교. 이후 Release/Presentation 분리로 WBS2-065·WBS2-066이 추가되어 활성 WBS2는 66건. Internal ID는 DevCopilot의 불변 숫자 record ID이며 Task ID가 아닙니다.

## 방법 및 한계

- 요구사항 태그, 제목 범위, 저장소 대상, deliverable, 구체적 로컬 evidence를 비교했습니다. 유사 단어만으로는 중복으로 보지 않았습니다.
- `SUPERSEDED` 레코드는 DevCopilot에 `[SUPERSEDED]` 제목 접두사와 `EXCLUDED` 상태로 보존됩니다. 대체 매핑은 이 표가 권위 있습니다.
- DevCopilot WBS MCP schema에는 Description 필드가 없고 `update_wbs_task`로 쓸 수 없습니다. 따라서 요청된 `Replaced by WBS2-XXX` 텍스트는 여기에 보관하며, DevCopilot에 기록했다고 허위 주장하지 않습니다.
- `DONE`은 완료된 문서/데이터 산출물에만 허용합니다. React 구현, 실행 QA, 동작하는 backend API를 주장하지 않습니다.

| Legacy Internal ID | Legacy Task ID | Legacy Title | Related WBS2 | Relationship | Recommended Status | Evidence |
|---:|---|---|---|---|---|---|
| 10 | WBS-001 | 메뉴 구조 · 옵션 트리 설계 | — | COMPLETED_WITH_EVIDENCE | DONE 유지 | Product Bible/Notion menu-option 정의 존재; design/data 구조만 해당. |
| 11 | WBS-010 | 프론트: 결제 화면 구현 | WBS2-026, WBS2-027 | SUPERSEDED | EXCLUDED | Payment route·실패 작업은 WBS2에서 별도 범위; 구현 완료 주장 없음. |
| 12 | WBS-021 | 프론트: 타임아웃 정책/카운트다운 기준 확정 | WBS2-029, WBS2-030 | SUPERSEDED | EXCLUDED | WBS2가 경고/카운트다운과 결제 PROCESSING 비활성 규칙을 분리. |
| 14 | WBS-002 | 화면 흐름도 · 기능 정의서 | WBS2-005, WBS2-064 | SUPERSEDED | EXCLUDED | WBS2가 현재 요구사항/시나리오/화면 감사·handoff traceability 담당. |
| 15 | WBS-003 | 기술스택 확정 · 역할분담 | WBS2-002 | COMPLETED_WITH_EVIDENCE | DONE 유지 | 저장소 baseline·역할/스택 기록 존재; 문서이며 코드 납품 아님. |
| 16 | WBS-004 | ERD · API 명세서 작성 | WBS2-007, WBS2-008, WBS2-056 | COMPLETED_WITH_EVIDENCE | DONE 유지 | Legacy API/DB 산출물 존재; WBS2가 미해결 target-contract·migration 갭 감사. |
| 17 | WBS-005 | 와이어프레임 · 컴포넌트 구조 | WBS2-009 to WBS2-016 | SUPERSEDED | EXCLUDED | WBS2가 design evidence, mapping, accessibility, prototype, 충돌 경계 분리. |
| 18 | WBS-008 | 프론트: 옵션선택 화면 구현 | WBS2-019, WBS2-020, WBS2-021 | SUPERSEDED | EXCLUDED | Detail, validation, allergy 고지는 WBS2 work package로 독립. |
| 19 | WBS-011 | 백엔드: 메뉴/옵션 API | WBS2-048, WBS2-049 | SUPERSEDED | EXCLUDED | WBS2가 두 backend vertical slice 명시; backend API evidence 없음. |
| 20 | WBS-012 | 백엔드: 주문 생성 API | WBS2-050 | SUPERSEDED | EXCLUDED | WBS2가 주문 검증/트랜잭션/API-test evidence 담당. |
| 21 | WBS-013 | 백엔드: 판매 항목 품절 상태 변경 API | WBS2-052 | SUPERSEDED | EXCLUDED | WBS2가 sold-out backend slice·API evidence 담당. |
| 22 | WBS-015 | 프론트-백엔드 연동 테스트 | WBS2-057 to WBS2-060 | SUPERSEDED | EXCLUDED | Contract mapping과 Kiosk/Admin/Sales 통합이 WBS2에서 분리. |
| 23 | WBS-016 | 키오스크 예외처리(결제/터치/타임아웃) | WBS2-027, WBS2-029 to WBS2-032 | SUPERSEDED | EXCLUDED | 실패, timeout, state, touch QA가 WBS2에서 각각 테스트 가능. |
| 24 | WBS-019 | 배포 · 발표자료 · 시연 시나리오 | WBS2-065, WBS2-066 | SUPERSEDED | EXCLUDED | Release readiness와 Presentation/Demo readiness로 분리. 원 회의 evidence상 발표는 공동 작업; 대표 owner·배포 환경 미확정. |
| 25 | WBS-022 | 프론트: 접근성 UI 적용 | WBS2-015, WBS2-032, WBS2-044, WBS2-062 | SUPERSEDED | EXCLUDED | Checklist, Kiosk/Admin state, 실행 QA가 WBS2에서 구분. |
| 27 | WBS-024 | DB: ASAK 샘플 메뉴/재료/옵션 데이터 구성 | WBS2-047 | COMPLETED_WITH_EVIDENCE | DONE 유지 | `asak-data/seed/asak_seed_bundle.json`에 menu/ingredient/option 데이터; 앱 migration은 별도. |
| 28 | WBS-025 | 백엔드: 장바구니 검증 API | WBS2-050 | SUPERSEDED | EXCLUDED | Cart/order validation은 WBS2 transaction slice 일부; backend 구현 증거 없음. |
| 29 | WBS-026 | 백엔드: 추천 드레싱 menu_option 반영 | WBS2-049 | SUPERSEDED | EXCLUDED | Legacy source는 planned이며 backend slice 없음; WBS2-049가 target detail API 담당. |
| 30 | WBS-027 | 프론트: 결제 실패/재시도 화면 구현 | WBS2-027 | SUPERSEDED | EXCLUDED | 결제 실패/장바구니 유지 범위는 WBS2-027과 일치. |
| 31 | WBS-028 | 프론트: 타임아웃 안내/자동 초기화 구현 | WBS2-029, WBS2-030 | SUPERSEDED | EXCLUDED | WBS2가 카운트다운과 PROCESSING-state 동작 분리. |
| 32 | WBS-029 | 관리자: 메뉴 관리 화면/API 설계 | WBS2-039, WBS2-052 | SUPERSEDED | EXCLUDED | Admin UI와 backend sold-out/menu 작업이 WBS2에서 분리 담당. |
| 33 | WBS-030 | 관리자: 결제수단 설정 화면/API 설계 | WBS2-040 | SUPERSEDED | EXCLUDED | 현재 활성 범위는 Admin payment-method 화면; backend contract 완료 주장 없음. |
| 34 | WBS-031 | 테스트: 요구사항-시나리오-화면-API 추적성 점검 | WBS2-005, WBS2-061, WBS2-064 | SUPERSEDED | EXCLUDED | Traceability 감사, 실제 QA 실행, handoff가 WBS2에서 분리. |
| 35 | WBS-032 | 프론트: 접근성 설정 화면 초안 | WBS2-015, WBS2-044, WBS2-062 | SUPERSEDED | EXCLUDED | Design checklist, Admin state, 실행 accessibility QA가 WBS2 범위. |
| 36 | WBS-034 | 장치: 영수증 출력 모의 구현 | — | UNIQUE_LEGACY | EXCLUDED | Receipt/device 작업은 명시적 Future Scope; 활성 WBS2 구현 매핑 없음. |
| 37 | WBS-035 | 백엔드: 관리자 주문 목록/상태변경 API | WBS2-053 | SUPERSEDED | EXCLUDED | WBS2-053이 admin order/status slice·API evidence 담당. |
| 38 | WBS-036 | 프론트: 관리자 주문 관리/상세 화면 구현 | WBS2-035, WBS2-036, WBS2-037 | SUPERSEDED | EXCLUDED | Live order, list, status/TTS 정책이 WBS2에서 분리 범위. |
| 39 | WBS-EXT-001 | [삭제요망] 장바구니 서버 검증 | WBS2-050 | SUPERSEDED | EXCLUDED | Legacy replacement/삭제 표식은 WBS2 transaction validation으로 대체. |
| 40 | WBS-EXT-002 | [삭제요망] 관리자 결제수단 설정 | WBS2-040 | SUPERSEDED | EXCLUDED | Legacy replacement/삭제 표식은 WBS2 Admin payment 작업으로 대체. |
| 41 | WBS-006 | Git 전략 · 백로그 티켓화 | WBS2-002, WBS2-064 | SUPERSEDED | EXCLUDED | 현재 저장소 baseline·문서 handoff가 generic legacy task 대체. |
| 42 | WBS-007 | 프론트: 메뉴선택 화면 구현 | WBS2-017, WBS2-018 | SUPERSEDED | EXCLUDED | Route 평가와 menu-list contract가 독립 추적. |
| 43 | WBS-009 | 프론트: 장바구니 화면 구현 | WBS2-022 to WBS2-025 | SUPERSEDED | EXCLUDED | 수량 한도, toast, cart edit/delete가 분리 범위. |
| 44 | WBS-014 | 주간 데모 & 회고 | — | UNIQUE_LEGACY | TODO 유지 | 진행 중 팀 조율에 중복 WBS2 구현 범위 없음. |
| 45 | WBS-017 | 시나리오 기반 QA | WBS2-061 to WBS2-063 | SUPERSEDED | EXCLUDED | Requirement, accessibility, regression 실행이 WBS2 QA 레코드로 구분. |
| 46 | WBS-018 | 성능 · UX 개선 | WBS2-032, WBS2-045 | SUPERSEDED | EXCLUDED | Kiosk touch/responsive와 Admin date/totals QA가 현재 제한 범위. |
| 47 | WBS-020 | 최종 리허설 | WBS2-061 to WBS2-064 | SUPERSEDED | EXCLUDED | 최종 통합 QA·문서/demo handoff가 WBS2로 표현됨. |

## 결과 운영 건수

| Metric | Count | Calculation |
|---|---:|---|
| Legacy active | 6 | 5 `COMPLETED_WITH_EVIDENCE` + 1 retained `UNIQUE_LEGACY` |
| Active WBS2 | 66 | WBS2-065 Release와 WBS2-066 Presentation/Demo가 Legacy Internal ID 24에서 분리 |
| Active total | 72 | `6 + 66` |
| Newly superseded Legacy | 31 | 30 `SUPERSEDED` + 1 Future Scope `UNIQUE_LEGACY` |
| Legacy `UNIQUE_LEGACY` retained | 1 | Internal ID 44 |
| `NEEDS_CONFIRMATION` | 1 | WBS2-066 대표 Primary Owner 미합의 |
| DONE | 8 | evidence-backed Legacy 5 + evidence-backed WBS2 3 |
| EXCLUDED | 98 | 이전 duplicate 67 + 여기서 제외한 Legacy 31 |
| Total WBS | 170 | WBS2 split 2건 생성; 레코드 삭제 없음 |

남은 사람 결정: WBS2-065 배포 환경/Release Candidate 담당 (`BLOCKED`), WBS2-066 대표 Primary Owner (`NEEDS_CONFIRMATION`).
