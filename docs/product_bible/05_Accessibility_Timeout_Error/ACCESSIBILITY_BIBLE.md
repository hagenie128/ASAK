# Accessibility Bible

> Status: **CANONICAL**
> Updated: `2026-08-14`
> 이 문서는 아래 원문을 출처별 구획으로 통합했습니다. 원문의 규칙·표·체크리스트는 삭제하지 않았습니다.

## 통합 원문

- `ACCESSIBILITY_ARCHITECTURE.md`
- `ACCESSIBILITY_RULES_AND_QA.md`

---

## 원문: `ACCESSIBILITY_ARCHITECTURE.md`

### Accessibility Architecture

> Status: Current
> Figma: SCR-014

#### 목적
접근성은 부가 기능이 아니라 주문 성공률을 높이는 핵심 기능이다.

#### MVP 범위
- 글자 크기 3단계
- 고대비 모드
- 최소 터치 영역 80×80px
- 색상 외 텍스트·아이콘 상태 표현
- 설정 적용·초기화
- 현재 세션 유지

#### 설정 모델
```js
{
  fontScale: "DEFAULT",
  contrastMode: "DEFAULT",
  largeTouchTarget: true
}
```

#### 저장 정책
- 현재 세션: Zustand
- 단말 유지: localStorage

#### 적용 대상
Home, Menu List, Menu Detail, Cart, Payment, Complete, Timeout Modal

#### 글자 크기
```text
DEFAULT
LARGE
EXTRA_LARGE
```

CSS zoom보다 디자인 토큰 기반 scale을 권장한다.

#### 고대비
- 텍스트 대비 강화
- border 강화
- 선택 상태를 색상+아이콘+텍스트로 표현
- 브랜드 라임만으로 상태를 구분하지 않음

#### React 구조
```text
AccessibilityPage
AccessibilityPreview
AccessibilityToggle
AccessibilityScaleSelector
accessibilityStore
useAccessibilityMode
```

#### 구현 체크리스트
- [ ] fontScale
- [ ] contrastMode
- [ ] localStorage
- [ ] preview
- [ ] apply/reset
- [ ] 전체 Kiosk 반영
- [ ] overflow QA

---

## 원문: `ACCESSIBILITY_RULES_AND_QA.md`

### Accessibility Rules and QA

#### 터치
- 최소 80×80px
- 주요 CTA 100~120px
- 작은 아이콘만으로 핵심 행동 제공 금지

#### 대비
- 오류·성공·선택은 색상 외 아이콘·문구 병행
- disabled도 상태를 식별 가능하게 유지

#### 포커스
- Admin은 keyboard focus 제공
- Kiosk도 focus outline을 제거하지 않음

#### 오류
- 관련 입력 위치와 연결
- 해결 방법 포함
- 사용자를 탓하지 않음

#### QA
- [ ] 고대비에서 모든 텍스트 식별
- [ ] 글자 확대 시 overflow 없음
- [ ] Bottom CTA 가림 없음
- [ ] Modal clipping 없음
- [ ] 색상 없이 상태 구분
- [ ] 확대 후 뒤로가기 가능
