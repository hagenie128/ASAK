# Backend Codex Prompt

ASAK-back의 현재 scaffold를 유지하며 구현한다.

반드시 먼저:

1. 실제 package 구조를 읽는다.
2. 기존 Controller/Service/Repository/DTO를 목록화한다.
3. Product Bible과 충돌을 보고한다.
4. 기존 파일을 삭제하지 않는다.

구현 순서:

- 공통 Response/Exception
- Menu Read
- Order Create
- Payment
- Admin Order
- Sold-out/Menu Management
- Dashboard/Sales
- Test

금지:

- Entity 직접 Response
- Controller에서 Repository 호출
- Client 가격 신뢰
- Spring/Java 버전 변경
- 전체 구조 일괄 리팩터링
