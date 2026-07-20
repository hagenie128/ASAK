# Cursor MCP 설정 (ASAK 팀)

> **관련:** [worklog/guide-mcp-sync.md](../../../worklog/guide-mcp-sync.md) · [getting-started.md](getting-started.md)  
> **자동 설정:** `.\scripts\setup-mcp.ps1` (또는 `setup-windows.ps1` 에 포함)

Cursor에서 Notion·기타 MCP를 쓰기 위한 팀 공통 안내입니다.

---

## 빠른 설정

PowerShell (저장소 루트):

```powershell
cd C:\ASAK
.\scripts\setup-mcp.ps1
```

스크립트가 하는 일:

1. `config/mcp.json.example` → `.cursor/mcp.json` 복사 (**이미 있으면 건너뜀**)
2. 필요한 환경 변수 목록 출력
3. Cursor Notion 플러그인 연결 안내

---

## MCP 설정 위치

| 위치 | 용도 |
|------|------|
| **프로젝트** `.cursor/mcp.json` | 이 저장소를 열었을 때만 적용 (팀 템플릿) |
| **사용자** `%USERPROFILE%\.cursor\mcp.json` | Cursor 전역 MCP |
| **Cursor UI** Settings → MCP | Notion 등 플러그인 마켓플레이스 연결 |

프로젝트 템플릿 예시 (`config/mcp.json.example`):

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

> 실제 Notion 연동은 Cursor **Notion 플러그인** OAuth가 더 편합니다. 위 JSON은 REST 대안·참고용입니다.

---

## Notion MCP (Cursor 플러그인 — 권장)

1. **Cursor** 실행
2. **Settings** (`Ctrl+,`) → **MCP** (또는 **Features → MCP**)
3. **Notion** 플러그인 추가 · Marketplace에서 "Notion" 검색
4. Notion 계정 로그인 · ASAK 워크스페이스 접근 허용
5. 채팅에서 Notion 페이지·DB 검색·작업 가능 여부 확인

### 워크로그 MCP 워크플로

| 경로 | 언제 쓰나요 |
|------|-------------|
| **REST API** (`NOTION_TOKEN` + `sync_daily_to_notion.py`) | 로컬·CI, 토큰 있을 때 **권장** |
| **Cursor Notion MCP** | 토큰 없이 에이전트가 Notion에 직접 upsert |

상세: [worklog/guide-mcp-sync.md](../../../worklog/guide-mcp-sync.md)

---

## 필수·권장 환경 변수

| 변수 | 필수 | 용도 | 설정 방법 |
|------|------|------|-----------|
| `NOTION_TOKEN` | 워크로그·스크립트 시 | Notion REST API (`secret_...`) | `.env` 또는 Windows 사용자 환경 변수 |
| `FIGMA_TOKEN` | Figma 스크립트 시 | `sync_figma_links.py` 등 | `.env` |

`.env` 템플릿: 저장소 루트 `.env.example` → `.env` 복사 후 값 입력.

```powershell
# 검증
python asak-data/scripts/verify_notion_token.py
```

**토큰은 Git에 커밋하지 마세요.**

영구 환경 변수 설정: [install-windows.md §9](install-windows.md#9-환경-변수-notion_token-설정)

---

## 수동 MCP 추가 (선택)

Cursor Settings → MCP → **Add new MCP server**

- **Notion (HTTP):** `https://mcp.notion.com/mcp`
- 팀에서 추가하는 서버가 있으면 이 문서에 이름·URL을 PR로 보강하세요.

---

## 문제 해결

| 증상 | 해결 |
|------|------|
| Notion MCP 연결 안 됨 | Cursor 재시작 · Notion 플러그인 재연결 · 워크스페이스 Integration 권한 확인 |
| `NOTION_TOKEN not set` | `.env` 또는 `$env:NOTION_TOKEN` 설정 후 터미널 재시작 |
| `.cursor/mcp.json` 없음 | `.\scripts\setup-mcp.ps1` 재실행 |
| MCP와 REST 결과 불일치 | Git `worklog/daily/` 가 정본 — [guide-mcp-sync.md](../../../worklog/guide-mcp-sync.md) upsert 규칙 확인 |

---

## 관련 파일

| 파일 | 역할 |
|------|------|
| `scripts/setup-mcp.ps1` | 템플릿 복사·안내 |
| `config/mcp.json.example` | 프로젝트 MCP 템플릿 |
| `.env.example` | `NOTION_TOKEN`, `FIGMA_TOKEN` 플레이스홀더 |
| `worklog/notion_config.json` | 워크로그 DB ID |
| `docs/operations/setup/install-windows.md` | Windows 전체 설치 (수동 fallback) |
