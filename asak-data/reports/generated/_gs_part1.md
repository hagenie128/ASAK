> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: One-off generated report fragment.
> Canonical Replacement: None; regenerate only when required.
> Original Path: `asak-data/scripts/_gs_part1.md`

<callout icon="📌" color="blue_bg">
**Notion 정본** · Git mirror: [`docs/GETTING_STARTED.md`](https://github.com/hagenie128/ASAK/blob/main/docs/GETTING_STARTED.md)
</callout>
---
> **한 줄 요약:** ASAK는 샐러디 키오스크를 만드는 풀스택 학습 프로젝트입니다. 화면(프론트)과 API(백엔드)를 **둘 다** 켜야 실제 주문 흐름을 볼 수 있습니다.

처음이어도 괜찮아요. 이 문서만 순서대로 따라 하면 됩니다.

**목차**

- [Part 1 — 프로젝트 세팅](https://github.com/hagenie128/ASAK/blob/main/#part-1--프로젝트-세팅)
- [Part 2 — 워크로그 쓰기 (유치원 선생님 모드)](https://github.com/hagenie128/ASAK/blob/main/#part-2--워크로그-쓰기-유치원-선생님-모드)

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

<table header-row="true">
<tr>
<td>로컬 폴더 (예시)</td>
<td>GitHub</td>
<td>하는 일</td>
</tr>
<tr>
<td>`c:\ASAK`</td>
<td>[ASAK](https://github.com/hagenie128/ASAK)</td>
<td>문서, 데이터 파이프라인, 팀 가이드</td>
</tr>
<tr>
<td>`c:\ASAK-front`</td>
<td>[ASAK-front](https://github.com/hagenie128/ASAK-front)</td>
<td>**실제** 키오스크 화면 (React)</td>
</tr>
<tr>
<td>`c:\ASAK-back`</td>
<td>[ASAK-back](https://github.com/hagenie128/ASAK-back)</td>
<td>**실제** API 서버 (Spring Boot)</td>
</tr>
</table>

`ASAK` 통합 저장소 안의 `frontend/`, `backend/` 폴더는 **구조 참고용**에 가깝습니다.  
실제 키오스크 개발은 `ASAK-front`와 `ASAK-back`에서 합니다.

> 작업 후 통합 저장소(`ASAK`)에 다시 합칠 필요는 **없습니다.** 어디서 작업했으면 그 저장소에만 push 하면 됩니다.

---

## 왜 프론트와 백엔드를 둘 다 켜야 하나요?

<table header-row="true">
<tr>
<td>케이스</td>
<td>어떻게 되나요?</td>
</tr>
<tr>
<td>**프론트만** 켬</td>
<td>화면은 뜨지만 API 호출이 실패합니다. 메뉴가 안 나오거나, 로딩만 돌거나, 에러 화면이 나옵니다.</td>
</tr>
<tr>
<td>**백엔드만** 켬</td>
<td>API는 살아 있지만 **화면이 없어서** 주문 흐름을 눈으로 확인할 수 없습니다.</td>
</tr>
<tr>
<td>**둘 다** 켬</td>
<td>화면에서 버튼을 누르면 → 백엔드가 데이터를 주고 → 화면에 메뉴·주문 결과가 보입니다. ✅</td>
</tr>
</table>

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

### 2. Python 3.13

- 설치: https://www.python.org/downloads/ (설치 시 **"Add Python to PATH"** 체크)
- 확인:

```powershell
python --version
py -3.13 --version
```

**성공 예:** `Python 3.13.x`

> 데이터 파이프라인·뷰어·워크로그 스크립트에 사용합니다.

### 3. Java 25 LTS (백엔드 개발 시)

- 설치: https://adoptium.net/ (Temurin 25 권장)
- 확인:

```powershell
java -version
```

**성공 예:** `openjdk version "25.x"`

### 4. Node.js 24 LTS (프론트 React 개발 시)

- 설치: https://nodejs.org/ (Active LTS)
- 확인:

```powershell
node --version
npm --version
```

**성공 예:** `v24.x.x`, `11.x.x`

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
py -3.13 -m venv .venv
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
