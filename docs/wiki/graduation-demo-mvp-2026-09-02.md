# 종강 시연 MVP 실행본

> 시연일: **2026-09-02**  
> 목표: "고객 주문 흐름과 관리자 운영 흐름이 같은 주문·결제·매출 데이터로 연결된다"를 안정적으로 보여 준다.  
> 기준: [WBS](wbs.md) · [QA 테스트 케이스](qa-test-cases.md) · [종강 전 전체 체크리스트](project-completion-checklist-2026-09-01.md)  
> **문서 갱신: 2026-09-01** — Admin 실DB QA 근거와 미검증(Kiosk E2E) 구간을 분리했다.  
> **2026-09-02:** [문서·코드 대조](admin-doc-code-verification-2026-09-02.md) · [Admin QA](qa-execution-report-2026-09-02.md) · [Kiosk QA](qa-kiosk-execution-report-2026-09-02.md) · [TC 실행표](demo-tc-execution-sheet-2026-09-02.md) · [발표 대본](graduation-presentation-script-2026-09-02.md)

## 0. 검증 상태 요약 (말할 때 구분)

| 구간 | 상태 | 근거 |
| --- | --- | --- |
| Admin 로그인·주문 상태 전이·승인 결제 취소 차단 | **실DB 확인** | TC-014, WBS-042 (2026-09-01) |
| 가상 CARD 환불·매출 합계 | **실DB 확인** | TC-017·013 (2026-09-01), `951,100 - 60,800 = 890,300` (2026-08-28) |
| Admin 재료 품절 PATCH 저장/복구 | **실DB 확인** | WBS-044/062 (2026-09-01) |
| Admin 결제수단 CARD active 토글 | **실DB 확인** | TC-012 (2026-09-01). Kiosk 노출은 **미검증** |
| Admin 매출 화면(기간 버튼·달 전체 차트) | **코드 반영** | 2026-09-02 `fillDailyRows`·오늘/주/월. **화면 E2E 미기록** |
| Kiosk 주문·결제 API (TC-001~002) | **API 확인** | 2026-09-02 EAT_IN/TAKE_OUT·CARD APPROVED · **UI 클릭 미검증** |
| Kiosk 품절 (MENU/OPTION) | **API 확인** | TC-003 MENU·OPTION **PASS** · INGREDIENT ing125 **FAIL** |
| Admin 결제수단 → Kiosk | **FAIL** | Admin CARD OFF 후에도 Kiosk에 CARD 노출 |
| RTOS 콘솔 영수증 | **미검증** | 코드·절차만 정리, 리허설 성공 전 Plan B |

## 1. 내일 시연에서 완료로 보는 MVP 범위

### 반드시 시연할 흐름

1. **고객 주문**: 주문 유형 선택 → 메뉴/옵션 → 장바구니 → 결제 → 주문 완료 *(시연에서 최초 E2E 확인)*
2. **관리자 운영**: 매장 번호 `0001` 로그인 → 대시보드/주문 목록 → 주문 상태 변경 *(Admin 실DB 확인됨)*
3. **품절 관리**: Admin **MENU** 품절 저장/복구 → Kiosk `isSoldOut` 반영 *(API 확인)* · ing125 재료는 영향 0 → **MENU 단위** 시연 권장
4. **결제수단 관리**: Admin CARD active 토글 *(Admin API 확인)* → Kiosk 반영은 **FAIL** → Admin만 시연 또는 설명
5. **매출 확인**: 환불 전후 일별·요약 API 또는 화면에서 `gross - canceled = total` 대조 *(API 실DB 확인, 화면 E2E 미검증)*

### RTOS·환불 시연 후보 (시간 있을 때)

