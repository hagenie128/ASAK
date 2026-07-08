# 키오스크 디자인 시스템 후보 비교 (A / B / D / E)

> **목적**: 팀이 1안을 선택하기 위한 비교표 — **4안 독립 유지 (병합 없음)**  
> **후보 C (Warm Bistro)**: 팀 결정으로 **후보 목록에서 제외** — [candidate-C](./kiosk-design-system-candidate-C.md) · Trend-2 스와치 참고용 보관  
> **캔버스**: 834×1194 · 터치 ≥44px · safe area 상하 24 / 좌우 16  
> **인덱스**: [kiosk-design-system-index.md](./kiosk-design-system-index.md) · **Notion**: [디자인 & 화면 hub](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc) · [브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7)

---

## 1. 한눈에 보기

| 구분 | 후보 A — Fresh Greens | 후보 B — Modern Minimal | 후보 D — Trend Forward | **후보 E — A+C 트렌디** |
|------|----------------------|-------------------------|------------------------|---------------------------|
| **컨셉** | 샐러드·신선함 | 흑백+포인트 미니멀 | 딥 포레스트+네온 민트·글래스 | **A 신선 + C 따뜻 + 트렌디 (라이트)** |
| **Primary** | `#16A34A` green | `#1A1C20` charcoal | `#0F2E1F` deep forest | **`#3D8B5F` sage** → `#2D6A4F` |
| **배경** | `#FFFDF3` cream | `#F0F1ED` cool gray | `#F4F7F5` cool white | **`#FAF7F2` warm off-white** |
| **Accent** | `#A3E635` lime · `#FACC15` yellow | `#C8F135` electric lime | `#3DFFA8` mint · `#FF6B4A` coral | **`#E07A5F` terracotta** |
| **CTA** | flat green 56px | flat lime 52px | mint→teal gradient 60px | **sage→forest gradient 56px** |
| **폰트** | Pretendard | Pretendard + Space Grotesk | Pretendard + Sora | Pretendard + Fraunces/DM Sans |
| **Dark mode** | ❌ | ❌ | **✅** | ❌ |
| **Notion Trend** | 회의 팔레트 · Option A Salady | Trend-3 Electric Lime | Trend-3/4 · QSR forward | **Trend-1 sage + Trend-2 coral** |
| **문서** | [candidate-A](./kiosk-design-system-candidate-A.md) | [candidate-B](./kiosk-design-system-candidate-B.md) | [candidate-D](./kiosk-design-system-candidate-D.md) | **[candidate-E](./kiosk-design-system-candidate-E-ac-trendy.md)** |
| **CSS** | [tokens-A](./kiosk-tokens-candidate-A.css) | [tokens-B](./kiosk-tokens-candidate-B.css) | [tokens-D](./kiosk-tokens-candidate-D.css) | **[tokens-E](./kiosk-tokens-candidate-E.css)** |

---

## 2. 색상 비교

| 역할 | A Fresh Greens | B Modern Minimal | D Trend Forward | **E A+C 트렌디** |
|------|----------------|------------------|-----------------|------------------|
| Primary | `#16A34A` | `#1A1C20` | `#0F2E1F` | **`#3D8B5F` sage** |
| Primary Dark | `#15803D` | `#4A4E57` | `#081A12` | **`#2D6A4F` forest** |
| Secondary | `#E8F5E9` | `#4A4E57` | glass `rgba(255,255,255,0.72)` | **`#EDE6DB`** |
| Accent | `#A3E635` | `#C8F135` | `#3DFFA8` + `#FF6B4A` | **`#E07A5F` terracotta** |
| Background | `#FFFDF3` | `#F0F1ED` | `#F4F7F5` / dark `#121816` | **`#FAF7F2`** |
| Surface | `#FFFFFF` | `#FFFFFF` | `#FFFFFF` / glass | `#FFFFFF` |
| Text | `#1F2937` | `#1A1C20` | `#0A0F0D` | **`#2C2C2C`** |
| Success | `#22C55E` | `#C8F135` | `#3DFFA8` | `#40916C` |
| Error | `#EF4444` | `#DC2626` | `#FF4D4D` | `#D64545` |

---

## 3. 타이포 비교

| 토큰 | A | B | D | **E** |
|------|---|---|---|-------|
| Display | 36px / 700 | 40px / 800 | **44px / 800** | **40px / 700** |
| Menu bold | — | — | — | **22px / 700** |
| H1 | 32px / 700 | 34px / 800 | 36px / 800 | 32px / 700 |
| H2 | 24px / 600 | 24px / 700 | 26px / 700 | 24px / 600 |
| Body | 18px / 400 | 16px / 500 | 17px / 500 | 18px / 400 |
| Button | 20px / 600 | 18px / 700 | **20px / 700** | 20px / 600 |
| 특징 | 가독성·친근 | 대형·임팩트 | oversized·glass | **warm+sage·gradient CTA** |

---

## 4. UX·브랜드 정합

| 평가 축 | A | B | D | **E** |
|---------|---|---|---|-------|
| 회의 팔레트 `#16A34A` | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ | ★★★★☆ |
| 지양: 촌스러운 초록 | ★★☆☆☆ | ★★★★★ | ★★★★★ | ★★★★★ |
| 지양: 과한 자연풍 | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| 브랜드: 신선·건강 | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| 브랜드: 친근·건강메이트 | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★★★ |
| photo-first 메뉴 (SCR-003) | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ |
| 키오스크 속도·가독성 | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| Admin (Courses kit) 연계 | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ |
| 트렌드·차별화 | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★★★ |
| dark mode · glass · gradient | ★☆☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| **A+C 하이브리드 (트렌디)** | ★★☆☆☆ | ★☆☆☆☆ | ★★☆☆☆ | **★★★★★** |

---

