# ASAK 학습 레포트 — 2026-08-20~21 관리자 매출·주문 상세·영수증 준비

## 0. 문서 기본 정보와 한 줄 결론

| 항목 | 내용 |
| --- | --- |
| 학습 기준 | 2026-08-20~21 Git 커밋과 2026-08-21 현재 작업 트리 |
| 대상 저장소 | `ASAK-Admin` 중심, `ASAK-back`·공용 `ASAK/docs` 연결 범위 |
| 대상 화면 | SCR-019 매출 요약, SCR-020 월별 매출, SCR-021 일별 매출, SCR-022 대시보드, SCR-010 주문 관리, SCR-023 영수증 출력 |
| Figma 기준 | Screen Bible: SCR-019 `39:7405`, SCR-020 `39:7701`, SCR-021 `39:7894`, SCR-010 Default `134:10630` 등. SCR-022/023은 신규 제작 대상·Extension으로 기록됨. 실제 Figma 파일은 이번 검토에서 열지 못함. |
| 확인 범위 | Git diff, React·Spring 코드, Mapper XML, Screen Bible, 로컬 HTTP 응답, ESLint |

**한 줄 결론:** 어제는 DB의 실제 매출 행을 30/60분 시간대 API로 분리하고 Service에서 빈 시간대를 0으로 채우는 계약을 만들었고, 오늘은 그 계약을 Admin 대시보드·요약·월별·일별 화면에 연결했다. 주문 상세 결제수단과 영수증 포맷은 키오스크 명칭으로 정렬 중이지만 실제 출력 흐름은 아직 연결 전이다.

---

## 1. 날짜별·기능별 변경 요약

| 날짜 | 기능 | Git/작업 트리 근거 | 현재 판단 |
| --- | --- | --- | --- |
| 08-20 | 매출 DTO·대시보드·월/일·시간대 집계 | `ASAK-back` `fd1ee04`, `0f6f6ab`, `48b2589`; `ASAK-Admin` `bd33d10`, `fb6df5f`, `3acd0c7` | API·프런트 시간대 훅은 확인됨. 배포 DB View 검증은 별도 필요. |
| 08-21 | Dashboard 실 API | `ASAK-Admin` `d21436c` | `GET /api/admin/dashboard`를 Hook·adapter로 화면에 연결. 로컬 HTTP 200 확인. |
| 08-21 | 매출 요약·월별·일별 실 API | `4f82cf9`, `142ceab`; `ASAK-back` `1efaa93`, `9eb1bc0` | 기간별 API와 adapter 연결, 직접 기간의 null `period` 오류 수정. 로컬 직접 기간 요약 200 확인. |
| 08-21 | 일별 30분/1시간 선택 UI | `d77be80` | 기존 select에 CSS를 추가하고 빈 데이터 문구를 정리. |
| 08-21 | 주문 상세 결제수단·영수증 포맷 | 현재 미커밋 `OrderDetailPanel.jsx`, `orderLabels.js`, `receiptFormat.js` | 결제수단 명칭 처리·영수증 문자열 생성은 확인. 실제 출력 버튼/API/RTOS 경로는 미연결. |
| 08-21 | RTOS 영수증 연동 가이드 | `ASAK` `3f7b533` | 구현 완료 증거가 아닌 연결 설계·검증 절차 문서. |

---

## 2. 화면 목적과 사용자 관점의 동작

### 2-1. SCR-022 대시보드

관리자가 한 화면에서 오늘 KPI, 최근 주문, 주문 현황, 품절 알림, 주간 매출을 빠르게 본다. Screen Bible은 KPI를 4개로 제한하며 `default/loading/empty/error/partialError`를 요구한다.

### 2-2. SCR-019~021 매출 화면

- 요약: 오늘·이번 주·이번 달 또는 직접 기간의 총매출, 주문 수, 객단가와 차트를 본다.
- 월별: 선택 연도의 월 행과 월별 인기 메뉴를 본다.
- 일별: 기간별 일 매출을 보고 선택한 날을 30분 또는 1시간 단위로 분석한다.

### 2-3. SCR-010 주문 관리와 SCR-023 영수증

