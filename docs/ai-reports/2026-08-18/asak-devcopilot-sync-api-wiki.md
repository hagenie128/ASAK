# ASAK DevCopilot 동기화 — API·Wiki (2026-08-18)

- 작업공간: **workspace 2**
- Wiki: **MCP 미지원 → REST fallback** (`asak-data/scripts/upload_wiki.py`)
- API: MCP `get_api_specs` / `update_api_spec` / `create_api_spec`
- Git commit/push: **미수행**
- 토큰·자격 증명은 본 문서에 기록하지 않음

## 조회 범위

| 종류 | 조회 | 판정 |
|---|---|---|
| API | `get_api_specs` 1회. page 파라미터 없음. 재조회 **28건** | 동기화 (기존 22 갱신 + 코드에만 있던 6건 생성) |
| Wiki | REST `GET /api/workspaces/2/wikis` **20건** 전체 | 기존 제목 8건 upsert. 신규 생성 없음 |
| 요구사항 | 미갱신 | 사람 결정 필요 (상태 추정 금지) |
| WBS 카드 | 미갱신 | 로컬 `wbs.md`만 wiki/81 본문 반영. Hub WBS 작업 카드 DONE 상향 없음 |
| 시나리오·QA·화면·DB | 미갱신 | MCP 관계/ERD 덮어쓰기 금지 |

전수 8종 상태 변경은 **완료하지 않음**. API·Wiki 문서 반영만 수행.

## API — 기존 ID 갱신 (변경 후 재조회 일치)

기존 22건 description을 2026-08-18 코드 기준으로 맞춤. 구현 완료로 올리지 않은 스텁: 77, 212, 68, 81, 82, 213, 214, 84.

주요 필드 변경:

| api_id | 제목 | 변경 요지 |
|---|---|---|
| 261 | API-001 | `categoryName` (구 Hub `name` 폐기) |
| 78 | API-011 | query page/size/sort/tagId, `ADMIN_MENU_LIST_SUCCESS` |
| 69 | API-023 | 상세 DTO + optionGroups 요약 |
| 79 / 76 | API-012 / 013 | `CreateMenuRequest`, 성공 코드 |
| 74 | API-007 | query 8개. 구 `status=APPROVED` 폐기 |
| 212 | API-009 | 스텁. body `changes[]` |
| 81 | API-016 | 스텁. TODO `isActive` (구 `isEnabled`와 결정 필요) |
| 211 | API-006 | 서버 구현. 클라이언트 `/payments` 불일치. approvePayment 미호출 |
| 80 | API-014 | JSON 키 `active`. PaymentPage 연결 |
| 214 | API-019 | 월별 매출 스텁. 영수증 출력 아님 |

## API — 신규 생성 (코드 path 근거, 제목 추정 번호 없음)

| api_id | method | endpoint |
|---|---|---|
| 430 | GET | `/api/health` |
| 431 | GET | `/api/admin/menus/categories` |
| 432 | GET | `/api/admin/menus/ingredients` |
| 433 | DELETE | `/api/admin/menus/{menuId}` |
| 434 | GET | `/api/admin/opts/groups` |
| 435 | GET | `/api/admin/opts/{optionGroupId}` |

재조회에서 430~435와 기존 카드가 함께 반환됨 (총 28).

로그인 `POST /api/admin/login`은 Controller 스텁이라 **생성하지 않음**.

## Wiki REST upsert (기존 제목 정확 일치)

| id | 원격 제목 (유지) | 로컬 파일 | URL |
|---|---|---|---|
| 12 | ASAK REST API 명세서 | `docs/wiki/rest-api-spec.md` | https://devcopilot.ai.kr/workspace/2/wiki/12 |
| 15 | ASAK 회의록 및 최종 배포 검증 | `docs/wiki/meeting-deliverables-checklist.md` | https://devcopilot.ai.kr/workspace/2/wiki/15 |
| 23 | ASAK 현재 운영 기준 · 최신 | `docs/wiki/current-status-baseline.md` | https://devcopilot.ai.kr/workspace/2/wiki/23 |
| 78 | ASAK 주차별 회의록 (2026-07~08) | `docs/wiki/meeting-minutes-weekly.md` | https://devcopilot.ai.kr/workspace/2/wiki/78 |
| 79 | ASAK 전체 흐름도 (Mermaid) | `docs/wiki/project-flow.md` | https://devcopilot.ai.kr/workspace/2/wiki/79 |
| 81 | ASAK WBS 상태·일정 (2026-08-07) | `docs/wiki/wbs.md` | https://devcopilot.ai.kr/workspace/2/wiki/81 |
| 82 | ASAK WBS 상태 메모 | `docs/wiki/wbs-status-notes.md` | https://devcopilot.ai.kr/workspace/2/wiki/82 |
| 83 | ASAK 워크로그 인덱스 (daily · entries · weekly) | `docs/wiki/worklog-index.md` | https://devcopilot.ai.kr/workspace/2/wiki/83 |

PUT 응답으로 `updated`·동일 id 확인. wiki/81 원격 제목 날짜는 기존값 유지(신규 제목 생성 방지).

업로드하지 않은 Wiki (HISTORY Notion export 또는 매핑 불명확): 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 24, 25.

## MCP 미지원

| 범위 | 판정 | 대안 |
|---|---|---|
| Wiki | MCP 도구 없음 | REST fallback |
| WBS Evidence / 항목 간 관계 | 미지원 | 로컬 `wbs.md` 정본 유지 |
| GET wiki/{id} | 이 세션에서 405 | 목록+PUT 응답으로 검증 |

## 보류

- Hub 요구/WBS/QA/화면/DB 카드 상태 상향
- 소스코드 수정 (결제 path 불일치는 문서만 기록)
- 자동 Git 작업 없음
