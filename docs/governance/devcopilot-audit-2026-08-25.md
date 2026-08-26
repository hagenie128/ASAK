# DevCopilot 허브 점검 (2026-08-25)

관리자 결제수단/로그인/환불 문서 갱신 후 workspace 2 API 카드 대조.

## 결과 요약

| 카드 | 상태 | 조치 |
|---|---|---|
| API-015 GET `/api/admin/paymentMethods` | 허브가 "Controller 메서드 없음"으로 정체됨 (2026-08-18 기준) | 실제 코드 재확인 후 구현 상태·응답 shape(`data`가 배열, `{methods:[...]}` 아님) 갱신 |
| API-016 PATCH `/api/admin/paymentMethods/{paymentMethodId}` | 응답 필드명 `isActive` 오기, path variable명 `{methodId}` 오기 | `active`/`sortNo`로 필드명 수정, path variable을 실제 `{paymentMethodId}`로 수정, 성공 응답 `data:null`로 수정 |
| 로그인 `POST /api/admin/login` | Hub에 카드 없음 | 새로 만들지 않음 — 정본 API 번호 미정(2026-08-19 방침 유지). 계약(매장 번호 하드코드, 단순 승인 플래그)은 로컬 `rest-api-spec.md`에만 기록 |
| 환불 `PATCH /api/admin/orders/{orderId}/refund` | Hub에 카드 없음 | 동일 — 새로 만들지 않음. 정책(TODO-001) 확정 내용은 로컬 문서에만 기록 |

## 확인 방법

DevCopilot MCP HTTP transport로 직접 조회·수정. `get_api_specs(workspace_id=2)` → 결제수단 관련 3개 카드(API-014/015/016) 확인 → 실제 Controller/DTO(`AdminPaymentMethodController`, `UpdatePaymentMethodRequest`, `AdminPaymentMethodResponse`) 재확인 → 불일치 2건(API-015/016)을 `update_api_spec`으로 수정.

`sync_current_docs_devcopilot.py`(wiki 페이지 push용)는 `--push` 없이 dry-run만 실행. 대상 8개 중 7개는 로컬 소스 파일 자체가 과거 문서 정리로 삭제되어 SKIP됨(`docs/notion/README.md` 참고). "화면 설계" 1건만 로컬에 존재하나 허브 쪽 분량이 로컬의 약 5배로 커서(로컬 2846자 / 허브 13750자) **push하지 않음** — 덮어쓰면 허브 쪽 내용이 유실될 위험.

## 남은 작업

- 로그인·환불 API 번호는 여전히 미정 — TODO-027/038 실제 구현 후 정본 번호를 부여하고 그때 Hub 카드를 새로 만든다.
- "화면 설계" wiki 페이지는 로컬 파일이 허브보다 훨씬 부실 — 로컬 파일을 허브 기준으로 보강할지, 아니면 로컬을 정본으로 삼고 허브를 갱신할지 별도 결정 필요.
- `docs/notion/`의 6개 소스 파일(00/02/03/06/07/09)이 없어 `sync_current_docs_devcopilot.py`의 나머지 타겟은 계속 SKIP됨 — 필요해지면 `docs/wiki/*.md` 기준으로 재생성.

## 재실행

```powershell
$env:DEVCOPILOT_TOKEN = "..."
python asak-data/scripts/sync_current_docs_devcopilot.py          # dry-run diff
python asak-data/scripts/sync_current_docs_devcopilot.py --push   # 실제 반영
```

API 카드 조회/수정은 `$env:DEVCOPILOT_MCP_URL`로 MCP HTTP transport 직접 호출 (`sync_devcopilot_views.py`의 `McpClient` 패턴 재사용 가능).
