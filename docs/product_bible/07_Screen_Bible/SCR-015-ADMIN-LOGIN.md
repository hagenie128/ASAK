# SCR-015: Admin Login

> Status: **DRAFT**
> Route: `/login`
> Purpose: 관리자 인증
> 2026-08-25 결정: 계정(아이디/비밀번호) 인증 대신 매장 번호 하드코드 승인으로 방향 변경 —
> [`admin-todo-2026-08-24.md`](../../planning/admin-todo-2026-08-24.md) 우선순위 2 참고


## 1. Domain

`Admin`

## 2. Figma Reference

Figma node 39:8747 (매장 번호 입력 UI로 갱신 필요 — 기존 아이디/비밀번호 폼 기준)

## 3. Main Data

```text
storeNumber, session(단순 승인 플래그)
```

## 4. Required States

- `default`
- `loading`
- `error`

## 5. Product Rules

- 매장 번호 하나만 입력받아 승인한다 — 아이디/비밀번호 2필드 입력이 아니다.
- 매장 번호는 고정값 `'0001'` 하드코드 비교. DB 매장 테이블 조회·매장별 로그인 확장 없음.
- 세션은 JWT 없이 단순 승인 플래그로 유지한다 (토큰 발급·만료 관리 없음).
- error/loading을 제공한다. password visibility는 해당 없음(비밀번호 필드 없음).
- 성공 후 Dashboard로 이동한다.
- 인증이 mock인지 실제인지 명시한다.

## 6. React Component Map

- `LoginPage`
- `LoginForm` (매장 번호 입력 단일 필드로 교체 예정 — 미구현, 현재 코드는 아이디/비밀번호 mock)

## 7. API Contract

- `POST /api/admin/login`

## 8. User Actions

- 화면의 단일 핵심 행동을 유지한다.
- destructive action은 확인 단계를 둔다.
- 실패 시 이전 입력과 선택 상태를 가능한 한 유지한다.

## 9. Edge Cases

- 네트워크 실패
- 중복 클릭
- 오래된 응답
- 품절 또는 상태 변경
- 데이터 없음
- 화면 이탈과 복귀
- 접근성 모드 적용

## 10. Accessibility

- 핵심 터치 타겟 80×80px 이상
- 색상만으로 상태를 표현하지 않음
- focus/label/aria 속성 제공
- 글자 확대 시 overflow 방지

## 11. QA Checklist

- [ ] Figma state와 React state가 일치한다.
- [ ] API 필드와 화면 표시값이 일치한다.
- [ ] Empty·Loading·Error가 누락되지 않는다.
- [ ] 접근성 기준을 충족한다.
- [ ] 잘못된 더미데이터와 개발 메모가 노출되지 않는다.

## 12. Definition of Done

- [ ] Figma 완료
- [ ] React skeleton 또는 구현
- [ ] API 계약 확인
- [ ] DB source 확인
- [ ] PrototypeMap 반영
- [ ] P0 이슈 0건
