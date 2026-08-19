# 문서 동기화: Sales API / DTO 패키지 리팩터링

- 날짜: 2026-08-19
- 대상 저장소: ASAK-back (feat/admin-monthly-sales-endpoint, 6755aa8)
- 기준 커밋: 79c4581 (main)

## 확인한 코드

| 파일 | 변경 내용 |
|---|---|
| `AdminSalesController.java` | `GET /sales/summary`, `GET /sales/monthly` 엔드포인트 |
| `AdminSalesService.java` | `DailySalesSummaryItemResponse`, `HourlySalesSummaryItemResponse` 반환 |
| `AdminSalesMapper.java` | 리턴 타입 SalesSummaryResponse → DailySalesSummaryItemResponse 등 |
| `AdminSalesMapper.xml` | 뷰 이름 수정 (vw_sales_summary→vw_sales_daily, vw_daily_top_menu→vw_top_menu_daily 등) |
| `ErrorCode.java` | 57개 enum 상수 (매출 관련 6개 추가, 중복 1개 삭제) |
| `dto/request/*` | menus/orders/item 서브패키지로 이동 완료, 구 패키지에 파일 없음 |
| `dto/response/*` | menus/orders/item/sales 서브패키지로 이동 완료, 구 패키지에 파일 없음 |

## 갱신한 문서

### 1. `ASAK/docs/implementation-guide/04-api-db-implementation.md`

| 항목 | 변경 전 | 변경 후 | 근거 |
|---|---|---|---|
| 빈 Mapper | 4개 (AdminPaymentMethod, AdminSoldOut, AdminStats, DeviceEvent) | 3개 (AdminPaymentMethod, AdminSoldOut, DeviceEvent) | AdminSalesMapper.xml에 SQL 4문 구현 |
| SQL 보유 Mapper | 6개(66문) | 7개(70문) | AdminSalesMapper 4문 추가 |
| ErrorCode 개수 | 51개 | 57개 | 실제 enum 상수 수 |
| HTTP status 분포 | CONFLICT 17, NOT_FOUND 13, BAD_REQUEST 12, ISE 11 | CONFLICT 17, BAD_REQUEST 15, NOT_FOUND 14, ISE 11 | 실제 분포 |

### 2. `ASAK/docs/planning/admin-todo-2026-08-05.md`

| 항목 | 변경 전 | 변경 후 |
|---|---|---|
| 39행 매출 영역 클래스명 | AdminStatsController·Service·Mapper | AdminSalesController·Service·Mapper |
| 048행 위치 | AdminStatsController | AdminSalesController |
| 056행 위치 | AdminStatsController | AdminSalesController |

## 남은 불일치 (결정 필요)

| # | 문서 | 내용 | 상태 |
|---|---|---|---|
| 1 | wbs.md, admin-todo-checklist | API-017~020 번호가 Kiosk 확장 기능(접근성, 멤버십, 영수증)과 Admin 매출에서 이중 사용 | 결정 필요 |
| 2 | 03-admin-implementation.md SCR-019 | 응답 구조가 복합 객체(period, kpis, dailyTrend 등)로 기재되어 있으나 실제는 `List<DailySalesSummaryItemResponse>` | 구현 불일치 |
| 3 | admin-api-contract.md | 매출 API를 mock으로 표기하나 백엔드에 실 엔드포인트 존재 (스텁 포함) | 구현됨 / 문서 미갱신 |

## 수정하지 않은 범위

- 소스코드 (스킬 규칙에 따라 수정 금지)
- API 번호 재할당 (사용자 결정 필요)
- SCR-019 응답 구조 변경 (기획 의도 확인 필요)
- admin-api-contract.md (Admin 프론트 담당 영역)
- ASAK-back/docs/implementation-guide/04-api-db-implementation.md (이미 최신 상태)
