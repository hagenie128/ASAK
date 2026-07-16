# ASAK Product Bible Pack 9 — QA Bible

> Status: Current Draft

## 목적

ASAK의 품질 기준을 기능 완료 여부가 아니라 실제 사용 시나리오와 데이터 정합성 기준으로 검증한다.

## 범위

- Kiosk
- Admin
- API
- Backend
- Database
- Accessibility
- Regression
- Demo
- Release

## 우선순위

```text
P0 = 핵심 흐름이 막히거나 데이터가 틀리는 문제
P1 = 주요 기능은 되지만 불편하거나 일부 기능이 깨지는 문제
P2 = 표현·세부 UX·확장 기능 문제
```

## 가장 중요한 원칙

1. Default 화면만 확인하고 완료 처리하지 않는다.
2. Loading·Empty·Error·Disabled·Processing을 확인한다.
3. Figma와 React가 같아도 API·DB 값이 다르면 실패다.
4. Mock Data도 숫자 정합성을 지켜야 한다.
5. 기존 팀원이 만든 프론트 코드를 살리되 회귀 테스트로 보호한다.
