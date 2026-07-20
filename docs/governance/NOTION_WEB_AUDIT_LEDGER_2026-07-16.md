# Notion Web Audit Ledger — 2026-07-16

> **PARTIAL AUDIT — RESUME REQUIRED**
>
> 기준 Repository commit: `1e4fa2e4b15fc958a0be6d2a39ca849798e4d415` (PR #5 merge commit)
>
> 원칙: 이 Ledger는 Notion Web의 실제 페이지·Database record를 개별 열람한 결과만 기록한다. 검색 제목만으로 판정하지 않으며, 수정은 재열람으로 확인한다.

## 현재 범위와 수치의 의미

| 구분 | 수치 | 의미 |
|---|---:|---|
| 발견 | P0 120 / P1·P2 48 | 키워드 검색의 순위 결과 수. 중복 결과를 포함하며, 열람·검증 완료를 뜻하지 않는다. |
| 실제 개별 열람 | 33 | 상위 문서/DB 10건, WBS·요구사항 record 12건, 화면·API 대표 record 11건 |
| 수정 후 재열람 검증 | 10 | 상위 문서 5건과 DB record 5건의 변경 반영 확인 |
| 실제 수정 | 10 | 상위 문서 5건, DB record 5건 |

P0는 **초기 감사만 수행**했다. P1/P2는 후보 검색만 수행했으며 개별 열람·검증·수정은 아직 시작하지 않았다. 열지 않은 record를 `VERIFIED`로 표기하지 않는다.

### 재개 세션 집계 (2026-07-16)

| 구분 | 수치 | 의미 |
|---|---:|---|
| 실제 OPENED record | 16 | 화면 DB record 11건, Cart/Sold-out/관련 API record 5건을 개별로 열람. 상위 화면 DB schema 재열람 1건은 record 수에 미포함. |
| VERIFIED | 14 | 수정한 Notion record를 개별 재열람하여 속성 또는 본문 반영을 확인. |
| MODIFIED | 14 | 기존 화면 record 9건 정정, 월별/일별 매출 record 2건 생성, Cart/Sold-out/스크린 상태 3건 정정. |
| SEARCH_RESULT_ONLY | 19 | 검색 후보만 확인했으며 개별 열람하지 않은 고유 페이지 수. |
| NOT_ACCESSIBLE | 0 | 접근 실패 없음. |

이 세션도 P0 일부만 검증했다. 따라서 상태는 계속 **PARTIAL AUDIT — RESUME REQUIRED** 이다.

## 다음 시작 지점

1. **Batch 3 시작 record: API-007 `관리자 주문 목록/상세 조회`** — 검색으로 존재만 확인했으며 열람하지 않았다. API-006은 이번 Batch에서 `POST /api/kiosk/payments` 후보와 승인 DTO를 실제 record·Backend 근거로 확인했다.
2. `GET /api/sold-out/status`는 exact record 검색 결과가 0건이다. 새 API를 만들거나 canonical으로 승격하지 말고, 메뉴 목록/상세 응답과의 역할 중복 및 Backend 구현 근거부터 확인한다.
3. DB는 Notion 설계 문서만 확인됐다. Entity/Migration/Schema 근거가 생기기 전에는 `IMPLEMENTED`로 바꾸지 않는다. WBS·Requirements는 다음 별도 Batch에서만 다룬다.

## 기준 문서

- `docs/wiki/current-status-baseline.md`
- `docs/wiki/devcopilot-sync-report.md`
- `docs/wiki/wbs-v2.md`
- `docs/wiki/legacy-wbs2-mapping-audit-2026-07-16.md`
- `docs/wiki/rest-api-spec.md`, `docs/wiki/db-audit-plan.md`, `docs/wiki/qa-test-cases.md`
- `docs/product_bible/07_Screen_Bible/docs/07-screens/SCREEN_REGISTRY.md`

## 배치 체크포인트

| Batch | 우선순위 | 범위 | 개별 열람 | 수정 | 결과 |
|---|---|---|---:|---:|---|
| 0 | Setup | main 기준 문서 및 Notion 연결 확인 | 0 | 0 | 완료 — 연결 워크스페이스와 ASAK 허브 확인 |
| 1 | P0 | WBS·요구사항·화면·API·DB 상위 문서와 5개 인라인 DB 구조 확인 | 10 | 5 | 완료 — 상위 문서에 현재 기준 병기, 각 수정 직후 재열람 완료 |
| 2 | P0 | WBS/요구사항 record 후보 개별 열람 | 12 | 2 | 완료 — 근거가 명확한 2건만 상태·비고 정정, 나머지는 보존 |
| 3 | P0 | 화면/API DB 후보 조회 및 대표 record 개별 열람 | 11 | 3 | 완료 — 화면은 구현 완료 오표기 없음, API 경로 불일치 3건을 검토중으로 전환 |
| 4 | P1/P2 | 디자인·QA·Git·회의록·워크로그·아카이브 키워드 후보 검색 | 0 | 0 | 완료 — 후보만 수집, 개별 열람·수정은 다음 배치 |
| 5 | P0 | DB 설계·테이블 정의 재검색 | 0 | 0 | 완료 — DB 설계는 단일 문서 중심이며 별도 테이블 모델 DB는 검색 결과에서 확인되지 않음 |
| 6 | P0 | Screen Registry: SCR-009/010/011/015/016/018/019 및 잘못 배정된 SCR-020/021 | 9 | 9 | 완료 — C handoff 참조와 ID/명칭을 정정하고 기존 영수증·멤버십 record는 삭제 없이 SCR-023/024로 재매핑 |
| 7 | P0 | Screen Registry 누락 SCR-020/021 | 2 | 2 | 완료 — 중복 조회 0건 후 월별 매출·일별 매출 record를 생성하고 즉시 재열람 |
| 8 | P0 | Cart·Sold-out 시나리오/요구사항/화면/API 후보 | 5 | 3 | 완료 — Cart 정책, SCR-005 상태 누락, Sold-out 정책을 정정. API-016은 Batch 2에서 계약 확정 필요 |
| 9 | P0 | API-002~006/009/010/016 | 8 | 8 | 완료 — 8건을 개별 열람·수정·재열람. Backend에는 `/api/health` 외 controller가 없어 구현 완료 표기 없음. API-016은 Client-only Cart 정책에 따라 `LEGACY`로 분류 |
| 10 | P0 | DB 설계 키워드 `menu`~`cartItemId` | 1 | 1 | 완료 — 단일 DB 설계 문서를 열람·수정·재열람. Entity/Migration/Schema 근거 부재로 `IMPLEMENTED` 금지 |

## 변경 및 판정 기록

| 대상 URL/ID | 유형 | 우선순위 | 판정 | 변경 전 → 후 | 검증 근거 | 비고 |
|---|---|---|---|---|---|---|
| `cd951ef0-4f0b-82b0-81de-019cc9a4c580` | 프로젝트 허브 | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | WBS·요구사항 등 하위 프로젝트 허브 연결 확인 |
| `dfd51ef0-4f0b-820e-9b5a-01f2c1343d16` | WBS DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | `작업 ID`, `상태`, `진척률`, 요구사항 Relation 존재 |
| `22551ef0-4f0b-8217-94d4-012f787551bc` | 요구사항 DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | WBS·시나리오 Relation 존재 |
| `f9251ef0-4f0b-83a6-85ef-8190b77d5748` | 화면 DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | 화면 설계 상위 문서 하위 DB |
| `56a51ef0-4f0b-83fb-bfb0-81c63640f66d` | API DB | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | API 명세 상위 문서 하위 DB |
| `1d951ef0-4f0b-8301-9b42-81f04c7b12cc` | DB 설계 문서 | P0 | 구조 확인 | 변경 없음 | Notion Web 개별 열람 | P0 대상 문서로 식별 |
| `1ab51ef0-4f0b-8330-afca-012a4e8d14fa` | WBS 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 기존 WBS 본문 보존 |
| `81b51ef0-4f0b-8259-a933-01381182f754` | 요구사항 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 구현율 0.0%, 일괄 DONE 없음 |
| `1c751ef0-4f0b-825e-a3aa-8145f563bbc8` | 화면 설계 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | DESIGN_DONE과 구현 완료 분리 |
| `34651ef0-4f0b-838c-a3a4-81e55eebfb2b` | API 상위 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 명세와 백엔드 구현 분리 |
| `1d951ef0-4f0b-8301-9b42-81f04c7b12cc` | DB 설계 문서 | P0 | 현재 기준 병기 | 하단 정합성 기준 추가 | 수정 후 Notion Web 재열람 | 모델과 애플리케이션 구현 분리 |
| `39151ef0-4f0b-81ee-8778-c89fce69ea1d` | WBS-001 record | P0 | 정정 | 예정/미기재 → 완료/100% | 수정 후 Notion Web 재열람 | 설계·데이터 정의 완료만 의미, React/API/QA 완료 아님 |
| `39151ef0-4f0b-8193-ab52-ec6221dfd7b3` | FWD-CART-002 포장봉투 추가 | P0 | 정정 | 예정 → 제외 | 수정 후 Notion Web 재열람 | 기존 설명이 이미 Future Scope였음 |
| `3a551ef0-4f0b-8376-bd80-87f10660acc4` | 화면 설계 DB | P0 | 후보 조회 | 변경 없음 | 20 record 조회, 대표 5 record 개별 열람 | 모두 `개발 완료=아니오`; Figma/구현 근거 불충분으로 상태 보존 |
| `98151ef0-4f0b-82c8-91e2-87cc01b9eb15` | API 명세 DB | P0 | 후보 조회 | 변경 없음 | 20 record 조회, API-002/003/004/005/006/009 개별 열람 | 구현 완료 표기 없음 |
| `04851ef0-4f0b-831a-bbe6-01a5cd258ac9` | API-002 record | P0 | 정정 | 예정 → 검토중 | 수정 후 Notion Web 재열람 및 DB 재조회 | `/api/menus`와 최신 목표 경로 간 계약 결정 필요 |
| `39251ef0-4f0b-81b6-a23b-d0da22f3632e` | API-003 record | P0 | 정정 | 예정 → 검토중 | 수정 후 Notion Web 재열람 및 DB 재조회 | legacy `/api/menus/**` 계약 검토 필요 |
| `39151ef0-4f0b-8165-83b6-f7d373600582` | API-004 record | P0 | 정정 | 예정 → 검토중 | 수정 후 Notion Web 재열람 및 DB 재조회 | legacy `/api/menus/**` 계약 검토 필요 |
| `39151ef0-4f0b-816a-89b6-c3b956e9974a` | SCR-009 | P0 | MODIFIED / VERIFIED | 관리자 주문 관리 → 관리자 실시간 주문; C handoff 참조 추가 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; legacy 링크는 비고에 보존, `PENDING_FIGMA_CONFIRMATION` |
| `39251ef0-4f0b-8186-9277-fd3fc980ff52` | SCR-010 | P0 | MODIFIED / VERIFIED | 관리자 주문 상세 → 관리자 주문 관리; C handoff 참조 추가 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; 구현 완료 표기 없음 |
| `39151ef0-4f0b-8111-89b2-fc39fe4f1959` | SCR-011 | P0 | MODIFIED / VERIFIED | 관리자 판매 항목 품절 관리 → 관리자 품절 관리; C handoff 참조 추가 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; Sold-out 세부 정책은 별도 흐름 page에서 정정 |
| `39251ef0-4f0b-81ad-9057-eec10351023e` | SCR-015 | P0 | MODIFIED / VERIFIED | legacy Figma → C handoff 참조 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; Login 유지, `PENDING_FIGMA_CONFIRMATION` |
| `39251ef0-4f0b-812f-ba53-ed19e6089d7b` | SCR-016 | P0 | MODIFIED / VERIFIED | legacy Figma → C handoff 참조 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; Menu Management 유지 |
| `39251ef0-4f0b-81b0-84fa-e81a1dc8e1c7` | SCR-018 | P0 | MODIFIED / VERIFIED | 관리자 결제수단 설정 → 관리자 결제 설정; C handoff 참조 추가 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; SCR-015 Toggle Changed record는 Screen DB 검색에서 0건 |
| `39251ef0-4f0b-813d-8e9f-f5fa34adf007` | SCR-019 | P0 | MODIFIED / VERIFIED | legacy Figma → C handoff 참조 | 수정 후 Notion Web 개별 재열람 | `FIGMA_REFERENCE_MISMATCH`; Sales Summary 유지 |
| `39551ef0-4f0b-810a-84aa-e4af6de3d5c7` | Receipt Output | P0 | MODIFIED / VERIFIED | SCR-020 → SCR-023 | 수정 후 Notion Web 개별 재열람 | 삭제하지 않고 재매핑; MVP 제외 및 `PENDING_FIGMA_CONFIRMATION` |
| `39551ef0-4f0b-810c-bfac-fec11674a302` | Membership/Coupon | P0 | MODIFIED / VERIFIED | SCR-021 → SCR-024 | 수정 후 Notion Web 개별 재열람 | 삭제하지 않고 재매핑; MVP 제외 및 `PENDING_FIGMA_CONFIRMATION` |
| `39f51ef0-4f0b-8162-acd1-f8814cc9ebb1` | SCR-020 Monthly Sales | P0 | MODIFIED / VERIFIED | 신규 record 생성 | 생성 직후 Notion Web 개별 열람 | 중복 조회 0건. `PENDING_FIGMA_CONFIRMATION`, API는 `NEEDS_CONFIRMATION` |
| `39f51ef0-4f0b-81f2-bd23-cc44476868fa` | SCR-021 Daily Sales | P0 | MODIFIED / VERIFIED | 신규 record 생성 | 생성 직후 Notion Web 개별 열람 | 중복 조회 0건. `PENDING_FIGMA_CONFIRMATION`, API는 `NEEDS_CONFIRMATION` |
| `39151ef0-4f0b-81ab-9a44-d01540d67a95` | SC-009 Cart 수정 시나리오 | P0 | MODIFIED / VERIFIED | Client-only Cart, 수량 1 minus disabled, 별도 삭제/전체비우기, cartItemId 수정, 9/30 제한, 재검증 정책 추가 | 수정 후 Notion Web 개별 재열람 | `CART_POLICY_MISMATCH` 정정 |
| `39151ef0-4f0b-8116-bfff-d862136bfde4` | FWD-CART-003 | P0 | OPENED | 변경 없음 | Notion Web 개별 열람 | 기존 FWD-CART-002 중복으로 `제외` 상태 유지; 정책은 SC-009에서 보완 |
| `39151ef0-4f0b-81ad-b474-ddf94c33827d` | SCR-005 Cart | P0 | MODIFIED / VERIFIED | legacy Figma → C handoff; 편집/삭제/비우기/품절/결제차단 상태를 누락으로 기록 | 수정 후 Notion Web 개별 재열람 | `SCREEN_STATE_MISSING`, `FIGMA_REFERENCE_MISMATCH`; 모든 상태 `PENDING_FIGMA_CONFIRMATION` |
| `39251ef0-4f0b-816b-8473-d1ab408cd8ed` | Sold-out 관리 흐름 | P0 | MODIFIED / VERIFIED | CORE/DEFAULT/BASE/Category/Cart 재검증 정책으로 교체 | 수정 후 Notion Web 개별 재열람 | `SOLD_OUT_POLICY_MISMATCH` 정정 |
| `39251ef0-4f0b-8127-a34b-e3534f376a63` | API-016 Cart 검증 | P0 | MODIFIED / VERIFIED / LEGACY | server Cart validation endpoint를 Client-only 정책과 대조 | 수정 후 Notion Web 개별 재열람 | `cartItemId`·수량 1/0/9/30 정책과 Cart View Model DTO 차이를 기록 |
| `04851ef0-4f0b-831a-bbe6-01a5cd258ac9` | API-002 메뉴 목록 | P0 | MODIFIED / VERIFIED / SPEC_ONLY | `GET /api/menus` → `GET /api/kiosk/menuList`; camelCase response·Owner·Last Verified 기록 | 수정 후 Notion Web 개별 재열람, ASAK-back controller scan | Backend는 `/api/health`만 확인. 구현 완료 아님 |
| `39251ef0-4f0b-81b6-a23b-d0da22f3632e` | API-003 메뉴 상세 | P0 | MODIFIED / VERIFIED / SPEC_ONLY | `GET /api/menus/{menuId}` → `GET /api/kiosk/menuDetail/{menuId}`; optionGroups 및 DTO/View Model 경계 기록 | 수정 후 Notion Web 개별 재열람, Product Bible `MENU_API_CONTRACT.md` | Backend menu controller 근거 없음 |
| `39151ef0-4f0b-8165-83b6-f7d373600582` | API-004 메뉴 옵션 | P0 | MODIFIED / VERIFIED / NEEDS_CONFIRMATION | legacy options endpoint의 menuDetail `optionGroups` 중복을 기록 | 수정 후 Notion Web 개별 재열람 | 별도 endpoint 필요성 미확정, 구현 완료 아님 |
| `30b51ef0-4f0b-8358-af2f-01c096421506` | API-005 주문 생성 | P0 | MODIFIED / VERIFIED / SPEC_ONLY | `POST /api/orders` → `POST /api/kiosk/orders`; `totalAmount` 등 response 계약 기록 | 수정 후 Notion Web 개별 재열람, Product Bible `ORDER_API_CONTRACT.md` | Backend order controller 근거 없음 |
| `36651ef0-4f0b-829b-94e5-01c66c7c66a9` | API-006 가상 결제 처리 | P0 | MODIFIED / VERIFIED / SPEC_ONLY | `POST /api/payments` → `POST /api/kiosk/payments`; `approvedAmount`·`approvedAt`·`waitingOrderCount` response 계약 기록 | 수정 후 Notion Web 개별 재열람, Product Bible `PAYMENT_API_CONTRACT.md` | Backend payment controller 근거 없음 |
| `39151ef0-4f0b-8180-9b72-c1daaac09498` | API-009 품절 처리 | P0 | MODIFIED / VERIFIED / SPEC_ONLY | `PATCH /api/admin/sold-out-items` → `PATCH /api/admin/soldOut` 후보 및 Owner 기록 | 수정 후 Notion Web 개별 재열람 | Backend sold-out controller 근거 없음 |
| `39251ef0-4f0b-8184-853e-c576e1b9ba99` | API-010 관리자 판매 항목 목록 | P0 | MODIFIED / VERIFIED / NEEDS_CONFIRMATION | admin list 후보와 `GET /api/sold-out/status` 부재를 구분 | 수정 후 Notion Web 개별 재열람 | menuList/menuDetail와 역할 중복 가능, Backend 근거 없음 |
| `1d951ef0-4f0b-8301-9b42-81f04c7b12cc` | DB 설계 문서 | P0 | MODIFIED / VERIFIED | `menu`·`ingredient`·`base`·`category`·`option`·`allergen`·`soldOut`=`SPEC_ONLY`; `order`·`payment`=`NEEDS_CONFIRMATION`; DB 영속 `cartItemId`=`LEGACY` | 수정 후 Notion Web 개별 재열람, Entity/Migration/Schema 파일 검색 | 설계/ERD·seed는 구현 근거가 아님. 화면 문구는 DTO가 아니라 View Model/Selector에서 생성 |

### Batch 2 세션 집계 (2026-07-16)

| 구분 | 수치 | 의미 |
|---|---:|---|
| DISCOVERED | 1 | `API-007 관리자 주문 목록/상세 조회`는 검색으로 존재만 확인했고 개별 열람하지 않았다. |
| OPENED | 9 | API record 8건과 DB 설계 문서 1건을 실제로 열람했다. |
| VERIFIED | 9 | 수정한 9건을 각각 재열람했다. |
| MODIFIED | 9 | API 8건과 DB 설계 문서 1건의 속성 또는 본문에 감사 근거를 기록했다. |
| SEARCH_RESULT_ONLY | 7 | exact `GET /api/sold-out/status` 및 DB 키워드 검색의 고유 후보. 검색 결과만으로 수정·검증하지 않았다. |
| NOT_ACCESSIBLE | 0 | 접근 실패 없음. |

**Batch 2 분류 수치:** API record 기준 `SPEC_ONLY` 5건(API-002/003/005/006/009), `NEEDS_CONFIRMATION` 4건(API-002/003의 DTO 필드 차이, API-004/010의 별도 endpoint 필요성), `LEGACY` 1건(API-016)이다. 한 record가 SPEC_ONLY이면서 확인 필요 쟁점을 가질 수 있어 중복 집계가 있다. DB 설계 문서 안의 논리 데이터 항목은 `SPEC_ONLY` 6개(menu, ingredient, base, category, option, allergen/soldOut 정책), `NEEDS_CONFIRMATION` 2개(order, payment), `LEGACY` 1개(cartItemId DB 영속 후보)로 기록했다. `IMPLEMENTED`는 0건이다.

## 다음 배치 후보

| 우선순위 | 실제 Notion 후보 | 다음 확인 목적 |
|---|---|---|
| P1 | `2026-07-09~14 이하진 Figma 디자인 작업`, `Figma 가이드 + SCR×Figma 매트릭스` | 디자인 완료와 구현 완료의 경계, Figma 링크 정합성 |
| P1 | `09. 테스트/오류 관리`, `11. 최종 제출 체크리스트` | 실행 근거 없는 PASS/완료 표기 확인 |
| P1 | `문서 읽는 순서`, `Git 전략` | Git 정본 링크와 현재 원칙 점검 |
| P2 | `10. 회의록`, `회의록 목록`, `📅 일일 워크로그` | 중복·이관 후보와 기록 위치 점검 |
| P2 | `Zip Import - ASAK 키오스크 프로젝트.zip - Jul 13, 2026`, `Zip Import - notion.zip - Jul 13, 2026` | import 보관물의 정본 혼동 여부 확인 |

DB 설계의 "22개 테이블"·seed 관련 과거 서술과 현재 DevCopilot 26 tables/4 views의 차이는 확인됐다. 그러나 별도 DB 모델 database record는 검색 결과에서 확인되지 않아, DB 설계 문서의 현재 기준 안내만 병기하고 데이터 모델을 추정 생성·수정하지 않았다.

## 미지원·보류

| 항목 | 사유 | 후속 |
|---|---|---|
| `docs/DATA_CONTRACT_CART_SOLDOUT.md` | 현재 checkout의 `docs/`에서 파일을 찾지 못함 | Batch 2 전에 실제 경로 또는 병합 전 PR 제공 여부 확인; 추정 생성 금지 |
| 05-C/06-C/07-C의 개별 Frame 상태 | handoff Figma 파일의 Start Here/Source Inventory는 실제 이관 범위를 보였지만, 이번 조회에서 각 C page Frame을 직접 확정하지 못함 | 모든 새/정정 Screen record를 `PENDING_FIGMA_CONFIRMATION`으로 유지 |
