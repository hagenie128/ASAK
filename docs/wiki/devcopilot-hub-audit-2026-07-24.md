# DevCopilot 허브 점검 (2026-07-24)

실DB `asak_db` 뷰 22개 · 허브 workspace 2 ERD/API 대조.

## 결과 요약

| 영역 | 상태 | 메모 |
|------|------|------|
| 뷰 이름 커버리지 | OK | 실DB 22개 = 허브 22개 이름 일치 (`vw_payment_result` 포함) |
| 핵심 뷰 컬럼 | OK (16/22) | 메뉴/옵션/품절/결제 등 신규 변경분 반영됨 |
| 주문·매출 일부 ERD | 부분 | 컬럼 중복·유령 테이블·`customer_count` 잔존 (아래) |
| API 명세 24개 | 보완 완료 | 깨진 제목·빈약한 응답 예시 5건 갱신 |

## ERD — 남은 이슈 (플랫폼)

삭제 API가 완전히 반영되지 않음. 같은 뷰가 2개로 보이거나 컬럼이 2번씩 남는 경우가 있음.

- 중복 테이블: `vw_order_item_full`, `vw_order_list_summary`, `vw_order_live`, `vw_order_status_summary`
- 컬럼 중복 표시: `vw_order_summary` 등
- 구필드 잔존: `vw_sales_daily` / `vw_sales_hourly` 의 `customer_count` (실DB에는 없음)

**사용 팁:** 동일 이름 뷰가 두 개면 컬럼이 실DB와 맞는 쪽(중복 없는 쪽)을 본다.  
정본 DDL: `ASAK-back/docs/view.sql` · 정의서: `docs/wiki/db-view-definition.md`

## API — 이번에 수정한 항목

| ID | 엔드포인트 | 조치 |
|----|------------|------|
| 211 | `POST /api/kiosk/payments` | 제목 깨짐 수정, `vw_payment_result` 응답 필드 명시 |
| 80 | `GET /api/kiosk/payment-methods` | 제목 깨짐 수정 |
| 72 | `GET /api/admin/orders/{orderId}` | `unitPrice` / `optionItems` / `excludedIngredients` 예시 보강 |
| 209 | `GET /api/kiosk/menuDetail/{menuId}` | optionGroups·ingredients·allergens 신 필드명 예시 |
| 208 | `GET /api/kiosk/menuList` | `categoryId` / `isOrderable` 반영 |

구 필드명(`optId`, `addPrice` 등)은 허브 API JSON에서 더 이상 검색되지 않음.

## 워크스페이스 지표 (참고)

- req_rate 0% · wbs_rate 6.5% · qa_rate 0% · trace_rate 88.3%
- 스크린 24 · API 24

## 재동기화

```powershell
$env:DEVCOPILOT_MCP_URL='(MCP URL)'
python asak-data/scripts/sync_devcopilot_views.py
```