## 5. SCR별 추천 매핑

| SCR | A | B | D | **E** | hub 권장 Trend |
|-----|---|---|---|-------|----------------|
| 001 홈 | ★ | ★ | ★ | **★** | **Trend-1 vs Trend-4** A/B |
| 002 유형 | ★ | ○ | ○ | **★** | Trend-5 / terra chip |
| 003 메뉴 | ★ | ○ | ★ | **★** | Trend-1 photo |
| 004 옵션 | ★ | ○ | ○ | **★** | Trend-4 |
| 005~008 | ★ | ○ | ○ | **★** | Trend-4 |
| 012 결제실패 | ○ | ★ | ★ | ○ | Trend-3 mint |
| 009~011 Admin | ○ | ○ | ○ | ○ | Courses kit |
| 015~019 Admin | ○ | ○ | ○ | ○ | Courses + Trend-5 |
| 014 접근성 | ○ | ○ | ★ | ○ | dark mode toggle |

★ = 최적 · ○ = 적용 가능

---

## 6. 왜 다른가 (옵션별)

> 유사한 hue라도 **CTA·배경·액센트·타이포·radius** 가 다르면 별도 안입니다. **병합하지 않습니다.**

### 후보 A — Fresh Greens

- **왜 다른가**: 회의 확정 `#16A34A`·cream `#FFFDF3`를 **그대로** 씀. Trend-4 blush·rose 없음 · E의 sage gradient 없음 · B/D의 트렌디 탈피 없음
- **장점**: 회의 정본 직결 · 샐러드 브랜드 직관 · MVP 설득 용이
- **단점**: green-heavy · 경쟁사 유사 · 촌스러운 초록 리스크

### 후보 B — Modern Minimal

- **왜 다른가**: Trend-3 hex와 **유사 축**이나 DS **프레임·타이포·컴포넌트 세트**가 독립. D와 달리 **플랫·dark mode 없음**
- **장점**: green 탈피 · 고대비·대타이포 · 완료/에러 명확
- **단점**: 따뜻함 부족 · 회의 green과 거리

### ~~후보 C — Warm Bistro~~ (제외)

- 팀 결정으로 후보 목록에서 제외. warm appetite·terracotta 무드는 **Trend-2 Variables** 또는 **후보 E** terra 액센트로 참고. 상세: [candidate-C](./kiosk-design-system-candidate-C.md)

### 후보 D — Trend Forward

- **왜 다른가**: B(Trend-3)와 **실행 레이어 완전 분리** — glass·gradient·dark mode·mint+coral. E와 달리 **쿨·다크 트렌디**
- **장점**: food photo + bold UI · 2025–26 QSR 무드
- **단점**: 회의 green 거리 · glass 구현 비용

### 후보 E — A+C 트렌디

- **왜 다른가**: A+C를 50:50 섞은 게 아님 — **sage primary·warm bg·terra 액센트만·gradient CTA**. Trend-4 blush forest와 **hex 불일치** · A의 `#16A34A` flat CTA와 **다름**
- **장점**: 신선+따뜻함을 라이트 트렌디로 실행 · 인스타그램mable
- **단점**: 회의 green hue 거리 · dark mode 없음

### Trend-1 vs Trend-4 (Variables · DS 후보 아님)

> **2026-07 refresh — 영한·쨍한**: 채도↑·베이지 톤 제거·쿨 핑크 배경·타이포 weight↑. A~E 후보와 **병합 없음**.

- **Trend-1**: vivid coral CTA `#FF5C7A`→`#FF4D8D` **gradient** + fresh sage `#52D98A` — **non-green CTA** · photo-first · 뱃지 `#FFD93D` 포인트
- **Trend-4**: fresh forest `#1B6B47` CTA + vivid blush `#FFE4EE` + rose `#FF6B9D` — **핑크그린 무드** (forest CTA 유지)
- **왜 둘 다 필요한가**: SCR-001에서 **CTA 색 전략**(coral gradient vs forest)과 **배경 온도**(cool pink tint vs blush)를 A/B로 비교. 후보 A·E·Trend-4를 **하나로 합치면 이 비교가 사라짐**

---

## 7. 팀 선택 가이드

| 팀 우선순위 | 추천 후보 |
|-------------|-----------|
| 회의 팔레트·MVP 일관성 최우선 | **A** |
| 트렌드·차별화·가독성 (미니멀) | **B** |
| 친근·매장 무드·food photo (따뜻함) | **E** 또는 Trend-2 Variables |
| 트렌드·bold·2025–26 QSR (다크·glass) | **D** |
| A+C 원하지만 트렌디하게 (라이트·웜) | **E** |
| Variables A/B (DS 확정 전) | SCR-001 **Trend-1 vs Trend-4** |
| DS frame A/B | SCR-001 **A vs E** · SCR-003 **E vs D** |

---

## 8. 다음 단계

1. Figma `02. User Flow`에서 플러그인으로 **DS-01~07** 프레임 생성 → [figma-create-ds-plugin](./figma-create-ds-plugin/README.md)
2. SCR-001·003에 선택 후보 + Trend Variables mode 적용
3. 팀 리뷰 후 1안 확정 → Notion [브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) 갱신
4. `figma-links.template.json` · DevCopilot 반영

---

## Git 파일 목록

| 파일 | 설명 |
|------|------|
| `kiosk-design-system-index.md` | A,B,D,E · Trend 매핑 인덱스 |
| `kiosk-design-system-candidate-A.md` ~ `E` | 후보 명세 (C는 보관) |
| `kiosk-design-system-comparison.md` | 이 비교표 |
| `kiosk-tokens-candidate-A.css` ~ `E.css` | 후보 CSS (C는 보관) |
| `figma-create-ds-plugin/` | Figma DS frame 7개 생성 |
