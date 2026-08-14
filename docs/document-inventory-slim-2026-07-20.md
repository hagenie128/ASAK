# 문서 인벤토리 (슬림)

> 갱신: **2026-08-14** · 대형 archive 제거와 Product Bible 통합 반영.
> 진입: [START_HERE](START_HERE.md) · 태그: [document-tag-index-2026-07-20.md](document-tag-index-2026-07-20.md)

## KEEP_ACTIVE (매일~이번 스프린트)

| 경로 | 역할 |
|---|---|
| `docs/START_HERE.md` | 단일 진입 |
| `docs/wiki/current-status-baseline.md` | `#historical` 2026-08-07 코드 현실 요약 |
| `docs/planning/current-implementation-map-2026-07-16.md` | `#historical` 2026-07-23 SCR별 상태표 |
| `docs/planning/app-implementation-hub.md` | Bible / guide / PLAN 역할 표 |
| `docs/wiki/wbs.md` | 할 일 정본 |
| `docs/wiki/wbs-status-notes.md` | WBS↔코드 요약 |
| `docs/wiki/index.md` | 위키 색인 |
| `docs/architecture/document-code-gap-report-2026-07-16.md` | `#historical` 2026-07-20 Gap |
| `docs/governance/canonical-contract-decisions-2026-07-16.md` | 계약 |
| `docs/governance/document-status-manifest-2026-07-16.md` | 상태 매니페스트 |
| `docs/product_bible/product-bible-hub.md` | **바이블 읽기 허브** (역할별·MVP 15) |
| `docs/product_bible/README.md` | Pack별 전체 목록 |
| `docs/design/README.md` + 플러그인 3종 | 동결 Figma 기준·실행 도구 |
| `docs/implementation_guide/00-start-here.md` | 구현 작업대 |
| `ASAK-Kiosk/IMPLEMENTATION_PLAN.md` + `STRUCTURE_GUIDE.md` | 키오스크 가이드 |
| `ASAK-Admin/src/STRUCTURE_GUIDE.md` + `public/mocks/README.md` | 관리자 가이드 (루트 PLAN 삭제됨) |
| `ASAK-back/IMPLEMENTATION_PLAN.md` | 백엔드 계획 |
| 워크스페이스 `ui-index.md` | Figma↔코드 |

## HISTORICAL_BANNER (배너만 · 삭제 금지)

| 경로 | 대신 볼 것 |
|---|---|
| `docs/wiki/wbs-schedule.md` · `wbs-v2-2026-07-16.md` | → `wbs.md` 리다이렉트 |
| `docs/wiki/requirements-definition.md` 등 Notion export 5종 | Product Bible Pack |
| `docs/wiki/snapshots/README.md` | 과거 JSON 제거 안내 |
| `docs/planning/implementation-priority-2026-07-16.md` | 구현 맵 · app-implementation-hub |
| `docs/governance/repository-cleanup-inventory-2026-07-16.md` 등 감사 3종 | document-inventory-slim |
| 날짜별 design QA·교정·토큰 보고 | `#historical` · design/README |
| 삭제한 archive 이력 | Git history · START_HERE |
| ASAK 루트 `README.md` (레거시 frontend/) | START_HERE · 워크스페이스 README |

## 2026-08-14 완료한 정리

| 조치 | 내용 |
|---|---|
| archive 감축 | `docs/_archive`, `docs/design/_archive`, `docs/product_bible/_archive` 제거 |
| 고유 자산 승격 | future scope, API 피드백, Figma 플러그인·토큰·체크리스트 |
| Product Bible | Pack 유지, 181개 원문을 46개 통합 문서로 재구성 |
| 링크 | 통합 문서와 승격 경로로 내부 링크 치환 |
| 라벨 | 코드 실측·계획·Figma 완료 기록을 시점 스냅샷으로 명시 |

## 원칙

1. 활성 정본은 **START_HERE와 Pack README**에서 찾는다.
2. 병합 문서는 원문 파일명별 구획을 유지해 추적성을 보존한다.
3. `docs/notion`, `worklog/daily`는 스크립트 입력 — 무단 이동 금지
4. 삭제된 이력은 Git history에서 조회하며 활성 기준으로 되돌리지 않는다.
