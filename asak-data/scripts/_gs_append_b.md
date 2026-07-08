## 워크로그가 뭐예요? 왜 써요?

<table header-row="true">
<tr>
<td>질문</td>
<td>답</td>
</tr>
<tr>
<td>**뭐예요?**</td>
<td>하루에 한 줄 요약 + (선택) 조금 더 자세한 메모</td>
</tr>
<tr>
<td>**어디에 남겨요?**</td>
<td>Git `worklog/daily/{이름}/` + Notion [📅 일일 워크로그](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9) 캘린더</td>
</tr>
<tr>
<td>**왜 써요?**</td>
<td>팀이 서로 뭘 하고 있는지 알 수 있고, 나중에 포트폴리오·회고에 쓸 수 있어요</td>
</tr>
</table>

**정본(상세 설명):** Notion [📅 일일 워크로그 — 팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95)

---

## 언제 쓰면 되나요?

- **매일 퇴근 전** (또는 하루 작업 끝난 뒤)
- Git에 커밋·푸시한 뒤, Notion에 올리기 전에
- "오늘 한 일"이 생겼을 때 — 아무것도 안 했으면 **블로커**만 적어도 OK

---

## 0단계: NOTION_TOKEN 준비하기

Notion에 자동으로 올리려면 **비밀 열쇠(토큰)** 가 필요해요.  
팀 리더에게 Integration 토큰을 받으세요. (토큰은 채팅·Git에 올리지 마세요!)

PowerShell에서 **이 창에서만** 설정:

```powershell
$env:NOTION_TOKEN = "secret_여기에_받은_토큰"
```

> PowerShell 창을 닫으면 토큰이 사라져요. 매번 새 창을 열 때마다 다시 설정하거나, 팀 가이드의 영구 설정 방법을 참고하세요.

---

## 1단계: 토큰이 잘 됐는지 확인하기

```powershell
cd C:\ASAK
python asak-data/scripts/verify_notion_token.py
```

### ✅ 성공하면 이렇게 나와요

```text
OK: Integration 연결됨 — bot/user: (이름)
OK: 워크로그 DB 접근 — 📅 일일 워크로그
OK: DB query 성공 (샘플 1건 조회)

다음 단계:
  python worklog/scripts/sync_daily_to_notion.py --date today --dry-run
  python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "테스트" --dry-run
```

### ❌ 실패하면

<table header-row="true">
<tr>
<td>메시지</td>
<td>해결</td>
</tr>
<tr>
<td>`NOTION_TOKEN 환경 변수가 설정되지 않았습니다`</td>
<td>위 0단계 `$env:NOTION_TOKEN = "..."` 다시 실행</td>
</tr>
<tr>
<td>`Notion API ... failed (401)`</td>
<td>토큰이 틀렸거나 만료됨 → 팀 리더에게 새 토큰 요청</td>
</tr>
<tr>
<td>`Notion API ... failed (404)`</td>
<td>Integration이 워크로그 DB에 연결 안 됨 → Notion [팀 가이드 §3~§5](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95) 참고</td>
</tr>
</table>

---

## 2단계: 오늘 일기 파일 만들기 (Git)

```powershell
cd C:\ASAK
python worklog/scripts/init_daily.py
# → worklog/daily/{본인}/YYYY-MM-DD.md 생성
```

다른 팀원 파일을 만들 때:

```powershell
python worklog/scripts/init_daily.py --person 김나연
```

파일을 열어 **오늘 요약** 표에 한 줄 적어요:

<table header-row="true">
<tr>
<td>담당자</td>
<td>저장소</td>
<td>작업</td>
<td>WBS / Issue</td>
<td>상태</td>
<td>블로커</td>
</tr>
<tr>
<td>이하진</td>
<td>ASAK-front</td>
<td>SCR-003 메뉴 옵션 UI</td>
<td>WBS-012 / #12</td>
<td>✅ 완료</td>
<td>-</td>
</tr>
</table>## 3단계: Notion에 한 줄 올리기

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

또는 Notion 웹에서 [일일 워크로그 DB](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9)에 직접 입력하세요.## 자주 쓰는 명령 모음

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