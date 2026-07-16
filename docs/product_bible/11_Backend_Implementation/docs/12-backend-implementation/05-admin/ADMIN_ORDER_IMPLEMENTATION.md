# Admin Order Implementation

## Active Orders

```http
GET /api/admin/orders/active
```

조건:

```text
status IN (RECEIVED, PREPARING)
```

정렬:

```text
createdAt ASC
```

## Order List

```http
GET /api/admin/orders
```

Filter:

- status
- orderType
- startDate
- endDate
- keyword
- page
- size

## Order Detail

- items
- options
- payment
- timestamps
