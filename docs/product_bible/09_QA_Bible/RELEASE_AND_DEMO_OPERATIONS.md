# Release and Demo Operations

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `BUG_REPORT_TEMPLATE.md`
- `DEMO_SCENARIO.md`
- `KNOWN_LIMITATIONS.md`
- `RELEASE_CHECKLIST.md`

---

## 원문: `BUG_REPORT_TEMPLATE.md`

### Bug Report Template

#### Title

[Domain][Priority] Summary

#### Environment

- Browser
- OS
- Branch
- Commit
- API/Mock

#### Preconditions

#### Steps

1.
2.
3.

#### Expected

#### Actual

#### 근거

- Screenshot
- Console
- Network
- DB

#### Scope

- Screen
- Component
- API
- DB

#### Severity

P0 / P1 / P2

---

## 원문: `DEMO_SCENARIO.md`

### Demo Scenario

#### Demo 1 — 고객 주문

1. Home
2. EAT_IN
3. Menu List
4. Detail 옵션 선택
5. Cart
6. Payment
7. Complete
8. waitingOrderCount

#### Demo 2 — 결제 실패 복구

1. Payment failure
2. Cart 유지
3. Retry
4. Approved

#### Demo 3 — 관리자 운영

1. Login
2. Dashboard
3. Live Order
4. PREPARING
5. COMPLETED
6. TTS

#### Demo 4 — 품절

1. Ingredient sold-out
2. 영향 메뉴 확인
3. Save
4. Kiosk 반영

#### Demo 5 — Sales

1. 기간 선택
2. KPI
3. Chart
4. Popular menu

---

## 원문: `KNOWN_LIMITATIONS.md`

### Known Limitations

#### MVP / Demo

- 실제 PG 미연동
- 실물 영수증 프린터 미연동
- 회원·쿠폰 확장
- WebSocket 미적용
- 매출 데이터는 Mock Data
- 외부 AI TTS 미사용
- 재고 수량·발주 미포함

#### Important

제한사항은 숨기지 않는다.

대신 다음을 설명한다.

- 왜 MVP에서 제외했는가
- 구조상 어떻게 확장 가능한가
- 현재 어떤 Mock/Interface를 준비했는가

---

## 원문: `RELEASE_CHECKLIST.md`

### Release Checklist

#### Code

- [ ] build
- [ ] lint
- [ ] no console fatal
- [ ] no secret
- [ ] env example
- [ ] README

#### Data

- [ ] seed
- [ ] mock consistency
- [ ] status code
- [ ] amount

#### Figma

- [ ] latest frames
- [ ] no visible spec
- [ ] prototype
- [ ] screenshot

#### QA

- [ ] P0 all pass
- [ ] P1 reviewed
- [ ] Demo complete
- [ ] regression
- [ ] accessibility

#### Presentation

- [ ] demo account
- [ ] stable mock
- [ ] fallback video/screenshots
- [ ] known limitation
