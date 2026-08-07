# ASAK WBS (통합본)

> **정본.** 기획·디자인·키오스크→관리자·백엔드·연동→QA·운영·발표까지 한 백로그로 관리합니다.
> 입구: [START_HERE](../START_HERE.md) · 코드 요약: [wbs-status-notes.md](wbs-status-notes.md)
> **팀:** 김나연 · 이하진 · 기준일 **2026-08-07**
>
> Hub 상태값: `TODO`(예정) · `IN_PROGRESS`(진행 중) · `IN_REVIEW`(검토 중) · `DONE`(완료) · `DELAYED`(지연)
> 제외(Hub 미등록): RTOS-SYS 추적성 · 미사용 번호 · RTOS 영수증 · EXT 외부연동

## 쓰는 법

1. 아래 **영역별 표**만 본다. 허브·Notion WBS 카드와 동일하다.
2. DONE은 evidence 칸을 채운다.

## 영역별 ID 구간

| 영역 | ID |
|---|---|
| 기획 | WBS-001~WBS-013 (13건) |
| 디자인 | WBS-014~WBS-022 (9건) |
| 키오스크 | WBS-023~WBS-038 (16건) |
| 관리자 | WBS-039~WBS-051 (13건) |
| 백엔드 | WBS-052~WBS-066 (15건) |
| 연동 | WBS-067~WBS-071 (5건) |
| QA | WBS-072~WBS-079 (8건) |
| 운영 | WBS-080 (1건) |
| 발표 | WBS-081~WBS-085 (5건) |

## 9주 로드맵

| Week | 날짜 | 목표 | 초점 WBS |
|------|------|------|----------|
| Week 1 | 7/2~7/4 | 기획·리드·ERD | WBS-001~013 |
| Week 2 | 7/7~7/11 | 디자인·골조 | WBS-014~022 |
| Week 3~4 | 7/14~7/25 | 키오스크 | WBS-023~038 |
| Week 5~6 | 7/28~8/8 | MVP·관리자·BE | WBS-039~066 |
| Week 7 | 8/11~8/13 | QA | WBS-072~079 |
| Week 8~9 | 8/25~9/2 | 연동·발표 | WBS-067~085 |

> 8/7 업무 우선: **키오스크 장바구니·주문→결제** → **관리자 주문** → 메뉴 → 품절 → 결제수단 → 매출.

## 백로그


### 기획 (13)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-001 | 쓸 기술과 역할을 정하기 | DEV-SYS-001 | — | 기획 | DEV | 하진, 나연 | DONE | 하 | 2026-07-03 | 2026-07-03 | 100 | 완료 조건: 팀 합의 | ASAK | 기획 / 스택 | 팀 합의 | [DEV-SYS-001] |
| WBS-002 | Git·브랜치·작업 티켓 규칙 정하기 | DEV-SYS-001 | Git 전략, 07 WBS, GitHub Projects | 협업 | DEV | 하진, 나연 | TODO | 중 | 2026-07-03 | 2026-07-04 | — | 브랜치/커밋/PR 규칙과 WBS 작업 단위가 팀 내 합의되면 완료 완료 조건: 브랜치·티켓 규칙 문서화 | ASAK | 기획 / Git | 브랜치·티켓 규칙 문서화 | [DEV-SYS-001] |
| WBS-003 | 메뉴·옵션 구조를 그리기 | LMIS-MENU-003, KSD-ARCH-001 | — | 기획 | LMIS | 하진, 나연 | TODO | 중 | 2026-07-03 | 2026-07-04 | — | 완료 조건: 옵션 트리 리뷰 | ASAK | 기획 / 메뉴모델 | 옵션 트리 리뷰 | [KSD-ARCH-001][LMIS-MENU-003] |
| WBS-004 | 화면 흐름과 기능을 문서에 적기 | FWD-UI-001, LMIS-ORDER-001 | — | 기획 | FWD | 나연, 하진 | TODO | 중 | 2026-07-03 | 2026-07-04 | — | 완료 조건: 흐름도 검토 | ASAK | 기획 / 화면정의 | 흐름도 검토 | [FWD-UI-001][LMIS-ORDER-001] |
| WBS-005 | DB 그림(ERD)과 API 목록 초안 쓰기 | KSD-ARCH-001, LMIS-ORDER-001 | — | 기획 | KSD | 하진 | TODO | 중 | 2026-07-03 | 2026-07-05 | — | 완료 조건: ERD·API 초안 리뷰 | ASAK / ASAK-back | 기획 / ERD·API | ERD·API 초안 리뷰 | [KSD-ARCH-001][LMIS-ORDER-001] |
| WBS-006 | 지금 프로젝트 상태를 스냅샷으로 남기기 | DEV-SYS-002, LMIS-MENU-003, KSD-ARCH-001 | — | 기획 | DEV | 하진 | DONE | 하 | 2026-07-03 | 2026-07-04 | 100 | 완료 조건: Snapshot 검토 완료 | ASAK | P1 Baseline / Snapshot | Snapshot 검토 완료 | Snapshot, DEV-SYS-002 |
| WBS-007 | 저장소 네 곳의 실제/목표 위치 정리하기 | FWD-UI-001, LMIS-ORDER-001 | — | 기획 | FWD | 하진 | DONE | 하 | 2026-07-03 | 2026-07-04 | 100 | 완료 조건: Map 검토 완료 | ASAK | P1 Baseline / Repository | Map 검토 완료 | current-status-baseline |
| WBS-008 | 키오스크 코드 정본 저장소 정하기 | DEV-SYS-001 | — | 기획 | DEV | 나연, 하진 | DELAYED | 상 | 2026-08-14 | 2026-08-20 | — | 완료 조건: 담당자가 마이그레이션 계획 확인 | ASAK-Kiosk | P1 Baseline / Kiosk remote | 담당자가 마이그레이션 계획 확인 | NEEDS_CONFIRMATION |
| WBS-009 | 저장소 옮기기 전 브랜치·미커밋 비교하기 | KSD-ARCH-001, LMIS-ORDER-001 | — | 기획 | KSD | 나연, 하진 | DELAYED | 상 | 2026-08-14 | 2026-08-20 | — | 완료 조건: 나연이 evidence 제공 | ASAK-Kiosk | P1 Baseline / Kiosk remote | 나연이 evidence 제공 | NEEDS_CONFIRMATION |
| WBS-010 | 요구사항·시나리오·화면 ID가 안 겹치는지 점검하기 | FWD-UI-001, FWD-UI-002, FWD-UI-003, FWD-UI-005 | — | 기획 | FWD | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-21 | 50 | 완료 조건: 발견 사항 연결 완료 | ASAK | P1 Baseline / Docs | 발견 사항 연결 완료 | traceability-matrix |
| WBS-011 | 이번 MVP와 나중에 할 일 나누기 | DEV-SYS-001 | — | 기획 | DEV | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-21 | 50 | 완료 조건: 범위 문서 검토 완료 | ASAK | P1 Baseline / Docs | 범위 문서 검토 완료 | future-scope |
| WBS-012 | 예전 API와 목표 API 차이표 만들기 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002 | — | 기획 | FWD | 하진, 나연 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-21 | 50 | 완료 조건: 백엔드 검토 요청 | ASAK | P1 Baseline / API | 백엔드 검토 요청 | rest-api-spec |
| WBS-013 | DB를 깨지 않고 점검하는 계획 세우기 | FWD-MENU-002, FWD-MENU-003, FWD-MENU-009, FWD-MENU-010, FWD-MENU-014 | — | 기획 | FWD | 하진, 나연 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-21 | 50 | 완료 조건: 백엔드 산출물 확보 | ASAK | P1 Baseline / DB | 백엔드 산출물 확보 | db-audit-plan · 7/28 중간점검 |

