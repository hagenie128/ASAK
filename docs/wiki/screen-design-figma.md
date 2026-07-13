# ASAK 화면 설계 및 Figma 연동

> Notion 04. 화면 설계 · SCR-001~021 · Figma 프로토타입 연동 예정 (2026-07-06)

## Figma 연동

| 항목 | 내용 |
|------|------|
| 디자인 도구 | Figma (와이어프레임→프로토타입) |
| Notion 역할 | SCR 목록·요구사항·API·테스트 추적 |
| DevCopilot | Screens 탭 + Wiki 본 문서 (wiki/5) |
| Week 5 MVP | SCR-001~008 (8/1) + Week 6 SCR-009~011 (고객+관리자+결제실패) |

## 디자인 시스템 (DS-02)

**프로덕션 DS (2026-07-06)**: **DS-02 Modern Minimal** (charcoal + electric lime). 다른 후보와 하이브리드 문서는 정리했다.

Figma `kiosk_design` 파일의 DS 프레임. 상세: [kiosk-design-system-index.md](../design/kiosk-design-system-index.md)

| DS | Figma frame | 정본 |
|:--:|-------------|------|
| **02** | `DS-02 Modern Minimal` | Candidate B — Modern Minimal |

> 플러그인: [Create DS-02 Components](../design/figma-create-ds02-components-plugin/README.md) — DS-02 컴포넌트·UI Kit 생성

## SCR 요약표

| ID | 화면명 | Figma | 상태 |
|----|--------|-------|------|
| SCR-001 | 홈 (매장·포장) | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=61-273 | 와이어프레임 |
| SCR-002 | 먹고가기 / 포장 선택 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-2 | 병합됨 |
| SCR-003 | 메뉴 선택 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-3 | 와이어프레임 |
| SCR-004 | 메뉴 상세 / 옵션 선택 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-4 | 와이어프레임 |
| SCR-005 | 장바구니·주문확인 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-6 | 와이어프레임 |
| SCR-006 | 주문 확인 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-7 | 병합됨 |
| SCR-007 | 결제 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-8 | 와이어프레임 |
| SCR-008 | 주문 완료 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-9 | 와이어프레임 |
| SCR-009 | 관리자 주문 관리 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-17 | 와이어프레임 |
| SCR-010 | 관리자 주문 상세 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-18 | 와이어프레임 |
| SCR-011 | 관리자 판매 항목 품절 관리 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-19 | 와이어프레임 |
| SCR-012 | 결제 실패 / 재시도 (팝업·토스트) | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-10 | 기획중 |
| SCR-013 | 타임아웃 안내 / 자동 초기화 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-11 | 기획중 |
| SCR-014 | 접근성 설정 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-12 | 기획중 |
| SCR-015 | 관리자 로그인 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-13 | 기획중 |
| SCR-016 | 관리자 메뉴 관리 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-14 | 기획중 |
| SCR-017 | 관리자 메뉴 등록/수정 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-15 | 기획중 |
| SCR-018 | 관리자 결제수단 설정 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-16 | 기획중 |
| SCR-019 | 관리자 매출 요약 | https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-23 | 기획중 |
| SCR-020 | 영수증 출력 여부 선택 | *(Figma 예정)* | 기획중 |
| SCR-021 | 포인트·쿠폰 적립 | *(Figma 예정)* | 기획중 |

## 고객·관리자 흐름

**고객**: 홈(매장·포장) → 메뉴 → 옵션 → 장바구니·주문확인(컨펌 팝업) → 결제(로딩) → 완료

> 2026-07-06: SCR-002→001, SCR-006→005 병합. **DS-02 Modern Minimal** 채택.

**관리자**: 주문관리 → 주문상세 / 품절관리 / (후반) 로그인·메뉴·결제·매출

---

## SCR 상세 (SCR-001~021)

출처: Notion 04. 화면 설계 (2026-07-06 export)

## 고객 키오스크 흐름
홈(매장·포장) → 메뉴선택 → 메뉴상세/옵션 → 장바구니·주문확인(컨펌 팝업) → 결제(로딩) → 주문완료

> 2026-07-06: SCR-002→001, SCR-006→005 병합. SCR-002·006 ID는 참조용 유지.

