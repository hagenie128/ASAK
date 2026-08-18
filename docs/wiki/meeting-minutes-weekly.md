# ASAK 주차별 회의록 (2026-07 ~ 08)

> Status: **REFERENCE**
> 원본: [`../operations/meeting-minutes/`](../operations/meeting-minutes/README.md)
> **개인/팀 주간 rollup:** [`../../worklog/weekly/`](../../worklog/weekly/README.md) (이 문서와 역할이 다름)
> Hub: [wiki/78](https://devcopilot.ai.kr/workspace/2/wiki/78)

# ASAK 프로젝트 2조 회의록

| 항목 | 내용 |
|---|---|
| 기간 | 2026-07-01 ~ 2026-08-18 |
| 팀 | 프로젝트 2조 (최종 구성: **김나연**, **이하진**) |
| 프로젝트 | ASAK — 샐러드 키오스크 + 관리자 연동 |
| 문서 성격 | 공식 회의록 (주차별) |
| 작성일 | 2026-08-18 |
| 근거 | 2조 공용 채널, 팀 내부 협의, 로컬 `worklog/daily`·`entries`·`weekly` |

> **범위 안내**
> - 최종 팀원(김나연·이하진) 기준으로만 기록한다.
> - 일상 잡담·개인 신상·시크릿(계정·비밀번호)은 수록하지 않는다.
> - 상태 표기: `확정` / `진행` / `미결` / `선생님 지시`

---

## 현재 상태 스냅샷 (2026-08-18)

| 영역 | 상태 | 근거 한 줄 |
|---|---|---|
| Figma | `동결` | 0718 UI 이식 · 7/20 이후 추가 디자인 중지 |
| Kiosk | `진행` | 메뉴·장바구니·결제수단(API-014)·주문생성(API-005) 코드 연결. 결제는 타이머 mock · `approvePayment` 미호출. 클라이언트 `/payments` ≠ 서버 `/api/kiosk/payments` |
| Admin | `진행` | 주문 Live·목록·상태·취소 + 메뉴 CRUD/soft delete **코드 연결·미검증**. 품절·결제수단·매출·대시보드·로그인은 BE 스텁 |
| Backend | `진행` | Kiosk 조회·cart·orders·payments Controller 있음. Admin 주문·메뉴·옵션 있음. soldOut/paymentMethods/sales/dashboard/login은 클래스만 |
| DB | `진행` | 외부 MySQL·View 존재 · 실주문 E2E·뷰 합계 대조 미검증 |
| QA | `미착수` | Bruno health만 성공 assert · 브라우저 E2E 미실행 → PASS 금지 |
| 일정 | `선생님 지시` | ~08/21 RTOS(`device_event`+콘솔, 적어도 Spring↔React). 코드에 `device_event` 없음 |

> 아래 08-07 표는 당시 스냅샷이며 현재 구현으로 해석하지 않는다.

## 현재 상태 스냅샷 (2026-08-07)

| 영역 | 상태 | 근거 한 줄 |
|---|---|---|
| Figma | `동결` | 0718 UI 이식 · 7/20 이후 추가 디자인 중지 · 구독 종료 전 백업 공유 |
| Kiosk | `진행` | Home→Cart mock 동작 · 주문 생성·결제 실연동 미완 |
| Admin | `진행` | 주문 Live·목록·상세·상태·취소 BE 구현(미검증) · CRUD·품절·결제수단·매출은 mock |
| Backend | `진행` | 조회 경로 존재 · `createOrder()` 저장 미완 · 변경/통계 Controller 스텁 |
| DB | `진행` | 외부 MySQL·View 존재 · 실주문 E2E·뷰 합계 대조 미검증 |
| QA | `미착수` | TC 다수 TODO · 실행 기록 없음 → PASS로 올리지 말 것 |

> **읽는 법** — 위 표는 **주요 기능 구현 기준**이며 완료(DONE) 주장이 아니다.
> **1차 mock 연결 ≠ DONE** · **코드 있음 ≠ 통합 검증 완료**.
> 진행률 백분율(%)은 운영 지표로 쓰지 않는다.
> 근거 정본: [`current-status-baseline.md`](current-status-baseline.md)

---

## 주차별 회의록

| 주차 | 기간 | 주제 | 파일 |
|---|---|---|---|
| W27 | 06-29 ~ 07-05 | 킥오프·기획 정비 | [2026-W27.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W27.md) |
| W28 | 07-06 ~ 07-12 | 디자인 방향·관리자 UI 골격 | [2026-W28.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W28.md) |
| W29 | 07-13 ~ 07-19 | 저장소 분리·Figma→코드·구현 경계 | [2026-W29.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W29.md) |
| W30 | 07-20 ~ 07-26 | mock 완성·백엔드 골격·제출 | [2026-W30.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W30.md) |
| W31 | 07-27 ~ 08-02 | Admin API·계약 통일·연동 시작 | [2026-W31.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W31.md) |
| W32 | 08-03 ~ 08-07 | 실연동·관리자 CRUD·문서화 | [2026-W32.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W32.md) |
| W33 | 08-10 ~ 08-16 | 키오스크 실API·관리자 메뉴 연동 | [2026-W33.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W33.md) |
| W34 | 08-17 ~ 08-21 | 장치 이벤트/RTOS 연동 | [2026-W34.md](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W34.md) |

---

## 팀·저장소 개요

### 구성 변경

| 일자 | 내용 | 상태 |
|---|---|---|
| 2026-07-01 | 2조 공용 채널 개설, 선생님·팀원 합류 | 확정 |
| 2026-07-02 | 프로젝트명 후보 논의 → 선생님 의견 반영, **아삭(ASAK)** 방향 | 확정 |
| 2026-07-13 | 채널에서 일부 구성원 제외 → **김나연·이하진** 2인 체제 | 확정 |

### 역할 (도메인 오너십)

> **백엔드는 두 사람이 도메인을 나눠 담당한다.** 프론트 담당과 백엔드 담당이 다르지 않다.

| 담당 | 프론트 | 백엔드 도메인 | 공통·운영 |
|---|---|---|---|
| 김나연 | 키오스크 화면·주문 세션 로직 | **고객(`user`)** — 메뉴 조회(API-003), 주문 생성(API-005), `UserOrderMapper`·`UserMenuMapper` | Spring/MyBatis 골격, API 명세 반영 |
| 이하진 | 디자인 시스템·Figma, **Admin 전담** | **관리자(`admin`)** — 주문 Live·목록·상세·상태전이·취소, 메뉴 CRUD, 품절·결제수단, `AdminOrderMapper`, MySQL 스키마·CORS | API·DB 계약, 문서·에이전트 도구, 배포 미리보기 |

> **근거** — `ASAK-back` 커밋 기준 이하진 72건 / 김나연 59건.
> `ASAK-Admin`은 이하진 87건(단독), `ASAK-Kiosk`는 이하진 124건 / 김나연 68건.

### 산출물

| 구분 | 위치·URL |
|---|---|
| 문서 정본 | `ASAK` 저장소 `docs/` |
| 키오스크 FE | ASAK-Kiosk — https://asak-kiosk.vercel.app/ |
| 관리자 FE | ASAK-Admin — https://asak-admin.vercel.app/ |
| 백엔드 | ASAK-backend (Spring Boot + MyBatis) |
| DB | 팀 공용 MySQL `asak_db` (시크릿 별도 관리) |
| 워크로그 | `ASAK/worklog/daily`, `entries`, `weekly` |

---

## 횡단 결정 요약 (현재 정본)

| # | 주제 | 정본 | 상태 |
|---|---|---|---|
| 1 | 제품 방향 | 실사용 프랜차이즈형 샐러드 키오스크 + Admin 연동 | 확정 |
| 2 | FE 저장소 | ASAK-Kiosk / ASAK-Admin | 확정 |
| 3 | BE 접근 | MyBatis XML·뷰에서 가공, Java는 I/O | 확정 |
| 4 | 주문 세션 | 유형·카트·주문·결제 통합 store / 서버 목록과 분리 | 확정 |
| 5 | 결제 실패 | 카트 유지 / 성공·타임아웃 시 세션 초기화 | 확정 |
| 6 | orderType | `EAT_IN`, `TAKE_OUT` | 확정 |
| 7 | 결제수단 코드 | `CARD`, `KAKAO_PAY`, `NAVER_PAY` | 확정 |
| 8 | 금액 필드(API) | `totalAmount`, `approvedAmount`, `approvedAt`, `lineAmount`, `extraPrice` 등 | 확정(방향) |
| 9 | 취소 철자 | `CANCELED` | 확정 |
| 10 | Live | `GET /api/admin/orders/live` | 확정 |
| 11 | 디자인 추가 | 7/20 이후 추가 디자인 중지, 구현·연동 우선 | 확정 |
| 12 | 구현 단위 | 수직 슬라이스(한 API 경로 end-to-end) | 확정 |

---

## ⚠️ 확인 필요 사항 (결정 ↔ 구현 갭)

> **이 섹션의 목적** — "회의에서 정했는데 코드가 따라왔는지 아무도 확인하지 않은" 항목만 모은다.
> 아직 **정하지 못한** 것은 아래 계약 미결에 둔다. 둘을 섞지 않는다.

| # | 결정 | 결정 시점 | 코드 실측 (2026-08-07) | 판정 |
|---|---|---|---|---|
| 1 | 필드명 정본 변환은 **adapter 경계에서만** 수행 | W31 | `ASAK-Kiosk/src/adapters/orderAdapter.js:20`이 `return payload` — TODO 주석만 있고 변환 **미구현** | ❌ 미반영 |
| 2 | `orderType` = `EAT_IN` / `TAKE_OUT` (`STORE`·`TAKEOUT` 폐기) | W30·W31 | BE `OrderType.java` 준수 ✅ / 과거 mock `asak-data/archive/frontend-mocks/student-project-data.json`에 `"STORE"` 잔존(런타임 미사용) | ✅ 프론트 런타임 정리됨 |
| 3 | 취소 철자 `CANCELED` | W31 | BE `OrderStatus.java`·`PaymentStatus.java` 준수 ✅ / `scripts/expand-mocks.js:520,549,652`가 `CANCELLED` 생성 | ⚠️ mock 생성기 미정리 |
| 4 | 옵션 추가금 필드 `extraPrice` | W31 | BE `add_price AS extraPrice` 준수 ✅ / kiosk mock JSON 전반 `priceDelta` | ⚠️ mock만 미정리 |
| 5 | 결제수단 정본 **3종** `CARD`·`KAKAO_PAY`·`NAVER_PAY` | W30 | kiosk mock **8종**(`card`,`kakao`,`naver`,`toss`,`payco`,`apple`,`cash`,`zero`) / Admin Figma SCR-018 **4종** / DB 정본 **3종**. kiosk `methodId`는 소문자 슬러그로 `paymentMethodCode` enum과 **형식도 불일치** | ❌ 3중 불일치 |
| 6 | DB 컬럼명 유지 + API만 `totalAmount` 매핑 | W31 | `AdminOrderMapper.xml:12` `total_price → totalAmount` 준수 ✅ | ✅ 반영됨 |

**해석** — 백엔드는 정본을 잘 지키고 있고, 갭은 **프론트 mock/adapter 계층에 몰려 있다.**
1번(adapter no-op)이 나머지를 실연동 시점에 한꺼번에 터뜨릴 수 있는 지점이므로 우선순위가 가장 높다.

---

## 현재 미결·후속 (2026-08-07)

### 👤 김나연 — 키오스크·고객 백엔드

1. 장바구니 검증(실 DB) → 주문 생성 실연동
2. `createOrder()` 저장 완성 (현재 검증 후 `null` 반환)
3. `UserOrderService` 컴파일·런타임 안정성 확인
4. 상세메뉴 API 오류 재발 여부 점검

### 👤 이하진 — 관리자·계약·문서

1. Admin 메뉴 CRUD 완성·연동 → 품절 → 결제수단 → 매출·대시보드 순 mock 제거
2. 결제수단 조회·승인 API (키오스크 결제 연결의 선행)
3. 위 확인 필요 사항 1·5번 정리
4. Screen ID·WBS ID·위키와 코드 정합 유지

### 👥 공통

1. 메뉴 선택 → 장바구니 → 주문 → 결제 → 완료 통합 QA 1사이클
2. 아래 계약 미결 확정 후 양쪽 반영
3. QA TC 실행 기록 남기기 (현재 전부 TODO)

### 계약 미결 (2026-08-07)

| 항목 | 내용 | 담당 |
|---|---|---|
| 주문 옵션 요청 | Bible `selectedOptionItemIds[]` vs DTO `optionItems[{ optionItemId, quantity }]` | 공통 협의 |
| 메뉴 기본가 이름 | `price` / `unitPrice` / `basePrice` / `baseAmount` 혼용 | 공통 협의 |
| 상태변경 응답 | `previousStatus`/`status` vs `previousOrderStatus`/`orderStatus` | 이하진 |
| 상태변경 path | `/{orderId}/{status}` vs `/{orderId}/status` | 이하진 |
| API 명명 케이스 | camelCase vs snake_case 최종 통일 (7/14 선생님 지적, 미해결 지속) | 공통 협의 |

---

## 참고 문서 (2026-08-07)

> 정본 폴더: [operations/meeting-minutes](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07). WBS는 [wbs.md](wbs.md).

### 입구·상태

| 종류 | 링크 |
|---|---|
| 문서 입구 | [START_HERE](https://github.com/hagenie128/ASAK/blob/main/docs/START_HERE.md) |
| 영역별 현황 | [current-status-baseline](current-status-baseline.md) |
| 구현 맵 | [current-implementation-map](https://github.com/hagenie128/ASAK/blob/main/docs/planning/current-implementation-map-2026-07-16.md) |
| 전체 흐름도 | [project-flow](project-flow.md) |

### 계획·WBS

| 종류 | 링크 |
|---|---|
| WBS 정본 | [wbs.md](wbs.md) (`WBS-001`~`085`) |
| WBS 상태 메모 | [wbs-status-notes](wbs-status-notes.md) |
| DONE·PASS 점검 | [asak-done-pass-audit](https://github.com/hagenie128/ASAK/blob/main/docs/ai-reports/2026-08-07/asak-done-pass-audit.md) |
| WBS 일정 rebase | [asak-wbs-date-rebase](https://github.com/hagenie128/ASAK/blob/main/docs/ai-reports/2026-08-07/asak-wbs-date-rebase.md) |

### 계약·DB·API

| 종류 | 링크 |
|---|---|
| 정본 계약 | [canonical-contract-decisions](https://github.com/hagenie128/ASAK/blob/main/docs/governance/canonical-contract-decisions-2026-07-16.md) |
| REST API 명세 | [rest-api-spec](rest-api-spec.md) |
| DB 테이블 | [db-table-definition](db-table-definition.md) |
| DB 뷰 | [db-view-definition](db-view-definition.md) |
| MySQL 스키마 DDL | `ASAK-back/docs/아삭_mysql.sql` · `view.sql` (파일 반영 · 실DB 적용 미검증) |

### 회의록·워크로그·미리보기

| 종류 | 링크 |
|---|---|
| 주차별 정본 | [meeting-minutes README](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) |
| 산출물 체크리스트 | [meeting-deliverables-checklist](meeting-deliverables-checklist.md) |
| 주간 워크로그 | [W28](https://github.com/hagenie128/ASAK/blob/main/worklog/weekly/2026-W28.md) · [W29](https://github.com/hagenie128/ASAK/blob/main/worklog/weekly/2026-W29.md) |
| daily/entries | `worklog/daily/{김나연\|이하진}/` · `worklog/entries/...` |
| Kiosk / Admin | https://asak-kiosk.vercel.app/ · https://asak-admin.vercel.app/ |
| RTOS 공부 노트 | [study/RTOS](https://github.com/hagenie128/ASAK/blob/main/docs/study/RTOS/RTOS.md) |

---

## 문서 이력

| 일자 | 내용 |
|---|---|
| 2026-08-07 | 초안(통합본). 2조 채널·팀 협의·워크로그 통합. |
| 2026-08-07 | 주차별 파일 분리 (`meeting-minutes/2026-W*.md`). |
| 2026-08-07 | 상태 스냅샷·`⚠️ 확인 필요 사항`(결정↔구현 갭) 신설, Action Items 담당자 배정, 역할표에 백엔드 도메인 분담 반영. 회의록 `_TEMPLATE.md` 추가. |
| 2026-08-07 | 참고 문서를 `wbs.md`·START_HERE·baseline·API/DB·DONE/PASS 등 현재 정본으로 갱신. |


---

# 회의록 2026-W27 — 킥오프·기획 정비

| 항목 | 내용 |
|---|---|
| 주차 | ISO 2026-W27 |
| 기간 | 2026-06-29 ~ 2026-07-05 |
| 팀 | 김나연, 이하진 |
| 목차 | [회의록 목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) · [다음 주 →](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W28.md) |

---

## 확정·합의

| 항목 | 내용 | 상태 |
|---|---|---|
| 프로젝트명 | 투표 분산 → 선생님: 아삭/그린츠 계열 권장 → **ASAK(아삭)** | 확정 |
| 기획 산출 | 요구사항 조사서 통합본, 향후 확장 아이디어 공유 | 확정 |
| 워크스페이스 | front/back/pipeline 영역 분리·워크로그 템플릿 정비 (이하진) | 확정 |

## 선생님·채널

- 시나리오–요구사항 매핑 ID 오류 정정 지시 (SC-006 등 다수 ID 재매핑) — `선생님 지시`
- DB·계정 정보는 채널에 공유됨 → **시크릿은 문서화하지 않고 로컬/시크릿 저장소로만 관리**

## 진척

- **이하진**: 팀 workflow·작업기록 체계, 모노레포/다중 저장소 운영 문서화
- **김나연**: (해당 주 로컬 daily 기록 없음 — 채널·기획 참여)

## 관련 워크로그

> 해당 주차 기간에 존재하는 daily/entries 전체. 기간이 걸친 entries(-to-)는 겹치는 주차에 중복 표기. 작업 없는 날(파일 없음)은 나열하지 않는다.

### 이하진

- **daily**
  - worklog/daily/이하진/2026-07-02.md
  - worklog/daily/이하진/2026-07-03.md
  - worklog/daily/이하진/2026-07-05.md
- **entries**
  - worklog/entries/이하진/2026-07-02-to-03-project-bootstrap.md
  - worklog/entries/이하진/2026-07-05-notion-docs-cleanup.md

### 김나연

- **daily:** (해당 기간 파일 없음)
- **entries:** (해당 기간 파일 없음)

# 회의록 2026-W28 — 디자인 방향·관리자 UI 골격

| 항목 | 내용 |
|---|---|
| 주차 | ISO 2026-W28 |
| 기간 | 2026-07-06 ~ 2026-07-12 |
| 팀 | 김나연, 이하진 |
| 목차 | [← 이전](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W27.md) · [목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) · [다음 →](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W29.md) |
| 주간 일지 | [`worklog/weekly/2026-W28.md`](https://github.com/hagenie128/ASAK/blob/main/worklog/weekly/2026-W28.md) |

---

## 확정·합의

| 항목 | 내용 | 상태 |
|---|---|---|
| 제품 톤 | 과제용·과한 라임톤이 아닌 **프랜차이즈형 실사용 키오스크**(버거킹형 명확성 + 샐러디/서브웨이형 깔끔함) | 확정 |
| 제품 한 줄 | 샐러드 주문을 빠르고 쉽게 하는 키오스크 + 관리자/주방 연동 실무형 시스템 | 확정 |
| 디자인 담당 | 김나연·이하진이 디자인 작업 담당 | 확정 |
| 관리자 화면 범위 | 로그인, 주문현황, 메뉴 관리·등록·수정, 매출 요약, 품절, 결제수단 등 UI 컴포넌트 설계 | 진행→완료(나연 7/8) |

## 선생님·채널

- DB 서버 접속 정보 공유 (7/8) — 본 문서에는 미기재
- 화면설계 페이지 데이터 저장이 로컬로 보이는 이슈 제기(하진) → 확인 요청

## 진척 (워크로그)

- **김나연**: 키오스크 레퍼런스 리서치·시안 선택, 고객/관리자 시안, 관리자 카테고리·핵심 화면 UI 컴포넌트
- **이하진**: React/Vite·mock 부트스트랩(메뉴/옵션/주문/결제), DS·터치 영역·비주얼 에셋 정리

## 미결·리스크

- 주문 취소/환불 요구사항 보강 필요 (팀 내부 인지)
- 관리자 매출 페이지 공백 인지 → 이후 스프린트에서 보강

## 관련 워크로그

> 해당 주차 기간에 존재하는 daily/entries 전체. 기간이 걸친 entries(-to-)는 겹치는 주차에 중복 표기. 작업 없는 날(파일 없음)은 나열하지 않는다.

### 이하진

- **daily**
  - worklog/daily/이하진/2026-07-06.md
  - worklog/daily/이하진/2026-07-09.md
  - worklog/daily/이하진/2026-07-10.md
- **entries**
  - worklog/entries/이하진/2026-07-06-worklog-onboarding.md
  - worklog/entries/이하진/2026-07-09-to-14-figma-design.md
  - worklog/entries/이하진/2026-07-10-frontend-mock-bootstrap.md

### 김나연

- **daily**
  - worklog/daily/김나연/2026-07-07.md
  - worklog/daily/김나연/2026-07-08.md
  - worklog/daily/김나연/2026-07-09.md
  - worklog/daily/김나연/2026-07-11.md
- **entries**
  - worklog/entries/김나연/2026-07-07-업무-정리.md
  - worklog/entries/김나연/2026-07-08-업무-정리.md
  - worklog/entries/김나연/2026-07-09-team-config.md
  - worklog/entries/김나연/2026-07-11-team-config.md

### 주간 워크로그

- `worklog/weekly/2026-W28.md`

- 참고 문서: [회의록 README §참고 문서](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07)
# 회의록 2026-W29 — 저장소 분리·Figma→코드·구현 경계

| 항목 | 내용 |
|---|---|
| 주차 | ISO 2026-W29 |
| 기간 | 2026-07-13 ~ 2026-07-19 |
| 팀 | 김나연, 이하진 (2인 체제 확정) |
| 목차 | [← 이전](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W28.md) · [목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) · [다음 →](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W30.md) |
| 주간 일지 | [`worklog/weekly/2026-W29.md`](https://github.com/hagenie128/ASAK/blob/main/worklog/weekly/2026-W29.md) |

---

## 확정·합의

| 항목 | 내용 | 상태 |
|---|---|---|
| 팀 구성 | 채널에서 일부 구성원 제외 → **김나연·이하진** 2인 | 확정 |
| 저장소 명칭 | ASAK-Kiosk / ASAK-Admin 분리 운영 | 확정 |
| 키오스크 해상도 | 1080×1920 기본 레이아웃 | 확정 |
| CSS 구조 | 전역(`commonStyle`/`tokens`) + 화면·컴포넌트별 CSS. Figma 결과물은 화면 단위 이식 후 공통만 추출 | 확정 |
| Figma→코드 경계 | UI·토큰·Variant·상태는 Figma/MCP; JSON/API·Zustand·가격·결제 로직은 코드에서 직접 구현 | 확정 |
| AI 구현 범위 | HTML/CSS 껍데기·정적 UI까지 허용. **상태·데이터 연결은 팀이 직접** | 확정 |
| 구현 순서(권장) | Figma·프로토타입 → 페이지/공통 컴포넌트/CSS → mock → 주문·결제 API | 확정 |

## 선생님 피드백

### 2026-07-14

- API path 형식 통일 (`/api/menus` 또는 `/api/v1/menus`) + **camelCase vs snake_case 통일 필요** — `선생님 지시` / 일부 `미결`
- Screen ID·문서 최신화 (예: SCR-001이 로그인으로 남아 있는 등 불일치)
- `layout/ny`: 전역 상태 과다 금지 → **주문 세션만** 전역. 메뉴·관리자 주문 목록 등 서버 데이터는 세션과 분리
- 결제 실패 시 장바구니 유지 / 성공·타임아웃 시에만 세션 초기화 — 초기화 함수 하나로 통일

### 2026-07-15

- WBS ID 중복(WBS-001 등) 정리 필요
- Admin 권장 순서: 로그인 → 세션 store → 라우트 → 주문 목록 → 상세·상태 전이 → 품절 → 메뉴 CRUD → 결제수단
- Kiosk: SCR-003 메뉴선택 우선 (URL 검증 → 카테고리 목록 → 카드·품절 클릭 방지 → 메뉴 ID 라우트)
- 주문 세션 store에 주문유형·장바구니·주문·결제 통합 방향 **유지 권장**

### 2026-07-16

- `OptionGroup.jsx` return을 JSX로 변환
- 디테일/상세 페이지 추가 후 피드백 가능

## 진척 (워크로그·협의)

- **이하진**: Figma 공통·관리자 컴포넌트, React 매핑, 0718 기준 Kiosk·Admin 정적 UI 이식(Kiosk PR #4 등), Agent Kit 배포
- **김나연**: 키오스크 레이아웃·주문/장바구니 로직 쪽 구현, guides 07~11 커밋, Admin 이관·키오스크 브랜치 작업 협의
- 팀 내부: MCP로 가져온 정적 UI와 나연 쪽 로직 구현 경계 재정렬(7/19 협의) → **정적 틀 + props/상태/API는 팀 구현**으로 재확정

## 블로커

- Backend business API 실연동 전 → mock 단계 유지 (`진행`)

## 관련 워크로그

> 해당 주차 기간에 존재하는 daily/entries 전체. 기간이 걸친 entries(-to-)는 겹치는 주차에 중복 표기. 작업 없는 날(파일 없음)은 나열하지 않는다.

### 이하진

- **daily**
  - worklog/daily/이하진/2026-07-13.md
  - worklog/daily/이하진/2026-07-14.md
  - worklog/daily/이하진/2026-07-15.md
  - worklog/daily/이하진/2026-07-16.md
  - worklog/daily/이하진/2026-07-17.md
  - worklog/daily/이하진/2026-07-18.md
  - worklog/daily/이하진/2026-07-19.md
- **entries**
  - worklog/entries/이하진/2026-07-15-figma-admin-review.md
  - worklog/entries/이하진/2026-07-16-figma-final-component-state-audit.md
  - worklog/entries/이하진/2026-07-16-notion-api-dto-db-audit.md
  - worklog/entries/이하진/2026-07-16-product-bible-wbs-release-governance.md
  - worklog/entries/이하진/2026-07-16-to-17-frontend-contract-handoff.md
  - worklog/entries/이하진/2026-07-17-asak-agent-kit-install-and-release.md
  - worklog/entries/이하진/2026-07-17-implementation-guides-and-assets.md
  - worklog/entries/이하진/2026-07-18-to-19-figma-static-ui.md

### 김나연

- **daily**
  - worklog/daily/김나연/2026-07-13.md
  - worklog/daily/김나연/2026-07-14.md
  - worklog/daily/김나연/2026-07-15.md
  - worklog/daily/김나연/2026-07-16.md
  - worklog/daily/김나연/2026-07-17.md
  - worklog/daily/김나연/2026-07-18.md
- **entries**
  - worklog/entries/김나연/2026-07-13-docs.md
  - worklog/entries/김나연/2026-07-14-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-15-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-16-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-17-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-18-kiosk-frontend.md

### 주간 워크로그

- `worklog/weekly/2026-W29.md`

- 참고 문서: [회의록 README §참고 문서](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07)
# 회의록 2026-W30 — mock 완성·백엔드 골격·제출

| 항목 | 내용 |
|---|---|
| 주차 | ISO 2026-W30 |
| 기간 | 2026-07-20 ~ 2026-07-26 |
| 팀 | 김나연, 이하진 |
| 목차 | [← 이전](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W29.md) · [목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) · [다음 →](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W31.md) |
| 주간 일지 | [`worklog/weekly/2026-W30.md`](https://github.com/hagenie128/ASAK/blob/main/worklog/weekly/2026-W30.md) |

---

## 확정·합의

| 항목 | 내용 | 상태 |
|---|---|---|
| 추가 디자인 | **추가 디자인 작업 중지**, 남은 페이지 흐름·함수 골격(차후 API 호출 자리) 우선 | 확정 (선생님 7/20) |
| Figma 추가 반입 | 토큰·공통 Variant·화면 상태·누락 에셋만. 화면 전체 재생성·실데이터 자동 연결 금지 | 확정 |
| 백엔드 스택 | Spring Boot 4.x + Java(수업 공지) + **MyBatis**. 데이터 가공은 SQL(XML)/뷰, Java는 상하차 | 확정 |
| orderType enum | `TAKE_OUT` / `EAT_IN` (`TAKEOUT` 표기 폐기) | 확정 |
| 결제수단 정본(DB) | `CARD`, `KAKAO_PAY`, `NAVER_PAY` (`SAMSUNG_PAY` 제거) | 확정 |
| 포맷터 | JS/CSS/JSON → Prettier, Java → Red Hat Java / Spotless. Prettier를 Java에 쓰지 않음 | 확정 |
| 패키지 | `admin` / `user` / `common` 유지, 전면 이동 금지 | 확정 |
| 프론트 발표물 | 키오스크·관리자 PPT 제출 (나연, 7/22) | 확정 |
| 미리보기 | Vercel Admin/Kiosk URL 공개 (7/21) | 확정 |
| 매출 집계 | `CANCELED` / `REFUNDED` 제외 | 확정 |
| Admin 결제수단 UI | Figma SCR-018 기준 4종 표시 — DB 정본과 표기 정합은 지속 점검 | 진행 |
| API 빈 목록 | 200 + 빈 목록 / 없는 주문 상세 → `ORDER_NOT_FOUND` | 확정 |

## 선생님 피드백

### 2026-07-20

- 디자인 추가 중지, 흐름·함수 골격 우선

### 2026-07-23

- DTO는 `dto/request`, `dto/response` 패키지 + 기능별 분리
- Mapper는 MyBatis **인터페이스**
- 수직 슬라이스: Controller → Service → Mapper → DB → 응답 DTO 한 경로로 완성

### 2026-07-24

- MCP(문서) 테이블 vs 실제 MySQL 스키마 비교·불일치 수정
- 권장 순서: 실행 기반 확정 → **메뉴 조회 수직** → **주문·결제 수직**(서버 재검증·주문번호·저장·결제 실패)
- 완료 기준: 메뉴 선택 → 주문 완료까지 **실제 DB 한 사이클**
- 백엔드도 프론트처럼 admin/user 분리 가능 — **구조 먼저 합의 후** 구현 (하진 질의 → 선생님 승인)

## 진척 (워크로그)

- **이하진**: Admin mock 바인딩(주문·품절·결제수단·매출·메뉴), API/Bruno/공통 응답, DB 뷰·계약, Admin 주문 조회 기반, AI guides·뷰 레퍼런스
- **김나연**: 키오스크 스케일 가이드 반영·커밋, Spring 백엔드 저장소 재구축·폴더/README, Mapper XML 구조, 고객 TC 착수, `ApiResponse` 공통 정리
- 채널: 백엔드 clone 주소 공유, 미사용 스캐폴딩 클래스(JWT 등)는 시점별 필요 시에만 도입

## 관련 워크로그

> 해당 주차 기간에 존재하는 daily/entries 전체. 기간이 걸친 entries(-to-)는 겹치는 주차에 중복 표기. 작업 없는 날(파일 없음)은 나열하지 않는다.

### 이하진

- **daily**
  - worklog/daily/이하진/2026-07-20.md
  - worklog/daily/이하진/2026-07-21.md
  - worklog/daily/이하진/2026-07-22.md
  - worklog/daily/이하진/2026-07-23.md
  - worklog/daily/이하진/2026-07-24.md
- **entries**
  - worklog/entries/이하진/2026-07-20-docs-wbs2-devcopilot-sync.md
  - worklog/entries/이하진/2026-07-20-mock-state-sprint.md
  - worklog/entries/이하진/2026-07-21-admin-mock-page-binding.md
  - worklog/entries/이하진/2026-07-23-admin-mock-figma-parity.md
  - worklog/entries/이하진/2026-07-23-api-contract-backend-foundation.md
  - worklog/entries/이하진/2026-07-24-db-contract-admin-order-foundation.md

### 김나연

- **daily**
  - worklog/daily/김나연/2026-07-20.md
  - worklog/daily/김나연/2026-07-21.md
  - worklog/daily/김나연/2026-07-22.md
  - worklog/daily/김나연/2026-07-23.md
  - worklog/daily/김나연/2026-07-24.md
- **entries**
  - worklog/entries/김나연/2026-07-20-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-21-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-22-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-23-kiosk-frontend.md
  - worklog/entries/김나연/2026-07-24-backend-api.md

### 주간 워크로그

- `worklog/weekly/2026-W30.md`

- 참고 문서: [회의록 README §참고 문서](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07)
# 회의록 2026-W31 — Admin API·계약 통일·연동 시작

| 항목 | 내용 |
|---|---|
| 주차 | ISO 2026-W31 |
| 기간 | 2026-07-27 ~ 2026-08-02 |
| 팀 | 김나연, 이하진 |
| 목차 | [← 이전](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W30.md) · [목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) · [다음 →](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W32.md) |

---

## 확정·합의

| 항목 | 내용 | 상태 |
|---|---|---|
| API 필드명 통일(제안→적용 방향) | `totalPrice`→`totalAmount`, `amount`→`approvedAmount`, `paidAt`→`approvedAt`, `waitingCount`→`waitingOrderCount`, `CANCELLED`→`CANCELED`, `PAID`→`APPROVED`, `STORE`→`EAT_IN`, `orderNumber`→`orderNo`, `lineTotal`→`lineAmount`, `priceDelta`→`extraPrice` 등 | 확정(방향) |
| DB 컬럼 | `orders.total_price` 등 **DB 컬럼명 유지**, API만 `totalAmount` 매핑 | 확정 |
| Live API | `GET /api/admin/orders/live` (목록용 `/active`와 분리) | 확정 |
| 환불 | 주문 `COMPLETED` 유지, 결제만 `REFUNDED` | 확정 |
| 제외 재료 | 정본 `item_exclusion` (legacy REQUEST 옵션과 중복 표시 금지) | 확정 |
| 프론트 mock | API 명세서 기준으로 컬럼명 맞춤; 백엔드는 명세서 보고 구현 병행 | 확정 |
| CORS·Admin API 설정 | 저장소에 반영 (7/28) | 확정 |

## 선생님 피드백

### 2026-07-27

- Admin 주문·상세·Live 완성분을 FE 연동 테스트 → 주문·결제 한 흐름 완성 후 연동 → WBS 갱신

### 2026-07-28

- 완성 백엔드 ↔ 키오스크/관리자 연동 테스트
- **상세메뉴 API 오류** 점검

### 2026-07-29

- 주문 상태 변경·취소를 실 API로
- 키오스크 음료/사이드 옵션 노출 수정
- 키오스크 주문~완료 BE 연동

### 2026-07-31

- `UserOrderService` 컴파일 오류 해결
- 키오스크 주문·결제 연동, Admin BE 연동
- **앞·뒤를 연결하며** 작업

## 진척 (워크로그)

- **이하진**: Live·메뉴·주문 API, 상세 금액 근거, `*Api.js` 모듈화, Live 상태변경/취소 FE–BE, Figma 토큰·환불 계약 문서
- **김나연**: (채널) API 명세서 필드(`unitAmount`↔`unitPrice` 등) 정본 확인·백엔드 반영, mock/명세 동기화 협의

## 미결

| 항목 | 내용 | 상태 |
|---|---|---|
| 주문 옵션 요청 | Product Bible `selectedOptionItemIds[]` vs DTO `optionItems[{ optionItemId, quantity }]` | 미결 |
| 메뉴 기본가 이름 | `price` / `unitPrice` / `basePrice` / `baseAmount` 혼용 → `baseAmount` 체계 제안 | 미결 |
| 상태변경 응답 | `previousStatus`/`status` vs `previousOrderStatus`/`orderStatus` | 미결 |
| 상태변경 path | `/{orderId}/{status}` vs `/{orderId}/status` | 미결 |
| API 명명 케이스 | camelCase vs snake_case 최종 통일 (7/14 선생님 지적) | 미결(지속) |

## 관련 워크로그

> 해당 주차 기간에 존재하는 daily/entries 전체. 기간이 걸친 entries(-to-)는 겹치는 주차에 중복 표기. 작업 없는 날(파일 없음)은 나열하지 않는다.

### 이하진

- **daily**
  - worklog/daily/이하진/2026-07-27.md
  - worklog/daily/이하진/2026-07-28.md
  - worklog/daily/이하진/2026-07-29.md
  - worklog/daily/이하진/2026-07-30.md
  - worklog/daily/이하진/2026-07-31.md
- **entries**
  - worklog/entries/이하진/2026-07-27-admin-live-menu-order-api.md
  - worklog/entries/이하진/2026-07-28-admin-order-detail-receipt-api-modules.md
  - worklog/entries/이하진/2026-07-29-admin-live-order-and-menu-option-catalog.md
  - worklog/entries/이하진/2026-07-30-figma-token-live-order-contract.md
  - worklog/entries/이하진/2026-07-31-backend-api.md

### 김나연

- **daily**
  - worklog/daily/김나연/2026-07-27.md
  - worklog/daily/김나연/2026-07-28.md
  - worklog/daily/김나연/2026-07-29.md
  - worklog/daily/김나연/2026-07-30.md
  - worklog/daily/김나연/2026-07-31.md
- **entries**
  - worklog/entries/김나연/2026-07-27-backend-api.md
  - worklog/entries/김나연/2026-07-28-backend-api.md
  - worklog/entries/김나연/2026-07-29-backend-api.md
  - worklog/entries/김나연/2026-07-30-backend-api.md
  - worklog/entries/김나연/2026-07-31-backend-api.md

### 주간 워크로그

- `worklog/weekly/2026-W31.md`

- 참고 문서: [회의록 README §참고 문서](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07)
# 회의록 2026-W32 — 실연동·관리자 CRUD·문서화

| 항목 | 내용 |
|---|---|
| 주차 | ISO 2026-W32 |
| 기간 | 2026-08-03 ~ 2026-08-07 |
| 팀 | 김나연, 이하진 |
| 목차 | [← 이전](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/2026-W31.md) · [목록](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md) |

---

## 확정·합의

| 항목 | 내용 | 상태 |
|---|---|---|
| 로컬 미리보기 | Admin/Kiosk `npm run dev -- --host`로 동일 Wi-Fi 기기 접속; Admin은 `/api` 프록시, Kiosk는 base URL 주의 | 확정(운영 팁) |
| Figma 백업 | 구독 종료 전 디자인 파일 백업본 공유 | 확정 |
| 팀 호칭 | 조 이름·프로젝트명(아삭) 정리 공유 | 참고 |

## 선생님 피드백

### 2026-08-04

1. 키오스크 장바구니 → 주문 생성 API 실연결 + DB 검증
2. 결제수단 조회·결제 승인 API 후 키오스크 결제 연결 (토스페이먼츠 예제 참고)
3. Admin 주문 통합 테스트 후 메뉴 → 품절 → 결제수단 → 매출 순 연동

### 2026-08-05 (Admin)

- 주문 목록·상세·Live·상태변경·취소 통합 테스트
- 메뉴 목록·상세·등록·수정 연동
- 품절 → 결제수단 → 매출 → 대시보드 순 mock 제거

### 2026-08-06

- Admin: 메뉴 추가·수정·삭제 + FE 연결; 품절·결제수단 Controller→Service→Mapper
- Kiosk: 결제수단 조회·결제 승인 BE; 장바구니 검증(실 DB)
- **회의록·위키·기타 문서 최신화**

### 2026-08-07

- Admin: 메뉴 CRUD, 매출/대시보드
- Kiosk: 장바구니 완료 후 주문·결제
- **기능 단위로 끝까지 완성**하는 순서 유지

## 진척 (워크로그)

- **이하진**: 관리자 메뉴 검색 draft/submit·상세 응답 shape, 메뉴 등록·결제수단·품절 API 요청 계약, MySQL 스키마 DDL·CORS 정리, `bootRun` 확인 (저장/삭제·HTTP 실호출·브라우저 회귀는 미검증 구간 존재)
- **김나연**: API-003 명세 변경 반영(옵션 그룹 REQUEST 제외, 제외 재료·칼로리·description), 백엔드·키오스크 연동 작업 지속

## 🗄️ DB 변경 사항

- MySQL 스키마 DDL 정리 및 CORS 허용 범위 조정 (8/07, `chore/mysql-schema-cors`)
- 그 외 별도 테이블 추가·삭제 없음
- **미검증** — 실제 DB 반영 결과와 뷰 합계 대조는 실행하지 않음

## 🧪 QA / 안정화

- 관리자 메뉴 상세 응답 shape·TODO 순서 정리, 주문 상태 전이·취소 가드 구현
- `bootRun` 기동 확인
- **미실행** — HTTP 실호출 회귀, 브라우저 회귀, 통합 QA 1사이클, QA 테스트 실행 기록

## ⚠️ 확인 필요 사항

이번 주 신규로 확인된 **결정↔구현 갭** (전체 표는 이 문서 상단 참조)

1. `ASAK-Kiosk/src/adapters/orderAdapter.js:20`이 `return payload` — W31에서 정한 필드명 변환이 **경계에 자리만 있고 미구현**. 실연동 시 `orderNumber`/`totalPrice`/`waitingCount`가 그대로 흘러감
2. 결제수단이 kiosk mock **8종** / Admin Figma **4종** / DB 정본 **3종**으로 갈림. kiosk `methodId`는 소문자 슬러그라 `paymentMethodCode` enum과 형식도 다름
3. `STORE`·`CANCELLED`·`priceDelta` 등 폐기 표기가 kiosk mock과 `scripts/expand-mocks.js`에 잔존

## 📌 Action Items

### 👤 김나연

- 키오스크 장바구니 검증(실 DB) → 주문 생성 실연동
- `createOrder()` 저장 완성 (현재 검증 후 `null` 반환)
- `UserOrderService` 컴파일·런타임 안정성 확인
- 상세메뉴 API 오류 재발 여부 점검

### 👤 이하진

- Admin 메뉴 CRUD 완성·연동 → 품절 → 결제수단 → 매출·대시보드 mock 제거
- 결제수단 조회·승인 API 완성 (키오스크 결제 연결의 선행)
- `orderAdapter` 변환 구현 또는 mock 정본화 중 택일
- 결제수단 3종/4종/8종 불일치 정리

### 👥 공통

- 메뉴 선택 → 장바구니 → 주문 → 결제 → 완료 통합 QA 1사이클
- 계약 미결(옵션 요청·단가 필드·상태변경 path·API 케이스) 확정 후 양쪽 반영
- QA TC 실행 기록 남기기

## 관련 워크로그

> 해당 주차 기간에 존재하는 daily/entries 전체. 기간이 걸친 entries(-to-)는 겹치는 주차에 중복 표기. 작업 없는 날(파일 없음)은 나열하지 않는다.

### 이하진

- **daily**
  - worklog/daily/이하진/2026-08-05.md
  - worklog/daily/이하진/2026-08-06.md
  - worklog/daily/이하진/2026-08-07.md
- **entries**
  - worklog/entries/이하진/2026-08-05-admin.md
  - worklog/entries/이하진/2026-08-06-admin-menu-search-and-detail-contract.md
  - worklog/entries/이하진/2026-08-07-mysql-schema-cors.md
  - worklog/entries/이하진/2026-08-07-wbs-study-rtos-docs.md

### 김나연

- **daily**
  - worklog/daily/김나연/2026-08-04.md
  - worklog/daily/김나연/2026-08-05.md
  - worklog/daily/김나연/2026-08-06.md
  - worklog/daily/김나연/2026-08-07.md
- **entries**
  - worklog/entries/김나연/2026-08-04-kiosk-frontend.md
  - worklog/entries/김나연/2026-08-05-backend-api.md
  - worklog/entries/김나연/2026-08-06-kiosk-frontend.md
  - worklog/entries/김나연/2026-08-07-kiosk-cart-api.md

### 주간 워크로그

- `worklog/weekly/2026-W32.md`

- 참고 문서: [회의록 README §참고 문서](https://github.com/hagenie128/ASAK/blob/main/docs/operations/meeting-minutes/README.md#참고-문서-2026-08-07)