### 디자인 (9)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-014 | 화면 뼈대(와이어)와 공통 부품 구조 잡기 | FWD-UI-001, FWD-UI-002, FWD-UI-003, FWD-UI-005 | — | 디자인 | FWD | 하진, 나연 | TODO | 중 | 2026-07-03 | 2026-07-06 | — | 완료 조건: 와이어 리뷰 | Figma / ASAK | 디자인 / 와이어 | 와이어 리뷰 | [FWD-UI-001~005] |
| WBS-015 | 디자인 색·간격(토큰)과 모드 확인하기 | FWD-CART-001, FWD-CART-002, FWD-ORDER-001 | — | 디자인 | FWD | 하진 | DONE | 하 | 2026-07-07 | 2026-07-10 | 100 | 완료 조건: Design QA 기록 | Figma / ASAK | P2 Design / Foundation | Design QA 기록 | DESIGN_DONE |
| WBS-016 | 로딩/빈화면/오류 공통 부품 문서 확인하기 | FWD-PAY-001, FWD-PAY-002, DEV-PAY-001, FWD-ORDER-002 | — | 디자인 | FWD | 하진 | IN_PROGRESS | 상 | 2026-08-18 | 2026-08-25 | 50 | 완료 조건: Cover/visual QA 검토 | Figma / ASAK | P2 Design / Shared | Cover/visual QA 검토 | DESIGN_DONE |
| WBS-017 | 키오스크 디자인 부품을 화면에 맞춰 정리하기 | FWD-MENU-001, FWD-MENU-003, FWD-MENU-006 | SCR-003 | 디자인 | FWD | 하진, 나연 | IN_PROGRESS | 상 | 2026-08-18 | 2026-08-25 | 50 | 완료 조건: 매핑 승인 | Figma / ASAK | P2 Design / Kiosk | 매핑 승인 | SCR-003–008 |
| WBS-018 | 관리자 디자인 부품을 화면에 맞춰 정리하기 | FWD-ORDER-001, LMIS-ORDER-001, DEV-ORDER-001 | SCR-009 | 디자인 | FWD | 하진 | IN_PROGRESS | 상 | 2026-08-18 | 2026-08-25 | 50 | 완료 조건: 매핑 승인 | Figma / ASAK | P2 Design / Admin | 매핑 승인 | SCR-009–022 |
| WBS-019 | 키오스크 화면에 디자인 적용이 빠진 곳 적기 | LMIS-MENU-001, LMIS-MENU-002 | — | 디자인 | LMIS | 하진, 나연 | TODO | 중 | 2026-08-18 | 2026-08-25 | — | 완료 조건: Figma 담당 확인 | Figma / ASAK | P2 Design / Kiosk screens | Figma 담당 확인 | DESIGN_DONE only |
| WBS-020 | 관리자 디자인 작업이 서로 안 겹치게 경계 정하기 | DEV-SYS-001 | SCR-019 | 디자인 | DEV | 하진 | IN_PROGRESS | 상 | 2026-08-18 | 2026-08-25 | 50 | 완료 조건: active agent와 충돌 없음 | Figma / ASAK | P2 Design / Admin screens | active agent와 충돌 없음 | SCR-019–022 |
| WBS-021 | 고대비(읽기 쉬운 색) 점검 목록 만들기 | FWD-UI-001, DEV-SYS-001, FWD-MENU-001 | — | 디자인 | FWD | 하진, 나연 | TODO | 중 | 2026-08-18 | 2026-08-25 | — | 완료 조건: Design·구현 evidence | ASAK | P2 Design / Accessibility | Design·구현 evidence | FWD-UI-001 |
| WBS-022 | 프로토타입 교체는 보류한다고 기록하기 | FWD-PAY-002, FWD-SYS-001, DEV-SYS-001, DEV-PAY-001 | — | 디자인 | FWD | 하진 | TODO | 중 | 2026-08-18 | 2026-08-25 | — | 완료 조건: Figma 담당 evidence | Figma / ASAK | P2 Design / Prototype | Figma 담당 evidence | NEEDS_CONFIRMATION |

