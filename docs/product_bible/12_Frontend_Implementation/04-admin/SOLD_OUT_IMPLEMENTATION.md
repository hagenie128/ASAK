# Sold-out Frontend Implementation

## Current Code Status (2026-08-06)

- 화면은 `SoldOutManagePage` + `useSoldOutDraft`로 동작한다.
- 초기 로드와 저장은 아직 `adminMockRepository`를 사용한다.
- `soldOutApi.listSoldOutCatalog`, `soldOutApi.patchSoldOut`는 아직 없다.
- 좌측 판매 항목 / 우측 품절 항목 2패널, 탭, 검색, 카테고리, 페이지네이션, 저장 확인 다이얼로그까지는 구현되어 있다.

## Draft

```js
{
  changes: []
}
```

현재 구현은 단순 `changes[]`보다 아래 상태를 함께 들고 있다.

```text
available
soldOut
selectedAvailable
selectedSoldOut
dirtyCount
baselineAvailable
baselineSoldOut
```

## 흐름

```text
toggle
→ dirty change
→ affected count
→ SaveBar
→ ConfirmDialog
→ PATCH
→ Toast
```

현재 코드 기준 실제 흐름:

```text
mock getSoldOutCatalog()
→ available / soldOut 로드
→ 카드 선택 후 → / ← 이동
→ dirtyCount 계산
→ 저장 확인
→ mock saveSoldOutCatalog()
→ 성공 시 baseline 갱신 / 실패 시 baseline 롤백
```

## 위계

- Menu / Ingredient / Option = Tabs
- Category = Chips

현재 탭 값은 `MENU`, `INGREDIENT`, `OPTION`이다.

## 기존 컴포넌트

Admin/Toast, ConfirmDialog, Filter components를 재사용.

## Current Gaps

- 실제 API 미연결
- Error 상태 분기는 저장 toast 외에는 제한적이며, 초기 load 실패 처리도 mock 기준
- 영향 메뉴 수(`affectedMenus`)는 현재 코드에 없다
