# Sold-out Management

> Status: Current  
> Figma: SCR-011

## 1. 화면 목적

관리자가 메뉴·재료·옵션의 품절 상태를 빠르게 변경하고, 저장 전 영향 범위를 확인하게 한다.

---

## 2. Information Hierarchy

### Primary Tabs

```text
메뉴
재료
옵션
```

큰 Segmented Tab 또는 명확한 Navigation.

### Secondary Filter

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

## 3. Target Type

```text
MENU
INGREDIENT
OPTION_ITEM
```

API·React·Figma에서 동일한 code 사용.

---

## 4. Dirty Change Model

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

## 5. Save Flow

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

## 6. Affected Menu Display

재료 품절 시:

```text
영향 메뉴 4개
```

클릭 시 목록 표시 가능.

MVP에서는 count만 제공해도 충분.

---

## 7. Figma Required States

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

## 8. Existing Figma Issue

예전 문구 잔존 여부 전체 검색:

```text
변경 내용을 저장 변경할까요?
```

공식 문구:

```text
변경 내용을 저장할까요?
```

---

## 9. React Mapping

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

## 10. API Draft

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
