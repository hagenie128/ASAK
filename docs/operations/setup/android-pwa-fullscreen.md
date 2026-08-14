# Android 태블릿 PWA 전체화면 실행

> Status: `#current`
> 대상: `ASAK-Kiosk` Vite 앱 · Android Chrome · 세로형 태블릿

## 현재 프로젝트 기준

`ASAK-Kiosk/vite.config.js`에 다음 설정이 이미 들어 있습니다.

- 개발 서버: `host: "0.0.0.0"`, `port: 5173`
- PWA: `vite-plugin-pwa`
- 앱 이름: `ASAK Kiosk`
- 표시 모드: `fullscreen` 우선, `standalone` 대체
- 화면 방향: `portrait`
- 아이콘: `pwa-192x192.png`, `pwa-512x512.png`, `maskable-icon-512x512.png`

CRA의 `.env HOST`, `public/manifest.json`, 수동 service worker 등록 방식은 현재 프로젝트에 적용하지 않습니다. PWA manifest와 service worker는 Vite 플러그인이 생성합니다.

## 1. 개발 서버 실행

```powershell
cd C:\ASAK-workspace\ASAK-Kiosk
npm install
npm run dev
```

PC와 태블릿을 같은 네트워크에 연결하고, 태블릿에서 Vite의 Network 주소를 엽니다.

```text
http://<개발-PC-IP>:5173
```

IP는 고정값이 아닙니다. Windows에서는 `ipconfig`로 현재 IPv4 주소를 확인합니다.

## 2. PWA 아이콘 확인

아래 파일이 `ASAK-Kiosk/public/`에 있어야 합니다.

- `pwa-192x192.png`
- `pwa-512x512.png`
- `maskable-icon-512x512.png`

manifest의 선언 크기와 실제 PNG 크기가 다르면 Chrome 설치 검사를 통과하지 못할 수 있습니다.

## 3. 내부 HTTP 주소를 설치 대상으로 허용

PWA 설치와 service worker는 원칙적으로 HTTPS 또는 `localhost` 보안 컨텍스트가 필요합니다. 내부망 HTTP 주소로 시연할 때만 개발용 Chrome 플래그를 사용합니다.

```text
chrome://flags/#unsafely-treat-insecure-origin-as-secure
```

1. `Insecure origins treated as secure`를 `Enabled`로 바꿉니다.
2. 실제 접속 주소를 프로토콜과 포트까지 입력합니다.

```text
http://<개발-PC-IP>:5173
```

3. Chrome을 재시작하고 주소에 다시 접속합니다.
4. Chrome 메뉴에서 `앱 설치` 또는 `홈 화면에 추가`를 선택합니다.
5. 설치된 ASAK Kiosk 아이콘으로 실행합니다.

이 플래그는 개발·시연용입니다. 운영 배포는 HTTPS를 사용합니다.

## 4. 전체화면 확인

설치 앱을 실행한 뒤 다음을 확인합니다.

- 주소창이 보임: 일반 Chrome 탭 또는 단순 바로가기
- 주소창은 없고 시스템 상태 표시줄만 보임: `standalone`
- 주소창과 상태 표시줄이 모두 없음: `fullscreen`

Android 정책상 웹페이지가 사용자 입력 없이 Fullscreen API를 호출할 수는 없습니다. manifest 전체화면이 적용되지 않는 기기에서 추가 Fullscreen API를 사용한다면 최초 한 번의 터치가 필요합니다.

## 5. 변경 후 갱신

manifest, 아이콘, service worker 설정을 바꾼 뒤 이전 설치가 남아 있으면 다음 순서로 갱신합니다.

1. 설치된 ASAK Kiosk 앱을 삭제합니다.
2. Chrome 사이트 설정에서 해당 내부망 주소의 저장 데이터를 삭제합니다.
3. 개발 서버와 Chrome을 재시작합니다.
4. 다시 접속해 앱을 설치합니다.

`vite-plugin-pwa`의 `registerType: "autoUpdate"`가 새 service worker를 갱신하지만, manifest 식별자·아이콘·표시 모드 변경은 재설치가 더 확실합니다.

## 6. 운영 키오스크 한계

PWA만으로는 전원 부팅 후 자동 실행, 사용자의 앱 이탈 차단, 시스템 UI 영구 숨김을 보장하지 못합니다. 완전한 무인 키오스크 운영에는 Android Device Owner/Lock Task, 관리형 WebView 앱 또는 전용 키오스크 브라우저를 검토합니다.

## 관련 경로

- `ASAK-Kiosk/vite.config.js`
- `ASAK-Kiosk/src/main.jsx`
- [Windows 설치](install-windows.md)
- [첫 시작](getting-started.md)
