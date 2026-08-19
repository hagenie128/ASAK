# ASAK 문서 동기화 — DevCopilot Hub API 번호 (2026-08-19)

- 범위: DevCopilot workspace 2의 기존 API 카드 제목과 로컬 API 정본 번호 정렬
- 소스코드·DB·Figma·Git 작업: 수정하지 않음
- 인증 정보: 기록하지 않음

## 근거

- 로컬 정본: `docs/wiki/rest-api-spec.md`
- 원격 확인: DevCopilot MCP `get_api_specs(workspace_id=2)`
- 원격 변경: 기존 API 카드만 `update_api_spec`으로 제목 갱신 후 재조회

## 반영 결과

| 원격 API 카드 ID | endpoint | 제목 API 번호 |
|---|---|---|
| 430 | `GET /api/health` | `API-025` |
| 431 | `GET /api/admin/menus/categories` | `API-026` |
| 432 | `GET /api/admin/menus/ingredients` | `API-027` |
| 433 | `DELETE /api/admin/menus/{menuId}` | `API-028` |
| 434 | `GET /api/admin/opts/groups` | `API-029` |
| 435 | `GET /api/admin/opts/{optionGroupId}` | `API-030` |

## 확인 결과

- `API-001~024` 제목을 가진 기존 카드 24개는 변경하지 않았다.
- 위 6개 카드는 재조회로 `API-025~030` 제목 반영을 확인했다.
- `POST /api/admin/login`, 환불, 영수증은 정본 API 번호가 아직 없어 새 카드를 만들거나 번호를 임의로 부여하지 않았다.

## 로컬 문서 반영

- `docs/wiki/rest-api-spec.md`: 기존 Hub 내부 ID `430~435`를 `API-025~030`으로 표기
- `docs/planning/admin-todo-checklist-2026-08-05.md`: 메뉴 삭제를 `API-028`로 표기
- `docs/wiki/wbs.md`: 메뉴 삭제를 `API-028`로 표기

## 남은 결정 필요

- RTOS receipt-print endpoint의 경로·method·request/response·API 번호
- 관리자 로그인, 환불, 영수증의 정본 API 계약과 번호
