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

---

## 7. 일상 워크플로 (main에 반영하기)

`main`에 직접 커밋하지 않는다. **브랜치에서 작업 → push → main에 merge** 순서를 지킨다.

### 7.1 작업 시작

```powershell
git checkout main
git pull origin main
git checkout -b docs/작업내용-요약   # 또는 feat/..., fix/...
# 코드 수정
git add .
git commit -m "docs: 무엇을 왜 바꿨는지"
git push -u origin HEAD
```

### 7.2 main에 넣기 (권장: PR)

```powershell
git checkout main
git pull origin main

git checkout docs/작업내용-요약
git merge main          # main 최신을 작업 브랜치에 먼저 반영
# 충돌 있으면 해결 → git add . → git commit
git push

gh pr create --base main --head docs/작업내용-요약
# GitHub에서 Merge
```

### 7.3 PR 없이 바로 넣을 때

```powershell
git checkout docs/작업내용-요약
git merge main
git push

git checkout main
git pull origin main
git merge docs/작업내용-요약
git push origin main
```

작업 브랜치와 `main`이 갈라져 있으면, **먼저 작업 브랜치에 `main`을 merge한 뒤** `main`으로 합친다.

### 7.4 자주 막히는 경우

| 메시지 | 의미 | 할 일 |
|--------|------|--------|
| `non-fast-forward` / behind | 원격이 더 앞섬 | `git pull` 후 다시 `push` |
| `Everything up-to-date` | 올릴 새 커밋 없음 | 보통 정상 (이미 같음) |
| merge 충돌 | 같은 파일 양쪽 수정 | 파일 고치고 `add` → `commit` |

**요약:** main 최신 받기 → 브랜치에서 작업 → push → (PR로) main에 merge → push

`git push --force`는 원격 커밋을 덮어쓰므로, 단순 behind 상황에서는 쓰지 않는다.
