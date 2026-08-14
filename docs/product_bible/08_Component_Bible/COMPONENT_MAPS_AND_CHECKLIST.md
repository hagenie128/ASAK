# Component Maps and Checklist

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `COMPONENT_IMPLEMENTATION_CHECKLIST.md`
- `COMPONENT_OWNERSHIP_MATRIX.md`
- `FIGMA_REACT_COMPONENT_MAP.md`
- `SCREEN_COMPONENT_DEPENDENCY.md`

---

## 원문: `COMPONENT_IMPLEMENTATION_CHECKLIST.md`

### Component Implementation Checklist

- [ ] 기존 컴포넌트 검색
- [ ] Figma mapping 확인
- [ ] Owner 확인
- [ ] Tier 확인
- [ ] props contract
- [ ] state/variant
- [ ] token 사용
- [ ] accessibility
- [ ] loading/disabled/error
- [ ] no duplicate component
- [ ] 사용 화면 확인
- [ ] build/lint
- [ ] Story 또는 demo state
- [ ] QA

---

## 원문: `COMPONENT_OWNERSHIP_MATRIX.md`

### Component Ownership Matrix

| Component | Owner | Kiosk | Admin | Shared |
|---|---|---:|---:|---:|
| Button | Shared | O | O | O |
| Badge | Shared | O | O | O |
| Chip | Shared | O | O | O |
| BottomCTA | Kiosk | O | X | X |
| MenuCard | Kiosk | O | X | X |
| CartItemCard | Kiosk | O | X | X |
| PaymentMethodCard | Kiosk | O | X | X |
| OrderCard | Admin | X | O | X |
| SalesMetricCard | Admin | X | O | X |
| Toast | Shared/Admin | O | O | O |
| ConfirmDialog | Shared | O | O | O |
| FilterDropdown | Admin | X | O | X |
| DateRangePicker | Admin | X | O | X |

---

## 원문: `FIGMA_REACT_COMPONENT_MAP.md`

### Figma ↔ React Component Map

| Figma | React |
|---|---|
| Kiosk/BottomCTA | BottomCTA.jsx |
| menu-card | MenuCard.jsx |
| Kiosk/CartItemCard | CartItemCard.jsx 또는 기존 CartItem |
| Kiosk/PaymentMethodCard | PaymentMethodCard.jsx |
| Admin/OrderCard | OrderCard.jsx |
| Admin/StatusBadge | OrderStatusBadge.jsx 또는 StatusBadge.jsx |
| Admin/SalesMetricCard | SalesMetricCard.jsx |
| Admin/Toast | Toast.jsx |
| Shared/ConfirmDialog | ConfirmDialog.jsx |
| Admin/FilterDropdown | FilterDropdown.jsx |
| Admin/DateRangePicker | DateRangePicker.jsx |
| Admin/IngredientSelectModal | IngredientSelectModal.jsx |

#### Rule

이름이 달라도 역할이 같으면 기존 React 컴포넌트를 우선 확장한다.

---

## 원문: `SCREEN_COMPONENT_DEPENDENCY.md`

### Screen Component Dependency

#### SCR-005 Cart

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

#### SCR-009 Live Order Board

```text
LiveOrderBoardPage
├─ TtsControl
├─ OrderColumn
│  └─ OrderCard
│     ├─ StatusBadge
│     └─ Button
└─ Toast
```

#### SCR-022 Dashboard

```text
DashboardPage
├─ DashboardSummary
│  └─ SalesMetricCard
├─ ActiveOrderSummary
├─ PopularMenuList
└─ SoldOutSummary
```