### 키오스크 (16)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-023 | 키오스크 화면 이동(라우트) 전체 연결 확인하기 | DEV-SYS-002 | SCR-001 | 프론트엔드 | DEV | 나연 | DONE | 하 | 2026-07-11 | 2026-07-17 | 100 | 완료 조건: Route 검토 완료 | ASAK-Kiosk | P3 Kiosk / Route | Route 검토 완료 | SCR-001,003,004 · Sprint Target **2026-07-20** |
| WBS-024 | 메뉴 목록 화면을 가짜 데이터와 연결하기 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, DEV-SYS-002, FWD-UI-001 | SCR 메뉴 선택, API-001, API-002 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-07-17 | 2026-08-07 | 50 | 카테고리 탭, 메뉴 카드, 품절/태그/가격 표시가 API 응답 기준으로 동작하면 완료 완료 조건: Contract 검토 | ASAK-Kiosk | P3 Kiosk / Menu | Contract 검토 | FWD-MENU-001 · mock adapter의 정본 필드 정렬(`totalAmount` 등) · Vite build 통과 **2026-07-28** · 실API/브라우저 QA 남음/008 |
| WBS-025 | 메뉴 상세·옵션·담기 화면 동작 확인하기 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, DEV-SYS-002 | SCR 메뉴 선택, API-001, API-002, SCR-004 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-08-17 | 2026-08-27 | 50 | 카테고리 탭, 메뉴 카드, 품절/태그/가격 표시가 API 응답 기준으로 동작하면 완료 완료 조건: Contract·담기 동작 | ASAK-Kiosk | P3 Kiosk / Detail | Contract·담기 동작 | SCR-004 · Target **2026-07-21**/008 |
| WBS-026 | 필수/선택 옵션과 담기 버튼 켜고 끄기 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, FWD-MENU-002, DEV-SYS-002 | SCR 메뉴 선택, API-001, API-002 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-08-27 | 2026-08-28 | 50 | 카테고리 탭, 메뉴 카드, 품절/태그/가격 표시가 API 응답 기준으로 동작하면 완료 완료 조건: Interaction evidence | ASAK-Kiosk | P3 Kiosk / Options | Interaction evidence | FWD-MENU-002 · Target **2026-07-21**/008 |
| WBS-027 | 알레르기 정보가 있을 때만 펼쳐 보이게 하기 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, FWD-MENU-004, FWD-SYS-001 | SCR 메뉴 선택, API-001, API-002 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 카테고리 탭, 메뉴 카드, 품절/태그/가격 표시가 API 응답 기준으로 동작하면 완료 완료 조건: UI·QA evidence | ASAK-Kiosk | P3 Kiosk / Allergy | UI·QA evidence | FWD-MENU-004 · Target **2026-07-21**/008 |
| WBS-028 | 같은 메뉴는 최대 9개까지만 담기 | FWD-UI-001, FWD-UI-005 | — | 프론트엔드 | FWD | 나연 | DONE | 하 | 2026-07-21 | 2026-08-07 | 100 | 완료 조건: Store 테스트 evidence | ASAK-Kiosk | P3 Kiosk / Store | Store 테스트 evidence | cart policy · Target **2026-07-20** |
| WBS-029 | 장바구니 전체는 최대 30개까지만 담기 | KSD-ARCH-001 | — | 프론트엔드 | KSD | 나연 | DONE | 하 | 2026-07-04 | 2026-07-07 | 100 | 완료 조건: Store 테스트 evidence | ASAK-Kiosk | P3 Kiosk / Store | Store 테스트 evidence | cart policy · Target **2026-07-20** |
| WBS-030 | 수량 초과하면 4초짜리 안내 띄우기 | FWD-MENU-001, LMIS-MENU-003 | — | 프론트엔드 | FWD | 나연 | TODO | 중 | 2026-08-18 | 2026-08-21 | — | 완료 조건: Interaction evidence | ASAK-Kiosk | P3 Kiosk / Store | Interaction evidence | cart policy · Target **2026-07-20** |
| WBS-031 | 장바구니에서 수량 바꾸기·삭제·비우기 | FWD-CART-001, FWD-CART-002, FWD-ORDER-001 | SCR 장바구니, API-005, SCR-005 | 프론트엔드 | FWD | 나연, 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 수량 변경/삭제, 옵션 요약이 가능하면 완료. 2026-07-04 수정: Day 10 범위에서 API-016(장바구니 검증) 제외 (8주 확장 API). Day 10은 API-005 응답 기준 클라이언트 검증만. 서버 검증(API-016)은 확장 WBS로 이관. 완료 조건: SCR-005 route 동작 | ASAK-Kiosk | P3 Kiosk / Cart | SCR-005 route 동작 | FWD-CART-002 · Target **2026-07-20** |
| WBS-032 | 결제 화면에서 결제 수단 고르기 | FWD-PAY-001, FWD-PAY-002, DEV-PAY-001, FWD-ORDER-002, FWD-MENU-004, FWD-MENU-015 | SCR-007 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: SCR-007 route 동작 | ASAK-Kiosk | P3 Kiosk / Payment | SCR-007 route 동작 | FWD-PAY-001 · payment adapter/API 용어 정렬 · Vite build 통과 **2026-07-28** · 실API/브라우저 QA 남음/027 |
| WBS-033 | 결제 실패해도 장바구니는 그대로 두기 | FWD-PAY-001, FWD-PAY-002, DEV-PAY-001, FWD-ORDER-002, DEV-PAY-002, DEV-SYS-001, KSD-PAY-001 | SCR-012 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Error-flow evidence | ASAK-Kiosk | P3 Kiosk / Payment | Error-flow evidence | SCR-012 · `usePayment` 실패 시 cart 유지 · 실연동 QA 남음/027 |
| WBS-034 | 주문 완료 화면에 번호·금액·대기 보여 주기 | FWD-SYS-001 | SCR-008 | 프론트엔드 | FWD | 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Completion evidence | ASAK-Kiosk | P3 Kiosk / Complete | Completion evidence | SCR-008 · Target **2026-07-21** |
| WBS-035 | 손 안 대면 타임아웃 경고·카운트다운 띄우기 | FWD-SYS-001, LMIS-MENU-004, LMIS-MENU-005, LMIS-MENU-006 | SCR-013 | 프론트엔드 | FWD | 나연 | TODO | 중 | 2026-08-18 | 2026-08-21 | — | 완료 조건: Timer QA evidence | ASAK-Kiosk | P3 Kiosk / Timeout | Timer QA evidence | SCR-013 · Target **2026-07-21**/028 |
| WBS-036 | 결제 중에는 타임아웃이 안 걸리게 하기 | FWD-SYS-001, LMIS-PAY-001 | SCR-013 | 프론트엔드 | FWD | 나연 | TODO | 중 | 2026-08-18 | 2026-08-21 | — | 완료 조건: Payment-state evidence | ASAK-Kiosk | P3 Kiosk / Timeout | Payment-state evidence | SCR-013 · Target **2026-07-21**/028 |
| WBS-037 | 키오스크 로딩·빈화면·오류 상태 만들기 | DEV-SYS-002, RTOS-SYS-001 | — | 프론트엔드 | DEV | 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: State QA evidence | ASAK-Kiosk | P3 Kiosk / States | State QA evidence | Target **2026-07-22** |
| WBS-038 | 키오스크 터치·화면 크기 QA 돌리기 | FWD-UI-001, FWD-UI-003 | — | 프론트엔드 | FWD | 나연, 하진 | TODO | 중 | 2026-08-18 | 2026-08-21 | — | 완료 조건: QA 실행 | ASAK-Kiosk | P3 Kiosk / QA | QA 실행 | 48px · Target **2026-07-22** |

