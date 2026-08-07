# Hub WBS 정리 (REST 삭제, 2026-08-07)

- 수단: Hub REST `DELETE /api/workspaces/2/tasks/{id}` (MCP 아님)
- 삭제 기준: `status=EXCLUDED` **또는** 제목에 `[ARCHIVED DUPLICATE]`
- 유지: 실행용 `WBS2-*` (비-EXCLUDED)

## 결과

| 항목 | 값 |
|---|---|
| 삭제 성공 | **97** |
| 삭제 실패 | 0 |
| 정리 전 | 169건 (EXCLUDED 97 포함) |
| 정리 후 | **72건** |
| 남은 ARCHIVED | **0** |
| 남은 EXCLUDED | **0** |
| WBS2 행 | **66** |

## 정리 후 상태 분포

- IN_PROGRESS 37
- DONE 14
- TODO 14
- BLOCKED 5
- DELAYED 1
- IN_REVIEW 1

칸반에 다시 보이려면 검색을 비우고 새로고침하면 됩니다.
