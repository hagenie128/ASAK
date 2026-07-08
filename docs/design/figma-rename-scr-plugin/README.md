# SCR Frame Rename (kiosk_design)



`kiosk_design` Figma 파일의 Page 구조를 **무료 플랜 3페이지**(02 User Flow · 03 Kiosk · 04 Admin)에 맞추고, SCR 프레임 이름을 `SCR-XXX 화면명` 형식으로 일괄 정리하는 개발용 플러그인입니다.



| 항목 | 값 |

|------|-----|

| 플러그인 표시 이름 | **SCR Frame Rename (kiosk_design)** |

| 패키지 경로 | `docs/design/figma-rename-scr-plugin/` |

| 대상 | **모든 페이지**의 FRAME·COMPONENT (재귀 스캔) |

| 필요 환경 | **Figma Desktop 권장** — Web에서도 이름변경·이동 동작 (개발 플러그인은 Desktop에서 등록) |



---



## 목표 Page 구조 (무료 플랜 3페이지)

> **Figma Free: 페이지 최대 3개** — Notion 유료 권장 7페이지(00~06)는 아래 3페이지로 통합. 플러그인은 **이 3페이지만 생성**합니다.

| Page | SCR | 내용 |
|------|-----|------|
| **02. User Flow** | — | Cover·DS 토큰·고객·관리자 흐름·Prototype 링크·Archive 참고 (수동 배치) |
| **03. Kiosk Screens** | SCR-001~014, 020~021 | 키오스크 고객 + Day10 관리자(009~011) |
| **04. Admin Screens** | SCR-015~019 | 후반 관리자 (로그인·메뉴·결제·매출) |

유료 플랜 전환 시 00 Cover · 01 Design System · 05 Prototype · 06 Archive 분리 가능.

> 구버전 `📱 Customer` / `🛠 Admin` / `00~06` 페이지 프레임도 **자동으로** 03·04로 이동합니다.



### 03. Kiosk Screens 배치



```

SCR-001~008   고객 주문 흐름 (홈 → 완료)

SCR-009~011   관리자 (주문·품절) — 같은 Page

SCR-012~014   결제실패·타임아웃·접근성

SCR-020~021   영수증·멤버십 (없으면 플레이스홀더 생성)

```



Frame 이름 규칙: `SCR-001 홈` (`SCR-{ID} {화면명}`)



---



## 방법 1 — 매니페스트에서 가져오기 (권장)



### 1단계: 사전 준비



