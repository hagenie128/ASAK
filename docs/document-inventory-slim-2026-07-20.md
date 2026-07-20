# 문서 인벤토리 (슬림)

> 갱신: **2026-07-20 (오후 정리)** · 삭제 없음.  
> 진입: [START_HERE](START_HERE.md) · 태그: [document-tag-index-2026-07-20.md](document-tag-index-2026-07-20.md)

## KEEP_ACTIVE (매일~이번 스프린트)

| 경로 | 역할 |
|---|---|
| `docs/START_HERE.md` | 단일 진입 |
| `docs/wiki/current-status-baseline.md` | 코드 현실 **요약** |
| `docs/planning/current-implementation-map-2026-07-16.md` | SCR별 **상세** 상태표 |
| `docs/planning/app-implementation-hub.md` | Bible / guide / PLAN 역할 표 |
| `docs/wiki/wbs-v2-2026-07-16.md` | 할 일 정본 |
| `docs/wiki/wbs-status-notes.md` | WBS↔코드 요약 |
| `docs/wiki/index.md` | 위키 색인 |
| `docs/architecture/document-code-gap-report-2026-07-16.md` | Gap |
| `docs/governance/canonical-contract-decisions-2026-07-16.md` | 계약 |
| `docs/governance/document-status-manifest-2026-07-16.md` | 상태 매니페스트 |
| `docs/product_bible/product-bible-hub.md` | **바이블 읽기 허브** (역할별·MVP 15) |
| `docs/product_bible/README.md` | Pack별 전체 목록 |
| `docs/planning/frontend-wednesday-wbs-2026-07-20.md` | 3일 스프린트 |
| `docs/design/README.md` + 실행 스택 8종 | Figma QA·실행·0718 갭 |
| `docs/implementation_guide/00-start-here.md` | 구현 작업대 |
| `ASAK-Kiosk|Admin/IMPLEMENTATION_PLAN.md` + `STRUCTURE_GUIDE.md` | 앱 가이드 |
| `ASAK-back/IMPLEMENTATION_PLAN.md` | 백엔드 계획 |
| 워크스페이스 `ui-index.md` | Figma↔코드 |

## HISTORICAL_BANNER (배너만 · 삭제 금지)

| 경로 | 대신 볼 것 |
|---|---|
| `docs/wiki/wbs-schedule.md` | `wbs-v2-2026-07-16.md` |
| `docs/wiki/requirements-definition.md` 등 Notion export 5종 | Product Bible Pack |
| `docs/wiki/snapshots/*` → `_archive/wiki-secondary/snapshots/` | baseline · wbs-status-notes |
| `docs/planning/implementation-priority-2026-07-16.md` | 구현 맵 · app-implementation-hub |
| `docs/governance/repository-cleanup-inventory-2026-07-16.md` 등 감사 3종 | document-inventory-slim |
| `docs/design/_archive/**` · `docs/design/_archive/figma-plans-2026-07-17/**` | design/README 실행 스택 |
| `docs/_archive/**` · `docs/product_bible/_archive/**` | START_HERE |
| ASAK 루트 `README.md` (레거시 frontend/) | START_HERE · 워크스페이스 README |

## 2026-07-20 완료한 정리

| 조치 | 내용 |
|---|---|
| baseline 복구 | `wiki/current-status-baseline.md` ← `_archive/wiki-secondary` 내용 + 구현 맵 링크 |
| design archive | 중복 실행계획 5종 → `design/_archive/figma-plans-2026-07-17/` |
| Wiki Historical | requirements / rest-api / qa / scenarios / screen-design 배너 |
| 태그 인덱스 | `document-tag-index-2026-07-20.md` 신설 |
| Figma wave rename | active docs → kebab-case (`document-naming-guide`) |

## 원칙

1. 삭제보다 **배너 + START_HERE 링크**  
2. Product Bible 본문 대량 이동 금지  
3. `docs/notion`, `worklog/daily`는 스크립트 입력 — 무단 이동 금지  
4. Figma wave 끝나면 **실행계획은 archive**, QA 통합본만 유지
