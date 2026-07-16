# Canonical Contract Decisions

> Status: Current — human decision confirmed 2026-07-16. This document declares documentation contracts only; it does not authorize source changes in this phase.

## Repository ownership

- `ASAK-Admin` is the canonical repository for administrator implementation.
- Admin pages/components/API scaffolds inside `ASAK-Kiosk` are **Legacy Reference** and duplicate-review assets. Do not delete, move, or use them as the admin implementation source of truth.
- Product Bible remains at `ASAK/docs/product_bible`; do not rename it to `product-bible`.

## Canonical API paths

```text
GET   /api/kiosk/menuList
GET   /api/kiosk/menuDetail/{menuId}
POST  /api/kiosk/orders
POST  /api/kiosk/payments
PATCH /api/admin/soldOut
```

URL and API paths use camelCase. Existing constants are not changed in this documentation phase.

## Canonical Admin routes

```text
/
/orders/live
/orders
/soldOut
/menus
/paymentMethods
/sales
/sales/monthly
/sales/daily
```

## Canonical response fields and adapter rule

Canonical API fields are `totalAmount`, `approvedAmount`, `approvedAt`, and `waitingOrderCount`.

Existing Kiosk store fields `totalPrice`, `amount`, and `paidAt` must not be renamed now. A future API adapter maps canonical response fields at the boundary, preserving existing imports and store consumers.

## Mock data

The following are MVP Demo Data source assets and remain in place until a future shape/integrity update:

- `ASAK-Kiosk/public/mocks/kiosk.json`
- `ASAK-Admin/public/mocks/asak-admin-data.json`

Future mock edits must match canonical API response shape and keep sales KPI/chart/table totals and ratios consistent.
