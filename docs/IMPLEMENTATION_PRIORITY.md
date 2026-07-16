# Implementation Priority

> `DECIDED_PENDING_CODE_CHANGE`: canonical contracts are decided in [Canonical Contract Decisions](CANONICAL_CONTRACT_DECISIONS.md), but this phase authorizes documentation only. Slice 1 uses the decided kiosk paths; Slice 5 is implemented in ASAK-Admin.

> 원칙: 계층별 일괄 구현 대신 API–Backend–UI–검증을 하나씩 완료하는 Vertical Slice로 진행한다. 승인 전 이 문서는 계획일 뿐 소스 변경을 포함하지 않는다.

## 첫 번째 Vertical Slice 5개

| 순서 | Slice | 완료 기준 | 재사용/영향 파일 |
|---|---|---|---|
| 1 | 메뉴 목록 조회 | 카테고리와 주문 가능 메뉴를 canonical API 또는 정합 mock에서 표시 | Kiosk `MenuListPage`, `MenuCard`, `CategoryTabs`, `api/menu`, `api/category`, Backend Menu DTO/Service/Repository/Controller, schema/seed |
| 2 | 메뉴 상세·옵션 검증 | 옵션 최소/최대·품절·제외재료 검증 후 세션 항목 추가 | `MenuDetailPage`, `MenuDetailSummary`, `OptionGroup`, `OptionItem`, `orderSessionStore`, Menu detail API |
| 3 | 장바구니·주문 생성 | 수량/삭제/합계/재검증, `POST /api/kiosk/orders` 성공·실패 처리 | `CartPage`, `CartItem`, cart rules, session store, Order Entity/Service/Controller/Test |
| 4 | 결제·완료·복구 | 결제수단, idempotency, 승인/실패, waitingOrderCount, reset 정책 | `PaymentPage`, `PaymentMethodList`, `OrderCompletePage`, `ReceiptActions`, payment API, Payment domain, timeout/error UI |
| 5 | Admin Live Order 상태 변경 | 승인 주문 조회, PREPARING/COMPLETED 상태 전이, TTS trigger 후 성공 처리 | ASAK-Admin routes/pages, `OrderTable`, `OrderStatusBadge`, admin API, Order status endpoint/test |

## 이후 MVP 순서

6. Admin Dashboard aggregate (고객 수=승인 결제 건수, 평균 객단가=총매출/고객 수).
7. Sold-out draft/save 및 Kiosk 메뉴 재조회.
8. Sales summary: mock 허용, 단 KPI/차트/표 합계·비율 정합성 검증.
9. Admin menu management CRUD.
10. QA smoke, contract, timeout/accessibility, regression.

## 단계별 위험과 선행 확인

- Slice 1 전: API-01/02의 canonical path와 Menu response 필드를 확정해야 한다.
- Slice 3 전: DB schema와 가격·품절의 서버 최종 권한, 주문 idempotency 정책을 확정해야 한다.
- Slice 4 전: 결제 mock/실결제 범위, `waitingOrderCount` 산정 시점, 실패 후 보존 정책을 확정해야 한다.
- Slice 5 전: Admin route ownership과 상태 전이 권한을 확정해야 한다.

## FUTURE_SCOPE 제외 목록

SCR-023, SCR-024, 외부 TTS, WebSocket, 고급 차트·분석, 영양 자동 계산, 이미지 업로드, 주문 취소 action, Premium Figma 전면 적용은 MVP 완료 후 별도 승인으로 진행한다.
