# ASAK 문서 — 여기부터 시작

> 초보자용 **단일 진입점** (2026-07-20).  
> 문서가 많아도 **아래 링크만** 따라가면 됩니다. 세부 바이블·아카이브는 필요할 때만.

---

## 1. 지금 상태 (코드 현실)

| # | 문서 | 한 줄 |
|---|---|---|
| 1 | [구현 맵](planning/CURRENT_IMPLEMENTATION_MAP.md) | **구현 현실 1순위** — 화면·mock·API 상태표 |
| 2 | [WBS 상태 메모](wiki/wbs-status-notes.md) | 코드↔WBS 요약 · DevCopilot 한글 제목 |
| 3 | [문서–코드 Gap](architecture/DOCUMENT_CODE_GAP_REPORT.md) | Canonical vs 코드 충돌 |

**한 줄 요약:** Kiosk Home→Cart는 mock 동작 · Admin은 정적 UI + mock READY(미연결) · Backend는 health만.

**그림으로 보기:** [전체 흐름도 (Mermaid)](wiki/project-flow.md) — 저장소 구조·키오스크 주문 흐름·관리자 운영 흐름·데이터/API 목표 흐름·가격·수량 흐름·이번 스프린트 WBS 흐름을 그림 6개로 정리.

---

## 2. 할 일 (WBS)

| # | 문서 | 한 줄 |
|---|---|---|
| 4 | [WBS 상태 메모](wiki/wbs-status-notes.md) | **실행 할 일 확인** — 코드↔WBS 요약 |

레거시 `wbs-schedule.md`(WBS-001~)는 **실행에 쓰지 마세요.**

---

## 3. 앱 가이드 (코딩할 때)

| # | 문서 | 한 줄 |
|---|---|---|
| 6 | [Kiosk 구조](../../ASAK-Kiosk/src/STRUCTURE_GUIDE.md) · [구현 계획](../../ASAK-Kiosk/IMPLEMENTATION_PLAN.md) | P3 · WBS2-017~032 |
| 7 | [Admin 구조](../../ASAK-Admin/src/STRUCTURE_GUIDE.md) · [구현 계획](../../ASAK-Admin/IMPLEMENTATION_PLAN.md) | P4 · WBS2-033~045 |
| 8 | [Backend 구현 계획](../../ASAK-back/IMPLEMENTATION_PLAN.md) | P5 · health only · WBS2-046~056 |

워크스페이스에서 UI 찾을 때: 루트 [`UI-INDEX.md`](../../UI-INDEX.md).

---

## 4. 계약 (Canonical)

| # | 문서 | 한 줄 |
|---|---|---|
| 9 | [Canonical Contract Decisions](governance/CANONICAL_CONTRACT_DECISIONS.md) | API 경로·필드 결정 (코드 미반영 가능) |

충돌 시: **실행 코드 > baseline/맵 > Canonical(목표) > Product Bible**.

---

## 5. Product Bible (팩 README만)

| # | 문서 | 한 줄 |
|---|---|---|
| 10 | [Product Bible 안내](product_bible/README.md) | MVP에 필요한 팩 · FUTURE_SCOPE |
| 11 | [Product Bible Index](governance/PRODUCT_BIBLE_INDEX.md) | Pack 1~12 표 (세부 문서는 필요할 때만) |

세부 계약 문서는 **팩 README를 연 뒤** 필요한 파일만 읽으세요. `_archive`는 구현 기준 아님.

---

## 6. 한물간 / 참고만

| # | 문서 | 한 줄 |
|---|---|---|
| 12 | [Archive](_archive/) | 실행 금지 · 이력 보존 |
| 13 | [Legacy & Reference Index](governance/LEGACY_AND_REFERENCE_INDEX.md) | 비정본 분류 |
| 14 | [문서 이름 규칙](DOCUMENT_NAMING.md) | **신규** 문서 네이밍 |
| 15 | [문서 인벤토리(슬림)](DOC_INVENTORY_SLIM.md) | KEEP / 배너 / 아카이브 후보 |

---

## 매일 볼 문서 5개

1. [구현 맵](planning/CURRENT_IMPLEMENTATION_MAP.md)
2. [wbs-status-notes](wiki/wbs-status-notes.md)
4. 담당 앱 `IMPLEMENTATION_PLAN.md`  
5. [Canonical](governance/CANONICAL_CONTRACT_DECISIONS.md) (계약 건드릴 때)

더 넓은 색인: [docs/README](README.md) · [wiki/index](wiki/index.md) · [PROJECT_HUB](../PROJECT_HUB.md)
