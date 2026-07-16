# Backend Architecture

> Status: Current  
> Stack: Spring Boot 4.1.0 · Java 25

## 1. 목적

Backend는 UI 데이터를 저장하는 단순 중계기가 아니라 ASAK의 비즈니스 규칙과 데이터 정합성을 보장한다.

---

## 2. Layer

```text
Controller
→ Service
→ Repository
→ Entity
→ Database
```

DTO와 Mapper가 계층 사이의 데이터 계약을 담당한다.

---

## 3. Controller

책임:

- HTTP request 수신
- DTO validation
- Service 호출
- HTTP response 반환

금지:

- Repository 직접 호출
- 가격 계산
- 품절 정책
- 상태 전이
- Transaction 비즈니스 흐름

### 왜 Repository 직접 호출을 금지하는가

Controller가 DB 구조를 알게 되면:

- 비즈니스 규칙이 흩어진다.
- 재사용이 어렵다.
- 테스트가 복잡해진다.
- API 변경이 DB 변경으로 바로 이어진다.

---

## 4. Service

책임:

- 비즈니스 규칙
- 상태 전이
- 트랜잭션
- 여러 Repository 조합
- 가격 재계산
- 품절 영향
- DTO 변환 orchestration

---

## 5. Repository

책임:

- Entity 조회·저장
- 존재 여부
- 조건 검색
- 집계 query

금지:

- 사용자 문구
- UI 상태
- 복잡한 비즈니스 판단

---

## 6. Entity

책임:

- DB persistence model
- 도메인 상태
- 최소한의 자기 상태 변경

Entity를 API Response로 직접 반환하지 않는다.

### 이유

- lazy loading 노출
- 민감 필드 노출
- DB 변경이 API 변경이 됨
- 순환 참조
- serialization 문제

---

## 7. DTO

```text
Request DTO
Response DTO
```

Entity와 분리한다.

---

## 8. Mapper

Entity ↔ DTO 변환을 한 곳에 모은다.

작은 프로젝트에서는 static mapper도 가능하다.

Service 안에 수십 줄 변환 코드가 반복되면 분리한다.

---

## 9. Package

현재 scaffold를 우선한다.

권장 domain-based 확장:

```text
com.asak
├─ order/
├─ menu/
├─ payment/
├─ ingredient/
├─ sales/
├─ dashboard/
└─ common/
```

프로젝트 구현 단계와 팀 합의를 무시하고 전면 이동하지 않는다.
