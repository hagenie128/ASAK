# 2026-08-11 재료 영양 분리 시드·마이그레이션

> **일일 기록:** [2026-08-11 daily](../../daily/이하진/2026-08-11.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-11
- 담당자: 이하진
- 저장소: `ASAK`
- 브랜치: `feat/nutrition-seed-split` → `main` (`b7dad73`)
- 관련 이슈/PR: Issue 없음
- 작업 유형: `feature` / `data`
- 구현 근거: `03a1656` · merge `b7dad73` · `HEAD == origin/main`
- Figma 기준: 해당 없음 (`Figma 미확인` — UI 작업 아님)
- 완료 판정: **시드·SQL·스크립트 Git 반영**. 실 DB 적용·적재 실행 결과 미확인.

## 2. 작업 목적

- 재료(ing)와 영양(ing_nutr/menu_nutr)을 분리한 시드와 마이그레이션을 재현 가능한 스크립트로 남긴다.
- PDF 기반 영양 컬럼 보강·뷰 갱신 경로를 `asak-data/scripts`에 고정한다.

## 3. 직접 구현 영역

커밋 `03a1656`에서 확인:

- 시드: `asak-data/seed-v3/ing_nutr.json` 추가, `ing.json` 제거·manifest 갱신, `menu_nutr`·`seed/ingredient`·`menu_nutrition` 갱신
- 마이그레이션 SQL: `20260811_split_ing_nutrition.sql`, `20260811_add_nutrition_pdf_columns.sql`, `20260811_update_views_ing_nutr.sql`
- 스크립트: `apply_ing_nutr_split.py`, `apply_nutrition_schema.py`, `apply_nutrition_pdf_260715.py`, `apply_views_ing_nutr.py`, `split_ing_seed_nutrition.py`, `generate_diverse_orders.py` 등
- 리포트 산출: `nutrition_pdf_260715_report.json`, `ing_names.txt`

## 4. 구현 로직 / 적용한 방식

- 시드 JSON 분리 → SQL 마이그레이션 → Python apply/load 순으로 로컬에서 재실행 가능하게 구성.
- 뷰 갱신 SQL을 별도 파일로 두어 스키마 변경과 조회 계층을 나눔.
- **주의:** 저장소에 스크립트가 있어도 실행 로그·DB 조회 없이는 “데이터 반영 완료”로 쓰지 않음.

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor (co-authored-by)
- 요청: 영양 분리 시드·마이그레이션·적재 스크립트 정리 및 깃반영
- AI 도움: 스크립트·시드 분리 초안
- 사람이 남긴 부분: DB 미적용을 완료와 분리해 기록

## 6. 발생 이슈

### 이슈 1 — 파일 반영 ≠ DB 반영

- 증상: migration/seed가 main에 있어도 운영·로컬 MySQL 상태는 모름.
- 해결: 워크로그·블로커에 미적용 명시.

## 7. 디버깅 기록

| 확인 항목 | 사실 | 다음 |
|---|---|---|
| 커밋 | `03a1656` / merge `b7dad73` | `asak-data/scripts` |
| 실DB | 미확인 | information_schema · 샘플 SELECT |

## 8. 이번 작업에서 배운 점

1. 영양 PDF·시드 분리 작업은 산출물(JSON/SQL/report)과 적용 증거를 짝으로 남겨야 한다.
2. 시드 구조 변경은 Admin/메뉴 nutrition 응답과 함께 대조할 항목이다.

## 9. 개선사항 / TODO

- [ ] 대상 DB에 split/PDF/뷰 SQL 적용 후 테이블·뷰 확인
- [ ] `load_seed_mysql` 등 적재 실행 로그 남기기
- [ ] Admin/Kiosk nutrition 필드와 시드 키 대조

## 10. 검증 내용

- Git 원격 포함·파일 트리 존재 확인.
- 스크립트 실행·DB 조회: 미실행.

## 11. 포트폴리오 요약

재료·영양 분리용 시드와 마이그레이션·적재 스크립트를 ASAK 데이터 트리에 고정하고 원격 main에 병합했다. DB 적용은 별도 검증으로 남겼다.

## 12. 연결된 기록

- [일일 2026-08-11](../../daily/이하진/2026-08-11.md)
- [관리자 메뉴·영양 API](2026-08-11-admin-menu-nutrition-api.md)
