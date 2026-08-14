# API Adapter Implementation

## 목적

기존 Mock 기반 화면을 큰 수정 없이 실제 API로 교체한다.

## 구조

```text
Page
→ feature hook
→ api adapter
→ Axios client
```

## 예

```js
export const menuRepository = {
  async getMenuList(params) {
    const response = await kioskApi.getMenuList(params);
    return mapMenuListResponse(response.data);
  }
};
```

## Mock 전환

```js
const dataSource =
  import.meta.env.VITE_USE_MOCK === "true"
    ? mockMenuRepository
    : menuRepository;
```

팀 일정에 따라 단순화 가능.
