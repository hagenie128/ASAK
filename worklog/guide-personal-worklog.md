# 개인별 일일 워크로그 (Git stub)

> **처음이면:** Notion [🚀 ASAK 처음 시작하기 — Part 2](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b) · Git [`docs/operations/setup/GETTING_STARTED.md`](../docs/operations/setup/GETTING_STARTED.md#part-2--워크로그-쓰기-유치원-선생님-모드)
> **상세 정본:** Notion [📅 일일 워크로그 — 팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95) · [`guide-team-daily.md`](guide-team-daily.md) · [`worklog/README.md`](README.md)

## 매일 (본인)

```powershell
cd C:\ASAK
python worklog/scripts/init_daily.py
.\worklog\scripts\sync_today.ps1
```

| 목적 | 명령 |
|---|---|
| 오늘 파일 | `python worklog/scripts/init_daily.py` |
| Notion 업로드 | `.\worklog\scripts\sync_today.ps1` |
| 토큰 검증 | `python asak-data/scripts/verify_notion_token.py` |

`team_config.json`의 `git_user_map`에 본인 GitHub ID를 등록하면 `--person` 없이 동작합니다.
