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

## 7. 일상 워크플로 (원격 main까지 반영하기)

`main`에 직접 커밋하지 않는다. 독립 저장소마다 아래 1→10 순서를 지킨다. 변경 파일은 `git add .`로 일괄 stage하지 않고, 승인된 경로만 명시한다. 작업 트리가 더럽거나 `main`을 안전하게 최신화할 수 없으면 stash·reset·rebase를 하지 말고 중단한다.

```powershell
# 1. main 최신화
git switch main
git pull --ff-only origin main

# 2. 기능별·레포별 작업 브랜치 생성
git switch -c feat/admin-order-list   # 또는 docs/..., fix/..., chore/...

# 3. 승인된 파일 검토·stage·검증
git diff
git diff --check
git add -- src/api/ordersApi.js src/pages/admin/OrderListPage.jsx
# 프로젝트에 맞는 build/test 실행

# 4. 한글 커밋: 에이전트 이름을 제목에 넣지 않는다
git commit -m "feat: admin 주문목록 조회 구현"

# 5. 작업 브랜치를 GitHub에 푸시
git push -u origin feat/admin-order-list

# 6. main으로 이동 후 다시 최신화
git switch main
git pull --ff-only origin main

# 7. 작업 브랜치를 main에 병합
git merge feat/admin-order-list

# 8. 병합된 main을 GitHub에 푸시
git push origin main

# 9. 병합된 로컬 작업 브랜치 삭제
git branch -d feat/admin-order-list

# 10. GitHub 원격 작업 브랜치 삭제
git push origin --delete feat/admin-order-list
```

8단계 뒤에는 대상 커밋이 `main`에 포함되고 `HEAD == origin/main`인지 확인한다. 7단계에서 충돌이 발생하면 자동 해결하지 말고 중단한다. PR이 필수인 저장소는 5단계에서 PR을 만든 뒤, 승인·병합 후 6·8·9·10단계를 수행한다.

### 7.4 자주 막히는 경우

| 메시지 | 의미 | 할 일 |
|--------|------|--------|
| `non-fast-forward` / behind | 원격이 더 앞섬 | `main`에서 `git pull --ff-only origin main` 후 병합 가능 여부를 다시 확인 |
| `Everything up-to-date` | 올릴 새 커밋 없음 | 보통 정상 (이미 같음) |
| merge 충돌 | 같은 파일 양쪽 수정 | 자동 해결하지 말고 충돌 범위와 다음 조치를 팀에 확인 |

**요약:** main 최신화 → 기능/레포별 브랜치 → 명시 stage·검증 → 한글 커밋 → 원격 브랜치 푸시 → main 최신화 → 병합 → 원격 main 푸시 → 로컬 브랜치 삭제 → 원격 브랜치 삭제

`git push --force`는 원격 커밋을 덮어쓰므로, 단순 behind 상황에서는 쓰지 않는다.
