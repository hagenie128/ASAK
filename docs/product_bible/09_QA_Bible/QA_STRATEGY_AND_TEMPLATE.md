# QA Strategy and Template

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `QA_STRATEGY.md`
- `TEST_CASE_TEMPLATE.md`

---

## 원문: `QA_STRATEGY.md`

### QA Strategy

#### 1. 테스트 레벨

##### Smoke

앱 실행과 핵심 화면 진입.

##### Functional

기능별 입력·행동·결과.

##### Integration

Kiosk → API → DB → Admin.

##### 회귀 점검

기존 기능이 수정 후에도 유지되는지 확인.

##### Acceptance

요구사항과 Figma 기준 충족.

##### Demo

발표·포트폴리오 시연 흐름.

---

#### 2. 우선순위

##### P0

- 주문 불가
- 결제 중복
- 금액 불일치
- Cart 초기화
- 상태 전이 오류
- 품절 메뉴 주문 가능
- 화면 ID/route 충돌
- 서버 가격 검증 누락

##### P1

- Loading/Empty/Error 누락
- 필터·검색 오류
- TTS 중복 호출
- Dashboard 일부 데이터 오류
- 접근성 모드 일부 미반영

##### P2

- 카피
- 간격
- hover
- 미세한 차트 표현
- 확장 기능

---

#### 3. 테스트 순서

```text
Build
→ Smoke
→ Feature
→ Integration
→ Data Integrity
→ 회귀 점검
→ Accessibility
→ Demo
→ Release
```

---

#### 4. Definition of Done

- [ ] Build 성공
- [ ] Lint 오류 없음
- [ ] 핵심 P0 통과
- [ ] Figma state 존재
- [ ] API contract 일치
- [ ] 금액 정합성
- [ ] 상태값 일치
- [ ] Error recovery
- [ ] Accessibility
- [ ] Demo script 통과

---

## 원문: `TEST_CASE_TEMPLATE.md`

### Test Case Template

```md
#### TC-{DOMAIN}-{NUMBER}

##### Priority
P0 / P1 / P2

##### Feature
Order / Cart / Payment / Menu / Admin / Sales / ...

##### Preconditions
- 상태
- 데이터
- 로그인 여부

##### Steps
1.
2.
3.

##### Expected Result
-

##### Actual Result
-

##### Result
PASS / FAIL / BLOCKED

##### 근거
- Screenshot
- Console
- Network
- DB

##### Related
- Screen
- API
- Requirement
- Component
```
