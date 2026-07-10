# ASAK 프론트 데이터 구현 안내

이 문서는 **디자인 없이 데이터 흐름만 구현**하기 위한 안내입니다.

현재 프로젝트 구조는 아래 기준으로 작업합니다.

```text
src/
├─ api/
│  ├─ axiosInstance.js
│  └─ endpoints.js
├─ components/
│  ├─ common/
│  └─ layout/
├─ features/
│  ├─ kiosk/
│  │  ├─ components/
│  │  └─ hooks/
│  └─ admin/
│     ├─ components/
│     └─ hooks/
├─ pages/
│  ├─ kiosk/
│  └─ admin/
├─ store/
│  ├─ useCartStore.js
│  └─ useAdminStore.js
├─ utils/
├─ App.jsx
└─ main.jsx
```

## 제일 중요한 원칙

지금 할 일은 **디자인 구현이 아닙니다.**

하지 마세요:

```text
CSS 추가
CSS 수정
색상 지정
카드 디자인 만들기
레이아웃 예쁘게 잡기
버튼 디자인 만들기
className을 많이 추가하기
inline style 넣기
```

해야 할 일:

```text
목업 데이터를 불러오기
store에 저장하기
hooks로 데이터를 꺼내기
페이지에서 데이터가 보이는지 확인하기
나중에 백엔드 API로 교체하기 쉽게 구조 만들기
```

화면은 못생겨도 됩니다. 지금은 데이터 연결이 목적입니다.

## 목업 데이터 위치

목업 JSON은 여기에 있습니다.

```text
public/mocks/asak-admin-data.json
```

Vite 실행 중에는 아래 경로로 불러옵니다.

```text
/mocks/asak-admin-data.json
```

## 데이터 흐름

반드시 이 흐름으로 짜세요.

```text
public/mocks/asak-admin-data.json
  ↓
src/api/endpoints.js
  ↓
src/store/useAdminStore.js
  ↓
src/features/admin/hooks/useAdminData.js
  ↓
src/pages/admin/Dashboard.jsx
src/pages/admin/OrderManage.jsx
src/pages/admin/MenuManage.jsx
```

페이지에서 직접 `fetch('/mocks/asak-admin-data.json')`를 여러 번 쓰지 마세요.  
데이터 불러오는 코드는 store 또는 hook 안에 모아야 합니다.

## 1단계: endpoints.js에 목업 경로 추가

파일:

```text
src/api/endpoints.js
```

예시:

```js
export const ENDPOINTS = {
  mockAdminData: '/mocks/asak-admin-data.json',
};
```

나중에 백엔드가 생기면 이 값을 API 주소로 바꾸면 됩니다.

```js
export const ENDPOINTS = {
  mockAdminData: '/api/admin/bootstrap',
};
```

## 2단계: useAdminStore.js에서 데이터 관리

파일:

```text
src/store/useAdminStore.js
```

역할:

- 목업 JSON을 한 번 불러옵니다.
- 관리자 데이터를 store에 저장합니다.
- 로딩 상태를 저장합니다.
- 에러 상태를 저장합니다.
- 페이지가 직접 fetch하지 않게 합니다.

예시:

```js
import { create } from 'zustand';
import { ENDPOINTS } from '../api/endpoints';

export const useAdminStore = create((set, get) => ({
  data: null,
  isLoading: false,
  error: null,

  loadAdminData: async () => {
    if (get().isLoading) return;
    if (get().data) return;

    set({ isLoading: true, error: null });

    try {
      const response = await fetch(ENDPOINTS.mockAdminData);

      if (!response.ok) {
        throw new Error('관리자 목업 데이터를 불러오지 못했습니다.');
      }

      const data = await response.json();
      set({ data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.',
        isLoading: false,
      });
    }
  },
}));
```

## 3단계: admin hook 만들기

파일:

```text
src/features/admin/hooks/useAdminData.js
```

역할:

- 페이지에서 store 구조를 자세히 몰라도 되게 합니다.
- 필요한 데이터만 이름 붙여서 꺼내줍니다.
- Dashboard, OrderManage, MenuManage에서 같이 씁니다.

