# WBS / 요구사항 / QA — DONE·PASS 점검 (2026-08-07)

- 기준: 코드 실측 + Hub 원격 상태 + 실행 증거 유무
- 원칙: **코드 있음 ≠ DONE** · **TC 미실행 ≠ PASS**
- 원격 쓰기: 이 문서 작성 시점 **미수행** (아래 권고만)

## 1. Hub 현황 요약

| 범위 | 원격 집계 | 비고 |
|---|---|---|
| WBS 전체 | EXCLUDED 98 / IN_PROGRESS 35 / TODO 19 / DONE 11 / BLOCKED 7 | `wbs_rate` 6.5%는 EXCLUDED 포함 → 지표 무시 |
| WBS2 계열 | DONE **6** · IN_PROGRESS 35 · TODO 18 · BLOCKED 7 (+ EXCLUDED 보존) | 로컬 `wbs-v2`와 DONE 집합 일치 |
| 요구사항 | DONE **0** · IN_PROGRESS 다수 · TODO · EXCLUDED | `req_rate` 0% |
| QA | 16건 **전부 TODO** · PASS **0** | `qa_rate` 0% |

## 2. 이미 DONE인 WBS — 유지해도 되는가?

| task | 제목 요약 | 판정 | 근거 |
|---|---|---|---|
| WBS2-001 | MCP baseline | **DONE 유지** | 기획/문서 산출 |
| WBS2-002 | 저장소 역할/목표 | **DONE 유지** | 산출 완료 |
| WBS2-009 | Foundation 산출 | **DONE 유지** | 산출 완료 |
| WBS2-017 | 키오스크 라우트·흐름 | **DONE 유지** | 라우트 연결 evidence |
| WBS2-022 | 메뉴 수량 max 9 | **DONE 유지** | quantityLimits |
| WBS2-023 | 장바구니 max 30 | **DONE 유지** | quantityLimits |
| 레거시 WBS-001~024 일부 DONE | ERD/스키마 등 | **보존** | SUPERSEDED/일반 DONE 혼재 — 일괄 변경 금지 |

→ **잘못 올라간 DONE은 없음.** 추가로 DONE 올릴 항목도 **없음** (통합 테스트 전).

## 3. DONE으로 올리면 안 되는 후보 (코드는 있으나 미검증)

| ID | Hub 상태 | 코드 | 왜 DONE 불가 |
|---|---|---|---|
| WBS2-035 Live | IN_PROGRESS | `GET .../orders/live` 구현 | 브라우저·실DB 통합 미검증 |
| WBS2-036 주문 목록/상세 | IN_PROGRESS | Admin GET 구현 · FE 연동 | 동일 |
| WBS2-053 주문 조회/상태 | IN_PROGRESS | PATCH status/cancel 구현 | Bruno/HTTP E2E 미기록 |
| WBS2-048/049 메뉴 GET | IN_PROGRESS | AdminMenu GET(+POST create) | CRUD·FE E2E 미완 |
| LMIS-ORDER-001~003 | IN_PROGRESS | 위와 동일 | 요구사항 DONE = 업무 완료 주장 → 금지 |
| LMIS-MENU-004 | IN_PROGRESS | GET·POST 있음, PATCH/DELETE TODO | 등록/수정/삭제 전체 미완 |
| DEV-ORDER-001 | IN_PROGRESS | `POST /orders` 매핑 있음 | 실DB 저장·응답 검증 전 |
| DEV-PAY-001 | IN_PROGRESS | `UserPayController` **빈 껍데기** | 오히려 **TODO 하향** 검토 |

## 4. 상태만 조정 권고 (DONE/PASS 아님)

| 대상 | 현재 | 권고 | 근거 |
|---|---|---|---|
| DEV-CART-001 | TODO | → **IN_PROGRESS** | `POST /api/kiosk/cart/validate` 구현됨 |
| DEV-ORDER-002 | TODO | → **IN_PROGRESS** | `PATCH .../cancel` 구현됨 · 통합 미검증 |
| WBS2-037 (상태 UI·TTS) | TODO | → **IN_PROGRESS** (선택) | Live 상태변경/취소 코드 있음 · TTS는 여전히 stub |
| DEV-PAY-001 | IN_PROGRESS | → **TODO** (선택) | Pay Controller 미구현 |
| LMIS-MENU-001 품절 | IN_PROGRESS | 유지 또는 TODO | `AdminSoldOutController` 빈 클래스 |
| LMIS-PAY-001 | IN_PROGRESS | 유지 또는 TODO | PaymentMethod Controller 스텁 |
| LMIS-DASH-001 | TODO | **TODO 유지** | Stats 스텁 |
| QA TC-001~016 | TODO | **전부 TODO 유지** | 실행 로그/증거 없음 → **PASS 0건** |
| TC-005/015/016 FUTURE | TODO | PASS 금지 · EXCLUDED/보류 유지 | 범위 밖 |

## 5. QA PASS 가능 여부

| TC | PASS? | 조건 |
|---|---|---|
| TC-001 orderType | **불가(지금)** | Kiosk→API-005 실요청·DB 확인 후 |
| TC-014 주문목록·상태 | **불가(지금)** | Admin Live/목록/PATCH 수동+로그 후 |
| TC-010/011 메뉴 | **불가** | CRUD·품절 연동 후 |
| TC-012/013 결제·매출 | **불가** | BE 스텁 |
| 나머지 | **불가** | 미실행 |

## 6. 권고 액션

1. **즉시 하지 않음:** 어떤 WBS/요구도 DONE, 어떤 QA도 PASS
2. **승인 시 안전 갱신만:** DEV-CART-001·DEV-ORDER-002를 TODO→IN_PROGRESS (및 선택적 WBS2-037 / DEV-PAY-001 조정)
3. **PASS/DONE 승격:** 스모크 실행 체크리스트에 날짜·담당·결과 URL/로그를 남긴 뒤에만 개별 ID로 처리

## 7. 결론

- Hub의 **기존 DONE 6건(WBS2)은 타당**하다.
- **새로 DONE·PASS 할 항목은 0건**이다.
- 진행 중으로 보이는 주문/메뉴 조회는 **IN_PROGRESS가 정답**이며, 선생님 요청의 통합 테스트·실DB 검증이 끝나기 전 DONE 승격은 허위 완료가 된다.

## 8. Hub 반영 (승인 후)

| 대상 | 변경 | 결과 |
|---|---|---|
| DEV-CART-001 | TODO → IN_PROGRESS | 반영 |
| DEV-ORDER-002 | TODO → IN_PROGRESS | 반영 |
| WBS DONE / QA PASS | 변경 없음 | — |
