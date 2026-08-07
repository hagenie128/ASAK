# Admin 기능별 화면–API–DB 검증 투두 (2026-08-06)

> 작업 원칙: **기능별로 화면–API–DB 결과를 함께 확인**하며 진행
> 인라인 코드 태그: `TODO-NNN` (`admin-todo-checklist-2026-08-05.md`)
> 완료 조건: 각 ID의 **화면 · API · DB** 세 칸 모두 통과

## 오늘(2026-08-06) 작업 순서

교사 8/5(주문→메뉴→품절→결제…) + 8/6(메뉴 CRUD·FE / 품절·결제 C→S→M)을 합친 **오늘 실행 순**:

| 순위 | ID | 할 일 | 비고 |
|---|---|---|---|
| **1** | T-1 ~ T-2 | **메뉴 목록·상세 조회** FE mock 제거 + 화면–API–DB 검증 | BE GET은 있음. 등록보다 **조회 먼저** |
| **2** | T-3 ~ T-6 | **메뉴 등록·수정** BE → FE 연결 + 검증 | 기본 필드만 (계약 MVP) |
| **3** | T-7 | **메뉴 삭제** BE → FE (가능 범위) | soft-delete 컬럼 없으면 범위 확인 후 |
| **4** | T-8 | **품절** Controller → Service → Mapper (+ 가능하면 FE) | 8/6 |
| **5** | T-9 | **결제수단** Controller → Service → Mapper (+ 가능하면 FE) | 8/6 |
| 병행/여유 | O-* | 주문 통합 테스트 잔여 | 8/5 P1. 메뉴 조회 한 줄기 후·사이사이 |
| 후순위 | S-* / D-* | 매출 → 대시보드 | 8/5 P4 후반. 오늘 필수 아님 |
| 키오스크·문서 | — | 결제수단·장바구니 / 위키 | 관리자 메뉴 조회+등록 줄기 이후 또는 분담 |

---

## 검증 공통 규칙

1. 한 기능(행)을 끝낸 뒤에만 다음으로 넘어간다.
2. **API → DB → 화면** (또는 역순) 결과가 같아야 한다.
3. mock이 남아 있으면 해당 기능은 미완료.
4. 목록 0건은 **ErrorCode가 아니라 200 + 빈 content** (Empty ≠ NOT_FOUND).

---

## T · 오늘 메뉴 (우선) — SCR-016

| ID | 기능 | 화면 | API | DB | TODO | 상태 |
|---|---|---|---|---|---|---|
| **T-1** | 메뉴 목록 조회 연동 | `/menus`가 mock이 아닌 실데이터 | `GET /api/admin/menus` **200** (0건도 200+빈목록; `MENU_NOT_FOUND` 쓰지 않음) | `menu`와 건수·이름·가격 일치 | **015·016** | 🟡 구현 완료 · 화면/API/DB 미검증 |
| **T-2** | 메뉴 상세 조회 연동 | 선택/편집 화면에 상세 표시 | `GET /api/admin/menus/{menuId}` 200 / 없으면 404 | 상세 row·관계 일치 | **015** | 🟡 구현 완료 · 화면/API/DB 미검증 |
| **T-3** | 메뉴 등록 BE | — | `POST /api/admin/menus` (categoryId,name,price,imageUrl,description) | `menu` INSERT | **017~019** | ⬜ Mapper 선언 → Service 저장 → Controller POST |
| **T-4** | 메뉴 등록 FE | `/menus/new` 저장 → 목록 반영 | 네트워크 POST | INSERT row = 화면 | **023·025** | ⬜ api 함수 추가 → save handler 연결 |
| **T-5** | 메뉴 수정 BE | — | `PATCH /api/admin/menus/{menuId}` | row UPDATE | **020~022** | ⬜ Mapper UPDATE → Service 존재여부 기준 → Controller PATCH |
| **T-6** | 메뉴 수정 FE | `/menus/edit` 저장 → 목록·상세 갱신 | 네트워크 PATCH | DB = 화면 | **024·025** | ⬜ api 함수 추가 → save handler 연결 |
| **T-7** | 메뉴 삭제 | 삭제 후 목록에서 사라짐(또는 비활성) | `DELETE` 또는 정책에 맞는 API | DB 반영 | **026~028·030·031** | ⬜ 삭제 정책 확정 → API 함수 → confirm handler 연결 |