### 관리자 (13)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-039 | 관리자 메뉴 경로를 화면 목록과 맞추기 | — | — | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: Registry 검토 | ASAK-Admin | P4 Admin / Route | Registry 검토 | Target **2026-07-20** |
| WBS-040 | 관리자 홈(대시보드)에 숫자·최근 주문 붙이기 | RTOS-DEVICE-001, RTOS-DEVICE-002, RTOS-DEVICE-003 | SCR-022 | 프론트엔드 | RTOS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: Route·state evidence | ASAK-Admin | P4 Admin / Dashboard | Route·state evidence | SCR-022 · `DashboardPanels`·`useDashboard` · 최근주문←`getDashboard().recentOrders` · AsyncState · 전주 대비 등 잔여 · Target **2026-07-20** · Ev **2026-07-23** |
| WBS-041 | 실시간 주문 현황 목록·상태 보여 주기 | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003 | SCR-009 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Route evidence | ASAK-Admin | P4 Admin / Live order | Route evidence | SCR-009 · `getLiveOrders`·완료/취소 ConfirmDialog · 페이징 상수 · Target **2026-07-20** · Ev **2026-07-23**/036 |
| WBS-042 | 주문 관리 목록과 상세 화면 연결하기 | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003, LMIS-ORDER-006 | SCR-010 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Screen evidence | ASAK-Admin | P4 Admin / Orders | Screen evidence | SCR-010 · `useOrdersQuery`·DetailPanel·환불/영수증 Confirm · 주문 상세 기본 단가/옵션 추가금/제외 재료/메뉴 합계 표시 보강 · 제외 재료 인라인 표시(`d2a900f`) · API 모듈 명명·연결 환경 정렬 · Vite build 통과 **2026-07-28** · 실API/브라우저 QA·필터 고도화 남음/036 |
| WBS-043 | 주문 상태 바꾸기(완료/취소) 버튼 만들기 | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003 | — | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: PATCH mock evidence | ASAK-Admin | P4 Admin / Orders | PATCH mock evidence | Live 완료/취소만 · 목록 PATCH/TTS 미완(의도적 표시만) · Target **2026-07-21**/036 |
| WBS-044 | 품절 체크하고 저장하기 | — | SCR-011 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-11 | 2026-08-14 | 50 | 완료 조건: UI state evidence | ASAK-Admin | P4 Admin / Sold-out | UI state evidence | SCR-011 · `useSoldOutDraft`·Confirm 저장 · 카드 2줄·카테고리 뱃지·menus 동기화 · **실패 fixture·menus.isSoldOut 저장 연동 TODO** · Target **2026-07-21** · Ev **2026-07-23** |
| WBS-045 | 메뉴 추가·수정 화면(가짜 저장) 만들기 | LMIS-MENU-004, LMIS-MENU-005, LMIS-MENU-006 | SCR-016 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-11 | 2026-08-14 | 50 | 완료 조건: UI evidence | ASAK-Admin | P4 Admin / Menu | UI evidence | SCR-016 · Page=조합(`useMenusQuery`+List/Detail/Edit) · IngredientModal · 카드 2줄·가격 nowrap · **저장/삭제 stub** · Target **2026-07-22** · Ev **2026-07-23** |
| WBS-046 | 결제 수단 켜고 끄고 저장하기 | LMIS-PAY-001 | SCR-018 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: UI evidence | ASAK-Admin | P4 Admin / Payments | UI evidence | SCR-018 · Figma 4종(card/kakao/naver/zero) · 토글·정렬·미리보기·Confirm · **실패 fixture · Kiosk 8종 정합 TODO** · Target **2026-07-21** · Ev **2026-07-23** |
| WBS-047 | 매출 요약과 기간(날짜) 필터 만들기 | — | SCR-019 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: UI evidence | ASAK-Admin | P4 Admin / Sales | UI evidence | SCR-019 · `useSalesQuery`+DatePicker range · AsyncState · Target **2026-07-21** · Ev **2026-07-23** |
| WBS-048 | 월별 매출 보고 달 바꾸기 | — | SCR-020 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: UI evidence | ASAK-Admin | P4 Admin / Sales | UI evidence | SCR-020 · mock+월 네비 · Target **2026-07-22** · Ev **2026-07-23** |
| WBS-049 | 일별 매출 보고 날짜 고르기 | — | SCR-021 | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: UI evidence | ASAK-Admin | P4 Admin / Sales | UI evidence | SCR-021 · DatePicker single·연간 · mock 외 달 empty · CSS span 누수 수정 · Target **2026-07-22** · Ev **2026-07-23** |
| WBS-050 | 관리자 로딩·빈화면·오류·메뉴 강조 맞추기 | — | — | 프론트엔드 | LMIS | 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: State QA evidence | ASAK-Admin | P4 Admin / States | State QA evidence | Shared `AdminAsyncState`·ConfirmDialog를 주문/품절/메뉴/결제/매출·대시보드에 적용 · **전 화면 QA·결제 스켈레톤 잔여** · Target **2026-07-22** · Ev **2026-07-23** |
| WBS-051 | 날짜 필터·합계·메뉴 강조 QA 하기 | — | — | 프론트엔드 | LMIS | 하진, 나연 | IN_PROGRESS | 상 | 2026-08-18 | 2026-08-21 | 50 | 완료 조건: QA 실행 | ASAK-Admin | P4 Admin / QA | QA 실행 | Sales·KEEP QA 1차 · 실행 evidence·P2 폴리시 잔여 · ASAK_Admin #4 · Target **2026-07-22** |

