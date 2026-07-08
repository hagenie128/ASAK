#Requires -Version 5.1
<#
.SYNOPSIS
  ASAK Windows 원클릭 개발 환경 설정 (idempotent)

.DESCRIPTION
  도구 버전 확인 → 부족하면 winget/choco 설치 시도 → 폴더 생성 → (선택) Git clone
  → Python venv → .env 복사 → MCP 템플릿 → 최종 체크리스트

.PARAMETER RootPath
  통합 저장소 경로 (기본 C:\ASAK)

.PARAMETER CloneRepos
  비어 있는 폴더에 Git 저장소 자동 clone

.PARAMETER SkipInstall
  패키지 설치 단계 건너뛰기 (버전 확인만)

.PARAMETER SkipVenv
  Python 가상환경 생성·pip install 건너뛰기

.PARAMETER SkipMcp
  MCP 설정 단계 건너뛰기

.EXAMPLE
  .\scripts\setup-windows.ps1
  .\scripts\setup-windows.ps1 -CloneRepos
  .\scripts\setup-windows.ps1 -RootPath D:\work\ASAK -SkipInstall
#>
[CmdletBinding()]
param(
    [string]$RootPath = 'C:\ASAK',
    [switch]$CloneRepos,
    [switch]$SkipInstall,
    [switch]$SkipVenv,
    [switch]$SkipMcp
)

$ErrorActionPreference = 'Continue'
$libPath = Join-Path $PSScriptRoot 'asak-setup-lib.ps1'
. $libPath

$summary = [ordered]@{}
$paths = Get-AsakRepoPaths -RootPath $RootPath
$repoRoot = Get-AsakRepoRoot -StartPath $PSScriptRoot

Write-Host ""
Write-Host '========================================' -ForegroundColor Cyan
Write-Host '  ASAK Windows 개발 환경 설정' -ForegroundColor Cyan
Write-Host "  RootPath: $($paths.Asak)" -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ""

# --- 1. 도구 버전 확인 및 설치 ---
Write-SetupBanner '1/6 도구 버전 확인'

$toolSpecs = @(
    @{
        Name       = 'Git'
        TestFn     = { Test-GitInstalled }
        MinLabel   = '2.40+'
        WingetId   = 'Git.Git'
        ChocoId    = 'git'
        ManualUrl  = 'https://git-scm.com/download/win'
        Required   = $true
    },
    @{
        Name       = 'Python'
        TestFn     = { Test-PythonInstalled }
        MinLabel   = '3.13+'
        WingetId   = 'Python.Python.3.13'
        ChocoId    = 'python313'
        ManualUrl  = 'https://www.python.org/downloads/'
        Required   = $true
    },
    @{
        Name       = 'Java (Temurin)'
        TestFn     = { Test-JavaInstalled }
        MinLabel   = '25 LTS+'
        WingetId   = 'EclipseAdoptium.Temurin.25.JDK'
        ChocoId    = 'temurin25'
        ManualUrl  = 'https://adoptium.net/temurin/releases/?version=25'
        Required   = $false
    },
    @{
        Name       = 'Node.js'
        TestFn     = { Test-NodeInstalled }
        MinLabel   = '24 LTS+'
        WingetId   = 'OpenJS.NodeJS.LTS'
        ChocoId    = 'nodejs-lts'
        ManualUrl  = 'https://nodejs.org/'
        Required   = $false
    },
    @{
        Name       = 'npm'
        TestFn     = { Test-NpmInstalled }
        MinLabel   = '11+'
        WingetId   = ''
        ChocoId    = ''
        ManualUrl  = 'Node.js 24 LTS 재설치 시 함께 설치됨'
        Required   = $false
    }
)

