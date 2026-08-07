# ASAK 문서 — 여기부터 시작

> 초보자용 **단일 진입점** (2026-08-07 갱신).
> 문서가 많아도 **아래 링크만** 따라가면 됩니다. 세부 바이블·아카이브는 필요할 때만.

---

## 1. 지금 상태 (코드 현실)

| #   | 문서                                                                 | 한 줄                                                                         |
| --- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | [구현 맵](planning/current-implementation-map-2026-07-16.md)         | **SCR별 상세** — 화면·mock·API 상태표                                         |
| 2   | [baseline 요약](wiki/current-status-baseline.md)                     | **영역별 요약** — Kiosk/Admin/Backend 한눈에                                  |
| 3   | [WBS 상태 메모](wiki/wbs-status-notes.md)                            | 코드↔WBS 요약 · DevCopilot 한글 제목                                          |
| 4   | [문서–코드 Gap](architecture/document-code-gap-report-2026-07-16.md) | 정본 vs 코드 충돌                                                        |
| 5   | [Backend·DB 중간점검](wiki/backend-db-midpoint-audit-2026-07-28.md)  | 실제 원격·Spring context·실DB·읽기 API 점검 결과                              |
| 6   | [주차별 회의록](operations/meeting-minutes/README.md)                | 2조 공식 회의록 · [Hub wiki/78](https://devcopilot.ai.kr/workspace/2/wiki/78) |

**한 줄 요약 (2026-08-07):** Admin 주문(Live·목록·상태·취소)은 BE 연동 **구현·미검증**. 메뉴 GET 부분, 메뉴 CRUD·품절·결제수단·매출/대시보드는 **스텁 또는 mock**. Kiosk는 장바구니→주문 생성→결제(토스 예제) **실연동**이 이번 주 우선. Hub 대시보드 %는 운영 지표로 쓰지 않음. WBS 정본: **[wbs.md](wiki/wbs.md)** (`WBS-001`~`085`).

**이번 주 작업 순서 (선생님):** ① Kiosk 장바구니·주문·결제 DB 검증 → ② Admin 주문 통합 테스트 → ③ 메뉴 CRUD → 품절 → 결제수단 → 매출·대시보드.

**Hub WBS 일정 (8/7 rebase):** P0 주문·연동 `8/7~8/11` · P1 메뉴·품절 `8/11~8/14` · P2 매출·결제수단 `8/14~8/18` · QA `8/18~8/21` · 문서·발표 `~8/28`. 상세: [asak-wbs-date-rebase](ai-reports/2026-08-07/asak-wbs-date-rebase.md).

**그림으로 보기:** [전체 흐름도 (Mermaid)](wiki/project-flow.md) — 저장소 구조·키오스크 주문 흐름·관리자 운영 흐름·데이터/API 목표 흐름·가격·수량 흐름·이번 스프린트 WBS 흐름을 그림 6개로 정리.

---

## 2. 할 일 (WBS)

| #   | 문서                                      | 한 줄                                  |
| --- | ----------------------------------------- | -------------------------------------- |
| 5   | [WBS 통합본](wiki/wbs.md)                 | **정본** — `WBS-001`~`085` (기획→발표) |
| 6   | [WBS 상태 메모](wiki/wbs-status-notes.md) | 코드↔WBS 요약                          |

`wbs-v2` / `wbs-schedule`는 리다이렉트(정본은 `wbs.md`).

---

## 3. 앱 가이드 (코딩할 때)

> **AI 도구 사용:** [AI 스킬 및 코드 그래프 사용 가이드](guides/12-ai-agent-tools-guide.md)에서 Codex·Claude·Cursor·Antigravity의 스킬과 코드 그래프를 확인한다. 바로 복사해 쓸 요청문은 [AI 스킬 명령어 예시](guides/13-ai-skill-prompt-examples.md)에 있다.

| #   | 문서                                                                                                         | 한 줄                        |
| --- | ------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| 6   | [Kiosk 구조](../../ASAK-Kiosk/src/STRUCTURE_GUIDE.md) · [구현 계획](../../ASAK-Kiosk/IMPLEMENTATION_PLAN.md) | 키오스크 WBS-023~038         |
| 7   | [Admin 구조](../../ASAK-Admin/src/STRUCTURE_GUIDE.md) · [Mock 사전](../../ASAK-Admin/public/mocks/README.md) | 관리자 WBS-039~051           |
| 8   | [Backend 구현 계획](../../ASAK-back/IMPLEMENTATION_PLAN.md)                                                  | 백엔드 WBS-052~066           |
| 9   | [앱 구현 허브](planning/app-implementation-hub.md)                                                           | Bible / guide / PLAN 역할 표 |

워크스페이스에서 UI 찾을 때: 루트 [`ui-index.md`](../../ui-index.md).

---

## 4. 계약 (정본)

| #   | 문서                                                                                  | 한 줄                                 |
| --- | ------------------------------------------------------------------------------------- | ------------------------------------- |
| 10  | [정본 계약 Decisions](governance/정본-contract-decisions-2026-07-16.md) | API 경로·필드 결정 (코드 미반영 가능) |

충돌 시: **실행 코드 > baseline/맵 > 정본(목표) > Product Bible**.

---

## 5. Product Bible (팩 README만)

| #   | 문서                                                     | 한 줄                             |
| --- | -------------------------------------------------------- | --------------------------------- |
| 10  | [Product Bible 허브](product_bible/product-bible-hub.md) | **역할별 한 페이지** · MVP 15링크 |
| 11  | [Product Bible Pack README](product_bible/README.md)     | Pack별 전체 목록                  |

세부 계약 문서는 **팩 README를 연 뒤** 필요한 파일만 읽으세요. `_archive`는 구현 기준 아님.

---

## 6. 한물간 / 참고만

| #   | 문서                                                                            | 한 줄                                         |
| --- | ------------------------------------------------------------------------------- | --------------------------------------------- |
| 12  | [Archive](_archive/)                                                            | 실행 금지 · 이력 보존                         |
| 13  | [Legacy & Reference Index](governance/legacy-and-reference-index-2026-07-16.md) | 비정본 분류                                   |
| 14  | [문서 이름 규칙](document-naming-guide-2026-07-20.md)                           | **파일명 문법** · 폴더별 패턴 · 검사 스크립트 |
| 15  | [문서 태그 인덱스](document-tag-index-2026-07-20.md)                            | KEEP / `#current` · `#archive`                |
| 16  | [design 실행 스택](design/README.md)                                            | Figma QA·CORRECTIVE 계획                      |
| 17  | [문서 인벤토리(슬림)](document-inventory-slim-2026-07-20.md)                    | KEEP / archive 후보                           |

---

## 매일 볼 문서 5개

1. [구현 맵](planning/current-implementation-map-2026-07-16.md)
2. [wbs.md](wiki/wbs.md)
3. [wbs-status-notes](wiki/wbs-status-notes.md)
4. 담당 앱 `STRUCTURE_GUIDE` / Mock 사전 (Admin `IMPLEMENTATION_PLAN`은 삭제됨)
5. [정본](governance/정본-contract-decisions-2026-07-16.md) (계약 건드릴 때)

더 넓은 색인: [docs/README](README.md) · [wiki/index](wiki/index.md) · [PROJECT_HUB](../PROJECT_HUB.md)