**T 완료 기준:** T-1~T-2 필수 통과 후 T-3~T-6. T-7은 스키마 제약 확인 후.

---

## T · 오늘 품절·결제수단 BE (메뉴 CRUD 다음)

| ID | 기능 | 화면 | API | DB | TODO | 상태 |
|---|---|---|---|---|---|---|
| **T-8** | 품절 C→S→M | (가능하면 `/sold-out` mock 제거까지) | `GET`/`PATCH /api/admin/soldOut` | `is_sold_out` | **032~039** | ⬜ |
| **T-9** | 결제수단 C→S→M | (가능하면 `/payment-methods`까지) | `GET`/`PATCH paymentMethods` | 마스터 UPDATE | **040~047** | ⬜ |

---

## O · 주문 통합 테스트 (8/5 · 병행/여유) — SCR-009 / SCR-010

| ID | 기능 | 화면 | API | DB | 상태 |
|---|---|---|---|---|---|
| **O-1** | 주문 목록 | `/orders` | `GET /admin/orders` | orders 일치 | ⬜ |
| **O-2** | 주문 상세 | 상세 패널 | `GET /orders/{id}` | items 일치 | ⬜ |
| **O-3** | Live 보드 | `/` | `GET /orders/live` 200+빈목록 가능 | RECEIVED/PREPARING | ⬜ |
| **O-4** | →PREPARING | Live 이동 | PATCH .../PREPARING | status_id | ⬜ |
| **O-5** | →COMPLETED | Live 완료 | PATCH .../COMPLETED | status_id | ⬜ |
| **O-6** | 잘못된 전이 | 409 toast | 409 ErrorCode | DB 미변경 | ⬜ |
| **O-7** | 취소 | 화면 반영 | PATCH .../cancel | CANCELED + canceled_at | ⬜ |
| **O-8** | 취소 잔여 | — | 정책 코드 | **008** 환불 stub / **010** 코드테이블(진행중·확인) | 🟡 |
| **O-9** | Empty vs Error | 목록 구분 UI | 200 empty vs fail | — | ✅ hook 수정 · 화면 확인 ⬜ |

---

## 후순위 · 매출 → 대시보드 (8/5 P4 후반)

| ID | 기능 | TODO | 상태 |
|---|---|---|---|
| **S-1~3** | 매출 요약·월·일 mock 제거 | **048~055** | ⬜ |
| **D-1** | 대시보드 mock 제거 | **056~058** | ⬜ |

---

## 보류

| ID | 내용 | TODO |
|---|---|---|
| HOLD-TTS | TTS 명세 고도화 | 013a~d |
| HOLD-LIVE | Live 가로 스크롤 | 059 |
| HOLD-AUTH | 로그인·JWT | 060~068 |
| HOLD-ROUTE | 정본·403 | 069~070 |
| HOLD-FUTURE | 환불·영수증 | 071~076 |
| HOLD-KIOSK | 결제수단 조회·승인 / 장바구니 검증 | 8/6 키오스크 |
| HOLD-DOCS | 회의록·위키 최신화 | 8/6 문서 |

---

## 진행 로그

| 날짜 | ID | 화면 | API | DB | 메모 |
|---|---|---|---|---|---|
| 2026-08-06 | T-1 | ⬜ | ✅ | ⬜ | `useMenusQuery`가 `PageResult` 기준 목록·필터·페이지네이션 실연동 |
| 2026-08-06 | T-2 | ⬜ | ✅ | ⬜ | `selectedMenuId` 기준 `getMenu(menuId)` 상세 조회 연결 |
| 2026-08-06 | — | — | — | — | 인라인 메뉴 TODO를 **015 조회 → 017~ 등록·수정 → 026~ 삭제** 순으로 재번호 |
| 2026-08-06 | O-9 | — | — | — | useOrdersQuery Empty/Error 분리 · Live 빈목록 200 |
| | | ✅/❌ | ✅/❌ | ✅/❌ | |
