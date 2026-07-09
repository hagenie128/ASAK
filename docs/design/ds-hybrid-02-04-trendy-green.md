# DS-08 Trendy Sage Hybrid — DS-02×04 미니멀·웜 트렌디 그린

> **(Figma 제안 프레임: `DS-08 Trendy Sage Hybrid`)**  
> **역할**: DS-01~07과 **병합 없이** 나란히 두는 **8번째 비교 프레임** — **2026-07-06 회의에서 논의된 DS-02+04 하이브리드 아이디어** · **미채택** 참고안 (회의 최종 채택: **DS-02 Modern Minimal**)  
> **회의록**: [screen-design-meeting-minutes-2026-07-06.md](./meetings/screen-design-meeting-minutes-2026-07-06.md)  
> **정본 참조**: [kiosk-design-system-index.md](./kiosk-design-system-index.md) · [candidate-B](./kiosk-design-system-candidate-B.md) · [candidate-E](./kiosk-design-system-candidate-E-ac-trendy.md) · [comparison](./kiosk-design-system-comparison.md)

---

## 1. 이름 · 포지션

| 항목 | 값 |
|------|-----|
| **공식 명칭** | **DS-08 Trendy Sage Hybrid** |
| **짧은 별칭** | DS-02×04 · Minimal Warm Sage |
| **Figma frame** | `DS-08 Trendy Sage Hybrid` |
| **Variables mode** *(제안)* | `ds-hybrid-b-e-trendy-sage` |
| **스와치 ID** *(제안)* | `asak-hybrid-b-e-sage` |

> DS-07(B×Trend-1 coral CTA)과 동일하게 **하이브리드 전용 프레임**으로 두고, DS-02·DS-04 본문에는 병합하지 않습니다.

---

## 2. 컨셉

**DS-02 Modern Minimal**의 레이아웃·타이포·고대비 구조 위에, **DS-04 A+C Trendy**의 웜 배경·포토 히어로·소프트 엘리베이션을 얹은 **프리미엄 샐러드 키오스크** 무드입니다.

CTA 그린은 DS-02의 일렉트릭 라임 `#C8F135`도, DS-04의 딥 sage→forest `#3D8B5F`→`#2D6A4F`도 아닌 **그 사이의 트렌디한 중간 그린**을 씁니다. 2025–26 웰니스·QSR 트렌드( Sweetgreen · CAVA · 영한 fresh green )에 맞춰 **네온 라임·촌스러운 corporate green·과한 포레스트**를 모두 피합니다.

| 항목 | 값 |
|------|-----|
| 무드 키워드 | minimal, warm, fresh, premium, instagrammable |
| UI 패턴 | DS-02 flat hierarchy + DS-04 photo-card · **emerald CTA** · 미세 terra 포인트 |
| 추천 SCR | 001 홈 · 003 메뉴 · 004 옵션 · 008 완료 |
| 지양 | `#C8F135` 라임 CTA · `#16A34A` flat corporate · `#2D6A4F` 이하 딥 포레스트 단독 CTA |

---

## 3. 색상 토큰 (전체)

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-primary` | **`#10B981`** | CTA·활성 탭·선택 칩·주문 완료 아이콘 (Emerald — **채택 primary**) |
| `color-primary-dark` | `#059669` | CTA pressed·그라데이션 끝·강조 stroke |
| `color-primary-light` | `#D1FAE5` | 선택 row·칩 배경·리스트 아이콘 fill |
| `color-secondary` | `#EDE8E0` | DS-04 warm neutral 축소 — 섹션·보조 surface |
| `color-accent` | **`#6EE7B7`** | 하이라이트·뱃지 outline·포커스 링·완료 glow (**채택 accent**) |
| `color-accent-warm` | `#E07A5F` | DS-04 terracotta — **뱃지·할인만** 미세 사용 (CTA 아님) |
| `color-background` | `#F3F2ED` | 페이지 — DS-02 cool gray `#F0F1ED` + DS-04 cream `#FAF7F2` 중간 |
| `color-surface` | `#FFFFFF` | 카드·패널·모달 |
| `color-surface-warm` | `#F8F5F0` | sticky bar·히어로 strip (DS-04 `#F5F0E8` 톤다운) |
| `color-text` | `#1F2320` | 본문 — DS-02 charcoal + DS-04 warm charcoal 블렌드 |
| `color-text-muted` | `#6B7280` | 캡션·칼로리·보조 라벨 |
| `color-text-inverse` | `#FFFFFF` | emerald CTA 위 텍스트 |
| `color-border` | `#E0E4DF` | 1px 구분선·카드 stroke |
| `color-border-strong` | `#1F2320` | DS-02 스타일 포커스·ghost 버튼 stroke |
| `color-cta` | `#10B981` → `#059669` | Primary 버튼 **135deg gradient** |
| `color-success` | `#10B981` | 주문 완료·결제 성공 (primary 재사용) |
| `color-error` | `#DC2626` | 결제 실패·품절 (DS-02 축 — 과한 경고 지양) |
| `color-overlay` | `rgba(31,35,32,0.48)` | 타임아웃·모달 dim |

