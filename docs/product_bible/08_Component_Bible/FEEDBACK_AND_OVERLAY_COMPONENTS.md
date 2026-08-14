# Feedback and Overlay Components

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `CONFIRM_DIALOG.md`
- `STATUS_BADGE.md`
- `TOAST.md`

---

## 원문: `CONFIRM_DIALOG.md`

### ConfirmDialog

#### Tier / Owner

- Tier: Composite
- Owner: Shared
- Figma: `Shared/ConfirmDialog`

#### Use Cases

- Cart item delete
- Menu delete
- Sold-out save
- 전체 결제수단 비활성화
- 변경사항 폐기

#### Props

```js
{
  open,
  title,
  description,
  confirmLabel,
  cancelLabel,
  destructive,
  loading,
  onConfirm,
  onCancel
}
```

#### Rules

- Shared/Modal 중복 정리 전 삭제 금지
- destructive action만 danger 강조
- loading 중 닫기 정책 명확히

---

## 원문: `STATUS_BADGE.md`

### StatusBadge

#### Tier / Owner

- Tier: Primitive/Composite boundary
- Owner: Shared
- Figma: `Admin/StatusBadge`
- React: 기존 `OrderStatusBadge.jsx`가 있으면 확장

#### Values

```text
RECEIVED
PREPARING
COMPLETED
READY
APPROVED
FAILED
ENABLED
DISABLED
MAINTENANCE
```

#### Rules

- 상태 code와 label 분리
- 상태별 semantic color
- StatusChip 신규 생성 금지

---

## 원문: `TOAST.md`

### Toast

#### Tier / Owner

- Tier: Composite
- Owner: Shared/Admin
- Figma: `Admin/Toast` id 93:475

#### Variants

```text
success
deleted
loading
failed
```

#### Props

```js
{
  status,
  message,
  duration,
  actionLabel,
  onAction,
  onClose
}
```

#### Rules

- 성공 2~3초
- 실패는 사용자가 읽을 시간 제공
- 중요한 destructive confirm 대체 금지
- 서버 raw message 노출 금지
