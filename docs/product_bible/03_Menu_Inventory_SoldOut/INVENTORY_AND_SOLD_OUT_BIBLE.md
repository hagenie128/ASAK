# Inventory and Sold-Out Bible

> Status: `Canonical`
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `INVENTORY_ARCHITECTURE.md`
- `INVENTORY_EDGE_CASE_AND_QA.md`
- `INVENTORY_POLICY.md`
- `SOLD_OUT_MANAGEMENT.md`
- `SOLD_OUT_WHY.md`

---

## 원문: `INVENTORY_ARCHITECTURE.md`

### Inventory Architecture

> Status: Current

#### 1. 목적

Inventory는 재료와 옵션의 판매 가능 상태를 관리하고, 메뉴 판매 상태에 미치는 영향을 계산한다.

ASAK MVP에서 재고 수량까지 완전한 ERP 수준으로 관리할 필요는 없다.

우선순위는:

- 품절 여부
- 품절 영향
- 관리자 변경
- Kiosk 즉시 반영

---

#### 2. Inventory Scope

##### MVP

- ingredient sold-out
- option item sold-out
- menu direct sold-out
- affected menu count
- Kiosk disable/badge

##### Extension

- stock quantity
- safety stock
- auto sold-out
- purchase order
- supplier
- expiry date

---

#### 3. Ingredient Classification

```text
CORE
BASE
STANDARD
OPTIONAL
```

Inventory 영향은 role에 따라 달라진다.

---

#### 4. Direct vs Derived Sold-out

##### Direct

관리자가 메뉴 자체를 품절 처리.

##### Derived

재료 또는 옵션 품절로 메뉴가 판매 불가능해짐.

권장 데이터:

```text
directSoldOut
derivedSoldOut
effectiveSoldOut
```

```text
effectiveSoldOut = directSoldOut OR derivedSoldOut
```

---

#### 5. Why Separate Direct and Derived

하나의 boolean만 사용하면:

- 왜 품절인지 알 수 없다.
- 재료가 복구되어도 메뉴를 자동 복구할지 판단하기 어렵다.
- 관리자 화면에서 영향 원인을 설명할 수 없다.

---

#### 6. React Mapping

Admin:

```text
SoldOutManagementPage
SoldOutTargetTabs
CategoryFilterChips
SoldOutItemRow
AffectedMenuList
SaveBar
ConfirmDialog
```

Kiosk:

```text
SoldOutBadge
DisabledMenuCard
DisabledOptionItem
```

---

#### 7. Backend Mapping

```text
inventory/
soldout/
menu/
ingredient/
option/
```

service responsibility:

- target validation
- affected menu calculation
- save batch changes
- rollback on failure
- effective sold-out calculation

---

#### 8. DB Consideration

기존 entity/table 구조를 우선 사용한다.

필요 데이터:

```text
menu.is_sold_out
ingredient.is_sold_out
option_item.is_sold_out
```

추가 권장:

```text
sold_out_reason
updated_at
updated_by
```

단, 기존 schema와 중복이면 새 컬럼을 만들지 않는다.

---

## 원문: `INVENTORY_EDGE_CASE_AND_QA.md`

### Inventory Edge Cases and QA

#### Edge Cases

##### 품절 저장 중 일부 실패

전체 transaction rollback 권장.

##### 여러 재료가 동시에 한 메뉴에 영향

원인 목록 유지.

##### 옵션 품절 해제

추천 option badge 복구 여부 확인.

##### 베이스 일부 품절

다른 베이스가 있으면 메뉴 유지.

##### 모든 베이스 품절

메뉴 품절.

##### 관리자 두 명 동시 수정

MVP에서는 updatedAt 기반 optimistic lock 검토.

---

#### QA

- [ ] direct sold-out
- [ ] core propagation
- [ ] base partial
- [ ] base all unavailable
- [ ] standard ingredient notice
- [ ] option disabled
- [ ] required group all sold-out
- [ ] recovery
- [ ] transaction rollback

---

## 원문: `INVENTORY_POLICY.md`

### Inventory and Sold-out Policy

> Status: Current

#### 1. Policy Matrix

| Target | Result |
|---|---|
| Menu direct sold-out | 해당 메뉴 주문 불가 |
| CORE ingredient sold-out | 연결 메뉴 품절 |
| BASE ingredient sold-out | 해당 베이스를 필수로 쓰는 메뉴 품절 |
| STANDARD ingredient sold-out | 제거 가능하면 메뉴 유지 + 안내 |
| OPTIONAL ingredient sold-out | 해당 옵션만 disabled |
| Option Item sold-out | 해당 옵션만 disabled |
| Required Option Group 전체 품절 | 메뉴 품절 |

---

#### 2. CORE Ingredient

예:

- 닭가슴살이 메뉴 정체성의 핵심
- 연어가 핵심 재료

품절 시 메뉴 자체를 판매할 수 없으므로 derived sold-out.

---

#### 3. BASE Ingredient

베이스 품절 정책은 메뉴 구조에 따라 달라진다.

##### 메뉴가 단일 베이스에 의존

