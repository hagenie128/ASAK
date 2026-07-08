## 자주 쓰는 명령 모음

<table header-row="true">
<tr>
<td>목적</td>
<td>명령</td>
</tr>
<tr>
<td>토큰 검증</td>
<td>`python asak-data/scripts/verify_notion_token.py`</td>
</tr>
<tr>
<td>오늘 파일 생성</td>
<td>`python worklog/scripts/init_daily.py`</td>
</tr>
<tr>
<td>Notion 동기화 (미리보기)</td>
<td>`python worklog/scripts/sync_daily_to_notion.py --date today --dry-run`</td>
</tr>
<tr>
<td>Notion 동기화 (실제)</td>
<td>`python worklog/scripts/sync_daily_to_notion.py --date today`</td>
</tr>
<tr>
<td>한 줄 바로 올리기</td>
<td>`python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "작업 요약"`</td>
</tr>
<tr>
<td>전원 동기화</td>
<td>`python worklog/scripts/sync_daily_to_notion.py --date today --all`</td>
</tr>
<tr>
<td>중복 정리</td>
<td>`python worklog/scripts/archive_duplicate_worklogs.py --dry-run`</td>
</tr>
</table>

---

## 더 읽을 문서

<table header-row="true">
<tr>
<td>문서</td>
<td>내용</td>
</tr>
<tr>
<td>[worklog/guide-team-daily.md](https://github.com/hagenie128/ASAK/blob/main/worklog/guide-team-daily.md)</td>
<td>팀 일일 워크로그 상세</td>
</tr>
<tr>
<td>[worklog/guide-personal-worklog.md](https://github.com/hagenie128/ASAK/blob/main/worklog/guide-personal-worklog.md)</td>
<td>개인별 명령 요약</td>
</tr>
<tr>
<td>[worklog/README.md](https://github.com/hagenie128/ASAK/blob/main/worklog/README.md)</td>
<td>폴더 구조·확인 순서</td>
</tr>
<tr>
<td>[Notion 팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95)</td>
<td>토큰·DB 스키마 정본</td>
</tr>
</table>

---

## 다음에 할 일

1. [guides/README.md](https://github.com/hagenie128/ASAK/blob/main/docs/guides/README.md) 순서대로 01~02 읽기  
2. Notion [문서 읽는 순서](https://app.notion.com/p/39451ef04f0b81088a91d914f985fb11) 확인  
3. `develop` 브랜치에서 `feature/...` 로 작업 시작  
4. **매일 퇴근 전** 워크로그 한 줄 ✍️

화이팅! 🥗