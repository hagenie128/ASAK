# Backend · DB 중간점검 (2026-07-28)

> 범위: 로컬 `ASAK-back`과 실제 원격 `nayeon0828/ASAK-backend`, 연결된 외부 MySQL을 **읽기 전용**으로 점검했다.
>
> 이 문서는 기능 완료 선언이 아니다. 코드·Spring context·실DB·읽기 API 결과를 분리해 다음 구현 순서를 정하기 위한 중간점검 기록이다.

## 1. 결론

- 백엔드는 더 이상 health-only 골격이 아니다. Kiosk 메뉴/카테고리 조회, Admin 메뉴·주문 조회, 활성 주문 조회는 Controller → Service → MyBatis → 실제 DB까지 기동·응답을 확인했다.
- 주문 생성은 검증 일부만 있고 `CreateOrderResponse`를 만들거나 저장하지 않는다. 결제, 주문 상태 변경/취소, 품절, 결제수단, 매출/대시보드 API는 아직 Controller mapping이 없다.
- DB는 기본 테이블 25개와 View 22개가 실제로 존재하며, 메뉴 84건·주문 50,669건·결제 50,669건을 확인했다. 따라서 구현은 mock만이 아니라 실제 DB를 읽고 있다.
- 프론트 실연동은 유지 보류다. 조회 API의 정상 응답은 확인됐지만, 변경 API·오류 경로·정합성·브라우저 QA가 완료되지 않았다.

## 2. 확인 범위와 결과

| 구분 | 확인 방법 | 결과 |
|---|---|---|
| 원격 저장소 | `git remote -v`, `main` 추적 상태 | `https://github.com/nayeon0828/ASAK-backend.git` · 로컬 폴더명은 `ASAK-back` |
| Java 컴파일 | `gradlew.bat compileJava --no-daemon` | 통과 |
| Spring context | `gradlew.bat test --no-daemon`의 `@SpringBootTest` | 통과 — MyBatis XML·Datasource·JPA context 기동 확인 |
| 읽기 API | 임시 로컬 서버 + 실제 DB, 요청 뒤 서버 종료 | 아래 9개 `200` |
| DB 스키마 | `information_schema` 읽기 조회 | 기본 테이블 25개 · View 22개 · FK 39개 |
| DB view | 제한 샘플 조회 | `vw_order_live`, `vw_sales_daily/hourly`, `vw_top_menu_daily/hourly` 조회 가능 |

### 런타임에서 `200` 확인한 조회 API

- `GET /api/health`
- `GET /api/kiosk/categories`
- `GET /api/kiosk/menuList`
- `GET /api/kiosk/menuDetail/{menuId}`
- `GET /api/admin/menus?page=0&size=1`
- `GET /api/admin/menus/{menuId}`
- `GET /api/admin/orders?page=0&size=1`
- `GET /api/admin/orders/{orderId}`
- `GET /api/admin/orders/active`

> 주문 생성·결제·상태 변경·취소는 데이터를 바꿀 수 있으므로 실행하지 않았다. `cart/validate`는 소스상 읽기 전용이나, 이번 점검에서 만든 첫 요청 JSON이 잘못 직렬화되어 500이 발생했으므로 정상 응답 근거로 포함하지 않는다.

## 3. 실제 DB 상태

| 항목 | 확인값 | 의미 |
|---|---:|---|
| 기본 테이블 | 25 | 메뉴·옵션·주문·결제의 실제 저장 구조 존재 |
| View | 22 | 메뉴/주문/판매 읽기 모델이 DB에 적용됨 |
| FK | 39 | 핵심 관계의 참조 제약 존재 |
| category | 6건 | 메뉴 분류 데이터 존재 |
| menu | 84건 | Kiosk/Admin 메뉴 조회의 실제 원본 |
| orders | 50,669건 | 주문 조회·활성 주문의 실제 원본 |
| order_item | 81,226건 | 주문 상세 항목의 실제 원본 |
| payment | 50,669건 | 주문별 결제 데이터 존재 |

### 확인된 핵심 구조

- 실제 테이블명은 `ing`, `opt_item`, `menu_ing`, `menu_opt_policy`, `orders`, `order_item`, `payment`처럼 축약형이다. 문서나 새 SQL에서 `ingredient`, `option_item`을 가정하면 실패한다.
- `orders.order_no`와 `payment.order_id`는 UNIQUE이고, `order_item.order_id/menu_id`, `orders.status_id/order_type_id`, `payment.order_id/method_id/status_id` FK가 존재한다.
- DB 문자셋은 `utf8mb4`, collation은 `utf8mb4_0900_ai_ci`다. `time_zone`은 `SYSTEM`이므로 API 계약의 `Asia/Seoul`을 DB 세션/서버에서 보장하는지는 별도 확인이 필요하다.
- `vw_order_live`의 제한 샘플은 조회됐지만 전체 `COUNT(*)`는 20초 안에 끝나지 않았다. 실제 활성 주문 API는 응답했으나, 집계·모니터링 쿼리에는 성능 확인이 필요하다.

## 4. API 구현 상태

