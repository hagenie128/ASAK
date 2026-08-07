# 2026-08-07 MySQL 스키마 DDL·뷰 SQL·CORS 조정

> **템플릿:** [03-work-log-template.md](../../../docs/guides/03-work-log-template.md) · **일일:** [2026-08-07.md](../../daily/이하진/2026-08-07.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-07
- 담당자: 이하진
- 저장소: ASAK-back (`https://github.com/nayeon0828/ASAK-backend.git`)
- 브랜치: `chore/mysql-schema-cors` → 원격 `main` 병합 후 삭제
- 관련 이슈/PR: 없음
- 작업 유형: `chore` / `docs`

## 2. 작업 목적

- Migration SQL에 빠져 있던 FK를 CREATE 테이블명 기준으로 보완한다.
- 스키마 임포트 도구가 거부하는 비스키마 명령(존재 가드)을 제거하고 순수 DDL만 남긴다.
- 로컬 프론트 다포트 개발을 위해 CORS를 임시 완화한다.

## 3. 직접 구현 영역

- `docs/아삭_mysql.sql`: 테이블 24 + FK 39(누락분 포함). 참조 테이블명 `ing` / `opt_item` / `opt_group` / `opt_policy`.
- `docs/view.sql`: 뷰 정의 정리(대량 diff).
- `SecurityConfig.java`: `setAllowedOrigins(localhost:5173~5178)` → `setAllowedOriginPatterns(List.of("*"))`.

## 4. 구현 로직 / 적용한 방식

- 원본 FK 목록의 `ingredient`/`option_*` 이름은 실제 CREATE 테이블명으로 매핑.
- ERD 임포트 오류 메시지에 맞춰 `SET`/`PREPARE`/`information_schema` 가드 제거.
- SQL 파일 반영 ≠ DB 적용으로 분리 기록.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- 요청: 누락 FK 반영 DDL, 스키마-only SQL, 깃반영.
- 그대로 사용: FK 목록 대조 결과, DDL 초안.
- 수정해서 사용: `fk_payment_status_id` 컬럼 오타(`status_id`), 테이블명 매핑.

## 6. 발생 이슈

- 이슈 1: 존재 가드 SQL이 “비스키마 명령”으로 임포트 거부 → 순수 DDL로 재작성.
- 이슈 2: 초안 DDL에서 payment status FK 컬럼 오타 → `status_id`로 수정.

## 7. 디버깅 기록

- 실제 MySQL 오류 로그는 없음(파일·테스트 수준).
- DB 미적용 상태에서 FK 실패 여부는 미확인.

## 8. 테스트 / 검증

- 실행: `.\gradlew.bat test` 성공(커밋 전).
- 미실행: MySQL에 DDL 적용, FK/데이터 정합 조회, 브라우저 CORS preflight, 운영 origin 제한 복원.

## 9. 커밋과 원격

- `2bb235d` chore: MySQL 스키마 DDL 정리와 CORS 허용 범위 조정
- merge `792f84d` → `main` == `origin/main`
- 작업 브랜치 로컬·원격 삭제 완료

## 10. 남은 위험

- CORS `*`는 개발 편의. 배포 전 화이트리스트 복원 필요.
- `view.sql` 대량 변경의 뷰 동작은 DB에서 미검증.
- 기존 DB에 이미 다른 제약/데이터가 있으면 ALTER 실패 가능.

## 11. 포트폴리오 요약

- 백엔드 스키마 문서의 FK 누락을 정리하고, 개발용 CORS와 함께 원격 main에 반영했다. DB 실적용은 별도 검증 과제다.

## 12. 다음 작업

- 스테이징/로컬 MySQL에 DDL 적용 후 FK 목록 확인.
- CORS 복원 범위 팀 합의.
