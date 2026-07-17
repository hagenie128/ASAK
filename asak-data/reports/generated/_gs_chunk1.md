> Status: ARCHIVED
> Archived Date: 2026-07-16
> Reason: One-off generated report fragment.
> Canonical Replacement: None; regenerate only when required.
> Original Path: `asak-data/scripts/_gs_chunk1.md`

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
