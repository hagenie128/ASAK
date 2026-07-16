# Accessibility Architecture

> Status: Current
> Figma: SCR-014

## 목적
접근성은 부가 기능이 아니라 주문 성공률을 높이는 핵심 기능이다.

## MVP 범위
- 글자 크기 3단계
- 고대비 모드
- 최소 터치 영역 80×80px
- 색상 외 텍스트·아이콘 상태 표현
- 설정 적용·초기화
- 현재 세션 유지

## 설정 모델
```js
{
  fontScale: "DEFAULT",
  contrastMode: "DEFAULT",
  largeTouchTarget: true
}
```

## 저장 정책
- 현재 세션: Zustand
- 단말 유지: localStorage

## 적용 대상
Home, Menu List, Menu Detail, Cart, Payment, Complete, Timeout Modal

## 글자 크기
```text
DEFAULT
LARGE
EXTRA_LARGE
```

CSS zoom보다 디자인 토큰 기반 scale을 권장한다.

## 고대비
- 텍스트 대비 강화
- border 강화
- 선택 상태를 색상+아이콘+텍스트로 표현
- 브랜드 라임만으로 상태를 구분하지 않음

## React 구조
```text
AccessibilityPage
AccessibilityPreview
AccessibilityToggle
AccessibilityScaleSelector
accessibilityStore
useAccessibilityMode
```

## 구현 체크리스트
- [ ] fontScale
- [ ] contrastMode
- [ ] localStorage
- [ ] preview
- [ ] apply/reset
- [ ] 전체 Kiosk 반영
- [ ] overflow QA
