# Admin TODO 문서 동기화 기록

> 날짜: 2026-08-21
> 범위: `docs/planning/admin-todo-2026-08-05.md`

## 확인 근거

- `ASAK-Admin` 원격 main의 `soldOutApi.js`, `useSoldOutDraft.js`, `salesApi.js`, `useSalesQuery.js`, `adminApi.js`, `useDashboard.js`
- `ASAK-backend` 원격 main의 `AdminSoldOutController`, `AdminSoldOutService`, `AdminSoldOutMapper.xml`, `AdminSalesController`
- Product Bible `INVENTORY_AND_SOLD_OUT_BIBLE.md`, `SALES_BIBLE.md`
- Screen Bible `SCR-011`, `SCR-018`~`SCR-022`

## 반영 내용

- 기존 문서의 품절 007~010, 매출 015~022, 대시보드 023~025를 미구현 표기에서 코드 구현·빌드 확인 상태로 고쳤다.
- 품절 API의 request/response 구조, 메뉴·재료만 보이는 UI 결정, 옵션 항목의 API 포함 상태를 기록했다.
- 각 TODO에 실제 위치, 다음 1단위, 권장 인라인 TODO 문구를 넣었다.
- 결제수단, 인증, 환불/영수증은 미구현 또는 정책 선행 상태로 유지했다.

## 미검증/결정 필요

- 배포 DB View와 실제 Bruno/브라우저 E2E는 재실행하지 않았다.
- 품절 파생 상태(effectiveSoldOut), 옵션 탭 노출, payment method/화면 URL 정규화는 팀 결정이 필요하다.
- 완료된 품절 코드에 남은 과거 TODO-007~010 주석은 소스 수정 승인이 없으므로 변경하지 않았다.
