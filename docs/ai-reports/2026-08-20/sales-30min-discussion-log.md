# 매출 시간대 30분 집계 대화 기록

- 기록 시작: 2026-08-20 (Asia/Seoul)
- 범위: Admin 일별 매출(SCR-021) 시간대 집계와 빈 구간 처리
- 상태: 검토 완료 · 구현 미승인
- 관련 화면: `/sales/daily` / Screen ID `SCR-021`
- Figma 기준: 문서상 Node `39:7894` (최신 Frame 실제 접근은 미확인)

## 2026-08-20 — 제안 및 검토 결과

### 사용자 제안

1. DB View는 실제 매출이 있는 날짜·시간만 집계한다.
2. 날짜·영업시간 내 데이터가 없는 구간은 Service에서 0으로 채운다.
3. 시간 집계의 최소 단위를 30분으로 통일한다.
4. API의 `intervalMinutes` 값은 `30` 또는 `60`만 허용한다.
5. 60분 조회는 30분 View의 두 버킷을 Mapper에서 합산한다.
6. 미래 날짜와 아직 완료되지 않은 오늘의 미래 시간 버킷은 반환하지 않는다.

### 확인된 현재 상태

| 구분 | 현재 상태 | 영향 |
|---|---|---|
| DB View | `vw_sales_hourly`만 존재하며 정시 단위 집계 | `vw_sales_30min` 신설 또는 전환 설계 필요 |
| Backend DTO | `HourlySalesSummaryItemResponse`에 `salesMinute`가 이미 추가된 미커밋 변경 존재 | Mapper/View가 아직 해당 컬럼을 반환하지 않아 불일치 |
| Mapper | `getSalesHourly(LocalDate)`가 `vw_sales_hourly`를 직접 조회 | interval 파라미터와 30/60분 분기 없음 |
| Service | 월별 매출만 0-fill 구현됨 | 일별·시간대 0-fill은 아직 없음 |
| Controller | `/api/admin/sales/daily` 미구현 | 시간대 API 계약부터 확정 필요 |
| Admin 화면 | mock `{ hour, orderCount, totalAmount, avgAmount }` 및 1시간 표기 사용 | `salesMinute`와 30분 차트 축 처리 필요 |
| 영업시간 | 코드·문서에서 정본 설정을 찾지 못함 | `09:30~21:00` 하드코딩 전 정책 위치 확정 필요 |

### 합의 가능한 설계 원칙

```text
vw_sales_daily / vw_sales_30min
  실제 주문·결제 집계만 담당

AdminSalesMapper
  intervalMinutes=30: 30분 버킷 조회
  intervalMinutes=60: 같은 시간의 30분 버킷 2개 합산

AdminSalesService
  날짜 범위 및 영업시간의 누락 슬롯만 0 DTO로 보완
  미래 날짜·미완료 미래 슬롯은 생성하지 않음
```

### 매출 계산 규칙

- 매출 날짜·시간은 원 승인 시각인 `payment.paid_at` 기준이다.
- 승인 후 취소·환불된 거래도 gross sales에는 포함한다.
- `canceledAmount`는 취소·환불된 승인 결제 금액만 합산한다.
- `netSalesAmount = grossSalesAmount - canceledAmount`이며 음수가 되어서는 안 된다.
- 미결제 취소는 취소 건수에만 포함될 수 있고 매출 금액에는 포함하지 않는다.

### 구현 전 결정 필요 항목

1. 영업시간의 정본 위치와 값: 매장별 설정인지, 프로젝트 고정값인지
2. 시간 버킷 경계: `HH:00`/`HH:30` 고정으로 확정할지
3. 오늘의 처리: 진행 중인 30분 버킷을 제외할지 포함할지
4. API 응답 형태: 기존 `salesHour`, `salesMinute` 유지 여부와 `intervalMinutes`의 위치
5. `vw_sales_hourly`의 유지 기간 및 기존 소비처 전환 범위
6. Frontend까지 함께 전환할지, Backend·DB 계약만 먼저 확정할지

### 2026-08-20 — 사용자 확정 정책

| # | 결정 항목 | 확정 내용 |
|---|---|---|
| 1 | 영업시간 | 프로젝트 전체 고정값 `10:00~22:00`으로 관리한다. 종료 시각 `22:00`은 슬롯 시작 시각으로 포함하지 않는다. |
| 2 | 시간 버킷 경계 | `HH:00` / `HH:30` 고정 기준을 사용한다. |
| 3 | 오늘 진행 중 버킷 | 포함한다. 예: 현재가 `11:27`이면 `11:00` 버킷을 응답에 포함한다. 미래 버킷은 제외한다. |
| 4 | API 시간 필드 | `salesMinute`는 반드시 `0` 또는 `30`만 반환한다. |
| 5 | 기존 View | `vw_sales_hourly`는 당분간 유지한다. 현재 사용처는 새 30분 테이블/응답 계약으로 전환한다. |
| 6 | 전환 범위 | Backend·DB와 Admin Frontend를 함께 전환한다. |

