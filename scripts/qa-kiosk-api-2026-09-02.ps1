# ASAK Kiosk API QA — 2026-09-02 (코드 수정 없음, API E2E)
$ErrorActionPreference = "Continue"
$Kiosk = "http://localhost:8080/api/kiosk"
$Admin = "http://localhost:8080/api/admin"
$results = @()

function Test-Api {
  param(
    [string]$Id, [string]$Name, [string]$Method = "GET", [string]$Url,
    $Body = $null, [int[]]$ExpectStatus = @(200), [scriptblock]$Assert
  )
  $row = [ordered]@{ Id = $Id; Name = $Name; Pass = $false; Detail = "" }
  try {
    $params = @{ Uri = $Url; Method = $Method; ContentType = "application/json"; UseBasicParsing = $true; TimeoutSec = 20 }
    if ($Body -ne $null) { $params.Body = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Compress -Depth 10 } }
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
    elseif ($status -eq 200 -and $json.success -eq $false) { throw $json.code }
    $row.Pass = $true
    $row.Detail = "HTTP $status"
  } catch { $row.Detail = $_.Exception.Message }
  $script:results += [pscustomobject]$row
  Write-Host ("[{0}] {1} {2}" -f ($(if ($row.Pass) {"PASS"} else {"FAIL"})), $row.Id, $row.Name)
}

function Invoke-Json {
  param([string]$Method, [string]$Url, $Body)
  $params = @{ Uri = $Url; Method = $Method; ContentType = "application/json"; UseBasicParsing = $true; TimeoutSec = 20 }
  if ($Body) { $params.Body = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Compress -Depth 10 } }
  $r = Invoke-WebRequest @params
  return ($r.Content | ConvertFrom-Json)
}

Write-Host "=== ASAK Kiosk API QA $(Get-Date -Format 'yyyy-MM-dd HH:mm') ===" -ForegroundColor Cyan

# TC-003 / menu browse
Test-Api -Id "K-001" -Name "Categories" -Url "$Kiosk/categories" -Assert { param($j) if ($j.data.Count -lt 1) { throw "empty" } }
Test-Api -Id "K-002" -Name "MenuList" -Url "$Kiosk/menuList" -Assert {
  param($j)
  if ($j.data.menus.Count -lt 1) { throw "no menus" }
  $script:simpleMenuId = ($j.data.menus | Where-Object { $_.isSoldOut -eq $false } | Select-Object -First 1).menuId
}
Test-Api -Id "K-003" -Name "MenuDetail" -Url "$Kiosk/menuDetail/$simpleMenuId" -Assert { param($j) if (-not $j.data.name) { throw "no name" } }
Test-Api -Id "K-004" -Name "MenuDetail 404" -Url "$Kiosk/menuDetail/99999999" -ExpectStatus @(404) -Assert { param($j) if ($j.code -ne "MENU_NOT_FOUND") { throw $j.code } }

