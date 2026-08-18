# ASAK 프로젝트 2조 회의록

> Status: **CANONICAL**
> 아래 상태·갭 서술은 **2026-08-07 시점 스냅샷**이며 현재 구현 상태로 해석하지 않습니다.
> Hub 통합본: [`../../wiki/meeting-minutes-weekly.md`](../../wiki/meeting-minutes-weekly.md)
> 개인/팀 주간 rollup: [`../../../worklog/weekly/`](../../../worklog/weekly/README.md)

| 항목 | 내용 |
|---|---|
| 기간 | 2026-07-01 ~ 2026-08-07 |
| 팀 | 프로젝트 2조 (최종 구성: **김나연**, **이하진**) |
| 프로젝트 | ASAK — 샐러드 키오스크 + 관리자 연동 |
| 문서 성격 | 공식 회의록 (주차별) |
| 작성일 | 2026-08-07 |
| 근거 | 2조 공용 채널, 팀 내부 협의, 로컬 `worklog/daily`·`entries`·`weekly` |

> **범위 안내**
> - 최종 팀원(김나연·이하진) 기준으로만 기록한다.
> - 일상 잡담·개인 신상·시크릿(계정·비밀번호)은 수록하지 않는다.
> - 상태 표기: `확정` / `진행` / `미결` / `선생님 지시`

---

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
> 근거 정본: [`wiki/current-status-baseline.md`](../../wiki/current-status-baseline.md)

---

## 주차별 회의록

| 주차 | 기간 | 주제 | 파일 |
|---|---|---|---|
| W27 | 06-29 ~ 07-05 | 킥오프·기획 정비 | [2026-W27.md](2026-W27.md) |
| W28 | 07-06 ~ 07-12 | 디자인 방향·관리자 UI 골격 | [2026-W28.md](2026-W28.md) |
| W29 | 07-13 ~ 07-19 | 저장소 분리·Figma→코드·구현 경계 | [2026-W29.md](2026-W29.md) |
| W30 | 07-20 ~ 07-26 | mock 완성·백엔드 골격·제출 | [2026-W30.md](2026-W30.md) |
| W31 | 07-27 ~ 08-02 | Admin API·계약 통일·연동 시작 | [2026-W31.md](2026-W31.md) |
| W32 | 08-03 ~ 08-07 | 실연동·관리자 CRUD·문서화 | [2026-W32.md](2026-W32.md) |
| W33 | 08-10 ~ 08-16 | 키오스크 실API·관리자 메뉴 연동 | [2026-W33.md](2026-W33.md) |
| W34 | 08-17 ~ 08-21 | 장치 이벤트/RTOS 연동 | [2026-W34.md](2026-W34.md) |

---

## 남은 일정 (선생님 2026-08-18)

| 기간 | 단계 | 목표 |
|---|---|---|
| 08/17 ~ 08/21 | 장치 이벤트/RTOS | `device_event`, 콘솔. 적어도 Spring Boot와 React 연동 |
| 08/24 ~ 08/28 | 통합 테스트/기능 마감 | 오류 수정, 태블릿 테스트, 피드백 일부 반영 |
| 08/31 ~ 09/01 | 발표 준비 | README, PPT, 리허설 |
| 09/02 | 시연 및 발표 | 최종 |

