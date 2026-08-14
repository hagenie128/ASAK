# API, Backend, and Data Test Suite

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `API_CONTRACT_TESTS.md`
- `BACKEND_BUSINESS_RULE_TESTS.md`
- `DATA_INTEGRITY_TESTS.md`

---

## 원문: `API_CONTRACT_TESTS.md`

### API Contract Tests

#### 공통

- response envelope
- JSON camelCase
- status UPPER_SNAKE_CASE
- amount integer
- date ISO

#### Order

- create
- detail
- status update
- invalid transition
- price changed

#### Payment

- approved
- failed
- disabled method
- already approved
- idempotency

#### Menu

- list
- detail
- sold-out
- invalid option

#### Admin

- dashboard
- orders
- soldOut
- menus
- sales

---

## 원문: `BACKEND_BUSINESS_RULE_TESTS.md`

### Backend Business Rule Tests

#### Price Authority

- client amount tamper
- server recalculation
- mismatch rejection

#### Transaction

- Order + Item + Option rollback
- Sold-out batch rollback
- Menu relation rollback

#### Status Transition

- valid
- invalid
- duplicate

#### Validation

- Bean Validation
- Service Validation
- DB Constraint

#### History

- Menu rename 후 과거 Order snapshot 유지
- soft delete 후 history 유지

---

## 원문: `DATA_INTEGRITY_TESTS.md`

### Data Integrity Tests

#### Money

- integer
- no floating
- thousand separator UI

#### Relations

- FK validity
- orphan 없음
- shared Ingredient cascade delete 금지

#### Order Snapshot

- menuName
- unitAmount
- lineAmount

#### Sales

- approved only
- refund/cancel policy
- timezone Asia/Seoul

#### Seed / Mock

- duplicate date 없음
- category code 일치
- ratio 100%
- totals match
