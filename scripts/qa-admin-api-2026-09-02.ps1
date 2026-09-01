# ASAK Admin API QA — 2026-09-02 (fixed assertions)
$ErrorActionPreference = "Continue"
$Base = "http://localhost:8080/api/admin"
$results = @()

function Test-Api {
  param(
    [string]$Id, [string]$Name, [string]$Method = "GET", [string]$Url,
    $Body = $null, [int[]]$ExpectStatus = @(200), [scriptblock]$Assert
  )
  $row = [ordered]@{ Id = $Id; Name = $Name; Pass = $false; Detail = "" }
  try {
    $params = @{ Uri = $Url; Method = $Method; ContentType = "application/json"; UseBasicParsing = $true; TimeoutSec = 15 }
    if ($Body -ne $null) { $params.Body = ($Body | ConvertTo-Json -Compress) }
    try {
      $resp = Invoke-WebRequest @params
      $status = $resp.StatusCode
      $json = $resp.Content | ConvertFrom-Json
    } catch {
      $status = [int]$_.Exception.Response.StatusCode.value__
      $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
      $json = $reader.ReadToEnd() | ConvertFrom-Json
    }
    if ($ExpectStatus -notcontains $status) { throw "HTTP $status expected $($ExpectStatus -join ',')" }
    if ($Assert) { & $Assert $json $status }
    elseif ($status -eq 200 -and -not $json.success) { throw "success=false $($json.code)" }
    $row.Pass = $true
    $row.Detail = "HTTP $status"
  } catch {
    $row.Detail = $_.Exception.Message
  }
  $script:results += [pscustomobject]$row
  Write-Host ("[{0}] {1} {2}" -f ($(if ($row.Pass) {"PASS"} else {"FAIL"})), $row.Id, $row.Name)
}

Write-Host "=== ASAK Admin API QA $(Get-Date -Format 'yyyy-MM-dd HH:mm') ===" -ForegroundColor Cyan

Test-Api -Id "TC-009a" -Name "Login 0001" -Method POST -Url "$Base/login" -Body @{ storeNumber = "0001" } -Assert {
  param($j) if (-not $j.success -or $j.data.approved -ne $true) { throw "not approved" }
}
Test-Api -Id "TC-009b" -Name "Login empty 400" -Method POST -Url "$Base/login" -Body @{ storeNumber = "" } -ExpectStatus @(400) -Assert {
  param($j) if ($j.code -ne "INVALID_STORE_NUMBER") { throw $j.code }
}
Test-Api -Id "TC-009c" -Name "Login wrong 400" -Method POST -Url "$Base/login" -Body @{ storeNumber = "9999" } -ExpectStatus @(400) -Assert {
  param($j) if ($j.code -ne "NOT_APPROVED_STORE_NUMBER") { throw $j.code }
}

Test-Api -Id "WBS-040" -Name "Dashboard KPI+delta" -Url "$Base/dashboard" -Assert {
  param($j)
  if ($j.data.kpis.Count -lt 1) { throw "no kpis" }
  if ($null -eq $j.data.kpis[0].delta) { throw "no delta" }
  if ($j.data.recentOrders.Count -lt 1) { throw "no recentOrders" }
}

$liveData = $null
Test-Api -Id "TC-014a" -Name "Live orders" -Url "$Base/orders/live" -Assert {
  param($j) $script:liveData = $j.data
}
$receivedOrder = $liveData.content | Where-Object { $_.orderStatus -eq "RECEIVED" } | Select-Object -First 1
if ($receivedOrder) {
  $oid = $receivedOrder.orderId
  Test-Api -Id "TC-014b" -Name "RECEIVED->PREPARING" -Method PATCH -Url "$Base/orders/$oid/PREPARING" -Assert { param($j) if (-not $j.success) { throw $j.code } }
  Test-Api -Id "TC-014c" -Name "PREPARING->COMPLETED" -Method PATCH -Url "$Base/orders/$oid/COMPLETED" -Assert { param($j) if (-not $j.success) { throw $j.code } }
} else {
  $results += [pscustomobject]@{ Id="TC-014b"; Name="Status transition"; Pass=$false; Detail="SKIP: no RECEIVED" }
  Write-Host "[SKIP] TC-014b no RECEIVED order"
}

