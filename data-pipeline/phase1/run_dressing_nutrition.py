"""FatSecret 샐러디 드레싱 영양 보조 수집."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

from salady_scraper import DRESSING_CATALOG_EXTRAS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}

BASE = "https://www.fatsecret.kr/%EC%B9%BC%EB%A1%9C%EB%A6%AC-%EC%98%81%EC%96%91%EC%86%8C/%EC%83%90%EB%9F%AC%EB%94%94"

SLUGS: dict[str, str] = {
    "시저": "%EC%8B%9C%EC%A0%80",
    "허니머스타드": "%ED%97%88%EB%8B%88%EB%A8%B8%EC%8A%A4%ED%83%80%EB%93%9C",
    "(저당) 들기름소이": "(%EC%A0%80%EB%8B%B9)-%EB%93%A4%EA%B8%B0%EB%A6%84%EC%86%8C%EC%9D%B4",
}


FALLBACK_MACROS: dict[str, dict[str, float]] = {
    # FatSecret 샐러디 브랜드 페이지 (50g) — 요청 HTML에 매크로 미포함 시 보완
    "시저": {
        "fat_g": 24.0,
        "carbs_g": 5.0,
        "protein_g": 1.0,
        "sugar_g": 4.0,
        "saturated_fat_g": 3.9,
        "sodium_mg": 290.0,
    },
    "허니머스타드": {
        "fat_g": 12.5,
        "carbs_g": 19.4,
        "protein_g": 0.4,
    },
}


def parse_fatsecret_page(html: str, name: str) -> dict[str, Any] | None:
    text = re.sub(r"\s+", " ", html)

    cal_match = re.search(r"1인분\s*\(\s*(\d+)\s*g\s*\)\s*안에\s*(\d+)\s*칼로리", text)
    if not cal_match:
        return None
    weight_g = float(cal_match.group(1))
    calories = float(cal_match.group(2))

    nutrition: dict[str, Any] = {
        "menu": name,
        "weight_g": weight_g,
        "calories_kcal": calories,
    }

    summary = re.search(
        r"영양 요약:\s*Cal\s*(\d+(?:\.\d+)?)\s*"
        r"지방\s*(\d+(?:\.\d+)?)\s*g\s*"
        r"탄수화물\s*(\d+(?:\.\d+)?)\s*g\s*"
        r"단백질\s*(\d+(?:\.\d+)?)\s*g",
        text,
    )
    if summary:
        nutrition.update(
            {
                "calories_kcal": float(summary.group(1)),
                "fat_g": float(summary.group(2)),
                "carbs_g": float(summary.group(3)),
                "protein_g": float(summary.group(4)),
            }
        )

    for pattern, field in (
        (r"당류\s*(\d+(?:\.\d+)?)\s*g", "sugar_g"),
        (r"포화지방\s*(\d+(?:\.\d+)?)\s*g", "saturated_fat_g"),
        (r"나트륨\s*(\d+(?:\.\d+)?)\s*mg", "sodium_mg"),
    ):
        match = re.search(pattern, text)
        if match:
            nutrition[field] = float(match.group(1))

    if name in FALLBACK_MACROS:
        for key, value in FALLBACK_MACROS[name].items():
            nutrition.setdefault(key, value)

    return {
        "name": name,
        "nutrition_pdf": nutrition,
        "kcal": nutrition["calories_kcal"],
        "source": "fatsecret_salady",
    }


def fetch_dressing(name: str, slug: str) -> dict[str, Any] | None:
    url = f"{BASE}/{slug}/1%EC%9D%B8%EB%B6%84"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200 or name not in resp.text:
        return None
    row = parse_fatsecret_page(resp.text, name)
    if row:
        row["source_url"] = url
    return row


def build_supplements() -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for name in DRESSING_CATALOG_EXTRAS:
        slug = SLUGS.get(name, quote(name))
        row = fetch_dressing(name, slug)
        if row:
            items.append(row)
            print(f"OK {name}: {row['kcal']} kcal")
        else:
            print(f"SKIP {name}")

    # (저당) 들기름소이: FatSecret 단품 페이지 없음 — 참깨소이(공식 PDF) 대비 추정 보류
    items.append(
        {
            "name": "고추간장 소스",
            "nutrition_pdf": {
                "menu": "고추간장 소스",
                "weight_g": 50.0,
                "note": "단품 영양성분 미공개 (선재스님 메뉴 포함 소스)",
            },
            "source": "manual_placeholder",
        }
    )

    return {
        "note": "공식 영양 PDF DRESSING 섹션에 없는 드레싱 보조 데이터",
        "count": len(items),
        "items": items,
    }


def main() -> None:
    output = Path("output") / "dressing_nutrition_supplements.json"
    data = build_supplements()
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved {output} ({data['count']} items)")


if __name__ == "__main__":
    main()
