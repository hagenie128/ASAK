#!/usr/bin/env python3
"""ASAK ingredient symbol SVGs (stroke icons) + seed mapping."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed" / "ingredient.json"
OUT = ROOT / "images" / "ingredient-icons"
SVG_DIR = OUT / "svg"

# Shared stroke style for kiosk UI (color via CSS currentColor)
HEAD = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
  aria-hidden="true">
'''
TAIL = "\n</svg>\n"


def svg(body: str) -> str:
    return HEAD + body + TAIL


# --- icon library (simple food symbols) ---
ICONS: dict[str, str] = {
    "leaf": svg(
        """  <path d="M24 40c0-14 10-24 20-24-2 12-10 20-20 24Z"/>
  <path d="M24 40C24 26 14 16 4 16c2 12 10 20 20 24Z"/>
  <path d="M24 40V22"/>"""
    ),
    "tomato": svg(
        """  <circle cx="24" cy="26" r="12"/>
  <path d="M18 16c2-4 6-6 6-6s4 2 6 6"/>
  <path d="M24 10v6"/>"""
    ),
    "onion": svg(
        """  <ellipse cx="24" cy="28" rx="12" ry="10"/>
  <path d="M16 24c2-8 6-12 8-14 2 2 6 6 8 14"/>
  <path d="M24 14v4"/>"""
    ),
    "corn": svg(
        """  <ellipse cx="24" cy="26" rx="8" ry="14"/>
  <path d="M24 12v28"/>
  <path d="M18 18h12M18 24h12M18 30h12"/>
  <path d="M16 14c-4 2-6 6-4 8M32 14c4 2 6 6 4 8"/>"""
    ),
    "mushroom": svg(
        """  <path d="M10 24c0-10 6-16 14-16s14 6 14 16H10Z"/>
  <path d="M20 24v12h8V24"/>"""
    ),
    "olive": svg(
        """  <ellipse cx="24" cy="24" rx="10" ry="14"/>
  <ellipse cx="24" cy="24" rx="3" ry="5"/>
  <path d="M24 10V6"/>"""
    ),
    "pepper": svg(
        """  <path d="M18 18c0-6 4-10 6-10s4 2 4 6c4 0 8 4 8 10 0 8-6 14-12 14s-12-6-12-14c0-4 2-6 6-6Z"/>
  <path d="M24 8c2-3 4-4 6-4"/>"""
    ),
    "carrot": svg(
        """  <path d="M22 14l4 30 4-30"/>
  <path d="M20 14c-4-6-2-10 4-10 6 0 8 4 4 10"/>
  <path d="M24 20h4M23 28h5M22 34h4"/>"""
    ),
    "cabbage": svg(
        """  <circle cx="24" cy="26" r="12"/>
  <path d="M16 26c2-6 6-10 8-10s6 4 8 10"/>
  <path d="M18 30c3 4 6 6 6 6s3-2 6-6"/>"""
    ),
    "avocado": svg(
        """  <path d="M24 8c8 0 14 10 14 20s-6 12-14 12S10 38 10 28 16 8 24 8Z"/>
  <ellipse cx="24" cy="28" rx="5" ry="7"/>"""
    ),
    "cucumber": svg(
        """  <ellipse cx="24" cy="24" rx="8" ry="16"/>
  <path d="M20 16h8M19 24h10M20 32h8"/>"""
    ),
    "chicken": svg(
        """  <path d="M14 30c0-8 6-14 12-14 4 0 6 2 8 2 4 0 6 4 6 8 0 8-6 12-12 12-8 0-14-2-14-8Z"/>
  <circle cx="30" cy="20" r="1.5" fill="currentColor" stroke="none"/>
  <path d="M12 34c2 4 6 6 10 6"/>"""
    ),
    "egg": svg(
        """  <ellipse cx="24" cy="26" rx="10" ry="14"/>
  <ellipse cx="24" cy="28" rx="5" ry="6"/>"""
    ),
    "fish": svg(
        """  <path d="M8 24c8-10 20-12 28-8 2 4 2 12 0 16-8 4-20 2-28-8Z"/>
  <path d="M36 16l8-6v20l-8-6"/>
  <circle cx="16" cy="22" r="1.5" fill="currentColor" stroke="none"/>"""
    ),
    "beef": svg(
        """  <circle cx="24" cy="24" r="12"/>
  <circle cx="24" cy="24" r="5"/>
  <path d="M24 12v4M24 32v4M12 24h4M32 24h4"/>"""
    ),
    "pork": svg(
        """  <ellipse cx="24" cy="26" rx="14" ry="10"/>
  <circle cx="18" cy="24" r="2"/>
  <circle cx="30" cy="24" r="2"/>
  <path d="M16 16c2-4 6-6 8-6s6 2 8 6"/>"""
    ),
    "bacon": svg(
        """  <path d="M10 18c6 4 10 2 14 0s8-4 14 0"/>
  <path d="M10 24c6 4 10 2 14 0s8-4 14 0"/>
  <path d="M10 30c6 4 10 2 14 0s8-4 14 0"/>"""
    ),
    "shrimp": svg(
        """  <path d="M12 28c0-10 8-16 16-16 6 0 10 4 10 10 0 10-8 14-16 14-2 0-4-2-4-4"/>
  <path d="M28 14c4-4 8-4 12-2"/>
  <circle cx="34" cy="22" r="1.5" fill="currentColor" stroke="none"/>"""
    ),
    "tofu": svg(
        """  <rect x="12" y="14" width="24" height="24" rx="2"/>
  <path d="M12 22h24M12 30h24M20 14v24M28 14v24"/>"""
    ),
    "ham": svg(
        """  <path d="M10 28c0-10 8-16 18-16h4c4 0 6 4 6 8 0 12-8 18-18 18-6 0-10-4-10-10Z"/>
  <circle cx="26" cy="26" r="4"/>"""
    ),
    "bottle": svg(
        """  <path d="M20 8h8v6l4 4v22a2 2 0 0 1-2 2H18a2 2 0 0 1-2-2V18l4-4V8Z"/>
  <path d="M18 24h12"/>"""
    ),
    "sauce": svg(
        """  <path d="M16 14h16l2 6v18a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4V20l2-6Z"/>
  <path d="M20 8h8v6H20z"/>
  <path d="M18 28h12"/>"""
    ),
    "bowl": svg(
        """  <path d="M8 22h32c0 12-8 18-16 18S8 34 8 22Z"/>
  <path d="M12 22c2-6 6-10 12-10s10 4 12 10"/>"""
    ),
    "rice": svg(
        """  <path d="M8 26h32c0 10-8 14-16 14S8 36 8 26Z"/>
  <path d="M14 26c1-8 5-14 10-14s9 6 10 14"/>
  <circle cx="20" cy="22" r="1.2" fill="currentColor" stroke="none"/>
  <circle cx="26" cy="20" r="1.2" fill="currentColor" stroke="none"/>
  <circle cx="30" cy="24" r="1.2" fill="currentColor" stroke="none"/>"""
    ),
    "noodle": svg(
        """  <path d="M10 16c8 4 12-4 20 0s10 4 8 8"/>
  <path d="M10 24c8 4 12-4 20 0s10 4 8 8"/>
  <path d="M10 32c8 4 12-4 20 0s10 4 8 8"/>
  <path d="M8 38h32"/>"""
    ),
    "pasta": svg(
        """  <path d="M12 14c10 6 14-2 24 4"/>
  <path d="M10 22c10 6 14-2 24 4"/>
  <path d="M10 30c10 6 14-2 24 4"/>
  <ellipse cx="24" cy="38" rx="14" ry="4"/>"""
    ),
    "wrap": svg(
        """  <path d="M10 30c4-12 12-18 20-20l8 8c-2 8-8 16-20 20l-8-8Z"/>
  <path d="M18 18l12 12"/>"""
    ),
    "soup": svg(
        """  <path d="M10 22h28v6c0 8-6 12-14 12S10 36 10 28v-6Z"/>
  <path d="M14 22c2-6 6-8 10-8s8 2 10 8"/>
  <path d="M18 14c0-4 2-6 6-6"/>"""
    ),
    "chips": svg(
        """  <ellipse cx="18" cy="22" rx="8" ry="10" transform="rotate(-20 18 22)"/>
  <ellipse cx="30" cy="26" rx="8" ry="10" transform="rotate(15 30 26)"/>
  <ellipse cx="24" cy="30" rx="7" ry="9" transform="rotate(-5 24 30)"/>"""
    ),
    "nuts": svg(
        """  <ellipse cx="18" cy="24" rx="7" ry="10"/>
  <ellipse cx="30" cy="26" rx="7" ry="9"/>
  <path d="M18 18v12M30 20v12"/>"""
    ),
    "cheese": svg(
        """  <path d="M8 32 L24 12 L40 32Z"/>
  <circle cx="20" cy="26" r="2"/>
  <circle cx="28" cy="28" r="2"/>
  <circle cx="24" cy="22" r="1.5"/>"""
    ),
    "berry": svg(
        """  <circle cx="18" cy="26" r="6"/>
  <circle cx="28" cy="24" r="6"/>
  <circle cx="24" cy="32" r="5"/>
  <path d="M24 14c0 4-2 6-4 8M24 14c0 4 2 6 4 8"/>"""
    ),
    "seaweed": svg(
        """  <path d="M16 40c0-16 4-28 4-28s4 8 4 20"/>
  <path d="M24 40c2-18 6-28 6-28s2 10 2 20"/>
  <path d="M12 40c4-12 2-24 2-24"/>
  <path d="M8 12h32"/>"""
    ),
    "flake": svg(
        """  <path d="M24 8v32M12 16l24 16M12 32l24-16"/>
  <circle cx="24" cy="24" r="3"/>"""
    ),
    "bread": svg(
        """  <path d="M8 28c0-10 6-16 16-16s16 6 16 16v8H8v-8Z"/>
  <path d="M12 28h24"/>"""
    ),
    "seed": svg(
        """  <ellipse cx="18" cy="22" rx="5" ry="8" transform="rotate(-30 18 22)"/>
  <ellipse cx="28" cy="20" rx="5" ry="8" transform="rotate(20 28 20)"/>
  <ellipse cx="24" cy="30" rx="5" ry="7"/>"""
    ),
    "default": svg(
        """  <circle cx="24" cy="24" r="14"/>
  <path d="M24 16v10"/>
  <circle cx="24" cy="32" r="1.5" fill="currentColor" stroke="none"/>"""
    ),
}

# keyword → icon (order matters: first match wins)
RULES: list[tuple[str, str]] = [
    (r"닭가슴|치킨|닭다리|로스트닭", "chicken"),
    (r"연어|그라브락스|생선", "fish"),
    (r"쉬림프|새우", "shrimp"),
    (r"스크램블", "egg"),
    (r"에그마요|계란|에그(?!마)", "egg"),
    (r"베이컨", "bacon"),
    (r"우삼겹|비프|그라운드", "beef"),
    (r"삼겹|포크|돼지", "pork"),
    (r"잠봉|햄", "ham"),
    (r"두부", "tofu"),
    (r"토마토", "tomato"),
    (r"양파플레이크", "flake"),
    (r"양파", "onion"),
    (r"옥수수", "corn"),
    (r"머쉬룸|버섯", "mushroom"),
    (r"올리브", "olive"),
    (r"당근", "carrot"),
    (r"적채|양배추|캐베지", "cabbage"),
    (r"아보카도", "avocado"),
    (r"오이", "cucumber"),
    (r"크랜베리|베리", "berry"),
    (r"견과", "nuts"),
    (r"나쵸|카사바|칩", "chips"),
    (r"치즈|슈레드", "cheese"),
    (r"김자반|해조|김", "seaweed"),
    (r"후리가케|플레이크", "flake"),
    (r"스프|스튜", "soup"),
    (r"메밀|누들|면", "noodle"),
    (r"파스타", "pasta"),
    (r"포케|그레인|밥|라이스", "rice"),
    (r"채소볼|볼$|베이스|채소$", "bowl"),
    (r"랩|또띠아|또띠야|토르티야", "wrap"),
    (r"빵|치아바타|샌드", "bread"),
    (r"드레싱|소스|마요|페스토|바베큐|시저|오리엔탈|렌치|발사믹|크리미|사워|스위트포테이토|단호박|화이트치즈소스|참깨|허니|머스타드|칠리", "bottle"),
    (r"할라피뇨|고추", "pepper"),
    (r"시금치|로메인|채소|그린|케일|양상추|야채", "leaf"),
    (r"씨앗|시드|견과", "seed"),
]


TYPE_FALLBACK = {
    26: "leaf",  # 채소
    27: "chicken",  # 단백질
    28: "bottle",  # 드레싱
    29: "bowl",  # 베이스
    30: "chips",  # 사이드
    31: "seed",  # 기타
}


def pick_icon(name: str, type_id: int) -> str:
    for pattern, icon in RULES:
        if re.search(pattern, name, re.I):
            return icon
    return TYPE_FALLBACK.get(type_id, "default")


def main() -> None:
    SVG_DIR.mkdir(parents=True, exist_ok=True)

    for key, content in ICONS.items():
        (SVG_DIR / f"{key}.svg").write_text(content, encoding="utf-8")

    ingredients = json.loads(SEED.read_text(encoding="utf-8"))
    mapping = []
    for ing in ingredients:
        icon = pick_icon(ing["name"], ing["type_id"])
        mapping.append(
            {
                "ingredient_id": ing["id"],
                "ingredient_name": ing["name"],
                "type_id": ing["type_id"],
                "icon_key": icon,
                "icon_path": f"svg/{icon}.svg",
            }
        )

    (OUT / "mapping.json").write_text(
        json.dumps(
            {
                "style": {
                    "viewBox": "0 0 48 48",
                    "stroke": "currentColor",
                    "strokeWidth": 2,
                    "usage": "CSS color: inherit / currentColor 로 톤 맞추기",
                },
                "icons": sorted(ICONS.keys()),
                "items": mapping,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # preview HTML
    cards = []
    for row in mapping:
        cards.append(
            f'<div class="card"><img src="{row["icon_path"]}" alt=""/><span>{row["ingredient_name"]}</span>'
            f'<code>{row["icon_key"]}</code></div>'
        )
    preview = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8"/>
<title>ASAK Ingredient Icons</title>
<style>
  body {{ font-family: Pretendard, system-ui, sans-serif; background:#f7f7f5; color:#1a1a1a; margin:24px; }}
  h1 {{ font-size:20px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:12px; }}
  .card {{ background:#fff; border:1px solid #e8e8e4; border-radius:12px; padding:12px; display:flex; flex-direction:column; align-items:center; gap:8px; }}
  .card img {{ width:40px; height:40px; color:#2f6b3a; }}
  .card span {{ font-size:12px; text-align:center; }}
  .card code {{ font-size:10px; color:#888; }}
  .set {{ display:flex; flex-wrap:wrap; gap:16px; margin:16px 0 32px; }}
  .set figure {{ margin:0; text-align:center; }}
  .set img {{ width:48px; height:48px; }}
</style>
</head>
<body>
<h1>ASAK Ingredient Symbols</h1>
<p>stroke icons · currentColor · 48×48</p>
<div class="set">
{"".join(f'<figure><img src="svg/{k}.svg"/><figcaption>{k}</figcaption></figure>' for k in sorted(ICONS))}
</div>
<h2>재료 매핑 ({len(mapping)})</h2>
<div class="grid">{"".join(cards)}</div>
</body>
</html>
"""
    (OUT / "preview.html").write_text(preview, encoding="utf-8")

    (OUT / "README.md").write_text(
        """# ingredient-icons — ASAK 재료 심벌(SVG)

직접 그린 **stroke 심벌**입니다. 샐러디 사진(`ingredient-salady`)과 별개로 UI 아이콘용입니다.

## 사용
- 경로: `svg/{icon_key}.svg`
- 색: CSS에서 `color` / `currentColor` (예: 라임 악센트)
- 매핑: `mapping.json`의 `ingredient_id` → `icon_key`

## 다시 생성
```bash
python3 ../scripts/generate_ingredient_icons.py
```

## 미리보기
브라우저로 `preview.html` 열기.
""",
        encoding="utf-8",
    )

    used = {m["icon_key"] for m in mapping}
    print(f"icons={len(ICONS)} mapped={len(mapping)} used_keys={len(used)} out={OUT}")


if __name__ == "__main__":
    main()
