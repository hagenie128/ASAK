# Mock Data Implementation

## 목적

Backend 미완성 상태에서도 UI·발표 흐름을 안정적으로 유지한다.

## 위치

기존 `src/mocks` 구조를 우선한다.

## 규칙

- API Response shape과 동일
- 날짜 중복 없음
- status code 동일
- amount integer
- KPI 정합성
- 16,800원 흐름 유지

## 금지

Page 내부에 대량 더미데이터 직접 작성.
