# ASAK WBS 2.0

> 2026-07-16 Legacy 의미 중복 감사: 권위 있는 37건 매핑은 [legacy-wbs2-mapping-audit-2026-07-16.md](legacy-wbs2-mapping-audit-2026-07-16.md)를 참고하세요. `DevCopilot 대시보드 WBS 진행률은 운영상 신뢰할 수 없습니다`: 관측된 분모에 `EXCLUDED` 레코드가 포함됩니다. 팀 운영용으로는 활성 범위 진행률을 별도로 사용하세요.

> 기준일: 2026-07-16 · Legacy `WBS-*` 레코드는 보존됩니다. `WBS2-*`는 실행 계획이며 소스 코드 완료를 의미하지 않습니다.

## 필드 계약

모든 작업은 WBS2 ID, Phase, Epic, Work Package, Detailed Task, Deliverable, Repository, Primary Owner, Support Owner, Review Owner, QA Owner, Dependency, Handoff Condition, Start/Target Date, Status, Definition of Done, Evidence, Requirement, Scenario, SCR, API, DB, QA, Notes를 사용합니다. 아래 간략 표에서 **Handoff condition + Evidence / linked scope가 행 단위 Definition of Done**입니다: handoff condition을 충족하고 evidence가 구체적일 때만 행을 DONE으로 둘 수 있습니다. `—`는 해당 없음, `NEEDS_CONFIRMATION`은 evidence 또는 담당이 아직 확정되지 않음을 뜻합니다.

## 실행 백로그

