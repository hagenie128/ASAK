# ASAK Phase 1 Pipeline

이 폴더는 `ASAK (A Salad A Kiosk)`의 1차 크롤링 데이터 파이프라인입니다.

포함 범위:

- 샐러디 메뉴/드레싱/이벤트 크롤링
- OCR 기반 이미지 파싱
- JSON 산출물 생성
- DB 스키마 문서

## 주요 파일

- `salady_scraper.py`: 메인 크롤러
- `image_ocr.py`: OCR 파서
- `run_phase1.py`: 1차 크롤링 일괄 실행
- `output/`: 생성 데이터
- `db/`: DB 설계 문서와 SQL

## 실행

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_phase1.py
```

개별 실행 예시:

```powershell
.\.venv\Scripts\python.exe run_store_menus.py
.\.venv\Scripts\python.exe run_dressings.py
.\.venv\Scripts\python.exe run_events.py
```