- **환불**: 가상 CARD 환불은 실DB에서 이미 확인했다. 시연 중에는 **사전 준비 주문 1건**만 사용하고, 성공 뒤 `CANCELED`/`REFUNDED`·매출 캡처를 보여 준다. 실패 시 [§7 Plan B](#7-시연-실패-plan-b) 2번.
- **RTOS/영수증**: `~/ASAK-RTOS` POSIX polling 시연. **리허설 성공 전에는 본편에서 빼고** Q&A 또는 Plan B로 처리한다.

### 시연 범위에서 제외하고 명시할 기능

- 실제 PG 결제·실제 PG 취소/환불
- 실물 영수증 프린터·보드 펌웨어
- 회원·쿠폰·QR 적립
- WebSocket 실시간 갱신
- 접근성 설정 화면 전체 구현

> 제외 기능을 성공한 기능처럼 말하지 않는다. 환불은 **가상 카드**, RTOS는 **POSIX 콘솔 시연**이며 실물 장비 연동 증거는 없다.

## 2. 오늘 우선순위: 시연 가능 상태 만들기

### P0 — 시연 자체를 막는 항목

- [ ] **Kiosk E2E 1회**: dev 실행 → 주문 유형 → 메뉴 → 결제 완료까지 끊김 없이 진행 (실패 시 Plan B 녹화 준비).
- [x] Kiosk `npm run build` 통과 *(2026-09-01 확인. 과거 `uuid` lockfile 이슈는 해소됨)*.
- [ ] Admin `npm run build`와 backend `gradlew.bat test --no-daemon -x spotlessApply` 통과.
- [ ] Kiosk, Admin, backend를 같은 API/DB로 기동하고 브라우저 콘솔 fatal error가 없는지 확인한다.
- [ ] [§4 고정 데이터](#4-시연-직전-고정-데이터와-안전-규칙)를 종이·채팅에 적어 두고, 시연 직전 API 응답으로 ID를 재확인한다.
- [ ] 시연 API 응답 확인: 로그인, 메뉴, 주문, 결제, 주문 목록, 품절, 결제수단, 매출.

### P1 — 시연 신뢰도를 높이는 항목

- [ ] WSL `~/ASAK-RTOS`에서 `make`·polling 리허설 (성공 시에만 발표 본편에 포함).
- [ ] Loading/Empty/Error 문구, 메뉴명·가격·주문번호 대조.
- [ ] 새로고침 뒤 Admin 로그인·품절·결제수단 상태 유지 확인.
- [ ] 백업 스크린샷·1~2분 화면 녹화 준비.

## 2-1. RTOS 기본 시연 준비 (P1 · 리허설 성공 시만)

### 확인된 구현 경계

- RTOS 저장소: `~/ASAK-RTOS`
- 실행 방식: FreeRTOS `GCC_POSIX` 시뮬레이터
- 흐름: `POST receipt-print` → Spring 메모리 이벤트 큐 → `GET /api/rtos/device-events/pending` → RTOS 콘솔 영수증 → `PATCH /api/rtos/device-events/{eventId}/finish`
- payload: `주문번호|메뉴 요약|금액`의 pipe 문자열
- **DB:** `receipt`·`device_event` 테이블 **없음**. 영수증 본문은 주문·결제 테이블, 출력 이벤트는 JVM 메모리만 사용.
- 한계: 실물 프린터/ARM/QEMU/영구 DB 큐는 범위 밖. Spring 재시작 시 메모리 큐 초기화.

### 실행 순서

1. [ ] Windows backend 기동, `Tomcat started on port 8080` 확인.
2. [ ] WSL `cd ~/ASAK-RTOS && make`.
3. [ ] `HOST_IP=$(ip route show default | awk '/default/ {print $3}')`
4. [ ] `make run SERVER_URL=http://$HOST_IP:8080`
5. [ ] receipt 이벤트 생성 → 콘솔 출력·`COMPLETED` 캡처.

> WSL에서 `localhost:8080`은 Windows Spring이 아니다. Spring 프로세스를 유지한 채 이벤트를 처리한다.

## 2-2. Backend 기동 — 8080 포트 충돌

`bootRun` 또는 `.\scripts\boot-run.ps1` 실행 시:

```text
Web server failed to start. Port 8080 was already in use.
```

이전 `java.exe`가 8080을 점유한 상태다.

```powershell
netstat -ano | findstr :8080
tasklist /FI "PID eq <PID>"
taskkill /PID <PID> /F
cd C:\ASAK-workspace\ASAK-back
.\scripts\boot-run.ps1
```

예방: **Ctrl+C**로 정상 종료. 포트 변경 시 `application.properties`의 `server.port`와 Kiosk·Admin·RTOS URL을 함께 맞춘다.

## 2-3. 품절 카탈로그 범위 (시연 시 혼동 방지)

`vw_soldout_catalog` 재료 탭은 **약 20건**만 노출한다 (2026-09-01 운영 DB 기준).

| 포함 | 제외 |
| --- | --- |
| CORE / BASE / 제거 불가 DEFAULT | 빼기 가능 DEFAULT, opt_item 전용 ing |
| 이름이 정상인 재료 | `*미포함*`, `N배`, `xN` 변형명 |
| OPTION_ITEM(탭 숨김) | REQUEST 그룹(`group_type_id=25`), INGREDIENT와 중복 ing |

시연 품절은 **§4 고정 CORE 재료(닭가슴살 125)** 를 쓴다.

## 3. MVP QA 실행표

`PASS`는 실행 근거·캡처 후에만 체크. `BLOCKED`는 Plan B를 적는다.

| 우선 | TC/WBS | 사전조건 | 실행 | 기대 결과 | 결과 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | Build | 의존성 설치 | Kiosk/Admin build, backend test | 성공 | [ ] | Kiosk build ✓ |
| P0 | TC-001 | Kiosk 실행 | EAT_IN/TAKE_OUT 선택 | orderType 유지 | [ ] | **Kiosk 미검증** |
| P0 | TC-002/031~034 | 메뉴 데이터 | 주문→결제→완료 | 주문번호·금액 표시 | [ ] | **Kiosk 미검증** |
| P0 | TC-004 | 실패 재현 방법 확보 | 결제 실패 후 장바구니 | 안내·장바구니 유지 | [ ] | 재현 절차 미정 |
| P0 | TC-009 | Admin | `0001`/오류 번호 | 승인/오류 구분 | [ ] | Admin 확인됨 |
| P0 | TC-014 | 변경 가능 주문 | PREPARING·COMPLETED | 즉시 재조회 | [ ] | Admin 확인됨 |
| P0 | WBS-043 | READY 주문 | 관리자 취소 | **409 차단** | [ ] | 로컬 코드 확인 · 시연에서 시도 안 함 |
| P0 | TC-003/006 | CORE 재료(§4) | Admin 품절 ON→Kiosk→OFF | 표시·차단·복구 | [ ] | Admin PATCH ✓ / Kiosk **미검증** |
| P0 | TC-012 | CARD 1건 | active 토글·재조회 | Admin·Kiosk 일치 | [ ] | Admin PATCH ✓ / Kiosk **미검증** |
| P0 | TC-013/071 | 환불 데이터 | daily/summary | gross-canceled=total | [ ] | API ✓ / 화면 **미검증** |
| P1 | RTOS | make·polling | receipt→finish | COMPLETED | [ ] | 리허설 없으면 BLOCKED |
| P1 | TC-017 | 승인 CARD | 환불·재환불·OTHER | 200·409·400 | [ ] | 환불 1건 ✓ / 409·400 **미검증** |
| P1 | TC-007 | 장바구니 | 무입력 대기 | 홈·장바구니 초기화 | [ ] | |
| P1 | WBS-050 | 주요 화면 | Loading/Error·새로고침 | 치명 오류 없음 | [ ] | |

## 4. 시연 직전 고정 데이터와 안전 규칙

### 고정 데이터 (시연 직전 GET으로 재확인)

| 항목 | 권장 값 | 용도 |
| --- | --- | --- |
| Admin 로그인 | `storeNumber` = `0001` | SCR-015 |
| 품절 재료 | `ing_id` **125** · **닭가슴살** (CORE) | Admin 품절 탭. 빼기 가능 재료는 목록에 없음 |
| 품절 연동 확인 메뉴 | `menu_id` **1978** · **탄단지 샐러디** | 닭가슴살 포함 메뉴 (Kiosk에서 확인용) |
| 결제수단 | `code` = **CARD** | `GET /api/admin/paymentMethods`로 `methodId` 확인 |
| 매출 비교일 | **2026-08-28** | 검증된 합계 `951,100 - 60,800 = 890,300` |
| 환불 대상 주문 | 시연 당일 **신규 테스트 주문 1건** | 기환불 주문 재사용 금지. 실패 시 9/1 캡처로 대체 |

### 안전 규칙

- [ ] 위 표를 종이에 적고, 시연 시작 전 ID를 API로 다시 확인한다.
- [ ] 품절·결제수단은 시연 종료 전 **원상복구**한다.
- [ ] 환불은 **테스트 주문 1건**에만 실행한다.
- [ ] 매출 전/후 스크린샷을 저장한다.
- [ ] 운영 DB 임의 삭제·초기화 금지.
- [ ] 8080·API base URL·DB 연결을 시작 전 확인한다.

## 5. 발표 5분 구성과 대본 키워드

> **말할 대본 전문:** [graduation-presentation-script-2026-09-02.md](graduation-presentation-script-2026-09-02.md)  
> **시연 당일 TC 체크:** [demo-tc-execution-sheet-2026-09-02.md](demo-tc-execution-sheet-2026-09-02.md)

| 시간 | 화면/행동 | 말할 핵심 |
| --- | --- | --- |
| 0:00~0:30 | 문제·MVP 범위 | 고객 주문과 관리자 운영을 하나의 데이터 흐름으로 연결 |
| 0:30~1:50 | **Kiosk 주문** | 주문 유형·옵션·결제 완료 *(핵심, 리허설 필수)* |
| 1:50~2:50 | **Admin 주문** | `0001` 로그인, 상태 전이, Order/Payment 상태 분리 |
| 2:50~3:40 | **품절·결제수단** | Admin 저장은 확인됨. Kiosk 반영은 시연에서 보여 주거나 녹화로 대체 |
| 3:40~4:20 | **환불·매출** | 가상 CARD 환불, `CANCELED`/`REFUNDED`, 순매출 대조 |
| 4:20~5:00 | 한계·확장 | 실PG·실물 프린터·WebSocket·회원은 범위 밖. RTOS는 리허설 성공 시 Q&A |

> RTOS는 **본편 20초 슬롯을 쓰지 않는다**. 리허설 통과 후 질문이 있을 때만 데모한다.

### 각자 설명할 코드 포인트

- **Kiosk**: 주문·장바구니·결제 상태 흐름, 결제 실패 시 장바구니 유지.
- **Admin·backend**: 주문/결제 상태 분리, 품절 PATCH·`vw_soldout_catalog` 범위, 환불·매출 집계.
- **공동**: [§0 검증 상태](#0-검증-상태-요약-말할-때-구분)대로 **확인됨 / 시연 목표**를 구분해 말한다.

## 6. 예상 질문과 30초 답변

| 질문 | 답변 |
| --- | --- |
| 실제 결제인가요? | CARD는 시연용 가상 승인·취소입니다. 주문/결제 상태와 매출 집계는 실DB로 검증했고, 실 PG는 후속 범위입니다. |
| 환불하면 무엇이 바뀌나요? | 주문 `CANCELED`, 결제 `REFUNDED`, 매출은 취소액을 제외한 순매출로 집계됩니다. |
| 품절이 고객 화면에도 적용되나요? | Admin 재료 품절 저장/복구는 실DB에서 확인했습니다. Kiosk SOLD OUT 표시는 시연 목표이며, CORE 재료 기준으로 보여 줍니다. |
| 품절 목록에 재료가 적은 이유는? | 품절 탭은 주문 가능 여부에 영향 있는 재료(CORE/BASE/제거불가)만 보여 줍니다. 빼기 가능 옵션·미사용 재료는 제외합니다. |
| 실시간 갱신은 WebSocket인가요? | API 재조회 기반이며 WebSocket은 확장 범위입니다. |
| RTOS/프린터도 구현했나요? | POSIX 시뮬레이터로 이벤트 polling·콘솔 영수증 흐름까지 구현했습니다. 실물 프린터·영구 큐는 후속 범위입니다. |

## 7. 시연 실패 Plan B

1. **Kiosk 실패**: 즉시 수정하지 말고 빌드 로그·**사전 녹화**·API 응답으로 고객 흐름 설명.
2. **환불 실패**: 재시도하지 말고 9/1 `CANCELED`/`REFUNDED`·매출 캡처 제시.
3. **품절/결제수단 불일치**: §4 원복 후 **Admin 주문·환불·매출** 데모 우선. Kiosk 연동은 “시연 목표”로 명시.
4. **RTOS 실패**: 주문·Admin 계속. 이벤트 API 흐름만 설명.
5. **8080 충돌**: [§2-2](#2-2-backend-기동--8080-포트-충돌) 후 재기동. 불가 시 백업 영상.

## 8. 종강 직전 최종 체크

- [ ] P0 QA가 PASS이거나 BLOCKED+Plan B 승인.
- [ ] **Kiosk E2E 또는 Plan B 녹화** 준비 완료.
- [ ] 시연 순서 리허설 1회 이상.
- [ ] §4 고정 데이터·원복 절차·백업 자료 준비.
- [ ] WBS/QA와 MVP 범위 모순 없음.
- [ ] 발표에서 **확인됨 vs 시연 목표** 구분.

## 시연 결과 기록

| 항목 | PASS / FAIL / BLOCKED | 근거(캡처·응답·로그) | 담당 | 비고 |
| --- | --- | --- | --- | --- |
| Kiosk 주문 |  |  |  |  |
| Admin 주문 운영 |  |  |  |  |
| 품절 (Admin) |  |  |  |  |
| 품절 (Kiosk 연동) |  |  |  |  |
| 결제수단 (Admin) |  |  |  |  |
| 결제수단 (Kiosk) |  |  |  |  |
| 환불·매출 합계 |  |  |  |  |
| RTOS 콘솔 영수증 |  |  |  |  |
| 발표 리허설 |  |  |  |  |
