# 문서 인벤토리 (슬림)

> 갱신: **2026-07-20** · 삭제 없음.  
> 진입: [START_HERE](START_HERE.md)

## KEEP_ACTIVE (매일~이번 스프린트)

| 경로 | 역할 |
|---|---|
| `docs/START_HERE.md` | 단일 진입 |
| `docs/wiki/current-status-baseline.md` | 코드 현실 |
| `docs/wiki/wbs-v2-2026-07-16.md` | 할 일 정본 |
| `docs/wiki/wbs-status-notes.md` | WBS↔코드 요약 |
| `docs/wiki/index.md` | 위키 색인 |
| `docs/planning/CURRENT_IMPLEMENTATION_MAP.md` | 화면 상태표 |
| `docs/architecture/DOCUMENT_CODE_GAP_REPORT.md` | Gap |
| `docs/governance/CANONICAL_CONTRACT_DECISIONS.md` | 계약 |
| `docs/governance/DOCUMENT_STATUS_MANIFEST.md` | 상태 매니페스트 |
| `docs/product_bible/README.md` | 바이블 얇은 안내 |
| `docs/planning/FRONTEND_WEDNESDAY_WBS_2026-07-20.md` | 3일 스프린트 |
| `ASAK-Kiosk|Admin/IMPLEMENTATION_PLAN.md` + `STRUCTURE_GUIDE.md` | 앱 가이드 |
| `ASAK-back/IMPLEMENTATION_PLAN.md` | 백엔드 계획 |
| 워크스페이스 `UI-INDEX.md` | Figma↔코드 |

## HISTORICAL_BANNER (배너만 · 삭제 금지)

| 경로 | 대신 볼 것 |
|---|---|
| `docs/wiki/wbs-schedule.md` | `wbs-v2-2026-07-16.md` |
| `docs/wiki/legacy-wbs2-mapping-audit-2026-07-16.md` | `wbs-v2-2026-07-16` · `wbs-status-notes` |
| `docs/wiki/snapshots/*-07-16*` | `devcopilot-sync-report.md` |
| `docs/planning/IMPLEMENTATION_PRIORITY.md` | 목표 순서 — 현실은 MAP/baseline |
| `docs/governance/PRODUCT_BIBLE_INDEX.md` | 세부는 Pack README · 입구는 product_bible/README |
| `docs/governance/REPOSITORY_CLEANUP_INVENTORY_2026-07-16.md` | 정리 이력 |
| `docs/_archive/**` · `docs/design/_archive/**` | 실행 금지 |
| `docs/product_bible/_archive/**` | 구현 기준 제외 |
| ASAK 루트 `README.md` (레거시 frontend/ 설명) | START_HERE · 워크스페이스 README |

## NEEDS_USER_APPROVAL_TO_ARCHIVE (후보만)

승인 전까지 **이동·삭제 금지**. 배너/링크만 유지.

| 후보 | 이유 |
|---|---|
| `docs/wiki/wbs-schedule.md` | Legacy WBS-001~ · 이미 Historical |
| `docs/wiki/legacy-wbs2-mapping-audit-2026-07-16.md` | 1회성 감사 |
| `docs/wiki/meeting-deliverables-checklist.md` | 회의 체크리스트 — 중복 가능 |
| `docs/governance/REPOSITORY_CLEANUP_INVENTORY_2026-07-16.md` | 정리 스냅샷 |
| `docs/_archive/implementation-plans/` | 시점이 있는 계획 보관본 — planning과 중복 여부 정기 검토 |
| Notion stub 다수 (`docs/design/*` 구버전) | Notion 정본이면 Git stub만 유지 |
| `ASAK/README.md` 레거시 `frontend/`·`ASAK-front` 섹션 | 별도 Legacy README로 분리 검토 |

## 원칙

1. 삭제보다 **배너 + START_HERE 링크**  
2. Product Bible 본문 대량 이동 금지  
3. `docs/notion`, `worklog/daily`는 스크립트 입력 — 무단 이동 금지
