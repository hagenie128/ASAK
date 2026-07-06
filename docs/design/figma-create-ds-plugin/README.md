# Create DS Candidates (kiosk_design)



`kiosk_design` Figma 파일의 **`02. User Flow`** 페이지에 디자인 시스템 **DS-01~07** 프레임 **7개**를 자동 생성하는 개발용 플러그인입니다.



| 항목 | 값 |

|------|-----|

| 플러그인 표시 이름 | **Create DS Candidates (kiosk_design)** |

| 패키지 경로 | `docs/design/figma-create-ds-plugin/` |

| 대상 페이지 | **02. User Flow** (레거시명 자동 인식·이름 변경) |

| 필요 환경 | **Figma Desktop 권장** |



---



## 생성되는 프레임 (7개 · 가로 배치 · 간격 80px)



| Figma frame | 구 이름 | 컨셉 | Notion Trend |

|-------------|---------|------|--------------|

| `DS-01 Fresh Greens` | Candidate A | 회의 green `#16A34A` · cream | 회의 팔레트 |

| `DS-02 Modern Minimal` | Candidate B | Charcoal + Electric Lime | Trend-3 |

| `DS-03 Trend Forward` | Candidate D | Deep Forest + Mint Glass | Trend-3/4 |

| `DS-04 A+C Trendy` | Candidate E | Sage gradient + terracotta | Trend-1/2 hybrid |

| `DS-05 Pink-Green` | Trend-1 | Vivid coral `#FF5C7A`→`#FF4D8D` + sage `#52D98A` | Trend-1 · SCR-001 Variables A |

| `DS-06 Blush Forest` | Trend-4 | Forest `#1B6B47` + blush + rose | Trend-4 · SCR-001 Variables B ⭐ |

| `DS-07 Pink-Lime Hybrid` | Hybrid B×T1 | B minimal charcoal+lime + Trend-1 coral CTA | B×Trend-1 · 7번째 비교 |



> **DS-01~04는 후보 A,B,D,E** (C Warm Bistro는 보관 — 후보 목록 제외), **DS-05/06은 Trend 비교 프레임** — A/E에 병합하지 않음. SCR-001에서 coral CTA vs blush+forest를 나란히 보려면 DS-05/06 + Variables A/B를 함께 사용. hex 정본: [color-swatches](../color-swatches.html)



레거시 `DS-1~4` · `DS Candidate A~E` · `DS Trend-1/4` · `DS Hybrid B×T1` 등 구 프레임명은 재실행 시 자동 삭제됩니다.



각 프레임(834×1194) 포함 요소:

- **Colors** — 8개 스와치 + hex 라벨

- **Typography** — Display~Caption 스케일 샘플

- **Buttons** — Primary / Secondary 버튼

- **SCR-001 홈 무드** — 미니 CTA 프리뷰 (DS-04·05/06에 hero·accent 뱃지)



색상 정본: [kiosk-design-system-index.md](../kiosk-design-system-index.md) · candidate A~E `.md` · `kiosk-tokens-candidate-*.css` · Trend hex [color-swatches.html](../color-swatches.html)



---



## 사전 조건



