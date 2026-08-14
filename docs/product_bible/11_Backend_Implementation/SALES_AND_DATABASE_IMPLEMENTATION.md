# Sales and Database Implementation

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `SALES_IMPLEMENTATION.md`
- `SCHEMA_IMPLEMENTATION_ORDER.md`
- `SEED_DATA_GUIDE.md`

---

## 원문: `SALES_IMPLEMENTATION.md`

### Sales Implementation

#### 데이터 정의

```text
고객 수 = 결제 승인 건수
평균 객단가 = 총매출 / 고객 수
```

#### Endpoints

```http
GET /api/admin/sales/summary
GET /api/admin/sales/monthly
GET /api/admin/sales/daily
```

#### Mock Data

현재 포트폴리오용 Mock Data를 사용할 수 있다.

단:

- KPI 합계
- 차트 합계
- 표 합계
- 비율 100%
- 비교율

은 반드시 일치시킨다.

#### 실제 query 구현 시

- paymentStatus = APPROVED
- Asia/Seoul date boundary
- amount integer
- group by date/hour/menu/category

---

## 원문: `SCHEMA_IMPLEMENTATION_ORDER.md`

### Schema Implementation Order

1. category
2. ingredient_category
3. ingredient
4. allergen
5. option_group
6. option_item
7. menu
8. menu_ingredient
9. menu_option_group
10. order
11. order_item
12. order_item_option
13. payment_method
14. payment

#### 이유

참조되는 마스터 데이터부터 만든다.

#### 확인

- FK
- unique
- null
- default
- index
- soft delete

---

## 원문: `SEED_DATA_GUIDE.md`

### Seed Data Guide

#### 목적

Kiosk/Admin/매출 화면을 동일한 데이터로 시연한다.

#### Seed 포함

- categories
- ingredients
- option groups
- menus
- payment methods
- orders
- payments

#### 정합성

- 메뉴 가격과 Cart 금액 일치
- 8,400원 × 2 = 16,800원
- approved payments와 Sales 합계 일치
- 고객 수 = approved payment count
- 시간대 합계 일치
