# ASAK filename convention checker (human docs only)
# Usage: pwsh -File asak-data/scripts/check-filename-convention.ps1
# Exit 0 = OK, 1 = violations

param(
    [string]$AsakRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
)

$ErrorActionPreference = 'Stop'
$workspaceRoot = Split-Path $AsakRoot -Parent

$allowedFixed = @(
    'README.md', 'START_HERE.md', 'IMPLEMENTATION_PLAN.md', 'STRUCTURE_GUIDE.md',
    'PROJECT_HUB.md', 'ROOT_FOLDER_MAP.md'
)

$kebabMd = '^(?:\d{2}-)?[a-z0-9]+(?:-[a-z0-9]+)*(?:-\d{4}-\d{2}-\d{2})?\.md$'

$scanDirs = @(
    (Join-Path $AsakRoot 'docs'),
    (Join-Path $workspaceRoot 'ASAK-Kiosk\docs'),
    (Join-Path $workspaceRoot 'ASAK-Admin\docs')
)

$extraFiles = @(
    (Join-Path $workspaceRoot 'ui-index.md')
)

$violations = @()

foreach ($dir in $scanDirs) {
    if (-not (Test-Path $dir)) { continue }
    Get-ChildItem -Path $dir -Recurse -Filter '*.md' -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch '\\_archive\\|product_bible\\|\\docs\\notion\\' } |
        ForEach-Object {
            $name = $_.Name
            if ($allowedFixed -contains $name) { return }
            if ($name -notmatch $kebabMd) {
                $violations += $_.FullName.Replace($workspaceRoot + '\', '')
            }
        }
}

foreach ($file in $extraFiles) {
    if (-not (Test-Path $file)) { continue }
    $name = Split-Path $file -Leaf
    if ($name -ne 'ui-index.md') {
        $violations += $name
    }
}

if ($violations.Count -eq 0) {
    Write-Host "OK: human docs match kebab-case ($($scanDirs.Count) doc roots + ui-index)."
    exit 0
}

Write-Host "Naming violations ($($violations.Count)):"
$violations | Sort-Object | ForEach-Object { Write-Host "  - $_" }
Write-Host ""
Write-Host "Rule: docs/document-naming-guide-2026-07-20.md"
exit 1
