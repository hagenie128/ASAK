#Requires -Version 5.1
<#
.SYNOPSIS
  Cursor MCP 설정 안내 및 프로젝트 템플릿 복사 (idempotent)

.DESCRIPTION
  - config/mcp.json.example → .cursor/mcp.json 복사 (없을 때만)
  - 필요한 환경 변수 안내
  - 상세 문서: docs/MCP_SETUP.md

.PARAMETER RootPath
  ASAK 통합 저장소 경로 (기본: 자동 탐지 또는 C:\ASAK)

.PARAMETER RepoRoot
  현재 작업 중인 저장소 루트 (기본: 스크립트 기준 상위 폴더)

.EXAMPLE
  .\scripts\setup-mcp.ps1
  .\scripts\setup-mcp.ps1 -RepoRoot C:\ASAK
#>
[CmdletBinding()]
param(
    [string]$RootPath = 'C:\ASAK',
    [string]$RepoRoot = ''
)

$ErrorActionPreference = 'Continue'
$libPath = Join-Path $PSScriptRoot 'asak-setup-lib.ps1'
. $libPath

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = Get-AsakRepoRoot -StartPath $PSScriptRoot
    if (Test-Path $RootPath) {
        $RepoRoot = (Resolve-Path $RootPath).Path
    }
}

Write-SetupBanner 'ASAK Cursor MCP 설정'

$templatePath = Join-Path $RepoRoot 'config\mcp.json.example'
$cursorDir = Join-Path $RepoRoot '.cursor'
$targetPath = Join-Path $cursorDir 'mcp.json'
$userMcpPath = Join-Path $env:USERPROFILE '.cursor\mcp.json'

# 프로젝트 MCP
if (Test-Path $targetPath) {
    Write-SetupSkip "프로젝트 MCP 설정 이미 존재: $targetPath"
}
elseif (Test-Path $templatePath) {
    if (-not (Test-Path $cursorDir)) {
        New-Item -ItemType Directory -Force -Path $cursorDir | Out-Null
    }
    Copy-Item -LiteralPath $templatePath -Destination $targetPath
    Write-SetupOk "템플릿 복사: config/mcp.json.example → .cursor/mcp.json"
}
else {
    Write-SetupWarn "템플릿 없음: $templatePath"
    Write-SetupInfo 'docs/MCP_SETUP.md 에서 수동으로 MCP 를 설정하세요.'
}

# 사용자 전역 MCP 안내
if (Test-Path $userMcpPath) {
    Write-SetupSkip "사용자 전역 MCP 설정 존재: $userMcpPath"
}
else {
    Write-SetupInfo "사용자 전역 MCP (선택): $userMcpPath"
    Write-SetupInfo 'Cursor → Settings → MCP 에서 Notion 플러그인을 활성화할 수 있습니다.'
}

Write-Host ""
Write-SetupBanner '필수·권장 환경 변수'
Write-Host @"

  | 변수           | 용도                          | 설정 위치              |
  |----------------|-------------------------------|------------------------|
  | NOTION_TOKEN   | 워크로그·Notion REST API      | .env 또는 사용자 환경 변수 |
  | FIGMA_TOKEN    | Figma 링크 동기화 스크립트    | .env 또는 사용자 환경 변수 |

  .env 예시 (저장소 루트):

    NOTION_TOKEN=secret_...
    FIGMA_TOKEN=...

  토큰은 Git에 커밋하지 마세요. .env.example 만 저장소에 있습니다.

"@ -ForegroundColor White

Write-SetupBanner 'Cursor Notion MCP (팀 권장)'
Write-Host @"

  1. Cursor 실행 → Settings (Ctrl+,) → MCP
  2. "Notion" 플러그인 추가 (또는 Marketplace에서 Notion MCP)
  3. Notion 계정 연결 후 워크스페이스 권한 승인
  4. 워크로그 MCP 흐름: worklog/guide-mcp-sync.md

  REST API 경로 (권장, 로컬 스크립트):

    python asak-data/scripts/verify_notion_token.py
    python worklog/scripts/sync_daily_to_notion.py --date today --dry-run

"@ -ForegroundColor White

Write-SetupBanner 'MCP 요약'
$checks = @(
    @{ Label = '프로젝트 .cursor/mcp.json'; Ok = (Test-Path $targetPath) },
    @{ Label = 'config/mcp.json.example'; Ok = (Test-Path $templatePath) },
    @{ Label = 'docs/MCP_SETUP.md'; Ok = (Test-Path (Join-Path $RepoRoot 'docs\MCP_SETUP.md')) },
    @{ Label = '.env.example'; Ok = (Test-Path (Join-Path $RepoRoot '.env.example')) }
)
foreach ($c in $checks) {
    if ($c.Ok) { Write-SetupOk $c.Label } else { Write-SetupFail $c.Label }
}

Write-Host ""
Write-SetupInfo '상세 문서: docs/MCP_SETUP.md'