주문 행을 클릭하면 상세 API의 `items[]`까지 포함한 상세 패널을 연다. 결제수단은 코드값 또는 키오스크 표시명 모두를 표시할 수 있도록 보완됐다. 영수증은 현재 문자열을 만드는 유틸까지이며, SCR-023이 요구하는 `choice/printing/success/error` 화면 또는 실제 프린터 완료 확인은 아직 구현 증거가 없다.

---

## 3. 전체 호출·데이터 흐름

### 대시보드와 매출 요약/월별/일별

```text
[Admin Page]
 DashboardPage / SalesSummaryPage / MonthlySalesPage / DailySalesPage
        │ Hook의 useEffect, refetch
        ▼
[useDashboard / useSalesQuery]
        │ 이전 요청 cancelled 처리, loading/success/error 상태 갱신
        ▼
[adminApi / salesApi]
 GET /api/admin/dashboard
 GET /api/admin/sales/summary?period|startDate&endDate
 GET /api/admin/sales/monthly?year
 GET /api/admin/sales/daily?from&to
        ▼
[AdminSalesController]
        ▼
[AdminSalesService]
 기간 검증·KPI·0-fill·표시 DTO 조립
        ▼
[AdminSalesMapper.xml → 매출 View/DB]
        ▼
[ApiResponse envelope]
        ▼
[apiClient interceptor가 data 해제 → adapter]
 차트용 barHeight 등 렌더링 전용 값 추가
        ▼
[Page의 표·KPI·차트]
```

### 일별 시간대 API는 일별 API와 별도다

```text
DailySalesPage(selectedDate, intervalMinutes)
  → useDailySalesTimeSlots
  → GET /api/admin/sales/daily/time-slots?date=YYYY-MM-DD&intervalMinutes=30|60
  → AdminSalesService.getDailySalesTimeSlots
  → AdminSalesMapper.xml (vw_sales_30min)
  → 영업시간 10:00~22:00 안에서 Service 0-fill
  → 시간대 표·피크 시간 표시
```

`/sales/daily`는 일별 행·랭킹·비중을 가진 객체이고, `/sales/daily/time-slots`는 시간대 배열이다. 둘을 같은 배열로 취급하면 `.map` 오류가 날 수 있으므로 endpoint와 Hook을 분리한 것이 핵심이다.

### 주문 상세와 영수증 준비

```text
OrderTable 행 클릭
  → OrderManagePage.handleOrderDetail(orderId)
  → ordersApi.getOrder(orderId)
  → GET /api/admin/orders/{orderId}
  → selectedOrder
  → OrderDetailPanel
       ├─ paymentMethod 코드면 PAYMENT_METHOD_LABEL 변환
       └─ 이미 표시명이라면 그대로 렌더

buildReceiptText(order)  [현재 어느 화면에서도 import되지 않음]
  → 결제상태·결제수단·주문항목을 텍스트로 조립
  → 실제 printReceipt API 호출은 아직 없음
```

---

## 4. 확인 파일과 읽은 이유

| 파일 | 읽은 이유와 핵심 |
| --- | --- |
| `ASAK-Admin/src/api/adminApi.js`, `salesApi.js` | URL 상수 기반 GET 호출과 query 전달 위치. |
| `ASAK-Admin/src/hooks/useDashboard.js`, `useSalesQuery.js`, `useDailySalesTimeSlots.js` | 로딩·성공·오류 상태, refetch, 이전 요청 무시 경계를 확인. |
| `ASAK-Admin/src/adapters/dashboardAdapter.js`, `salesAdapter.js` | API DTO와 화면 표시 모델의 분리. `barHeight`는 프런트 렌더링 값이다. |
| `ASAK-Admin/src/pages/admin/DailySalesPage.jsx` | 30분/1시간 select, 선택 날짜, 시간대 API와 mock fallback 경계를 확인. |
| `ASAK-back/.../AdminSalesController.java` | 네 매출 GET endpoint의 request parameter 검증 위치. |
| `ASAK-back/.../AdminSalesService.java` | 기간 계산, KPI 비교문구, 실제 매출 집계와 Service 0-fill 책임을 확인. |
| `ASAK-back/src/main/resources/mappers/AdminSalesMapper.xml` | 시간대 집계가 `vw_sales_30min`을 읽는 DB 경계임을 확인. |
| `ASAK-Admin/src/components/admin/orders/OrderDetailPanel.jsx` | 상세 패널의 결제수단 표시와 영수증 출력 callback 자리 확인. |
| `ASAK-Admin/src/utils/receiptFormat.js` | 현재 작업 트리의 영수증 문자열 포맷과 실제 연결 여부 확인. |
| `ASAK/docs/product_bible/07_Screen_Bible/SCR-010,019~023` | Screen ID, Figma Node, 화면 상태와 API 요구사항 대조. |