## 관리자 흐름
주문관리 → 주문상세 / 품절관리 / (후반) 로그인·메뉴·결제수단·매출

## SCR-001 홈 (매장·포장) (FWD-UI-002)

- **구분**: 키오스크 | **단계**: FWD | **상태**: 와이어프레임
- **설명**: ASAK 키오스크 시작 화면. 브랜드 안내와 함께 매장(먹고가기)·포장 주문 유형을 한 화면에서 선택한다.
- **입력**: 없음
- **출력**: 브랜드 안내, 매장(먹고가기)/포장 선택, orderType(EAT_IN 또는 TAKE_OUT)
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=61-273
- **요구사항**: FWD-UI-002, FWD-ORDER-001
- **시나리오**: SC-001, 식당 키오스크 주문 흐름
- **비고**: 2026-07-06 SCR-002 병합. orderType은 장바구니·결제까지 유지. DS-02 Modern Minimal 적용.

## SCR-002 먹고가기 / 포장 선택

- **구분**: 키오스크 | **단계**: FWD | **상태**: 병합됨
- **설명**: 【병합됨】2026-07-06 회의 결정으로 SCR-001「홈 (매장·포장)」에 통합. 별도 화면 없음.
- **입력**: 없음
- **출력**: orderType(EAT_IN 또는 TAKE_OUT)
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-2
- **시나리오**: 식당 키오스크 주문 흐름
- **비고**: SCR-001에 병합. ID·Notion URL 참조용 유지. Figma 프레임은 SCR-001로 통합 예정.

## SCR-003 메뉴 선택 (FWD-MENU-001)

- **구분**: 키오스크 | **단계**: FWD | **상태**: 와이어프레임
- **설명**: 카테고리별 ASAK 메뉴 목록을 카드형으로 보여주는 화면
- **입력**: orderType, categoryId
- **출력**: 카테고리 목록, 메뉴 목록, 메뉴 이미지, 메뉴명, 가격, 계산된 기본 칼로리, 메뉴 품절 여부, 재료 품절 뱃지, 주문 가능 여부
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-3
- **요구사항**: FWD-UI-001, FWD-UI-002
- **시나리오**: 고객 주문 시나리오
- **API**: API-001, API-002
- **비고**: 핵심 재료/베이스 재료 품절 시 메뉴 주문 불가. 일반 기본 재료 품절 시 메뉴 카드에 재료 품절 뱃지 표시

## SCR-004 메뉴 상세 / 옵션 선택 (FWD-MENU-001)

- **구분**: 키오스크 | **단계**: FWD | **상태**: 와이어프레임
- **설명**: 메뉴 상세 정보를 확인하고 기본 재료 제외, 드레싱/토핑 등 옵션을 선택하는 화면입니다. 알레르기·칼로리 정보는 이 화면에서 표시합니다.
- **입력**: menuId, 기본 재료 목록, excludedIngredientIds, optionItems(optionItemId, ingredientId, quantity)
- **출력**: 선택 메뉴, 기본 재료, 제외 재료, 품절 재료 뱃지, 추가 옵션, 옵션 수량, 옵션그룹 유형, 세트 옵션, 옵션 제공량/단백질, 옵션 아이콘/색상, 품절 옵션칸, 베이스 변경 가능 여부, 예상 금액, 예상 알레르기 표시
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-4
- **요구사항**: FWD-MENU-001, FWD-MENU-002, FWD-MENU-003, FWD-MENU-004, FWD-MENU-005, FWD-MENU-015, LMIS-MENU-002
- **시나리오**: 옵션 선택 시나리오
- **API**: API-003, API-004
- **비고**: 기본 포함 재료도 추가 토핑으로 선택 가능. 옵션 재료 품절은 해당 옵션칸만 품절. 알레르기·칼로리는 장바구니가 아닌 본 화면(옵션 선택)에 표시 (2026-07-06).

## SCR-005 장바구니·주문확인 (FWD-CART-001)

