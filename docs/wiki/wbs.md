# ASAK WBS (?�합�?

> **?�본.** 기획?�디?�인?�키?�스?�→관리자?�백?�드?�연?�→QA?�운??발표�???백로그로 관리합?�다.
> ?�구: [START_HERE](../START_HERE.md) · 코드 ?�약: [wbs-status-notes.md](wbs-status-notes.md)
> **?�:** 김?�연 · ?�하�?· 기�???**2026-08-07**
>
> Hub ?�태�? `TODO`(?�정) · `IN_PROGRESS`(진행 �? · `IN_REVIEW`(검??�? · `DONE`(?�료) · `DELAYED`(지??
> ?�외(Hub 미등�?: RTOS-SYS 추적??· 미사??번호 · RTOS ?�수�?· EXT ??��?�망

## ?�는 �?

1. ?�래 **?�역�???*�?본다. ?�드??Notion WBS 카드?� ?�일?�다.
2. DONE?� evidence ?�을 ?�만.

## ?�역�?ID 구간

| ?�역 | ID |
|---|---|
| 기획 | WBS-001~WBS-013 (13�? |
| ?�자??| WBS-014~WBS-022 (9�? |
| ?�오?�크 | WBS-023~WBS-038 (16�? |
| 관리자 | WBS-039~WBS-051 (13�? |
| 백엔??| WBS-052~WBS-066 (15�? |
| ?�동 | WBS-067~WBS-071 (5�? |
| QA | WBS-072~WBS-079 (8�? |
| ?�영 | WBS-080 (1�? |
| 발표 | WBS-081~WBS-085 (5�? |

## 9�?로드�?

| Week | ?�짜 | 목표 | 초점 WBS |
|------|------|------|----------|
| Week 1 | 7/2~7/4 | 기획·?�드·ERD | WBS-001~013 |
| Week 2 | 7/7~7/11 | ?�자?�·골�?| WBS-014~022 |
| Week 3~4 | 7/14~7/25 | ?�오?�크 | WBS-023~038 |
| Week 5~6 | 7/28~8/8 | MVP·관리자·BE | WBS-039~066 |
| Week 7 | 8/11~8/13 | QA | WBS-072~079 |
| Week 8~9 | 8/25~9/2 | ?�동·발표 | WBS-067~085 |

> 8/7 ?�무 ?�선: **?�오?�크 ?�바구니?�주문→결제** ??**관리자 주문** ??메뉴 ???�절 ??결제?�단 ??매출.

## 백로�?

### 기획 (13)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-001 | 기술 ?�택·??�� ?�의 | DEV-SYS-001 | ??| 기획 | DEV | ?�진, ?�연 | DONE | ??| 2026-07-03 | 2026-07-03 | 100 | ?�료 조건: ?� ?�의 | ASAK | 기획 / ?�택 | ?� ?�의 | [DEV-SYS-001] |
| WBS-002 | Git·브랜치·티�?규칙 ?�의 | DEV-SYS-001 | Git ?�략, 07 WBS, GitHub Projects | ?�업 | DEV | ?�진, ?�연 | TODO | �?| 2026-07-03 | 2026-07-04 | ??| 브랜�?커밋/PR 규칙�?WBS ?�업 ?�위가 ?� ???�의?�면 ?�료 ?�료 조건: 브랜치·티�?규칙 문서??| ASAK | 기획 / Git | 브랜치·티�?규칙 문서??| [DEV-SYS-001] |
| WBS-003 | 메뉴·?�션 구조 ?�계 | LMIS-MENU-003, KSD-ARCH-001 | ??| 기획 | LMIS | ?�진, ?�연 | TODO | �?| 2026-07-03 | 2026-07-04 | ??| ?�료 조건: ?�션 ?�리 리뷰 | ASAK | 기획 / 메뉴모델 | ?�션 ?�리 리뷰 | [KSD-ARCH-001][LMIS-MENU-003] |
| WBS-004 | ?�면 ?�름·기능 문서??| FWD-UI-001, LMIS-ORDER-001 | ??| 기획 | FWD | ?�연, ?�진 | TODO | �?| 2026-07-03 | 2026-07-04 | ??| ?�료 조건: ?�름??검??| ASAK | 기획 / ?�면?�의 | ?�름??검??| [FWD-UI-001][LMIS-ORDER-001] |
| WBS-005 | ERD·API 목록 초안 ?�성 | KSD-ARCH-001, LMIS-ORDER-001 | ??| 기획 | KSD | ?�진 | TODO | �?| 2026-07-03 | 2026-07-05 | ??| ?�료 조건: ERD·API 초안 리뷰 | ASAK / ASAK-back | 기획 / ERD·API | ERD·API 초안 리뷰 | [KSD-ARCH-001][LMIS-ORDER-001] |
| WBS-006 | ?�로?�트 ?�태 ?�냅???�성 | DEV-SYS-002, LMIS-MENU-003, KSD-ARCH-001 | ??| 기획 | DEV | ?�진 | DONE | ??| 2026-07-03 | 2026-07-04 | 100 | ?�료 조건: Snapshot 검???�료 | ASAK | P1 Baseline / Snapshot | Snapshot 검???�료 | Snapshot, DEV-SYS-002 |
| WBS-007 | ?�?�소 ?�제·목표 ?�치 ?�리 | FWD-UI-001, LMIS-ORDER-001 | ??| 기획 | FWD | ?�진 | DONE | ??| 2026-07-03 | 2026-07-04 | 100 | ?�료 조건: Map 검???�료 | ASAK | P1 Baseline / Repository | Map 검???�료 | current-status-baseline |
| WBS-008 | ?�오?�크 ?�본 ?�?�소 ?�정 | DEV-SYS-001 | ??| 기획 | DEV | ?�연, ?�진 | DELAYED | ??| 2026-08-14 | 2026-08-20 | ??| ?�료 조건: ?�당?��? 마이그레?�션 계획 ?�인 | ASAK-Kiosk | P1 Baseline / Kiosk remote | ?�당?��? 마이그레?�션 계획 ?�인 | NEEDS_CONFIRMATION |
| WBS-009 | ?�전 ??브랜치·�?커밋 비교 | KSD-ARCH-001, LMIS-ORDER-001 | ??| 기획 | KSD | ?�연, ?�진 | DELAYED | ??| 2026-08-14 | 2026-08-20 | ??| ?�료 조건: ?�연??evidence ?�공 | ASAK-Kiosk | P1 Baseline / Kiosk remote | ?�연??evidence ?�공 | NEEDS_CONFIRMATION |
| WBS-010 | ?�구?�항·?�나리오·?�면 ID 추적???��? | FWD-UI-001, FWD-UI-002, FWD-UI-003, FWD-UI-005 | ??| 기획 | FWD | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-21 | 50 | ?�료 조건: 발견 ?�항 ?�결 ?�료 | ASAK | P1 Baseline / Docs | 발견 ?�항 ?�결 ?�료 | traceability-matrix |
| WBS-011 | MVP·?�속 범위 분리 | DEV-SYS-001 | ??| 기획 | DEV | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-21 | 50 | ?�료 조건: 범위 문서 검???�료 | ASAK | P1 Baseline / Docs | 범위 문서 검???�료 | future-scope |
| WBS-012 | 기존·목표 API 차이???�성 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002 | ??| 기획 | FWD | ?�진, ?�연 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-21 | 50 | ?�료 조건: 백엔??검???�청 | ASAK | P1 Baseline / API | 백엔??검???�청 | rest-api-spec |
| WBS-013 | DB 무중???��? 계획 ?�립 | FWD-MENU-002, FWD-MENU-003, FWD-MENU-009, FWD-MENU-010, FWD??| ??| 기획 | FWD | ?�진, ?�연 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-21 | 50 | ?�료 조건: 백엔???�출�??�보 | ASAK | P1 Baseline / DB | 백엔???�출�??�보 | db-audit-plan · 7/28 중간?��? |

### ?�자??(9)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-014 | ?�?�어·공통 컴포?�트 구조 ?�계 | FWD-UI-001, FWD-UI-002, FWD-UI-003, FWD-UI-005 | ??| ?�자??| FWD | ?�진, ?�연 | TODO | �?| 2026-07-03 | 2026-07-06 | ??| ?�료 조건: ?�?�어 리뷰 | Figma / ASAK | ?�자??/ ?�?�어 | ?�?�어 리뷰 | [FWD-UI-001~005] |
| WBS-015 | ?�자???�큰·모드 ?�인 | FWD-CART-001, FWD-CART-002, FWD-ORDER-001 | ??| ?�자??| FWD | ?�진 | DONE | ??| 2026-07-07 | 2026-07-10 | 100 | ?�료 조건: Design QA 기록 | Figma / ASAK | P2 Design / Foundation | Design QA 기록 | DESIGN_DONE |
| WBS-016 | 로딩·빈화면·오�?공통 컴포?�트 문서 ?�인 | FWD-PAY-001, FWD-PAY-002, DEV-PAY-001, FWD-ORDER-002 | ??| ?�자??| FWD | ?�진 | IN_PROGRESS | ??| 2026-08-18 | 2026-08-25 | 50 | ?�료 조건: Cover/visual QA 검??| Figma / ASAK | P2 Design / Shared | Cover/visual QA 검??| DESIGN_DONE |
| WBS-017 | ?�오?�크 ?�자??컴포?�트·?�면 매핑 | FWD-MENU-001, FWD-MENU-003, FWD-MENU-006 | SCR-003 | ?�자??| FWD | ?�진, ?�연 | IN_PROGRESS | ??| 2026-08-18 | 2026-08-25 | 50 | ?�료 조건: 매핑 ?�인 | Figma / ASAK | P2 Design / Kiosk | 매핑 ?�인 | SCR-003??08 |
| WBS-018 | 관리자 ?�자??컴포?�트·?�면 매핑 | FWD-ORDER-001, LMIS-ORDER-001, DEV-ORDER-001 | SCR-009 | ?�자??| FWD | ?�진 | IN_PROGRESS | ??| 2026-08-18 | 2026-08-25 | 50 | ?�료 조건: 매핑 ?�인 | Figma / ASAK | P2 Design / Admin | 매핑 ?�인 | SCR-009??22 |
| WBS-019 | ?�오?�크 ?�자???�용 ?��? | LMIS-MENU-001, LMIS-MENU-002 | ??| ?�자??| LMIS | ?�진, ?�연 | TODO | �?| 2026-08-18 | 2026-08-25 | ??| ?�료 조건: Figma ?�당 ?�인 | Figma / ASAK | P2 Design / Kiosk screens | Figma ?�당 ?�인 | DESIGN_DONE only |
| WBS-020 | 관리자 ?�자???�업 경계 ?�의 | DEV-SYS-001 | SCR-019 | ?�자??| DEV | ?�진 | IN_PROGRESS | ??| 2026-08-18 | 2026-08-25 | 50 | ?�료 조건: active agent?� 충돌 ?�음 | Figma / ASAK | P2 Design / Admin screens | active agent?� 충돌 ?�음 | SCR-019??22 |
| WBS-021 | 고�?�??��? 목록 ?�성 | FWD-UI-001, DEV-SYS-001, FWD-MENU-001 | ??| ?�자??| FWD | ?�진, ?�연 | TODO | �?| 2026-08-18 | 2026-08-25 | ??| ?�료 조건: Design·구현 evidence | ASAK | P2 Design / Accessibility | Design·구현 evidence | FWD-UI-001 |
| WBS-022 | ?�로?��???교체 보류 기록 | FWD-PAY-002, FWD-SYS-001, DEV-SYS-001, DEV-PAY-001 | ??| ?�자??| FWD | ?�진 | TODO | �?| 2026-08-18 | 2026-08-25 | ??| ?�료 조건: Figma ?�당 evidence | Figma / ASAK | P2 Design / Prototype | Figma ?�당 evidence | NEEDS_CONFIRMATION |

### ?�오?�크 (16)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-023 | ?�오?�크 ?�우???�결 ?�인 | DEV-SYS-002 | SCR-001 | ?�론?�엔??| DEV | ?�연 | DONE | ??| 2026-07-11 | 2026-07-17 | 100 | ?�료 조건: Route 검???�료 | ASAK-Kiosk | P3 Kiosk / Route | Route 검???�료 | SCR-001,003,004 · Sprint Target **2026-07-20** |
| WBS-024 | 메뉴 목록 ?�면 mock ?�동 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, DEV-SYS-002, FWD??| SCR 메뉴 ?�택, API-001, API-002 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-07-17 | 2026-08-07 | 50 | 카테고리 ?? 메뉴 카드, ?�절/?�그/가�??�시가 API ?�답 기�??�로 ?�작?�면 ?�료 ?�료 조건: Contract 검??| ASAK-Kiosk | P3 Kiosk / Menu | Contract 검??| FWD-MENU-001 · mock adapter???�본 ?�드 ?�렬(`totalAmount` ?? · Vite build ?�과 **2026-0??|
| WBS-025 | 메뉴 ?�세·?�션·?�기 ?�면 ?�작 ?�인 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, DEV-SYS-002 | SCR 메뉴 ?�택, API-001, API-002, SCR-004 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-08-17 | 2026-08-27 | 50 | 카테고리 ?? 메뉴 카드, ?�절/?�그/가�??�시가 API ?�답 기�??�로 ?�작?�면 ?�료 ?�료 조건: Contract·?�기 ?�작 | ASAK-Kiosk | P3 Kiosk / Detail | Contract·?�기 ?�작 | SCR-004 · Target **2026-07-21**/008 |
| WBS-026 | ?�수·?�택 ?�션 �??�기 버튼 ?�성 조건 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, FWD-MENU-002, DE??| SCR 메뉴 ?�택, API-001, API-002 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-08-27 | 2026-08-28 | 50 | 카테고리 ?? 메뉴 카드, ?�절/?�그/가�??�시가 API ?�답 기�??�로 ?�작?�면 ?�료 ?�료 조건: Interaction evidence | ASAK-Kiosk | P3 Kiosk / Options | Interaction evidence | FWD-MENU-002 · Target **2026-07-21**/008 |
| WBS-027 | ?�레르기 ?�보 조건부 ?�시 | FWD-MENU-001, FWD-MENU-006, LMIS-MENU-002, FWD-MENU-004, FW??| SCR 메뉴 ?�택, API-001, API-002 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | 카테고리 ?? 메뉴 카드, ?�절/?�그/가�??�시가 API ?�답 기�??�로 ?�작?�면 ?�료 ?�료 조건: UI·QA evidence | ASAK-Kiosk | P3 Kiosk / Allergy | UI·QA evidence | FWD-MENU-004 · Target **2026-07-21**/008 |
| WBS-028 | 같�? 메뉴 ?�바구니 최�? ?�량 9개로 ?�한 | FWD-UI-001, FWD-UI-005 | ??| ?�론?�엔??| FWD | ?�연 | DONE | ??| 2026-07-21 | 2026-08-07 | 100 | ?�료 조건: Store ?�스??evidence | ASAK-Kiosk | P3 Kiosk / Store | Store ?�스??evidence | cart policy · Target **2026-07-20** |
| WBS-029 | ?�바구니 ?�체 최�? ?�량 30개로 ?�한 | KSD-ARCH-001 | ??| ?�론?�엔??| KSD | ?�연 | DONE | ??| 2026-07-04 | 2026-07-07 | 100 | ?�료 조건: Store ?�스??evidence | ASAK-Kiosk | P3 Kiosk / Store | Store ?�스??evidence | cart policy · Target **2026-07-20** |
| WBS-030 | ?�량 초과 ??4�??�내 ?�시 | FWD-MENU-001, LMIS-MENU-003 | ??| ?�론?�엔??| FWD | ?�연 | TODO | �?| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: Interaction evidence | ASAK-Kiosk | P3 Kiosk / Store | Interaction evidence | cart policy · Target **2026-07-20** |
| WBS-031 | ?�바구니 ?�량 조절, ??��, ?�체 비우�?| FWD-CART-001, FWD-CART-002, FWD-ORDER-001 | SCR ?�바구니, API-005, SCR-005 | ?�론?�엔??| FWD | ?�연, ?�진 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�량 변�???��, ?�션 ?�약??가?�하�??�료. 2026-07-04 ?�정: Day 10 범위?�서 API-016(?�바구니 검�? ?�외 (8�??�장 API). Day 10?� API-0??| ASAK-Kiosk | P3 Kiosk / Cart | SCR-005 route ?�작 | FWD-CART-002 · Target **2026-07-20** |
| WBS-032 | 결제 ?�단 ?�택 ?�면 | FWD-PAY-001, FWD-PAY-002, DEV-PAY-001, FWD-ORDER-002, FWD-M??| SCR-007 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: SCR-007 route ?�작 | ASAK-Kiosk | P3 Kiosk / Payment | SCR-007 route ?�작 | FWD-PAY-001 · payment adapter/API ?�어 ?�렬 · Vite build ?�과 **2026-07-28** · ?�API/브�?|
| WBS-033 | 결제 ?�패 ???�바구니 ?��? | FWD-PAY-001, FWD-PAY-002, DEV-PAY-001, FWD-ORDER-002, DEV-P??| SCR-012 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Error-flow evidence | ASAK-Kiosk | P3 Kiosk / Payment | Error-flow evidence | SCR-012 · `usePayment` ?�패 ??cart ?��? · ?�연??QA ?�음/027 |
| WBS-034 | 주문 ?�료 ?�면 번호·금액·?��??�시 | FWD-SYS-001 | SCR-008 | ?�론?�엔??| FWD | ?�연 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Completion evidence | ASAK-Kiosk | P3 Kiosk / Complete | Completion evidence | SCR-008 · Target **2026-07-21** |
| WBS-035 | 미조???�?�아??경고·카운?�다??| FWD-SYS-001, LMIS-MENU-004, LMIS-MENU-005, LMIS-MENU-006 | SCR-013 | ?�론?�엔??| FWD | ?�연 | TODO | �?| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: Timer QA evidence | ASAK-Kiosk | P3 Kiosk / Timeout | Timer QA evidence | SCR-013 · Target **2026-07-21**/028 |
| WBS-036 | 결제 �??�?�아???�외 | FWD-SYS-001, LMIS-PAY-001 | SCR-013 | ?�론?�엔??| FWD | ?�연 | TODO | �?| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: Payment-state evidence | ASAK-Kiosk | P3 Kiosk / Timeout | Payment-state evidence | SCR-013 · Target **2026-07-21**/028 |
| WBS-037 | ?�오?�크 로딩·빈화면·오�??�태 | DEV-SYS-002, RTOS-SYS-001 | ??| ?�론?�엔??| DEV | ?�연 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: State QA evidence | ASAK-Kiosk | P3 Kiosk / States | State QA evidence | Target **2026-07-22** |
| WBS-038 | ?�오?�크 ?�치·?�면 ?�기 QA | FWD-UI-001, FWD-UI-003 | ??| ?�론?�엔??| FWD | ?�연, ?�진 | TODO | �?| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: QA ?�행 | ASAK-Kiosk | P3 Kiosk / QA | QA ?�행 | 48px · Target **2026-07-22** |

### 관리자 (13)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-039 | 관리자 메뉴 경로·?�면 목록 ?�합 | ??| ??| ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: Registry 검??| ASAK-Admin | P4 Admin / Route | Registry 검??| Target **2026-07-20** |
| WBS-040 | 관리자 ?�?�보??지?�·최�?주문 | RTOS-DEVICE-001, RTOS-DEVICE-002, RTOS-DEVICE-003 | SCR-022 | ?�론?�엔??| RTOS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: Route·state evidence | ASAK-Admin | P4 Admin / Dashboard | Route·state evidence | SCR-022 · `DashboardPanels`·`useDashboard` · 최근주문??getDashboard().recentOrders`??|
| WBS-041 | ?�시�?주문 ?�황 목록·?�태 ?�시 | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003 | SCR-009 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Route evidence | ASAK-Admin | P4 Admin / Live order | Route evidence | SCR-009 · `getLiveOrders`·?�료/취소 ConfirmDialog · ?�이�??�수 · Target **2026-07-20** ??|
| WBS-042 | 주문 관�?목록·?�세 ?�결 | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003, LMIS-ORDER-??| SCR-010 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Screen evidence | ASAK-Admin | P4 Admin / Orders | Screen evidence | SCR-010 · `useOrdersQuery`·DetailPanel·?�불/?�수�?Confirm · 주문 ?�세 기본 ?��?/?�션 추�?�??�외 ?��?|
| WBS-043 | 주문 ?�태 변�??�료/취소) | LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003 | ??| ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: PATCH mock evidence | ASAK-Admin | P4 Admin / Orders | PATCH mock evidence | Live ?�료/취소�?· 목록 PATCH/TTS 미완(?�도???�시�? · Target **2026-07-21**/036 |
| WBS-044 | ?�절 ?�정·?�??| ??| SCR-011 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-11 | 2026-08-14 | 50 | ?�료 조건: UI state evidence | ASAK-Admin | P4 Admin / Sold-out | UI state evidence | SCR-011 · `useSoldOutDraft`·Confirm ?�??· 카드 2줄·카?�고�?뱃�?·menus ?�기??· **?�패 fixture??|
| WBS-045 | 메뉴 추�?·?�정 ?�면(mock ?�?? | LMIS-MENU-004, LMIS-MENU-005, LMIS-MENU-006 | SCR-016 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-11 | 2026-08-14 | 50 | ?�료 조건: UI evidence | ASAK-Admin | P4 Admin / Menu | UI evidence | SCR-016 · Page=조합(`useMenusQuery`+List/Detail/Edit) · IngredientModal · 카드 2줄·�???|
| WBS-046 | 결제 ?�단 ?�성·비활?�·�???| LMIS-PAY-001 | SCR-018 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: UI evidence | ASAK-Admin | P4 Admin / Payments | UI evidence | SCR-018 · Figma 4�?card/kakao/naver/zero) · ?��?·?�렬·미리보기·Confirm · **?�패 fixture ·??|
| WBS-047 | 매출 ?�약·기간 ?�터 | ??| SCR-019 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: UI evidence | ASAK-Admin | P4 Admin / Sales | UI evidence | SCR-019 · `useSalesQuery`+DatePicker range · AsyncState · Target **2026-07-21**??|
| WBS-048 | ?�별 매출 조회·???�환 | ??| SCR-020 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: UI evidence | ASAK-Admin | P4 Admin / Sales | UI evidence | SCR-020 · mock+???�비 · Target **2026-07-22** · Ev **2026-07-23** |
| WBS-049 | ?�별 매출 조회·?�짜 ?�택 | ??| SCR-021 | ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: UI evidence | ASAK-Admin | P4 Admin / Sales | UI evidence | SCR-021 · DatePicker single·?�간 · mock ????empty · CSS span ?�수 ?�정 · Target **202??|
| WBS-050 | 관리자 로딩·빈화면·오류·메??강조 ?�합 | ??| ??| ?�론?�엔??| LMIS | ?�진 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: State QA evidence | ASAK-Admin | P4 Admin / States | State QA evidence | Shared `AdminAsyncState`·ConfirmDialog�?주문/?�절/메뉴/결제/매출·?�?�보?�에 ?�용 · **???�면 QA·결제 ??|
| WBS-051 | ?�짜 ?�터·?�계·메뉴 강조 QA | ??| ??| ?�론?�엔??| LMIS | ?�진, ?�연 | IN_PROGRESS | ??| 2026-08-18 | 2026-08-21 | 50 | ?�료 조건: QA ?�행 | ASAK-Admin | P4 Admin / QA | QA ?�행 | Sales·KEEP QA 1�?· ?�행 evidence·P2 ?�리???�여 · ASAK_Admin #4 · Target **2026-07-22** |

### 백엔??(15)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-052 | 추천 ?�레???�션 ?�이??반영 | FWD-MENU-004, FWD-MENU-015 | ??| 백엔??| FWD | ?�진 | TODO | �?| 2026-07-06 | 2026-07-09 | ??| ?�료 조건: ?�션 ?�드·API ?�인 | ASAK-back | Backend / Option | ?�션 ?�드·API ?�인 | [FWD-MENU-004][FWD-MENU-015] |
| WBS-053 | DB ?�약조건 schema 반영 | KSD-ARCH-001 | ??| 백엔??| KSD | ?�진 | TODO | �?| 2026-07-04 | 2026-07-07 | ??| ?�료 조건: ?�약조건 리뷰 | ASAK-back | Backend / DB constraints | ?�약조건 리뷰 | [KSD-ARCH-001] |
| WBS-054 | 메뉴·?�료·?�션 ?�드 ?�이??| FWD-MENU-001, LMIS-MENU-003 | ??| 백엔??| FWD | ?�진, ?�연 | TODO | �?| 2026-07-05 | 2026-07-09 | ??| ?�료 조건: ?�드 ?�이??검??| ASAK-back | Backend / Seed | ?�드 ?�이??검??| [FWD-MENU-001][LMIS-MENU-003] |
| WBS-055 | ?�바구니 주문 가??검�?API | FWD-CART-001 | ??| 백엔??| FWD | ?�진 | TODO | �?| 2026-07-08 | 2026-07-11 | ??| ?�료 조건: 검�?규칙 ?�스??| ASAK-back | Backend / Cart | 검�?규칙 ?�스??| [FWD-CART-001] |
| WBS-056 | ?�이???�??방식 결정 | ??| ??| 백엔??| LMIS | ?�진, ?�연 | TODO | �?| 2026-08-14 | 2026-08-20 | ??| ?�료 조건: ?� 결정 | ASAK-back | P5 Backend / Baseline | ?� 결정 | DB audit |
| WBS-057 | DB ?�키마·마?�그?�이?�·시??방식 ?�정 | ??| ??| 백엔??| LMIS | ?�진, ?�연 | TODO | �?| 2026-08-14 | 2026-08-20 | ??| ?�료 조건: 검???�인 | ASAK-back | P5 Backend / Schema | 검???�인 | DB audit |
| WBS-058 | 메뉴 목록 API | ??| ??| 백엔??| LMIS | NEEDS_CONFIRMATION,??| IN_PROGRESS | ??| 2026-08-11 | 2026-08-14 | 50 | ?�료 조건: API ?�스??evidence | ASAK-back | P5 Backend / Menu | API ?�스??evidence | GET menuList · AdminMenu DTO/Service/Mapper 골격 · ?�브 계약 갱신 · Ev **2026-07-24** |
| WBS-059 | 메뉴 ?�세 API | ??| ??| 백엔??| LMIS | NEEDS_CONFIRMATION,??| IN_PROGRESS | ??| 2026-08-11 | 2026-08-14 | 50 | ?�료 조건: API ?�스??evidence | ASAK-back | P5 Backend / Menu | API ?�스??evidence | GET menuDetail · MenuDetail/Ing/OptPolicy Response · vw_menu_* · Ev **2026-07-2??|
| WBS-060 | 주문 ?�성 API(검증·�??? | ??| ??| 백엔??| LMIS | NEEDS_CONFIRMATION,??| IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: API ?�스??evidence | ASAK-back | P5 Backend / Orders | API ?�스??evidence | POST orders · UserOrderController/Service/Mapper 골격 · Ev **2026-07-24** |
| WBS-061 | 결제 ?�인·?�패 API | ??| API-006 | 백엔??| LMIS | NEEDS_CONFIRMATION,??| IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: API ?�스??evidence | ASAK-back | P5 Backend / Payments | API ?�스??evidence | POST payments · PaymentResult/UserPayMapper · API-006 계약 · Ev **2026-07-24** |
| WBS-062 | ?�절 처리 API | ??| ??| 백엔??| LMIS | NEEDS_CONFIRMATION,??| TODO | �?| 2026-08-11 | 2026-08-14 | ??| ?�료 조건: API ?�스??evidence | ASAK-back | P5 Backend / Admin | API ?�스??evidence | PATCH soldOut |
| WBS-063 | 관리자 주문 조회·?�태 변�?API | ??| ??| 백엔??| LMIS | NEEDS_CONFIRMATION,??| IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: API ?�스??evidence | ASAK-back | P5 Backend / Admin | API ?�스??evidence | Admin orders · Controller/Service/Mapper?� `vw_order_live`·목록/?�세 조회 SQL 보강 · leg??|
| WBS-064 | 매출 집계 ?�이???�스 ?�합 | ??| API-017 | 백엔??| LMIS | NEEDS_CONFIRMATION,??| IN_PROGRESS | ??| 2026-08-14 | 2026-08-18 | 50 | ?�료 조건: ?�계 검�?| ASAK-back | P5 Backend / Sales | ?�계 검�?| sales views ?�비 · API-017/018/019 ?�시·취소/?�불 집계 규칙 ?��? · `compileJava` ?�과 **2026-07??|
| WBS-065 | API ?�류 ?�답·?�력 검�??�일 | ??| ??| 백엔??| LMIS | ??| IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Contract tests | ASAK-back | P5 Backend / Common | Contract tests | ApiResponse + GlobalExceptionHandler · Bruno 주문 ?�청???�본 ?�어 ?�렬 · `compileJava` ?�과??|
| WBS-066 | DB ?�계·?�테?�블 ?�합 비교 | ??| ??| 백엔??| LMIS | ?�진, ?�연 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-21 | 50 | ?�료 조건: Audit report | ASAK / ASAK-back | P5 Backend / DB | Audit report | db-audit-plan · 7/28 중간?��? |

### ?�동 (5)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-067 | ?�면·?�버 ?�모???�동 | DEV-SYS-001, FWD-MENU-001 | ??| ?�동 | DEV | ?�진, ?�연 | TODO | �?| 2026-07-10 | 2026-07-13 | ??| ?�료 조건: ?�모???�과 | ASAK-Kiosk / ASAK-back | Integration / Smoke | ?�모???�과 | [DEV-SYS-001][FWD-MENU-001] |
| WBS-068 | 금액·?�태 ?�드�??�면·?�버 ?�합 | ??| ??| ?�동 | DEV | ?�연, ?�진 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Contract 검??| ASAK-Kiosk / ASAK-Admin | P6 Integration / Contracts | Contract 검??| totalAmount / APPROVED / EAT_IN · 8/7 Hub API ?�렬 |
| WBS-069 | ?�오?�크 ?�서�?API ?�동 | ??| ??| ?�동 | DEV | ?�연 | DELAYED | ??| 2026-08-07 | 2026-08-11 | ??| ?�료 조건: Backend contract 존재 | ASAK-Kiosk | P6 Integration / Kiosk | Backend contract 존재 | Kiosk API |
| WBS-070 | 관리자 ?�서�?API ?�동 | ??| ??| ?�동 | DEV | ?�진 | IN_PROGRESS | ??| 2026-08-07 | 2026-08-11 | 50 | ?�료 조건: Backend contract 존재 | ASAK-Admin | P6 Integration / Admin | Backend contract 존재 | Admin 주문 API ?�동 진행 · 메뉴/?�절/매출 ?�여 |
| WBS-071 | 결제·주문·?�간?� 매출 ?�계 검�?| ??| ??| ?�동 | DEV | ?�진, ?�연 | DELAYED | ??| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: Sales source 존재 | All | P6 Integration / Sales | Sales source 존재 | Sales QA |

### QA (8)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-072 | ?�오?�크 ?�외(결제·?�치·?�?�아?? ?��? | FWD-PAY-002, FWD-SYS-001, DEV-SYS-001, DEV-PAY-001 | ??| ?�스??| FWD | ?�진, ?�연 | TODO | �?| 2026-07-11 | 2026-07-16 | ??| ?�료 조건: ?�외 ?�나리오 QA | ASAK-Kiosk | QA / Kiosk exception | ?�외 ?�나리오 QA | ??|
| WBS-073 | ?�나리오 ?�행·결과·버그 기록 | DEV-SYS-002 | 03 ?�나리오, 09 ?�스???�나리오, 버그 DB | ?�스??| DEV | ?�연, ?�진 | TODO | ??| 2026-07-11 | 2026-07-17 | ??| ?�심 ?�나리오�??�제 ?�행 결과?� 버그가 기록?�면 ?�료 ?�료 조건: ?�나리오 결과 기록 | All | QA / Scenario | ?�나리오 결과 기록 | [DEV-SYS-002] |
| WBS-074 | ?�린 ?�면·?�갈리는 버튼 UX 개선 | DEV-SYS-002, FWD-UI-001 | ?�능/UX 개선 목록, 반영 ?�역 | ?�스??| DEV | ?�연, ?�진 | TODO | �?| 2026-07-17 | 2026-08-07 | ??| 주문 ?�름?�서 ?�린 ?�면, ?�갈리는 버튼, 반복 ?�력??개선?�면 ?�료 ?�료 조건: 개선 ??�� 기록 | ASAK-Kiosk / ASAK-Admin | QA / UX | 개선 ??�� 기록 | ??|
| WBS-075 | 글???�기·?��?가?�성 조정 | FWD-UI-001, FWD-UI-005 | ??| ?�스??| FWD | ?�연, ?�진 | TODO | �?| 2026-07-21 | 2026-08-07 | ??| ?�료 조건: ?�비·�????�용 evidence | ASAK-Kiosk | QA / A11y UI | ?�비·�????�용 evidence | ??|
| WBS-076 | ?�근???�정 ?�면 초안 | FWD-UI-001, FWD-UI-003 | ??| ?�스??| FWD | ?�진, ?�연 | TODO | �?| 2026-07-21 | 2026-08-07 | ??| ?�료 조건: ?�정 UI 초안 | ASAK-Kiosk / ASAK-Admin | QA / A11y settings | ?�정 UI 초안 | ??|
| WBS-077 | ?�구?�항 ?�스???�행·결과 기록 | ??| ??| ?�스??| QA | ?�연, ?�진 | TODO | �?| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: ?�행 evidence | All | P7 QA / Requirement | ?�행 evidence | QA suite |
| WBS-078 | 고�?비·키보드·?�치 ?�근???�스??| ??| ??| ?�스??| QA | ?�연, ?�진 | TODO | �?| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: ?�행 evidence | All | P7 QA / Accessibility | ?�행 evidence | Accessibility QA |
| WBS-079 | ?�오?�크·관리자 ?�합 ?��? ?��? | ??| ??| ?�스??| QA | ?�연, ?�진 | DELAYED | ??| 2026-08-18 | 2026-08-21 | ??| ?�료 조건: ?�합 ???�용 가??| All | P7 QA / Regression | ?�합 ???�용 가??| Regression QA |

### ?�영 (1)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-080 | 주간 ?�모·?�고 기록 | DEV-SYS-001 | 주간 ?�모 기록, ?�고 메모, ?�음 �??�션 ?�이??| ?�업 | DEV | ?�연, ?�진 | TODO | �?| 2026-07-10 | 2026-08-21 | ??| 매주 구현???�면/API�??�연?�고 막힌 ?�과 ?�음 �??�업??WBS??반영?�면 ?�료 ?�료 조건: 주간 기록 | ASAK | Ops / Demo cadence | 주간 기록 | [DEV-SYS-001] |

### 발표 (5)

| ?�업 ID | ?�업�?| ?�구?�항 | 관???�출�?| 구분 | ?�계 | ?�당??| ?�태 | ?�선?�위 | ?�작??| 종료??| 진척�?| 비고 | Repository | Phase | Handoff | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WBS-081 | 발표 ?�료·?�연 ?�서 준�?| DEV-SYS-002 | ??| 발표 | DEV | ?�연, ?�진 | TODO | �?| 2026-08-17 | 2026-08-27 | ??| ?�료 조건: ?�료·?�나리오 검??| ASAK | Release / Materials | ?�료·?�나리오 검??| [PRESENT-001] |
| WBS-082 | 발표 ??최종 리허??| DEV-SYS-002 | 최종 리허??체크리스?? 발표 Q&A 메모 | 발표 | DEV | ?�연, ?�진 | TODO | ??| 2026-08-27 | 2026-08-28 | ??| ?�연 ?�름???�기지 ?�고 ?�?�별 발표/질의?�답 ?�?�이 가?�하�??�료 ?�료 조건: 리허??기록 | ASAK | Release / Rehearsal | 리허??기록 | ??|
| WBS-083 | 문서·?�수?�계·?�모 ?�료 ?�합 | ??| ??| 발표 | PRESENT | ?�진, ?�연 | IN_PROGRESS | ??| 2026-08-14 | 2026-08-21 | 50 | ?�료 조건: ?�람 검??| ASAK | P8 Docs / Handoff | ?�람 검??| DevCopilot sync |
| WBS-084 | 배포 ??빌드·?�경·체크리스???��? | ??| ??| 발표 | PRESENT | ?�진, ?�연 | DELAYED | ??| 2026-08-14 | 2026-08-28 | ??| ?�료 조건: 모든 ?�?�소 ?��? ?�과; 배포 ?�경·?�당 ?�인; Release Candidate 검??| All repositories | P8 Release / Readiness | 모든 ?�?�소 ?��? ?�과; 배포 ?�경·?�당 ?�인; Release Candidate 검??| Definition of Done: checklist ?�인 �?RC evidence 첨�?. Evidence: [Release Checklist??|
| WBS-085 | 발표 ?�라?�드·?�모 ?�본·비??계획 ?�료 | ??| ??| 발표 | PRESENT | ?�진, ?�연 | TODO | �?| 2026-08-14 | 2026-08-28 | ??| ?�료 조건: ?�라?�드, ?�크립트, Demo 1?? ?�서, fallback, 최종 리허??기록???� 검???�료 | All repositories | P8 Presentation / Demo | ?�라?�드, ?�크립트, Demo 1?? ?�서, fallback, 최종 리허??기록???� 검??| Definition of Done: ?� 검??�?리허??evidence ?�료. Evidence: 2026-07-03 ?�의?�서 발표/demo�???|

**�?85�?**

## ?�외 (Hub 미등�?

| ??�� | ?�용 | ?�유 |
|---|---|---|
| 추적?�·RTOS-SYS | RTOS-SYS-001 추적???��? | EXCLUDED |
| 미사??번호 | ?�정??건너?� 번호 | ??|
| RTOS ?�수�?| RTOS ?�수�?모의 | MVP ??|
| EXT-001/002 | ??��?�망 | Notion archive |

## ?�당

- ?�오?�크 I/O·QA: ?�연 / Admin·문서·Hub: ?�진 / ?�합: 공동
- ?�탈 ?�원(민�?·?�진) ??**?�연·?�진** ?��? ?�기
