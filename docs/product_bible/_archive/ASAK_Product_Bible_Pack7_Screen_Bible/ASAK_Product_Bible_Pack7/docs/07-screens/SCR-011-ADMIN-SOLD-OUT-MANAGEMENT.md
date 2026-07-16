# SCR-011: Admin Sold-out Management

> Status: Current Draft  
> Route: `/soldOut`  
> Purpose: 품절 변경·영향 확인


## 1. Domain

`Admin`

## 2. Figma Reference

Default 39:8577 / Loading 51:13887 / Empty 51:14020 / Error 51:14181 / Save 39:8653

## 3. Main Data

```text
targets, changes, affectedMenus
```

## 4. Required States

- `default`
- `loading`
- `empty`
- `error`
- `dirty`
- `saveConfirm`

## 5. Product Rules

- 대분류 Tab과 중분류 Chip을 구분한다.
- dirty changes와 영향 메뉴 수를 보여준다.
- 문구 '변경 내용을 저장할까요?'로 통일한다.

## 6. React Component Map

- `SoldOutManagementPage`
- `SoldOutTargetTabs`
- `SoldOutFilterChips`
- `SoldOutRow`
- `SaveBar`

## 7. API Contract

- `GET /api/admin/soldOut`
- `PATCH /api/admin/soldOut`

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
