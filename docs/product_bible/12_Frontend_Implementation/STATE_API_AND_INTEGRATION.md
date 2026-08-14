# State, API, and Integration

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `API_ADAPTER_IMPLEMENTATION.md`
- `ERROR_MAPPING_IMPLEMENTATION.md`
- `MOCK_DATA_IMPLEMENTATION.md`
- `FRONT_BACK_CONTRACT_CHECKLIST.md`
- `INTEGRATION_SEQUENCE.md`

---

## 원문: `API_ADAPTER_IMPLEMENTATION.md`

### API Adapter Implementation

#### 목적

기존 Mock 기반 화면을 큰 수정 없이 실제 API로 교체한다.

#### 구조

```text
Page
→ feature hook
→ api adapter
→ Axios client
```

#### 예

```js
export const menuRepository = {
  async getMenuList(params) {
    const response = await kioskApi.getMenuList(params);
    return mapMenuListResponse(response.data);
  }
};
```

#### Mock 전환

```js
const dataSource =
  import.meta.env.VITE_USE_MOCK === "true"
    ? mockMenuRepository
    : menuRepository;
```

팀 일정에 따라 단순화 가능.

---

## 원문: `ERROR_MAPPING_IMPLEMENTATION.md`

### Error Mapping Implementation

#### Map

```js
export const ErrorMessageMap = {
  MENU_SOLD_OUT: {
    title: "선택한 메뉴가 품절되었어요.",
    actionLabel: "다른 메뉴 보기",
  },
};
```

#### 원칙

- raw server message 금지
- code 중심
- canRetry 반영
- Cart/draft 유지

---

## 원문: `MOCK_DATA_IMPLEMENTATION.md`

### Mock Data Implementation

#### 목적

Backend 미완성 상태에서도 UI·발표 흐름을 안정적으로 유지한다.

#### 위치

기존 `src/mocks` 구조를 우선한다.

#### 규칙

- API Response shape과 동일
- 날짜 중복 없음
- status code 동일
- amount integer
- KPI 정합성
- 16,800원 흐름 유지

#### 금지

Page 내부에 대량 더미데이터 직접 작성.

---

## 원문: `FRONT_BACK_CONTRACT_CHECKLIST.md`

### Front ↔ Back Contract Checklist

- [ ] URL
- [ ] HTTP method
- [ ] request field
- [ ] response field
- [ ] status code
- [ ] error code
- [ ] amount
- [ ] date/timezone
- [ ] pagination
- [ ] null policy
- [ ] loading
- [ ] empty
- [ ] error

---

## 원문: `INTEGRATION_SEQUENCE.md`

### Integration Sequence

1. Menu List
2. Menu Detail
3. Order Create
4. Payment
5. Complete
6. Active Orders
7. Order Status
8. Sold-out
9. Menu Management
10. Dashboard
11. Sales

한 API씩 Mock → 실제 응답으로 교체하고 회귀 테스트한다.
