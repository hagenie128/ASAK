# Error Mapping Implementation

## Map

```js
export const ErrorMessageMap = {
  MENU_SOLD_OUT: {
    title: "선택한 메뉴가 품절되었어요.",
    actionLabel: "다른 메뉴 보기",
  },
};
```

## 원칙

- raw server message 금지
- code 중심
- canRetry 반영
- Cart/draft 유지