1. [kiosk_design](https://www.figma.com/design/iqaoVwFjFE6Zq1WpOVgjeG/kiosk_design) 파일 열기

2. **페이지 1개 이상** 존재 (`02. User Flow` 없어도 됨 — 레거시명 자동 변환)

3. Figma **무료 3페이지** 구조 권장: 02 User Flow · 03 Kiosk · 04 Admin  

   → [SCR Frame Rename 플러그인](../figma-rename-scr-plugin/README.md)을 먼저 실행하면 페이지 구조가 정리됩니다.



---



## 설치 (개발 플러그인)



### 1단계: 사전 준비



1. [Figma Desktop for Windows](https://www.figma.com/downloads/) 설치

2. Figma Desktop에서 **로그인**

3. **디자인 파일** `kiosk_design` 열기



### 2단계: 플러그인 등록 (최초 1회)



```

Figma → 플러그인 → 개발 → 매니페스트에서 플러그인 가져오기…

```



1. `C:\ASAK\docs\design\figma-create-ds-plugin\manifest.json` 선택

2. **Create DS Candidates (kiosk_design)** 등록 확인



### 3단계: 실행



```

Figma → 플러그인 → 개발 → Create DS Candidates (kiosk_design)

```



또는 `Ctrl + /` → `Create DS Candidates` 검색



### 4단계: 결과 확인



- `02. User Flow` 페이지에 위 **7개** 프레임이 가로로 배치됨 (간격 80px)

- 기존 동일 이름·레거시 이름 프레임이 있으면 **삭제 후 재생성**



### 코드 수정 후 재등록



```

Figma → 플러그인 → 개발 → 개발 중인 플러그인 관리

```



1. **제거** → **매니페스트 재가져오기** → 재실행



---



## 정상 실행 시 알림 순서



| 순서 | 알림 메시지 |

|------|-------------|

| 1 | `플러그인 시작…` |

| 2 | `페이지 로드 완료 · DS 후보 생성 중…` |

| 3 (8초 이상 걸릴 때) | `처리 중… 프레임 7개 생성에 20~45초 걸릴 수 있습니다…` |

| 4 (완료) | `DS 후보 7개 생성: DS-01 Fresh Greens · … · DS-07 Pink-Lime Hybrid` |



상세 로그: `Figma → 플러그인 → 개발 → 콘솔 열기` (`Ctrl+Shift+I`)



---



## 재실행 (Relaunch)



생성된 DS 프레임 선택 후 우클릭 → **플러그인** → **DS 후보 프레임 생성**



`manifest.json`의 `relaunchButtons.command`(`create`)와 `code.js`의 `setRelaunchData({ create: "" })`가 일치해야 합니다.



---



## 트러블슈팅



### 반응 없을 때



| 확인 | 방법 |

|------|------|

| **즉시 알림** | 실행 직후 `플러그인 시작…` 알림이 떠야 합니다 |

| **콘솔 먼저 열기** | `Ctrl+Shift+I` — 실행 **전에** 열어 두기 |

| **매니페스트 재등록** | 개발 중인 플러그인 **제거** → manifest 재가져오기 |

| **manifest `id`** | `"id": "3928475610293847"` 고정 — Relaunch에 필요 |



### 무료 플랜 3페이지 한도



이 플러그인은 **페이지를 새로 만들지 않습니다.** 기존 페이지 이름만 `02. User Flow`로 맞춥니다.



---



## 동작 요약



1. `loadAllPagesAsync()` 후 **02. User Flow** 페이지 해석

2. Inter 폰트 로드 (실패 시 Regular 폴백)

3. 기존 DS 프레임(레거시명·구 Candidate/Trend 프레임 포함) 삭제

4. DS-01 ~ DS-07 프레임 생성 후 뷰포트 이동

5. `setRelaunchData({ create: "" })` 로 Relaunch 등록



---



## 관련 문서



- [kiosk-design-system-index.md](../kiosk-design-system-index.md) — DS-01~07 매핑 인덱스

- [kiosk-design-system-comparison.md](../kiosk-design-system-comparison.md) — 비교표 · DS-05 vs DS-06

- [screen-design-meeting-opinion-template.md](../screen-design-meeting-opinion-template.md) — **초기 회의 DS Preview** (Step 4)

- [kiosk-design-system-candidate-A.md](../kiosk-design-system-candidate-A.md) … E

- [SCR Frame Rename 플러그인](../figma-rename-scr-plugin/README.md)

- Notion: [브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [화면 설계 초기 회의 템플릿](https://app.notion.com/p/39551ef04f0b8190b76ae4b48b8497ac)



## 주의



- 폰트는 Figma 기본 **Inter**로 렌더 (실제 구현은 Pretendard — CSS 토큰 참고)

- RGB는 Figma API 0–1 범위 (`hexToRgb` / `rgb` 헬퍼 사용)

- Variables Collection은 수동 생성 → Notion [Figma 태블릿 세로 Setup](https://app.notion.com/p/39451ef04f0b81c1b71accd381097699)

