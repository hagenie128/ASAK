# Backend Test Operations

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `API_SMOKE_CHECKLIST.md`
- `BACKEND_TEST_PLAN.md`

---

## 원문: `API_SMOKE_CHECKLIST.md`

### API Smoke Checklist

- [ ] GET menuList
- [ ] GET menuDetail
- [ ] POST order
- [ ] GET paymentMethods
- [ ] POST payment
- [ ] GET active orders
- [ ] PATCH order status
- [ ] GET dashboard
- [ ] PATCH soldOut
- [ ] CRUD menus
- [ ] GET sales summary

---

## 원문: `BACKEND_TEST_PLAN.md`

### Backend Test Plan

#### Unit

- price calculation
- option validation
- status transition
- sold-out propagation
- average order value

#### Repository

- active menu query
- active order query
- sales aggregation
- popular menu ranking

#### Integration

- create order transaction
- payment duplicate prevention
- menu soft delete
- sold-out batch rollback

#### Controller

- request validation
- status code
- response envelope
- error code
