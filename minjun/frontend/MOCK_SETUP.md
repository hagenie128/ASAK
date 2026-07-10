# ASAK 프론트 목업 데이터 설정

백엔드 API 구현 전까지 아래 목업 데이터를 사용하면 됩니다.

## 파일 위치

```text
public/mocks/asak-admin-data.json
```

Vite 개발 서버 기준으로 브라우저에서는 아래 경로로 접근합니다.

```text
/mocks/asak-admin-data.json
```

## 기본 사용법

```js
export async function fetchMockAdminData() {
  const response = await fetch('/mocks/asak-admin-data.json');

  if (!response.ok) {
    throw new Error('목업 데이터를 불러오지 못했습니다.');
  }

  return response.json();
}
```

컴포넌트에서는 이렇게 사용할 수 있습니다.

```js
import { useEffect, useState } from 'react';

export default function AdminDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/mocks/asak-admin-data.json')
      .then((response) => response.json())
      .then(setData);
  }, []);

  if (!data) return null;

  return <div>{data.adminSummary.todayNetSalesAmount.toLocaleString()}원</div>;
}
```

## 주요 데이터 키

```js
data.categories
data.menus
data.optionGroups
data.optionItems
data.optionPolicies
data.menuOptionPolicies
data.soldOutItems
data.paymentMethods
data.orders
data.commonCodes
data.adminSummary
data.salesAnalytics
```

## 관리자 매출 화면용 데이터

실제 DB View와 맞춘 목업입니다.

```js
data.salesAnalytics.salesDaily
data.salesAnalytics.salesHourly
data.salesAnalytics.topMenusDaily
data.salesAnalytics.topMenusHourly
```

각 항목의 의미는 다음과 같습니다.

```js
salesDate; // 매출 일자
salesHour; // 시간대, 0~23
orderCount; // 승인 주문 수
customerCount; // MVP 기준 주문 수와 동일
canceledOrderCount; // 취소/환불 주문 수
grossSalesAmount; // 승인 결제 금액
canceledAmount; // 취소/환불 금액
netSalesAmount; // 순매출
quantity; // 메뉴 판매 수량
salesAmount; // 메뉴 판매 금액
```

## 백엔드 연결 시 교체 기준

나중에 백엔드 API가 생기면 `fetch('/mocks/asak-admin-data.json')` 부분만 API 호출로 바꾸면 됩니다.

예상 매핑:

```text
salesDaily       -> GET /api/admin/sales/daily
salesHourly      -> GET /api/admin/sales/hourly
topMenusDaily    -> GET /api/admin/sales/top-menus/daily
topMenusHourly   -> GET /api/admin/sales/top-menus/hourly
menus            -> GET /api/admin/menus
soldOutItems     -> GET /api/admin/sold-out-items
orders           -> GET /api/admin/orders
paymentMethods   -> GET /api/payment-methods
```
