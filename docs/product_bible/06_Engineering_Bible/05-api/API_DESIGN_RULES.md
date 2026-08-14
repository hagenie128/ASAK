# API Design Rules

> Status: Current

## 1. URL

프로젝트 결정에 따라 camelCase 사용.

```text
/api/kiosk/menuList
/api/kiosk/menuDetail/{menuId}
/api/admin/paymentMethods
```

일반적인 REST 관례와 다르더라도 프로젝트 전 영역에서 일관성을 우선한다.

---

## 2. Method

| Purpose | Method |
|---|---|
| 조회 | GET |
| 생성 | POST |
| 일부 수정 | PATCH |
| 삭제 | DELETE |

---

## 3. Response Envelope

```json
{
  "success": true,
  "message": "OK",
  "data": {}
}
```

---

## 4. Error Response

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

## 5. Pagination

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

## 6. Filter

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

## 7. Date

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

## 8. Amount

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

## 9. Idempotency

적용 검토:

- 주문 생성
- 결제
- 주문 완료

Header 또는 request field 방식 중 하나를 선택한다.

---

## 10. Versioning

MVP에서 `/v1`을 반드시 넣을 필요는 없다.

외부 공개 API가 되거나 breaking change가 예상될 때 도입한다.
