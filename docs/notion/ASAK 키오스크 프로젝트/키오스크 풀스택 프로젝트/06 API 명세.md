# 06. API 명세

<aside>
🎯

Week 5 MVP: 고객 키오스크 주문 흐름(API-001~006) 완성이 최우선. 장치·멤버십·실결제·상세통계는 후반 확장.

</aside>

## 작성 체크리스트

- [ ]  API ID를 작성했는가?
- [ ]  Method와 URL이 명확한가?
- [ ]  Request Body 또는 Query String 예시가 있는가?
- [ ]  성공 Response Body 예시가 있는가?
- [ ]  실패 Response Body 예시가 있는가?
- [ ]  모든 응답이 `success`, `status`, `code`, `message`, `data` 구조를 따르는가?
- [ ]  관련 테이블을 적었는가?
- [ ]  처리 내용을 단계별로 적었는가?
- [ ]  화면 설계와 연결되는 API인지 확인했는가?
- [ ]  Week 5 MVP 범위 밖 API를 9주 로드맵의 확장 기능으로 분리했는가?

[API 명세 데이터베이스](06%20API%20%EB%AA%85%EC%84%B8/API%20%EB%AA%85%EC%84%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4.csv)

---

# Part 0 — 공통

모든 API 응답은 아래 JSON 구조를 기준으로 맞춥니다.

## 성공 응답 기본형

```json
{
  "success": true,
  "status": 200,
  "code": "SUCCESS_CODE",
  "message": "요청이 성공했습니다.",
  "data": {}
}
```

## 실패 응답 기본형

```json
{
  "success": false,
  "status": 400,
  "code": "ERROR_CODE",
  "message": "요청 처리에 실패했습니다.",
  "data": null
}
```

## 작성 규칙

- `success`: 성공 여부를 boolean으로 표시합니다.
- `status`: HTTP 상태 코드를 숫자로 표시합니다.
- `code`: 프론트엔드에서 분기 처리할 수 있는 영문 상수 코드입니다.
- `message`: 화면에 보여주거나 디버깅에 참고할 수 있는 한국어 메시지입니다.
- `data`: 실제 응답 데이터입니다. 실패 시 `null`로 통일합니다.
- 목록 조회 응답도 `data` 안에 배열을 넣습니다.
- Week 5 MVP(API-001~009)에서는 별도 인증 없음(`인증=N`). 관리자 API는 후반 JWT/세션 적용 예정.
- 공통 헤더: `Content-Type: application/json` (POST/PATCH), `Accept: application/json`
- 에러 처리: HTTP status + envelope `success=false`, `code`로 프론트 분기. 4xx=클라이언트, 5xx=서버.

---

## 읽기 순서 (TOC)

1. **Part 0 — 공통** — ApiResponse envelope · 인증·공통 헤더·에러 처리
2. **Part 1 — 고객 키오스크 (Week 5 MVP)** — API-001 카테고리 → 002 메뉴목록 → 003 메뉴상세 → 004 옵션 → 005 주문생성 → 006 결제
3. **Part 2 — 관리자 (Week 6)** — API-007 주문목록 → 008 상태변경 → 009 품절
4. **Part 3 — Week 7~8 확장** — API-010~017 (하단 details) · API-018~020 (장치/멤버십)

---

# Part 1 — 고객 키오스크 (Week 5 MVP)

키오스크 주문 흐름 순서: **카테고리 → 메뉴목록 → 메뉴상세 → 옵션 → 주문생성 → 결제**

