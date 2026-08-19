# Product Bible 구조 평탄화 근거

## 1. 대상과 기준

- 대상 저장소: `ASAK`
- 기준 커밋: `da24526`
- 작업일: 2026-08-14
- 범위: `docs/product_bible` 활성 Pack 01~12의 문서 경로와 해당 경로를 참조하는 로컬 문서

## 2. 확인한 자료

- `docs/product_bible/README.md`
- `docs/product_bible/product-bible-hub.md`
- Pack 01~12의 `README.md`와 활성 Markdown 문서 200개
- `docs/implementation-guide`, `docs/wiki`, `docs/ai-reports`, `docs/study`, `worklog`의 Product Bible 경로 참조
- `docs/product_bible/_archive`는 이력 보존 대상으로 확인만 하고 이동하지 않음

## 3. 변경 내용

- Pack 의미를 반복하던 `docs/<분류>/` 중간 계층을 제거함
- 실제 탐색에 필요한 기능 폴더(`cart`, `payment`, `screens`, `testing` 등)는 유지함
- Foundation 문서는 Pack 바로 아래로 옮기고 ADR만 `adr/`에 유지함
- Product Bible 허브, Pack README, 구현 가이드, WBS, 작업 기록의 경로를 새 위치로 갱신함
- `CANONICAL_SOURCE.md`의 정본 경로를 현재 실제 위치와 일치시킴

## 4. 변경 근거

기존 경로는 Pack 이름 아래에서 `docs/09-features`, `docs/10-qa`, `docs/11-ai-master`처럼 같은 의미를 반복해 탐색 깊이만 늘렸습니다. Pack 경계와 기능별 구분은 유지하면서 중복 계층만 제거했습니다.

## 5. 검증 결과

- 활성 Pack 아래 `docs/` 잔존 파일: 0개
- 이전 Pack 경로 문자열 잔존: 0건
- 변경 문서와 활성 Product Bible의 상대 Markdown 링크 검사: 깨진 링크 0건
- `git diff --check`: 통과
- IDE 문서 진단: 오류 없음

## 6. 남은 사항

- Product Bible 본문의 영문 문장은 이번 구조 정리 범위에서 번역하지 않음
- `_archive`의 과거 경로는 이력 보존을 위해 유지함
- 구조 변경은 아직 커밋하거나 원격에 반영하지 않음
- 전역 정리(삭제·병합·라벨링)는 [`asak-doc-sync-repo-cleanup.md`](asak-doc-sync-repo-cleanup.md) 참고

## 7. 수정하지 않은 범위

- 애플리케이션 소스코드
- DB와 seed
- Figma 및 DevCopilot 원격 데이터
- `docs/product_bible/_archive`