예시:

```js
import { useEffect } from 'react';
import { useAdminStore } from '../../../store/useAdminStore';

export function useAdminData() {
  const data = useAdminStore((state) => state.data);
  const isLoading = useAdminStore((state) => state.isLoading);
  const error = useAdminStore((state) => state.error);
  const loadAdminData = useAdminStore((state) => state.loadAdminData);

  useEffect(() => {
    loadAdminData();
  }, [loadAdminData]);

  return {
    data,
    isLoading,
    error,
    summary: data?.adminSummary ?? null,
    menus: data?.menus ?? [],
    orders: data?.orders ?? [],
    soldOutItems: data?.soldOutItems ?? [],
    paymentMethods: data?.paymentMethods ?? [],
    salesDaily: data?.salesAnalytics?.salesDaily ?? [],
    salesHourly: data?.salesAnalytics?.salesHourly ?? [],
    topMenusDaily: data?.salesAnalytics?.topMenusDaily ?? [],
    topMenusHourly: data?.salesAnalytics?.topMenusHourly ?? [],
  };
}
```

## 4단계: Dashboard.jsx에서 매출 요약 출력

파일:

```text
src/pages/admin/Dashboard.jsx
```

역할:

- 매출 요약
- 고객 수
- 취소 금액
- 인기 메뉴
- 시간대별 매출

디자인 없이 데이터가 나오는지만 확인합니다.

예시:

```jsx
import { useAdminData } from '../../features/admin/hooks/useAdminData';

export default function Dashboard() {
  const { isLoading, error, summary, salesHourly, topMenusDaily } = useAdminData();

  if (isLoading) return <div>데이터 불러오는 중</div>;
  if (error) return <div>{error}</div>;
  if (!summary) return <div>데이터 없음</div>;

  return (
    <div>
      <h1>관리자 대시보드</h1>

      <h2>오늘 요약</h2>
      <ul>
        <li>주문 수: {summary.todayOrderCount}</li>
        <li>고객 수: {summary.todayCustomerCount}</li>
        <li>총매출: {summary.todaySalesAmount}</li>
        <li>순매출: {summary.todayNetSalesAmount}</li>
        <li>취소 금액: {summary.todayCanceledAmount}</li>
        <li>취소 주문 수: {summary.todayCanceledOrderCount}</li>
        <li>인기 메뉴: {summary.todayTopMenuName}</li>
      </ul>

      <h2>시간대별 매출</h2>
      <table>
        <tbody>
          {salesHourly.map((row) => (
            <tr key={`${row.salesDate}-${row.salesHour}`}>
              <td>{row.salesHour}시</td>
              <td>주문 {row.orderCount}</td>
              <td>고객 {row.customerCount}</td>
              <td>순매출 {row.netSalesAmount}</td>
              <td>취소 {row.canceledAmount}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>많이 팔린 메뉴</h2>
      <table>
        <tbody>
          {topMenusDaily.map((row) => (
            <tr key={`${row.salesDate}-${row.menuId}`}>
              <td>{row.menuName}</td>
              <td>수량 {row.quantity}</td>
              <td>매출 {row.salesAmount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## 5단계: MenuManage.jsx에서 메뉴 데이터 출력

파일:

```text
src/pages/admin/MenuManage.jsx
```

역할:

- 메뉴 목록 확인
- 가격 확인
- 품절 여부 확인
- 옵션 정책 연결 확인

예시:

```jsx
import { useAdminData } from '../../features/admin/hooks/useAdminData';

