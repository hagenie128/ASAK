# Android 태블릿 PWA 전체화면 실행

> Status: **CURRENT**
> 대상: `ASAK-Kiosk` · `ASAK-Admin` · Android Chrome · 태블릿 시연

키오스크와 관리자 모두 `vite-plugin-pwa`로 설치형 앱처럼 실행합니다. CRA의 `public/manifest.json` / 수동 service worker 등록 방식은 쓰지 않습니다.

## 앱별 현재 설정

| 항목 | ASAK-Kiosk | ASAK-Admin |
| --- | --- | --- |
| 설정 파일 | `ASAK-Kiosk/vite.config.js` | `ASAK-Admin/vite.config.js` |
| 개발 포트 | `5173` | `5174` |
| host | `0.0.0.0` | `0.0.0.0` |
| 앱 이름 | `ASAK Kiosk` | `ASAK Admin` |
| manifest id | `/asak-kiosk` | `/asak-admin` |
| display | `fullscreen` (`standalone` 대체) | 동일 |
| orientation | `portrait` | `landscape` |
| 아이콘 | `public/pwa-*.png`, `maskable-icon-512x512.png` | 동일 파일명 |
| 전체화면 코드 | `src/entries/kiosk.jsx` | `AdminStartGate` · `LoginPage` · `utils/fullscreen.js` |

`registerType: "autoUpdate"`는 두 앱 모두 동일합니다.

## 1. 개발 서버 실행

### 키오스크 (세로)

```powershell
cd C:\ASAK-workspace\ASAK-Kiosk
npm install
npm run dev
```

태블릿 접속: `http://<개발-PC-IP>:5173`

### 관리자 (가로)

```powershell
cd C:\ASAK-workspace\ASAK-Admin
npm install
npm run dev
```

태블릿 접속: `http://<개발-PC-IP>:5174`

PC와 태블릿을 같은 네트워크에 연결합니다. IP는 고정값이 아니며 Windows에서는 `ipconfig`로 IPv4를 확인합니다.

## 2. PWA 아이콘 확인

각 앱의 `public/`에 아래 파일이 있어야 합니다.

- `pwa-192x192.png`
- `pwa-512x512.png`
- `maskable-icon-512x512.png`

manifest 선언 크기와 실제 PNG 크기가 다르면 Chrome 설치 검사를 통과하지 못할 수 있습니다.

## 3. 내부 HTTP 주소를 설치 대상으로 허용

PWA 설치와 service worker는 원칙적으로 HTTPS 또는 `localhost` 보안 컨텍스트가 필요합니다. 내부망 HTTP로 시연할 때만 개발용 Chrome 플래그를 사용합니다.

```text
chrome://flags/#unsafely-treat-insecure-origin-as-secure
```

1. `Insecure origins treated as secure`를 `Enabled`로 바꿉니다.
2. 실제 접속 주소를 프로토콜과 포트까지 입력합니다.

```text
http://<개발-PC-IP>:5173
http://<개발-PC-IP>:5174
```

3. Chrome을 재시작하고 주소에 다시 접속합니다.
4. Chrome 메뉴에서 `앱 설치` 또는 `홈 화면에 추가`를 선택합니다.
5. 설치된 ASAK Kiosk / ASAK Admin 아이콘으로 실행합니다.

이 플래그는 개발·시연용입니다. 운영 배포는 HTTPS를 사용합니다.

## 4. 전체화면 확인

설치 앱을 실행한 뒤 다음을 확인합니다.

- 주소창이 보임: 일반 Chrome 탭 또는 단순 바로가기
- 주소창은 없고 시스템 상태 표시줄만 보임: `standalone`
- 주소창과 상태 표시줄이 모두 없음: `fullscreen`

### 키오스크 추가 동작

`src/entries/kiosk.jsx`는 설치된 PWA에서 첫 터치/키 입력 시 `requestFullscreen`과 `portrait` orientation lock을 시도합니다. 실패해도 주문 흐름은 유지됩니다.

### 관리자 추가 동작

`AdminStartGate`의 「시작하기」와 `LoginPage` 로그인 성공 시 `utils/fullscreen.js`의 `requestAppFullscreen()`이 `landscape` lock을 시도합니다. Fullscreen API는 사용자 제스처 안에서만 호출됩니다.

## 5. 변경 후 갱신

manifest, 아이콘, service worker 설정을 바꾼 뒤 이전 설치가 남아 있으면 다음 순서로 갱신합니다.

1. 설치된 ASAK 앱을 삭제합니다.
2. Chrome 사이트 설정에서 해당 내부망 주소의 저장 데이터를 삭제합니다.
3. 개발 서버와 Chrome을 재시작합니다.
4. 다시 접속해 앱을 설치합니다.

`registerType: "autoUpdate"`가 새 service worker를 갱신하지만, manifest 식별자·아이콘·표시 모드 변경은 재설치가 더 확실합니다.

## 6. 운영 키오스크 한계

PWA만으로는 전원 부팅 후 자동 실행, 사용자의 앱 이탈 차단, 시스템 UI 영구 숨김을 보장하지 못합니다. 완전한 무인 키오스크 운영에는 Android Device Owner/Lock Task, 관리형 WebView 앱 또는 전용 키오스크 브라우저를 검토합니다.

## 관련 경로

- `ASAK-Kiosk/vite.config.js`
- `ASAK-Kiosk/src/entries/kiosk.jsx`
- `ASAK-Kiosk/README.md` § PWA
- `ASAK-Admin/vite.config.js`
- `ASAK-Admin/src/utils/fullscreen.js`
- `ASAK-Admin/src/components/admin/AdminStartGate.jsx`
- `ASAK-Admin/README.md` § PWA
- [Windows 설치](install-windows.md)
- [첫 시작](getting-started.md)