# TC-003 sold out MENU
Test-Api -Id "TC-003a" -Name "Menu soldOut reflects kiosk" -Url "$Kiosk/menuList" -Assert {
  param($j) { }
}
try {
  Invoke-WebRequest -Method PATCH -Uri "$Admin/soldOut" -ContentType "application/json" -Body "{`"changes`":[{`"targetType`":`"MENU`",`"targetId`":$simpleMenuId,`"isSoldOut`":true}]}" -UseBasicParsing | Out-Null
  $ml = (Invoke-WebRequest "$Kiosk/menuList" -UseBasicParsing).Content | ConvertFrom-Json
  $m = $ml.data.menus | Where-Object menuId -eq $simpleMenuId
  if ($m.isSoldOut -ne $true) { throw "menu not soldOut" }
  try {
    Invoke-WebRequest -Method POST -Uri "$Kiosk/cart/validate" -ContentType "application/json" -Body "{`"items`":[{`"clientCartItemId`":`"qa`",`"menuId`":$simpleMenuId,`"quantity`":1,`"optionItems`":[],`"excludedIngredientIds`":[]}]}" -UseBasicParsing | Out-Null
    throw "cart should fail"
  } catch {
    $reader = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream())
    $code = ($reader.ReadToEnd() | ConvertFrom-Json).code
    if ($code -ne "MENU_SOLD_OUT") { throw "got $code" }
  }
  $results += [pscustomobject]@{ Id = "TC-003a"; Name = "Menu soldOut kiosk"; Pass = $true; Detail = "isSoldOut + MENU_SOLD_OUT" }
  Write-Host "[PASS] TC-003a Menu soldOut kiosk"
} catch {
  $results += [pscustomobject]@{ Id = "TC-003a"; Name = "Menu soldOut kiosk"; Pass = $false; Detail = $_.Exception.Message }
  Write-Host "[FAIL] TC-003a $($_.Exception.Message)"
} finally {
  Invoke-WebRequest -Method PATCH -Uri "$Admin/soldOut" -ContentType "application/json" -Body "{`"changes`":[{`"targetType`":`"MENU`",`"targetId`":$simpleMenuId,`"isSoldOut`":false}]}" -UseBasicParsing | Out-Null
}

# Cart validate
Test-Api -Id "K-005" -Name "Cart validate simple" -Method POST -Url "$Kiosk/cart/validate" -Body @{
  items = @(@{ clientCartItemId = "qa-cart-1"; menuId = $simpleMenuId; quantity = 1; optionItems = @(); excludedIngredientIds = @() })
} -Assert { param($j) if ($j.data.totalAmount -lt 1) { throw "no total" } }
Test-Api -Id "K-006" -Name "Cart empty 400" -Method POST -Url "$Kiosk/cart/validate" -Body '{"items":[]}' -ExpectStatus @(400) -Assert { param($j) if ($j.code -ne "CART_EMPTY") { throw $j.code } }

# Required options negative
$complexMenuId = 768
Test-Api -Id "K-007" -Name "Missing required options" -Method POST -Url "$Kiosk/cart/validate" -Body @{
  items = @(@{ clientCartItemId = "qa-bad"; menuId = $complexMenuId; quantity = 1; optionItems = @(); excludedIngredientIds = @() })
} -ExpectStatus @(400) -Assert { param($j) if ($j.code -ne "INVALID_OPTION_SELECTION") { throw $j.code } }

# TC-001 EAT_IN / TAKE_OUT
$eatOrder = $null
Test-Api -Id "TC-001a" -Name "Order EAT_IN" -Method POST -Url "$Kiosk/orders" -Body @{
  orderType = "EAT_IN"; items = @(@{ menuId = $simpleMenuId; quantity = 1; optionItems = @(); excludedIngredientIds = @() })
} -Assert {
  param($j)
  $script:eatOrder = $j.data
  if (-not $j.data.orderNo -or $j.data.totalAmount -lt 1) { throw "bad order" }
}
$takeOrder = $null
Test-Api -Id "TC-001b" -Name "Order TAKE_OUT" -Method POST -Url "$Kiosk/orders" -Body @{
  orderType = "TAKE_OUT"; items = @(@{ menuId = $simpleMenuId; quantity = 1; optionItems = @(); excludedIngredientIds = @() })
} -Assert { param($j) $script:takeOrder = $j.data }
Test-Api -Id "TC-001c" -Name "TAKE_OUT stored in DB" -Url "$Admin/orders/$($takeOrder.orderId)" -Assert {
  param($j) if ($j.data.orderType -ne "TAKE_OUT") { throw "type=$($j.data.orderType)" }
}

# TC-002 payment flow
$key = [guid]::NewGuid().ToString()
Test-Api -Id "TC-002a" -Name "Payment CARD approve" -Method POST -Url "$Kiosk/payments" -Body @{
  orderId = $eatOrder.orderId; orderStatus = "RECEIVED"; paymentMethodCode = "CARD"; idempotencyKey = $key
} -Assert {
  param($j)
  if ($j.data.paymentStatus -ne "APPROVED") { throw $j.data.paymentStatus }
  if ($j.data.approvedAmount -ne $eatOrder.totalAmount) { throw "amount mismatch" }
  if (-not $j.data.orderNo) { throw "no orderNo" }
}
Test-Api -Id "TC-002b" -Name "Payment idempotency" -Method POST -Url "$Kiosk/payments" -Body @{
  orderId = $eatOrder.orderId; orderStatus = "RECEIVED"; paymentMethodCode = "CARD"; idempotencyKey = $key
} -Assert { param($j) if (-not $j.data.paymentId) { throw "no paymentId" } }
Test-Api -Id "TC-002c" -Name "Duplicate pay blocked" -Method POST -Url "$Kiosk/payments" -Body @{
  orderId = $eatOrder.orderId; orderStatus = "RECEIVED"; paymentMethodCode = "CARD"; idempotencyKey = ([guid]::NewGuid().ToString())
} -ExpectStatus @(409) -Assert { param($j) if ($j.code -ne "ORDER_STATUS_CONFLICT") { throw $j.code } }

# Payment methods
Test-Api -Id "K-010" -Name "Payment methods list" -Url "$Kiosk/payment-methods" -Assert {
  param($j) if ($j.data.methods.Count -lt 1) { throw "empty" }
}

# TC-012 admin sync (known issue)
try {
  $card = ((Invoke-WebRequest "$Admin/paymentMethods" -UseBasicParsing).Content | ConvertFrom-Json).data | Where-Object methodCode -eq "CARD" | Select-Object -First 1
  $orig = $card.active
  Invoke-WebRequest -Method PATCH -Uri "$Admin/paymentMethods/$($card.methodId)" -ContentType "application/json" -Body (@{ active = $false; sortNo = $card.sortNo } | ConvertTo-Json) -UseBasicParsing | Out-Null
  $kioskPm = ((Invoke-WebRequest "$Kiosk/payment-methods" -UseBasicParsing).Content | ConvertFrom-Json).data.methods
  $hasCard = @($kioskPm | Where-Object methodCode -eq "CARD").Count -gt 0
  Invoke-WebRequest -Method PATCH -Uri "$Admin/paymentMethods/$($card.methodId)" -ContentType "application/json" -Body (@{ active = $orig; sortNo = $card.sortNo } | ConvertTo-Json) -UseBasicParsing | Out-Null
  $results += [pscustomobject]@{ Id = "TC-012-kiosk"; Name = "Admin OFF hides CARD"; Pass = (-not $hasCard); Detail = if ($hasCard) { "CARD still visible" } else { "hidden" } }
  Write-Host ("[{0}] TC-012-kiosk Admin OFF hides CARD" -f $(if (-not $hasCard) {"PASS"} else {"FAIL"}))
} catch {
  $results += [pscustomobject]@{ Id = "TC-012-kiosk"; Name = "Admin OFF hides CARD"; Pass = $false; Detail = $_.Exception.Message }
}

# Receipt API
Test-Api -Id "K-011" -Name "Receipt print request" -Method POST -Url "$Kiosk/orders/$($eatOrder.orderId)/receipt-print" -Body @{
  eventType = "PRINT_RECEIPT_TEXT"; payload = "QA"; requestId = "qa-r1"
} -Assert { param($j) if (-not $j.success) { throw $j.code } }

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
$pass = ($results | Where-Object Pass).Count
$fail = ($results | Where-Object { -not $_.Pass }).Count
Write-Host "PASS: $pass  FAIL: $fail  TOTAL: $($results.Count)"
$out = "c:\ASAK-workspace\ASAK\docs\wiki\qa-kiosk-api-results-2026-09-02.json"
$results | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $out
$results | Format-Table -AutoSize
Write-Host "Saved: $out"