### CTA 그라데이션

```css
background: linear-gradient(135deg, #10B981 0%, #059669 100%);
box-shadow: 0 4px 16px rgba(16, 185, 129, 0.22);
```

---

## 4. 중간 그린 후보 비교 · 채택 이유

회의에서 요청한「라임과 sage 사이, 트렌디한 초록」을 기준으로 후보를 좁혔습니다.

| 후보 | Hex | 라임 `#C8F135` 대비 | Sage `#3D8B5F` 대비 | 판단 |
|------|-----|---------------------|----------------------|------|
| Electric Lime (DS-02) | `#C8F135` | — | 너무 밝·노란·Gen-Z 네온 | ❌ 회의 방향 제외 |
| Fresh Sage (Trend-1) | `#52D98A` | 가깝지만 여전히 라임 쪽 | 밝음·쨍함 | △ secondary 칩용 가능 |
| **Emerald** | **`#10B981`** | 채도·명도 중간 — **트렌디 웰니스 표준** | forest보다 밝아 CTA 가독성 확보 | ✅ **Primary 채택** |
| Sage (DS-04) | `#3D8B5F` | 어둡고 차분 | — | ❌ 단독 CTA 시 촌스러움·무거움 |
| Forest (DS-04) | `#2D6A4F` | — | 너무 딥 | ❌ gradient 끝만 참고, 단독 CTA 아님 |
| Muted Sage | `#6B9E7A` | 중간이나 2024–26 QSR에서 다소 무뎌 보임 | — | △ 보조 톤 |
| Mint (toned) | `#5EEAD4` | 시안 기운·food app에서 차가움 | 라임에 가까운 밝기 | ❌ 샐러드 웜 무드와 충돌 |
| Emerald Light | **`#6EE7B7`** | 라임에 가깝지 않은 **밝은 하이라이트** | primary와 같은 hue family | ✅ **Accent 채택** |

**채택 조합: Primary `#10B981` + Accent `#6EE7B7`**

- Tailwind Emerald 계열은 2025–26 **프리미엄 웰니스·푸드 테크**에서 가장 널리 쓰이는「중간 fresh green」축입니다.
- `#C8F135`(H≈72°)와 `#3D8B5F`(H≈152°)의 **시각적 중간**에 가깝고, 키오스크 CTA로 **흰 글자 대비(WCAG)**도 확보됩니다.
- `#6EE7B7`은 같은 hue family로 선택 row·뱃지 outline에 쓰면 DS-02의 `#E8F5A0` 역할을 하되 **네온 느낌 없이** 트렌디합니다.
- DS-04 terracotta `#E07A5F`는 **그린 CTA와 경쟁하지 않도록** 뱃지 한정으로만 유지합니다.

---

## 5. DS-02 vs DS-04 — 무엇을 가져올까

### DS-02 Modern Minimal에서

- **레이아웃**: 여백 극대화 · 단일 CTA 홈 · flat hierarchy · sticky bar 구조
- **타이포**: Pretendard + **Space Grotesk** Display 40/800 · Body 16–18px 고대비
- **컴포넌트**: 8–12px radius (미니멀) · ghost/secondary **strong stroke** · 옵션 row 좌측 accent bar
- **텍스트 축**: charcoal `#1A1C20` 계열 — primary를 green으로 바꿔도 **본문은 다크** 유지
- **에러 처리**: `#DC2626` 아이콘만 — 과한 경고 배너 지양

### DS-04 A+C Trendy에서

- **배경 온도**: warm off-white `#F3F2ED` · surface-warm strip
- **포토 UX**: oversized photo-card · SCR-003 2열 · **hero food photo** 허용
- **엘리베이션**: soft shadow `0 8px 32px rgba(31,35,32,0.07)` — DS-02 flat보다 한 단계만
- **radius**: 카드 **16px** (02의 8px와 04의 24px 중간)
- **CTA 형태**: **gradient + subtle glow** (색만 emerald로 교체)
- **웜 액센트**: terracotta `#E07A5F` — NEW/HOT 뱃지·할인만
- **메뉴 타이포**: `type-menu` 22px/700 (DM Sans 또는 Fraunces 대체 가능)

### 하이브리드에서 **버리는 것**