#### 요청값과 응답값의 역할

```text
Request:  intervalMinutes=30 또는 intervalMinutes=60
Response: 각 행의 salesHour, salesMinute
```

- `intervalMinutes`는 사용자가 화면에서 선택한 집계 단위다.
- `salesMinute`는 조회 결과가 실제로 시작하는 분이다.
- 따라서 30분 요청의 응답에는 `salesMinute: 0`과 `salesMinute: 30`이 모두 올 수 있고,
  60분 요청의 응답에는 `salesMinute: 0`만 온다.

#### 확정된 시간 슬롯 예시

```text
영업시간: 10:00~22:00 (프로젝트 고정)
버킷: 10:00, 10:30, 11:00, 11:30, ..., 21:30

30분 조회
  { salesHour: 10, salesMinute: 0  }  -> 10:00~10:30
  { salesHour: 10, salesMinute: 30 }  -> 10:30~11:00

60분 조회
  { salesHour: 10, salesMinute: 0  }  -> 10:00~11:00
```

#### 구현 시 주의할 계약

- `intervalMinutes=60`의 경우에도 `salesMinute`는 항상 `0`이다.
- `intervalMinutes=30`의 경우 `salesMinute`는 슬롯 시작 분을 표현하므로 `0` 또는 `30`이다. `30`만 반환하면 `10:00~10:30` 슬롯을 표현할 수 없다.
- 오늘은 현재 시각이 속한 버킷까지 포함한다. 아직 시작하지 않은 버킷은 생성하지 않는다.
- `vw_sales_hourly`를 유지하므로 기존 외부 사용처가 즉시 깨지지 않도록 하고, Admin 일별 매출 화면만 새 30분 계약으로 전환한다.
- 화면의 차트, 피크 시간, 표 행 key, mock 데이터, API adapter는 `salesHour + salesMinute`를 함께 사용해야 한다.

### 권장 구현 순서

1. Figma의 시간 단위 선택 상태와 영업시간 정책 확정
2. Product/Screen Bible 및 API 계약 갱신
3. `vw_sales_30min` 정의와 DB 검증 쿼리 작성
4. Mapper 인터페이스·XML의 30/60분 조회 분기 작성
5. Service의 날짜·시간 0-fill 작성
6. `/api/admin/sales/daily` Controller 계약 작성
7. Admin mock, API adapter, `DailySalesPage`의 30분 표시 전환
8. 취소·환불, 빈 날짜, 빈 시간, 오늘, 미래 날짜 회귀 테스트

### 작업 경계

- 이 기록은 대화 내용과 읽기 전용 검토 결과다.
- 소스코드, DB View, API 계약, Git 이력은 변경하지 않았다.
- 구현은 사용자의 명시적 `코드 수정 승인`과 대상 범위 지정 후에만 진행한다.

## 2026-08-20 — 구현 반영

### 반영 범위

- `ASAK-back`
  - `GET /api/admin/sales/daily?date=YYYY-MM-DD&intervalMinutes=30|60` 추가
  - `vw_sales_30min`을 30분 조회 원본으로 연결
  - 60분 조회는 같은 시간의 30분 버킷을 Mapper에서 합산
  - Service가 프로젝트 고정 영업시간 `10:00~22:00`의 누락 슬롯을 0으로 보완
  - 오늘은 현재 시각이 속한 슬롯까지 포함하고 미래 슬롯은 제외
  - 잘못된 interval 값은 `400 SALES_INTERVAL_INVALID`로 반환
- `ASAK-Admin`
  - 일별 매출 화면에 30분/1시간 선택 UI 추가
  - 시간대 차트·피크 시간·상세 표를 `salesHour + salesMinute` 기준으로 표시
  - 시간대 데이터만 새 daily API를 호출하며, 기존 KPI·랭킹·비율 영역은 현재 mock 계약을 유지

### 의도적으로 하지 않은 작업

- 실제 DB에 View DDL을 실행하지 않았다.
- `vw_sales_hourly`를 삭제하거나 변경하지 않았다.
- 일별 화면의 KPI·랭킹·결제/주문유형 비율 API는 이번 범위에 포함하지 않았다.
- Git commit, push, merge, branch 생성은 하지 않았다.

### 검증

- `ASAK-back`: `gradlew.bat compileJava --no-daemon` 성공
- `ASAK-Admin`: `npm.cmd run build` 성공
- `ASAK-Admin`: `npm.cmd run lint` 오류 0건, 기존 `CloudinaryImagePreview.jsx`의 미사용 React 경고 1건
- 실제 DB와 브라우저 API 통신은 실행하지 않았으므로 미검증
