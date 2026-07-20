# Document–Code Gap Report

> 기준일: **2026-07-20** · 코드 실측.  
> 문서 입구: [START_HERE](../START_HERE.md)  
> 「없다」와 「연결 안 됨」을 구분한다. UI가 있어도 mock/API 미연결이면 gap이다.  
> 정본 맵: [current-implementation-map-2026-07-16.md](../planning/current-implementation-map-2026-07-16.md)

## 핵심 충돌 (Canonical 결정됨 · 코드 미반영)

| ID | 문서(Canonical) | 실제 코드 | 분류 | 조치 |
|---|---|---|---|---|
| API-01 | `POST /api/kiosk/orders|payments` | `/api/orders`, `/api/payments` | CONFLICT | adapter/상수 정렬 (PENDING) |
| API-02 | `/api/kiosk/menuList`, `menuDetail/{id}` | `/api/menus…` | CONFLICT | 동일 |
| API-03 | `PATCH /api/admin/soldOut` | 문서·일부 stub vs kebab 경로 | CONFLICT | Admin 정렬 |
| API-04 | sales summary/monthly/daily | mock repository에 시나리오 있음, Page 미연결 | PARTIAL | Admin 바인딩 |
| SCR-01 | Dashboard `/` vs Live `/orders/live` | 코드: Live=`/`, Dashboard=`/dashboard` | CONFLICT | WBS2-033 |
| SCR-02 | `/soldOut`, `/paymentMethods` | `/sold-out`, `/payment-methods` | CONFLICT | 동일 |
| DATA-01 | `totalAmount`, `approvedAmount`… | store `totalPrice`, `amount`, `paidAt` | CONFLICT | adapter만 (이름 유지) |

---

## Gap 재분류 (2026-07-20)

### A. UI는 있음 · **연결**이 필요 (이전 문서가 “누락”으로 잘못 적음)

| 영역 | 있음 | 없는 것 |
|---|---|---|
| Kiosk Cart/Payment/Complete/Error/Timeout | 라우트 + 페이지 UI | 결제 flow, 타이머, complete 데이터 |
| Kiosk Menu/Detail/Cart | mock 동작 | adapter 계층, Canonical path |
| Admin 전 화면 | Figma 정적 UI + 라우트 | `adminMockRepository` 바인딩, 상태 변경, 필터 |
| Admin mock | JSON + repository | Page/Hook 사용처 0 |

### B. 진짜 누락 / BLOCKED

| 영역 | 내용 |
|---|---|
| Backend | health 외 business API, Entity, migration |
| Kiosk↔Admin 품절 동기화 | 없음 |
| QA 자동 실행 | Backend context test 외 Product Bible suite 미실행 |
| SCR-023/024 | Future Scope (의도적) |

### C. 반드시 보존

1. Kiosk `priceCalculation.js`, `quantityLimits.js`  
2. `orderSessionStore` + cart/order 호환 export  
3. Axios envelope unwrap  
4. Admin `AdminSidebar` / Layout / Figma 정적 페이지  
5. `kiosk.json`, `asak-admin-data.json` mock 자산  

---

## 지금 할 일 / 하지 말 일

| 할 일 | 하지 말 일 |
|---|---|
| Kiosk 결제·toast·timeout 연결 | UI 통째 재이식 |
| Admin mock → Page 바인딩 | Canonical 미확정 대규모 rename |
| gap을 “연결 작업”으로 추적 | “화면 파일이 없다”고 재작성 |
| Backend P5 슬라이스 | 문서만으로 DONE 주장 |

---

## FUTURE_SCOPE

SCR-023 영수증, SCR-024 멤버십, 외부 AI TTS, WebSocket, 고급 차트, 이미지 업로드.

## 문서 정리

| 문서 | 조치 |
|---|---|
| `CURRENT_IMPLEMENTATION_MAP` | **2026-07-20 재작성** |
| `IMPLEMENTATION_PLAN` (3저장소) | **2026-07-20 재작성** |
| `STRUCTURE_GUIDE` | Kiosk 갱신 · Admin 신규 |
| `docs/_archive/**`, `docs/design/_archive/**` | ARCHIVE 유지 |
| Product Bible | TARGET 정책 유지 (구현 증거 아님) |

## Human decision overlay

`API-01~03`, `SCR-01~02` = `DECIDED_PENDING_CODE_CHANGE`  
`DATA-01` = `DECIDED_NOT_IMPLEMENTED` (adapter)  
상세: [canonical-contract-decisions-2026-07-16.md](../governance/canonical-contract-decisions-2026-07-16.md)
