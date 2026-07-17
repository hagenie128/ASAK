> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: One-off generated report fragment.
> Canonical Replacement: None; regenerate only when required.
> Original Path: `asak-data/scripts/_gs_chunk2.md`

## 5단계 (선택): ASAK 간단 데이터 뷰어

크롤링 JSON만 빠르게 볼 때:

```powershell
cd c:\ASAK\frontend
```

데이터가 없으면 `data` 폴더에 JSON을 복사합니다.  
`data-pipeline\phase1\output\` 의 파일을 `frontend\data\` 로 복사하거나, 팀 배치 파일을 경로에 맞게 수정해 사용합니다.

```powershell
python run_viewer.py
```

**성공 확인:**

- 터미널: `뷰어 실행: http://127.0.0.1:8765/`
- 브라우저에 메뉴 데이터 뷰어가 열림

데이터가 없으면 "data 폴더 없음" 안내만 나옵니다. 그건 **실패가 아니라** JSON을 아직 안 넣은 상태입니다.

---

## 환경 변수 (비밀번호·토큰)

<table header-row="true">
<tr>
<td>변수</td>
<td>필요할 때</td>
<td>설정 예 (PowerShell, **이 창에서만**)</td>
</tr>
<tr>
<td>`NOTION_TOKEN`</td>
<td>일일 워크로그 Notion 동기화</td>
<td>`$env:NOTION_TOKEN = "secret_..."`</td>
</tr>
<tr>
<td>`FIGMA_TOKEN`</td>
<td>Figma 자동화 스크립트</td>
<td>`$env:FIGMA_TOKEN = "..."`</td>
</tr>
</table>

> 토큰은 **절대 Git에 커밋하지 마세요.** `.gitignore`에 `.env`가 포함되어 있습니다.

워크로그 토큰 설정·검증은 [Part 2](https://github.com/hagenie128/ASAK/blob/main/#part-2--워크로그-쓰기-유치원-선생님-모드)를 참고하세요.

---

## 주의사항 (꼭 읽기)

1. **`.env`는 Git에 올리지 마세요.** 토큰·비밀번호를 커밋하면 위험합니다.
2. **저장소 3개를 혼동하지 마세요.** 프론트 수정은 `ASAK-front`, 백엔드는 `ASAK-back`, 문서/파이프라인은 `ASAK` (`c:\ASAK`).
3. **포트 충돌:** 8080(백엔드), 5173(프론트 Vite), 8765(뷰어)가 이미 쓰이면 "Address already in use" 에러 → 다른 프로그램 종료 또는 포트 변경.
4. **`sync_phase1_data_to_front.bat`** 는 저장소 내 상대 경로를 사용합니다. 루트에서 `python sync_phase1_data_to_front.py`를 써도 됩니다.
5. **상업적 사용 금지:** 샐러디 공개 정보 참고용 학습 프로젝트입니다.
6. **PowerShell 실행 정책:** 스크립트 실행이 막히면 가상환경 Python 경로를 직접 호출하세요 (위 2단계 참고).

---

## 세팅이 잘 됐는지 확인하는 체크리스트

- [ ] `git --version`, `python --version` OK
- [ ] `c:\ASAK`, `c:\ASAK-front`, `c:\ASAK-back` 클론 완료
- [ ] `data-pipeline/phase1` 가상환경 + `run_phase1.py` → `output/` 파일 생성
- [ ] `ASAK-back` 서버 기동 (8080 등)
- [ ] `ASAK-front` `npm run dev` → 브라우저 화면 표시
- [ ] 프론트에서 메뉴가 보이면 **프론트+백 연동 성공** 🎉

---

## 막혔을 때 / 더 읽을 문서

<table header-row="true">
<tr>
<td>문서</td>
<td>내용</td>
</tr>
<tr>
<td>[guides/01-team-setup.md](https://github.com/hagenie128/ASAK/blob/main/docs/guides/01-team-setup.md)</td>
<td>팀 세팅·Git·9주 일정 (상세)</td>
</tr>
<tr>
<td>[guides/README.md](https://github.com/hagenie128/ASAK/blob/main/docs/guides/README.md)</td>
<td>가이드 읽는 순서</td>
</tr>
<tr>
<td>[wiki/tech-stack-summary.md](https://github.com/hagenie128/ASAK/blob/main/docs/wiki/tech-stack-summary.md)</td>
<td>Java, React, 라이브러리 정리</td>
</tr>
<tr>
<td>[worklog/README.md](https://github.com/hagenie128/ASAK/blob/main/worklog/README.md)</td>
<td>일일 워크로그</td>
</tr>
<tr>
<td>[Notion 프로젝트 허브](https://app.notion.com/p/39151ef04f0b808f99f8ea068efb5790)</td>
<td>요구사항·WBS 정본</td>
</tr>
</table>

팀원에게 물어볼 때: **어느 저장소에서 작업 중인지**, **에러 메시지 전문**, **어느 단계에서 막혔는지**를 함께 알려주면 빨리 도와줄 수 있습니다.

---

# Part 2 — 워크로그 쓰기 (유치원 선생님 모드)

안녕하세요! 오늘도 수고 많으셨어요. 🌱

워크로그는 **"오늘 뭘 했는지"를 팀에게 알려주는 일기**예요.  
퇴근 전 **5분**만 쓰면 됩니다. 어렵지 않아요 — 차근차근 따라와 주세요!
