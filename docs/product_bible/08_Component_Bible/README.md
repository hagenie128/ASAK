# ASAK Product Bible Pack 8 — Component Bible

> Status: Current Draft

## 목적

Figma 컴포넌트와 React 컴포넌트를 같은 기준으로 관리한다.

이 Pack은 다음 문제를 방지한다.

- 같은 역할의 컴포넌트 중복 생성
- 화면마다 다른 spacing·radius·typography 사용
- Figma variant와 React props 불일치
- Kiosk/Admin 컴포넌트 책임 혼선
- 기존 팀원이 구현한 컴포넌트를 무시한 재작성

## 가장 중요한 원칙

1. 기존 React 컴포넌트를 우선 재사용한다.
2. 기존 팀원이 작성한 코드는 삭제·대체하지 않는다.
3. Figma 이름과 React 이름이 달라도 역할이 같으면 mapping으로 연결한다.
4. 새 컴포넌트는 기존 컴포넌트로 표현할 수 없는 경우에만 만든다.
5. 화면 구현보다 공통 컴포넌트 재사용을 먼저 검토한다.
