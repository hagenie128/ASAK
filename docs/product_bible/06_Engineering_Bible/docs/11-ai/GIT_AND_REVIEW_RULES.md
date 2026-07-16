# Git and Code Review Rules

## 1. Branch

```text
feature/
fix/
docs/
refactor/
hotfix/
```

한 branch는 하나의 목적.

---

## 2. Commit

권장:

```text
feat:
fix:
docs:
refactor:
style:
test:
chore:
```

예:

```text
feat: 관리자 대시보드 KPI 카드 추가
fix: 결제 오류 화면 금액 정합성 수정
docs: TTS 중복 호출 정책 문서화
```

---

## 3. Commit Scope

너무 큰 commit 금지.

좋은 분리:

1. scaffold
2. component
3. state
4. API
5. QA/docs

---

## 4. PR Description

```md
## 목적
## 변경 내용
## 변경 이유
## 영향 화면
## API/DB 영향
## 테스트
## 스크린샷
## 남은 작업
```

---

## 5. Review Checklist

- naming
- duplication
- state
- error recovery
- API contract
- DB impact
- Figma consistency
- accessibility
- build/lint
- secrets

---

## 6. Merge

팀원 작업과 충돌 가능한 파일:

- App/Router
- store
- constants
- shared component
- API client

수정 전에 담당자와 범위를 확인한다.