### 백엔드 (15)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-052 | 추천 드레싱을 옵션 데이터에 넣기 | FWD-MENU-004, FWD-MENU-015 | — | 백엔드 | FWD | 하진 | TODO | 중 | 2026-07-06 | 2026-07-09 | — | 완료 조건: 옵션 시드·API 확인 | ASAK-back | Backend / Option | 옵션 시드·API 확인 | [FWD-MENU-004][FWD-MENU-015] |
| WBS-053 | DB 제약조건(규칙)을 schema에 반영하기 | KSD-ARCH-001 | — | 백엔드 | KSD | 하진 | TODO | 중 | 2026-07-04 | 2026-07-07 | — | 완료 조건: 제약조건 리뷰 | ASAK-back | Backend / DB constraints | 제약조건 리뷰 | [KSD-ARCH-001] |
| WBS-054 | 연습용 메뉴·재료·옵션 샘플 데이터 넣기 | FWD-MENU-001, LMIS-MENU-003 | — | 백엔드 | FWD | 하진, 나연 | TODO | 중 | 2026-07-05 | 2026-07-09 | — | 완료 조건: 시드 데이터 검수 | ASAK-back | Backend / Seed | 시드 데이터 검수 | [FWD-MENU-001][LMIS-MENU-003] |
| WBS-055 | 장바구니가 주문 가능한지 검사하는 API 만들기 | FWD-CART-001 | — | 백엔드 | FWD | 하진 | TODO | 중 | 2026-07-08 | 2026-07-11 | — | 완료 조건: 검증 규칙 테스트 | ASAK-back | Backend / Cart | 검증 규칙 테스트 | [FWD-CART-001] |
| WBS-056 | 데이터를 어디에 둘지(저장 방식) 팀에서 정하기 | — | — | 백엔드 | LMIS | 하진, 나연 | TODO | 중 | 2026-08-14 | 2026-08-20 | — | 완료 조건: 팀 결정 | ASAK-back | P5 Backend / Baseline | 팀 결정 | DB audit |
| WBS-057 | DB 스키마·마이그레이션·시드 방식 고르기 | — | — | 백엔드 | LMIS | 하진, 나연 | TODO | 중 | 2026-08-14 | 2026-08-20 | — | 완료 조건: 검토 승인 | ASAK-back | P5 Backend / Schema | 검토 승인 | DB audit |
| WBS-058 | 메뉴 목록 API 만들기 | — | — | 백엔드 | LMIS | NEEDS_CONFIRMATION, 나연 | IN_PROGRESS | 상 | 2026-08-11 | 2026-08-14 | 50 | 완료 조건: API 테스트 evidence | ASAK-back | P5 Backend / Menu | API 테스트 evidence | GET menuList · AdminMenu DTO/Service/Mapper 골격 · 허브 계약 갱신 · Ev **2026-07-24** |
| WBS-059 | 메뉴 상세 API 만들기 | — | — | 백엔드 | LMIS | NEEDS_CONFIRMATION, 나연 | IN_PROGRESS | 상 | 2026-08-11 | 2026-08-14 | 50 | 완료 조건: API 테스트 evidence | ASAK-back | P5 Backend / Menu | API 테스트 evidence | GET menuDetail · MenuDetail/Ing/OptPolicy Response · vw_menu_* · Ev **2026-07-24** |
| WBS-060 | 주문 생성 API(검증·저장) 만들기 | — | — | 백엔드 | LMIS | NEEDS_CONFIRMATION, 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: API 테스트 evidence | ASAK-back | P5 Backend / Orders | API 테스트 evidence | POST orders · UserOrderController/Service/Mapper 골격 · Ev **2026-07-24** |
| WBS-061 | 결제 승인·실패 API 만들기 | — | API-006 | 백엔드 | LMIS | NEEDS_CONFIRMATION, 나연 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: API 테스트 evidence | ASAK-back | P5 Backend / Payments | API 테스트 evidence | POST payments · PaymentResult/UserPayMapper · API-006 계약 · Ev **2026-07-24** |
| WBS-062 | 품절 처리 API 만들기 | — | — | 백엔드 | LMIS | NEEDS_CONFIRMATION, 하진 | TODO | 중 | 2026-08-11 | 2026-08-14 | — | 완료 조건: API 테스트 evidence | ASAK-back | P5 Backend / Admin | API 테스트 evidence | PATCH soldOut |
| WBS-063 | 관리자용 주문 조회·상태 변경 API 만들기 | — | — | 백엔드 | LMIS | NEEDS_CONFIRMATION, 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: API 테스트 evidence | ASAK-back | P5 Backend / Admin | API 테스트 evidence | Admin orders · Controller/Service/Mapper와 `vw_order_live`·목록/상세 조회 SQL 보강 · legacy REQUEST 옵션은 `optionItems`에서 제외하고 제외 재료는 `item_exclusion`만 사용하도록 View 정의 정리(`e9543ce`) · `compileJava` 통과 **2026-07-28** · 실API/DB/Bruno 테스트 남음 |
| WBS-064 | 매출 합계를 내는 데이터 소스 만들고 맞추기 | — | API-017 | 백엔드 | LMIS | NEEDS_CONFIRMATION, 하진 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-18 | 50 | 완료 조건: 합계 검증 | ASAK-back | P5 Backend / Sales | 합계 검증 | sales views 정비 · API-017/018/019 예시·취소/환불 집계 규칙 유지 · `compileJava` 통과 **2026-07-28** · Sales API/실DB 합계 검증 남음 |
| WBS-065 | API 오류 응답·입력 검사를 통일하기 | — | — | 백엔드 | LMIS | — | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Contract tests | ASAK-back | P5 Backend / Common | Contract tests | ApiResponse + GlobalExceptionHandler · Bruno 주문 요청의 정본 용어 정렬 · `compileJava` 통과 **2026-07-28** · contract test·오류 응답 검증 남음 |
| WBS-066 | DB 설계도와 실제 테이블·관계가 맞는지 비교하기 | — | — | 백엔드 | LMIS | 하진, 나연 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-21 | 50 | 완료 조건: Audit report | ASAK / ASAK-back | P5 Backend / DB | Audit report | db-audit-plan · 7/28 중간점검 |

