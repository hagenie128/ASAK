# ADR-001: Admin Dashboard를 별도 홈으로 둔다

- Status: Accepted
- Date: 2026-07-16

## Context

기존 Admin 구조는 주문 현황을 첫 화면으로 사용했다. 그러나 관리자 역할은 실시간 주문 처리뿐 아니라 매출, 품절, 인기 메뉴, 운영 이상을 함께 판단하는 것이다.

## Options

### A. 주문 목록을 홈으로 유지

장점:
- 구현이 단순하다.
- 기존 구조를 유지한다.

단점:
- 매장 전체 상태를 파악하기 어렵다.
- Navbar Home과 주문관리 역할이 겹친다.

### B. Dashboard를 별도 홈으로 추가

장점:
- 운영 상태를 한 화면에서 확인한다.
- 실시간 주문 보드와 주문 관리의 역할을 분리한다.
- 포트폴리오 제품 완성도가 높아진다.

단점:
- 신규 화면과 데이터 집계가 필요하다.

## Decision

B를 채택한다.

## Dashboard Minimum Data

- 오늘 매출
- 주문 수
- 평균 객단가
- 진행 중 주문
- 실시간 주문 요약
- 품절
- 인기 메뉴

## Consequences

- SCR-022 추가
- `/` route는 Dashboard
- 주문관리는 별도 route
- 로그인 성공 후 Dashboard 이동
- Dashboard API 또는 기존 API 조합 필요
