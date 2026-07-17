# 백엔드 개발 가이드 (ASAK-back)

> 이 문서는 ASAK 백엔드 구현을 시작할 때 참고할 공통 가이드입니다.  
> 기준 스택: Spring Boot 4.1 + Java 25 + Spring Data JPA + Gradle + MySQL/H2

---

## 1. 백엔드 설계 방식

백엔드는 과도한 추상화 없이, 팀 프로젝트 규모에 맞는 단순하고 명확한 구조로 설계하는 것을 권장합니다.  
기본 방식은 다음과 같습니다.

1. Controller
   - HTTP 요청 수신
   - 요청 검증 및 응답 포맷 정리

2. Service
   - 비즈니스 로직 처리
   - 트랜잭션 경계 관리

3. Repository
   - DB 접근 처리
   - JPA 엔티티 기반 조회/저장

4. Entity / DTO
   - Entity는 DB 모델
   - DTO는 API 요청/응답 모델

이 구조를 따라가면 화면 요구사항과 API 계약을 분리해서 관리하기 쉽습니다.

---

## 2. 백엔드 진행 순서

백엔드는 아래 순서로 진행하는 것을 권장합니다.

1. 환경 준비
   - Java 25 설치
   - Spring Boot 프로젝트 초기화
   - Gradle 의존성 확인

2. 공통 응답/예외 규칙 정의
   - API 응답 envelope 통일
   - 공통 예외 처리 구조 정의

3. 도메인 설계
   - 메뉴, 옵션, 주문, 결제, 관리자 기능 중심으로 엔티티와 관계 정리
   - 테이블 구조와 필드명을 먼저 명확히 함

4. 데이터 저장소 구성
   - Repository 생성
   - JPA 매핑 및 기본 CRUD 구현

5. 핵심 API 구현
   - 메뉴 조회
   - 옵션 조회
   - 주문 생성
   - 결제 승인
   - 관리자 주문 조회/상태 변경

6. 검증 및 예외 처리
   - 요청값 검증
   - null/empty/invalid 상태 처리
   - 프론트가 분기하기 쉬운 에러 코드 제공

7. 테스트 및 통합 확인
   - 서비스 로직 테스트
   - API 요청/응답 검증
   - 프론트 연동 확인

8. 리팩터링
   - 중복 로직 제거
   - 공통 유틸 분리
   - 패키지 구조 정리

---

## 3. 권장 폴더 구조

프로젝트가 커져도 관리하기 쉬운 수준으로 아래 구조를 기본 템플릿으로 권장합니다.

```text
src/main/java/com/asak/
  common/
    api/
    exception/
    config/
    util/
  domain/
    menu/
      controller/
      service/
      repository/
      entity/
      dto/
    order/
      controller/
      service/
      repository/
      entity/
      dto/
    payment/
      controller/
      service/
      repository/
      entity/
      dto/
    admin/
      controller/
      service/
      repository/
      entity/
      dto/
```

### 역할 정리

- `common/`: 공통 응답, 예외 처리, 설정, 유틸리티
- `domain/`: 기능별 도메인 패키지
- `controller/`: REST API 진입점
- `service/`: 비즈니스 로직
- `repository/`: JPA/DB 접근
- `entity/`: DB 매핑 모델
- `dto/`: 요청·응답 데이터 모델

---

## 4. 파일명 규칙

파일명은 역할이 바로 드러나게 짓는 것이 좋습니다.

| 역할         | 권장 규칙                                  | 예시                     |
| ------------ | ------------------------------------------ | ------------------------ |
| Controller   | `xxxController`                            | `MenuController`         |
| Service      | `xxxService`                               | `OrderService`           |
| Repository   | `xxxRepository`                            | `MenuRepository`         |
| Entity       | 클래스명 그대로                            | `Menu`, `Order`          |
| Request DTO  | `xxxRequest`                               | `OrderCreateRequest`     |
| Response DTO | `xxxResponse`                              | `MenuResponse`           |
| Exception    | `xxxException`                             | `BusinessException`      |
| Handler      | `xxxHandler` 또는 `GlobalExceptionHandler` | `GlobalExceptionHandler` |
| Test         | `xxxTest`                                  | `OrderServiceTest`       |