| ID | Phase / work package | Detailed task | Repository | Primary / support | Status | Handoff condition | Evidence / linked scope |
|---|---|---|---|---|---|---|---|
| WBS2-001 | P1 Baseline / Snapshot | MCP baseline 및 지표 값 보존 | ASAK | 하진 / — | DONE | Snapshot 검토 완료 | Snapshot, DEV-SYS-002 |
| WBS2-002 | P1 Baseline / Repository | 4개 저장소 실제/목표 맵 기록 | ASAK | 하진 / — | DONE | Map 검토 완료 | current-status-baseline |
| WBS2-003 | P1 Baseline / Kiosk remote | ASAK-front vs ASAK-Kiosk 정본 저장소 확인 | ASAK-Kiosk | 나연 / 하진 | BLOCKED | 담당자가 마이그레이션 계획 확인 | NEEDS_CONFIRMATION |
| WBS2-004 | P1 Baseline / Kiosk remote | 마이그레이션 전 브랜치·미커밋 작업 비교 | ASAK-Kiosk | 나연 / 하진 | BLOCKED | 나연이 evidence 제공 | NEEDS_CONFIRMATION |
| WBS2-005 | P1 Baseline / Docs | 요구사항·시나리오·화면 ID 충돌 감사 | ASAK | 하진 / — | IN_PROGRESS | 발견 사항 연결 완료 | traceability-matrix |
| WBS2-006 | P1 Baseline / Docs | MVP와 향후 범위 분리 | ASAK | 하진 / — | IN_PROGRESS | 범위 문서 검토 완료 | future-scope |
| WBS2-007 | P1 Baseline / API | Legacy→목표 API 갭 표 게시 | ASAK | 하진 / 나연 | IN_PROGRESS | 백엔드 검토 요청 | rest-api-spec |
| WBS2-008 | P1 Baseline / DB | 비파괴 DB 감사 계획 준비 | ASAK | 하진 / 나연 | TODO | 백엔드 산출물 확보 | db-audit-plan |
| WBS2-009 | P2 Design / Foundation | 01-C 토큰 evidence 및 모드 검증 | Figma / ASAK | 하진 / — | DONE | Design QA 기록 | DESIGN_DONE |
| WBS2-010 | P2 Design / Shared | 공유 상태 컴포넌트 문서 검증 | Figma / ASAK | 하진 / — | IN_PROGRESS | Cover/visual QA 검토 | DESIGN_DONE |
| WBS2-011 | P2 Design / Kiosk | 03-C 컴포넌트 구조 매핑 기록 | Figma / ASAK | 하진 / 나연 | IN_PROGRESS | 매핑 승인 | SCR-003–008 |
| WBS2-012 | P2 Design / Admin | 04-C 컴포넌트 구조 매핑 기록 | Figma / ASAK | 하진 / — | IN_PROGRESS | 매핑 승인 | SCR-009–022 |
| WBS2-013 | P2 Design / Kiosk screens | 05-C 화면 instance-apply 갭 기록 | Figma / ASAK | 하진 / 나연 | TODO | Figma 담당 확인 | DESIGN_DONE only |
| WBS2-014 | P2 Design / Admin screens | 06-C active-work 충돌 경계 기록 | Figma / ASAK | 하진 / — | IN_PROGRESS | active agent와 충돌 없음 | SCR-019–022 |
| WBS2-015 | P2 Design / Accessibility | 고대비 검토 체크리스트 정의 | ASAK | 하진 / 나연 | TODO | Design·구현 evidence | FWD-UI-001 |
| WBS2-016 | P2 Design / Prototype | prototype/instance swap 보류 기록 | Figma / ASAK | 하진 / — | TODO | Figma 담당 evidence | NEEDS_CONFIRMATION |
| WBS2-017 | P3 Kiosk / Route | home/menu/detail route 보존·평가 | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Route 검토 완료 | SCR-001,003,004 |
| WBS2-018 | P3 Kiosk / Menu | menu-list response adapter 계약 검증 | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Contract 검토 | FWD-MENU-001, API target |
| WBS2-019 | P3 Kiosk / Detail | menu-detail response adapter 계약 검증 | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Contract 검토 | SCR-004 |
| WBS2-020 | P3 Kiosk / Options | 옵션 선택 검증 구현/검증 | ASAK-Kiosk | 나연 / — | IN_PROGRESS | Interaction evidence | FWD-MENU-002 |
| WBS2-021 | P3 Kiosk / Allergy | 조건부 알레르기 고지 구현 | ASAK-Kiosk | 나연 / — | TODO | UI·QA evidence | FWD-MENU-004 |
| WBS2-022 | P3 Kiosk / Store | 동일 메뉴 최대 수량 9 적용 | ASAK-Kiosk | 나연 / — | TODO | Store 테스트 evidence | cart policy |
| WBS2-023 | P3 Kiosk / Store | 장바구니 총 최대 30 적용 | ASAK-Kiosk | 나연 / — | TODO | Store 테스트 evidence | cart policy |
| WBS2-024 | P3 Kiosk / Store | 한도 전용 4초 toast 동작 추가 | ASAK-Kiosk | 나연 / — | TODO | Interaction evidence | cart policy |
| WBS2-025 | P3 Kiosk / Cart | cart route 및 항목 수정/삭제 연동 | ASAK-Kiosk | 나연 / 하진 | TODO | SCR-005 route 동작 | FWD-CART-002 |
| WBS2-026 | P3 Kiosk / Payment | payment-method route·표시 연동 | ASAK-Kiosk | 나연 / — | TODO | SCR-007 route 동작 | FWD-PAY-001 |
| WBS2-027 | P3 Kiosk / Payment | 결제 실패·장바구니 유지 처리 | ASAK-Kiosk | 나연 / — | TODO | Error-flow evidence | SCR-012, TC-004 |
| WBS2-028 | P3 Kiosk / Complete | 주문번호·금액·대기 건수·홈 액션 렌더 | ASAK-Kiosk | 나연 / — | TODO | Completion evidence | SCR-008 |
| WBS2-029 | P3 Kiosk / Timeout | 30s, 20s 경고, 10s 카운트다운 구현 | ASAK-Kiosk | 나연 / — | TODO | Timer QA evidence | SCR-013 |
| WBS2-030 | P3 Kiosk / Timeout | 결제 PROCESSING 중 timeout 비활성화 | ASAK-Kiosk | 나연 / — | TODO | Payment-state evidence | SCR-013 |
| WBS2-031 | P3 Kiosk / States | 핵심 흐름에 loading/empty/error 상태 추가 | ASAK-Kiosk | 나연 / — | TODO | State QA evidence | FWD-MENU-001 |
| WBS2-032 | P3 Kiosk / QA | 터치 타깃·반응형 검토 | ASAK-Kiosk | 나연 / 하진 | TODO | QA 실행 | 48px target |
| WBS2-033 | P4 Admin / Route | route metadata를 Screen Registry와 정렬 | ASAK-Admin | 하진 / — | TODO | Registry 검토 | SCR-022,009–021 |
| WBS2-034 | P4 Admin / Dashboard | `/` Dashboard shell 구현 | ASAK-Admin | 하진 / — | TODO | Route·state evidence | SCR-022 |
| WBS2-035 | P4 Admin / Live order | `/orders/live` Live Order shell 구현 | ASAK-Admin | 하진 / — | TODO | Route evidence | SCR-009 |
| WBS2-036 | P4 Admin / Orders | `/orders` 주문 관리 목록 구현 | ASAK-Admin | 하진 / — | TODO | Screen evidence | SCR-010 |
| WBS2-037 | P4 Admin / Orders | 주문 상태 업데이트 UI·TTS 정책 구현 | ASAK-Admin | 하진 / — | TODO | PATCH/TTS evidence | LMIS-ORDER-003 |
| WBS2-038 | P4 Admin / Sold-out | `/soldOut` 페이지·저장 상태 구현 | ASAK-Admin | 하진 / — | TODO | UI state evidence | SCR-011 |
| WBS2-039 | P4 Admin / Menu | 메뉴 관리 shell 구현 | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-016 |
| WBS2-040 | P4 Admin / Payments | 결제수단 shell 구현 | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-018 |
| WBS2-041 | P4 Admin / Sales | 매출 요약 shell 구현 | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-019 |
| WBS2-042 | P4 Admin / Sales | 월별 매출 화면 구현 | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-020 |
| WBS2-043 | P4 Admin / Sales | 일별 매출 화면 구현 | ASAK-Admin | 하진 / — | TODO | UI evidence | SCR-021 |
| WBS2-044 | P4 Admin / States | loading/empty/error/navbar 상태 추가 | ASAK-Admin | 하진 / — | TODO | State QA evidence | Admin common |
| WBS2-045 | P4 Admin / QA | 날짜 필터·합계·활성 내비 검증 | ASAK-Admin | 하진 / 나연 | TODO | QA 실행 | Sales/Admin QA |
| WBS2-046 | P5 Backend / Baseline | persistence 구현 결정 기록 추가 | ASAK-back | 하진 / 나연 | TODO | 팀 결정 | DB audit |
| WBS2-047 | P5 Backend / Schema | schema/migration/seed 접근 방식 선택 | ASAK-back | 하진 / 나연 | TODO | 검토 승인 | DB audit |
| WBS2-048 | P5 Backend / Menu | Menu List controller/service/repository slice 구현 | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API 테스트 evidence | GET menuList |
| WBS2-049 | P5 Backend / Menu | Menu Detail controller/service/repository slice 구현 | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API 테스트 evidence | GET menuDetail |
| WBS2-050 | P5 Backend / Orders | 주문 검증·트랜잭션 slice 구현 | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API 테스트 evidence | POST orders |
| WBS2-051 | P5 Backend / Payments | 결제 승인/실패 slice 구현 | ASAK-back | NEEDS_CONFIRMATION / 나연 | TODO | API 테스트 evidence | POST payments |
| WBS2-052 | P5 Backend / Admin | sold-out slice 구현 | ASAK-back | NEEDS_CONFIRMATION / 하진 | TODO | API 테스트 evidence | PATCH soldOut |
| WBS2-053 | P5 Backend / Admin | 주문 조회/상태 slice 구현 | ASAK-back | NEEDS_CONFIRMATION / 하진 | TODO | API 테스트 evidence | Admin orders |
| WBS2-054 | P5 Backend / Sales | 매출 집계 소스 정의·구현 | ASAK-back | NEEDS_CONFIRMATION / 하진 | TODO | 합계 검증 | sales views |
| WBS2-055 | P5 Backend / Common | error envelope·validation evidence 추가 | ASAK-back | NEEDS_CONFIRMATION / — | TODO | Contract tests | API common |
| WBS2-056 | P5 Backend / DB | Modeler, schema, entity, FK, index, constraints 비교 | ASAK / ASAK-back | 하진 / 나연 | TODO | Audit report | db-audit-plan |
| WBS2-057 | P6 Integration / Contracts | canonical field용 adapter 매핑 정의 | ASAK-Kiosk / ASAK-Admin | 나연 / 하진 | TODO | Contract 검토 | totalAmount 등 |
| WBS2-058 | P6 Integration / Kiosk | 승인된 backend contract 기준 kiosk 연동 | ASAK-Kiosk | 나연 / — | BLOCKED | Backend contract 존재 | Kiosk API |
| WBS2-059 | P6 Integration / Admin | 승인된 backend contract 기준 admin 연동 | ASAK-Admin | 하진 / — | BLOCKED | Backend contract 존재 | Admin API |
| WBS2-060 | P6 Integration / Sales | 결제/주문/시간 합계 검증 | All | 하진 / 나연 | BLOCKED | Sales source 존재 | Sales QA |
| WBS2-061 | P7 QA / Requirement | 요구사항 기반 테스트 실행·실제 결과 기록 | All | 나연 / 하진 | TODO | 실행 evidence | QA suite |
| WBS2-062 | P7 QA / Accessibility | 고대비·키보드·터치 테스트 실행 | All | 나연 / 하진 | TODO | 실행 evidence | Accessibility QA |
| WBS2-063 | P7 QA / Regression | kiosk/admin 통합 회귀 테스트 | All | 나연 / 하진 | BLOCKED | 통합 앱 사용 가능 | Regression QA |
| WBS2-064 | P8 Docs / Handoff | evidence, WBS, traceability, demo checklist 동기화 | ASAK | 하진 / 나연 | IN_PROGRESS | 사람 검토 | DevCopilot sync |
| WBS2-065 | P8 Release / Readiness | branch/PR 상태, 저장소 빌드, 환경 설정, release checklist, Release Candidate 점검 | All repositories | 하진 / 나연 | BLOCKED | 모든 저장소 점검 통과; 배포 환경·담당 확인; Release Candidate 검토 | Definition of Done: checklist 승인 및 RC evidence 첨부. Evidence: [Release Checklist](../product_bible/09_QA_Bible/docs/10-qa/07-demo-release/RELEASE_CHECKLIST.md); 환경/RC evidence 아직 없음. |
| WBS2-066 | P8 Presentation / Demo | 슬라이드, demo 순서, Kiosk/Admin 시나리오, 스크립트, 비상 대안, 최종 리허설 준비 | All repositories | NEEDS_CONFIRMATION / Team | TODO | 슬라이드, 스크립트, Demo 1–5 순서, fallback, 최종 리허설 기록이 팀 검토 완료 | Definition of Done: 팀 검토 및 리허설 evidence 완료. Evidence: 2026-07-03 회의에서 발표/demo를 하진·나연이 공동 담당; [Demo Scenario](../product_bible/09_QA_Bible/docs/10-qa/07-demo-release/DEMO_SCENARIO.md). 대표 Primary Owner 미합의. |

## 담당 및 검토

- Primary owner는 책임 현재 리드; support는 계획된 경우만 기록합니다.
- Review owner: 구조·Admin·DevCopilot·문서는 하진; Kiosk 데이터 I/O는 나연; 통합 결정은 공동 검토.
- QA owner: Kiosk 흐름은 나연, Admin/데이터·문서 흐름은 하진, 통합 QA는 둘 다.
- 저장소 마이그레이션·backend 담당이 확정될 때까지 목표 일정은 의도적으로 미정입니다. 허위 일정을 만들지 않기 위함입니다.
