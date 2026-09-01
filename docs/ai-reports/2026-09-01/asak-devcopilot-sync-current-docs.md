# ASAK DevCopilot 현재 문서 동기화 — 2026-09-01

## 범위와 수단

- 대상: DevCopilot workspace 2의 기존 Wiki
- 수단: MCP 미지원에 따른 REST fallback
- 원칙: 로컬 `docs/wiki` 정본과 1:1로 확인된 기존 Wiki ID만 갱신했고, 신규 생성·삭제·WBS 카드 상태 일괄 변경은 하지 않았다.

## 반영 및 재조회 확인

| Wiki ID | 원격 제목 | 로컬 정본 | 판정 |
| --- | --- | --- | --- |
| 23 | ASAK 현재 운영 기준 · 최신 | `current-status-baseline.md` | 동기화·본문 일치 확인 |
| 9 | ASAK 요구사항 정의서 | `requirements-definition.md` | 동기화·본문 일치 확인 |
| 10 | ASAK 사용자 시나리오 명세 | `user-scenarios.md` | 동기화·본문 일치 확인 |
| 12 | ASAK REST API 명세서 | `rest-api-spec.md` | 동기화·본문 일치 확인 |
| 14 | ASAK QA 테스트 케이스 | `qa-test-cases.md` | 동기화·본문 일치 확인 |
| 15 | ASAK 회의록 및 최종 배포 검증 | `meeting-deliverables-checklist.md` | 동기화·본문 일치 확인 |
| 78 | ASAK 주차별 회의록 (2026-07~08) | `meeting-minutes-weekly.md` | 동기화·본문 일치 확인 |
| 79 | ASAK 전체 흐름도 (Mermaid) | `project-flow.md` | 동기화·본문 일치 확인 |
| 81 | ASAK WBS 상태·일정 (2026-08-07) | `wbs.md` | 동기화·본문 일치 확인 |
| 82 | ASAK WBS 상태 메모 | `wbs-status-notes.md` | 동기화·본문 일치 확인 |
| 83 | ASAK 워크로그 인덱스 | `worklog-index.md` | 동기화·본문 일치 확인 |

## 보류

| 범위 | 판정 | 이유 |
| --- | --- | --- |
| Wiki 5 화면 설계/Figma | 보류 | 기존 로컬 내보내기는 원격보다 짧아 덮어쓰기 위험이 있고, 최신 Figma·브라우저 검증이 필요하다. |
| Wiki 11 DB 설계 | 보류 | 운영 DB/View와 초기 설계 문서의 차이를 실DB 기준으로 다시 확인해야 한다. |
| Wiki 13 WBS 및 일정 계획 | 보류 | Wiki 81이 현재 WBS 정본으로 확인됐으며, 중복 계획 페이지를 같은 본문으로 덮어쓰지 않았다. |
| Wiki 6 종합 기획서 | 보류 | Notion에서 최신 종강 MVP 블록을 관리 중이며, 로컬 1:1 정본 매핑을 확정하지 않았다. |
| 요구사항·WBS·QA·화면·DB 관계 및 개별 WBS 카드 | MCP 미지원/사람 결정 필요 | 관계 변경과 Evidence 필드의 안전한 REST 계약을 확인하지 못했다. |

## 보안 및 Git

- 인증 토큰은 실행 중 환경변수로만 사용하고 파일·보고서·Git에 기록하지 않았다.
- 소스코드, DB, 원격 Git, commit, push, merge는 수행하지 않았다.
