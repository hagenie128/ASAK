# Regression Suite

기존 팀원이 만든 고객용 Frontend를 보호하기 위한 핵심 회귀 테스트다.

## 변경 후 반드시 확인

- Home → Menu
- Menu → Detail
- Detail → Cart
- Cart quantity
- Cart total
- Payment route
- Complete route
- orderSessionStore
- 기존 API mock
- 기존 component import
- build
- lint

## 중복 방지

- 기존 MenuCard가 유지되는가
- BottomCTA가 재사용되는가
- 기존 Store action이 유지되는가
- 기존 route가 깨지지 않았는가
- 새로운 component가 기존 역할을 대체하지 않았는가
