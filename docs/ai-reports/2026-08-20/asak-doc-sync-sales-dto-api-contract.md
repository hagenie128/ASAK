# Admin Sales DTO/API 명세 동기화

- 기준 문서: `docs/planning/admin_sales_dashboard_dto_api_design.md`
- 대상: Dashboard, Sales Summary, Monthly Sales, Daily Sales
- 반영일: 2026-08-20

## 반영한 계약

| API | 요청 | data DTO |
| --- | --- | --- |
| `GET /api/admin/dashboard` | 없음 | `AdminDashboardResponse` |
| `GET /api/admin/sales/summary` | `period=today|week|month` | `SalesSummaryResponse` |
| `GET /api/admin/sales/monthly` | `year=YYYY` | `MonthlySalesResponse` |
| `GET /api/admin/sales/daily` | `from`, 선택 `to` | `DailySalesResponse` |
| `GET /api/admin/sales/daily/time-slots` | `date`, `intervalMinutes=30|60` | `List<DailySalesTimeSlotResponse>` |

## 처리 규칙

- 시간 슬롯은 영업시간 10:00~22:00 안에서만 0을 채운다.
- 30분 조회는 분 값 `0`/`30`, 60분 조회는 `0`으로 반환한다.
- `SALES_PERIOD_INVALID`, `SALES_DATE_INVALID`, `SALES_YEAR_INVALID`, `SALES_INTERVAL_INVALID`, `DATE_RANGE_INVALID` 오류 코드를 사용한다.
- API는 차트 렌더링 값(`fill`, `barHeight` 등)을 반환하지 않는다.

## 검증 범위

- `ASAK-back`의 `gradlew.bat compileJava --no-daemon` 성공.
- DB View 생성·변경·적용은 승인 범위에서 제외되어 수행하지 않았다. 따라서 실제 DB 연결 실행과 View 컬럼 호환성은 미검증이다.
