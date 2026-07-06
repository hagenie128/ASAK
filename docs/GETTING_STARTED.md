# ASAK 처음 시작하기 (초보자용)

> **한 줄 요약:** ASAK는 샐러디 키오스크를 만드는 풀스택 학습 프로젝트입니다. 화면(프론트)과 API(백엔드)를 **둘 다** 켜야 실제 주문 흐름을 볼 수 있습니다.

처음이어도 괜찮아요. 이 문서만 순서대로 따라 하면 됩니다.

**목차**

- [Part 1 — 프로젝트 세팅](#part-1--프로젝트-세팅)
- [Part 2 — 워크로그 쓰기 (유치원 선생님 모드)](#part-2--워크로그-쓰기-유치원-선생님-모드)

---

# Part 1 — 프로젝트 세팅

## 이 프로젝트가 뭔가요?

**ASAK** = **A Salad A Kiosk** (샐러디 키오스크 풀스택 프로젝트)

- 고객이 키오스크에서 메뉴를 고르고 주문하는 **화면(프론트엔드)**
- 메뉴·주문 데이터를 주고받는 **서버(백엔드 API)**
- 메뉴 원본 데이터를 모으는 **데이터 파이프라인(Python)**

이 세 가지가 함께 동작합니다.

---

## 꼭 알아둘 것: 저장소가 3개예요

헷갈리기 쉬운 부분이라 **먼저** 읽어 주세요.

| 로컬 폴더 (예시) | GitHub | 하는 일 |
|------------------|--------|---------|
| `c:\ASAK` | [ASAK](https://github.com/hagenie128/ASAK) | 문서, 데이터 파이프라인, 팀 가이드 |
| `c:\ASAK-front` | [ASAK-front](https://github.com/hagenie128/ASAK-front) | **실제** 키오스크 화면 (React) |
| `c:\ASAK-back` | [ASAK-back](https://github.com/hagenie128/ASAK-back) | **실제** API 서버 (Spring Boot) |

`ASAK` 통합 저장소 안의 `frontend/`, `backend/` 폴더는 **구조 참고용**에 가깝습니다.  
실제 키오스크 개발은 `ASAK-front`와 `ASAK-back`에서 합니다.

> 작업 후 통합 저장소(`ASAK`)에 다시 합칠 필요는 **없습니다.** 어디서 작업했으면 그 저장소에만 push 하면 됩니다.

---

## 왜 프론트와 백엔드를 둘 다 켜야 하나요?

| 케이스 | 어떻게 되나요? |
|--------|----------------|
| **프론트만** 켬 | 화면은 뜨지만 API 호출이 실패합니다. 메뉴가 안 나오거나, 로딩만 돌거나, 에러 화면이 나옵니다. |
| **백엔드만** 켬 | API는 살아 있지만 **화면이 없어서** 주문 흐름을 눈으로 확인할 수 없습니다. |
| **둘 다** 켬 | 화면에서 버튼을 누르면 → 백엔드가 데이터를 주고 → 화면에 메뉴·주문 결과가 보입니다. ✅ |

**비유:** 프론트 = 식당 메뉴판·주문 화면, 백엔드 = 주방. 메뉴판만 있으면 주문이 주방으로 안 가고, 주방만 있으면 손님이 주문할 방법이 없습니다.

### 예외: 데이터만 보고 싶을 때

`ASAK` 통합 저장소의 **간단한 데이터 뷰어**(`frontend/run_viewer.py`)는 JSON 파일만으로도 동작합니다.  
이건 "연습용 뷰어"이고, **진짜 키오스크 앱**은 `ASAK-front` + `ASAK-back` 조합입니다.

---

## 준비물 (설치 & 확인)

Windows(PowerShell) 기준입니다.

### 1. Git

- 설치: https://git-scm.com/download/win
- 확인:

```powershell
git --version
```

**성공 예:** `git version 2.x.x` 가 나오면 OK

### 2. Python 3.11

- 설치: https://www.python.org/downloads/ (설치 시 **"Add Python to PATH"** 체크)
- 확인:

```powershell
python --version
py -3.11 --version
```

**성공 예:** `Python 3.11.x`

> 데이터 파이프라인·뷰어·워크로그 스크립트에 사용합니다.

### 3. Java 21 (백엔드 개발 시)

- 설치: https://adoptium.net/ (Temurin 21 권장)
- 확인:

```powershell
java -version
```

**성공 예:** `openjdk version "21.x"`

### 4. Node.js 20 LTS (프론트 React 개발 시)

- 설치: https://nodejs.org/ (LTS)
- 확인:

```powershell
node --version
npm --version
```

**성공 예:** `v20.x.x`, `10.x.x`

### 5. Docker?

**이 프로젝트는 Docker를 쓰지 않습니다.** 설치 안 해도 됩니다.

### 6. Cursor 또는 VS Code

코드 편집용. 팀에서 Cursor를 많이 씁니다.

---

## 1단계: 저장소 클론하기

PowerShell을 열고:

```powershell
git clone https://github.com/hagenie128/ASAK.git c:\ASAK
git clone https://github.com/hagenie128/ASAK-front.git c:\ASAK-front
git clone https://github.com/hagenie128/ASAK-back.git c:\ASAK-back
```

**성공 확인:** 각 폴더에 `.git` 폴더가 있고, `git status` 가 에러 없이 나옵니다.

```powershell
cd c:\ASAK
git status
```

---

## 2단계: 데이터 파이프라인 세팅 (ASAK)

메뉴 JSON을 만들거나 갱신할 때 필요합니다.

```powershell
cd c:\ASAK\data-pipeline\phase1
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

처음 한 번 크롤링 실행:

```powershell
.\.venv\Scripts\python.exe run_phase1.py
```

**성공 확인:** `c:\ASAK\data-pipeline\phase1\output\` 아래에 `menus.json` 등 파일이 생깁니다.

> ⚠️ `output/` 폴더는 Git에 올라가지 않습니다 (`.gitignore`).

### Windows 팁: 가상환경 활성화가 막힐 때

`Activate.ps1` 실행이 거부되면 **활성화 없이** 아래처럼 Python 경로를 직접 쓰면 됩니다.

```powershell
.\.venv\Scripts\python.exe run_phase1.py
```

---

## 3단계: 백엔드 실행 (ASAK-back)

```powershell
cd c:\ASAK-back
```

Spring Boot 프로젝트이므로 보통:

```powershell
.\gradlew.bat bootRun
```

(또는 IDE에서 `AsakBackendApplication` 실행)

**성공 확인 (일반적인 경우):**

- 터미널에 `Started ...Application` 비슷한 로그
- 브라우저에서 `http://localhost:8080` (또는 팀이 정한 포트) 접속 시 응답

> `ASAK\backend\` 는 골격만 있는 참고 폴더입니다. **실제 실행은 `c:\ASAK-back`에서** 하세요.

---

## 4단계: 프론트 실행 (ASAK-front)

```powershell
cd c:\ASAK-front
npm install
npm run dev
```

**성공 확인:**

- 터미널에 `Local: http://localhost:5173/` (Vite 기본) 비슷한 주소
- 브라우저에 키오스크 화면이 열림

백엔드 API 주소는 `ASAK-front`의 환경 설정(예: `.env`, `VITE_API_URL`)을 확인하세요.  
백엔드가 꺼져 있으면 **네트워크 에러·빈 목록**이 나올 수 있습니다.

---

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

| 변수 | 필요할 때 | 설정 예 (PowerShell, **이 창에서만**) |
|------|-----------|--------------------------------------|
| `NOTION_TOKEN` | 일일 워크로그 Notion 동기화 | `$env:NOTION_TOKEN = "secret_..."` |
| `FIGMA_TOKEN` | Figma 자동화 스크립트 | `$env:FIGMA_TOKEN = "..."` |

> 토큰은 **절대 Git에 커밋하지 마세요.** `.gitignore`에 `.env`가 포함되어 있습니다.

워크로그 토큰 설정·검증은 [Part 2](#part-2--워크로그-쓰기-유치원-선생님-모드)를 참고하세요.

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

| 문서 | 내용 |
|------|------|
| [guides/01-team-setup.md](guides/01-team-setup.md) | 팀 세팅·Git·9주 일정 (상세) |
| [guides/README.md](guides/README.md) | 가이드 읽는 순서 |
| [wiki/tech-stack-summary.md](wiki/tech-stack-summary.md) | Java, React, 라이브러리 정리 |
| [worklog/README.md](../worklog/README.md) | 일일 워크로그 |
| [Notion 프로젝트 허브](https://app.notion.com/p/39151ef04f0b808f99f8ea068efb5790) | 요구사항·WBS 정본 |

팀원에게 물어볼 때: **어느 저장소에서 작업 중인지**, **에러 메시지 전문**, **어느 단계에서 막혔는지**를 함께 알려주면 빨리 도와줄 수 있습니다.

---

# Part 2 — 워크로그 쓰기 (유치원 선생님 모드)

안녕하세요! 오늘도 수고 많으셨어요. 🌱

워크로그는 **"오늘 뭘 했는지"를 팀에게 알려주는 일기**예요.  
퇴근 전 **5분**만 쓰면 됩니다. 어렵지 않아요 — 차근차근 따라와 주세요!

---

## 워크로그가 뭐예요? 왜 써요?

| 질문 | 답 |
|------|-----|
| **뭐예요?** | 하루에 한 줄 요약 + (선택) 조금 더 자세한 메모 |
| **어디에 남겨요?** | Git `worklog/daily/{이름}/` + Notion [📅 일일 워크로그](https://app.notion.com/p/eeae4beb07ad4051928a87de0ea4c8f9) 캘린더 |
| **왜 써요?** | 팀이 서로 뭘 하고 있는지 알 수 있고, 나중에 포트폴리오·회고에 쓸 수 있어요 |

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

| 메시지 | 해결 |
|--------|------|
| `NOTION_TOKEN 환경 변수가 설정되지 않았습니다` | 위 0단계 `$env:NOTION_TOKEN = "..."` 다시 실행 |
| `Notion API ... failed (401)` | 토큰이 틀렸거나 만료됨 → 팀 리더에게 새 토큰 요청 |
| `Notion API ... failed (404)` | Integration이 워크로그 DB에 연결 안 됨 → Notion [팀 가이드 §3~§5](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95) 참고 |

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

| 담당자 | 저장소 | 작업 | WBS / Issue | 상태 | 블로커 |
|---|---|---|---|---|---|
| 이하진 | ASAK-front | SCR-003 메뉴 옵션 UI | WBS-012 / #12 | ✅ 완료 | - |

---

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

| 옵션 | 의미 |
|------|------|
| `--date today` | 오늘 날짜 (또는 `2026-07-06`) |
| `--author` | 담당자 실명: `이하진` · `김나연` · `박유진` · `강민준` |
| `--task` | 작업 한 줄 요약 |
| `--ref` | WBS/SCR 참조 (예: `WBS-002`) |
| `--hours` | 투입 시간 |
| `--notes` | 추가 메모 |
| `--blocker` | 블로커 있음 체크 |
| `--dry-run` | API 호출 없이 미리보기만 |

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

| 상황 | 어떻게 되나요? |
|------|----------------|
| `create_worklog.py`를 같은 날 두 번 | **업데이트**됩니다 (새 줄이 아니라 기존 줄 수정) |
| `sync` + `create_worklog` 둘 다 쓰면서 내용이 다름 | 헷갈릴 수 있음 → **하나의 방법**만 쓰는 걸 추천 |
| 예전에 실수로 중복 생성됨 | 정리 스크립트 실행 (아래) |

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

---

## 자주 쓰는 명령 모음

| 목적 | 명령 |
|---|---|
| 토큰 검증 | `python asak-data/scripts/verify_notion_token.py` |
| 오늘 파일 생성 | `python worklog/scripts/init_daily.py` |
| Notion 동기화 (미리보기) | `python worklog/scripts/sync_daily_to_notion.py --date today --dry-run` |
| Notion 동기화 (실제) | `python worklog/scripts/sync_daily_to_notion.py --date today` |
| 한 줄 바로 올리기 | `python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "작업 요약"` |
| 전원 동기화 | `python worklog/scripts/sync_daily_to_notion.py --date today --all` |
| 중복 정리 | `python worklog/scripts/archive_duplicate_worklogs.py --dry-run` |

---

## 더 읽을 문서

| 문서 | 내용 |
|------|------|
| [worklog/guide-team-daily.md](../worklog/guide-team-daily.md) | 팀 일일 워크로그 상세 |
| [worklog/guide-personal-worklog.md](../worklog/guide-personal-worklog.md) | 개인별 명령 요약 |
| [worklog/README.md](../worklog/README.md) | 폴더 구조·확인 순서 |
| [Notion 팀 가이드](https://app.notion.com/p/39451ef04f0b81c0a018e8fe6ea9fb95) | 토큰·DB 스키마 정본 |

---

## 다음에 할 일

1. [guides/README.md](guides/README.md) 순서대로 01~02 읽기  
2. Notion [문서 읽는 순서](https://app.notion.com/p/39451ef04f0b81088a91d914f985fb11) 확인  
3. `develop` 브랜치에서 `feature/...` 로 작업 시작  
4. **매일 퇴근 전** 워크로그 한 줄 ✍️

화이팅! 🥗
