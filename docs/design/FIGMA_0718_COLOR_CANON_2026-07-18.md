# ASAK Figma 0718 색·파일 정본 (Phase 0)

**작성:** 2026-07-18 · **쓰기 대상:** `yHhvn5RKjBd91U8BJUQz7F` 만

## 파일 역할

| 순서 | 파일 | fileKey | 역할 |
|---|---|---|---|
| 1 | ASAK-1 | `k67gDKvnB29ILSzIpFYSaT` | 원본 라임 팔레트 + Legacy 컴포넌트 |
| 2 | 0714 | `VXKyzoNdsgM4oN57mrECxb` | 화면 시각 정본 (`#B5E30F`). Color 컬렉션 파랑 무시 |
| 3 | 0715 | `JSrjOy668zhfkiLplCkreh` | AI 손상본 · 읽기 전용. **구분선(`---`) 아래**에 01~06·05-B/06-B·Pre-componentization Archive 등 화면·컴포넌트 다수 보관 |
| 4 | **0718** | `yHhvn5RKjBd91U8BJUQz7F` | 유일한 쓰기 타깃. 구분선 아래는 비움 · C페이지(위)만 유지 |

## 0718 Brand 정본 (유지)

| Token | Hex |
|---|---|
| `Semantic/Brand/Primary` → Green/300 | `#B5E30F` |
| `Semantic/Brand/Secondary` → Green/500 | `#6C9700` |
| `Semantic/Brand/Subtle` → Green/50 | `#F5FBE0` |
| `Semantic/Brand/OnPrimary` → Green/700 | `#243300` |
| Lime/300·400·500 | `#C5FF00` / `#B7FF00` / `#B3E500` |

## 0714 화면 top hex (검증용)

- Kiosk: `#B5E30F`, `#292D30`, `#FFFFFF`, `#5DA45D`, `#0D0D0D`
- Admin: `#B5E30F`, `#111827`, `#FFFFFF`, `#6B7280`, `#5B8C2A`

## TEXT 오바인딩 교정 규칙

| 잘못 | 교정 |
|---|---|
| `Semantic/BG/Page` | `Semantic/Text/Admin/Primary` |
| `Color/Surface/*` | `Semantic/Text/Admin/Primary` |
| `Semantic/BG/Admin` (흰 글자) | `Color/White` |
| `#B5E30F` ← `Color/Green/500` | `Semantic/Brand/Primary` |

## 사용자 재바인딩 표 (0718에 적용)

| From | To |
|---|---|
| `#3B82F6` `#0088FF` | 아이콘/선택=`Brand/Primary`, 텍스트=`Text/Tertiary` |
| `#ccc` | `Border/Subtle` `#F5F5F5` |
| `#f8f9fa` | `BG/Subtle` `#F5F5F5` |
| `#c8f230` | `Green/200` `#C8F064` |
| `#d1ff33` `#b7ff00` | `Brand/Primary` |
| `#e53333` | `Status/Error` |
| `#ff8d28` | `Semantic/Category/Side` (Orange/400) |
| SaveBar dirty `#292d30`/`#262626` | `WarningBG` + `WarningText` `#92400E` |

## 표에 없어 바꾸지 않은 unbound hex (04-C 샘플)

`#F2F5F5` `#167846` `#E8F8F0` `#4DB24D` `#4D4D4D` `#262626`(SaveBar 외) `#BFD99E` `#F28C0D` `#F0F0F0` `#1C1F1C` `#374151` `#4AA54E` `#FFF8E6` `#A06400` `#C83232` `#D9D9D9` `#4CAF50` `#6699FF` `#10B981` `#5A8C14` …

## 0715 구분선 아래 (반입 창고)

`01~06` · `05-B/06-B` · Visual Recovery Pilot · `06-C Pre-componentization Archive(68)` · `92-Archive`  
0718에는 구분선 아래 없음. 필요 Master만 골라 가져올 것.
