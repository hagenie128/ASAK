# Home and Menu Implementation

## Home

기존 디자인·컴포넌트 유지.

추가 확인:

- EAT_IN / TAKE_OUT
- 선택 state
- 접근성 진입
- Menu route
- orderType store

## Menu List

기존 MenuCard 재사용.

연결:

```text
GET menuList
→ loading
→ empty
→ error
→ default
```

## Menu Detail

- API data
- option draft
- validation
- price derived state
- Cart add

기존 UI 구조를 유지하고 로직만 연결한다.