- **구분**: 키오스크 | **단계**: FWD | **상태**: 와이어프레임
- **설명**: 담은 메뉴·옵션·수량·총액을 확인·수정한다. 결제 전 최종 확인은 컨펌 팝업으로만 처리하며, 하단에 추가 제안 상품을 배치한다.
- **입력**: 장바구니 항목, orderType, excludedIngredientIds, optionItems, 수량
- **출력**: 선택 메뉴, 기본 재료 제외 목록, 추가 옵션, 수량, 예상 총액, orderType, 추가 제안 상품, orderId(컨펌 팝업 확인 후)
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-6
- **요구사항**: FWD-CART-001, FWD-CART-002, FWD-CART-003 (EXCLUDED), FWD-ORDER-001, DEV-ORDER-001
- **시나리오**: 장바구니 확인 및 주문 생성 시나리오
- **API**: API-005
- **비고**: 2026-07-06 SCR-006 병합. 주문번호는 결제 완료(SCR-008) 후 표시. 알레르기·칼로리는 SCR-004에서 표시. 주문 생성 시 API-005.

## SCR-006 주문 확인

- **구분**: 키오스크 | **단계**: KSD | **상태**: 병합됨
- **설명**: 【병합됨】2026-07-06 회의 결정으로 SCR-005「장바구니·주문확인」에 통합. 최종 확인은 컨펌 팝업만.
- **입력**: 장바구니 항목, excludedIngredientIds, optionItems, 수량, orderType
- **출력**: orderId, orderNo, totalPrice, orderStatus
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-7
- **시나리오**: 장바구니 확인 및 주문 생성 시나리오
- **API**: API-005
- **비고**: SCR-005에 병합. ID·Notion URL 참조용 유지. Figma 프레임은 SCR-005로 통합 예정.

## SCR-007 결제 (FWD-PAY-001)

- **구분**: 키오스크 | **단계**: KSD | **상태**: 와이어프레임
- **설명**: 주문 금액을 확인하고 실제 PG 연동 없이 가상 결제를 진행하는 화면. 승인 대기 중 로딩 상태 필수.
- **입력**: orderId, paymentMethod, amount
- **출력**: paymentId, paymentStatus, orderStatus
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-8
- **요구사항**: FWD-PAY-001, KSD-MEMBER-001 (EXCLUDED), KSD-PAY-001
- **시나리오**: 가상 결제 완료 시나리오
- **API**: API-006
- **비고**: 실제 결제 연동이 아닌 가상 결제 승인 흐름. 결제 실패·재시도는 SCR-012 팝업/토스트 오버레이 (2026-07-06).

## SCR-008 주문 완료 (FWD-PAY-002)

- **구분**: 키오스크 | **단계**: KSD | **상태**: 와이어프레임
- **설명**: 결제 완료 후 주문번호와 주문 접수 상태를 보여주는 화면
- **입력**: orderNo, paymentStatus, totalPrice
- **출력**: 주문번호, 주문 완료 안내
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-9
- **요구사항**: FWD-PAY-002, FWD-ORDER-002, KSD-PAY-002, RTOS-DEVICE-001
- **시나리오**: 가상 결제 완료 시나리오
- **API**: API-006
- **비고**: 영수증 출력/장치 연동은 Week 5 MVP 제외

## SCR-009 관리자 주문 관리 (LMIS-ORDER-001)

- **구분**: 관리자 | **단계**: KSD | **상태**: 와이어프레임
- **설명**: 관리자가 주문 목록을 확인하고 특정 주문의 상세 화면으로 이동하는 화면
- **입력**: status
- **출력**: 주문 목록, 주문번호, 주문유형, 결제상태, 주문상태, 주문금액, 주문일시
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-17
- **요구사항**: LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-004
- **시나리오**: 관리자 주문 목록 확인, 주문 상세 확인 시나리오
- **API**: API-007
- **비고**: 주문 상태 변경은 관리자 주문 상세 화면에서 수행한다.

## SCR-010 관리자 주문 상세 (LMIS-ORDER-001)

- **구분**: 관리자 | **단계**: KSD | **상태**: 와이어프레임
- **설명**: 관리자가 특정 주문의 메뉴, 옵션, 주문유형, 결제상태, 주문상태를 확인하는 화면
- **입력**: orderId, 변경할 status
- **출력**: 주문 상세 정보, 변경된 주문 상태
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-18
- **요구사항**: LMIS-ORDER-001, LMIS-ORDER-002, LMIS-ORDER-003, LMIS-ORDER-004
- **시나리오**: 관리자 주문 상세 확인, 주문 상태 변경 시나리오
- **API**: API-007, API-008
- **비고**: 별도 주문 상세 API는 Week 5 MVP에서 만들지 않고 API-007 목록/상세 데이터 기반으로 표시