| 번호 | 구분 | 기능명 | Method | URL | 관련 테이블 | 상태 |
| --- | --- | --- | --- | --- | --- | --- |
| API-001 | 키오스크 | 카테고리 목록 조회 | GET | /api/categories | category | 필수 |
| API-002 | 키오스크 | 메뉴 목록 조회 | GET | /api/menus | menu, category, menu_ingredient, ingredient | 필수 |
| API-003 | 키오스크 | 메뉴 상세 조회 | GET | /api/menus/{menuId} | menu, menu_ingredient, ingredient, ingredient_allergen, allergen | 필수 |
| API-004 | 키오스크 | 메뉴 옵션 조회 | GET | /api/menus/{menuId}/options | menu_option_group, menu_option, option_group, option_item, ingredient, common_code | 필수 |
| API-005 | 주문 | 주문 생성 | POST | /api/orders | orders, order_item, order_item_option, item_exclusion, common_code | 필수 |
| API-006 | 결제 | 가상 결제 처리 | POST | /api/payments | payment, orders, common_code | 필수 |

# Part 2 — 관리자 (Week 6)

| 번호 | 구분 | 기능명 | Method | URL | 관련 테이블 | 상태 |
| --- | --- | --- | --- | --- | --- | --- |
| API-007 | 관리자 | 관리자 주문 목록/상세 조회 | GET | /api/admin/orders | orders, order_item, order_item_option, item_exclusion, menu, option_item, payment, common_code | 필수 |
| API-008 | 관리자 | 관리자 주문 상태 변경 | PATCH | /api/admin/orders/{orderId}/status | orders, common_code | 필수 |
| API-009 | 관리자 | 판매 항목 품절 상태 변경 | PATCH | /api/admin/sold-out-items | menu, ingredient, option_item, menu_ingredient, menu_option_group, common_code | 옵션 |

> API URL은 `/api` prefix를 포함한 실제 구현 기준으로 작성합니다. 화면/요구사항 문서에서 `/categories`처럼 적힌 경우도 실제 구현 시에는 `/api/categories`로 맞춥니다.
> 

---

# 상태값 기준

> DB에는 상태값 문자열을 직접 저장하지 않고 `code_group`, `common_code`에 등록한 값을 FK로 저장합니다. API 요청/응답에서는 아래 코드 문자열을 그대로 사용합니다.
> 

| 구분 | 값 | 설명 |
| --- | --- | --- |
| 주문상태 | RECEIVED | 주문 접수 |
| 주문상태 | PREPARING | 준비중 |
| 주문상태 | COMPLETED | 완료 |
| 결제상태 | READY | 결제 대기 |
| 결제상태 | APPROVED | 가상 결제 승인 |
| 결제상태 | FAILED | 가상 결제 실패 |
| 주문유형 | EAT_IN | 먹고가기 |
| 주문유형 | TAKE_OUT | 포장 |

---

# Part 1 상세 - API-001. 카테고리 목록 조회

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URL | /api/categories |
| 인증 필요 여부 | N |
| 사용 화면 | 메뉴 선택 화면 |
| 관련 테이블 | category |

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "CATEGORY_LIST_SUCCESS",
  "message": "카테고리 목록 조회 성공",
  "data": [
    {
      "categoryId": 231,
      "name": "신메뉴",
      "sortOrder": 0
    },
    {
      "categoryId": 236,
      "name": "샌드위치",
      "sortOrder": 1
    },
    {
      "categoryId": 233,
      "name": "샐러디·볼",
      "sortOrder": 2
    },
    {
      "categoryId": 235,
      "name": "랩",
      "sortOrder": 3
    },
    {
      "categoryId": 234,
      "name": "프로틴",
      "sortOrder": 5
    },
    {
      "categoryId": 232,
      "name": "기타",
      "sortOrder": 8
    }
  ]
}
```

## 실패 응답 예시

```json
{
  "success": false,
  "status": 500,
  "code": "CATEGORY_LIST_FAILED",
  "message": "카테고리 목록 조회 중 오류가 발생했습니다.",
  "data": null
}
```

## 처리 내용

1. category 테이블에서 sort_order 기준으로 카테고리를 조회한다.
2. 키오스크 상단 탭에 사용할 형태로 반환한다.

---

# API-002. 메뉴 목록 조회

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URL | /api/menus |
| 인증 필요 여부 | N |
| 사용 화면 | 메뉴 선택 화면 |
| 관련 테이블 | menu, category, menu_ingredient, ingredient |

## 요청 데이터

| 이름 | 위치 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- | --- |
| categoryId | Query | Long | N | 카테고리 필터 |

요청 예시:

```
GET /api/menus?categoryId=233
```

> categoryId 예시: 231=신메뉴, 236=샌드위치, 233=샐러디·볼, 235=랩, 234=프로틴, 232=기타 (`category.json` seed 기준)
> 

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "MENU_LIST_SUCCESS",
  "message": "메뉴 목록 조회 성공",
  "data": [
    {
      "menuId": 364,
      "categoryId": 231,
      "name": "스파이시 쉬림프 샌드위치",
      "price": 8900,
      "imageUrl": "/assets/menu/364.png",
      "baseKcal": 464,
      "isSoldOut": false,
      "hasSoldOutIngredient": false,
      "soldOutReason": null,
      "soldOutBadges": []
    }
  ]
}
```

