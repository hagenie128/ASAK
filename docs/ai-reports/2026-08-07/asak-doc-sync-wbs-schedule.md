# ASAK 문서 동기화 — WBS 상태·일정 (2026-08-07)

## 대상 저장소·기준

- 저장소: `ASAK` (`hagenie128/ASAK`)
- 기준: Hub WBS 재조회 + 로컬 `wbs-v2` / `wbs-status-notes` (2026-08-07)
- 소스코드·DB·Figma·QA PASS: **미변경**

## 확인한 근거

- Hub MCP `get_wbs_tasks` — 활성 WBS2 종료일 < 8/7 = **0건** (rebase 후)
- Hub `update_wbs_task` — TODO/BLOCKED→IN_PROGRESS 6건(008·027·045·056·057·059), 일정 57건
- 로컬 Evidence: Admin 주문 API 구현·미검증, Pay/SoldOut 스텁, Kiosk 결제 실패 cart 유지 코드

## 갱신한 문서

| 문서 | 변경 |
|---|---|
| `docs/START_HERE.md` | 8/7 요약에 WBS 일정 rebase 한 줄·윈도우 표기 |
| `docs/wiki/current-status-baseline.md` | Hub 문서 행에 상태+일정 rebase 반영 |
| `docs/wiki/meeting-deliverables-checklist.md` | 8/7 스냅샷에 WBS 상태·일정 행 추가 |
| `docs/wiki/README.md` | wbs-status-notes Hub 연계 표기 |
| `docs/wiki/wbs-status-notes.md` | 작업중 반영·일정 rebase 동기화 기록 |
| `docs/wiki/wbs-v2-2026-07-16.md` | 008·027·037·045·056·057·059 상태 정합 |
| `docs/ai-reports/2026-08-07/asak-wbs-date-rebase.md` | rebase 보고서 |
| `docs/ai-reports/2026-08-07/wbs-date-rebase-plan.json` | 57건 계획 |

## 실행·검증

- Hub 재조회: 샘플 P0/P1/P2/QA 날짜 일치
- `git diff --check`: 커밋 전 실행

## 남은 불일치·결정 필요

- Hub `WBS2-018~020`은 원격 DONE인데 로컬 wbs-v2는 과거 IN_PROGRESS 잔여 가능 → **사람 확인**(이번 sync에서 DONE 승격 안 함)
- Notion MCP/토큰 미연결 시 Notion 페이지는 별도 조치 필요
- Product/Screen Bible 본문: 이번 범위 밖(WBS·운영 문서만)

## Notion

- 반영: [ASAK WBS 상태·일정 동기화 (2026-08-07)](https://www.notion.so/3b551ef04f0b814f913afedb7b353ad3)
- 부모: 프로젝트 허브 페이지 (`39151ef04f0b808f99f8ea068efb5790`)
- Hub: [wiki/81](https://devcopilot.ai.kr/workspace/2/wiki/81) · [wiki/82](https://devcopilot.ai.kr/workspace/2/wiki/82) · [wiki/15](https://devcopilot.ai.kr/workspace/2/wiki/15)

## 수정하지 않은 범위

- ASAK-Kiosk / Admin / back 소스
- QA PASS, 요구사항 DONE
- Figma, ERD 덮어쓰기