1. [Figma Desktop for Windows](https://www.figma.com/downloads/) 설치

2. Figma Desktop에서 **로그인**

3. **디자인 파일** [`kiosk_design`](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) 열기



### 2단계: 플러그인 등록 (최초 1회)



```

Figma → 플러그인 → 개발 → 매니페스트에서 플러그인 가져오기…

```



1. `C:\ASAK\docs\design\figma-rename-scr-plugin\manifest.json` 선택

2. **SCR Frame Rename (kiosk_design)** 등록 확인



### 3단계: 실행



```

Figma → 플러그인 → 개발 → SCR Frame Rename (kiosk_design)

```



또는 `Ctrl + /` → `SCR Frame Rename` 검색



### 4단계: 결과 확인



하단 알림 예시:



| 상황 | 알림 메시지 예시 |

|------|------------------|

| 정상 정리 | `이름 18 · 이동 19 · 생성 2 · SCR스킵 0` |

| 이미 정리됨 | `정리 완료 (변경 없음 · SCR 21개 확인)` |

| 미매칭 있음 | `이름 N · 이동 N … — 콘솔(Ctrl+Shift+I) 확인` (빨간색) |



**알림 필드 의미**



| 필드 | 의미 |

|------|------|

| **이름** | `SCR-XXX 화면명`으로 바뀐 프레임 수 |

| **이동** | 03·04 Page로 옮긴 프레임 수 |

| **생성** | SCR-020·021 플레이스홀더 생성 수 |

| **SCR스킵** | 이미 `SCR-001 …` 형식이라 건너뛴 수 |



상세 로그: `Figma → 플러그인 → 개발 → 콘솔 열기` (`Ctrl+Shift+I`)



### 실행 후 기대 화면 (무료 플랜 3페이지)



왼쪽 Page 탭:



```

02. User Flow        ← 흐름·참고 (수동 배치)

03. Kiosk Screens    ← SCR-001~014, 020~021 프레임

04. Admin Screens    ← SCR-015~019 프레임

```



`03. Kiosk Screens` 안 프레임 이름 예:



- `SCR-001 홈`

- `SCR-002 먹고가기 / 포장 선택`

- …

- `SCR-020 영수증 출력 여부 선택` (없었으면 점선 플레이스홀더)

- `SCR-021 포인트·쿠폰 적립` (없었으면 점선 플레이스홀더)



`04. Admin Screens` 안:



- `SCR-015 관리자 로그인` ~ `SCR-019 관리자 매출 요약`



구 `📱 Customer` / `🛠 Admin` / `Page 1` 페이지는 **비워지거나** 남아 있을 수 있습니다. 내용이 비었으면 수동 삭제하세요.



### 코드 수정 후 재등록



```

Figma → 플러그인 → 개발 → 개발 중인 플러그인 관리

```



1. **제거** → **매니페스트 재가져오기** → 재실행



---



## 방법 2 — 빠른 작업 (Quick Actions)



`Ctrl + /` → `SCR Frame Rename` 또는 `Run last plugin`



---



## 트러블슈팅

### 반응 없을 때 (클릭해도 알림·변화 없음)

| 확인 | 방법 |
|------|------|
| **즉시 알림** | 수정된 버전은 실행 직후 하단에 `플러그인 시작…` 알림이 떠야 합니다. 없으면 아래 순서대로 진행하세요. |
| **콘솔 먼저 열기** | `Figma → 플러그인 → 개발 → 콘솔 열기` 또는 **`Ctrl+Shift+I`** — 실행 **전에** 열어 두면 오류·로그를 바로 볼 수 있습니다. |
| **실행 중 상태** | 메뉴 `플러그인 → 개발` 에 **SCR Frame Rename** 이 “실행 중”으로 보이는지 확인합니다. 오래 걸리면 8초 뒤 `처리 중…` 알림이 추가로 뜹니다. |
| **매니페스트 재등록** | `플러그인 → 개발 → 개발 중인 플러그인 관리` → **제거** → **매니페스트에서 플러그인 가져오기** → `manifest.json` 다시 선택 → 재실행 |
| **Desktop 권장** | 개발 플러그인 등록은 **Figma Desktop**에서 하세요. 실행은 Web에서도 가능하나 Desktop이 안정적입니다. |
| **무료 플랜 페이지 한도 (3개)** | 아래 [3페이지 한도 수동 정리](#무료-플랜-3페이지-한도-수동-정리) 참고. 수정된 플러그인은 생성 실패 시 **기존 페이지 이름을 02/03/04로 바꾸고** 프레임 정리를 계속합니다. |
| **코드 반영** | `code.js` 수정 후에는 **재가져오기 없이** 같은 세션에서 다시 실행해도 되지만, 반응이 없으면 **제거 후 재가져오기**를 권장합니다. |

**정상 실행 시 알림 순서 (참고)**

1. `플러그인 시작…`
2. (잠시 후) `페이지 로드 완료 · 스캔 중…`
3. (완료 후) `이름 N · 이동 N · 생성 N …` 또는 `정리 완료 …`

### 실행했는데 이름·이동이 안 됨



| 원인 | 해결 |

|------|------|

| 구버전 플러그인 캐시 | **제거 → 매니페스트 재가져오기** |

| 이미 SCR 형식 | 정상 — 재실행 안전 |

| 이름이 표와 다름 | 콘솔 미매칭 목록 확인 후 수동 수정 |



### 구버전 Page 이름 (`📱 Customer` 등)



2026-07 이전에는 `📱 Customer` / `🛠 Admin` 구조를 썼습니다.  

**현재 버전**은 무료 플랜 **3페이지**(02·03·04) 구조를 맞추고, SCR ID 기준으로 **03·04**에 이동합니다.



### 무료 플랜 3페이지 한도 — 수동 정리



Figma Free(Starter)는 **페이지 최대 3개**입니다. `04. Admin Screens` 생성 오류가 났다면 이미 3페이지를 쓰고 있는 상태입니다.



**방법 A — 플러그인 재실행 (권장)**



수정된 플러그인은 다음 순서로 동작합니다:



1. `02. User Flow` / `03. Kiosk Screens` / `04. Admin Screens` 이름이 있으면 그대로 사용

2. 3개 미만이면 부족한 페이지만 생성 시도

3. **정확히 3개**이면 새로 만들지 않고 기존 페이지 이름을 02→03→04로 변경

   - `📱 Customer` → `03. Kiosk Screens`, `🛠 Admin` → `04. Admin Screens` 등 레거시명 우선

   - 그 외 `Page 1` 등은 순서대로 02·03·04에 매핑

4. 프레임 이름 변경·이동은 페이지 생성 실패와 **무관하게 계속** 진행



`code.js` 저장 후 플러그인을 다시 실행하세요.



**방법 B — 실행 전 수동 정리**



| 상황 | 조치 |

|------|------|

| 페이지 **3개 초과** | 불필요한 페이지 삭제 후 **3개만** 남기기 |

| 페이지 **정확히 3개** (이름이 Page 1 등) | 수동으로 이름 변경: `02. User Flow` · `03. Kiosk Screens` · `04. Admin Screens` |

| 키오스크/관리자만 있음 | `📱 Customer` → `03. Kiosk Screens`, `🛠 Admin` → `04. Admin Screens` 로 이름만 바꿔도 됨 |



수동 정리 후 플러그인을 실행하면 페이지 생성 없이 바로 SCR 프레임 정리가 됩니다.



---



## 동작 요약



1. `loadAllPagesAsync()` 후 **02·03·04 Page** 해석 (생성 / 이름변경 / 기존 사용 — 3페이지 한도 준수)

2. 모든 PAGE의 FRAME·COMPONENT **재귀 스캔** → `SCR-XXX 화면명` 변경

3. SCR ID 기준 **03. Kiosk Screens** / **04. Admin Screens** 로 이동 (대상 페이지 없으면 레거시·가용 페이지로 폴백)

4. SCR-020·021 없으면 **03. Kiosk Screens**(또는 가용 페이지)에 834×1194 플레이스홀더 생성

5. 구 `📱 Customer` / `🛠 Admin` / `Page 1` 에 있던 프레임도 동일 규칙 적용

6. `createPage` 실패 시 **중단하지 않음** — 경고 알림 후 이름변경·이동 계속



---



## 파일 구성



```

figma-rename-scr-plugin/

├── manifest.json

├── code.js

└── README.md

```



레거시: `docs/design/figma-rename-scr-plugin.js` (패키지 사용 권장)



---



## 관련 문서



- Notion: [Figma 가이드 + SCR×Figma](https://app.notion.com/p/39451ef04f0b81849dc7d81f8106b5ad)

- Git: [`SCR_FIGMA_CHECKLIST.md`](../SCR_FIGMA_CHECKLIST.md) · [`figma-links.template.json`](../figma-links.template.json)

- Design System frame: [`figma-create-ds-plugin`](../figma-create-ds-plugin/README.md) · [`kiosk-design-system.md`](../kiosk-design-system.md)

