# 알레르기 정합성 문서 동기화

- 날짜: 2026-08-12
- 범위: `allergy_260715.csv`의 `SALADY` 우선 기준, `ing_allergen` seed 및 라이브 DB
- 상태: 부분 구현됨

## 확인 근거

| 구간 | 근거 |
| --- | --- |
| Source of truth | `asak-data/scripts/input/allergy_260715.csv` |
| Seed | `asak-data/seed-v3/ing_allergen.json`, `manifest.json` |
| DB | Approved high-confidence links were queried after insertion |
| Detail API | `ASAK-back/src/main/resources/mappers/UserMenuMapper.xml` |
| Kiosk screen | `ASAK-Kiosk/src/pages/kiosk/MenuDetailPage.jsx` |

## 반영 사실

- 고신뢰 재료-알레르기 연결 11건을 10개 재료에 대해 seed와 라이브 DB에 추가했다.
- seed `ing_allergen` 수를 108에서 119로 갱신했다.
- 기존 36개 메뉴 체크리스트를 재계산해 10개 메뉴가 해결되고 26건이 남은 것을 확인했다.
- 삭제 후보는 적용하지 않았다.

## 고객 화면 상태

DB 정합성 수정과 고객 화면 표시는 별도 단계다.

- `AllergenAccordion.jsx` exists.
- `MenuDetailPage.jsx` does not render it.
- User menu detail DTO and mapper do not return `allergens`.

따라서 현재 상태는 **DB 정합성 부분 구현됨 / 키오스크 고객 알레르기 표시는 미연결**이다.

## 검증

| 검증 | 결과 |
| --- | --- |
| 승인한 11개 DB 연결 존재 | 통과 |
| 승인한 11개 seed 연결 존재 | 통과 |
| seed 연결 중복 | 0건 |
| 라이브 체크리스트 | 36건에서 26건 |
| API 응답 및 브라우저 표시 | 미검증·미연결 |

## 결정 필요

1. 공유 재료 삭제 후보 6개를 공식표와 영향 메뉴 기준으로 검토할 담당자 지정
2. SCR-004에서 알레르기 없음 상태를 숨김 또는 안내 문구 중 무엇으로 표시할지 결정
3. API 계약 `allergens: string[]` 추가 승인
