# Existing Code Audit

## 목적

기존 팀원이 작성한 코드를 보호하고 중복 구현을 막는다.

## 조사 대상

```text
src/apps
src/pages
src/components
src/features
src/hooks
src/store
src/api
src/constants
src/mocks
src/styles
src/router
```

## 기록 양식

| Item | Existing Path | Status | Reuse | Change |
|---|---|---|---|---|
| MenuCard | ... | implemented | yes | props only |
| CartPage | ... | partial | yes | API/state |
| BottomCTA | ... | implemented | yes | loading state |

## 금지

- 기존 코드를 확인하지 않고 새 Page 생성
- 이름이 다르다는 이유로 중복 Component 생성
- 전체 폴더 이동
- 기존 스타일 제거
