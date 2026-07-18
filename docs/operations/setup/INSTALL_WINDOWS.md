# Windows 설치 가이드 (유치원 선생님 모드)

> **선생님이 따라가요** — 클릭할 버튼, 체크할 상자, 폴더 경로까지 **한 단계씩** 적어 두었습니다.  
> **LTS 기준:** 2026-07 · 실제 의존성은 `ASAK-Kiosk/package.json`, `ASAK-Admin/package.json`, `ASAK-back/build.gradle`을 확인합니다.  
> **Notion 온보딩:** [🚀 ASAK 처음 시작하기 (팀 온보딩)](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b)

**목차**

0. [한 방에 자동 설정 (추천)](#0-한-방에-자동-설정-추천)
1. [설치할 도구 한눈에 보기](#1-설치할-도구-한눈에-보기)
2. [폴더 한 번에 만들기](#2-폴더-한-번에-만들기)
3. [Git 설치](#3-git-설치)
4. [Python 3.13 설치](#4-python-313-설치)
5. [Java 25 LTS (Temurin) 설치](#5-java-25-lts-temurin-설치)
6. [Node.js 24 LTS 설치](#6-nodejs-24-lts-설치)
7. [Cursor 설치 (선택)](#7-cursor-설치-선택)
8. [저장소 클론하기](#8-저장소-클론하기)
9. [환경 변수 NOTION_TOKEN 설정](#9-환경-변수-notion_token-설정)
10. [전체 설치 확인 체크리스트](#10-전체-설치-확인-체크리스트)

---

## 0. 한 방에 자동 설정 (추천)

저장소를 클론한 뒤 PowerShell에서 **한 번에** 도구 확인·폴더·venv·`.env`·MCP 템플릿을 설정할 수 있습니다.

```powershell
cd C:\ASAK
.\scripts\setup-windows.ps1
```

저장소까지 자동 clone (빈 폴더만):

```powershell
.\scripts\setup-windows.ps1 -CloneRepos
```

**더블클릭:** `scripts\setup-windows.bat` (창이 닫히기 전에 결과 확인)

| 스크립트 | 하는 일 |
|----------|---------|
| `scripts/setup-windows.ps1` | 메인 — 버전 확인, winget/choco 설치 시도, 폴더, venv, `.env`, MCP |
| `scripts/setup-git.ps1` | Git clone 3개 + `develop` 안내 (**git config 는 변경 안 함**) |
| `scripts/setup-mcp.ps1` | `.cursor/mcp.json` 템플릿 복사 — 상세 [MCP_SETUP.md](MCP_SETUP.md) |

**이미 설치된 도구는 건너뜁니다** (Git 2.40+, Python 3.13+, Java 25+, Node 24+, npm 11+).

**winget/choco 가 실패하면** 아래 1~7절 **수동 설치**를 그대로 따라 하세요. 자동·수동 가이드는 같은 버전 기준입니다.

---

## 1. 설치할 도구 한눈에 보기

| 순서 | 도구 | 권장 버전 (2026-07) | 꼭 필요한 사람 |
|------|------|---------------------|----------------|
| 1 | Git | 2.4x 이상 | **모두** |
| 2 | Python | **3.13.x** | 데이터 파이프라인·워크로그·뷰어 |
| 3 | Java (Temurin) | **25 LTS** | 백엔드 (`ASAK-back`) |
| 4 | Node.js | **24.x Active LTS** | 프론트 React (`ASAK-front`) |
| 5 | Cursor | 최신 | 선택 (VS Code도 가능) |

> **Python 3.12 vs 3.13:** 3.12는 2026년부터 Windows 설치 파일(바이너리) 제공이 중단되었습니다. **새 PC는 3.13**을 설치하세요.

### 권장 폴더 구조 (Program Files 말고 여기!)

| 용도 | 권장 경로 | 왜? |
|------|-----------|-----|
| 통합 저장소 | `C:\ASAK` | 프로젝트 루트. 권한 문제 적음 |
| 프론트 저장소 | `C:\ASAK-front` | GitHub `ASAK-front` 클론 |
| 백엔드 저장소 | `C:\ASAK-back` | GitHub `ASAK-back` 클론 |
| Python 가상환경 | `C:\ASAK\data-pipeline\phase1\.venv` | 팀 공통 위치 |

**Program Files(`C:\Program Files\...`)에 클론하면 안 되나요?**

- 관리자 권한(UAC) 팝업이 자주 뜹니다.
- `npm install`, `gradlew`, Python venv 만들 때 **쓰기 거부** 오류가 날 수 있습니다.
- 그래서 **`C:\ASAK`처럼 내가 만든 폴더**에 두는 것을 권장합니다.

---

## 2. 폴더 한 번에 만들기

설치 **전에** PowerShell을 열고 아래를 **복사 → 붙여넣기 → Enter** 하세요.

```powershell
New-Item -ItemType Directory -Force -Path C:\ASAK
New-Item -ItemType Directory -Force -Path C:\ASAK-front
New-Item -ItemType Directory -Force -Path C:\ASAK-back
```

**성공하면:** 아무 에러 없이 프롬프트만 다시 나옵니다.

**확인:**

```powershell
Test-Path C:\ASAK
Test-Path C:\ASAK-front
Test-Path C:\ASAK-back
```

세 줄 모두 `True`면 OK.

---

## 3. Git 설치

### 3-1. 다운로드

1. 브라우저에서 **https://git-scm.com/download/win** 을 엽니다.
2. 페이지가 자동으로 **64-bit Git for Windows Setup** 을 내려받기 시작합니다.
   - 자동 시작이 안 되면 **"Click here to download manually"** 링크를 클릭합니다.
3. 내려받은 파일 이름 예: `Git-2.49.0-64-bit.exe` (버전 숫자는 달라도 됩니다).

### 3-2. 설치 마법사 — 화면별 체크리스트

설치 파일을 **더블클릭**한 뒤, 아래 순서대로 **Next** 를 누릅니다.

| 화면 | 선생님 체크 |
|------|-------------|
| **Information** | Next |
| **Select Destination Location** | 기본값 `C:\Program Files\Git` 그대로 → Next |
| **Select Components** | ✅ Git Bash, ✅ Git GUI, ✅ Associate .git* … (기본 체크 유지) → Next |
| **Select Start Menu Folder** | Next |
| **Choosing the default editor** | 아무거나 OK (Notepad++ / VS Code 등) → Next |
| **Adjusting the name of the initial branch** | "Let Git decide" 또는 "main" → Next |
| **Adjusting your PATH environment** | ⭐ **"Git from the command line and also from 3rd-party software"** 선택 (보통 2번째 옵션, **Recommended**) → Next |
| **Choosing HTTPS transport** | OpenSSL library (기본) → Next |
| **Configuring the line ending conversions** | "Checkout Windows-style, commit Unix-style" (기본) → Next |
| **Configuring the terminal emulator** | MinTTY (기본) → Next |
| **Configuring git pull** | Default (fast-forward or merge) → Next |
| **Choosing a credential helper** | Git Credential Manager (기본) → Next |
| **Configuring extra options** | Enable file system caching (기본) → Next |
| **Configuring experimental options** | 비워두고 → **Install** |
| **Completing** | Finish |

> **핵심:** PATH 화면에서 **"Recommended"** 옵션을 고르면 PowerShell에서 `git` 명령을 쓸 수 있습니다.

### 3-3. 설치 확인

**PowerShell을 새로 연 뒤** (중요: 설치 전에 열어둔 창은 닫고 새로 여세요):

```powershell
git --version
```

**✅ 성공 예:**

```text
git version 2.49.0.windows.1
```

**❌ 실패:** `'git' is not recognized...`  
→ PowerShell을 **완전히 닫았다가 다시 열기** → 그래도 안 되면 Git 재설치 시 PATH 옵션 확인.

---

## 4. Python 3.13 설치

### 4-1. 다운로드

1. **https://www.python.org/downloads/** 를 엽니다.
2. 큰 노란 버튼 **"Download Python 3.13.x"** 를 클릭합니다. (3.13 최신 패치)
3. 파일 예: `python-3.13.14-amd64.exe`

### 4-2. 설치 마법사 — 화면별 체크리스트

| 화면 | 선생님 체크 |
|------|-------------|
| **첫 화면 (Install Python 3.13.x)** | ⭐ **맨 아래 "Add python.exe to PATH"** ✅ **반드시 체크** → **"Install Now"** 클릭 |
| (또는 Customize) | "Customize installation" → Next → **Optional Features** 전부 기본 → Next → **Advanced Options**에서 ✅ **Add Python to environment variables** → Install location 예: `C:\Python313` → Install |
| **Setup was successful** | **"Disable path length limit"** 가 보이면 **Yes** (긴 경로 허용) → Close |

> **가장 많이 하는 실수:** "Add python.exe to PATH" 체크를 **안 함** → 나중에 `python` 명령이 안 됨.

### 4-3. 폴더 설정 (가상환경)

Python **본체**는 설치 프로그램이 `C:\Users\...\AppData\Local\Programs\Python\Python313\` 등에 둡니다.  
**프로젝트용 가상환경**은 클론 후 아래에서 만듭니다:

```text
C:\ASAK\data-pipeline\phase1\.venv
```

(8단계 [저장소 클론](#8-저장소-클론하기) 후 [`GETTING_STARTED.md`](GETTING_STARTED.md) 2단계 참고)

### 4-4. 설치 확인

PowerShell **새 창**:

```powershell
python --version
py -3.13 --version
pip --version
```

**✅ 성공 예:**

```text
Python 3.13.14
Python 3.13.14
pip 25.x from ...
```

**❌ 실패:** `Python was not found`  
→ Python 재설치, **Add to PATH** 다시 체크. 또는 Microsoft Store 우회:

```powershell
py -3.13 --version
```

`py` launcher만 되면 venv는 `py -3.13 -m venv .venv` 로 만들 수 있습니다.

---

## 5. Java 25 LTS (Temurin) 설치

백엔드(`ASAK-back`, Spring Boot) 개발 시 필요합니다. 프론트만 하면 **건너뛰어도** 됩니다.

### 5-1. 다운로드

1. **https://adoptium.net/temurin/releases/** 를 엽니다.
2. 필터를 이렇게 맞춥니다:
   - **Version:** `25 - LTS`
   - **Operating System:** `Windows`
   - **Architecture:** `x64`
   - **Package Type:** `JDK`
3. **`.msi` Installer** 행의 **Download** 버튼을 클릭합니다.  
   - 직접 링크 예: https://adoptium.net/temurin/releases/?version=25&os=windows&arch=x64&package=jdk

### 5-2. 설치 마법사 — 화면별 체크리스트

| 화면 | 선생님 체크 |
|------|-------------|
| Welcome | Next |
| **Custom Setup** | Next (기본 구성요소 유지) |
| **Installation directory** | 기본 `C:\Program Files\Eclipse Adoptium\jdk-25.x.x-hotspot\` → Next |
| **Set JAVA_HOME variable** | ⭐ ✅ **체크** (가능하면 켜 두기) |
| **Java associated with .jar** | ✅ (기본) |
| **Add to PATH** | ⭐ ✅ **"Add to PATH"** 또는 **"Set or override PATH variable"** ✅ **반드시** |
| **Install** | Install → Finish |

> Temurin MSI는 보통 **PATH + JAVA_HOME** 을 자동 설정합니다. 체크박스가 보이면 **전부 켜세요.**

### 5-3. 설치 확인

PowerShell **새 창**:

```powershell
java -version
javac -version
```

**✅ 성공 예:**

```text
openjdk version "25.0.3" 2025-10-21 LTS
OpenJDK Runtime Environment Temurin-25.0.3+9 (build 25.0.3+9-LTS)
...
```

**❌ 실패:** `'java' is not recognized`  
→ PC 재부팅 또는 PowerShell 새 창 → 그래도 안 되면 **시스템 환경 변수**에 `JAVA_HOME` 수동 추가 (9절 PATH 설정과 같은 방법).

---

## 6. Node.js 24 LTS 설치

프론트 React(`ASAK-front`) 개발 시 필요합니다.

### 6-1. 다운로드

1. **https://nodejs.org/** 를 엽니다.
2. **Active LTS** 배지가 붙은 **24.x** 버전의 큰 초록 버튼을 클릭합니다.  
   - 버튼 글자 예: **"24.17.0 LTS"** · **"Recommended For Most Users"**
3. **Windows Installer (.msi)** — **64-bit** 가 내려받아집니다.  
   - 파일 예: `node-v24.17.0-x64.msi`

> **Current(26.x)는 누르지 마세요.** 아직 LTS가 아닙니다. **24 LTS** 를 선택하세요.

### 6-2. 설치 마법사 — 화면별 체크리스트

| 화면 | 선생님 체크 |
|------|-------------|
| Welcome | Next |
| **License Agreement** | ✅ I accept → Next |
| **Destination Folder** | `C:\Program Files\nodejs\` (기본) → Next |
| **Custom Setup** | **Node.js runtime**, **npm**, **Add to PATH** 항목이 포함된 기본 선택 유지 → Next |
| **Tools for Native Modules** | (선택) "Automatically install necessary tools" — 체크해도 되고 안 해도 됨 → Next |
| **Ready to install** | Install |
| **Completed** | Finish |

> Node Windows MSI는 기본적으로 **PATH에 node, npm** 을 넣습니다. 별도 "Add to PATH" 체크 화면이 없어도 정상입니다.

### 6-3. 설치 확인

PowerShell **새 창**:

```powershell
node --version
npm --version
```

**✅ 성공 예:**

```text
v24.17.0
11.5.2
```

(패치 번호는 달라도 **v24.x**, **npm 10~11.x** 면 OK)

**❌ 실패:** `'node' is not recognized`  
→ PowerShell 새 창 → 재설치.  
**❌ `npm install` 권한 오류:** 프로젝트를 `C:\ASAK-front`처럼 **Program Files 밖**에 두세요.

---

## 7. Cursor 설치 (선택)

팀에서 많이 쓰는 AI 코드 에디터입니다. VS Code를 써도 됩니다.

### 7-1. 다운로드

1. **https://cursor.com/download** 를 엽니다.
2. **"Download for Windows"** (또는 **Windows 64-bit**) 버튼 클릭.
3. `Cursor Setup.exe` 실행.

### 7-2. 설치

| 단계 | 선생님 체크 |
|------|-------------|
| 설치 경로 | 기본값 → Install |
| 완료 후 | Cursor 실행 |
| **Open Folder** | `C:\ASAK` 폴더 선택 (통합 저장소 클론 후) |

### 7-3. 확인

Cursor가 열리고 왼쪽 파일 트리에 `docs`, `data-pipeline` 등이 보이면 OK.

---

## 8. 저장소 클론하기

### 방법 A — PowerShell 명령 (추천)

PowerShell에서 **한 줄씩** Enter:

```powershell
git clone https://github.com/hagenie128/ASAK.git C:\ASAK
git clone https://github.com/hagenie128/ASAK-front.git C:\ASAK-front
git clone https://github.com/hagenie128/ASAK-back.git C:\ASAK-back
```

**✅ 성공 확인:**

```powershell
cd C:\ASAK
git status
dir C:\ASAK-front
dir C:\ASAK-back
```

- `git status` 에 `On branch main` (또는 `develop`) 비슷한 문구
- 세 폴더 모두 `.git` 숨김 폴더 존재

```powershell
Test-Path C:\ASAK\.git
Test-Path C:\ASAK-front\.git
Test-Path C:\ASAK-back\.git
```

세 줄 `True` → 클론 성공.

### 방법 B — 클릭으로 (GitHub Desktop / Cursor)

**GitHub Desktop:**

1. GitHub Desktop 설치 후 실행
2. **File → Clone repository**
3. URL 탭 → `https://github.com/hagenie128/ASAK` 입력
4. Local path: `C:\ASAK` → **Clone**
5. `ASAK-front`, `ASAK-back`도 같은 방법으로 각각 `C:\ASAK-front`, `C:\ASAK-back`

**Cursor:**

1. **Ctrl+Shift+P** → `Git: Clone`
2. URL 붙여넣기 → 대상 폴더 `C:\ASAK` 선택

### 클론 후 Python 가상환경 (데이터 파이프라인)

```powershell
cd C:\ASAK\data-pipeline\phase1
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**✅ 성공:** `.venv` 폴더 생성, pip install 에러 없음.

---

## 9. 환경 변수 NOTION_TOKEN 설정

워크로그를 Notion에 자동 올릴 때 필요합니다. **토큰은 Git에 올리지 마세요.**

### 방법 A — Windows 설정 UI (영구 저장, 추천)

1. **Windows 키** → `환경 변수` 검색 → **"시스템 환경 변수 편집"** 클릭  
   - 또는: **설정 → 시스템 → 정보 → 고급 시스템 설정 → 환경 변수**
2. **사용자 변수** (본인 계정만) 영역에서 **새로 만들기**
   - 변수 이름: `NOTION_TOKEN`
   - 변수 값: 팀 리더가 준 `secret_...` (따옴표 없이)
3. **확인** → **확인** → **확인**
4. **PowerShell·Cursor·터미널을 모두 닫았다가 다시 열기**

**확인:**

```powershell
cd C:\ASAK
python asak-data/scripts/verify_notion_token.py
```

**✅ 성공 예:** `OK: Integration 연결됨`

### 방법 B — `.env` 파일 (프로젝트 로컬)

1. 메모장을 엽니다.
2. 한 줄만 적습니다 (예시):

```env
NOTION_TOKEN=secret_여기에_받은_토큰
```

3. **다른 이름으로 저장**
   - 경로: `C:\ASAK\.env`
   - 파일 이름: `.env` (따옴표 포함 `" .env "` 로 저장하면 Windows에서 점 파일 만들기 쉬움)
   - 파일 형식: **모든 파일**
4. `.gitignore`에 `.env`가 있으므로 **Git에 커밋되지 않습니다.**

### 방법 C — PowerShell 임시 (창 닫으면 사라짐)

```powershell
$env:NOTION_TOKEN = "secret_여기에_받은_토큰"
```

매번 새 PowerShell을 열 때마다 다시 입력해야 합니다.

---

## 10. 전체 설치 확인 체크리스트

PowerShell **새 창** 하나에서:

```powershell
git --version
python --version
py -3.13 --version
java -version
node --version
npm --version
Test-Path C:\ASAK\.git
Test-Path C:\ASAK-front\.git
Test-Path C:\ASAK-back\.git
```

| 항목 | 기대 결과 |
|------|-----------|
| Git | `git version 2.x` |
| Python | `Python 3.13.x` |
| Java | `openjdk version "25.x"` |
| Node | `v24.x.x` |
| npm | `11.x` 또는 `10.x` |
| 클론 3개 | 모두 `True` |

---

## 자주 나는 오류 & 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| `'git' / 'python' / 'node' is not recognized` | PATH 미설치 또는 터미널 재시작 안 함 | 프로그램 재설치(PATH 옵션) + **PowerShell 완전히 새로 열기** |
| `Access is denied` / `EPERM` npm·venv | `Program Files` 아래에서 작업 | 프로젝트를 `C:\ASAK` 등으로 이동 |
| Python `Add to PATH` 안 함 | 설치 시 체크 누락 | Python **Modify** 재설치 또는 `py -3.13` 사용 |
| `Activate.ps1` 실행 거부 | PowerShell 실행 정책 | 활성화 없이 `.\.venv\Scripts\python.exe` 직접 사용 ([`GETTING_STARTED.md`](GETTING_STARTED.md) 참고) |
| Java 버전 17/21만 보임 | 예전 JDK가 PATH 앞에 있음 | `where java` 로 경로 확인 → Temurin 25 PATH 순서 조정 |
| Node 26 설치됨 | Current 버전 클릭 | **24 LTS** 로 재설치 |
| NOTION 401 | 토큰 오류 | 팀 리더에게 새 토큰, 환경 변수 다시 설정 |

---

## 다음 단계

설치가 끝났으면:

1. [`GETTING_STARTED.md`](GETTING_STARTED.md) — 백엔드·프론트 실행, 워크로그
2. [`MCP_SETUP.md`](MCP_SETUP.md) — Cursor Notion MCP
3. [`guides/01-team-setup.md`](../../guides/01-team-setup.md) — Git 브랜치·9주 일정
3. [Notion 🚀 팀 온보딩](https://app.notion.com/p/39551ef04f0b8193ae2ad4d529ab2d7b)

화이팅! 🥗
