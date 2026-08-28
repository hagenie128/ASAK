# ASAK WBS·완료 기능·QA 대조 — 2026-08-28

- 동기화 일시: 2026-08-28
- 범위: `wbs.md`, QA 문서, Hub WBS/TC, Notion 07·09 페이지
- 제외: 소스코드, Git commit/push, 실제 TC 실행

## 기준 커밋

| 저장소 | HEAD |
|---|---|
| ASAK-back | `494baef` |
| ASAK-Admin | `4f0c9cd` |
| ASAK (문서) | `46740ea` (+ 로컬 수정) |

## main 코드 — 키오스크 연결됨 · 검증 대기

| API | FE | BE | 검증 |
|---|---|---|---|
| API-001 categories | `MenuListPage` | `UserMenuController` | 미완 |
| API-002 menuList | `MenuListPage` | 동상 | 미완 |
| API-003 menuDetail | `MenuDetailPage` | 동상 | 미완 |
| API-004 cart/validate | `CartPage` | `UserOrderController` | 미완 |
| API-005 orders | `PaymentProcessingPage` | 동상 | 미완 |
| API-006 payments | `PaymentProcessingPage` (`approvePayment`) | `UserPayController` | 미완 · 토스 SDK |
| API-014 payment-methods | `PaymentPage` | `UserPayController` | 미완 |

**Hub 정정:** API-006 설명이 “approvePayment 미호출”로 **구식**이었음 → 2026-08-28 갱신.

## Hub WBS — 키오스크 조정

| WBS | 조정 전 | 조정 후 | 사유 |
|---|---|---|---|
| WBS-069 | DONE | IN_PROGRESS | API FE 연결됐으나 E2E 없음 |
| WBS-033 | DONE | IN_PROGRESS | cart 유지 코드 있으나 E2E 없음 |

## main 코드 — Admin 연결됨 · 검증 대기

| 기능 | Backend | Frontend | 검증 |
|---|---|---|---|
| 로그인(매장번호 0001) | `AdminAuthController` | `LoginPage`, `adminSession` | 미완 |
| 결제수단 | `AdminPaymentMethodController` | `paymentMethodsApi`, `usePaymentMethodDraft` | 미완 (ORDER BY 갭) |
| 주문 목록/상세/상태/취소 | `AdminOrderController` | `ordersApi`, `OrderManagePage` | 미완 |
| Live 주문 | `GET .../orders/live` | `LiveOrderBoard` | 미완 |
| 환불 | `PATCH .../refund`, `GET .../refund-reasons` | `ordersApi`, `refundReasonsApi`, 사유 UI | 미완 |
| 품절 | `AdminSoldOutController` | `soldOutApi`, `useSoldOutDraft` | 미완 |
| 매출/대시보드 | `AdminSalesController` | `salesApi`, `useDashboard` | 미완 |
| 영수증 재출력 | `AdminDeviceEventController` | `ordersApi.printReceipt` | 미완 |

**원칙:** 위 항목은 **코드 연결 완료**이지 **기능 완료(DONE)** 가 아니다.

## Hub WBS — 조정한 불일치

| WBS | 조정 전 (Hub) | 조정 후 | 사유 |
|---|---|---|---|
| WBS-042 | DONE | IN_PROGRESS | 환불·사유 API main 구현, E2E 미검증 |
| WBS-062 | TODO | IN_PROGRESS | `AdminSoldOutController` 존재 |
| WBS-071 | DELAYED | IN_PROGRESS | 환불 포함 통합 QA 착수 대기 |

**유지 (주의):** WBS-043·041 등 Hub DONE — 기본 주문 UI는 연결됐으나 통합 TC 미실행. WBS-069 Hub DONE vs 로컬 DELAYED — 키오스크 API client 존재, E2E는 별도.

## QA

| 항목 | 상태 |
|---|---|
| Hub TC-001~016 | 전건 `TODO`, 실행 기록 없음 |
| TC-017 (신규) | Hub·로컬·Pack 추가 — 환불·사유 통합 검증 |
| Pack `ADMIN_TEST_SUITE` | ORD-REF-001~005 추가 |

## 갱신한 로컬 문서

| 문서 | 변경 |
|---|---|
| `docs/wiki/wbs.md` | 2026-08-28 정정 블록, WBS-042/044/046/062/070/071 행 갱신 |
| `docs/wiki/wbs-status-notes.md` | 이번 주 Hub 권고·키워드 갱신 |
| `docs/wiki/qa-test-cases.md` | TC-017 추가, Status CURRENT |
| `docs/product_bible/09_QA_Bible/ADMIN_TEST_SUITE.md` | ORD-REF-001~005 |

## Notion

| 페이지 | 변경 |
|---|---|
| 07. WBS / 개발 진행 현황 | `## 2026-08-28` 섹션 prepend |
| 09. 테스트/오류 관리 | `## 2026-08-28` 섹션 prepend |

## 남은 불일치

| 상태 | 내용 |
|---|---|
| Hub vs 로컬 | WBS-069 (DONE vs DELAYED), 다수 Hub DONE vs 로컬 IN_REVIEW |
| `미검증` | TC 전건, seed SQL, Bruno, E2E |
| `구현 불일치` | 환불 Mapper 파라미터명, `providerPaymentKey` SELECT |
