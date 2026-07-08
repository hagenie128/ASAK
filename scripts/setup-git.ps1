#Requires -Version 5.1
<#
.SYNOPSIS
  ASAK Git 저장소 클론 및 브랜치 안내 (idempotent)

.DESCRIPTION
  - C:\ASAK, C:\ASAK-front, C:\ASAK-back 폴더 생성
  - 비어 있는 폴더에만 git clone (기존 저장소는 건너뜀)
  - git config 는 절대 수정하지 않음 — 사용자 이름/이메일은 안내만 출력

.PARAMETER RootPath
  통합 저장소 경로 (기본: C:\ASAK). front/back 는 같은 부모 아래 {이름}-front, {이름}-back

.PARAMETER Force
  폴더가 비어 있지 않아도 clone 시도 (권장하지 않음)

.EXAMPLE
  .\scripts\setup-git.ps1
  .\scripts\setup-git.ps1 -RootPath D:\work\ASAK
#>
[CmdletBinding()]
param(
    [string]$RootPath = 'C:\ASAK',
    [switch]$Force
)

$ErrorActionPreference = 'Continue'
$libPath = Join-Path $PSScriptRoot 'asak-setup-lib.ps1'
. $libPath

$repos = @(
    @{
        Name = 'ASAK'
        Url  = 'https://github.com/hagenie128/ASAK.git'
        Key  = 'Asak'
    },
    @{
        Name = 'ASAK-front'
        Url  = 'https://github.com/hagenie128/ASAK-front.git'
        Key  = 'Front'
    },
    @{
        Name = 'ASAK-back'
        Url  = 'https://github.com/hagenie128/ASAK-back.git'
        Key  = 'Back'
    }
)

$paths = Get-AsakRepoPaths -RootPath $RootPath
$results = @{}

Write-SetupBanner 'ASAK Git 설정'

# 폴더 생성
foreach ($key in @('Asak', 'Front', 'Back')) {
    $p = $paths[$key]
    if (-not (Test-Path $p)) {
        New-Item -ItemType Directory -Force -Path $p | Out-Null
        Write-SetupOk "폴더 생성: $p"
    }
    else {
        Write-SetupSkip "폴더 이미 존재: $p"
    }
}

$git = Test-GitInstalled
if (-not $git.Ok) {
    Write-SetupFail 'Git이 설치되지 않았거나 버전이 낮습니다. setup-windows.ps1 을 먼저 실행하세요.'
    Write-SetupInfo '수동: https://git-scm.com/download/win'
    exit 1
}

Write-SetupOk "Git 사용 가능: $($git.Detail)"

foreach ($repo in $repos) {
    $dest = $paths[$repo.Key]
    $hasGit = Test-DirectoryHasGitRepo $dest
    $isEmpty = Test-DirectoryIsEmptyOrMissing $dest

    if ($hasGit) {
        Write-SetupSkip "$($repo.Name) — 이미 Git 저장소: $dest"
        $results[$repo.Name] = 'skipped-existing'
        continue
    }

    if (-not $isEmpty -and -not $Force) {
        Write-SetupWarn "$($repo.Name) — 폴더가 비어 있지 않아 clone 건너뜀: $dest"
        Write-SetupInfo '비어 있는 폴더에서만 자동 clone 합니다. -Force 로 재시도 가능 (주의).'
        $results[$repo.Name] = 'skipped-not-empty'
        continue
    }

    Write-SetupInfo "$($repo.Name) clone: $($repo.Url) -> $dest"
    & git clone $repo.Url $dest 2>&1 | Out-Host
    if ($LASTEXITCODE -eq 0 -and (Test-DirectoryHasGitRepo $dest)) {
        Write-SetupOk "$($repo.Name) clone 완료"
        $results[$repo.Name] = 'cloned'
    }
    else {
        Write-SetupFail "$($repo.Name) clone 실패"
        $results[$repo.Name] = 'failed'
    }
}

Write-Host ""
Write-SetupBanner 'Git 사용자 설정 (직접 입력 필요)'
Write-Host @"

  이 스크립트는 git config 를 변경하지 않습니다.
  아래 명령을 PowerShell에서 직접 실행하세요 (본인 이름·이메일로 교체):

    git config --global user.name "홍길동"
    git config --global user.email "you@example.com"

  확인:

    git config --global user.name
    git config --global user.email

"@ -ForegroundColor White

Write-SetupBanner 'develop 브랜치 (작업 시작 전)'
Write-Host @"

  각 저장소에서 팀 작업 브랜치로 전환:

    cd $($paths.Asak)
    git fetch origin
    git checkout develop

    cd $($paths.Front)
    git fetch origin
    git checkout develop

    cd $($paths.Back)
    git fetch origin
    git checkout develop

  기능 작업은 develop 에서 feature/기능명 브랜치를 만드세요.
  상세: docs/guides/01-team-setup.md

"@ -ForegroundColor White

Write-SetupBanner 'Git 요약'
foreach ($repo in $repos) {
    $dest = $paths[$repo.Key]
    $status = $results[$repo.Name]
    $gitOk = Test-DirectoryHasGitRepo $dest
    $label = if ($gitOk) { '저장소 OK' } else { '저장소 없음' }
    Write-Host "  $($repo.Name): $label ($status)" -ForegroundColor $(if ($gitOk) { 'Green' } else { 'Yellow' })
}

return $results