---

## 5. 파일별 복습

### 5-1. `useDashboard`: API 결과를 바로 화면에 넣지 않는 이유

`useDashboard`는 `adminApi.getDashboard()`가 성공하면 `toDashboardViewModel(response)`을 저장한다. adapter가 주간 매출 금액의 최대치를 기준으로 `barHeight`를 계산한다. 즉 DB/API는 금액·건수 같은 업무 데이터만 제공하고, 막대 높이는 화면 책임이다.

주의: `cancelled`는 네트워크 요청 자체를 중단하지 않고, 화면이 떠난 뒤 늦게 도착한 응답이 state를 덮지 않게 막는 플래그다.

### 5-2. `useSalesQuery`: mode별 endpoint와 직접 기간

`mode`가 `summary/monthly/daily`인지에 따라 `salesApi` getter와 adapter를 고른다. summary는 `period`가 없을 때 `startDate/endDate`를 보낼 수 있다. 08-21의 두 백엔드 수정은 이 경우 `periodLabel(null)` 및 비교문구의 `switch(null)`가 예외를 내던 문제를 방지했다.

주의: API client가 envelope의 `data`를 해제하므로 Hook에서 다시 `response.data`를 읽지 않는다. 실제 반환 모양을 apiClient와 HTTP 응답으로 함께 확인해야 한다.

### 5-3. `DailySalesPage`와 `useDailySalesTimeSlots`

초기 시간 단위 state는 60이고 select는 `30` 또는 `60`만 허용한다. `selectedDate` 또는 단위가 변하면 시간대 Hook이 재조회한다. API 성공 전에는 화면에 기존 mock `hourly`가 fallback으로 남는다.

주의: 이것은 UX상 화면이 비지 않는 장점이 있으나, API 오류를 실제 매출 데이터처럼 오해할 위험이 있다. 코드에는 time-slot error와 재시도 분기가 있으므로 QA에서 정상/빈/오류를 각각 확인해야 한다.

### 5-4. `AdminSalesService.getDailySalesTimeSlots`

Mapper가 반환한 실제 슬롯을 `hour:minute` 키로 모은 뒤 10:00부터 22:00 직전까지 순회한다. 없는 슬롯은 `orderCount/netSalesAmount/averageOrderAmount = 0` DTO로 생성한다. 오늘은 아직 지나지 않은 미래 슬롯을 제외한다.

이 구조의 의미는 **DB에는 실제 매출만 집계하고, 화면에 필요한 빈 시간대는 Service가 채운다**는 것이다. 60분 조회는 30분 View의 두 버킷을 합치는 Mapper 책임이다.

### 5-5. 주문 상세 결제수단과 `buildReceiptText`

실제 상세 API 응답의 예시는 `paymentMethod: "카카오페이 결제"`였고, 기존 Panel은 `KAKAO_PAY` 같은 코드 키만 찾았다. 현재 Panel은 코드면 `PAYMENT_METHOD_LABEL`로 변환하고, 일치하는 키가 없으면 원본 문자열을 표시한다. 라벨 상수도 키오스크 표기인 `카드 / 삼성페이 결제`, `카카오페이 결제`, `네이버페이 결제`로 보완됐다.

`buildReceiptText`는 `PAYMENT_STATUS_LABEL`로 결제상태를, 동일한 paymentMethod 규칙으로 결제수단을 출력한다. `orderStatus ?? status`로 현재 상세 DTO와 레거시 mock 양쪽을 받도록 했다.

주의: 이 유틸을 만든 사실은 영수증 출력 기능 완료가 아니다. 주문 관리의 `onPrintReceipt`와 `ordersApi.printReceipt`는 TODO/주석 상태다.

---

