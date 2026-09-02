# ASAK QA 실행 보고 (2026-09-02)

> Status: **CURRENT**  
> 실행: Agent · 로컬 `localhost:8080` Backend + API 스크립트 + Admin dev proxy  
> 실행 보고: [Admin QA](qa-execution-report-2026-09-02.md) · **[Kiosk QA](qa-kiosk-execution-report-2026-09-02.md)**  
> 스크립트: `scripts/qa-admin-api-2026-09-02.ps1` · `scripts/qa-kiosk-api-2026-09-02.ps1`

## 결론

| 구분 | 결과 |
| --- | --- |
| Admin API (P0) | **22/24 PASS** — 로그인·주문상태·품절·결제수단·매출·메뉴 |
| Admin build | **PASS** (`npm run build`) |
| Kiosk API E2E | **17/18 PASS** | [Kiosk QA 보고](qa-kiosk-execution-report-2026-09-02.md) |
| Kiosk build | **PASS** | `npm install` 후 `npm run build` |
| Kiosk dev/proxy | **PASS** | `5175` UI·proxy |
| Admin UI 브라우저 클릭 | **미실행** | |

**시연 가능:** Admin API 기준 P0는 대부분 통과.  
**주의:** 결제수단 Admin→Kiosk 반영 **미동작**, 품절 `affectedMenuCount` 전부 0. READY 취소는 **409 차단**(로컬 코드 2026-09-02, 당일 QA는 500이었음).

---

## P0 TC 결과

| TC | 결과 | 근거 |
| --- | --- | --- |
| **TC-009** 로그인 | **PASS** | `0001`→200 approved / 빈값·9999→400 |
| **TC-014** 주문 상태 | **PASS** | Live 조회, RECEIVED→PREPARING→COMPLETED PATCH 200 |
| **TC-006** 품절 | **PASS** △ | ing125 PATCH 토글·원복 OK · `affectedMenuCount=0` · Kiosk menuList 변화 없음 |
| **TC-012** 결제수단 Admin | **PASS** | GET 4건, CARD OFF/ON PATCH 200 |
| **TC-012** Kiosk 반영 | **FAIL** | Admin CARD OFF 후에도 `/api/kiosk/payment-methods`에 CARD 노출 (methodId 불일치: Admin 10828 vs Kiosk 19) |
| **TC-013** 매출 | **PASS** △ | today/week/month KPI, monthly 2026-08, **8/28 순매출 890,300** 일치 · `/sales/daily`는 응답 `rows[]` 정상(200)이나 QA 스크립트가 `dailySales` 필드를 기대해 TC-013-daily만 FAIL |
| **TC-001~002** Kiosk 주문 | **PASS** | API E2E: EAT_IN/TAKE_OUT·CARD 결제·idempotency·409 |
| **TC-003** Kiosk 품절 | **PASS** | MENU·OPTION_ITEM 반영 · INGREDIENT ing125는 FAIL |
| **TC-010~011** 메뉴 | **PASS** | 목록(content)·상세 name 필드 |
| **SC-022** 주문 상세 | **PASS** | items 배열 존재 |
| **WBS-040** 대시보드 | **PASS** | kpis·delta·recentOrders |
| **TC-017** 환불 | **BLOCKED** | 사유 목록 OK · 실주문 환불은 DB 훼손 방지로 스킵 |

---

## 추가 검증

| 항목 | 결과 | 비고 |
| --- | --- | --- |
| APPROVED 주문 취소 | **PASS** | orderId 52006 → HTTP **409** (차단 정상) |
| READY 주문 취소 | **PASS** | 당일 QA 500(NPE) → Admin 코드 **409 `ORDER_CANCEL_NOT_ALLOWED`**. **HTTP 재검증 2026-09-02** (orderId=51984) |
| Admin Vite proxy | **PASS** | `5173/api/admin/login` → 200 |
| Kiosk menuList | **PASS** | 72건 조회 |
| 품절→Kiosk | **FAIL** △ | ing125 soldOut 후 menuList soldOut/orderable 변화 0건 |
| Kiosk build (9/2 초기) | **FAIL** | `vite-plugin-pwa` 누락 |
| Kiosk build (npm install 후) | **PASS** | |

---

## 시연 시 권장

1. **결제수단:** Admin에서 CARD 끄기 → Kiosk에 **반영 안 됨** → 시연에서 **Admin만** 보여 주거나 「연동 예정」으로 설명
2. **품절:** ing125는 **영향 메뉴 0개** — UI에서 `affectedMenuCount` 표시만 설명하거나, 영향 있는 재료로 교체 검토
3. **READY 취소:** **취소 불가** — 409 `ORDER_CANCEL_NOT_ALLOWED` (시연에서 시도하지 않음)
4. **환불:** 사전 준비 주문·9/1 캡처 Plan B

---

## 재실행

```powershell
powershell -File c:\ASAK-workspace\ASAK\scripts\qa-admin-api-2026-09-02.ps1
```

Backend `8080` 실행 필수. 품절·결제수단 테스트는 **자동 원복** 포함.
