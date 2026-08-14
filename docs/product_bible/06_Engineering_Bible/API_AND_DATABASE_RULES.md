# API and Database Rules

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `DATABASE_ENGINEERING_RULES.md`
- `API_DESIGN_RULES.md`
- `API_REVIEW_CHECKLIST.md`

---

## 원문: `DATABASE_ENGINEERING_RULES.md`

### Database Engineering Rules

> Status: Current

#### 1. Naming

```text
snake_case
```

##### Table

```text
order_item
order_item_option
payment_method
ingredient_category
```

##### Column

```text
created_at
updated_at
menu_id
order_status
```

---

#### 2. Key

PK:

```text
id
```

FK:

```text
menu_id
order_id
ingredient_id
```

---

#### 3. Index Naming

```text
idx_order_created_at
idx_order_status
idx_menu_category_id
```

Unique:

```text
uk_menu_name
uk_payment_method_code
```

---

#### 4. Common Columns

필요 시:

```text
created_at
updated_at
created_by
updated_by
```

모든 테이블에 무조건 넣지 않고 운영 필요에 따라 선택한다.

---

#### 5. Status Storage

API/Java enum과 동일한 UPPER_SNAKE_CASE code.

예:

```text
RECEIVED
PREPARING
COMPLETED
```

---

#### 6. Money

정수 단위 원화:

```text
INT 또는 BIGINT
```

소수 floating type 금지.

---

#### 7. Historical Integrity

과거 OrderItem은 당시 메뉴명·가격을 snapshot으로 보관하는 것을 권장한다.

메뉴 이름이 바뀌어도 과거 주문이 변하면 안 된다.

---

#### 8. Foreign Key

관계는 명확히 하되 삭제 정책을 신중히 설정한다.

Menu 삭제가 Order history를 cascade delete하면 안 된다.

---

#### 9. Migration

스키마 변경은 문서만 수정하지 않는다.

- migration
- seed
- API contract
- Figma field
- QA

를 함께 갱신한다.

---

## 원문: `API_DESIGN_RULES.md`

### API Design Rules

> Status: Current

#### 1. URL

프로젝트 결정에 따라 camelCase 사용.

```text
/api/kiosk/menuList
/api/kiosk/menuDetail/{menuId}
/api/admin/paymentMethods
```

일반적인 REST 관례와 다르더라도 프로젝트 전 영역에서 일관성을 우선한다.

---

#### 2. Method

| Purpose | Method |
|---|---|
| 조회 | GET |
| 생성 | POST |
| 일부 수정 | PATCH |
| 삭제 | DELETE |

---

#### 3. Response Envelope

```json
{
  "success": true,
  "message": "OK",
  "data": {}
}
```

---

#### 4. Error Response

```json
{
  "success": false,
  "message": "MENU_SOLD_OUT",
  "data": {
    "field": null,
    "targetId": 1,
    "canRetry": true
  }
}
```

---

#### 5. Pagination

Query:

```text
page
size
sort
```

Response:

```json
{
  "content": [],
  "page": 0,
  "size": 20,
  "totalElements": 100,
  "totalPages": 5
}
```

0-based 또는 1-based를 프로젝트 전체에서 통일한다.

Spring 기본과 맞추려면 0-based가 단순하다.

---

#### 6. Filter

```text
status
categoryCode
orderType
startDate
endDate
keyword
```

빈 문자열과 null 처리 규칙을 통일한다.

---

#### 7. Date

```text
YYYY-MM-DD
```

Datetime:

```text
ISO-8601
```

매장 timezone:

```text
Asia/Seoul
```

---

#### 8. Amount

```text
integer
```

API field:

```text
totalAmount
approvedAmount
additionalAmount
```

---

#### 9. Idempotency

적용 검토:

- 주문 생성
- 결제
- 주문 완료

Header 또는 request field 방식 중 하나를 선택한다.

---

#### 10. Versioning

MVP에서 `/v1`을 반드시 넣을 필요는 없다.

외부 공개 API가 되거나 breaking change가 예상될 때 도입한다.

---

## 원문: `API_REVIEW_CHECKLIST.md`

### API Review Checklist

- [ ] URL camelCase
- [ ] HTTP method 적절
- [ ] Request/Response 분리
- [ ] Entity 미노출
- [ ] amount integer
- [ ] date ISO
- [ ] status UPPER_SNAKE_CASE
- [ ] error code
- [ ] validation
- [ ] pagination
- [ ] filter naming
- [ ] idempotency 필요 여부
- [ ] Figma field mapping
- [ ] React API module mapping
- [ ] DB source 확인