export default function MenuManage() {
  const { isLoading, error, menus } = useAdminData();

  if (isLoading) return <div>데이터 불러오는 중</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>메뉴 관리 데이터</h1>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>메뉴명</th>
            <th>가격</th>
            <th>품절</th>
            <th>옵션 정책 ID</th>
          </tr>
        </thead>
        <tbody>
          {menus.map((menu) => (
            <tr key={menu.id}>
              <td>{menu.id}</td>
              <td>{menu.name}</td>
              <td>{menu.price}</td>
              <td>{menu.isSoldOut ? '품절' : '판매중'}</td>
              <td>{menu.optionPolicyIds.join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## 6단계: OrderManage.jsx에서 주문 데이터 출력

파일:

```text
src/pages/admin/OrderManage.jsx
```

역할:

- 주문 목록 확인
- 주문 상태 확인
- 결제수단 확인
- 주문별 메뉴 확인

예시:

```jsx
import { useAdminData } from '../../features/admin/hooks/useAdminData';

export default function OrderManage() {
  const { isLoading, error, orders } = useAdminData();

  if (isLoading) return <div>데이터 불러오는 중</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>주문 관리 데이터</h1>

      {orders.map((order) => (
        <div key={order.id}>
          <h2>{order.orderNo}</h2>
          <p>상태: {order.status}</p>
          <p>주문 유형: {order.orderType}</p>
          <p>결제수단: {order.paymentMethodCode}</p>
          <p>금액: {order.totalAmount}</p>

          <ul>
            {order.items.map((item) => (
              <li key={item.id}>
                {item.menuName} / 수량 {item.quantity} / 단가 {item.unitPrice}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
```

## 7단계: admin/components는 언제 쓰나

처음부터 컴포넌트를 많이 나누지 마세요.

처음에는 `Dashboard.jsx`, `MenuManage.jsx`, `OrderManage.jsx` 안에 그냥 작성하세요.  
코드가 길어지면 그때 아래로 분리합니다.

```text
src/features/admin/components/SalesSummaryTable.jsx
src/features/admin/components/TopMenuTable.jsx
src/features/admin/components/MenuDataTable.jsx
src/features/admin/components/OrderDataList.jsx
```

컴포넌트를 나눌 때도 CSS는 만들지 마세요.

## 8단계: 데이터 키 설명

목업 전체:

```js
data.categories; // 카테고리
data.menus; // 메뉴
data.optionGroups; // 옵션 그룹
data.optionItems; // 옵션 항목
data.optionPolicies; // 옵션 정책
data.menuOptionPolicies; // 메뉴-옵션정책 연결
data.soldOutItems; // 품절 데이터
data.paymentMethods; // 결제수단
data.orders; // 주문
data.commonCodes; // 공통코드
data.adminSummary; // 관리자 요약
data.salesAnalytics; // 매출 통계
```

매출:

```js
data.salesAnalytics.salesDaily; // 일별 매출
data.salesAnalytics.salesHourly; // 시간대별 매출
data.salesAnalytics.topMenusDaily; // 일별 인기 메뉴
data.salesAnalytics.topMenusHourly; // 시간대별 인기 메뉴
```

매출 필드:

```js
salesDate; // 날짜
salesHour; // 시간
orderCount; // 주문 수
customerCount; // 고객 수
canceledOrderCount; // 취소 주문 수
grossSalesAmount; // 총매출
canceledAmount; // 취소 금액
netSalesAmount; // 순매출
quantity; // 판매 수량
salesAmount; // 메뉴 매출
```

## 백엔드 연결 시 교체 지점

백엔드가 생기면 페이지를 고치지 말고 아래만 바꾸세요.

```text
src/api/endpoints.js
src/store/useAdminStore.js
```

예상 API:

```text
GET /api/admin/menus
GET /api/admin/orders
GET /api/admin/sales/daily
GET /api/admin/sales/hourly
GET /api/admin/sales/top-menus/daily
GET /api/admin/sales/top-menus/hourly
GET /api/admin/sold-out-items
GET /api/payment-methods
```

## 완료 기준

아래가 모두 되면 완료입니다.

- 목업 JSON을 불러온다.
- `useAdminStore.js`에 데이터가 저장된다.
- `useAdminData.js` hook으로 데이터를 꺼낸다.
- `Dashboard.jsx`에서 매출/고객수/인기메뉴가 보인다.
- `MenuManage.jsx`에서 메뉴 목록이 보인다.
- `OrderManage.jsx`에서 주문 목록이 보인다.
- CSS를 추가하지 않았다.
- 디자인 작업을 하지 않았다.
