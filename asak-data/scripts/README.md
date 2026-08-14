# asak-data/scripts

> Status: **CURRENT**

## 유지 경로 (스크립트 계약)

| 경로 | 역할 |
|---|---|
| 이미지 | 다운로드·원본 반영·트림·재료 자산 생성 |
| Wiki/Figma | 화면 export·링크 동기화·Wiki 생성/업로드 |
| 데이터 | SQLite seed 로드·매출 View 생성 |
| 인증 | Notion 토큰 확인 |
| `notion_raw/` | Notion fetch 원본 JSON (다수 스크립트가 기록) |
| `output/` | 일회성 리포트 JSON |
| `*_report.json` 등 | 실행 산출 스냅샷 |

일회성 MCP 저장기, DB 보정, 데이터 migration, 과거 DevCopilot 배치 Python은 2026-08-14에 제거했습니다. 필요하면 Git 이력에서 복원합니다.