## 6. 화면 상태와 Figma/Screen Bible 대조

| 화면 | Default | Loading | Empty | Error | Disabled | Figma/명세 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| Dashboard | API 데이터 렌더 | `useDashboard` 초기 loading | widget별 empty는 이번 코드 검토에서 명확히 미확인 | page error + refetch 확인 | 별도 CTA disabled는 미확인 | SCR-022 요구 상태는 있지만 실제 Figma Node는 신규 제작 대상 |
| Sales Summary | KPI·차트·랭킹 | Hook loading | API 빈 배열 표시의 세부 UI는 Page별 추가 확인 필요 | Hook error | 기간 전환 중 중복 조작 제어는 추가 QA 필요 | SCR-019 Default/Loading/Empty/Error Node 기록 있음 |
| Monthly/Daily | 행·차트·랭킹 | Hook loading | 행 0건 처리 확인 필요 | Hook error | 날짜 picker/단위 select의 disabled 상태는 코드·브라우저 QA 추가 필요 | SCR-020/021 Figma Node 기록 있음 |
| Order Management | 목록·상세 패널 | `useOrdersQuery` 범위 | Screen Bible 요구 | Screen Bible 요구 | 출력 버튼은 payment 상태 기반 조건이 있으나 handler 미연결 | SCR-010의 Default/Loading/Empty/Error Node 기록 있음 |
| Receipt Output | 미구현 | 미구현 | 미구현 | 미구현 | 미구현 | SCR-023은 Extension·신규 화면으로 정의, 실행 화면 없음 |

실제 Figma 파일은 이번 검토에서 접근하지 못했다. 따라서 Node 값은 Screen Bible에 적힌 참조이며 시각적 일치 검증의 증거가 아니다.

---

## 7. 데이터 필드·Mock·API·DB 검증 상태

| 항목 | 현재 코드 계약 | 확인 상태 |
| --- | --- | --- |
| 대시보드 | `dateLabel`, `kpis[]`, `weeklySales[]`, 최근 주문·상태·재고 요약 | 로컬 HTTP에서 KPI 4개, weeklySales 7개 확인. DB View의 배포 상태는 미확인. |
| 매출 요약 | `label`, `dateRange`, `kpis[]`, `hourlySales[]` 또는 `dailySales[]`, 비중·랭킹 | 직접 기간 2026-08-01~07 요청에서 success와 일별 7행 확인. |
| 월별/일별 | 월 `rows/ranking`, 일 `rows/ranking/breakdown` | 코드·Controller 확인. 이번 문서 작성 중 로컬 endpoint 전체 재검증은 시간 제한으로 완료하지 못함. |
| 시간대 | `salesHour`, `salesMinute`, `orderCount`, `netSalesAmount`, `averageOrderAmount` | Controller·Service·Hook 확인. 실제 배포 `vw_sales_30min` 열/데이터는 미확인. |
| 주문 상세 | `orderId`, `orderNo`, `orderStatus`, `paymentStatus`, `paymentMethod`, `totalAmount`, `items[]` | 로컬 상세 API에서 `paymentMethod`이 표시명임을 확인. |
| 결제 승인 | `approvedAmount`, `approvedAt`, `waitingOrderCount` | 이번 범위의 Admin 주문 상세 DTO/영수증 포맷에서 사용하지 않음. 결제 완료/환불 구현 증거로 해석하면 안 됨. |
| 영수증 | 텍스트 포맷 함수 | 문자열 단위 테스트 확인. API 호출·DB device event·RTOS 완료 상태는 미확인. |

---

## 8. 사실 / 해석 / 미확인·TODO

### 사실

- 08-21 Admin 커밋 4개가 Dashboard, 매출 요약, 월/일 매출, 시간 단위 UI를 변경했다.
- 직접 기간 summary의 null `period`은 백엔드 `periodLabel`과 KPI 비교문구에서 방어됐다.
- 시간대 endpoint는 30/60 이외 값을 `SALES_INTERVAL_INVALID`로 거절한다.
- 현재 Admin 작업 트리에는 결제수단 표기, 영수증 포맷, TTS 관련 미커밋 변경이 있다.

### 코드 근거에 따른 해석

