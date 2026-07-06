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
</table>