> seed: menu 364 · category 231(신메뉴) · menu_nutrition kcal 463.7→464
> 

## 실패 응답 예시

```json
{
  "success": false,
  "status": 404,
  "code": "CATEGORY_NOT_FOUND",
  "message": "존재하지 않는 카테고리입니다.",
  "data": null
}
```

## 처리 내용

1. categoryId가 있으면 해당 카테고리의 메뉴만 조회한다.
2. `menu.is_sold_out`과 기본 재료 품절 여부를 함께 계산해 isSoldOut, hasSoldOutIngredient를 반환한다.
3. CORE 또는 BASE 역할의 기본 재료가 품절이면 isSoldOut=true로 내려준다.
4. DEFAULT 역할의 기본 재료가 품절이면 isSoldOut=false, hasSoldOutIngredient=true로 내려준다.
5. 재료 칼로리 합산값(baseKcal)을 포함해 카드 UI에 필요한 최소 정보를 반환한다.

---

# API-003. 메뉴 상세 조회

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URL | /api/menus/{menuId} |
| 인증 필요 여부 | N |
| 사용 화면 | 메뉴 상세 / 옵션 선택 화면 |
| 관련 테이블 | menu, menu_ingredient, ingredient, ingredient_allergen, allergen |

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "MENU_DETAIL_SUCCESS",
  "message": "메뉴 상세 조회 성공",
  "data": {
    "menuId": 364,
    "categoryId": 231,
    "name": "스파이시 쉬림프 샌드위치",
    "price": 8900,
    "imageUrl": "/assets/menu/364.png",
    "description": "케이준 쉬림프, 할라피뇨, 토마토, 슈레드치즈, 화이트치즈 · 기본 드레싱: 크리미칠리",
    "baseKcal": 464,
    "ingredients": [
      { "ingredientId": 155, "name": "케이준쉬림프", "canRemove": false, "isSoldOut": false },
      { "ingredientId": 105, "name": "크리미칠리", "canRemove": true, "isSoldOut": false },
      { "ingredientId": 377, "name": "화이트치즈", "canRemove": true, "isSoldOut": false }
    ],
    "allergens": [],
    "allergyText": "",
    "isSoldOut": false,
    "hasSoldOutIngredient": false,
    "isOrderable": true,
    "soldOutReason": null,
    "soldOutBadges": []
  }
}
```

> 예시: `GET /api/menus/364` · seed `menu.json` id=364, `category.json` id=231(신메뉴)
> 

## 실패 응답 예시

```json
{
  "success": false,
  "status": 404,
  "code": "MENU_NOT_FOUND",
  "message": "존재하지 않는 메뉴입니다.",
  "data": null
}
```

## 처리 내용

1. menuId로 메뉴를 조회한다.
2. 기본 재료는 menu_ingredient, ingredient를 조인해 반환한다.
3. 기본/추천 드레싱은 메뉴별 설정값인 `menu_option.is_default`, `menu_option.is_recommended` 기준으로 확인한다.
4. 알레르기 정보는 menu_ingredient, ingredient, ingredient_allergen, allergen을 조인해 allergyText로 가공해 반환한다.
5. baseKcal은 DB 컬럼이 아니라 기본 재료의 kcal 합산값으로 계산해 반환한다.
6. isOrderable은 `menu.is_sold_out`과 CORE/BASE 재료 품절 여부를 기준으로 계산한다.

---

# API-004. 메뉴 옵션 조회

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URL | /api/menus/{menuId}/options |
| 인증 필요 여부 | N |
| 사용 화면 | 옵션 선택 화면 |
| 관련 테이블 | menu_option_group, menu_option, option_group, option_item, ingredient, common_code |

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "MENU_OPTIONS_SUCCESS",
  "message": "메뉴 옵션 조회 성공",
  "data": [
    {
      "optionGroupId": 240,
      "name": "드레싱 선택",
      "groupType": "DRESSING",
      "selectType": "SINGLE",
      "minSelect": 1,
      "maxSelect": 1,
      "sortOrder": 1,
      "isRequired": true,
      "items": [
        {
          "optionItemId": 269,
          "ingredientId": 105,
          "name": "크리미칠리",
          "extraPrice": 0,
          "originalPrice": null,
          "extraKcal": 235,
          "servingAmount": 50,
          "servingUnit": "g",
          "proteinG": 0,
          "iconUrl": null,
          "colorHex": null,
          "isRecommended": true,
          "isDefault": true,
          "isSoldOut": false
        },
        {
          "optionItemId": 247,
          "ingredientId": 219,
          "name": "(저당) 들기름소이",
          "extraPrice": 0,
          "originalPrice": null,
          "extraKcal": null,
          "servingAmount": 50,
          "servingUnit": "g",
          "proteinG": null,
          "iconUrl": null,
          "colorHex": null,
          "isRecommended": false,
          "isDefault": false,
          "isSoldOut": false
        }
      ]
    }
  ]
}
```

