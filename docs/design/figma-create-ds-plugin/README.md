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



각 프레임(834×**2400**) 포함 요소:

- **Header (컴팩트)** — 프레임명 + subtitle + **4색 미니 dot** + **타이포 2샘플** 인라인
- **Components** — 키오스크·어드민 **시각적 UI 프리뷰** (2열 그리드 + 전폭 행 혼합 · Figma API 생성 · 외부 import 없음)
  - **Home hero strip (SCR-001)** — 브랜드명 + 태그라인 + 미니 CTA 「주문 시작」 + 포케볼 사진 배경(72% tint overlay)
  - **Category tab bar** — 메뉴 · 샐러드 · 음료 (활성 탭 1개)
  - **Menu photo card** — Salady 메뉴 실사(포케볼·연어 랩) + 18px 제목·우측 가격 + 칼로리 캡션 + NEW/HOT pill 뱃지 + 카드 drop shadow
  - **Menu card horizontal** — 연어 랩 썸네일 + 가격 · chevron (2열 좌)
  - **Menu card sold-out** — 동일 썸네일 dim + 품절 chip + 코너 SOLD chip (2열 우)
  - **Option chip row** — 소·보통·많이 3 pill (선택=채움 primary / 비선택=아웃라인)
  - **Option radio group (SCR-004)** — Regular / Large / Extra 단일 선택 + 가격 delta (2열 좌)
  - **Quantity stepper** — − 1 + (2열 우)
  - **List group ×2** — 원형 아이콘 bg + 제목·부제목 + chevron › + 구분선
  - **Payment method row (SCR-007)** — 카드 · 간편결제 아이콘 placeholder (2열 좌)
  - **Success toast** — ✓ 아이콘 + 「주문이 접수되었습니다」 (2열 우)
  - **Bottom sticky CTA bar** — 상단 그림자 + 합계·큰 가격 + 채움 결제 버튼

> 컴포넌트 섹션이 프레임 대부분을 차지 — Colors/Typography는 헤더 미니 dot·인라인 샘플로 압축, **visual component preview**로 DS를 한눈에 비교합니다.

DS별 시각 차별화: DS-01 rounded·green chips / DS-02 8px·charcoal·lime accent / DS-03 mint glass / DS-04 terra badge·24px warm / DS-05 coral·pink·yellow pop / DS-06 blush card surface·rose·forest / DS-07 charcoal·lime outline chip·coral CTA — **메뉴 사진은 DS 공통**(Salady 레퍼런스 2종)으로 토큰·컴포넌트 차이에 집중



### 메뉴 사진 (Salady 레퍼런스)



플러그인은 **오프라인 동작**을 위해 Salady 메뉴 PNG 2종을 `code.js`에 base64로 embed합니다 (`networkAccess: none` — CDN fetch 미사용).



| 키 | menu id | 메뉴명 | 용도 |

|----|---------|--------|------|

| `poke_roast_pork` | 2534 | 로스트삼겹 포케볼 | Menu photo card · Home hero strip 배경 |

| `salmon_wrap` | 4842 | 그라브락스 연어 랩 | Horizontal card · Sold-out thumb |



- **원본 경로:** `asak-data/images/menu/{id}.png` (data-pipeline / `menu.json` `image_url`: `/assets/menu/{id}.png`)

- **출처:** Salady 공식 메뉴 이미지 (레퍼런스 데이터 · 상업 사용 시 Salady/브랜드 가이드 확인)

- **재생성:** 이미지 변경 시 아래 스크립트 실행 후 Figma에서 플러그인 재등록



```powershell

python docs/design/figma-create-ds-plugin/embed_menu_images.py

```



> `code.js`가 ~0.6MB로 커집니다. Git에는 embed 결과를 포함합니다. 원본 PNG는 `asak-data/images/menu/`에만 두고 플러그인 폴더에 복사하지 않습니다.



색상 정본: [kiosk-design-system-index.md](../kiosk-design-system-index.md) · candidate A~E `.md` · `kiosk-tokens-candidate-*.css` · Trend hex [color-swatches.html](../color-swatches.html)

### Figma 커뮤니티 키트 참고 (스타일 영감)

플러그인 컴포넌트 쇼케이스 레이아웃·밀도는 아래 키트를 참고했습니다. **에셋 import 없이** Figma API 프레임만으로 재현합니다.

| 키트 | 용도 |
|------|------|
| [Courses Dashboard UI KIT](https://www.figma.com/design/MZ7cCNaum5g4nAspeuENgn/Courses---Courses-Dashboard-UI-KIT?node-id=14-410) | list row · 어드민/settings 행 · 카드 그리드 밀도 |
| [Kiosk Community](https://www.figma.com/design/9YLXX1NqX0xveVxNl9Y5aX/Kiosk213213--Community-) | 메뉴 카드 · 하단 sticky CTA · 옵션 chip |
| [Y2K UI Kit (Retro Bubblegum)](https://www.figma.com/design/ndHUuQpfTvanwdspoIKM4Q/Y2K-UI-Kit) | youth badge · coral/pink pop · DS-05/07 무드 |



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



`embed_menu_images.py`로 메뉴 사진을 바꾼 경우에도 동일 절차입니다.



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

