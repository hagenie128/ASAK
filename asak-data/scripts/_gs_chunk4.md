## 3단계: Notion에 한 줄 올리기

### 방법 A — 마크다운 파일에서 동기화 (추천)

```powershell
cd C:\ASAK
python worklog/scripts/sync_daily_to_notion.py --date today --dry-run
# 내용 확인 후:
python worklog/scripts/sync_daily_to_notion.py --date today
```

또는:

```powershell
.\worklog\scripts\sync_today.ps1
```

### 방법 B — 스크립트로 바로 한 줄 올리기

마크다운 파일 없이 Notion에 **딱 한 줄**만 빠르게 올릴 때:

```powershell
cd C:\ASAK
python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "SCR-003 옵션 UI"
```

옵션 예시:

```powershell
python asak-data/scripts/create_worklog.py --date 2026-07-06 --author 김나연 --task "API 골격" --ref WBS-002 --hours 2 --notes "스모크 통과"
python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "테스트" --dry-run
```

<table header-row="true">
<tr>
<td>옵션</td>
<td>의미</td>
</tr>
<tr>
<td>`--date today`</td>
<td>오늘 날짜 (또는 `2026-07-06`)</td>
</tr>
<tr>
<td>`--author`</td>
<td>담당자 실명: `이하진` · `김나연` · `박유진` · `강민준`</td>
</tr>
<tr>
<td>`--task`</td>
<td>작업 한 줄 요약</td>
</tr>
<tr>
<td>`--ref`</td>
<td>WBS/SCR 참조 (예: `WBS-002`)</td>
</tr>
<tr>
<td>`--hours`</td>
<td>투입 시간</td>
</tr>
<tr>
<td>`--notes`</td>
<td>추가 메모</td>
</tr>
<tr>
<td>`--blocker`</td>
<td>블로커 있음 체크</td>
</tr>
<tr>
<td>`--dry-run`</td>
<td>API 호출 없이 미리보기만</td>
</tr>
</table>

### ✅ `create_worklog.py` 성공 예

```json
{
  "action": "created",
  "page_id": "...",
  "url": "https://www.notion.so/...",
  "title": "2026-07-06 이하진 일일",
  "담당": "이하진",
  "날짜": "2026-07-06"
}
```

터미널에 `created: https://www.notion.so/...` 가 나오면 성공이에요!  
Notion [📅 일일 워크로그](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9) 캘린더에서 오늘 날짜를 확인해 보세요.

### ❌ `create_worklog.py` 실패 예

```text
NOTION_TOKEN not set. Set env var or see docs/GETTING_STARTED.md#part-2--워크로그-쓰기-유치원-선생님-모드
```

→ 0단계 토큰 설정 후 다시 실행하세요.

```text
담당 '홍길동' 는 DB select 옵션에 없습니다. 허용: 강민준, 김나연, 미지정, 박유진, 이하진
```

→ `--author`에 팀원 **실명**을 정확히 쓰세요.

---

## 4단계: 중복 행 주의하기 (중요!)

같은 날짜 + 같은 담당자로 **두 번** 올리면 Notion에 줄이 겹쳐 보일 수 있어요.

<table header-row="true">
<tr>
<td>상황</td>
<td>어떻게 되나요?</td>
</tr>
<tr>
<td>`create_worklog.py`를 같은 날 두 번</td>
<td>**업데이트**됩니다 (새 줄이 아니라 기존 줄 수정)</td>
</tr>
<tr>
<td>`sync` + `create_worklog` 둘 다 쓰면서 내용이 다름</td>
<td>헷갈릴 수 있음 → **하나의 방법**만 쓰는 걸 추천</td>
</tr>
<tr>
<td>예전에 실수로 중복 생성됨</td>
<td>정리 스크립트 실행 (아래)</td>
</tr>
</table>

중복·빈 행 정리:

```powershell
cd C:\ASAK
python worklog/scripts/archive_duplicate_worklogs.py --dry-run
# 확인 후:
python worklog/scripts/archive_duplicate_worklogs.py
```

> `--dry-run`으로 먼저 **뭐가 지워질지** 확인하고, 괜찮으면 `--dry-run` 없이 실행하세요.

---

## 토큰 없이도 할 수 있어요

`NOTION_TOKEN`이 없으면 Git에만 남기고, JSON을 팀 관리자에게 전달할 수 있어요:

```powershell
python worklog/scripts/sync_daily_to_notion.py --date today --json > _sync.json
```

또는 Notion 웹에서 [일일 워크로그 DB](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9)에 직접 입력하세요.