### 예시

```text
domain/menu/
  controller/MenuController.java
  service/MenuService.java
  repository/MenuRepository.java
  entity/Menu.java
  dto/MenuResponse.java
  dto/MenuListResponse.java
```

---

## 5. API 응답 규칙

프론트와의 일관된 연동을 위해 API 응답은 공통 envelope 형식을 따릅니다.

```json
{
  "success": true,
  "status": 200,
  "code": "MENU_LIST_SUCCESS",
  "message": "메뉴 목록 조회 성공",
  "data": {}
}
```

### 규칙

- 성공/실패 모두 `success`, `status`, `code`, `message`, `data` 포함
- 비즈니스 데이터는 `data` 안에만 담기
- 프론트가 분기하기 쉬운 `code` 값 사용
- HTTP status는 오류 상황을 명확히 표현

---

## 6. 데이터베이스/네이밍 규칙

백엔드 코드와 DB는 아래 규칙을 따릅니다.

- Java 클래스명: PascalCase
- 메서드/변수명: camelCase
- DB 컬럼명: snake_case
- 엔티티명: 단수형으로 사용
- 식별자명: `menuId`, `orderId`, `paymentId` 형태
- enum 값은 의미가 분명한 이름 사용

### 예시

- 엔티티: `OrderItem`
- DB 컬럼: `order_id`, `menu_id`, `total_price`
- DTO 필드: `orderType`, `totalPrice`

---

## 7. 기능별 개발 우선순위

ASAK 백엔드는 다음 순서로 구현하는 것이 자연스럽습니다.

### Phase 1 — 기본 조회

- 카테고리 조회
- 메뉴 조회
- 메뉴 상세 조회
- 옵션 조회

### Phase 2 — 주문 흐름

- 주문 생성
- 장바구니 검증
- 주문 상태 관리

### Phase 3 — 결제

- 결제 승인/실패 처리
- 주문 상태 변경

### Phase 4 — 관리자 기능

- 관리자 주문 목록
- 주문 상태 변경
- 품절 상태 변경
- 메뉴 관리

---

## 8. 팀 공통 규칙

- Controller는 얇게 유지하고, 로직은 Service로 옮기기
- Repository는 단순 CRUD 위주로 유지하고, 복잡한 조회는 Query 메서드나 Specification으로 확장하기
- 엔티티와 DTO를 분리해서 API 스펙 변경에 유연하게 대응하기
- 예외는 공통 처리로 모으고, 각 도메인별 예외는 필요한 만큼만 만들기
- 테스트는 핵심 서비스 로직부터 먼저 작성하기
- 과도한 설계보다는 MVP 흐름이 먼저 가능하도록 구현하기

---

## 9. 작업 템플릿

새 기능을 시작할 때는 아래 순서로 진행하면 좋습니다.

1. 도메인 패키지 생성
2. Entity 작성
3. Repository 작성
4. Request/Response DTO 작성
5. Service 작성
6. Controller 작성
7. 예외 처리/검증 추가
8. 테스트 작성

예시:

```text
domain/order/
  entity/Order.java
  repository/OrderRepository.java
  dto/OrderCreateRequest.java
  dto/OrderResponse.java
  service/OrderService.java
  controller/OrderController.java
```

---

## 10. 참고 문서

백엔드 구현 시 아래 문서를 기준으로 작업하면 일관성이 높습니다.

- [wiki/rest-api-spec.md](../wiki/rest-api-spec.md)
- [wiki/db-api-overview.md](../wiki/db-api-overview.md)
- [guides/06-team-ai-prompt.md](06-team-ai-prompt.md)
