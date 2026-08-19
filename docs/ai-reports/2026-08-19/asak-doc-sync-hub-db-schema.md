# ASAK 문서 동기화 — DevCopilot Hub DB 설계 (2026-08-19)

- 범위: 실제 운영 DB와 DevCopilot workspace 2의 운영 Base Table 스키마 정렬
- 제외: `backup_*`, `orders_backup_20260731` 백업 테이블과 `vw_*` 조회용 View
- 실제 DB의 데이터·테이블·컬럼: 변경하지 않음
- 인증 정보: 기록하지 않음

## 근거 및 방식

- 실제 DB: `information_schema`의 테이블·컬럼·PK·NULL·FK 정의를 읽기 전용으로 조회
- 로컬 정본: `docs/wiki/db-table-definition.md`, `ASAK-back/docs/아삭_mysql.sql`
- 원격 반영: DevCopilot MCP의 DB 스키마 카드만 비파괴적으로 생성·갱신 후 재조회

## 최종 확인 결과

| 항목 | 실제 운영 DB | DevCopilot Hub | 결과 |
|---|---:|---:|---|
| 운영 Base Table | 26 | 26 | 일치 |
| 누락/추가 테이블 | 0 | 0 | 일치 |
| 실제 DB에 있으나 Hub에 누락된 컬럼 | 0 | - | 일치 |
| 타입·NULL·PK·FK 불일치 | 0 | - | 일치 |

다음 실제 관계도 Hub에 반영되어 있음을 재조회로 확인했다.

- `media_asset.provider_id → common_code.id`
- `menu.image_asset_id → media_asset.id`
- `pay_method_cfg.image_asset_id → media_asset.id`
- 옵션·재료 관련 FK의 기존 영문 테이블명 참조를 실제 DB의 `ing`, `opt_group`, `opt_item`, `opt_policy` 기준으로 정렬

## 삭제 보류 항목

DevCopilot Hub의 `ing`에는 실제 운영 DB에 없는 레거시 영양 컬럼 6개가 남아 있다.

- `serving_g`
- `sugar_g`
- `fat_g`
- `saturated_fat_g`
- `carb_g`
- `sodium_mg`

이 항목은 Hub에서 컬럼을 **삭제**해야만 완전 동일해진다. 삭제는 복구가 어려운 변경이므로 이번 동기화에서는 보류했다. 삭제하려면 대상 6개를 확인한 뒤 별도 승인이 필요하다.

## 주의

- Hub의 `vw_*` View 카드와 실제 DB View는 표현식 결과 컬럼이라 물리 테이블의 FK와 1:1로 비교하지 않았다.
- 실제 DB의 백업 테이블은 운영 설계서에 포함하지 않았고 Hub에도 생성하지 않았다.
