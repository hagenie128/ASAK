# ASAK 위키 색인

> 현재 운영 진입점 — **2026-07-20** (코드 실측 동기화).  
> **전체 문서 입구:** [START_HERE](../START_HERE.md) · WBS 실행 정본은 **[wbs-v2-2026-07-16.md](wbs-v2-2026-07-16.md)** (+ [상태 메모](wbs-status-notes.md)).  
> `wbs-schedule.md`는 Historical — 실행에 쓰지 말 것.

## 지금 상태 (먼저)

- [현재 상태 baseline](current-status-baseline.md) ← **요약 1순위**
- [구현 맵](../planning/current-implementation-map-2026-07-16.md) ← **SCR별 상세**
- [WBS 2.0](wbs-v2-2026-07-16.md) ← **할 일 정본**
- [WBS 상태 메모](wbs-status-notes.md) ← 코드↔WBS↔DevCopilot 요약
- [문서–코드 Gap](../architecture/document-code-gap-report-2026-07-16.md)
- [앱 구현 허브](../planning/app-implementation-hub.md)

## 계획·스프린트

- [프론트 3일 WBS](../planning/frontend-wednesday-wbs-2026-07-20.md)
- [구현 우선순위](../planning/implementation-priority-2026-07-16.md) *(목표 순서 — 현실은 구현 맵)*
- [Canonical 계약](../governance/canonical-contract-decisions-2026-07-16.md)
- [전체 흐름도 (Mermaid)](project-flow.md)

## 추적·범위 (Historical — `_archive/wiki-secondary`)

- [추적성 매트릭스](../_archive/wiki-secondary/traceability-matrix.md)
- [향후 범위](../_archive/wiki-secondary/future-scope.md)
- [DevCopilot 동기화 보고](../_archive/wiki-secondary/devcopilot-sync-report.md)
- [레거시 WBS2 매핑 감사](../_archive/wiki-secondary/legacy-wbs2-mapping-audit-2026-07-16.md)
- [WBS 일정(레거시)](wbs-schedule.md) — 실행에 쓰지 말 것

## DB·API·QA (Notion export — Historical)

> 정본: [Product Bible 허브](../product_bible/product-bible-hub.md) · API 계약: [Canonical](../governance/canonical-contract-decisions-2026-07-16.md)

- [DB 테이블](db-table-definition.md)
- [DB 뷰](db-view-definition.md) ← **메뉴/주문/품절/매출 View**
- [DB 약어](../_archive/wiki-secondary/db-abbreviation-glossary.md)
- [DB 감사 계획](../_archive/wiki-secondary/db-audit-plan.md)
- [REST API 명세](rest-api-spec.md) *(legacy path 보존)*
- [요구사항](requirements-definition.md)
- [시나리오](user-scenarios.md)
- [QA 케이스](qa-test-cases.md)
- [화면·Figma](screen-design-figma.md) *(SCR 정본: Pack 07)*

## 스냅샷

- [DevCopilot baseline 2026-07-16](../_archive/wiki-secondary/snapshots/devcopilot-baseline-2026-07-16.md) (역사)
- 앱 구조: `ASAK-Kiosk/src/STRUCTURE_GUIDE.md`, `ASAK-Admin/src/STRUCTURE_GUIDE.md`
- 앱 계획: 각 저장소 `IMPLEMENTATION_PLAN.md`

제품 정책 정본은 `docs/product_bible`입니다. Wiki·Notion export는 요약/동기화용이며 **구현 DONE 증거로 쓰지 않습니다**.
