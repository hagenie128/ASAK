# ASAK 키오스크 — 디자인 시스템 마스터 인덱스

> **역할**: Figma **DS-01~07** · 후보 **A,B,D,E** · Notion **Trend-1~5** — **병합 없이** 나란히 매핑  
> **비교표**: [kiosk-design-system-comparison.md](./kiosk-design-system-comparison.md) · **구조**: [kiosk-design-system.md](./kiosk-design-system.md)  
> **회의 요약**: [screen-design-meeting-opinion-template.md](./screen-design-meeting-opinion-template.md) § DS Preview  
> **Notion**: [브랜드 · Trend 컬러](https://app.notion.com/p/39451ef04f0b814a9447f6fbf171b3b7) · [디자인 & 화면 hub](https://app.notion.com/p/39451ef04f0b8163b1f9ebb477917efc)

---

## 0. Figma frame 명명 (DS-01~07)

패턴: `DS-{NN} {Short Name}` — subtitle·컨셉은 프레임 본문에만.

| DS | Figma frame | 구 이름 |
|:--:|-------------|---------|
| **01** | `DS-01 Fresh Greens` | DS Candidate A — Fresh Greens |
| **02** | `DS-02 Modern Minimal` | DS Candidate B — Modern Minimal |
| **03** | `DS-03 Trend Forward` | DS Candidate D — Trend Forward |
| **04** | `DS-04 A+C Trendy` | DS Candidate E — A+C Trend |
| **05** | `DS-05 Pink-Green` | DS Trend-1 — Pink-Green |
| **06** | `DS-06 Blush Forest` | DS Trend-4 — Blush Forest |
| **07** | `DS-07 Pink-Lime Hybrid` | DS Hybrid B×T1 — Bold Pink-Lime |

> Candidate C (Warm Bistro)는 **보관** — DS 라인업 제외. 레거시 `DS-1~4` 프레임명도 플러그인 재실행 시 제거.

---

## 1. DS 후보 A,B,D,E ↔ Trend 매핑

| 후보 | 이름 | Figma frame | Variables mode | 가장 가까운 Trend | **차이점** |
|------|------|-------------|----------------|-------------------|------------|
| **A** | Fresh Greens | `DS-01 Fresh Greens` | `ds-candidate-a-fresh-greens` | 회의 팔레트 | **`#16A34A` + cream** — blush·sage gradient 없음 (Trend-4·E와 별개) |
| **B** | Modern Minimal | `DS-02 Modern Minimal` | `ds-candidate-b-modern-minimal` | Trend-3 | Charcoal+lime **플랫 DS** · dark mode 없음 (D와 별개) |
| **D** | Trend Forward | `DS-03 Trend Forward` | `ds-candidate-d-trend-forward` | Trend-3/4 실행 | **glass·gradient·dark mode** · B(Trend-3)와 실행 레이어 분리 |
| **E** | A+C 트렌디 | `DS-04 A+C Trendy` | `ds-candidate-e-fresh-warm-trend` | Trend-1+2 | **sage gradient CTA + terra 액센트** — A·C 단순 혼합·Trend-4 blush 아님 |

> **병합 금지**: A ≠ E ≠ Trend-4. 유사 hue라도 CTA·배경·액센트·타이포가 다르면 별도 안 유지.

### 보관 (후보 목록 제외)

| 후보 | 이름 | 비고 |
|------|------|------|
| ~~**C**~~ | Warm Bistro | 팀 결정으로 제외 — [candidate-C](./kiosk-design-system-candidate-C.md) · Trend-2 terracotta 스와치 참고 |

---

## 2. 후보별 Git 문서

| 후보 | 명세 | CSS |
|:----:|------|-----|
| A | [candidate-A](./kiosk-design-system-candidate-A.md) | [tokens-A](./kiosk-tokens-candidate-A.css) |
| B | [candidate-B](./kiosk-design-system-candidate-B.md) | [tokens-B](./kiosk-tokens-candidate-B.css) |
| D | [candidate-D](./kiosk-design-system-candidate-D.md) | [tokens-D](./kiosk-tokens-candidate-D.css) |
| E | [candidate-E](./kiosk-design-system-candidate-E-ac-trendy.md) | [tokens-E](./kiosk-tokens-candidate-E.css) |
| ~~C~~ | [candidate-C](./kiosk-design-system-candidate-C.md) *(보관)* | [tokens-C](./kiosk-tokens-candidate-C.css) *(보관)* |

viewer 구현 기본(색상 확정 전): [`kiosk-tokens.css`](./kiosk-tokens.css)

---

## 3. Trend-1~5 (Notion Variables)

| Trend | Primary feel | 관련 후보 | **차이점** |
|-------|--------------|-----------|------------|
| **Trend-1** | Vivid coral CTA + fresh sage | E (sage 무드) | CTA **`#FF5C7A`→`#FF4D8D` gradient** + sage `#52D98A` — *2026-07 영한·쨍한 refresh* |
| **Trend-2** | Terracotta + cream | (Variables) | ~~DS C 제외~~ — Trend-2 terracotta Variables · warm appetite 참고 |
| **Trend-3** | Charcoal + lime | B | 후보 B = DS 세트 · Trend-3 = Variables 스위치 |
| **Trend-4** | Vivid blush + fresh forest | (Variables) | **blush `#FFE4EE` + rose `#FF6B9D`** + forest `#1B6B47` — *2026-07 영한·쨍한 refresh* |
| **Trend-5** | Navy + lemon | — | DS 후보 없음 · SCR-007·012 결제 옵션 |

스와치: [color-swatches.html](./color-swatches.html)

---

## 4. 자주 헷갈리는 쌍

| 비교 | 왜 다른가 |
|------|-----------|
| **A vs Trend-4** | A = `#16A34A` cream. Trend-4 = forest + blush + rose |
| **A vs E** | A = flat corporate green. E = sage gradient + warm + terra |
| **E vs Trend-4** | E = warm sage·terra. Trend-4 = blush pink-green 무드 |
| **B vs D** | B = 플랫 minimal. D = glass·dark·gradient |
| **Trend-1 vs Trend-4** | vivid coral gradient CTA vs fresh forest CTA — SCR-001 **Variables A/B** · *둘 다 2026-07 영한·쨍한 팔레트로 갱신* |
| **B vs Hybrid B×T1** | B = lime flat CTA · Hybrid = coral→pink CTA + lime outline secondary |
| **Trend-1 vs Hybrid B×T1** | Trend-1 = blush hero·sage secondary · Hybrid = B cool gray·charcoal hero·lime badge |

---

## 5. Figma · SCR

- 플러그인: [figma-create-ds-plugin](./figma-create-ds-plugin/README.md) → **`DS-01`~`DS-07` 프레임 7개** (§0 매핑표) · 각 프레임 **Components** 섹션에 아래 **플러그인 예시 컴포넌트** 자동 생성 (834×2400 · 2열 그리드)

### 플러그인 예시 컴포넌트 (DS-01~07 공통)

- Home hero strip (SCR-001) · category tab bar · menu photo card · menu card horizontal · menu card sold-out
- option chip row · option radio group (SCR-004) · quantity stepper · list group ×2
- payment method row (SCR-007) · success toast · bottom sticky CTA bar
- 헤더: 4색 미니 dot + 타이포 2샘플 인라인 (Colors/Typography 대형 섹션 없음)
- Variables `asak-trend-1`~`5`는 Figma Variables로 별도 (DS-05/06 프레임과 병합하지 않음)
- SCR-001: **DS-05 vs DS-06** (Variables A/B + 플러그인 프레임) + **DS-01 vs DS-04** (후보 비교) + **DS-02 vs DS-07** (minimal vs youth coral)
- **DS-07 Pink-Lime Hybrid**: B의 charcoal·cool gray·electric lime 구조에 Trend-1의 vivid coral→pink CTA를 합친 **7번째 비교 프레임** — DS-02·DS-05에 병합하지 않음 · 스와치 `asak-hybrid-b-t1`

---

## 폐기 (병합 시도 — 사용 안 함)

`kiosk-design-system-modes.md`, `kiosk-tokens-modes.css`, DS-1~4 명명 — 2026-07-06 되돌림