| 출처 | 제외 항목 | 이유 |
|------|-----------|------|
| DS-02 | `#C8F135` lime CTA·chip | 회의 방향「라임 아님」 |
| DS-02 | cool gray 단독 `#F0F1ED` | DS-04 웜 무드 상실 |
| DS-04 | sage→forest `#3D8B5F`→`#2D6A4F` CTA | 너무 딥·촌스러운 green CTA 리스크 |
| DS-04 | radius 24px 전면 | DS-02 미니멀 정체성 희석 |

---

## 6. 타이포 · 간격 (요약)

| 토큰 | 값 | 출처 |
|------|-----|------|
| `type-display` | 40px / 800 | DS-02 |
| `type-menu` | 22px / 700 | DS-04 |
| `type-h1` | 34px / 800 | DS-02 |
| `type-body` | 17px / 500 | 02·04 중간 |
| `type-button` | 18px / 700 | DS-02 CTA |
| `radius-md` | 12px | 버튼·칩 |
| `radius-lg` | 16px | photo-card |
| CTA height | **52px** | DS-02 (04의 56px보다 미니멀) |

---

## 7. Figma 플러그인 프레임 제안

| 항목 | 값 |
|------|-----|
| **Frame title** | `DS-08 Trendy Sage Hybrid` |
| **Subtitle (프레임 본문)** | `B minimal layout · E warm mood · emerald #10B981 CTA · 8번째 비교` |
| **헤더 dot 4색** | `#10B981` · `#6EE7B7` · `#E07A5F` · `#1F2320` |
| **Primary button** | gradient `#10B981`→`#059669` · text `#FFFFFF` |
| **Secondary button** | white · stroke `#1F2320` · text `#1F2320` (DS-02) |
| **Chip selected** | fill `#10B981` · text `#FFFFFF` |
| **Badge NEW** | `#E07A5F` terra (DS-04) |

> 플러그인 `code.js` 반영 완료 — DS-01~08 생성. 아래 스니펫은 후보 객체 정본입니다.

### code.js 후보 스니펫 (초안)

```javascript
{
  id: "hybrid-b-e-sage",
  frameName: "DS-08 Trendy Sage Hybrid",
  subtitle: "B minimal layout · E warm mood · emerald #10B981 CTA · 8번째 비교",
  colors: [
    { role: "Emerald Primary", hex: "#10B981" },
    { role: "Emerald Dark", hex: "#059669" },
    { role: "Emerald Light", hex: "#6EE7B7" },
    { role: "Warm Secondary", hex: "#EDE8E0" },
    { role: "Accent Terra", hex: "#E07A5F" },
    { role: "Background", hex: "#F3F2ED" },
    { role: "Surface", hex: "#FFFFFF" },
    { role: "Text", hex: "#1F2320" },
    { role: "Border", hex: "#E0E4DF" },
  ],
  buttonPrimary: {
    gradient: true,
    fillStart: "#10B981",
    fillEnd: "#059669",
    fill: "#10B981",
    text: "#FFFFFF",
    label: "주문 시작하기",
  },
  buttonSecondary: { fill: "#FFFFFF", stroke: "#1F2320", text: "#1F2320", label: "장바구니" },
  bg: "#F3F2ED",
  mood: { hero: true, cornerRadius: 16, miniBtnRadius: 12, badgeColor: "#E07A5F" },
}
```

---

## 8. 회의록 · Notion용 한 줄 요약

> **2026-07-06 화면 설계 회의에서 논의·미채택 참고안.** **DS-08 Trendy Sage Hybrid**는 이하진·김나연 교차 후보인 **DS-02(미니멀·고대비)**와 **DS-04(웜·포토·트렌디)**를 합친 하이브리드 아이디어입니다. CTA는 emerald `#10B981`. **회의 최종 채택은 DS-02 Modern Minimal.** [회의록](./meetings/screen-design-meeting-minutes-2026-07-06.md)

---

## 9. SCR 비교 제안

| 비교 | 목적 |
|------|------|
| **DS-02 vs DS-08** | 같은 미니멀 구조에서 **lime vs emerald** CTA 체감 |
| **DS-04 vs DS-08** | 같은 웜·포토 무드에서 **sage-forest vs emerald** CTA 체감 |
| **DS-08 vs DS-07** | green CTA family 내 **emerald 단색 vs coral CTA** |

---

## 관련 파일

- [kiosk-design-system-index.md](./kiosk-design-system-index.md) — DS-01~07 매핑 (DS-08은 본 문서)
- [figma-create-ds-plugin](./figma-create-ds-plugin/README.md) — 플러그인 (DS-08 스니펫 §7)
- [screen-design-meeting-opinion-consolidated.md](./meetings/screen-design-meeting-opinion-consolidated.md) — DS-02·04 교차 후보 근거
