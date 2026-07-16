# SCR-016: Admin Menu Management

> Status: Current Draft  
> Route: `/menus`  
> Purpose: 메뉴 추가·수정


## 1. Domain

`Admin`

## 2. Figma Reference

Default 39:8851 / Detail Add 39:9082 / Detail Edit 39:9576

## 3. Main Data

```text
menuList, menuDraft, validationErrors
```

## 4. Required States

- `default`
- `detailAdd`
- `detailEdit`
- `saving`
- `error`

## 5. Product Rules

- Add/Edit는 같은 Form을 공유한다.
- original/draft/dirtyFields를 분리한다.
- 메뉴·재료·옵션·영양·알레르기를 동일 계약으로 연결한다.

## 6. React Component Map

- `MenuManagementPage`
- `MenuForm`
- `IngredientSelectModal`
- `OptionGroupEditor`
- `NutritionEditor`
- `SaveBar`

## 7. API Contract

- `GET/POST/PATCH/DELETE /api/admin/menus`

## 8. User Actions

- 화면의 단일 핵심 행동을 유지한다.
- destructive action은 확인 단계를 둔다.
- 실패 시 이전 입력과 선택 상태를 가능한 한 유지한다.

## 9. Edge Cases

- 네트워크 실패
- 중복 클릭
- 오래된 응답
- 품절 또는 상태 변경
- 데이터 없음
- 화면 이탈과 복귀
- 접근성 모드 적용

## 10. Accessibility

- 핵심 터치 타겟 80×80px 이상
- 색상만으로 상태를 표현하지 않음
- focus/label/aria 속성 제공
- 글자 확대 시 overflow 방지

## 11. QA Checklist

- [ ] Figma state와 React state가 일치한다.
- [ ] API 필드와 화면 표시값이 일치한다.
- [ ] Empty·Loading·Error가 누락되지 않는다.
- [ ] 접근성 기준을 충족한다.
- [ ] 잘못된 더미데이터와 개발 메모가 노출되지 않는다.

## 12. Definition of Done

- [ ] Figma 완료
- [ ] React skeleton 또는 구현
- [ ] API 계약 확인
- [ ] DB source 확인
- [ ] PrototypeMap 반영
- [ ] P0 이슈 0건
