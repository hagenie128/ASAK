# ASAK 팀 AI 도구 설치 가이드

> 상태: **Current** · 갱신: 2026-07-24
> 이 문서는 팀원 각자의 Windows PC에서 스킬과 `code-review-graph`를 설치하는 방법이다. 사용 방법은 [07-ai-agent-tools-guide.md](07-ai-agent-tools-guide.md), 바로 쓰는 요청문은 [08-ai-skill-prompt-examples.md](08-ai-skill-prompt-examples.md)를 본다.

## 1. 먼저 알아둘 점

- 스킬은 각 PC의 개인 폴더(`~/.agents/skills`, `~/.claude/skills`, `~/.codex/skills`)에 설치된다. Git push만으로 팀원 PC에 설치되지 않는다.
- `code-review-graph`는 저장소별로 그래프를 따로 만든다. `ASAK-Admin`, `ASAK-Kiosk`, `ASAK-back`을 한 그래프로 섞지 않는다.
- 자동 생성되는 `.mcp.json`, `.cursor/mcp.json`에는 개인 PC의 Python 경로가 들어갈 수 있다. **현재는 Git에 추가하거나 커밋하지 않는다.**
- 실제 구현은 팀원이 직접 한다. AI에는 분석·리뷰·테스트 항목을 우선 요청한다.

## 2. 공통 준비

PowerShell에서 확인한다.

```powershell
python --version
npx.cmd --version
```

Python 3.10 이상이 필요하다. `npx.cmd`가 없으면 Node.js를 먼저 설치한다.

## 3. 공통 스킬 설치

아래 명령은 `grill-with-docs`, `diagnosing-bugs`, `handoff`만 설치한다. 구현·TDD·자동 리팩터링 스킬은 설치하지 않는다.

```powershell
npx.cmd skills@latest add mattpocock/skills --global --agent codex claude-code cursor antigravity --skill grill-with-docs diagnosing-bugs handoff --yes --copy
```

설치 후 Codex·Claude Code·Cursor·Antigravity를 재시작한다.

> `diagnosing-bugs`는 진단 전용이다. 요청에 `자동 수정·파일 생성·Git 명령은 하지 마`를 반드시 넣는다.

## 4. 코드 그래프 설치

### 4-1. 패키지 설치

```powershell
python -m pip install code-review-graph
```

### 4-2. 저장소별 그래프 만들기

아래 세 블록을 저장소마다 한 번씩 실행한다. 그래프 DB는 저장소 밖 작업공간 폴더에 저장한다.

```powershell
Set-Location C:\ASAK-workspace\ASAK-Admin
code-review-graph build --repo . --data-dir C:\ASAK-workspace\.code-review-graph-data\ASAK-Admin
```

```powershell
Set-Location C:\ASAK-workspace\ASAK-Kiosk
code-review-graph build --repo . --data-dir C:\ASAK-workspace\.code-review-graph-data\ASAK-Kiosk
```

```powershell
Set-Location C:\ASAK-workspace\ASAK-back
code-review-graph build --repo . --data-dir C:\ASAK-workspace\.code-review-graph-data\ASAK-back
```

`ASAK-back`에 미추적 파일이 있으면 그래프에는 포함되지 않는다. 팀원 파일을 억지로 Git에 추가하지 말고, 해당 파일은 AI에게 별도로 읽게 한다.

### 4-3. Claude Code·Cursor 연결

각 저장소에서 아래 명령을 실행한다. 이 과정은 로컬 `.mcp.json`, `.cursor/mcp.json`, `.gitignore`를 만들거나 갱신한다. **팀원 개인 설정이므로 커밋하지 않는다.**

```powershell
code-review-graph install --platform claude --repo . --no-skills --no-hooks --no-instructions -y
code-review-graph install --platform cursor --repo . --no-skills --no-hooks --no-instructions -y
```

### 4-4. Codex·Antigravity 연결

두 도구는 사용자 전역 MCP 설정을 공유한다. 자동 설치를 저장소마다 반복하면 이전 저장소의 `cwd`를 덮어쓸 수 있다.

1. [Codex 템플릿](agent-config-templates/code-review-graph-codex.example.toml)을 열어 `<WORKSPACE>`를 각자 작업공간 절대 경로로 바꾼다.
2. 세 서버 항목을 개인 Codex 설정 파일에 추가한다.
3. [Antigravity 템플릿](agent-config-templates/code-review-graph-antigravity.example.json)을 같은 방식으로 개인 Antigravity MCP 설정에 병합한다.
4. 각 도구를 재시작한다.

템플릿은 예시 파일이므로 수정한 뒤에도 Git에 올리지 않는다.

## 5. 확인과 갱신

```powershell
code-review-graph status --repo . --data-dir C:\ASAK-workspace\.code-review-graph-data\ASAK-Admin --json
code-review-graph update --repo . --data-dir C:\ASAK-workspace\.code-review-graph-data\ASAK-Admin
```

첫 명령은 그래프 파일 수·노드 수·현재 커밋 일치 여부를 확인한다. 두 번째 명령은 팀원이 변경한 Git 추적 파일만 빠르게 갱신한다.

## 6. 첫 사용 요청문

```text
[ASAK-Admin / ASAK-Kiosk / ASAK-back]에서 code-review-graph로 변경 영향 범위를 분석해줘.
먼저 읽어야 할 파일, 호출·의존 관계, 관련 테스트만 알려줘.
Product Bible, Screen Bible, Figma는 별도 근거로 구분하고 코드 수정은 하지 마.
```

## 7. 공유하지 않는 것

- `~/.agents/skills`, `~/.claude/skills`, `~/.codex/skills`
- 개인 Codex·Antigravity 설정 파일
- 자동 생성된 `.mcp.json`, `.cursor/mcp.json`
- `.code-review-graph-data/`의 그래프 DB

공유할 것은 이 가이드, 요청문 예시, 그리고 `agent-config-templates/`의 **빈칸 템플릿**뿐이다.