foreach ($spec in $toolSpecs) {
    $result = & $spec.TestFn
    $key = $spec.Name
    if ($result.Ok) {
        $detail = if ($result.Detail) { $result.Detail } else { $result.Version }
        Write-SetupSkip "$($spec.Name) $($spec.MinLabel) — 이미 충족: $detail"
        $summary[$key] = 'ok'
    }
    else {
        Write-SetupFail "$($spec.Name) $($spec.MinLabel) — 미설치 또는 버전 부족"
        $summary[$key] = 'missing'

        if ($SkipInstall) {
            Write-SetupInfo 'SkipInstall — 자동 설치 건너뜀'
            continue
        }

        if ($spec.Name -eq 'npm') {
            Write-SetupInfo $spec.ManualUrl
            continue
        }

        if ($spec.WingetId -or $spec.ChocoId) {
            $installed = Invoke-PackageInstall -ToolName $spec.Name `
                -WingetId $spec.WingetId -ChocoId $spec.ChocoId -ManualUrl $spec.ManualUrl
            if ($installed) {
                $recheck = & $spec.TestFn
                if ($recheck.Ok) {
                    $summary[$key] = 'installed'
                    Write-SetupOk "$($spec.Name) 설치 후 버전 확인됨"
                }
                else {
                    Write-SetupWarn "$($spec.Name) 설치됐지만 PATH 반영 전일 수 있습니다. PowerShell을 새로 열고 다시 실행하세요."
                    $summary[$key] = 'pending-restart'
                }
            }
        }
        else {
            Write-SetupInfo "수동 설치: $($spec.ManualUrl)"
        }
    }
}

# --- 2. 폴더 생성 ---
Write-SetupBanner '2/6 작업 폴더'
foreach ($key in @('Asak', 'Front', 'Back')) {
    $p = $paths[$key]
    if (-not (Test-Path $p)) {
        New-Item -ItemType Directory -Force -Path $p | Out-Null
        Write-SetupOk "생성: $p"
        $summary["folder-$key"] = 'created'
    }
    else {
        Write-SetupSkip "존재: $p"
        $summary["folder-$key"] = 'exists'
    }
}

# --- 3. Git clone (선택) ---
Write-SetupBanner '3/6 Git 저장소'
if ($CloneRepos) {
    $gitScript = Join-Path $PSScriptRoot 'setup-git.ps1'
    & $gitScript -RootPath $RootPath
    $summary['git-clone'] = 'attempted'
}
else {
    Write-SetupInfo 'CloneRepos 플래그 없음 — clone 건너뜀'
    Write-SetupInfo "자동 clone: .\scripts\setup-windows.ps1 -CloneRepos"
    Write-SetupInfo "또는: .\scripts\setup-git.ps1"
    $summary['git-clone'] = 'skipped'
}

# --- 4. Python venv ---
Write-SetupBanner '4/6 Python 가상환경 (data-pipeline/phase1)'
$phase1Path = Join-Path $repoRoot 'data-pipeline\phase1'
$venvPath = Join-Path $phase1Path '.venv'
$reqPath = Join-Path $phase1Path 'requirements.txt'

if ($SkipVenv) {
    Write-SetupSkip 'SkipVenv — 가상환경 단계 건너뜀'
    $summary['venv'] = 'skipped'
}
elseif (-not (Test-Path $phase1Path)) {
    Write-SetupWarn "phase1 경로 없음: $phase1Path (저장소 clone 후 다시 실행)"
    $summary['venv'] = 'no-repo'
}
else {
    $py = Get-PythonInvoker
    if (-not $py) {
        Write-SetupFail 'Python 3.13 없음 — venv 생성 불가'
        $summary['venv'] = 'no-python'
    }
    else {
        if (Test-Path (Join-Path $venvPath 'Scripts\python.exe')) {
            Write-SetupSkip "가상환경 이미 존재: $venvPath"
            $summary['venv'] = 'exists'
        }
        else {
            Write-SetupInfo "venv 생성: $venvPath"
            $venvArgs = $py.Args + @('-m', 'venv', $venvPath)
            & $py.Exe @venvArgs 2>&1 | Out-Host
            if (Test-Path (Join-Path $venvPath 'Scripts\python.exe')) {
                Write-SetupOk '가상환경 생성 완료'
                $summary['venv'] = 'created'
            }
            else {
                Write-SetupFail '가상환경 생성 실패'
                $summary['venv'] = 'failed'
            }
        }

        $venvPython = Join-Path $venvPath 'Scripts\python.exe'
        if ((Test-Path $venvPython) -and (Test-Path $reqPath)) {
            Write-SetupInfo 'pip install -r requirements.txt'
            & $venvPython -m pip install --upgrade pip --quiet 2>&1 | Out-Null
            & $venvPython -m pip install -r $reqPath 2>&1 | Out-Host
            if ($LASTEXITCODE -eq 0) {
                Write-SetupOk 'requirements.txt 설치 완료'
                $summary['pip'] = 'ok'
            }
            else {
                Write-SetupWarn 'pip install 일부 실패 — 수동 확인 필요'
                $summary['pip'] = 'warn'
            }
        }
    }
}

# --- 5. .env ---
Write-SetupBanner '5/6 환경 변수 파일 (.env)'
$envExample = Join-Path $repoRoot '.env.example'
$envFile = Join-Path $repoRoot '.env'

if (-not (Test-Path $envExample)) {
    @"
# ASAK 로컬 환경 변수 템플릿
NOTION_TOKEN=
FIGMA_TOKEN=
"@ | Set-Content -Path $envExample -Encoding UTF8
    Write-SetupOk '.env.example 생성'
}

if (Test-Path $envFile) {
    Write-SetupSkip ".env 이미 존재: $envFile"
    $summary['env'] = 'exists'
}
else {
    Copy-Item -LiteralPath $envExample -Destination $envFile
    Write-SetupOk ".env 생성 (.env.example 복사) — 토큰을 직접 채우세요"
    $summary['env'] = 'created'
}

# --- 6. MCP ---
Write-SetupBanner '6/6 MCP 설정'
if ($SkipMcp) {
    Write-SetupSkip 'SkipMcp — MCP 단계 건너뜀'
    $summary['mcp'] = 'skipped'
}
else {
    $mcpScript = Join-Path $PSScriptRoot 'setup-mcp.ps1'
    & $mcpScript -RepoRoot $repoRoot -RootPath $RootPath
    $summary['mcp'] = 'attempted'
}

# --- 최종 체크리스트 ---
Write-Host ""
Write-Host '========================================' -ForegroundColor Cyan
Write-Host '  설정 완료 체크리스트' -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ""

$finalChecks = @(
    @{ Label = 'Git'; Fn = { (Test-GitInstalled).Ok } },
    @{ Label = 'Python 3.13+'; Fn = { (Test-PythonInstalled).Ok } },
    @{ Label = 'Java 25+ (백엔드)'; Fn = { (Test-JavaInstalled).Ok } },
    @{ Label = 'Node 24+ (프론트)'; Fn = { (Test-NodeInstalled).Ok } },
    @{ Label = 'npm 11+'; Fn = { (Test-NpmInstalled).Ok } },
    @{ Label = "폴더 $($paths.Asak)"; Fn = { Test-Path $paths.Asak } },
    @{ Label = "폴더 $($paths.Front)"; Fn = { Test-Path $paths.Front } },
    @{ Label = "폴더 $($paths.Back)"; Fn = { Test-Path $paths.Back } },
    @{ Label = 'ASAK .git'; Fn = { Test-DirectoryHasGitRepo $paths.Asak } },
    @{ Label = 'ASAK-front .git'; Fn = { Test-DirectoryHasGitRepo $paths.Front } },
    @{ Label = 'ASAK-back .git'; Fn = { Test-DirectoryHasGitRepo $paths.Back } },
    @{ Label = 'phase1 .venv'; Fn = { Test-Path (Join-Path $venvPath 'Scripts\python.exe') } },
    @{ Label = '.env 파일'; Fn = { Test-Path $envFile } },
    @{ Label = '.cursor/mcp.json'; Fn = { Test-Path (Join-Path $repoRoot '.cursor\mcp.json') } }
)

foreach ($check in $finalChecks) {
    $ok = & $check.Fn
    $mark = if ($ok) { '[x]' } else { '[ ]' }
    $color = if ($ok) { 'Green' } else { 'DarkGray' }
    Write-Host "  $mark $($check.Label)" -ForegroundColor $color
}

Write-Host ""
Write-SetupBanner '다음 단계'
Write-Host @"
  1. git user.name / user.email 직접 설정 (setup-git.ps1 안내 참고)
  2. .env 에 NOTION_TOKEN, FIGMA_TOKEN 입력
  3. 저장소 clone 안 했다면: .\scripts\setup-git.ps1
  4. develop 브랜치 checkout 후 feature/... 작업 시작
  5. docs/GETTING_STARTED.md — 백엔드·프론트 실행

  수동 설치 상세: docs/INSTALL_WINDOWS.md
  MCP 상세: docs/MCP_SETUP.md

"@ -ForegroundColor White

if ($summary.Values -contains 'pending-restart') {
    Write-SetupWarn '일부 도구가 PATH 에 아직 반영되지 않았을 수 있습니다. PowerShell을 닫고 새로 연 뒤 스크립트를 다시 실행하세요.'
}

return $summary
