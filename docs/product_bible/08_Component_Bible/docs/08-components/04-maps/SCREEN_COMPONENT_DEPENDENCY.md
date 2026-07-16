# Screen Component Dependency

## SCR-005 Cart

```text
CartPage
├─ CartItemList
│  └─ CartItemCard
│     ├─ QuantityControl
│     └─ Button
├─ OrderSummary
├─ BottomCTA
└─ ConfirmDialog
```

## SCR-009 Live Order Board

```text
LiveOrderBoardPage
├─ TtsControl
├─ OrderColumn
│  └─ OrderCard
│     ├─ StatusBadge
│     └─ Button
└─ Toast
```

## SCR-022 Dashboard

```text
DashboardPage
├─ DashboardSummary
│  └─ SalesMetricCard
├─ ActiveOrderSummary
├─ PopularMenuList
└─ SoldOutSummary
```
