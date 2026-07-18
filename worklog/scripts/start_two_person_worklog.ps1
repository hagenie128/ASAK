<#
.SYNOPSIS
이 스크립트는 이전 보조 도구입니다. 평소에는 실행하지 말고 `worklog/TEAM_WORKLOG.md`의 한 가지 프롬프트를 사용한다.

.EXAMPLE
  .\worklog\scripts\start_two_person_worklog.ps1 -Person 이하진
  .\worklog\scripts\start_two_person_worklog.ps1 -Person 김나연 -Date 2026-07-18
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('이하진', '김나연')]
    [string]$Person,

    [string]$Date = 'today'
)

$ErrorActionPreference = 'Stop'
$worklogDir = Split-Path -Parent $PSScriptRoot
$projectDir = Split-Path -Parent $worklogDir
$initDaily = Join-Path $PSScriptRoot 'init_daily.py'
$promptPath = Join-Path $worklogDir 'TEAM_WORKLOG.md'

Push-Location $projectDir
try {
    & python $initDaily --person $Person --date $Date --template auto
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    Pop-Location
}

Write-Host ''
Write-Host '일일 파일만 준비되었습니다.' -ForegroundColor Cyan
Write-Host "작성 기준과 프롬프트: $promptPath"
Write-Host "결과는 daily/$Person/ 에 기록합니다. 이슈는 팀 확인 후에만 실제 등록합니다."
