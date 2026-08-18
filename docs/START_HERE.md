# ASAK 문서 — 여기부터 시작

> 초보자용 **단일 진입점** (2026-08-18 갱신).
> 문서가 많아도 **아래 링크만** 따라가면 됩니다. 세부 바이블은 필요한 Pack만 엽니다.

---

## 1. 지금 상태 (코드 현실)

| #   | 문서                                                                 | 한 줄                                                                         |
| --- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | [구현 맵](planning/current-implementation-map-2026-07-16.md)         | **화면별 상세** — 화면·가상 데이터·API 상태표                                 |
| 2   | [구현 현황 요약](wiki/current-status-baseline.md)                    | **영역별 요약** — 키오스크·관리자·백엔드를 한눈에 확인                         |
| 3   | [WBS 상태 메모](wiki/wbs-status-notes.md)                            | 코드↔WBS 요약 · DevCopilot 한글 제목                                          |
| 4   | [문서–코드 차이](architecture/document-code-gap-report-2026-07-16.md) | 정본과 코드의 충돌                                                            |
| 5   | [백엔드·DB 중간점검](wiki/backend-db-midpoint-audit-2026-07-28.md)   | 실제 원격·Spring 맥락·실제 DB·조회 API 점검 결과                              |
| 6   | [주차별 회의록](operations/meeting-minutes/README.md)                | 2조 공식 회의록 · [Hub wiki/78](https://devcopilot.ai.kr/workspace/2/wiki/78) |

**한 줄 요약 (2026-08-18):** 남은 일정은 선생님이 다시 못 박았다. **08/17~08/21 RTOS 연동(적어도 Spring Boot와 React)**, 08/24~08/28 기능 마감·테스트, 08/31~09/01 문서·PPT·리허설, **09/02 최종 시연**. 구현 완료 주장이 아니다. 작업 분해표 정본: **[wbs.md](wiki/wbs.md)**.

**이번 주 작업 순서 (선생님 2026-08-18):** ① `device_event` + 콘솔 출력 + Spring↔React 연동 → ② 키오스크 주문·결제 실연동 잔여 → ③ 관리자 주문·메뉴 잔여는 08/24 기능 마감 전에 이어서.

**남은 일정:** [wbs.md 남은 일정](wiki/wbs.md#남은-일정-선생님-2026-08-18) · 8/7 허브 재조정 기록은 [asak-wbs-date-rebase](ai-reports/2026-08-07/asak-wbs-date-rebase.md) (과거).

**그림으로 보기:** [전체 흐름도 (Mermaid)](wiki/project-flow.md) — 저장소 구조·키오스크 주문 흐름·관리자 운영 흐름·데이터/API 목표 흐름·가격·수량 흐름·이번 스프린트 WBS 흐름을 그림 6개로 정리.

---

## 2. 할 일 (WBS)

| #   | 문서                                      | 한 줄                                  |
| --- | ----------------------------------------- | -------------------------------------- |
| 5   | [WBS 통합본](wiki/wbs.md)                 | **정본** — `WBS-001`~`085` (기획→발표) |
| 6   | [WBS 상태 메모](wiki/wbs-status-notes.md) | 코드↔WBS 요약                          |

WBS 정본은 [`wiki/wbs.md`](wiki/wbs.md). 구 `wbs-v2` / `wbs-schedule` 스텁은 삭제했다.

---

## 3. 앱 가이드 (코딩할 때)

> AI 작업 절차는 설치된 ASAK 스킬을 직접 사용합니다. 중복 프롬프트 문서는 유지하지 않습니다.

| #   | 문서                                                                                                         | 한 줄                        |
| --- | ------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| 6   | [키오스크 구조](../../ASAK-Kiosk/src/STRUCTURE_GUIDE.md) · [구현 계획](../../ASAK-Kiosk/IMPLEMENTATION_PLAN.md) · [README PWA](../../ASAK-Kiosk/README.md#-pwa--키오스크-전체화면) | 키오스크 WBS-023~038 · PWA |
| 7   | [관리자 구조](../../ASAK-Admin/src/STRUCTURE_GUIDE.md) · [가상 데이터 사전](../../ASAK-Admin/public/mocks/README.md) · [README PWA](../../ASAK-Admin/README.md#-pwa--태블릿-전체화면) | 관리자 WBS-039~051 · PWA |
| 8   | [백엔드 구현 계획](../../ASAK-back/IMPLEMENTATION_PLAN.md)                                                  | 백엔드 WBS-052~066                 |
| 9   | [앱 구현 허브](planning/app-implementation-hub.md)                                                           | 기준 문서·가이드·계획의 역할 표    |
| 9a  | [Android PWA 전체화면](operations/setup/android-pwa-fullscreen.md)                                           | 키오스크·관리자 태블릿 설치·fullscreen |

워크스페이스에서 UI 찾을 때: 루트 [`ui-index.md`](../../ui-index.md).

---

## 4. 계약 (정본)

| #   | 문서                                                                                  | 한 줄                                 |
| --- | ------------------------------------------------------------------------------------- | ------------------------------------- |
| 10  | [정본 계약 결정](governance/canonical-contract-decisions-2026-07-16.md) | API 경로·필드 결정 (코드 미반영 가능) |

충돌 시: **실행 코드 > 구현 현황·맵 > 정본(목표) > 제품 기준 문서** 순으로 현재 구현 사실을 판단합니다.

---

## 5. 제품 기준 문서 (팩 안내문만)

| #   | 문서                                                     | 한 줄                             |
| --- | -------------------------------------------------------- | --------------------------------- |
| 10  | [제품 기준 문서 허브](product_bible/product-bible-hub.md) | **역할별 한 페이지** · 최소 기능 제품 15개 링크 |
| 11  | [제품 기준 문서 팩 안내](product_bible/README.md)          | 팩별 전체 목록                              |

세부 계약 문서는 **팩 README를 연 뒤** 필요한 통합 파일만 읽으세요.

---

## 6. 한물간 / 참고만

| #   | 문서                                                                            | 한 줄                                         |
| --- | ------------------------------------------------------------------------------- | --------------------------------------------- |
| 12  | Git history                                                                    | 삭제된 과거 이력 조회용 · 실행 기준 아님      |
| 13  | [문서 이름 규칙](document-naming-guide-2026-07-20.md)                           | 파일명 문법 · 폴더별 패턴                     |
| 14  | [문서 상태 라벨](document-tag-index-2026-07-20.md)                              | 5개 공통 라벨                                 |
| 15  | [디자인 참고](design/README.md)                                                 | Figma 링크·플러그인                           |

---

## 매일 볼 문서 5개

1. [구현 맵](planning/current-implementation-map-2026-07-16.md)
2. [wbs.md](wiki/wbs.md)
3. [wbs-status-notes](wiki/wbs-status-notes.md)
4. 담당 앱 `STRUCTURE_GUIDE` / Mock 사전 (Admin `IMPLEMENTATION_PLAN`은 삭제됨)
5. [정본 계약 결정](governance/canonical-contract-decisions-2026-07-16.md) (계약 건드릴 때)

더 넓은 색인: [docs/README](README.md) · [wiki/index](wiki/index.md) · [PROJECT_HUB](../PROJECT_HUB.md)
