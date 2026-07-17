# ASAK Figma 확장 설계 프롬프트 — 알레르기 · 결제수단 · 매출 분석

> 작성일: 2026-07-14  
> 대상 파일: [ASAK Figma](https://www.figma.com/design/o9mxSeovLQPdWNwM4mNySk/ASAK)  
> 범위: 기존 화면·컴포넌트를 보존하고 필요한 Component/Variant/레이어를 추가하는 설계 작업

## 1. 현재 파일·데이터 기준

### Figma에서 확인한 기존 자산

| 영역 | 기존 화면/컴포넌트 | 판단 |
| --- | --- | --- |
| 메뉴 상세 | `k003` (`330:26875`) — `product-info`, `MenuDetail`, `OptionCategory`, `OrderDetailRow` | 알레르기 전용 섹션·태그·안내 컴포넌트 없음 |
| 결제수단 | 관리자 결제수단 설정 화면, `PaymentMethodCard` | 카드/간편결제 노출 및 정책 문구 초안 존재. 저장·실패·순서 변경 상태 보강 필요 |
| 매출 요약 | `A-006 sales-summary` (`303:18679`) | Filters, SummaryCards, 일별/시간대별 영역 존재 |
| 월별 매출 | `A-006 monthly-sales` (`303:19003`) | 연간 요약, 월별 추이·상세 데이터 영역 존재 |
| 일별 매출 | `A-006 daily-sales` (`303:19251`) | 일 단위 분석 화면 존재 |

### 지금 데이터로 실제 표시 가능한 값

| 데이터 원천 | 확정 필드 | 바로 만들 수 있는 UI |
| --- | --- | --- |
| `GET /api/admin/sales/daily?from&to` (API-015) | `date`, `orderCount`, `totalAmount` | 기간 총매출, 총 주문수, 객단가, 일별 매출 차트·테이블, 월별 집계 |
| 관리자 주문 목록 (API-007 mock) | `orderNo`, `orderType`, `totalPrice`, `orderStatus`, `paymentStatus`, `createdAt`, `items[].menuName`, `items[].quantity` | 메뉴별 판매량, 포장/매장 비중, 최근 주문 목록, 결제 상태별 주문 수 |
| 메뉴 상세/seed | `allergens`, `allergyText`, 재료·옵션 | 알레르기 태그, 알레르기 안내, 옵션 변경 후 포함 성분 표시 |

### 지금 데이터만으로 확정 표시하면 안 되는 값

- 시간대별 매출: `createdAt`을 사용하는 클라이언트 집계 또는 별도 API가 필요하다.
- 결제수단별 매출: 주문 목록 응답에는 `paymentMethod`가 없으므로 결제 데이터 조인 또는 별도 API가 필요하다.
- 환불·취소액, 전월 대비, 목표 대비, 순매출: 관련 금액/비교 기준이 아직 확정되지 않았다.

이 값들은 차트를 억지로 채우지 말고 `데이터 연결 예정` 또는 `추후 확장` 상태로 표시한다.

---

## 2. 화면별 섹션 계획

### A. 고객 키오스크 메뉴 상세 — 알레르기 안내

**삽입 위치:** `k003 > MenuDetail`의 첫 `OptionCategory` 위, `product-info`와 옵션 선택 영역 사이.

| 섹션 | 표시 정보 | 상태 |
| --- | --- | --- |
| 알레르기·식단 태그 | 견과류, 우유, 계란, 갑각류, 대두, 밀 등 / 비건 여부 | `default`, `warning` |
| 알레르기 안내 | “선택한 메뉴에 알레르기 유발 가능 성분이 포함되어 있어요.” | `default`, `hasAllergen`, `optionChanged` |
| 옵션 반영 안내 | 옵션 추가/제외 뒤 새로 포함된 알레르기 표시 | `hidden`, `visible` |
| 상세 모달(선택) | 성분명, 포함 출처(기본/추가 옵션), 안내 문구 | `default` |

**필수 컴포넌트**

```text
AllergenTag
  properties: type=nut|milk|egg|shellfish|soy|wheat|…, state=default|warning, label

DietaryTag
  properties: type=vegan|vegetarian|…, label

AllergenNotice
  properties: state=default|hasAllergen|optionChanged, title, description

AllergenDetailModal (선택)
  properties: state=default, allergenList, sourceList
```

**권장 레이어 구조**

```text
MenuDetail
├─ product-info
├─ allergen-section
│  ├─ allergen-section-header
│  ├─ allergen-tag-list
│  │  ├─ allergen-tag/*
│  │  └─ dietary-tag/*
│  └─ allergen-notice
├─ option-section
└─ menu-detail-footer
```

> 알레르기 UI는 성분 정보 고지용이다. “안전 보장”, “섭취 가능”처럼 의료적 판단으로 해석될 문구는 사용하지 않는다.

### B. 관리자 결제수단 설정

| 섹션 | 표시 정보 | 상태 |
| --- | --- | --- |
| 결제수단 목록 | 아이콘, 이름, 설명, 활성 여부, 우선순위 | `enabled`, `disabled`, `maintenance` |
| 노출 순서 | 위/아래 이동, 첫/마지막 버튼 비활성 | `default`, `first`, `last` |
| 결제 정책 | 실패 시 초기화, 안내문, 영수증 정책 | `default`, `changed` |
| 저장 바 | 변경 감지, 저장, 성공, 오류 | `idle`, `dirty`, `saving`, `success`, `error` |
| 위험 변경 확인 | 모든 수단 비활성화 등 | `default` |

**필수 컴포넌트**

```text
Admin/PaymentMethodSettingRow
  properties: state=enabled|disabled|maintenance, name, description, icon, enabled

Admin/PaymentMethodOrderControl
  properties: state=default|first|last, direction=up|down

Admin/PaymentPolicyCard
  properties: policyType=resetOnFailure|notice|receipt, state=default|changed

Admin/SaveBar
  properties: state=idle|dirty|saving|success|error

Admin/ConfirmDialog
  properties: type=disableAllPaymentMethods|discardChanges
```

**흐름**

```text
결제수단 설정 진입
→ 활성/비활성 또는 노출 순서 변경
→ SaveBar: dirty
→ 저장
→ saving
→ success: 키오스크 PaymentMethodCard 목록 갱신
→ error: 기존 설정 유지 + 오류 안내
```

> 현재 API에는 실제 결제수단 설정 저장 계약이 없으므로, Figma에서는 `mock settings` 또는 `연동 예정`으로 표기한다.

### C. 관리자 매출 요약

**현재 데이터로 구성할 섹션**

| 섹션 | 데이터 | 계산/표현 |
| --- | --- | --- |
| 기간 필터 | `from`, `to` | 오늘, 최근 7일, 이번 달, 직접 선택 |
| 핵심 지표 | `totalAmount`, `orderCount` | 총매출, 총 주문수, 객단가(`총매출 ÷ 주문수`) |
| 일별 매출 추이 | `date`, `totalAmount` | 선/막대 차트 |
| 최근 주문 | 주문 목록 | 주문번호, 주문유형, 결제상태, 주문상태, 금액, 주문일시 |
| 메뉴별 판매량 | `items[].menuName`, `quantity` | 상위 메뉴 목록·판매 수량 |
| 상태 안내 | API 응답 | `loading`, `empty`, `error` |

**보류 또는 연결 예정 섹션**

- 시간대별 매출: 집계 API가 생기기 전까지 `연결 예정` 상태 카드로 둔다.
- 결제수단별 매출: `paymentMethod` 데이터가 주문 목록에 포함된 뒤 추가한다.

### D. 관리자 월별 매출

**현재 데이터로 구성할 섹션**

| 섹션 | 데이터 | 계산/표현 |
| --- | --- | --- |
| 연도 필터 | API-015 `from/to` | 해당 연도 1/1~12/31 |
| 연간 총매출 | 일별 `totalAmount` 합계 | 숫자 카드 |
| 연간 주문수 | 일별 `orderCount` 합계 | 숫자 카드 |
| 월 평균 객단가 | 총매출 ÷ 총 주문수 | 숫자 카드 |
| 월별 매출 추이 | 일별 데이터를 월 단위로 집계 | 막대/선 차트 |
| 월별 상세 테이블 | 월, 주문수, 매출, 객단가 | 테이블 |
| 최다 판매 메뉴 | 주문 목록 `items` 집계 | 상위 메뉴 3개 |

**제외/연결 예정**

- 전년 동월 대비, 성장률, 목표 달성률은 비교 기준 데이터가 확정된 뒤 추가한다.

### E. 관리자 일별 매출

**현재 데이터로 구성할 섹션**

| 섹션 | 데이터 | 계산/표현 |
| --- | --- | --- |
| 날짜 선택 | `from=to=선택일` | 이전/다음 날짜 이동 포함 |
| 일 매출 요약 | `totalAmount`, `orderCount` | 총매출, 주문수, 객단가 |
| 메뉴별 판매량 | 주문 목록 `items` | 메뉴명, 판매 수량, 매출(수량×unitPrice) |
| 주문 유형 비중 | `orderType` | 매장/포장 주문 수 또는 비율 |
| 주문 상태 요약 | `orderStatus`, `paymentStatus` | 접수/준비/완료, 결제완료/대기/실패 |
| 주문 상세 테이블 | 주문 목록 | 주문번호, 시각, 메뉴 요약, 금액, 상태 |

**제외/연결 예정**

- 시간대별 차트는 별도 집계 API가 생기기 전에는 노출하지 않거나 `데이터 연결 예정`으로 처리한다.

---

## 3. 공통 컴포넌트·레이어 명명 규칙

```text
Admin/SalesPeriodFilter
  state=default|open|customRange|loading

Admin/SalesMetricCard
  metric=totalSales|orderCount|averageOrderValue
  state=default|loading|empty

Admin/SalesChart
  granularity=daily|monthly
  state=default|loading|empty|error

Admin/SalesBreakdownTable
  type=daily|monthly|menu|order
  state=default|empty|loading|error

Admin/EmptyState
  type=sales|paymentMethods

Admin/ErrorState
  type=salesLoad|paymentSave
```

레이어는 보이는 문구가 아니라 데이터 의미로 이름을 짓는다.

```text
sales-page
├─ sales-header
│  ├─ title-area
│  └─ sales-period-filter
├─ sales-metrics
├─ sales-analysis
│  ├─ sales-chart-card
│  └─ sales-breakdown-card
├─ sales-detail-table
└─ sales-state
```

---

## 4. Figma AI/MCP 실행 프롬프트

아래 프롬프트를 Figma AI 또는 Figma MCP 작업 요청에 그대로 붙여 넣는다.

```text
ASAK Figma 파일을 수정해줘. 기존 화면과 컴포넌트는 삭제하거나 덮어쓰지 말고, 새 컴포넌트·Variant를 먼저 만든 뒤 기존 화면에 인스턴스로 적용해줘.

작업 범위는 다음 3가지야.
1) 고객 키오스크 메뉴 상세(k003): 알레르기·비건 정보
2) 관리자 결제수단 설정: 저장 가능한 설정 UI
3) 관리자 매출 요약/월별 매출/일별 매출: 현재 데이터로 가능한 분석 UI

공통 원칙:
- 현재 파일의 색상, 타이포, Auto Layout, Admin/Kiosk 컴포넌트 구조를 재사용한다.
- 새 프레임/컴포넌트는 의미 있는 이름을 사용한다. `Frame 123`, `Property 1`, `Variant2` 같은 자동 이름을 남기지 않는다.
- 모든 컴포넌트는 Auto Layout을 사용하고, Variant는 상태를 표현할 때만 사용한다.
- 데이터가 아직 없는 차트나 지표는 임의 숫자를 만들지 말고 `데이터 연결 예정` 또는 `빈 상태`로 표시한다.
- 기존 컴포넌트와 화면은 보존한다.

[1. 알레르기]
k003의 product-info와 첫 OptionCategory 사이에 `allergen-section`을 추가한다.

새 컴포넌트:
- `AllergenTag`: type=nut|milk|egg|shellfish|soy|wheat|etc, state=default|warning, label Text property
- `DietaryTag`: type=vegan|vegetarian|etc, label Text property
- `AllergenNotice`: state=default|hasAllergen|optionChanged, title/description Text property
- 필요하면 `AllergenDetailModal`: 알레르기 성분과 포함 출처(기본 구성/추가 옵션)를 표시

레이어 구조:
MenuDetail > allergen-section > allergen-section-header, allergen-tag-list, allergen-notice

표시 규칙:
- 메뉴 기본 성분 또는 선택 옵션의 알레르기 유발 성분을 태그로 표시한다.
- 옵션 변경 후 새로 포함된 성분이 있으면 AllergenNotice를 warning 상태로 바꾼다.
- 의료적 안전 보장 문구는 사용하지 말고, 성분 정보 안내 문구만 사용한다.

[2. 관리자 결제수단 설정]
기존 결제수단 설정 화면을 확장한다.

새 컴포넌트:
- `Admin/PaymentMethodSettingRow`: state=enabled|disabled|maintenance, icon/name/description/enabled Property
- `Admin/PaymentMethodOrderControl`: state=default|first|last, direction=up|down
- `Admin/PaymentPolicyCard`: policyType=resetOnFailure|notice|receipt, state=default|changed
- `Admin/SaveBar`: state=idle|dirty|saving|success|error
- `Admin/ConfirmDialog`: type=disableAllPaymentMethods|discardChanges

화면 레이어:
payment-method-settings > settings-header, method-list, payment-policy, save-bar

흐름:
설정 진입 → 결제수단 토글/순서 변경 → dirty 저장 바 노출 → 저장 중 → 성공 또는 오류 상태

현재 실제 설정 저장 API는 없으므로 화면의 데이터 표시는 mock settings 또는 연동 예정으로 명시한다.

[3. 관리자 매출]
기존 A-006 sales-summary, monthly-sales, daily-sales를 유지하고, 공통 필터와 상태 컴포넌트를 추가한다.

실제 사용 가능한 데이터:
- API-015 일별 매출: date, orderCount, totalAmount
- 관리자 주문 목록: orderNo, orderType, totalPrice, orderStatus, paymentStatus, createdAt, items[].menuName, items[].quantity

새 공통 컴포넌트:
- `Admin/SalesPeriodFilter`: state=default|open|customRange|loading
- `Admin/SalesMetricCard`: metric=totalSales|orderCount|averageOrderValue, state=default|loading|empty
- `Admin/SalesChart`: granularity=daily|monthly, state=default|loading|empty|error
- `Admin/SalesBreakdownTable`: type=daily|monthly|menu|order, state=default|empty|loading|error
- `Admin/EmptyState`: type=sales|paymentMethods
- `Admin/ErrorState`: type=salesLoad|paymentSave

매출 요약 화면 섹션:
- 기간 필터: 오늘, 최근 7일, 이번 달, 직접 선택
- 총매출, 총 주문수, 객단가(총매출 ÷ 주문수)
- 일별 매출 추이 차트
- 메뉴별 판매량 상위 목록
- 최근 주문 목록
- loading/empty/error 상태

월별 매출 화면 섹션:
- 연도 필터
- 연간 총매출, 연간 주문수, 평균 객단가
- 월별 매출 추이 차트
- 월별 상세 테이블: 월, 주문수, 매출, 객단가
- 상위 메뉴 3개

일별 매출 화면 섹션:
- 날짜 선택과 이전/다음 날짜 이동
- 일 매출, 주문수, 객단가
- 메뉴별 판매량
- 매장/포장 주문 비중
- 주문 상태·결제 상태 요약
- 주문 상세 테이블

중요:
- 시간대별 매출은 현재 확정 API가 없으므로 `데이터 연결 예정` 상태로 처리한다.
- 결제수단별 매출도 paymentMethod 데이터가 주문 목록에 없으므로 동일하게 처리한다.
- 전년 대비, 성장률, 목표 달성률, 환불/취소액은 데이터 기준이 확정되기 전에는 새 지표로 만들지 않는다.

매출 화면 레이어 구조:
sales-page > sales-header(title-area, sales-period-filter), sales-metrics, sales-analysis(sales-chart-card, sales-breakdown-card), sales-detail-table, sales-state

완료 후 확인:
- 기존 A-006 화면 3종이 보존됐는지
- 새 컴포넌트 이름·Variant·레이어 이름에 자동 생성 이름이 없는지
- 모든 loading/empty/error 상태가 Default 화면과 동일한 레이아웃을 유지하는지
- 알레르기 섹션, 저장 바, 기간 필터의 텍스트가 잘리지 않는지
```

## 5. 구현 우선순위

1. `AllergenTag`·`AllergenNotice`와 `k003` 삽입
2. `SalesPeriodFilter`, `SalesMetricCard`, 매출 화면의 `loading/empty/error`
3. 결제수단 설정의 `PaymentMethodSettingRow`, `SaveBar`
4. 메뉴별 판매량·월별 집계 테이블
5. 새 API 확정 뒤 시간대별/결제수단별/비교 분석 확장
