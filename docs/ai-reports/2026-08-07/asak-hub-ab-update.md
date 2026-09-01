# ASAK Hub A+B 업데이트 근거 (2026-08-07)

- 범위: Phase **A**(로컬 문서·Wiki) + **B**(계약 필드)
- Git commit/push: **미수행**
- 토큰·자격 증명은 본 문서에 기록하지 않음

## A. 로컬 문서

| 파일                                          | 변경                                                   |
| --------------------------------------------- | ------------------------------------------------------ |
| `docs/START_HERE.md`                          | 8/7 한 줄 요약·선생님 우선순위·회의록 링크             |
| `docs/wiki/current-status-baseline.md`        | 근거 표 8/7 실연동 기준                                |
| `docs/wiki/wbs-status-notes.md`               | 8/7 가속 메모 · DONE으로 올리지 말 것                  |
| `docs/wiki/project-flow.md`                   | 기준일 8/7 · 이번 주 순서                              |
| `docs/wiki/meeting-deliverables-checklist.md` | 8/7 스냅샷·계약 필드·Figma 동결                        |
| `docs/wiki/rest-api-spec.md`                  | `totalAmount`/`APPROVED`/`approvedAt`/`approvedAmount` |

## B. DevCopilot API (MCP update)

| api_id | 제목    | 변경                      |
| ------ | ------- | ------------------------- |
| 74     | API-007 | totalAmount · APPROVED    |
| 72     | API-022 | totalAmount · APPROVED    |
| 210    | API-005 | totalAmount · orderStatus |
| 213    | API-018 | DINE_IN → EAT_IN          |
| 82     | API-017 | DINE_IN → EAT_IN          |

(이미 8/6 반영분 유지: Live path, paymentMethods, soldOut body)

## Wiki REST (업로드 완료)

| 제목                          | 로컬 파일                         | URL                                          |
| ----------------------------- | --------------------------------- | -------------------------------------------- |
| ASAK REST API 명세서          | rest-api-spec.md                  | https://devcopilot.ai.kr/workspace/2/wiki/12 |
| ASAK 회의록 및 최종 배포 검증 | meeting-deliverables-checklist.md | https://devcopilot.ai.kr/workspace/2/wiki/15 |
| ASAK 전체 흐름도 (Mermaid)    | project-flow.md                   | https://devcopilot.ai.kr/workspace/2/wiki/79 |

## 하지 않은 것

- WBS/요구/QA DONE·PASS로 올리기
- DB ERD 덮어쓰기
- Product Bible 본문 대량 수정
- 소스코드 변경