### 연동 (5)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-067 | 화면과 서버를 짧게 연결해 보기(스모크) | DEV-SYS-001, FWD-MENU-001 | — | 연동 | DEV | 하진, 나연 | TODO | 중 | 2026-07-10 | 2026-07-13 | — | 완료 조건: 스모크 통과 | ASAK-Kiosk / ASAK-back | Integration / Smoke | 스모크 통과 | [DEV-SYS-001][FWD-MENU-001] |
| WBS-068 | 금액·상태 필드 이름을 화면·서버가 같게 맞추기 | — | — | 연동 | DEV | 나연, 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Contract 검토 | ASAK-Kiosk / ASAK-Admin | P6 Integration / Contracts | Contract 검토 | totalAmount / APPROVED / EAT_IN · 8/7 Hub API 정렬 |
| WBS-069 | 키오스크를 실제 서버 API에 연결하기 | — | — | 연동 | DEV | 나연 | DELAYED | 상 | 2026-08-07 | 2026-08-11 | — | 완료 조건: Backend contract 존재 | ASAK-Kiosk | P6 Integration / Kiosk | Backend contract 존재 | Kiosk API |
| WBS-070 | 관리자를 실제 서버 API에 연결하기 | — | — | 연동 | DEV | 하진 | IN_PROGRESS | 상 | 2026-08-07 | 2026-08-11 | 50 | 완료 조건: Backend contract 존재 | ASAK-Admin | P6 Integration / Admin | Backend contract 존재 | Admin 주문 API 연동 진행 · 메뉴/품절/매출 잔여 |
| WBS-071 | 결제·주문·시간대 매출 합계가 맞는지 확인하기 | — | — | 연동 | DEV | 하진, 나연 | DELAYED | 상 | 2026-08-18 | 2026-08-21 | — | 완료 조건: Sales source 존재 | All | P6 Integration / Sales | Sales source 존재 | Sales QA |

