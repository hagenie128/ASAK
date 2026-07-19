# Cursor 프롬프트 — 일일 워크로그 자동 작성·동기화

아래 블록을 Cursor 채팅에 붙여넣고, 오늘 작업 맥락(브랜치·이슈·PR)을 함께 전달하세요.

---

## 프롬프트 A: 오늘 daily 작성

```text
ASAK worklog 규칙에 맞춰 오늘 worklog/daily/{본인}/YYYY-MM-DD.md 를 채워줘.

요구사항:
1. 파일이 없으면 `python worklog/scripts/init_daily.py` 로 생성 (개인 폴더)
2. `## 오늘 요약` 표 — 담당자 | 저장소 | 작업 | WBS/Issue | 상태 | 블로커
3. `## 오늘 작업` — 미니 카드 + `entries/{본인}/YYYY-MM-DD-주제.md` 링크
4. 내가 오늘 한 작업·PR·이슈를 반영 (없으면 물어봐)
5. WBS ID, GitHub Issue (#번호), PR 링크를 작업 열에 포함

참고: worklog/guide-team-daily.md, worklog/templates/template-daily-auto.md
```

## 프롬프트 B: Notion 동기화

```text
방금 작성한 worklog/daily/{본인}/YYYY-MM-DD.md 를 Notion 일일 워크로그 DB에 올려줘.

순서:
1. `python worklog/scripts/sync_daily_to_notion.py --date today --dry-run`
2. NOTION_TOKEN 이 있으면 sync 실행 (기본: git user → 본인 파일)
3. 토큰 없으면 `--json` + Notion MCP upsert
```

## 프롬프트 C: 퇴근 전 5분 (올인원)

```text
퇴근 전 worklog 루틴:
1. init_daily.py (오늘 본인 파일 없으면 생성)
2. 오늘 커밋/PR/이슈 기준으로 daily md 채우기
3. sync_daily_to_notion.py --date today
4. Notion 캘린더 확인 방법 안내
```

## 프롬프트 D: 이번 주 weekly 작성

```text
ASAK worklog 규칙에 맞춰 이번 주 `worklog/weekly/YYYY-Www.md` 를 작성하거나 갱신해줘.

먼저 확인:
- worklog/weekly/README.md
- 이번 ISO 주차의 worklog/daily/{팀원}/YYYY-MM-DD.md
- 관련 entries/{팀원}/ 상세 기록
- 이번 주 커밋, PR, GitHub Issue, Figma 작업 기록

작성 규칙:
1. ISO 주차와 기간을 정확히 계산한다. 파일명은 `YYYY-Www.md` 형식이다.
2. 기존 weekly 파일이 있으면 유용한 내용은 유지하고, 실제 근거가 있는 내용만 추가·정리한다.
3. `## 이번 주 완료 / 진행 / 다음 주 계획` 표를 작성한다.
   - 담당자 | 날짜 | 완료 / 진행 업무 | 상태 | daily
   - 작업명에 Screen ID, WBS2 ID, GitHub Issue `#번호`, PR 링크를 함께 적는다.
4. `## 주요 블로커 / 리스크`에는 실제 미해결 이슈만 적고, 없으면 `현재 기록된 블로커 없음`으로 쓴다.
5. `## daily 링크 모음`에는 이번 주 실제 작성된 daily만 담당자별로 연결한다.
6. `## 포트폴리오용 요약`에는 entries 상세 기록을 바탕으로 결과·문제 해결·검증 중심으로 2~5줄 작성한다.
7. 누락 날짜는 커밋·PR·Issue·Figma·프로젝트 채팅 기록으로 확인 가능한 날만 daily 초안을 작성한다. 근거가 없으면 지어내지 말고 누락 목록과 필요한 정보를 질문한다.

참고:
- worklog/weekly/README.md
- worklog/README.md
- worklog/daily/
- worklog/entries/
```

## 프롬프트 E: GitHub Issue 정리·연결

```text
ASAK의 이번 작업을 GitHub Issue 기준으로 정리해줘.

먼저 확인:
- docs/guides/02-github-issues-guide.md
- 현재 저장소와 브랜치
- 기존 열린 Issue / PR / 최근 커밋
- WBS2 ID, 요구사항 ID, Screen ID, Figma 작업 기록
- worklog/daily/{본인}/ 및 entries/{본인}/ 기록

순서:
1. 기존 Issue와 PR을 먼저 확인해서 중복 이슈를 만들지 않는다.
2. 작업별로 아래 형식의 이슈 후보 표를 만든다.
   - 제목
   - 대상 저장소
   - WBS2 ID / 요구사항 ID / Screen ID
   - 유형: feature / bug / docs / data
   - 라벨: wbs + frontend 또는 backend + 유형 + week-N
   - 완료 조건
   - 연결할 PR / worklog 경로
3. 기존 이슈가 있으면 새로 만들지 말고 해당 `#번호`와 URL을 daily·weekly·entries에 연결할 위치를 제안한다.
4. 새 이슈가 필요하면 GitHub Issue 템플릿(task 또는 bug)에 맞춘 제목·본문·라벨 초안을 먼저 보여준다.
5. 내가 `이슈 생성 승인`이라고 말한 이슈만 실제 생성한다.
6. 생성 또는 확인된 Issue 번호는 daily의 `WBS / Issue` 열과 작업 카드 제목에 반영한다.
7. PR이 있으면 작업 열에 PR URL도 함께 넣는다.

주의:
- WBS 실행 ID는 `WBS2-*`를 우선 사용한다. 기존 `WBS-*`는 과거 기록일 수 있으므로 임의로 바꾸지 않는다.
- 저장소 이전, remote 변경, pull/reset/rebase, 파일 이동은 하지 않는다.
- 근거 없는 Issue, 완료 조건, 블로커는 만들지 않는다.
```

## 프롬프트 F: 주간 마감 올인원

```text
ASAK 주간 마감 루틴을 진행해줘.

1. 이번 주 daily 누락일을 커밋·PR·Issue·Figma·프로젝트 채팅 기록으로 확인한다.
2. 근거가 있는 누락 daily만 초안으로 채운다. 근거가 없으면 추측하지 말고 목록으로 보여준다.
3. daily의 WBS2 ID, GitHub Issue #번호, PR URL을 확인·보완한다.
4. 기존 GitHub Issue와 PR을 점검해 중복 없는 이슈 후보만 제안한다.
5. `이슈 생성 승인` 전에는 실제 Issue를 만들지 않는다.
6. weekly/YYYY-Www.md를 작성 또는 갱신한다.
7. Notion 일일 워크로그는 각 daily에 대해 먼저 dry-run으로 확인하고, 토큰 또는 MCP 권한이 있을 때만 동기화한다.
8. 마지막에 완료·진행·블로커·다음 주 계획·확인 필요한 항목을 짧게 보고한다.

참고:
- worklog/README.md
- worklog/weekly/README.md
- worklog/guide-team-daily.md
- docs/guides/02-github-issues-guide.md
```

## 수동 명령 (비-Cursor)

```powershell
cd C:\ASAK
python worklog/scripts/init_daily.py
# worklog/daily/{본인}/YYYY-MM-DD.md 편집 후
python worklog/scripts/sync_daily_to_notion.py --date today
```