| 기능 | 코드/런타임 상태 | 다음 완료 조건 |
|---|---|---|
| Kiosk 메뉴·카테고리 조회 | Controller·Service·Mapper 및 실제 DB `200` 확인 | 없는 메뉴·필터·empty/error Bruno 추가 |
| Kiosk 장바구니 검증 | 메뉴·품절·옵션·제외 재료 검증 및 `totalAmount` 재계산 코드 존재 | 정상/품절/잘못된 옵션/제외 재료의 Bruno·실DB 검증 |
| Kiosk 주문 생성 | mapping은 있으나 `createOrder()`가 검증 뒤 `null` 반환 | 주문 헤더/항목/옵션/제외 재료 저장, 응답·transaction·오류 검증 |
| Kiosk 결제 | `UserPayController`와 Service/Mapper가 비어 있음 | 결제수단 조회·승인·idempotency·환불 정책 구현 |
| Admin 메뉴 조회 | 목록/상세 Controller·Service·Mapper 및 실제 DB `200` 확인 | empty를 오류로 처리할지 정책 확정, 필터 조합 검증 |
| Admin 주문 조회 | 목록/상세/활성 주문의 실제 DB `200` 확인 | 날짜/상태/검색/없는 주문·empty Bruno 검증 |
| Admin 상태/취소 | Bruno 요청은 있으나 Controller mapping 없음 | 허용 전이·409·환불 transaction 구현 |
| Admin 품절/결제수단/매출/대시보드 | View/계약 일부 존재, Controller mapping 없음 | 기능별 DTO→Service→Mapper→Bruno 세로 슬라이스 구현 |

## 5. 발견 사항과 우선순위

| 우선 | 발견 사항 | 근거/영향 |
|---|---|---|
| P0 | 주문 생성이 성공 응답처럼 보이지만 실제로는 `null`을 반환 | `UserOrderService#createOrder()`에 INSERT·응답 조립 없음. 프론트 실연동 금지 |
| P1 | Bruno의 변경/통계 API 다수가 소스 mapping 없음 | 결제, 상태 변경, 취소, 품절, 결제수단, 대시보드·매출은 명세와 구현을 구분해야 함 |
| P1 | 활성 주문 API가 `OrderListResponse`를 반환 | `LiveOrderResponse`·`getLiveOrders()`·`vw_order_live`는 존재하지만 `/active`는 `menus[]`/경과시간이 없는 목록 DTO를 사용. SCR-009 계약을 하나로 확정 필요 |
| P2 | 제외 재료 SQL 파라미터명이 불일치 | Mapper interface는 `ingredientId`, XML은 `#{ingId}`. 제외 재료가 있는 장바구니 검증은 BindingException 위험 |
| P2 | 잘못된 JSON body가 500으로 처리됨 | `HttpMessageNotReadableException` 전용 처리 없이 일반 예외 처리기로 감. 입력 오류는 400 envelope가 필요 |
| P2 | `vw_order_live` 전체 집계가 20초 내 끝나지 않음 | 제한 샘플/활성 주문 조회는 가능하나 대용량 집계·모니터링 성능 점검 필요 |
| P3 | DB timezone이 `SYSTEM` | `Asia/Seoul` 계약과 실행 환경이 다를 수 있어 날짜 매출/필터에서 경계값 위험 |

## 6. 권장 다음 순서

1. `cart/validate`의 정상·품절·옵션·제외 재료 케이스를 Bruno로 고정하고, P2 Mapper 파라미터/400 예외 처리를 먼저 보완한다.
2. 주문 생성(API-005)을 요청 DTO → 금액 재계산 → 주문/항목/옵션/제외 재료 INSERT → `CreateOrderResponse` → transaction/Bruno까지 완성한다.
3. 결제(API-006)와 Admin 주문 상태 변경/취소를 같은 DB 상태 전이 규칙으로 구현한다.
4. `/active`의 Live DTO와 `vw_order_live` 사용 여부를 SCR-009·Admin adapter와 결정한다.
5. 판매 view의 실행계획·날짜 timezone을 확인한 뒤 매출/대시보드 API를 구현한다.

## 7. 수정 범위

- 이 점검에서는 소스 코드·DB 데이터·스키마를 수정하지 않았다.
- 로컬 서버는 읽기 API 점검 후 모두 종료했다.
- 정본 진행 상태는 [작업 분해표](wbs.md)와 [상태 메모](wbs-status-notes.md)를 함께 본다.

## 8. 점검 후 반영된 표시 정합 수정

- Backend `e9543ce`는 `docs/view.sql`에서 legacy `REQUEST` 옵션 그룹을 `option_items`와 옵션 표시 View에서 제외하고, 제외 재료는 `item_exclusion`만 정본으로 사용하게 했다.
- Admin `d2a900f`는 `OrderDetailPanel`의 제외 재료를 목록 대신 쉼표로 연결한 인라인 텍스트로 표시하게 했다.
- 이 수정은 상세 화면에서 과거 “빼기” 옵션과 실제 제외 재료가 중복 표시되는 위험을 줄인다. 다만 SQL 문서 변경이 실제 외부 MySQL View에 적용됐는지와 실제 주문의 API/브라우저 결과는 아직 별도 검증 대상이다.