메뉴 품절.

##### 여러 베이스 중 선택

해당 베이스만 disabled.

모든 베이스가 품절이면 메뉴 품절.

---

#### 4. STANDARD Ingredient

기본 포함 재료가 품절이어도:

- 제거 가능
- 메뉴 정체성에 영향 없음

이면 메뉴 판매 유지 가능.

Kiosk에서는:

```text
현재 양파는 제공되지 않습니다.
```

같은 안내 가능.

---

#### 5. OPTIONAL Ingredient

옵션만 disabled.

메뉴 전체 품절로 전파하지 않는다.

---

#### 6. Required Option Group

필수 그룹의 활성 option 수가 minimumSelection보다 적으면 메뉴 품절.

예:

```text
minimumSelection = 1
activeOptions = 0
```

→ 메뉴 품절.

---

#### 7. Recovery Policy

품절 해제 시:

##### direct sold-out

관리자가 직접 해제해야 한다.

##### derived sold-out

원인이 모두 해제되면 자동 복구 가능.

단, direct sold-out이 true면 계속 품절.

---

#### 8. Display Policy

##### Kiosk

- 메뉴 품절: badge + card disabled
- 옵션 품절: option disabled
- 일부 재료 미제공: 안내
- 숨김 메뉴: 노출하지 않음

##### Admin

- 직접 품절
- 영향 품절
- 원인
- 영향 메뉴 수

를 구분한다.

---

#### 9. Implementation Checklist

- [ ] ingredient role
- [ ] direct/derived distinction
- [ ] required option group rule
- [ ] recovery rule
- [ ] affected menus
- [ ] Kiosk badge
- [ ] Admin explanation

---

## 원문: `SOLD_OUT_MANAGEMENT.md`

### Sold-out Management

> Status: Current
> Figma: SCR-011

#### 1. 화면 목적

관리자가 메뉴·재료·옵션의 품절 상태를 빠르게 변경하고, 저장 전 영향 범위를 확인하게 한다.

---

#### 2. Information Hierarchy

##### Primary Tabs

```text
메뉴
재료
옵션
```

큰 Segmented Tab 또는 명확한 Navigation.

##### Secondary Filter

```text
전체
샐러드
샌드위치
웜볼
랩
사이드
음료
```

Chip.

두 계층을 같은 스타일로 만들지 않는다.

---

#### 3. Target Type

```text
MENU
INGREDIENT
OPTION_ITEM
```

API·React·Figma에서 동일한 code 사용.

---

#### 4. Dirty Change Model

저장 전 변경사항을 local draft로 보관한다.

```js
{
  targetType: "INGREDIENT",
  targetId: 33,
  previousSoldOut: false,
  nextSoldOut: true
}
```

---

#### 5. Save Flow

```text
toggle
→ dirty change added
→ affected menu calculation
→ SaveBar visible
→ click save
→ ConfirmDialog
→ batch API
→ success Toast
```

---

#### 6. Affected Menu Display

재료 품절 시:

```text
영향 메뉴 4개
```

클릭 시 목록 표시 가능.

MVP에서는 count만 제공해도 충분.

---

#### 7. Figma Required States

- default
- loading
- empty
- error
- dirty
- saveConfirm
- saving
- saveSuccess
- saveFailed

---

#### 8. Existing Figma Issue

예전 문구 잔존 여부 전체 검색:

```text
변경 내용을 저장 변경할까요?
```

공식 문구:

```text
변경 내용을 저장할까요?
```

---

#### 9. React Mapping

```text
SoldOutManagementPage
SoldOutTargetTabs
SoldOutFilterChips
SoldOutList
SoldOutRow
SaveBar
ConfirmDialog
Toast
```

---

#### 10. API Draft

```http
PATCH /api/admin/soldOut
```

```json
{
  "changes": [
    {
      "targetType": "INGREDIENT",
      "targetId": 33,
      "isSoldOut": true
    }
  ]
}
```

Response:

```json
{
  "success": true,
  "data": {
    "updatedCount": 1,
    "affectedMenuCount": 4
  }
}
```

---

## 원문: `SOLD_OUT_WHY.md`

### Why Sold-out Is Designed This Way

#### 왜 메뉴·재료·옵션을 분리하는가

각 대상은 영향 범위가 다르다.

- 메뉴: 직접 판매 중지
- 재료: 여러 메뉴에 전파 가능
- 옵션: 특정 선택지만 제한

같은 toggle 목록으로 보이더라도 정책은 다르다.

---

#### 왜 저장 버튼을 둔다

토글 즉시 저장은 빠르지만 실수 복구가 어렵다.

품절은 여러 메뉴에 영향을 줄 수 있으므로:

- 변경사항 확인
- 영향 범위 확인
- 일괄 저장

이 더 안전하다.

---

#### 왜 대분류와 중분류를 다르게 보이게 하는가

메뉴/재료/옵션은 데이터 종류를 바꾸는 Navigation이다.

샐러드/랩/음료는 현재 종류 안에서 결과를 거르는 Filter다.

역할이 다르므로 시각 위계도 달라야 한다.