## SCR-011 관리자 판매 항목 품절 관리 (LMIS-MENU-001)

- **구분**: 관리자 | **단계**: KSD | **상태**: 와이어프레임
- **설명**: 관리자가 메뉴 또는 재료의 품절 상태를 변경하는 화면입니다. 품절 변경 후 메뉴·재료 상태 목록을 확인할 수 있습니다.
- **입력**: targetType(MENU/INGREDIENT), targetId, isSoldOut
- **출력**: 메뉴 목록, 메뉴 기본 재료, 옵션 항목, 재료 역할, 변경된 품절 상태, 영향받는 메뉴/옵션
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-19
- **요구사항**: LMIS-MENU-001, LMIS-MENU-002
- **시나리오**: 판매 항목 품절 관리 흐름(옵션기능)
- **API**: API-002, API-003, API-004, API-009
- **비고**: 옵션기능 화면. 메뉴 상세/API-004 옵션 응답에서 ingredientId 확인 후 API-009로 품절 변경. 품절 목록 뷰 필요 (2026-07-06).

## SCR-012 결제 실패 / 재시도 (팝업·토스트) (FWD-PAY-002)

- **구분**: 오류예외 | **단계**: FWD | **상태**: 기획중
- **설명**: 가상 결제 실패 또는 금액 불일치 시 팝업·토스트로 실패 사유를 안내하고 재결제하거나 장바구니로 돌아간다.
- **입력**: paymentId/orderId, errorCode, message
- **출력**: 재결제 요청, 장바구니·주문확인(SCR-005) 복귀
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-10
- **요구사항**: FWD-PAY-002, KSD-PAY-001
- **시나리오**: 결제 실패 흐름
- **API**: API-006
- **비고**: 2026-07-06: 별도 전체 화면보다 팝업·토스트 오버레이 우선. SCR-007 결제 중 표시.

## SCR-013 타임아웃 안내 / 자동 초기화 (FWD-SYS-001)

- **구분**: 오류예외 | **단계**: FWD | **상태**: 기획중
- **설명**: 일정 시간 입력이 없을 때 주문 초기화 전 안내 카운트다운을 보여주는 화면
- **입력**: 남은 시간, 현재 주문 상태
- **출력**: 주문 계속하기, 처음으로 이동
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-11
- **요구사항**: FWD-SYS-001
- **시나리오**: 일정시간 미입력 시 자동 초기화
- **비고**: API 없이 프론트 상태로 처리 가능

## SCR-014 접근성 설정 (FWD-UI-001)

- **구분**: 공통 | **단계**: FWD | **상태**: 기획중
- **설명**: 글자 크기, 고대비 등 키오스크 접근성 옵션을 선택하는 화면
- **입력**: 선택 가능한 접근성 옵션
- **출력**: 적용된 UI 설정
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-12
- **요구사항**: FWD-UI-001, FWD-UI-004
- **시나리오**: 접근성 옵션으로 저시력 고객 주문
- **API**: API-017
- **비고**: 8주 후반 고도화 항목

## SCR-015 관리자 로그인 (LMIS-AUTH-001 (EXCLUDED))

- **구분**: 관리자 | **단계**: LMIS | **상태**: 기획중
- **설명**: 관리자가 주문/메뉴 관리 화면에 접근하기 전 로그인하는 화면
- **입력**: 아이디, 비밀번호
- **출력**: 관리자 세션/토큰
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-13
- **요구사항**: LMIS-AUTH-001 (EXCLUDED)
- **시나리오**: 관리자 접근 흐름
- **비고**: Week 5 MVP에서는 인증 생략 가능, 후반 주차 적용

## SCR-016 관리자 메뉴 관리 (LMIS-MENU-004)

