---
name: asak-git-publish
description: "Use for approved ASAK branch creation, Korean commits, push, main merge, and merged branch cleanup."
---

# 깃반영

ASAK의 독립 저장소별 변경을 안전하게 원격 main까지 반영한다. 브랜치 생성, 한글 커밋, 푸시, main 병합, 브랜치 삭제는 상태 확인과 사용자의 명시적 승인 범위 안에서만 실행한다.

`/asak-git-publish` 호출만으로 원격 상태를 바꾸지 않는다. 대상 저장소, 포함 파일/전체 작업 트리 허용 여부, 브랜치 이름, 한글 커밋 제목, 푸시·main 병합·로컬/원격 브랜치 삭제 여부를 확인해 승인된 단계만 수행한다.

1. `AGENTS.md`, `git status --short --branch`, 현재 브랜치·추적 원격·`origin/main`·최근 커밋·원격 URL을 확인한다.
2. 승인된 파일만 `git diff`, `git diff --check`로 검토하고, 관련 없는 변경은 stage하지 않는다. 프로젝트에 맞는 빌드/테스트 결과도 확인한다.
3. 브랜치 생성은 승인됐을 때만 한다. stage 결과를 재확인하고 실제 변경을 설명하는 한글 제목으로 승인 파일만 commit한다.
4. push는 승인된 브랜치에만 하며 force push는 금지한다.
5. main 병합 전 최신 `origin/main`과 조상 관계·충돌 가능성을 점검한다. PR 또는 명시 승인된 로컬 병합만 사용하고 충돌이면 중단한다.
6. 브랜치 삭제 전 원격 main이 대상 커밋을 포함하는지 확인한다. local/remote 삭제를 각각 승인받고 main·보호·현재 브랜치는 삭제하지 않는다.

별도 승인 없이는 force push, rebase, reset, 기존 커밋 수정, 충돌 자동 해결, main 직접 커밋, 다른 저장소 변경 포함을 하지 않는다.

보고: 브랜치·커밋 해시/한글 제목, stage 파일·검증, push/main 반영 여부, 삭제/미삭제 브랜치, 다음 작업.