상세 로드맵(과거 주차 포함): [`wiki/wbs.md`](../../wiki/wbs.md#남은-일정-선생님-2026-08-18)

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
> 아직 **정하지 못한** 것은 아래 [계약 미결](#계약-미결-2026-08-07)에 둔다. 둘을 섞지 않는다.

| # | 결정 | 결정 시점 | 코드 실측 (2026-08-07) | 판정 |
|---|---|---|---|---|
| 1 | 필드명 정본 변환은 **adapter 경계에서만** 수행 | W31 | `ASAK-Kiosk/src/adapters/orderAdapter.js:20` 당시 경로에서 `return payload` — TODO 주석만 있고 변환 **미구현** | ❌ 미반영 |
| 2 | `orderType` = `EAT_IN` / `TAKE_OUT` (`STORE`·`TAKEOUT` 폐기) | W30·W31 | BE `OrderType.java` 준수 ✅ / 과거 mock `asak-data/archive/frontend-mocks/student-project-data.json`에 `"STORE"` 잔존(런타임 미사용) | ✅ 프론트 런타임 정리됨 |
| 3 | 취소 철자 `CANCELED` | W31 | BE `OrderStatus.java`·`PaymentStatus.java` 준수 ✅ / `scripts/expand-mocks.js:520,549,652`가 `CANCELLED` 생성 | ⚠️ mock 생성기 미정리 |
| 4 | 옵션 추가금 필드 `extraPrice` | W31 | BE `add_price AS extraPrice` 준수 ✅ / kiosk mock JSON 전반 `priceDelta` | ⚠️ mock만 미정리 |
| 5 | 결제수단 정본 **3종** `CARD`·`KAKAO_PAY`·`NAVER_PAY` | W30 | kiosk mock **8종**(`card`,`kakao`,`naver`,`toss`,`payco`,`apple`,`cash`,`zero`) / Admin Figma SCR-018 **4종** / DB 정본 **3종**. 게다가 kiosk는 `methodId` 소문자 슬러그로 `paymentMethodCode` enum과 **형식도 불일치** | ❌ 3중 불일치 |
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
3. 위 **확인 필요 사항** 표의 1·5번 정리 (adapter 변환, 결제수단 3중 불일치)
4. Screen ID·WBS ID·위키와 코드 정합 유지

### 👥 공통

1. 인증 없는 흐름 기준 **메뉴 선택 → 장바구니 → 주문 → 결제 → 완료** 통합 QA 1사이클
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

> 회의록과 같이 볼 **현재 정본**. WBS는 [`wbs.md`](../../wiki/wbs.md).

### 입구·상태

| 종류 | 링크·경로 |
|---|---|
| 문서 입구 | [`docs/START_HERE.md`](../../START_HERE.md) |
| 영역별 현황 | [`wiki/current-status-baseline.md`](../../wiki/current-status-baseline.md) |
| 구현 맵 (SCR) | [`planning/current-implementation-map-2026-07-16.md`](../../planning/current-implementation-map-2026-07-16.md) |
| 전체 흐름도 | [`wiki/project-flow.md`](../../wiki/project-flow.md) |

### 계획·WBS

| 종류 | 링크·경로 |
|---|---|
| WBS 정본 | [`wiki/wbs.md`](../../wiki/wbs.md) (`WBS-001`~`085`) |
| WBS 상태 메모 | [`wiki/wbs-status-notes.md`](../../wiki/wbs-status-notes.md) |
| DONE·PASS 점검 | [`ai-reports/2026-08-07/asak-done-pass-audit.md`](../../ai-reports/2026-08-07/asak-done-pass-audit.md) |
| WBS 일정 rebase | [`ai-reports/2026-08-07/asak-wbs-date-rebase.md`](../../ai-reports/2026-08-07/asak-wbs-date-rebase.md) |

### 계약·DB·API

| 종류 | 링크·경로 |
|---|---|
| 정본 계약 | [`governance/canonical-contract-decisions-2026-07-16.md`](../../governance/canonical-contract-decisions-2026-07-16.md) |
| REST API 명세 | [`wiki/rest-api-spec.md`](../../wiki/rest-api-spec.md) |
| DB 테이블 | [`wiki/db-table-definition.md`](../../wiki/db-table-definition.md) |
| DB 뷰 | [`wiki/db-view-definition.md`](../../wiki/db-view-definition.md) |
| MySQL 스키마 DDL | `ASAK-back/docs/아삭_mysql.sql` · 뷰 `ASAK-back/docs/view.sql` (파일 반영 · **실DB 적용 미검증**) |

### 회의록·워크로그

| 종류 | 링크·경로 |
|---|---|
| 주차별 정본 | 이 폴더 [`README`](README.md) · [W27](2026-W27.md)~[W32](2026-W32.md) |
| Hub 업로드본 | [`wiki/meeting-minutes-weekly.md`](../../wiki/meeting-minutes-weekly.md) |
| 워크로그 Hub 인덱스 | [`wiki/worklog-index.md`](../../wiki/worklog-index.md) (daily · entries · weekly 링크) |
| 산출물 체크리스트 | [`wiki/meeting-deliverables-checklist.md`](../../wiki/meeting-deliverables-checklist.md) |
| 주간 워크로그 | [W28](../../../worklog/weekly/2026-W28.md) · [W29](../../../worklog/weekly/2026-W29.md) · [W30](../../../worklog/weekly/2026-W30.md) · [W31](../../../worklog/weekly/2026-W31.md) · [W32](../../../worklog/weekly/2026-W32.md) |
| daily / entries | `worklog/daily/{김나연\|이하진}/` · `worklog/entries/{김나연\|이하진}/` |

### 미리보기·학습

| 종류 | 링크·경로 |
|---|---|
| Kiosk 미리보기 | https://asak-kiosk.vercel.app/ |
| Admin 미리보기 | https://asak-admin.vercel.app/ |
| RTOS 공부 노트 | [`docs/study/RTOS/RTOS.md`](../../study/RTOS/RTOS.md) |
| 스케일 가이드 | 채널 공유 `ASAK_FRONT_S9_ULTRA_SCALE_APPLY_GUIDE.md` |

---

## 문서 이력

| 일자 | 내용 |
|---|---|
| 2026-08-07 | 초안(통합본). 2조 채널·팀 협의·워크로그 통합. |
| 2026-08-07 | 주차별 파일 분리 (`meeting-minutes/2026-W*.md`). |
| 2026-08-07 | 상태 스냅샷·`⚠️ 확인 필요 사항`(결정↔구현 갭) 신설, Action Items 담당자 배정, 역할표에 백엔드 도메인 분담 반영. 회의록 [`_TEMPLATE.md`](_TEMPLATE.md) 추가. |
| 2026-08-07 | 참고 문서 섹션을 `wbs.md`·START_HERE·baseline·API/DB·DONE/PASS 점검 등 현재 정본으로 갱신. |
