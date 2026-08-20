# Admin Dashboard DTO 분리 계획

> 상태: 설계만 작성. 소스 수정·DB 적용·브랜치 병합은 하지 않음.
>
> 기준 브랜치: `ASAK-back/feat/admin-monthly-sales-endpoint`

## 목적

`AdminDashboardResponse` 한 파일 안에 있는 6개 내부 DTO를 역할별 파일로 분리한다.

- `AdminDashboardResponse`는 대시보드 전체 응답을 묶는 역할만 한다.
- 카드·목록·차트 행의 필드는 각 DTO가 맡는다.
- MyBatis의 내부 클래스 경로(`$RecentOrder`, `$CountSummary`) 의존을 제거한다.

## 수정 대상

| 순서 | 파일 | 수정 내용 |
| --- | --- | --- |
| 1 | `dto/response/dashboard/DashboardKpiResponse.java` | `label`, `value` 분리 |
| 2 | `dto/response/dashboard/DashboardRecentOrderResponse.java` | 최근 주문 1행 분리 |
| 3 | `dto/response/dashboard/DashboardStatusSummaryResponse.java` | 주문 상태별 개수 1행 분리 |
| 4 | `dto/response/dashboard/DashboardOrderTypeResponse.java` | `eatIn`, `takeOut` 분리 |
| 5 | `dto/response/dashboard/DashboardInventoryAlertResponse.java` | 품절 알림 1행 분리 |
| 6 | `dto/response/dashboard/DashboardWeeklySalesResponse.java` | 주간 매출 차트 1행 분리 |
| 7 | `AdminDashboardResponse.java` | 내부 클래스 삭제, 위 DTO 타입으로 필드 변경 |
| 8 | `AdminSalesMapper.java` | `RecentOrder`, `CountSummary` 반환 타입을 새 DTO로 변경 |
| 9 | `AdminSalesMapper.xml` | 내부 클래스 경로 대신 새 DTO의 전체 경로를 `resultType`에 사용 |
| 10 | `AdminSalesService.java` | builder 호출과 helper 메서드 반환 타입을 새 DTO로 변경 |

## 변경 뒤 구조

```text
AdminDashboardResponse
 ├─ List<DashboardKpiResponse> kpis
 ├─ List<DashboardRecentOrderResponse> recentOrders
 ├─ List<DashboardStatusSummaryResponse> statusSummary
 ├─ DashboardOrderTypeResponse orderTypeSummary
 ├─ List<DashboardInventoryAlertResponse> inventoryAlerts
 └─ List<DashboardWeeklySalesResponse> weeklySales
```

## 구현 순서

1. 새 DTO 6개를 생성한다. 모두 `@Data`, `@Builder`를 사용한다.
2. `AdminDashboardResponse`의 내부 클래스를 제거하고 import와 필드 타입을 교체한다.
3. `AdminSalesMapper`와 XML의 최근 주문·상태 요약 result type을 새 DTO로 바꾼다.
4. `AdminSalesService`의 `dashboardKpi`, `inventoryAlert`, 주간 매출 builder를 새 DTO로 바꾼다.
5. `compileJava`로 타입·MyBatis XML 참조 오류를 확인한다.
6. 서버 실행 뒤 `GET /api/admin/dashboard` 응답 필드명이 기존과 같은지 확인한다.

## 변경하지 않는 것

- API URL과 JSON 필드명
- DB View·테이블·SQL 컬럼
- 매출 30/60분 집계 로직
- RTOS 흐름

## 주의

- DTO 분리는 코드 가독성 개선이다. 대시보드 API가 실제 DB에서 동작했다는 증거는 아니다.
- 현재 대시보드 구현은 feature 브랜치에 있으므로, `main` 병합 전에는 현재 작업 폴더에서 이 DTO가 보이지 않을 수 있다.
