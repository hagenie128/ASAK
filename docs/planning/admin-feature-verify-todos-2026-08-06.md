# Admin 기능별 화면–API–DB 검증 투두 (2026-08-06)

> 교사 지시: **기능별로 화면–API–DB 결과를 함께 확인**하며 진행
> 우선순위: 주문 통합테스트 → 메뉴 → 품절 → 결제수단 → 매출 → 대시보드
> 인라인 코드 태그: `TODO-NNN` — **번호순 = 위 우선순위** (`admin-todo-checklist-2026-08-05.md`)
> 완료 조건: 아래 각 항목의 **화면 · API · DB** 세 칸을 모두 통과해야 해당 기능 완료

---

## 검증 공통 규칙

1. 한 기능(행)을 끝낸 뒤에만 다음 기능으로 넘어간다.
2. 확인 순서: **API(네트워크/Swagger) → DB(조회) → 화면(Admin UI)** 또는 역순이어도 세 결과가 같아야 한다.
3. 불일치 시 원인 층을 기록한다. (`FE 매핑` / `API 계약` / `Service` / `SQL` / `시드 데이터`)
4. mock이 남아 있으면 해당 기능은 미완료다.

---

## P1 · 주문 (통합 테스트) — SCR-009 / SCR-010

| ID | 기능 | 화면 확인 | API 확인 | DB 확인 | 관련 TODO | 상태 |
|---|---|---|---|---|---|---|
| **P1-1** | 주문 목록 조회 | `/orders`(SCR-010)에 주문 행·필터·페이징 표시. mock/fixture 문구 없음 | `GET /api/admin/orders` 200, `content[]`에 `orderId/orderNo/orderStatus/paymentStatus` | `orders` 최신 N건과 목록 건수·상태 코드 일치 | 구현됨 · 검증 | ⬜ |
| **P1-2** | 주문 상세 조회 | 목록에서 주문 선택 시 상세 패널: 메뉴·옵션·제외재료·금액 | `GET /api/admin/orders/{orderId}` 200, 항목/옵션/제외재료 필드 존재 | `order_items`·옵션·제외재료 조인 결과와 상세 동일 | 구현됨 · 검증 | ⬜ |
| **P1-3** | Live 보드 조회 | `/`(SCR-009)에 RECEIVED/PREPARING 카드 표시, 폴링/새로고침 반영 | `GET /api/admin/orders/live` 200 | live 대상 상태(`RECEIVED`,`PREPARING`) 주문만 노출되는지 `orders.status_id`로 대조 | 014 완료 · 검증 | ⬜ |
| **P1-4** | 상태 변경 RECEIVED→PREPARING | Live에서 "접수/조리" 등 액션 → 카드 컬럼 이동, toast 성공 | `PATCH /api/admin/orders/{id}/PREPARING` 200 `ADMIN_ORDER_STATUS_CHANGE_SUCCESS` | 해당 `orders.status_id`가 PREPARING 코드로 변경 | 001~006·011 · 검증 | ⬜ |
| **P1-5** | 상태 변경 PREPARING→COMPLETED | Live "완료 처리" → 보드에서 사라짐/완료 처리, toast 성공 | `PATCH .../COMPLETED` 200 | `status_id` COMPLETED 코드로 변경 | 001~006·011 · 검증 | ⬜ |
| **P1-6** | 잘못된 전이 거부 | COMPLETED→PREPARING 등 시도 시 오류 toast (409 메시지) | 409 `INVALID_ORDER_STATUS_TRANSITION` 또는 `ORDER_STATUS_CONFLICT` | DB 상태 **변경되지 않음** | 002·003·006·011 · 검증 | ⬜ |
| **P1-7** | 주문 취소 | Live/주문관리에서 취소 → 목록·보드 반영, toast | `PATCH /api/admin/orders/{id}/cancel` 200 | `orders.status_id`=CANCELED, `canceled_at` 설정 | 검증 / **008·010** 잔여 | ⬜ |
| **P1-8** | 취소 잔여 정리 | APPROVED 결제 취소 시 정책대로 동작(환불 stub 여부 문서화) | cancel 응답 코드가 정책과 일치 | `status_id` 하드코딩 `43` 제거(**010**), APPROVED 분기(**008**) | **008·010** | ⬜ |
| **P1-9** | Empty vs Error UI | 주문 0건 Empty / 서버 다운 Error 화면이 구분됨 | 200 empty vs 5xx/네트워크 실패 | (데이터 없을 때) 테이블 0건 = Empty | **012** | ⬜ |

**P1 완료 기준:** P1-1~P1-9 전부 통과. (TTS 013a~d·보드 가로스크롤 023은 보류)

---

## P2 · 메뉴 (목록·상세·등록·수정) — SCR-016

