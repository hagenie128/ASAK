# Admin 구현 TODO 정리표 (TODO-001 ~ TODO-076)

> 인라인 주석 태그: `TODO-NNN`  
> 순서대로 구현하면 된다. 파일 상단에 모아 두지 않고, **해당 코드 위치**에만 달아 두었다.  
> 검색: `TODO-00` / `TODO-0` / `TODO-` 
> 진행 갱신: 2026-08-05 (코드 실측 기준)

## 진행 요약

| 상태 | 번호 |
|---|---|
| 완료 | **001~007**, **009**, **011**, **014** |
| 부분 | **008**, **012**, **013** |
| 미착수 | **010**, **013a~013d**, **015~076** |

다음 권장: TTS 명세 마무리 **013a~013d** (중복 방지·Queue·Mute·localStorage) → **012** Empty/Error UI → **008·010**

| # | 상태 | 위치 | 할 일 |
|---|---|---|---|
| **001** | ✅ 완료 | `AdminOrderController.changeOrderStatus` | `response == null` → `ORDER_NOT_FOUND` |
| **002** | ✅ 완료 | 동상 | 거절 시 `INVALID_ORDER_STATUS_TRANSITION` 사용 |
| **003** | ✅ 완료 | `AdminOrderService.changeOrderStatus` | `RECEIVED→PREPARING→COMPLETED`만 허용 |
| **004** | ✅ 완료 | 동상 | `findOrderStatusId` 코드테이블 조회 |
| **005** | ✅ 완료 | `AdminOrderMapper.xml` | `expectedStatusId` optimistic update |
| **006** | ✅ 완료 | `AdminOrderController` | `INVALID_TRANSITION` vs `ORDER_STATUS_CONFLICT` |
| **007** | ✅ 완료 | `AdminOrderController.cancelOrder` | `response == null` → `ORDER_NOT_FOUND` |
| **008** | 🟡 부분 | `AdminOrderService.cancelOrder` | 검사 일부만. APPROVED 시 환불 연동 미완(현재 0 반환) |
| **009** | ✅ 완료 | `AdminOrderMapper` + XML | `cancelOrder`로 이름 수정됨 (주석만 잔여 가능) |
| **010** | ⬜ 미착수 | `AdminOrderMapper.xml` cancel | `status_id=43` → 코드테이블/상수 |
| **011** | ✅ 완료 | `LiveOrderPreview.jsx` catch | `err.status`/`err.code` 로 409 분기(`ORDER_STATUS_CONFLICT`/`INVALID_ORDER_STATUS_TRANSITION`) + 그 외 toast 처리됨 |
| **012** | 🟡 부분 | `useOrdersQuery.js` | empty/error state 존재. 보드 UI(`LiveOrderPreview`)의 Empty vs Error 구분·필터 정합 확인 필요 |
| **013** | 🟡 부분 | `LiveOrderPreview.jsx` + `utils/ttsMessages.js` | `speak`/`isTtsSupported`/`createOrderCompletedMessage` **구현됨**(커밋 `5cbf861`). 성공 후 호출·실패 격리 OK. 아래 명세 항목 013a~013d 미구현 |
| **013a** | ⬜ 미착수 | `utils/ttsMessages.js` 또는 tts 서비스 | **중복 방지**: 동일 orderNo 10초 이내 재발화 금지(recent order map) |
| **013b** | ⬜ 미착수 | 동상 | **Queue**: 연속 완료 시 cancel 없이 SpeechSynthesis 큐 순서 발화 |
| **013c** | ⬜ 미착수 | `components/admin/TtsControl.jsx` | **Mute 토글**: enabled/muted/speaking/unsupported 상태 · 상단 "주문 호출 [켜짐/꺼짐]" |
| **013d** | ⬜ 미착수 | tts 설정 저장 | **localStorage 설정**: enabled/rate/pitch/volume/lang 저장·복원 |
| **014** | ✅ 완료 | `LiveOrderPreview.jsx` | `asak_live_fixture`·`console.log` 제거, 에러 UI 일반 문구로 정리됨 |
| **015** | ⬜ 미착수 | `SoldOutPatchRequest.java` | DTO 필드 |
| **016** | ⬜ 미착수 | `AdminSoldOutMapper` + XML | 카탈로그 SELECT |
| **017** | ⬜ 미착수 | 동상 | `is_sold_out` UPDATE |
| **018** | ⬜ 미착수 | `AdminSoldOutService.java` | 조회·변경·롤백 |
| **019** | ⬜ 미착수 | `AdminSoldOutController.java` | GET/PATCH |
| **020** | ⬜ 미착수 | `soldOutApi.js` | `listSoldOutCatalog` |
| **021** | ⬜ 미착수 | `soldOutApi.js` | `patchSoldOut` |
| **022** | ⬜ 미착수 | `useSoldOutDraft.js` | mock → API |
| **023** | ⬜ 미착수 | `LiveOrderPreview.jsx` 보드 | 가로 스크롤 |
| **024** | ⬜ 미착수 | `PatchPaymentMethodRequest.java` | DTO 필드 |
| **025** | ⬜ 미착수 | `AdminPaymentMethodMapper` + XML | SELECT |
| **026** | ⬜ 미착수 | 동상 | UPDATE |
| **027** | ⬜ 미착수 | `AdminPaymentMethodService.java` | 서비스 |
| **028** | ⬜ 미착수 | `AdminPaymentMethodController.java` | GET/PATCH |
| **029** | ⬜ 미착수 | `paymentMethodsApi.js` | list |
| **030** | ⬜ 미착수 | `paymentMethodsApi.js` | patch |
| **031** | ⬜ 미착수 | `usePaymentMethodDraft.js` | mock → API |
| **032** | ⬜ 미착수 | `CreateMenuRequest.java` | DTO 필드 |
| **033** | ⬜ 미착수 | `AdminMenuMapper.java` | insertMenu |
| **034** | ⬜ 미착수 | `AdminMenuService.createMenu` | INSERT 트랜잭션 |
| **035** | ⬜ 미착수 | `AdminMenuController` | POST |
| **036** | ⬜ 미착수 | `AdminMenuMapper.java` | updateMenu |
| **037** | ⬜ 미착수 | `AdminMenuService` | updateMenu |
| **038** | ⬜ 미착수 | `AdminMenuController` | PATCH |
| **039** | ⬜ 미착수 | `AdminMenuMapper.java` | deleteMenu |
| **040** | ⬜ 미착수 | `AdminMenuService` | deleteMenu |
| **041** | ⬜ 미착수 | `AdminMenuController` | DELETE |
| **042** | ⬜ 미착수 | Mapper + Controller | ingredients |
| **043** | ⬜ 미착수 | `menusApi.js` | createMenu |
| **044** | ⬜ 미착수 | `menusApi.js` | updateMenu |
| **045** | ⬜ 미착수 | `menusApi.js` | deleteMenu |
| **046** | ⬜ 미착수 | `useMenusQuery.js` | mock → API |
| **047** | ⬜ 미착수 | `MenuManagePage.jsx` | save → API |
| **048** | ⬜ 미착수 | `MenuManagePage.jsx` | delete → API |
| **049** | ⬜ 미착수 | `AdminStatsController` | sales/summary |
| **050** | ⬜ 미착수 | 동상 | sales/monthly |
| **051** | ⬜ 미착수 | 동상 | sales/daily |
| **052** | ⬜ 미착수 | Stats Service/Mapper | 집계 |
| **053** | ⬜ 미착수 | `salesApi.js` | getSummary |
| **054** | ⬜ 미착수 | `salesApi.js` | getMonthly |
| **055** | ⬜ 미착수 | `salesApi.js` | getDaily |
| **056** | ⬜ 미착수 | `useSalesQuery.js` | mock → API |
| **057** | ⬜ 미착수 | `AdminStatsController` | dashboard |
| **058** | ⬜ 미착수 | `adminApi.js` | getDashboard |
| **059** | ⬜ 미착수 | `useDashboard.js` | mock → API |
| **060** | ⬜ 미착수 | `AdminAuthController` | POST /login |
| **061** | ⬜ 미착수 | `JwtTokenProvider.java` | JWT |
| **062** | ⬜ 미착수 | `JwtAuthenticationFilter.java` | 필터 |
| **063** | ⬜ 미착수 | `SecurityConfig.java` | authorize |
| **064** | ⬜ 미착수 | `adminApi.js` | login |
| **065** | ⬜ 미착수 | `adminSession.js` | token |
| **066** | ⬜ 미착수 | `apiClient.js` | Bearer + 401 |
| **067** | ⬜ 미착수 | `LoginPage.jsx` | 실로그인 |
| **068** | ⬜ 미착수 | `useAdminAuth.js` | 401 가드 |
| **069** | ⬜ 미착수 | `AdminApp.jsx` | Canonical 경로 |
| **070** | ⬜ 미착수 | `apiClient.js` | 403 매핑 |
| **071** | ⬜ Future | `AdminOrderController` | refund |
| **072** | ⬜ Future | `AdminOrderMapper.xml` | payments 환불 |
| **073** | ⬜ Future | `ordersApi.js` | refundOrder |
| **074** | ⬜ Future | `ordersApi.js` | printReceipt |
| **075** | ⬜ Future | `OrderManagementPreview.jsx` | 환불 UI |
| **076** | ⬜ Future | `OrderManagementPreview.jsx` | 영수증 UI |

## 구간 요약

| 구간 | 주제 | 진행 |
|---|---|---|
| 001–010 | 주문 상태·취소 BE | 001~007·009 완료 · 008 부분 · 010 미착수 |
| 011–014, 023 | Live FE | 011·014 완료 · 012·013 부분 · 013a~013d(TTS 명세)·023 미착수 |
| 015–022 | 품절 | 미착수 |
| 024–031 | 결제수단 | 미착수 |
| 032–048 | 메뉴 CRUD | 미착수 |
| 049–059 | 매출·대시보드 | 미착수 |
| 060–068 | 로그인·JWT | 미착수 |
| 069–070 | 라우트·공통 에러 | 미착수 |
| 071–076 | Future 환불·영수증 | 미착수 |

## 사용법

1. `TODO-001`부터 구현한다.
2. 완료한 항목은 인라인 주석을 지우고, 이 표 상태를 ✅로 갱신한다.
3. 이 표와 코드 주석이 어긋나면 **코드 인라인을 정본**으로 맞춘다.
