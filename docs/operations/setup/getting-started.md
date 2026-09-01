# ASAK 시작 안내

> Status: **CURRENT**

## 1. 설치

처음 설치하는 PC는 [Windows 설치](install-windows.md)를 먼저 진행합니다.

필수 도구:

- Git
- Node.js
- Java 17
- Python 3
- MySQL

## 2. 워크스페이스

```text
C:\ASAK-workspace\
├─ ASAK
├─ ASAK-Kiosk
├─ ASAK-Admin
├─ ASAK-back
└─ ASAK-skill (선택)
```

여섯 폴더(및 workspace 루트)는 **독립 Git 저장소**입니다. 변경·커밋·푸시는 해당 저장소에서 수행합니다.

저장소 URL·브랜치·Issues·PR·클론 방법은 [Git 저장소 현황](git-repositories.md)을 봅니다.

## 3. 실행

### Kiosk

```powershell
cd C:\ASAK-workspace\ASAK-Kiosk
npm install
npm run dev
```

### Admin

```powershell
cd C:\ASAK-workspace\ASAK-Admin
npm install
npm run dev
```

### Backend

```powershell
cd C:\ASAK-workspace\ASAK-back
.\scripts\boot-run.ps1
```

또는 `.\gradlew bootRun`. `build` 삭제 실패·`clean` 오류가 나면 [Backend 트러블슈팅](troubleshooting-backend.md)을 봅니다.

## 4. 문서 확인 순서

1. [START_HERE](../../START_HERE.md)
2. [WBS](../../wiki/wbs.md)
3. [Product Bible Hub](../../product_bible/product-bible-hub.md)
4. 담당 앱의 `STRUCTURE_GUIDE.md`

## 5. 워크로그

```powershell
cd C:\ASAK-workspace\ASAK
python worklog/scripts/init_daily.py
python worklog/scripts/init_entry.py --slug 작업-주제
python worklog/scripts/sync_daily_to_notion.py --date today --dry-run
```

상세 규칙은 [worklog/README](../../../worklog/README.md)를 봅니다. Cursor에서는 설치된 `asak-signoff` 스킬을 사용합니다.

## 6. 태블릿 PWA

Android 태블릿 설치·전체화면은 [Android PWA 가이드](android-pwa-fullscreen.md)를 봅니다.

## 7. 실행 전 확인

- 각 저장소의 `.env`와 DB 연결 정보가 준비되었는지 확인
- `git status`로 기존 변경을 확인
- 기능 완료 전 Kiosk·Admin·Backend를 함께 검증
- 비밀키와 개인 토큰은 Git에 커밋하지 않음
