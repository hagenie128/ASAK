# ASAK Product Bible Pack 11 — Backend Implementation Bible

> Status: Current Draft  
> Stack: Spring Boot 4.1.0 · Java 25  
> Repository: ASAK-back

## 목적

이 Pack은 ASAK-back을 실제로 구현하는 순서와 각 계층의 책임을 정의한다.

기존 scaffold와 주석을 유지하면서 다음을 연결한다.

```text
Figma / Screen Bible
→ API Contract
→ DTO
→ Service
→ Entity
→ Repository
→ DB
→ Test
```

## 중요 원칙

1. 기존 package와 scaffold를 먼저 읽는다.
2. 클래스 이름이 다르다는 이유로 기존 파일을 삭제하지 않는다.
3. Entity를 Controller 응답으로 직접 반환하지 않는다.
4. 가격·상태·품절은 서버가 최종 판단한다.
5. 하나의 기능을 Controller부터 DB까지 세로로 완성한 뒤 다음 기능으로 이동한다.
6. 실제 구현 전 Pack 1~10의 정책과 충돌 여부를 확인한다.
