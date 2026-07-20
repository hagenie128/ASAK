# DevCopilot Sync Report

## 코드 기준 재동기화 (2026-07-20)

문서(07-16)만 믿지 않고 **실제 코드**를 1차 정본으로 재감사했습니다.

| 항목 | 결과 |
|---|---|
| WBS2-001~066 제목 | 전부 **한글**로 통일 (`update_wbs_task`) |
| WBS P3/P4 상태 | 코드 증거 반영 (예: 라우트·수량한도 DONE, Admin 정적 UI IN_PROGRESS, 결제 flow TODO) |
| LMIS 요구사항 8건 | UI shell 존재 → `IN_PROGRESS` (DONE 아님) |
| 화면 SCR-020~024 | 월별/일별 매출·대시보드 / 영수증·멤버십은 향후 범위로 정리 |
| Target API | MCP update 불가 → `[TARGET]` create: `/api/kiosk/*`, `/api/admin/soldOut`, sales summary/monthly |
| 로컬 문서 | `current-status-baseline.md`, `wbs-v2.md`, `screens.json` 동시 갱신 |

**코드 현실 요약**

- Kiosk: Home→장바구니 mock 동작. 결제/타임아웃은 shell.
- Admin: Figma 정적 화면 연결. mock repository는 있으나 Page 연동 0.
- Backend: `GET /api/health`만.

정본 우선순위: **코드 → Canonical/Product Bible → DevCopilot → 구 문서**.

## Legacy 의미 중복 후속 (2026-07-16)

DevCopilot internal record ID 기준으로 활성 Legacy WBS 37건을 활성 WBS2 64건과 감사했습니다. 상세 매핑, 대체 사유, evidence는 [legacy-wbs2-mapping-audit-2026-07-16.md](legacy-wbs2-mapping-audit-2026-07-16.md)를 참고하세요.

| Metric | Before audit | After audit | Formula / reason |
|---|---:|---:|---|
| Legacy Active | 37 | 6 | Legacy Internal ID 24 분리·제외; 레코드 삭제 없음 |
| WBS2 Active | 64 | 66 | WBS2-065 Release, WBS2-066 Presentation/Demo 생성 |
| Active total | 101 | 72 | `6 + 66` |
| DONE | 9 | 8 | Legacy Internal ID 29는 planned Notion source만 있고 backend evidence 없음; DONE 아님 |
| EXCLUDED | 67 | 98 | duplicate `67` + Legacy superseded/future `31` |
| Total WBS | 168 | 170 | WBS2 split 2건 생성; 삭제 없음 |
| Dashboard WBS progress | 5.4% | 4.7% | `8 DONE / 170 total records = 4.71%` |
| Operational WBS progress | n/a | 11.1% | `8 DONE / 72 Active records = 11.11%`; EXCLUDED 제외 |

`DevCopilot 대시보드 WBS 진행률은 운영상 신뢰할 수 없습니다`. 관측된 대시보드 공식 분모에 `EXCLUDED` 레코드가 포함됩니다. 시스템 지표는 수정하지 말고, 현재 실행 추적에는 위 operational 공식을 사용하세요.

### Release and presentation split

Legacy Internal ID 24는 `[SUPERSEDED]`·`EXCLUDED`로 보존한 뒤 소스 코드 변경 없이 분리:

| WBS2 ID | DevCopilot status | Owner | Definition of Done | Evidence |
|---|---|---|---|---|
| WBS2-065 | BLOCKED | Primary 하진; Support 나연 | branch/PR, 저장소별 빌드, 환경, release checklist, RC 검토; 배포 환경/담당 확인. | Product Bible Release Checklist 존재; 환경·RC evidence 아직 없음. |
| WBS2-066 | TODO | `NEEDS_CONFIRMATION` Primary; Team 공동 | 슬라이드, Kiosk/Admin Demo 1–5 순서, 스크립트, contingency, 리허설 팀 검토. | 2026-07-03 회의에서 하진·나연 공동 발표/demo owner; Demo Scenario 존재; 대표 owner·리허설 evidence 아직 없음. |

### DONE evidence 검증

| Internal ID | Task ID | Result | Evidence boundary |
|---:|---|---|---|
| 10 | WBS-001 | DONE 유지 | Menu/option design/data 정의 존재; React 완료 주장 없음. |
| 15 | WBS-003 | DONE 유지 | Stack/role 문서 존재; 기능 완료 주장 없음. |
| 16 | WBS-004 | DONE 유지 | ERD/API 문서 존재; backend API 완료 주장 없음. |
| 27 | WBS-024 | DONE 유지 | Seed bundle에 menu/ingredient/option 데이터; 앱 migration은 미완. |
| 29 | WBS-026 | EXCLUDED로 변경 | Source는 planned, backend 구현 evidence 없음. |
| 31 | WBS-023 | DONE 유지 | Schema constraint 산출물 존재; 연결된 앱 migration 아님. |
| 119 | WBS2-001 | DONE 유지 | Baseline snapshot 문서 존재. |
| 120 | WBS2-002 | DONE 유지 | 저장소 actual/target baseline 문서 존재. |
| 127 | WBS2-009 | DONE 유지 | Design-system evidence 검토 존재; design-only. |

> 기준일: 2026-07-16 · Status: IN_PROGRESS

## 지원 MCP 변경

Requirements, scenarios, screens, WBS tasks, API specs, DB tables/columns, QA test cases, bug reports를 읽거나 업데이트할 수 있습니다.

