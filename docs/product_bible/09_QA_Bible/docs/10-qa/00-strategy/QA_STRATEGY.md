# QA Strategy

## 1. 테스트 레벨

### Smoke

앱 실행과 핵심 화면 진입.

### Functional

기능별 입력·행동·결과.

### Integration

Kiosk → API → DB → Admin.

### Regression

기존 기능이 수정 후에도 유지되는지 확인.

### Acceptance

요구사항과 Figma 기준 충족.

### Demo

발표·포트폴리오 시연 흐름.

---

## 2. 우선순위

### P0

- 주문 불가
- 결제 중복
- 금액 불일치
- Cart 초기화
- 상태 전이 오류
- 품절 메뉴 주문 가능
- 화면 ID/route 충돌
- 서버 가격 검증 누락

### P1

- Loading/Empty/Error 누락
- 필터·검색 오류
- TTS 중복 호출
- Dashboard 일부 데이터 오류
- 접근성 모드 일부 미반영

### P2

- 카피
- 간격
- hover
- 미세한 차트 표현
- 확장 기능

---

## 3. 테스트 순서

```text
Build
→ Smoke
→ Feature
→ Integration
→ Data Integrity
→ Regression
→ Accessibility
→ Demo
→ Release
```

---

## 4. Definition of Done

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
