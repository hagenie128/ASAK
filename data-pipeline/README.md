# ASAK Data Pipeline

> Status: **HISTORY**

## 폴더 역할

| 경로 | 역할 | 태그 |
|---|---|---|
| `phase1/` | 1차 크롤·가공 결과와 설명 | `HISTORY` |
| `phase1/output/` | 생성물 (gitignore) | `HISTORY` |
| `phase1/audit_20260812_v3/` | 최신 감사 스냅샷 | `REFERENCE` |
| `phase1/_archive/` | 이전 감사 v1·v2 | `HISTORY` |
| `phase1/db/` | phase1용 SQL 참고 | `REFERENCE` |

## 저장소 경계

- 파이프라인 코드·생성물은 여기
- 시드 정본: `../asak-data/seed/`
- 메뉴 이미지 원본·가공 소스: `../asak-data/images/menu/`
- 앱 전달 URL 정본: Cloudinary가 연결된 DB `media_asset.url`
- `seed`와 `seed-v3`를 합치지 않음

1차 수집 Python은 완료된 일회성 도구라 제거했습니다. 현재 데이터 정본은 `asak-data/seed/`이며, 이미지 파일은 `asak-data/images/menu/`에 재업로드 가능한 소스로 보관합니다. 실행 앱은 `menu.image_asset_id → media_asset.url → API imageUrl` 흐름으로 Cloudinary 이미지를 받습니다. 재수집이 필요하면 Git 이력에서 기존 파이프라인을 복원해 별도 검증합니다.