## 적용 변경

| Area | Before | After | Change |
|---|---:|---:|---|
| Requirements | DONE 3 / TODO 47 / EXCLUDED 7 | TODO 33 / IN_PROGRESS 11 / EXCLUDED 13 | 미지원 DONE 제거; 기존 Kiosk scaffold를 IN_PROGRESS 기록; 명시적 future scope를 MVP 밖으로 이동 |
| Scenarios | DRAFT 24 | DRAFT 21 / ARCHIVED 3 | Receipt, membership, QR 시나리오를 Future Scope로 보존 |
| Screens | 21 | 24 | SCR-020/021을 Monthly/Daily Sales로 migration; SCR-022 Dashboard 및 archived SCR-023/024 추가 |
| WBS | 65 | 170 records | Legacy·우발 duplicate 보존; Release/Presentation split 포함 활성 WBS2 66건 |
| QA | TODO 16 | TODO 16 | PASS 주장 없음; Future Scope 테스트는 제목만 변경 |
| Bugs | 0 | 0 | 테스트 실행 없음 |

## 초기 WBS reconciliation (internal record ID 기준)

> 이 표는 원래 duplicate reconciliation을 보존합니다. Legacy semantic-overlap 감사·Release/Presentation split 이후 최종 건수는 위 follow-up 섹션을 참고하세요.

| Category | Record count | Meaning |
|---|---:|---|
| Before: total WBS | 65 | 원 DevCopilot 레코드 |
| Before: unique Task ID | 37 | `65 - 28` duplicate extra records |
| Before: duplicate Task ID groups | 28 | legacy 그룹마다 추가 레코드 1개 |
| Before: duplicate additional records | 28 | EXCLUDED로 보존, 삭제 안 함 |
| New intended WBS2 | 64 | 고유 활성 `WBS2-001`–`WBS2-064` |
| Existing retained Active | 37 | 원 대표 레코드 |
| Existing EXCLUDED / ARCHIVED | 0 / 0 | baseline에 해당 WBS status 없음 |
| New EXCLUDED | 67 | legacy duplicate 28 + 우발 WBS2 duplicate 39 |
| After: total records | 168 | `37 active legacy + 64 active WBS2 + 67 EXCLUDED` |
| After: Active | 101 | TODO 74 / DONE 9 / IN_PROGRESS 12 / BLOCKED 6 |
| After: EXCLUDED | 67 | 모두 `[ARCHIVED DUPLICATE]` 표시; 영구 삭제 없음 |
| After: other status | 0 | WBS ARCHIVED record status 없음 |

`67`은 duplicate Task ID 그룹 수도 Legacy WBS 총수도 아닙니다. EXCLUDED로 보존한 **추가 duplicate record** 총수입니다. legacy duplicate Task ID 그룹 28개, reconciliation 후 활성 duplicate Task ID 그룹 0.

`WBS2-006`은 Future Scope를 분리하는 문서 작업이라 활성 유지; Future Scope 구현 작업이 아닙니다.

## API mismatch record

| API ID | Existing DevCopilot path | Latest target path | Implementation evidence | Decision needed | Status |
|---|---|---|---|---|---|
| API-002/003/004 | `/api/menus/**` | `/api/kiosk/menuList`, `/api/kiosk/menuDetail/{menuId}` | Backend menu API 없음 | Adapter/contract 선택 | TODO |
| API-005 | `/api/orders` | `/api/kiosk/orders` | Backend order API 없음 | Canonical path 승인 | TODO |
| API-006 | `/api/payments` | `/api/kiosk/payments` | Backend payment API 없음 | Canonical path 승인 | TODO |
| API-009 | `/api/admin/sold-out-items` | `/api/admin/soldOut` | Backend sold-out API 없음 | Canonical path 승인 | TODO |

MCP는 API create/read만 노출하고 update/archive는 없습니다. 해당 capability 전까지 이 표가 권위 있는 비파괴 reconciliation 기록입니다.

## Dashboard 재계산

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Requirement implementation | 5.3% | 0.0% | 미지원 DONE 3건 수정; IN_PROGRESS는 DONE으로 취급 안 함 |
| Traceability | 87.7% | 87.7% | MCP가 explicit link mutation 미노출 |
| WBS progress | 9.2% | 5.4% | `9 DONE / 168 total records = 5.36%`; MCP가 분모에 EXCLUDED 67 포함. 계산 한계이지 delivery regression 아님. |
| QA pass | 0.0% | 0.0% | 실행 evidence 없음 |
| Open bug | 0 | 0 | 테스트 실행 없음 |

## MCP_UNSUPPORTED

- Native backup/export
- Member management
- Kanban board management
- Wiki/checklist management
- Explicit traceability-link mutation

## Metric verification limitation

`MCP_UNSUPPORTED`: dashboard 계산 공식과 분모 설정이 노출되지 않습니다. 관측 WBS 값은 EXCLUDED가 여전히 포함됨(`9 / 168`)을 보여 주며, traceability는 numerator/denominator 없이 시스템 제공 87.7%입니다. 지표 개선만을 위해 상태를 바꾸지 마세요.

## Safety controls

- 모든 mutation 전 로컬 baseline snapshot.
- 소스 코드, Figma, kiosk remote, pull/reset/rebase, 파괴적 delete는 범위 밖.
- Legacy duplicate WBS는 status/title 메모로만 표시·보존.
- DevCopilot의 API/DB 명세 존재만으로 implementation evidence로 쓰지 않음.
