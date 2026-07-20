# Docs · Worklog · GitHub Issue · WBS2 교차 중복 Matrix

> Audit Date: 2026-07-16
> GitHub read-only audit: `hagenie128/ASAK`, `ASAK-Kiosk`, `ASAK-Admin`, `ASAK-back`에서 connector가 반환한 Open/Closed Issue는 각각 0건이다. 이 결과는 Issue가 없다는 뜻이며 Issue 수정·Close·라벨 변경은 수행하지 않았다.

| Topic | Canonical Doc | Worklog Entry | GitHub Issue | WBS2 | Duplicate Type | Recommended Action |
| --- | --- | --- | --- | --- | --- | --- |
| 메뉴별 최대 수량·주문 정책 | `docs/product_bible/02_Order_Cart_Payment/` | 구현 일자의 `worklog/daily/` 증거 | 없음 | `docs/wiki/wbs-v2-2026-07-16.md` 해당 작업 | SAME_POLICY | 정책을 Issue/Worklog에 복제하지 않고 Product Bible 링크만 사용 |
| 현재 구현 현황·추적성 | `docs/wiki/current-status-baseline.md`, `traceability-matrix.md` | 완료 시점 증거 | 없음 | `docs/wiki/wbs-v2-2026-07-16.md` | RELATED_NOT_DUPLICATE | Wiki는 현황, WBS2는 일정·담당, Worklog는 증거로 유지 |
| DevCopilot 동기화 | `docs/wiki/devcopilot-sync-report.md` | `worklog/daily/_team/2026-07-06.md` | 없음 | `docs/wiki/wbs-v2-2026-07-16.md` | SAME_EVIDENCE | Worklog는 Archive 링크로 보존하고 Wiki를 현재 상태 정본으로 유지 |
| Figma/SCR 병합 | `docs/product_bible/07_Screen_Bible/` | 2026-07-06 팀 기록 | 없음 | 해당 Screen 정비 항목 | SUPERSEDED_PLAN | 완료된 회의·프롬프트는 Archive, 현재 Screen Registry만 정본 |
| 배포 준비 | `docs/wiki/wbs-v2-2026-07-16.md` WBS2-065 | 해당 시점의 배포 증거 | 없음 | WBS2-065 | RELATED_NOT_DUPLICATE | 환경·release owner·RC가 확정될 때까지 BLOCKED 유지 |
| 발표/Demo 준비 | `docs/wiki/wbs-v2-2026-07-16.md` WBS2-066 | 리허설·발표 증거 | 없음 | WBS2-066 | NEEDS_CONFIRMATION | Primary Owner 확정 전에는 Team/NEEDS_CONFIRMATION 유지 |
| 과거 Notion Export | Product Bible 및 Wiki | 과거 worklog evidence | 없음 | 없음 | HISTORY_ONLY | `docs/_archive/notion-export/` 보존, 정책 정본으로 사용하지 않음 |

## Worklog 분류

- `worklog/daily/`, `worklog/entries/`: CURRENT_EVIDENCE — 현 동기화·캘린더 경로를 유지한다.
- 날짜가 지난 기록: COMPLETED_HISTORY 성격이지만 자동 경로가 직접 읽으므로 별도 `archive/` 이동은 Source Code 변경 승인 후 수행한다.
- `worklog/archive/*`: 새로 생성한 향후 이관 대상 구조이며 현재 파일은 없다.
- 의미상 중복 그룹: 0건 확정. 같은 주제의 Worklog와 WBS2는 증거/일정 역할이 다르므로 삭제 대상이 아니다.

## .github 감사

| Path | Classification | Result |
| --- | --- | --- |
| `.github/ISSUE_TEMPLATE/bug.yml` | ISSUE_FORM | ASAK-front 선택지를 ASAK-Kiosk/ASAK-Admin/ASAK-back/ASAK로 갱신 |
| `.github/ISSUE_TEMPLATE/task.yml` | ISSUE_FORM | 동일하게 현재 저장소 목록으로 갱신 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PULL_REQUEST_TEMPLATE | PR 필수 검토 항목을 보강 |
| `.github/workflows/pages.yml` | WORKFLOW | 실행 영향 가능성이 있어 변경하지 않음 |
| `.github/ISSUE_TEMPLATE/config.yml` | LABEL_CONFIG | 현재 설정으로 유지 |

Kiosk canonical remote는 아직 **NEEDS_CONFIRMATION**이다. ASAK-front remote 변경·Issue 이전·Workflow 비활성화는 수행하지 않았다.
