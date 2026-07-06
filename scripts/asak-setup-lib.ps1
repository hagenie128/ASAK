# ASAK setup 공통 헬퍼 (dot-source 전용)
#Requires -Version 5.1

function Write-SetupBanner {
    param([string]$Title)
    Write-Host ""
    Write-Host "=== $Title ===" -ForegroundColor Cyan
}

function Write-SetupOk {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor Green
}

function Write-SetupSkip {
    param([string]$Message)
    Write-Host "  [SKIP] $Message" -ForegroundColor Yellow
}

function Write-SetupWarn {
    param([string]$Message)
    Write-Host "  [WARN] $Message" -ForegroundColor DarkYellow
}

function Write-SetupFail {
    param([string]$Message)
    Write-Host "  [MISS] $Message" -ForegroundColor Red
}

function Write-SetupInfo {
    param([string]$Message)
    Write-Host "  [INFO] $Message" -ForegroundColor Gray
}

function Get-CommandVersionOutput {
    param(
        [string]$Command,
        [string[]]$Arguments = @('--version')
    )
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        return $null
    }
    try {
        $output = & $Command @Arguments 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
            return $null
        }
        return $output.Trim()
    }
    catch {
        return $null
    }
}

function ConvertTo-VersionTuple {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return $null }
    $match = [regex]::Match($Text, '(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?')
    if (-not $match.Success) { return $null }
    $parts = @()
    foreach ($i in 1..4) {
        if ($match.Groups[$i].Success -and $match.Groups[$i].Value) {
            $parts += [int]$match.Groups[$i].Value
        }
        else {
            $parts += 0
        }
    }
    return ,$parts
}

function Test-VersionMeetsMinimum {
    param(
        [string]$ActualText,
        [int[]]$Minimum
    )
    $actual = ConvertTo-VersionTuple $ActualText
    if (-not $actual) { return $false }
    for ($i = 0; $i -lt $Minimum.Count; $i++) {
        $a = if ($i -lt $actual.Count) { $actual[$i] } else { 0 }
        $m = $Minimum[$i]
        if ($a -gt $m) { return $true }
        if ($a -lt $m) { return $false }
    }
    return $true
}

function Get-AsakRepoPaths {
    param([string]$RootPath = 'C:\ASAK')
    $parent = Split-Path -Parent $RootPath
    $baseName = Split-Path -Leaf $RootPath
    return [ordered]@{
        Asak  = $RootPath
        Front = Join-Path $parent "$baseName-front"
        Back  = Join-Path $parent "$baseName-back"
    }
}

function Get-AsakScriptRoot {
    $libDir = Split-Path -Parent $PSCommandPath
    if (Test-Path (Join-Path $libDir 'setup-windows.ps1')) {
        return $libDir
    }
    return (Get-Location).Path
}

function Get-AsakRepoRoot {
    param([string]$StartPath)
    $scriptsDir = if ($StartPath) { $StartPath } else { Get-AsakScriptRoot }
    $candidate = Split-Path -Parent $scriptsDir
    if (Test-Path (Join-Path $candidate 'data-pipeline\phase1\requirements.txt')) {
        return (Resolve-Path $candidate).Path
    }
    if (Test-Path (Join-Path $candidate '.git')) {
        return (Resolve-Path $candidate).Path
    }
    return $candidate
}

function Test-CommandAvailable {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-PackageInstall {
    param(
        [string]$ToolName,
        [string]$WingetId,
        [string]$ChocoId,
        [string]$ManualUrl
    )
    if (Test-CommandAvailable 'winget') {
        Write-SetupInfo "winget으로 $ToolName 설치 시도: $WingetId"
        winget install --id $WingetId -e --accept-source-agreements --accept-package-agreements 2>&1 | Out-Host
        if ($LASTEXITCODE -eq 0) {
            Write-SetupOk "$ToolName winget 설치 완료 (또는 이미 설치됨)"
            return $true
        }
        Write-SetupWarn "winget 설치 실패 (exit $LASTEXITCODE). 수동 설치를 시도하세요."
    }
    elseif (Test-CommandAvailable 'choco') {
        Write-SetupInfo "choco로 $ToolName 설치 시도: $ChocoId"
        choco install $ChocoId -y 2>&1 | Out-Host
        if ($LASTEXITCODE -eq 0) {
            Write-SetupOk "$ToolName choco 설치 완료 (또는 이미 설치됨)"
            return $true
        }
        Write-SetupWarn "choco 설치 실패 (exit $LASTEXITCODE). 수동 설치를 시도하세요."
    }
    else {
        Write-SetupWarn "winget/choco 없음 — 수동 설치 필요"
    }
    if ($ManualUrl) {
        Write-SetupInfo "수동 설치: $ManualUrl"
    }
    return $false
}

function Test-GitInstalled {
    $out = Get-CommandVersionOutput 'git'
    if (-not $out) { return @{ Ok = $false; Version = $null; Detail = $null } }
    $ok = Test-VersionMeetsMinimum $out @(2, 40)
    return @{ Ok = $ok; Version = $out; Detail = $out }
}

function Test-PythonInstalled {
    $commands = @(
        @{ Cmd = 'python'; Args = @('--version') },
        @{ Cmd = 'py'; Args = @('-3.13', '--version') }
    )
    foreach ($c in $commands) {
        $out = Get-CommandVersionOutput $c.Cmd $c.Args
        if ($out -and (Test-VersionMeetsMinimum $out @(3, 13))) {
            return @{ Ok = $true; Version = $out; Launcher = $c.Cmd }
        }
    }
    return @{ Ok = $false; Version = $null; Launcher = $null }
}

function Test-JavaInstalled {
    $out = Get-CommandVersionOutput 'java'
    if (-not $out) { return @{ Ok = $false; Version = $null; Detail = $null } }
    $ok = Test-VersionMeetsMinimum $out @(25)
    return @{ Ok = $ok; Version = $out; Detail = ($out -split "`n")[0] }
}

function Test-NodeInstalled {
    $out = Get-CommandVersionOutput 'node'
    if (-not $out) { return @{ Ok = $false; Version = $null; Detail = $null } }
    $ok = Test-VersionMeetsMinimum $out @(24)
    return @{ Ok = $ok; Version = $out; Detail = $out }
}

function Test-NpmInstalled {
    $out = Get-CommandVersionOutput 'npm'
    if (-not $out) { return @{ Ok = $false; Version = $null; Detail = $null } }
    $ok = Test-VersionMeetsMinimum $out @(11)
    return @{ Ok = $ok; Version = $out; Detail = ($out -split "`n")[0] }
}

function Get-PythonInvoker {
    $py = Test-PythonInstalled
    if (-not $py.Ok) { return $null }
    if ($py.Launcher -eq 'py') {
        return @{ Exe = 'py'; Args = @('-3.13') }
    }
    return @{ Exe = 'python'; Args = @() }
}

function Test-DirectoryHasGitRepo {
    param([string]$Path)
    return Test-Path (Join-Path $Path '.git')
}

function Test-DirectoryIsEmptyOrMissing {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return $true }
    $items = Get-ChildItem -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    return ($null -eq $items -or $items.Count -eq 0)
}