- adapter 계층은 서버 DTO 변경이 차트 컴포넌트까지 직접 퍼지는 것을 줄이는 경계다.
- Service 0-fill은 차트/표의 시간축을 일관되게 만들어 프런트에서 누락 슬롯을 추론하지 않게 한다.
- 영수증 문자열 선조립 방식은 RTOS의 중첩 JSON 파싱 부담을 줄일 수 있지만, payload 크기와 이스케이프 처리 합의가 선행돼야 한다.

### 미확인 또는 TODO

- `vw_sales_30min`이 실행 DB에 반영됐는지와 실제 30/60분 합계 정합성.
- 매출·대시보드 각 화면의 브라우저 상태 및 Figma 시각 대조.
- Admin 영수증 출력 버튼 → device-event API → RTOS polling → 완료 상태 보고 전체 흐름.
- 환불은 TODO이며, 주문 취소와 실제 결제 환불을 같은 완료 상태로 볼 수 없다.
- 현재 `ASAK-back`은 `origin/main`보다 ahead 2/behind 1, Admin은 ahead 4이며, 이 문서는 publish 여부를 판단하지 않는다.

---

## 9. 검증 기록

| 항목 | 결과 | 한계 |
| --- | --- | --- |
| Git 이력 | 08-20~21의 ASAK/Admin/back/Kiosk log와 현재 status 확인 | 원격 병합·배포는 수행하지 않음 |
| 로컬 Dashboard API | `GET /api/admin/dashboard` success, KPI 4개, weeklySales 7개 | 로컬 8080 기준 |
| 로컬 직접 기간 Summary API | `GET /api/admin/sales/summary?startDate=2026-08-01&endDate=2026-08-07` success, dailySales 7개 | 로컬 8080 기준 |
| Admin ESLint | 오류 0건, 기존 `CloudinaryImagePreview.jsx` unused React 경고 1건 | 브라우저 E2E를 대체하지 않음 |
| 영수증 문자열 | `KAKAO_PAY` 입력에서 `결제상태: 결제완료`, `결제수단: 카카오페이 결제` 포함 확인 | 실제 인쇄/API 호출 미검증 |
| Figma/브라우저 | 미실행 | 브라우저 세션을 사용할 수 없었고, 최신 Figma 파일 키도 제공되지 않음 |

---

## 10. 직접 해 볼 확인 항목과 연습문제

### 직접 해 볼 확인 항목

1. Admin에서 30분과 1시간을 번갈아 선택해 표의 시간 라벨·피크 시간·합계가 같은 날짜 기준으로 맞는지 본다.
2. Network에서 `/sales/daily` 객체와 `/sales/daily/time-slots` 배열을 각각 열어 shape 차이를 기록한다.
3. 직접 기간 매출의 이전 기간 비교문구가 `기간 대비`로 보이는지 확인한다.
4. 결제수단이 코드(`CARD`)와 표시명(`카카오페이 결제`)인 주문 각각에서 상세·영수증 문자열을 비교한다.
5. 영수증 출력 구현 전에는 버튼이 성공 토스트만 띄우거나 완료로 오인하지 않는지 확인한다.

### 연습문제

1. `useSalesQuery`가 빠른 기간 전환에서 늦은 응답을 무시하는 코드를 찾아 설명해 본다.
2. Service 0-fill을 프런트에서 하지 않고 백엔드에서 하는 장점 두 가지를 적어 본다.
3. `/sales/daily` 응답을 시간대 표에 그대로 `map`하면 왜 위험한지 응답 모양으로 설명해 본다.
4. `paymentMethod`의 코드와 표시명을 하나의 필드에 섞어 보낼 때 생기는 장단점을 적어 본다.
5. 주문 취소 API가 존재해도 환불 완료라고 말할 수 없는 증거 조건을 세 가지 적어 본다.

### 다음에 읽을 파일 (최대 3개)

1. `ASAK-Admin/src/api/apiClient.js` — envelope 해제와 오류 처리의 공통 경계.
2. `ASAK-back/src/main/resources/mappers/AdminSalesMapper.xml` — 30/60분 집계 SQL과 View 열 확인.
3. `ASAK-Admin/src/pages/admin/OrderManagePage.jsx` — 영수증 출력 TODO를 실제 device-event 흐름으로 연결할 자리.