- **구분**: 관리자 | **단계**: LMIS | **상태**: 기획중
- **설명**: 관리자가 메뉴 목록, 가격, 태그, 품절 상태를 확인하는 화면
- **입력**: 메뉴 목록, 카테고리, 태그, 품절 상태
- **출력**: 메뉴 등록/수정 화면 이동, 품절 변경
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-14
- **요구사항**: LMIS-MENU-001, LMIS-MENU-004
- **시나리오**: 관리자의 신규 메뉴 등록, 판매 항목 품절 처리
- **API**: API-010, API-011, API-009
- **비고**: 관리자 기능 5~6주차 확장

## SCR-017 관리자 메뉴 등록/수정 (LMIS-MENU-004)

- **구분**: 관리자 | **단계**: LMIS | **상태**: 기획중
- **설명**: 관리자가 메뉴 기본정보, 기본 재료, 추천 드레싱, 옵션그룹, 태그를 등록/수정하는 화면
- **입력**: 메뉴명, 가격, 이미지, 재료, 옵션그룹, 추천 옵션, 태그
- **출력**: 메뉴 저장 요청
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-15
- **요구사항**: LMIS-MENU-004, FWD-MENU-013, FWD-MENU-014, FWD-MENU-015
- **시나리오**: 관리자의 신규 메뉴 등록
- **API**: API-012
- **비고**: 추천 드레싱은 menu_option 기준으로 저장

## SCR-018 관리자 결제수단 설정 (LMIS-PAY-001)

- **구분**: 관리자 | **단계**: LMIS | **상태**: 기획중
- **설명**: 관리자가 카드/간편결제 등 결제수단 노출 여부와 순서를 설정하는 화면
- **입력**: 결제수단 목록, 활성 여부, 정렬 순서
- **출력**: 결제수단 설정 변경 요청
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-16
- **요구사항**: LMIS-PAY-001
- **시나리오**: 결제 성공 흐름(수단 노출 포함)
- **API**: API-013, API-014
- **비고**: 결제수단은 common_code/payment_method_config 기준

## SCR-019 관리자 매출 요약 (LMIS-ORDER-005)

- **구분**: 관리자 | **단계**: LMIS | **상태**: 기획중
- **설명**: 관리자가 일별 주문수·매출 금액·매출 평균, 시간대별·판매 제품 통계를 확인하는 화면
- **입력**: 조회 기간, 일별 매출 데이터
- **출력**: 매출 요약 표시
- **Figma**: https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design?node-id=75-23
- **요구사항**: LMIS-ORDER-005, ARCHIVE-LMIS-ORDER-005 (EXCLUDED)
- **시나리오**: 관리자의 일별 매출 조회
- **API**: API-015
- **비고**: Week 5 MVP 제외, 8주 후반 확장. 시간대별 판매·제품 통계 확장 (2026-07-06).

## SCR-020 영수증 출력 여부 선택 (RTOS-DEVICE-001)

- **구분**: 키오스크 | **단계**: 장치 | **상태**: 기획중
- **설명**: 결제 완료 직후 고객이 영수증 출력 여부를 선택하는 화면
- **입력**: orderId, orderNo, paymentStatus, totalPrice
- **출력**: 영수증 출력 선택(예/아니오), 출력 결과 또는 화면 주문번호 표시
- **요구사항**: RTOS-DEVICE-001
- **시나리오**: SC-015
- **API**: API-019
- **비고**: Week 5 MVP 제외, Week 7~8 확장. SCR-008 주문 완료 후 분기

## SCR-021 포인트·쿠폰 적립 (LMIS-MEMBER-001)

- **구분**: 키오스크 | **단계**: KSD | **상태**: 기획중
- **설명**: 결제 단계에서 멤버십 스탬프 적립 1회 확인 및 쿠폰 QR 스캔·할인 표시
- **입력**: memberId, orderId, scanValue(쿠폰/멤버십 QR), 결제 금액
- **출력**: 적립 확인 결과, 스탬프 적립 여부, 쿠폰 할인 금액, 최종 결제 금액
- **요구사항**: LMIS-MEMBER-001, KSD-MEMBER-001 (EXCLUDED), RTOS-DEVICE-004 (EXCLUDED), RTOS-DEVICE-005 (EXCLUDED), RTOS-DEVICE-006
- **시나리오**: SC-006, SC-016
- **API**: API-018, API-020
- **비고**: Week 5 MVP 제외. SCR-007 결제 화면 내 패널/모달. 적립 확인 1회만
