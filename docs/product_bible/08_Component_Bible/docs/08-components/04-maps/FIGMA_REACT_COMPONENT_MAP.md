# Figma ↔ React Component Map

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

## Rule

이름이 달라도 역할이 같으면 기존 React 컴포넌트를 우선 확장한다.