Test-Api -Id "TC-006a" -Name "SoldOut ing 125 exists" -Url "$Base/soldOut" -Assert {
  param($j)
  $ing = $j.data.available | Where-Object { $_.targetType -eq "INGREDIENT" -and $_.targetId -eq 125 } | Select-Object -First 1
  if (-not $ing) { throw "ing 125 missing" }
  if ($null -eq $ing.affectedMenuCount) { throw "no affectedMenuCount" }
  $script:ing125 = $ing
}
if ($ing125) {
  $orig = [bool]$ing125.soldOut
  $toggle = -not $orig
  Test-Api -Id "TC-006b" -Name "SoldOut toggle ing125" -Method PATCH -Url "$Base/soldOut" -Body @{
    changes = @(@{ targetType = "INGREDIENT"; targetId = 125; isSoldOut = $toggle })
  } -Assert { param($j) if (-not $j.success) { throw $j.code } }
  Test-Api -Id "TC-006c" -Name "SoldOut restore ing125" -Method PATCH -Url "$Base/soldOut" -Body @{
    changes = @(@{ targetType = "INGREDIENT"; targetId = 125; isSoldOut = $orig })
  } -Assert { param($j) if (-not $j.success) { throw $j.code } }
}

Test-Api -Id "TC-012a" -Name "Payment methods list" -Url "$Base/paymentMethods" -Assert {
  param($j)
  if ($j.data.Count -lt 1) { throw "empty" }
  $card = $j.data | Where-Object { $_.methodCode -eq "CARD" } | Select-Object -First 1
  if (-not $card) { throw "no CARD" }
  $script:cardPm = $card
}
if ($cardPm) {
  $origActive = [bool]$cardPm.active
  Test-Api -Id "TC-012b" -Name "CARD OFF" -Method PATCH -Url "$Base/paymentMethods/$($cardPm.methodId)" -Body @{ active = $false; sortNo = $cardPm.sortNo } -Assert { param($j) if (-not $j.success) { throw $j.code } }
  Test-Api -Id "TC-012c" -Name "CARD restore" -Method PATCH -Url "$Base/paymentMethods/$($cardPm.methodId)" -Body @{ active = $origActive; sortNo = $cardPm.sortNo } -Assert { param($j) if (-not $j.success) { throw $j.code } }
}

foreach ($p in @("today","week","month")) {
  Test-Api -Id "TC-013-$p" -Name "Sales summary $p" -Url "$Base/sales/summary?period=$p" -Assert {
    param($j)
    if ($j.data.kpis.Count -lt 1) { throw "no kpis" }
    if ($j.data.availablePeriods.Count -lt 3) { throw "no periods" }
  }
}
Test-Api -Id "TC-013-daily" -Name "Sales daily Aug2026" -Url "$Base/sales/daily?from=2026-08-01&to=2026-08-31" -Assert {
  param($j) if ($j.data.dailySales.Count -lt 1) { throw "no dailySales" }
}
Test-Api -Id "TC-013-monthly" -Name "Sales monthly 2026-08" -Url "$Base/sales/monthly?year=2026&month=8" -Assert { param($j) if (-not $j.data) { throw "empty" } }
Test-Api -Id "TC-013-verify" -Name "Net sales 890300 on 8/28" -Url "$Base/sales/summary?startDate=2026-08-28&endDate=2026-08-28" -Assert {
  param($j)
  $net = [decimal]$j.data.kpis[0].value
  if ($net -ne 890300) { throw "net=$net expected 890300" }
}

Test-Api -Id "TC-010" -Name "Menus list" -Url "$Base/menus" -Assert {
  param($j)
  if ($j.data.content.Count -lt 1) { throw "empty" }
  $script:firstMenuId = $j.data.content[0].menuId
}
if ($firstMenuId) {
  Test-Api -Id "TC-011" -Name "Menu detail" -Url "$Base/menus/$firstMenuId" -Assert { param($j) if (-not $j.data.name) { throw "no name" } }
}

Test-Api -Id "SC-022" -Name "Order detail" -Url "$Base/orders?page=0&size=1" -Assert {
  param($j)
  $oid = $j.data.content[0].orderId
  $detail = (Invoke-WebRequest "$Base/orders/$oid" -UseBasicParsing).Content | ConvertFrom-Json
  if (-not $detail.data.items) { throw "no items" }
}

Test-Api -Id "TC-017" -Name "Refund reasons" -Url "$Base/refund-reasons" -Assert { param($j) if ($j.data.Count -lt 1) { throw "empty" } }

# Kiosk payment methods (customer API)
Test-Api -Id "TC-012-kiosk" -Name "Kiosk payment methods" -Url "http://localhost:8080/api/kiosk/payment-methods" -Assert {
  param($j)
  if ($j.data.Count -lt 1) { throw "empty kiosk methods" }
}

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
$pass = ($results | Where-Object Pass).Count
$fail = ($results | Where-Object { -not $_.Pass }).Count
Write-Host "PASS: $pass  FAIL/SKIP: $fail  TOTAL: $($results.Count)"
$out = "c:\ASAK-workspace\ASAK\docs\wiki\qa-admin-api-results-2026-09-02.json"
$results | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $out
$results | Format-Table -AutoSize