> 예시: `GET /api/menus/364/options` · seed option_group 240, option_item 269(기본), 247
> 

## 실패 응답 예시

```json
{
  "success": false,
  "status": 404,
  "code": "MENU_NOT_FOUND",
  "message": "존재하지 않는 메뉴입니다.",
  "data": null
}
```

## 처리 내용

1. menuId로 menu_option_group을 조회해 해당 메뉴가 참조하는 option_group 목록을 가져온다.
2. 각 option_group에 포함된 option_item을 함께 반환하되, 메뉴별 추천/기본 선택 여부는 menu_option에서 조회한다.
3. 프론트엔드는 menu_option_group.sort_order, is_required와 option_group의 groupType, minSelect, maxSelect 기준으로 선택 가능 여부와 노출 순서를 제어한다.
4. extraKcal은 DB 컬럼이 아니라 option_item에 연결된 ingredient.kcal 기준으로 계산해 반환한다. 단, 화면 표시용 제공량/단위/아이콘/색상은 option_item의 amount, unit_id, icon_url, color_hex 값을 API 응답용 servingAmount, servingUnit, iconUrl, colorHex로 가공해 반환한다. proteinG는 ingredient.protein_g 기준으로 계산한다.
5. option_item에 연결된 `ingredient.is_sold_out=true`이면 해당 옵션 항목만 선택 불가로 반환한다.
6. 세트 구성은 groupType=SET_SIDE 옵션그룹과 groupType=SET_DRINK 옵션그룹을 각각 두고, 고객이 사이드와 음료를 따로 선택하도록 처리한다. 각 선택 항목의 추가금액은 option_item.extraPrice로 계산하고, 할인 전 금액 표시는 originalPrice를 사용한다.
7. 기본 메뉴에 이미 포함된 핵심 재료도 추가 토핑으로 선택할 수 있다. 이 경우 기본 포함량은 `menu_ingredient`, 추가 선택량은 `order_item_option.quantity`로 분리해 처리한다.

