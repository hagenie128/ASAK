# Sales Cancellation and Refund Rules

> Status: Current (2026-07-23)
> Related: API-024, DEV-ORDER-002, SCR-010, SCR-019, SCR-020, SCR-021

## 1. Timestamp preservation

- `payment.paid_at` is the original approval time. A later cancellation or refund must not erase it.
- `orders.canceled_at` records when an order is cancelled.
- `payment.refunded_at` records when an approved payment is refunded.

## 2. Cancellation state transition

Only orders in `RECEIVED` or `PREPARING` may be cancelled.

1. Set the order status to `CANCELED` and populate `orders.canceled_at`.
2. If the payment was approved, retain `payment.paid_at`, set the payment status to `REFUNDED`, and populate `payment.refunded_at`.
3. A completed or already-cancelled order returns `409 ORDER_CANCEL_NOT_ALLOWED`.

## 3. Sales aggregation

- Gross sales includes every payment with a non-null `paid_at`, including a payment later refunded.
- Cancelled amount includes only a paid transaction whose order is `CANCELED` or whose payment is `CANCELED` or `REFUNDED`.
- Net sales equals gross sales minus cancelled amount. A fully refunded payment therefore contributes zero net sales, never a negative amount.
- Sales date and hour use the original `paid_at`; an unpaid cancellation falls back to the order creation timestamp only for cancellation counts.

## 4. Menu sales and ranking

`vw_top_menu_daily` and `vw_top_menu_hourly` include an item only when:

- `payment.paid_at` is not null;
- the order status is not `CANCELED`; and
- the payment status is neither `CANCELED` nor `REFUNDED`.

Cancelled or refunded order items must not affect menu quantity, order count, sales amount, or popularity ranking.

## 5. Verification

- No row in `vw_sales_daily` or `vw_sales_hourly` may have negative `net_sales_amount`.
- The sales views and top-menu views must use the same cancellation/refund predicates.
