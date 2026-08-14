# Frontend API Client Rules

> Status: Current

## 1. Axios Client

공통 설정:

- baseURL
- timeout
- JSON headers
- response unwrap
- error normalization

---

## 2. Page에서 URL 직접 작성 금지

나쁜 예:

```js
axios.get("/api/kiosk/menuList");
```

권장:

```js
const data = await kioskApi.getMenuList(params);
```

---

## 3. API Module

```js
export const kioskApi = {
  getMenuList: (params) =>
    apiClient.get("/api/kiosk/menuList", { params }),

  createOrder: (payload) =>
    apiClient.post("/api/kiosk/orders", payload),
};
```

---

## 4. Response Envelope

```json
{
  "success": true,
  "message": "OK",
  "data": {}
}
```

Frontend는 공통 함수로 `data`를 unwrap한다.

---

## 5. Error Normalization

```js
{
  code: "MENU_SOLD_OUT",
  message: "MENU_SOLD_OUT",
  field: null,
  canRetry: true,
  originalError: error
}
```

사용자 문구는 `errorMessageMap`에서 결정한다.

서버 raw message를 직접 노출하지 않는다.

---

## 6. Request Cancellation

검색·필터처럼 빠르게 바뀌는 요청은 AbortController 또는 최신 요청 우선 정책을 사용한다.

---

## 7. Duplicate Request

- 결제
- 주문 생성
- 저장
- 상태 변경

은 `isSubmitting`으로 중복 방지한다.