---

# API-005. 주문 생성

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | POST |
| URL | /api/orders |
| 인증 필요 여부 | N |
| 사용 화면 | 장바구니 / 주문 확인 화면 |
| 관련 테이블 | orders, order_item, order_item_option, item_exclusion, common_code |

## 요청 예시

```json
{
  "orderType": "TAKE_OUT",
  "items": [
    {
      "menuId": 364,
      "quantity": 1,
      "optionItems": [
        { "optionItemId": 269, "quantity": 1 }
      ],
      "excludedIngredientIds": [169]
    }
  ]
}
```

> seed: menu 364, option_item 269(크리미칠리), ingredient 169(양파) 제외
> 

## 성공 응답 예시

```json
{
  "success": true,
  "status": 201,
  "code": "ORDER_CREATE_SUCCESS",
  "message": "주문 생성 성공",
  "data": {
    "orderId": 1,
    "orderNo": "ASAK-20260703-001",
    "orderType": "TAKE_OUT",
    "orderStatus": "RECEIVED",
    "totalPrice": 8900
  }
}
```

## 실패 응답 예시

```json
{
  "success": false,
  "status": 400,
  "code": "ORDER_INVALID",
  "message": "주문 정보가 올바르지 않습니다.",
  "data": null
}
```

```json
{
  "success": false,
  "status": 409,
  "code": "MENU_SOLD_OUT",
  "message": "품절된 메뉴가 포함되어 있습니다.",
  "data": null
}
```

## 처리 내용

1. orderType이 EAT_IN 또는 TAKE_OUT인지 검증한다.
2. menuId와 optionItems.optionItemId가 유효한지 검증한다.
3. 품절 메뉴, CORE/BASE 재료 품절 메뉴, 품절 옵션 항목이 포함되어 있으면 실패 응답을 반환한다. DEFAULT 재료 품절은 화면 뱃지로 안내하되 주문 생성 자체는 허용한다.
4. 메뉴 가격과 옵션 추가 금액으로 총액을 계산한다. 기본 재료 제외는 금액 차감 없이 알레르기/표시 정보에만 반영한다.
5. orders, order_item, order_item_option에 주문 정보와 옵션 수량을 저장한다. order_item_option은 `00주문 안의 00메뉴에 선택된 00옵션`을 저장하는 테이블이며, 주문번호(order_no)는 중복 저장하지 않고 `order_item → orders` 조인으로 확인한다. 같은 재료가 기본 재료와 추가 토핑 양쪽에 있더라도 기본 포함분은 메뉴 구성으로 보고, 추가분만 order_item_option.quantity에 저장한다.
6. 기본 메뉴에 포함된 재료 중 고객이 제외한 재료가 있으면 item_exclusion에 저장한다.
7. 주문번호와 총액을 반환한다.

---

# API-006. 가상 결제 처리

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | POST |
| URL | /api/payments |
| 인증 필요 여부 | N |
| 사용 화면 | 결제 화면 |
| 관련 테이블 | payment, orders, common_code |

## 요청 예시

