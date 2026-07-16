# Component System

## Tier

### Tier 1 — Primitive

작은 UI 단위.

- Button
- IconButton
- Input
- Checkbox
- Radio
- Switch
- Badge
- Chip
- Divider
- Spinner

### Tier 2 — Composite

Primitive 조합.

- BottomCTA
- MenuCard
- CartItemCard
- PaymentMethodCard
- OrderCard
- SalesMetricCard
- Toast
- ConfirmDialog
- FilterDropdown

### Tier 3 — Section

화면의 의미 단위.

- CategoryTabs
- OrderSummary
- MenuGrid
- DashboardSummary
- OrderTable
- SalesChartSection
- MenuFormSection

### Tier 4 — Screen

Route 단위.

- SCR-001~SCR-024

## Dependency Rule

```text
Screen
→ Section
→ Composite
→ Primitive
```

반대 의존 금지.

Primitive가 특정 Screen을 import하지 않는다.

## Ownership

```text
Shared
Kiosk
Admin
```

같은 역할의 컴포넌트를 Kiosk/Admin에 중복 생성하지 않는다.
