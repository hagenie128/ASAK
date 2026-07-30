---
name: asak-git-publish
description: "Use for approved ASAK branch creation, Korean commits, remote branch push, origin/main merge and push, remote verification, and merged branch cleanup."
---

# 깃반영

ASAK의 독립 저장소를 기능별·레포별 작업 브랜치로 안전하게 원격 `main`까지 반영한다. 브랜치 생성, 한글 커밋, 원격 푸시, main 병합·푸시, 브랜치 삭제는 상태 확인과 사용자의 명시적 승인 범위 안에서만 실행한다.

`/asak-git-publish` 호출만으로 원격 상태를 바꾸지 않는다. 대상 저장소, 포함 파일/전체 작업 트리 허용 여부, 브랜치 이름, 한글 커밋 제목, 원격 작업 브랜치 푸시·원격 `main` 반영·로컬/원격 브랜치 삭제 여부를 확인해 승인된 단계만 수행한다.

브랜치 이름에는 `agent/` 접두어를 사용하지 않는다. 작업 성격에 따라 `feat/`, `fix/`, `docs/`, `chore/` 중 하나를 쓰고, 뒤에는 소문자와 하이픈으로 작업 내용을 적는다. 예: `fix/kiosk-category-mock-contract`.

작업 트리가 더럽거나 현재 `main`을 안전하게 최신화할 수 없으면 stash·reset·rebase를 하지 말고 중단 사유를 보고한다. 저장소마다 다음 순서를 지킨다.

1. `main`으로 이동하고 `git pull --ff-only origin main`으로 최신화한다.
2. 기능별·레포별 작업 브랜치를 생성한다. 예: `git switch -c feat/admin-order-list`.
3. 승인된 파일만 `git diff`, `git diff --check`로 검토하고 명시적으로 stage한다. 프로젝트에 맞는 빌드 또는 테스트를 실행한다.
4. 에이전트 표기 없이 실제 변경을 설명하는 한글 커밋을 만든다. 예: `git commit -m "feat: admin 주문목록 조회 구현"`.
5. 작업 브랜치를 GitHub 원격에 푸시한다. `git push -u origin <branch>` 후 원격 추적 브랜치와 커밋 해시를 확인한다.
6. `main`으로 이동하고 `git pull --ff-only origin main`으로 다시 최신화한다.
7. 작업 브랜치를 `main`에 병합한다. 충돌이 발생하면 자동 해결하지 말고 중단한다.
8. 병합된 `main`을 GitHub 원격에 푸시한다. `git push origin main` 후 `HEAD == origin/main`과 대상 커밋 포함을 확인한다.
9. 병합된 로컬 작업 브랜치를 삭제한다. `git branch -d <branch>`. 현재 브랜치·`main`·보호 브랜치는 삭제하지 않는다.
10. GitHub 원격 작업 브랜치를 삭제한다. `git push origin --delete <branch>` 후 원격 참조가 사라졌는지 확인한다.

별도 승인 없이는 force push, rebase, reset, 기존 커밋 수정, 충돌 자동 해결, main 직접 커밋, 다른 저장소 변경 포함을 하지 않는다.

보고: 원격 URL, 브랜치·커밋 해시/한글 제목, stage 파일·검증, 원격 작업 브랜치 푸시와 원격 main 반영 여부, `HEAD == origin/main` 결과, 삭제/미삭제 로컬·원격 브랜치, 다음 작업.