```json
{
  "orderId": 1,
  "paymentMethod": "CARD",
  "amount": 8900
}
```

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "PAYMENT_APPROVED",
  "message": "가상 결제가 승인되었습니다.",
  "data": {
    "paymentId": 1,
    "orderId": 1,
    "orderNo": "ASAK-20260703-001",
    "amount": 8900,
    "paymentStatus": "APPROVED",
    "paidAt": "2026-07-03T13:30:00"
  }
}
```

## 실패 응답 예시

```json
{
  "success": false,
  "status": 404,
  "code": "ORDER_NOT_FOUND",
  "message": "존재하지 않는 주문입니다.",
  "data": null
}
```

```json
{
  "success": false,
  "status": 400,
  "code": "PAYMENT_AMOUNT_MISMATCH",
  "message": "결제 금액과 주문 금액이 일치하지 않습니다.",
  "data": null
}
```

## 처리 내용

1. orderId로 주문을 조회한다.
2. 요청 amount와 주문 total_price가 일치하는지 검증한다.
3. 실제 PG 연동 없이 payment.method_id와 payment.status_id를 저장한다.
4. 결제 결과를 반환한다.

---

# Part 2 상세 - API-007. 관리자 주문 목록/상세 조회

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | GET |
| URL | /api/admin/orders |
| 인증 필요 여부 | Week 5 MVP에서는 N, 이후 관리자 인증 적용 |
| 사용 화면 | 관리자 주문 관리 / 관리자 주문 상세 화면 |
| 관련 테이블 | orders, order_item, order_item_option, item_exclusion, menu, option_item, payment, common_code |

## 요청 데이터

| 이름 | 위치 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- | --- |
| status | Query | String | N | 주문 상태 필터 |

요청 예시:

```
GET /api/admin/orders?status=RECEIVED
```

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ADMIN_ORDER_LIST_SUCCESS",
  "message": "관리자 주문 목록 조회 성공",
  "data": {
    "content": [
      {
        "orderId": 1,
        "orderNo": "ASAK-20260703-001",
        "orderType": "TAKE_OUT",
        "orderStatus": "RECEIVED",
        "paymentStatus": "APPROVED",
        "totalPrice": 8900,
        "createdAt": "2026-07-03T13:25:00",
        "items": [
          {
            "orderItemId": 1,
            "menuId": 364,
            "menuName": "스파이시 쉬림프 샌드위치",
            "quantity": 1,
            "price": 8900,
            "selectedOptions": [
              { "optionItemId": 269, "name": "크리미칠리", "quantity": 1 }
            ],
            "excludedIngredients": [
              { "ingredientId": 169, "name": "양파" }
            ]
          }
        ]
      }
    ],
    "totalElements": 1
  }
}
```

## 실패 응답 예시

```json
{
  "success": false,
  "status": 400,
  "code": "ORDER_STATUS_INVALID",
  "message": "주문 상태값이 올바르지 않습니다.",
  "data": null
}
```

## 처리 내용

1. 주문 목록을 최신순으로 조회한다.
2. status가 있으면 해당 주문 상태만 조회한다.
3. 결제 상태와 주문 상태를 함께 반환한다.
4. 관리자 주문 상세 화면에서 바로 사용할 수 있도록 주문별 메뉴, 선택 옵션, 제외 재료 목록을 함께 반환한다.
5. Week 5 MVP에서는 페이징 없이 배열 반환으로 시작하고, 이후 확장 시 페이징을 추가한다.

---

# API-008. 관리자 주문 상태 변경

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | PATCH |
| URL | /api/admin/orders/{orderId}/status |
| 인증 필요 여부 | Week 5 MVP에서는 N, 이후 관리자 인증 적용 |
| 사용 화면 | 관리자 주문 관리 화면 |
| 관련 테이블 | orders, common_code |

## 요청 예시