| ID | 기능 | 화면 확인 | API 확인 | DB 확인 | 관련 TODO | 상태 |
|---|---|---|---|---|---|---|
| **P2-1** | 메뉴 목록 조회 연동 | `/menus` 목록이 mock이 아닌 실데이터. 카테고리/검색 동작 | `GET /api/admin/menus` 200 | `menu` 테이블 active 목록과 건수·이름·가격 일치 | **024** | ⬜ |
| **P2-2** | 메뉴 상세 조회 연동 | 선택/수정 화면(`/menus/edit`)에 상세·옵션·재료 표시 | `GET /api/admin/menus/{menuId}` 200 | `menu` + 옵션/재료 관계 테이블과 동일 | **024** | ⬜ |
| **P2-3** | 메뉴 등록 BE | (API/Swagger로) 신규 메뉴 POST 성공 | `POST /api/admin/menus` 201/200, id 반환 | `menu` INSERT + 연결 테이블 트랜잭션 커밋 | **015~018** | ⬜ |
| **P2-4** | 메뉴 등록 FE | `/menus/new` 저장 → 목록에 즉시 반영, mock 경로 없음 | 네트워크에 `POST /api/admin/menus` | 방금 INSERT된 row가 화면에 보임 | **022·025** | ⬜ |
| **P2-5** | 메뉴 수정 BE | PATCH로 이름/가격 등 변경 성공 | `PATCH /api/admin/menus/{menuId}` 200 | 해당 row 컬럼 갱신 확인 | **019~021** | ⬜ |
| **P2-6** | 메뉴 수정 FE | `/menus/edit` 저장 → 목록·상세 갱신 | 네트워크에 `PATCH .../menus/{id}` | DB 변경값 = 화면 표시값 | **023·025** | ⬜ |

**P2 후순위(이번 사이클 제외):** 삭제 **026~028·030·031**, ingredients **029**

**P2 완료 기준:** P2-1~P2-6 전부 통과(목록·상세·등록·수정이 화면·API·DB 일치).

---

## P3 · 품절 — SCR-011

| ID | 기능 | 화면 확인 | API 확인 | DB 확인 | 관련 TODO | 상태 |
|---|---|---|---|---|---|---|
| **P3-1** | 품절 카탈로그 조회 | `/sold-out`(또는 동등 경로)에 메뉴·재료·옵션 목록, mock 제거 | `GET /api/admin/soldOut` 200 | 대상 테이블 `is_sold_out` 현황과 카탈로그 일치 | **032~033·035~037·039** | ⬜ |
| **P3-2** | 품절 ON | 토글/저장 → 화면 품절 표시 | `PATCH /api/admin/soldOut` `{targetType,targetId,isSoldOut:true}` 200 | 해당 대상 `is_sold_out=1` | **032·034~036·038·039** | ⬜ |
| **P3-3** | 품절 OFF | 해제 → 화면 정상 판매 표시 | PATCH `isSoldOut:false` 200 | `is_sold_out=0` | 동상 | ⬜ |
| **P3-4** | 실패 롤백 | 잘못된 target 등 오류 시 화면 롤백·에러 toast | 4xx + ErrorCode | DB 값 **원복/미변경** | **035** | ⬜ |

**P3 완료 기준:** P3-1~P3-4 통과. (키오스크 반영은 가능하면 스모크로 추가 확인)

---

## P4-1 · 결제수단 — SCR-018

| ID | 기능 | 화면 확인 | API 확인 | DB 확인 | 관련 TODO | 상태 |
|---|---|---|---|---|---|---|
| **P4A-1** | 결제수단 목록 | `/payment-methods`에 실데이터, mock 제거 | `GET /api/admin/paymentMethods` 200 | 결제수단 마스터 테이블과 일치 | **040~041·043~045·047** | ⬜ |
| **P4A-2** | 결제수단 변경 | 활성/정렬/영수증문구 저장 반영 | `PATCH /api/admin/paymentMethods/{id}` 200 | 해당 row UPDATE 확인 | **040·042~044·046·047** | ⬜ |

**P4A 완료 기준:** P4A-1~P4A-2 통과 후 P4-2로 이동.

---

## P4-2 · 매출 — SCR-019 / SCR-020 / SCR-021

| ID | 기능 | 화면 확인 | API 확인 | DB 확인 | 관련 TODO | 상태 |
|---|---|---|---|---|---|---|
| **P4B-1** | 매출 요약 | `/sales` 기간 요약 숫자 표시, mock 제거 | `GET /api/admin/sales/summary` 200 | 기간 내 결제완료 주문 합계와 일치 | **048·051·052·055** | ⬜ |
| **P4B-2** | 월별 매출 | `/sales/monthly` 월 단위 표시 | `GET /api/admin/sales/monthly` 200 | 월별 집계 SQL/뷰와 일치 | **049·051·053·055** | ⬜ |
| **P4B-3** | 일별 매출 | `/sales/daily` 일자 표시 | `GET /api/admin/sales/daily` 200 | 해당일 주문·결제 합계와 일치 | **050·051·054·055** | ⬜ |

**P4B 완료 기준:** P4B-1~P4B-3 통과 후 P4-3으로 이동.

---

## P4-3 · 대시보드 — SCR-022

| ID | 기능 | 화면 확인 | API 확인 | DB 확인 | 관련 TODO | 상태 |
|---|---|---|---|---|---|---|
| **P4C-1** | 대시보드 조회 | `/dashboard` 실지표 표시, mock 제거 | `GET /api/admin/dashboard` 200 | 대시보드 집계(오늘 주문·매출·대기 등)와 일치 | **056~058** | ⬜ |

**P4C 완료 기준:** P4C-1 통과.

---

## 보류 (P1~P4 이후)

| ID | 내용 | 관련 TODO |
|---|---|---|
| HOLD-TTS | TTS 중복방지·Queue·Mute·localStorage | 013a~013d |
| HOLD-LIVE | Live 보드 가로 스크롤 | **059** (구 023) |
| HOLD-AUTH | 로그인·JWT·가드 | 060~068 |
| HOLD-ROUTE | Canonical 경로·403 | 069~070 |
| HOLD-FUTURE | 환불·영수증 | 071~076 |

---

## 진행 로그 (작업 시 기입)

| 날짜 | ID | 화면 | API | DB | 메모 |
|---|---|---|---|---|---|
| | | ✅/❌ | ✅/❌ | ✅/❌ | |