### QA (8)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-072 | 키오스크 예외(결제·터치·타임아웃) 점검하기 | FWD-PAY-002, FWD-SYS-001, DEV-SYS-001, DEV-PAY-001 | — | 테스트 | FWD | 하진, 나연 | TODO | 중 | 2026-07-11 | 2026-07-16 | — | 완료 조건: 예외 시나리오 QA | ASAK-Kiosk | QA / Kiosk exception | 예외 시나리오 QA | — |
| WBS-073 | 시나리오대로 눌러 보고 결과·버그 적기 | DEV-SYS-002 | 03 시나리오, 09 테스트 시나리오, 버그 DB | 테스트 | DEV | 나연, 하진 | TODO | 상 | 2026-07-11 | 2026-07-17 | — | 핵심 시나리오별 실제 수행 결과와 버그가 기록되면 완료 완료 조건: 시나리오 결과 기록 | All | QA / Scenario | 시나리오 결과 기록 | [DEV-SYS-002] |
| WBS-074 | 느린 화면·헷갈리는 버튼 개선하기 | DEV-SYS-002, FWD-UI-001 | 성능/UX 개선 목록, 반영 내역 | 테스트 | DEV | 나연, 하진 | TODO | 중 | 2026-07-17 | 2026-08-07 | — | 주문 흐름에서 느린 화면, 헷갈리는 버튼, 반복 입력을 개선하면 완료 완료 조건: 개선 항목 기록 | ASAK-Kiosk / ASAK-Admin | QA / UX | 개선 항목 기록 | — |
| WBS-075 | 글자 크기·대비를 읽기 쉽게 맞추기 | FWD-UI-001, FWD-UI-005 | — | 테스트 | FWD | 나연, 하진 | TODO | 중 | 2026-07-21 | 2026-08-07 | — | 완료 조건: 대비·글자 적용 evidence | ASAK-Kiosk | QA / A11y UI | 대비·글자 적용 evidence | — |
| WBS-076 | 접근성 설정 화면 초안 만들기 | FWD-UI-001, FWD-UI-003 | — | 테스트 | FWD | 하진, 나연 | TODO | 중 | 2026-07-21 | 2026-08-07 | — | 완료 조건: 설정 UI 초안 | ASAK-Kiosk / ASAK-Admin | QA / A11y settings | 설정 UI 초안 | — |
| WBS-077 | 요구사항 테스트 돌리고 실제 결과 적기 | — | — | 테스트 | QA | 나연, 하진 | TODO | 중 | 2026-08-18 | 2026-08-21 | — | 완료 조건: 실행 evidence | All | P7 QA / Requirement | 실행 evidence | QA suite |
| WBS-078 | 고대비·키보드·터치 접근성 테스트하기 | — | — | 테스트 | QA | 나연, 하진 | TODO | 중 | 2026-08-18 | 2026-08-21 | — | 완료 조건: 실행 evidence | All | P7 QA / Accessibility | 실행 evidence | Accessibility QA |
| WBS-079 | 키오스크+관리자 전체를 다시 점검하기 | — | — | 테스트 | QA | 나연, 하진 | DELAYED | 상 | 2026-08-18 | 2026-08-21 | — | 완료 조건: 통합 앱 사용 가능 | All | P7 QA / Regression | 통합 앱 사용 가능 | Regression QA |