```json
{
  "orderStatus": "PREPARING"
}
```

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "ORDER_STATUS_UPDATE_SUCCESS",
  "message": "주문 상태 변경 성공",
  "data": {
    "orderId": 1,
    "orderNo": "ASAK-20260703-001",
    "orderStatus": "PREPARING"
  }
}
```

## 실패 응답 예시

```json
{
  "success": false,
  "status": 404,
  "code": "ORDER_NOT_FOUND",
  "message": "존재하지 않는 주문입니다.",
  "data": null
}
```

```json
{
  "success": false,
  "status": 400,
  "code": "ORDER_STATUS_INVALID",
  "message": "변경할 수 없는 주문 상태입니다.",
  "data": null
}
```

## 처리 내용

1. orderId로 주문을 조회한다.
2. orderStatus가 RECEIVED, PREPARING, COMPLETED 중 하나인지 검증한다.
3. 주문 상태를 변경한다.
4. 변경 결과를 반환한다.

---

# API-009. 판매 항목 품절 상태 변경 (옵션기능)

## 기본 정보

| 항목 | 내용 |
| --- | --- |
| Method | PATCH |
| URL | /api/admin/sold-out-items |
| 인증 필요 여부 | Week 5 MVP에서는 N, 이후 관리자 인증 적용 |
| 사용 화면 | 관리자 판매 항목 품절 관리 화면 |
| 관련 테이블 | menu, ingredient, option_item, menu_ingredient, menu_option_group, common_code |

## 요청 예시

```json
{
  "targetType": "INGREDIENT",
  "targetId": 155,
  "isSoldOut": true
}
```

> targetType은 MENU, INGREDIENT, OPTION_ITEM 중 하나입니다. seed ingredient 155 = 케이준쉬림프 (menu 364 CORE)
> 

## 성공 응답 예시

```json
{
  "success": true,
  "status": 200,
  "code": "SOLD_OUT_UPDATE_SUCCESS",
  "message": "판매 항목 품절 상태 변경 성공",
  "data": {
    "targetType": "INGREDIENT",
    "targetId": 155,
    "name": "케이준쉬림프",
    "isSoldOut": true
  }
}
```

## 실패 응답 예시

```json
{
  "success": false,
  "status": 404,
  "code": "SOLD_OUT_TARGET_NOT_FOUND",
  "message": "존재하지 않는 판매 항목입니다.",
  "data": null
}
```

```json
{
  "success": false,
  "status": 400,
  "code": "SOLD_OUT_REQUEST_INVALID",
  "message": "품절 변경 요청값이 올바르지 않습니다.",
  "data": null
}
```

## 처리 내용

1. targetType이 MENU, INGREDIENT, OPTION_ITEM 중 하나인지 검증한다.
2. targetType이 MENU이면 `menu.is_sold_out`을 변경한다.
3. targetType이 INGREDIENT이면 `ingredient.is_sold_out`을 변경한다.
4. targetType이 OPTION_ITEM이면 `option_item.is_sold_out`을 변경한다. 이 경우 해당 옵션 항목만 선택 불가로 표시하고 메뉴 자체의 주문 가능 여부에는 영향을 주지 않는다.
5. 기본 재료 또는 옵션 재료가 품절되면 키오스크 화면에서 품절 상태로 표시한다. 같은 재료가 기본 구성과 추가 토핑에 모두 쓰이면 한 번의 재료 품절 변경으로 메뉴 카드, 상세 기본 재료, 옵션 항목 상태가 함께 갱신된다.
6. 핵심 재료(role=CORE)가 품절되면 해당 메뉴는 주문 불가로 표시한다.
7. 일반 기본 재료(role=DEFAULT)가 품절되면 메뉴는 주문 가능하지만 해당 재료는 품절 뱃지로 표시한다.
8. 베이스 재료(role=BASE)가 품절되면 해당 베이스를 사용하는 메뉴/카테고리와 베이스 변경 옵션을 주문 불가 또는 선택 불가로 표시한다.

---

# Part 3 — Week 7~8 확장 (API-010~020)

API 명세 데이터베이스에는 아래 확장 API를 추가로 관리합니다.

| API ID | 기능 | 시점 |
| --- | --- | --- |
| API-010 | 관리자 판매 항목 목록 조회 | 품절 관리 확장 |
| API-011 | 관리자 메뉴 목록 조회 | 관리자 메뉴 관리 |
| API-012 | 관리자 메뉴 등록/수정 | 관리자 메뉴 관리 |
| API-013 | 활성 결제수단 조회 | 결제수단 설정 |
| API-014 | 관리자 결제수단 설정 변경 | 결제수단 설정 |
| API-015 | 관리자 일별 매출 조회 | 후반 확장 |
| API-016 | 장바구니 검증 | 주문 안정화 |
| API-017 | 접근성 설정 조회 | 후반 확장 |
| API-018 | 멤버십 스탬프 적립 | 멤버십 확장 |
| API-019 | 영수증 출력 요청 | 장치/RTOS |
| API-020 | QR/바코드 스캔 | 장치/RTOS |

# Week 5 MVP에서 제외하거나 후반으로 미루는 API

| 제외 API | 제외 이유 | 추후 시점 |
| --- | --- | --- |
| 관리자 로그인 / 권한 (API-HOLD-001) | Week 5 MVP에서는 주문 흐름 완성이 우선이며, 관리자 인증은 후반 관리자 기능과 함께 적용 | 관리자 기능 고도화 시 |
| 영수증 출력 / 프린터 | 장치 연동 범위가 커짐 | 장치/RTOS 단계 |
| QR/바코드 스캔 | 멤버십/쿠폰 기능과 연결됨 | 확장 기능 |
| 멤버십 / 스탬프 | 주문 MVP와 별도 도메인 | 확장 기능 |
| 장치 이벤트 로그 | device_event 테이블이 MVP에서 제외됨 | 장치 연동 구현 시 |
| 매출 통계 | Week 5 MVP 필수 범위는 아니지만 API-015 관리자 일별 매출 조회로 9주 후반 확장 API에 등록 | 후반 주차 |

---

# Part 3 상세 — API-010~017 (collapsed)

<aside>
📌

Week 5 MVP(API-001~009) 이후 구현. seed 예시는 menu 364·ingredient 155·payment_method CARD 기준.

</aside>

- API-010 GET `/api/admin/sold-out-items`
    
    관리자 품절 대상 목록 조회
    
    - Query: `targetType`, `keyword`
    - Response: `[{ targetType, targetId, name, isSoldOut, reasonType }]`
    - 테이블: menu, ingredient, option_item
- API-011 GET `/api/admin/menus`
    
    관리자 메뉴 목록
    
    - Query: `categoryId`, `keyword`, `isSoldOut`
    - seed: menu 364, category 231
- API-012 POST/PUT `/api/admin/menus`
    
    메뉴 등록/수정
    
    - Body: categoryId, name, price, imageUrl, optionGroupIds
- API-013 GET `/api/payment-methods`
    
    활성 결제수단
    
    - seed: payment_method_config CARD(method_id 19)
- API-014 PATCH `/api/admin/payment-methods/{methodId}`
    
    결제수단 활성/정렬 변경
    
    - 테이블: payment_method_config, common_code
- API-015 GET `/api/admin/sales/daily`
    
    일별 매출·메뉴별 판매량
    
    - Query: `from`, `to`
    - 테이블: orders, order_item, payment
- API-016 POST `/api/cart/validate`
    
    장바구니 서버 검증(품절·필수옵션·금액)
    
    - Body: API-005와 동일 items 구조
- API-017 GET `/api/ui/accessibility-options`
    
    접근성 설정 조회(fontScale, highContrast 등)
    
    - FWD-UI-001 연계
- API-018 POST `/api/membership/stamps`
    
    멤버십 스탬프 1회 확인·적립. SC-006, LMIS-MEMBER-001
    
    - Body: orderId, memberId, confirmStamp
    
    ```json
    {
      "success": true,
      "status": 200,
      "code": "MEMBERSHIP_STAMP_SUCCESS",
      "data": { "memberId": 10, "orderId": 1, "orderNo": "ASAK-20260703-001", "stampAdded": true, "stampCount": 5 }
    }
    ```
    
- API-019 POST `/api/orders/{orderId}/receipt-print`
    
    영수증 출력 요청. SC-015, RTOS-DEVICE-001. Week 5 MVP 제외.
    
- API-020 POST `/api/device/scan`
    
    QR/바코드 스캔·쿠폰 할인. SC-016, RTOS-DEVICE-002
    
    - Body: scanType, code