# 2026-08-07 MySQL 스키마 DDL·뷰 SQL·CORS 조정

> **일일 기록:** [2026-08-07 daily](../../daily/이하진/2026-08-07.md)
> **같은 날 문서 작업:** [WBS 통합·공부 경로·RTOS](2026-08-07-wbs-study-rtos-docs.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-07
- 담당자: 이하진
- 저장소: `ASAK-back`
- 브랜치: `chore/mysql-schema-cors` → `main` merge (`792f84d` 구간)
- 관련 이슈/PR: MySQL 스키마 DDL · 뷰 SQL · CORS 개발 허용 (Issue 번호 미기재)
- 작업 유형: `chore` / `docs`
- 구현 근거: `2bb235d` (작업 커밋) · merge `792f84d`
- Figma 기준: UI 작업 아님. `Figma 미확인`(해당 없음).
- 완료 판정: DDL/뷰/CORS **파일·코드 반영** 확인. **실 MySQL 적용·브라우저 CORS·운영 origin 제한은 미검증.**

## 2. 작업 목적

- ERD/스키마 도구와 문서용으로 쓸 수 있게, 누락 FK를 포함한 **순수 MySQL DDL**을 `docs/아삭_mysql.sql`로 정리한다.
- 매출·주문 등 조회용 `docs/view.sql`을 스키마와 맞춰 정리한다.
- 로컬 프론트 연동 편의를 위해 `SecurityConfig` CORS를 `allowedOriginPatterns("*")`로 임시 개방한다.
- 존재 가드(`SET`/`PREPARE`) 없이 CREATE/ALTER만 남겨 스키마 임포트 거부 상황을 피한다.

## 3. 직접 구현 영역

Git 커밋 `2bb235d`로 다음을 확인했다.

- **스키마 DDL:** `docs/아삭_mysql.sql` 추가. 테이블 CREATE 기준 실제 이름(`ing`, `opt_item`, `opt_group`, `opt_policy` 등)에 맞춘 FK를 포함했다.
- **뷰 SQL:** `docs/view.sql` 정리(대량 갱신).
- **CORS:** `src/main/java/com/asak/common/config/SecurityConfig.java`에서 origin 패턴 `*` 허용.

통계: 3 files changed, 916 insertions(+), 1003 deletions(-).

## 4. 구현 로직 / 적용한 방식

- **정본 대조:** 실제 CREATE 테이블명 ↔ FK 참조명을 맞춰 “문서상 이름”과 “DDL 이름”이 어긋나지 않게 했다.
- **DDL 형태:** 존재 여부 가드/동적 SQL은 스키마 임포트 도구가 거부할 수 있어 제거하고, CREATE TABLE + ALTER TABLE … ADD CONSTRAINT 형태만 남겼다.
- **CORS:** 개발 중 다양한 로컬 포트를 허용하려고 `allowedOriginPatterns("*")`를 택했다. 운영 화이트리스트 복원은 별도 작업이다.
- **검증 경계:** `gradlew test` 성공은 커밋 전 확인. 실제 DB에 DDL을 적용했는지, 브라우저에서 CORS preflight가 통과하는지는 이 기록 범위 밖이다.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 어떤 질문/요청을 했는지: 누락 FK 목록 대조, 순수 DDL 재작성, CORS 설정 위치 확인, 깃반영 절차.
- AI가 도움 준 내용: FK 후보·DDL 초안·SecurityConfig 수정안.
- 그대로 사용한 부분: 테이블명·컬럼명 evidence에 맞는 제약 이름 정리.
- 수정해서 사용한 부분: 존재 가드 제거, `status_id` 등 실제 컬럼명 정합, 운영 CORS 미완 고지.

## 6. 발생 이슈

### 이슈 1 — 존재 가드 SQL이 스키마 임포트에 거부됨

- 증상: `SET`/`PREPARE` 기반 “있으면 스킵” 구문을 넣으면 도구/임포트 경로에서 실패했다.
- 원인: 순수 DDL만 받는 경로와 운영 마이그레이션 스크립트 요구가 달랐다.
- 해결: 가드를 제거하고 CREATE/ALTER만 유지. 적용 전 백업·환경 분리는 운영자가 수행해야 한다.

### 이슈 2 — CORS `*`는 개발 편의이지 운영 완료가 아님

- 증상: 모든 origin 허용은 보안상 운영에 부적합하다.
- 원인: 로컬 Admin/Kiosk 포트를 빠르게 붙이려는 임시 선택.
- 해결: 코드에는 반영하되, 워크로그·블로커에 **운영 제한 재설정 필요**를 명시했다.

### 이슈 3 — SQL 파일 반영 ≠ DB 반영

- 증상: 저장소에 DDL이 있어도 information_schema에 FK/뷰가 생겼다고 볼 수 없다.
- 원인: 실제 MySQL 적용·조회를 이 세션에서 하지 않았다.
- 해결: 완료 판정을 파일 반영으로 제한하고 DB 적용을 TODO로 남겼다.

## 7. 디버깅 기록

| 확인 항목 | 이번에 확인한 사실 | 다음에 먼저 볼 곳 |
|---|---|---|
| 커밋 | `2bb235d` · merge `792f84d` | `ASAK-back` `git log` |
| DDL 파일 | `docs/아삭_mysql.sql` 존재·FK 포함 | 해당 파일 · ERD |
| 뷰 | `docs/view.sql` 대량 정리 | 뷰 정의 ↔ 앱 조회 |
| CORS | `SecurityConfig` `allowedOriginPatterns("*")` | SecurityConfig · 브라우저 preflight |
| 테스트 | 커밋 전 `gradlew test` 성공 이력 | `.\gradlew.bat test` 재실행 |
| 실DB | 미적용 | `information_schema` FK/뷰 조회 |

## 8. 이번 작업에서 배운 점

1. 스키마 문서는 “읽기 좋은 설명”과 “임포트 가능한 DDL”을 분리해야 한다. 가드가 오히려 임포트를 막을 수 있다.
2. 테이블 alias/문서 이름과 실제 CREATE 이름이 다르면 FK를 아무리 써도 적용이 실패한다.
3. CORS 완화는 연동 속도를 올리지만, 워크로그에 운영 복원 TODO를 남기지 않으면 그대로 잊된다.
4. SQL 커밋만으로 DB 상태를 주장하면 안 된다. 적용 로그·information_schema가 필요하다.

## 9. 개선사항 / TODO

- [ ] 대상 MySQL에 `아삭_mysql.sql` / `view.sql` 적용 후 FK·뷰 존재 확인
- [ ] CORS를 로컬 origin 화이트리스트로 되돌릴지 팀 합의
- [ ] 결제/주문 E2E 전에 스키마·뷰가 앱 쿼리와 맞는지 대조
- [ ] 운영/스테이징과 로컬 DDL 차이 문서화

## 10. 검증 내용

- 실행한 명령어:
  - `git show --stat 2bb235d`
  - 커밋 전 `.\gradlew.bat test` (성공 이력)
- 테스트한 시나리오:
  - DDL/뷰/SecurityConfig 파일 변경 범위 확인
  - 실제 DB 임포트·브라우저 CORS·운영 배포는 **미실행**
- 확인 결과:
  - 원격 `ASAK-back` main에 스키마·뷰·CORS 변경이 포함됐다.
  - DB 적용·CORS 실측은 미완이므로 기능 완료로 기록하지 않는다.

## 11. 포트폴리오용 요약

ASAK-back에 누락 FK를 포함한 MySQL 스키마 DDL과 뷰 SQL을 정리하고, 로컬 연동용 CORS 임시 개방을 반영했다. 테스트 스위트는 통과했지만 실DB 적용과 운영 CORS 복원은 명시적으로 미검증으로 남겼다.

## 12. 첨부하면 좋은 자료

- 일일: [2026-08-07 daily](../../daily/이하진/2026-08-07.md)
- 스키마: `ASAK-back/docs/아삭_mysql.sql`
- 뷰: `ASAK-back/docs/view.sql`
- CORS: `ASAK-back/src/main/java/com/asak/common/config/SecurityConfig.java`
- 커밋: `2bb235d` · merge `792f84d`