### 운영 (1)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-080 | 매주 데모하고 회고 적기 | DEV-SYS-001 | 주간 데모 기록, 회고 메모, 다음 주 액션 아이템 | 협업 | DEV | 나연, 하진 | TODO | 중 | 2026-07-10 | 2026-08-21 | — | 매주 구현된 화면/API를 시연하고 막힌 점과 다음 주 작업을 WBS에 반영하면 완료 완료 조건: 주간 기록 | ASAK | Ops / Demo cadence | 주간 기록 | [DEV-SYS-001] |

### 발표 (5)

| 작업 ID | 작업명 | 요구사항 | 관련 산출물 | 구분 | 단계 | 담당자 | 상태 | 우선순위 | 시작일 | 종료일 | 진척률 | 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-081 | 발표 자료·시연 순서 준비하기 | DEV-SYS-002 | — | 발표 | DEV | 나연, 하진 | TODO | 중 | 2026-08-17 | 2026-08-27 | — | 완료 조건: 자료·시나리오 검토 | ASAK | Release / Materials | 자료·시나리오 검토 | [PRESENT-001] |
| WBS-082 | 발표 전 최종 리허설하기 | DEV-SYS-002 | 최종 리허설 체크리스트, 발표 Q&A 메모 | 발표 | DEV | 나연, 하진 | TODO | 상 | 2026-08-27 | 2026-08-28 | — | 시연 흐름이 끊기지 않고 팀원별 발표/질의응답 대응이 가능하면 완료 완료 조건: 리허설 기록 | ASAK | Release / Rehearsal | 리허설 기록 | — |
| WBS-083 | 문서·인수인계·데모 자료 맞춰 두기 | — | — | 발표 | PRESENT | 하진, 나연 | IN_PROGRESS | 상 | 2026-08-14 | 2026-08-21 | 50 | 완료 조건: 사람 검토 | ASAK | P8 Docs / Handoff | 사람 검토 | DevCopilot sync |
| WBS-084 | 배포 전 빌드·환경·체크리스트 점검하기 | — | — | 발표 | PRESENT | 하진, 나연 | DELAYED | 상 | 2026-08-14 | 2026-08-28 | — | 완료 조건: 모든 저장소 점검 통과; 배포 환경·담당 확인; Release Candidate 검토 | All repositories | P8 Release / Readiness | 모든 저장소 점검 통과; 배포 환경·담당 확인; Release Candidate 검토 | Definition of Done: checklist 승인 및 RC evidence 첨부. Evidence: [Release Checklist](../product_bible/09_QA_Bible/docs/10-qa/07-demo-release/RELEASE_CHECKLIST.md); 환경/RC evidence 아직 없음. |
| WBS-085 | 발표 슬라이드·데모 대본·비상 계획 끝내기 | — | — | 발표 | PRESENT | 하진, 나연 | TODO | 중 | 2026-08-14 | 2026-08-28 | — | 완료 조건: 슬라이드, 스크립트, Demo 1–5 순서, fallback, 최종 리허설 기록이 팀 검토 완료 | All repositories | P8 Presentation / Demo | 슬라이드, 스크립트, Demo 1–5 순서, fallback, 최종 리허설 기록이 팀 검토 완료 | Definition of Done: 팀 검토 및 리허설 evidence 완료. Evidence: 2026-07-03 회의에서 발표/demo를 하진·나연이 공동 담당; [Demo Scenario](../product_bible/09_QA_Bible/docs/10-qa/07-demo-release/DEMO_SCENARIO.md). |

## 제외

| 항목 | 설명 | 비고 |
|---|---|---|
| 추적성·RTOS-SYS | RTOS-SYS-001 추적성 점검 | EXCLUDED |
| 미사용 번호 | 일정표 건너뜀 번호 | — |
| RTOS 영수증 | RTOS 영수증 모의 | MVP 외 |
| EXT-001/002 | 삭제요망 | Notion archive |

## 담당

- 키오스크 I/O·QA: 나연 / Admin·문서·Hub: 하진 / 통합: 공동
- 이탈 인원(민준·유진) → **나연·하진** 이관 표기
