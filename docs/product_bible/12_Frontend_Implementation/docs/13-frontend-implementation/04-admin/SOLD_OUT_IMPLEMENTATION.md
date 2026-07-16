# Sold-out Frontend Implementation

## Draft

```js
{
  changes: []
}
```

## 흐름

```text
toggle
→ dirty change
→ affected count
→ SaveBar
→ ConfirmDialog
→ PATCH
→ Toast
```

## 위계

- Menu / Ingredient / Option = Tabs
- Category = Chips

## 기존 컴포넌트

Admin/Toast, ConfirmDialog, Filter components를 재사용.
