# API Contract Tests

## 공통

- response envelope
- JSON camelCase
- status UPPER_SNAKE_CASE
- amount integer
- date ISO

## Order

- create
- detail
- status update
- invalid transition
- price changed

## Payment

- approved
- failed
- disabled method
- already approved
- idempotency

## Menu

- list
- detail
- sold-out
- invalid option

## Admin

- dashboard
- orders
- soldOut
- menus
- sales
