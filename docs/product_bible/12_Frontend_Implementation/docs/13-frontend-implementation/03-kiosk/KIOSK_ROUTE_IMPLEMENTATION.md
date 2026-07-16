# Kiosk Route Implementation

## Routes

```text
/                  Home
/menu              Menu List
/menu/:menuId      Menu Detail
/cart              Cart
/payment           Payment
/complete          Complete
/accessibility     Accessibility
```

## Route Guard

### Payment

- Cart 없음 → Cart 또는 Home
- orderId 없음 → Cart

### Complete

- approved result 없음 → Home

## Navigation

승인 후 Complete는 replace navigation 권장.
