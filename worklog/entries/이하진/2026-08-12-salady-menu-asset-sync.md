# 2026-08-12 샐러디 메뉴·에셋 동기화

> **일일 기록:** [2026-08-12 daily](../../daily/이하진/2026-08-12.md)

---

## 1. 기본 정보

- 작업 날짜: 2026-08-12
- 담당자: 이하진
- 저장소: `ASAK`, `ASAK-Kiosk`
- 브랜치:
  - ASAK: `feat/salady-menu-seed-sync` → `main` (`eda7b68`)
  - ASAK-Kiosk: `chore/kiosk-salady-menu-assets` → `main` (`b8c190f`)
- 관련 이슈/PR: Issue 없음
- 작업 유형: `feature` / `data` / `chore`
- Figma 기준: 해당 없음 (`Figma 미확인` — 정적 에셋·데이터 작업)
- 완료 판정: **seed·스크립트·Kiosk public 에셋·원격 main 반영 + DB menu 58·이름 중복 0 조회 확인.** Kiosk 빌드·UI·알레르기 체크리스트 자동 적용은 미완.

## 2. 작업 목적

- `salady_menu_merged_20260812.csv`(40메뉴)를 seed-v3·MySQL 정본으로 반영한다.
- 메뉴 이름 중복을 dedupe하고(92→58), 삭제된 menu id에 해당하는 이미지를 제거한다.
- Kiosk `public/assets`의 menu·재료 photo/icon을 DB와 맞추고 PNG 배경·여백을 정리한다.

## 3. 직접 구현 영역

### ASAK (`4dc3677`)

- 스크립트: `apply_salady_menu_merged_20260812.py`, `apply_nutrition_allergy_csv_260715.py`, `dedupe_menus_seed_v3.py`, `trim_kiosk_png_assets.py`, media asset 마이그레이션·apply 스크립트
- input: `salady_menu_merged_20260812.csv`, `nutrition_260715.csv`, `allergy_260715.csv`
- output: dedupe/salady/csv 리포트 JSON·SQL, `allergy_fix_checklist_live38.*`
- seed-v3: `menu.json`, `menu_nutr.json`, `menu_ing.json`, `menu_tag.json`, `menu_opt_policy.json`, `ing*.json`, `tag.json`, `manifest.json`
- 이미지: `asak-data/images/menu/` 중 dedupe remove_id 34건 삭제
- scraper: `salady_scraper.py` 설명 셀렉터 보강

### ASAK-Kiosk (`47f5d90`)

- `public/assets/menu/` — 58 png (DB 일치), remove_id 34 png 삭제, 10768~10775 추가
- `public/assets/ingredients/photos/` — jpg→png, 배경 제거·트림 반영
- `public/assets/ingredients/icons/9817.svg`, `photos/9816.png`, `catalog.json`

## 4. 구현 로직 / 데이터 흐름

```text
salady_menu_merged_20260812.csv
  → apply_salady_menu_merged_20260812.py (--apply-db)
  → seed-v3 JSON + MySQL menu/menu_nutr/menu_ing/menu_tag/menu_opt_policy/ing*

dedupe_menus_seed_v3.py (--apply-db)
  → 동명 메뉴 34쌍 remove → keep 이관 (order_item 포함)
  → menu 92 → 58

trim_kiosk_png_assets.py
  → public/assets menu·ingredients/photos PNG 배경 제거·크롭
  → 원본 백업 public/assets/.bak/20260812T123811Z/ (Git 미포함)

orphan 정리
  → DB menu id 집합 vs public/dist/asak-data/images/menu 파일 id 비교
  → remove_id 34건 파일 삭제
```

## 5. AI 도움 영역

- 사용한 AI 도구: Cursor
- AI 도움: CSV 갭 분석, 스크립트 작성·확장, dedupe 규칙 적용, PNG 처리, orphan 삭제, 깃반영 절차
- 사람이 남긴 부분: 깃반영 제외 범위(Cloudinary, .bak, audit), DB/에셋 건수 재확인

## 6. 발생 이슈

### 이슈 1 — dist와 public 불일치

- 증상: `dist/assets/menu` 50개, DB 58개 — 10768~10775 8건 누락
- 조치: dist는 gitignore. **빌드로 재생성 필요.** 퇴근 시점 미해결.

### 이슈 2 — 알레르기 체크리스트

- 증상: `allergy_fix_checklist_live38` 36건 리포트만 존재
- 조치: **자동 apply 미실행.** 내일 범위 합의 필요.

## 7. 디버깅 / 확인 기록

| 확인 항목 | 사실 | 시점 |
|---|---|---|
| MySQL `menu` | 58 | 퇴근 SELECT |
| MySQL `menu_nutr` | 58 | 퇴근 SELECT |
| MySQL `ing` | 92 | 퇴근 SELECT |
| menu 이름 중복 | 0건 | 퇴근 SELECT |
| Kiosk public menu png | 58, orphan 0 | 퇴근 파일·DB 비교 |
| Kiosk public ing photo png | 56 | 퇴근 파일 count |
| dedupe remove_id | 34 | `dedupe_menus_seed_v3_report.json` |
| ASAK `HEAD == origin/main` | `eda7b68` | 깃반영 후 |
| ASAK-Kiosk `HEAD == origin/main` | `b8c190f` | 깃반영 후 |

## 8. 검증 내용

### 실행한 검증

- Python 스크립트 `--apply-db` (세션 중): nutrition/allergy CSV, salady merged, dedupe
- CSV vs DB 리포트: missing_menu 0, nutr/allergy diff 0 (세션 중)
- PNG trim 148건 (세션 중)
- 퇴근 시 MySQL SELECT, Kiosk public 에셋 건수·orphan 확인
- Git 원격 main push 및 `HEAD == origin/main` 확인

### 미검증

- `npm run build` / `npm test`
- Kiosk 브라우저에서 메뉴·옵션 이미지 표시
- Admin 메뉴 API와 seed 필드 대조
- `allergy_fix_checklist_live38` 자동 적용
- Figma Screen 대조

## 9. 제외·미커밋 항목

| 항목 | 저장소 | 사유 |
|---|---|---|
| Cloudinary deps, `.env.example` | ASAK-Kiosk | 별도 작업 |
| `public/assets/.bak/` | ASAK-Kiosk | 백업, Git 제외 |
| `audit_20260812*` | ASAK | 임시 audit |
| `.env.example` | ASAK-back | 범위 외 |
| worklog 본 파일 | ASAK | 퇴근 기록만 로컬 |

## 10. 포트폴리오 요약

샐러디 공식 CSV를 seed·DB·Kiosk 정적 에셋까지 한 흐름으로 맞추고, 중복 메뉴 dedupe와 orphan 이미지 정리까지 반영했다. UI·dist·알레르기 잔여 건은 다음 검증으로 남겼다.

## 11. 연결된 기록

- AI signoff: [`docs/ai-reports/2026-08-12/asak-signoff-salady-menu-asset-sync.md`](../../../../docs/ai-reports/2026-08-12/asak-signoff-salady-menu-asset-sync.md) (워크스페이스 루트)
- dedupe 리포트: `asak-data/scripts/output/dedupe_menus_seed_v3_report.json`
- merged 리포트: `asak-data/scripts/output/salady_menu_merged_20260812_report.json`
