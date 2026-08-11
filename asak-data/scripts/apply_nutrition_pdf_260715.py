#!/usr/bin/env python3
"""Apply nutrition_260715.pdf fields into ASAK ingredient/menu nutrition seeds.

PDF columns:
  serving_g, kcal, carb_g, sugar_g, protein_g, fat_g, saturated_fat_g, sodium_mg

seed-v3 writes ingredient nutrition into ing_nutr.json (1:1 with ing).
Legacy seed/ingredient.json still keeps nutrition fields inline.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED_V3_ING = ROOT / "seed-v3" / "ing.json"
SEED_V3_ING_NUTR = ROOT / "seed-v3" / "ing_nutr.json"
SEED_ING = ROOT / "seed" / "ingredient.json"
SEED_V3_MENU = ROOT / "seed-v3" / "menu.json"
SEED_V3_MENU_NUTR = ROOT / "seed-v3" / "menu_nutr.json"
SEED_MENU = ROOT / "seed" / "menu.json"
SEED_MENU_NUTR = ROOT / "seed" / "menu_nutrition.json"
REPORT = ROOT / "scripts" / "output" / "nutrition_pdf_260715_report.json"

# name -> (serving_g, kcal, carb_g, sugar_g, protein_g, fat_g, saturated_fat_g, sodium_mg)
ING_NUTRITION: dict[str, tuple[float, float, float, float, float, float, float, float]] = {
    # BASE
    "채소볼": (80, 10.5, 1.4, 0.5, 0.9, 0.2, 0.0, 7.9),
    "포케볼": (172, 271.1, 50.6, 0.4, 7.9, 4.2, 0.7, 53.0),
    "메밀면볼": (164, 144.2, 25.8, 0.4, 5.8, 1.9, 0.3, 182.8),
    "파스타볼": (164, 157.7, 28.0, 0.4, 5.2, 2.8, 0.3, 6.3),
    "파스타면": (200, 298.6, 53.8, 0.0, 9.0, 5.3, 0.7, 0.0),
    "곡물밥": (195, 386.3, 73.2, 0.0, 10.6, 5.7, 0.9, 4.6),
    # SIDE
    "양송이크림스프": (200, 150.0, 12.0, 4.0, 3.0, 10.0, 7.0, 561.0),
    "단호박크림스프": (200, 218.8, 21.3, 15.0, 2.5, 13.8, 10.0, 325.0),
    "포테이토크림스프": (200, 210.0, 18.0, 9.0, 7.0, 12.0, 12.0, 600.0),
    "치킨토마토스튜": (200, 124.0, 12.6, 9.6, 14.0, 1.8, 0.4, 713.2),
    "카사바칩": (50, 244.5, 35.5, 0.5, 1.5, 10.5, 4.5, 71.5),
    # DRESSING
    "오리엔탈": (50, 160.0, 8.0, 7.0, 1.0, 14.0, 2.2, 280.0),
    "(저당) 발사믹": (50, 110.0, 14.0, 2.0, 0.0, 6.0, 0.9, 250.0),
    "(저당) 랜치": (50, 137.3, 9.7, 1.4, 1.1, 11.9, 2.6, 463.3),
    "고추장비빔": (30, 80.0, 17.0, 14.0, 1.0, 1.0, 0.5, 480.0),
    "크리미칠리": (50, 235.0, 14.0, 11.0, 0.0, 20.0, 3.2, 410.0),
    "크리미할라피뇨": (50, 235.0, 7.0, 7.0, 1.0, 23.0, 3.6, 320.0),
    "(저당) 레몬허브": (50, 4.1, 8.4, 0.5, 0.2, 0.1, 0.1, 360.0),
    "(저당) 참깨소이": (50, 110.0, 6.0, 0.1, 1.0, 11.0, 1.8, 410.0),
    "(저당) 스리라차소이": (50, 58.2, 13.6, 2.1, 0.8, 0.0, 0.0, 562.5),
    # DRINK
    "아메리카노": (290, 22.5, 2.4, 0.0, 1.8, 0.5, 0.0, 24.3),
    "그린밀싹": (240, 120.0, 28.0, 22.0, 1.0, 0.0, 0.0, 39.0),
    "오렌지당근": (240, 113.0, 27.0, 23.0, 1.0, 0.0, 0.0, 43.0),
    "레드클렌즈": (240, 120.0, 29.0, 24.0, 1.2, 0.0, 0.0, 43.0),
    "코크제로": (355, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 22.0),
    "스프라이트제로": (355, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 11.0),
    "애사비사과스파클링": (350, 8.0, 9.0, 0.0, 0.0, 0.0, 0.0, 25.0),
    # PROTEIN
    "닭가슴살": (50, 64.3, 2.0, 0.0, 13.1, 0.4, 0.4, 118.8),
    "그라브락스연어": (60, 99.1, 1.4, 0.4, 12.8, 4.7, 0.5, 346.6),
    "로스트닭다리살": (60, 113.8, 6.0, 1.3, 10.5, 5.3, 2.1, 272.5),
    "그라운드비프": (40, 108.0, 0.0, 0.0, 10.2, 7.2, 2.9, 38.4),
    "우삼겹": (50, 161.1, 3.0, 2.5, 9.3, 12.4, 5.1, 165.6),
    "베이컨": (20, 66.3, 0.7, 0.4, 3.0, 5.7, 2.1, 105.6),
    "로스트삼겹": (50, 187.4, 3.2, 0.4, 9.0, 15.4, 4.8, 116.2),
    "에그": (50, 72.5, 0.7, 0.1, 6.7, 4.3, 1.4, 64.0),
    "두부": (80, 100.0, 8.0, 1.2, 4.2, 5.7, 0.7, 12.8),
    "잠봉슬라이스": (25, 34.4, 0.6, 0.3, 4.7, 1.4, 0.4, 250.0),
    "케이준쉬림프": (60, 36.9, 0.1, 0.1, 8.3, 0.6, 0.0, 332.5),
    "스크램블에그": (50, 115.0, 5.5, 1.0, 4.0, 8.5, 1.4, 260.0),
    # VEGGIES
    "올리브": (30, 31.5, 1.8, 0.0, 0.3, 2.9, 0.4, 264.0),
    "할라피뇨": (40, 6.7, 1.3, 0.0, 0.0, 0.0, 0.0, 293.2),
    "머쉬룸": (60, 59.1, 3.3, 0.4, 1.5, 5.6, 0.9, 1.1),
    "옥수수": (30, 19.5, 3.6, 2.1, 0.6, 0.3, 0.0, 78.0),
    "양파": (30, 8.7, 2.0, 1.7, 0.3, 0.0, 0.0, 0.9),
    "토마토": (40, 7.6, 1.7, 0.9, 0.4, 0.1, 0.0, 0.8),
    "드라이토마토": (30, 44.7, 4.6, 2.9, 0.5, 2.3, 0.5, 0.3),
    "당근라페": (40, 27.7, 4.1, 3.7, 0.5, 1.1, 0.2, 44.1),
    "적채": (15, 6.2, 1.4, 0.7, 0.3, 0.0, 0.0, 1.1),
    "파인애플": (30, 22.8, 5.7, 5.1, 0.0, 0.0, 0.0, 0.6),
    # CRISPY
    "후리가케": (3, 12.5, 1.6, 0.1, 0.5, 0.5, 0.1, 69.0),
    "견과류": (15, 90.7, 4.9, 0.5, 2.5, 6.8, 0.6, 0.3),
    "나쵸칩": (15, 75.0, 9.2, 0.0, 1.1, 3.8, 0.3, 34.5),
    "양파플레이크": (10, 55.1, 5.5, 1.1, 0.4, 3.5, 1.7, 5.0),
    "크랜베리": (10, 31.4, 8.6, 7.4, 0.0, 0.1, 0.0, 0.2),
    "슈레드치즈": (20, 65.0, 0.0, 0.0, 5.0, 4.3, 3.0, 85.0),
    "몬테레이치즈": (30, 111.9, 0.2, 0.0, 7.3, 9.1, 5.7, 186.0),
    "김자반": (3, 17.3, 1.1, 0.4, 0.6, 1.2, 0.1, 33.0),
    # SAUCE & MOUSSE
    "에그마요": (50, 122.5, 2.5, 0.0, 4.5, 10.5, 2.1, 140.0),
    "스윗포테이토": (70, 126.0, 17.5, 9.1, 1.4, 5.6, 1.0, 98.0),
    "단호박": (70, 58.6, 12.5, 7.0, 0.7, 0.4, 0.1, 0.1),
    "사워크림": (10, 23.2, 0.5, 0.3, 0.3, 2.2, 1.4, 4.0),
    "바질페스토": (20, 119.0, 0.5, 1.8, 2.8, 10.7, 2.0, 171.0),
    "바베큐소스": (10, 24.6, 5.5, 2.8, 0.3, 0.2, 0.0, 151.2),
    "화이트치즈소스": (20, 72.0, 4.6, 3.6, 0.4, 5.8, 1.6, 98.0),
    # PROMOTION extras listed as ingredients
    "엑스트라버진올리브오일": (10, 90.0, 0.0, 0.0, 0.0, 10.0, 1.5, 0.0),
    "[고창] 리얼수박주스": (240, 84.0, 19.0, 19.0, 1.0, 0.0, 0.0, 0.0),
}

# Menu-level nutrition from PDF (latest page values preferred when duplicated)
MENU_NUTRITION: dict[str, tuple[float, float, float, float, float, float, float, float]] = {
    "탄단지샐러디": (225, 322.9, 34.3, 17.6, 17.9, 13.1, 2.0, 225.3),
    "랜치콥샐러디": (217, 160.9, 6.8, 2.3, 16.7, 7.3, 2.0, 457.5),
    "로스트닭다리살샐러디": (290, 326.6, 34.7, 14.4, 13.8, 14.8, 4.8, 569.8),
    "그라브락스연어샐러디": (235, 247.3, 7.8, 5.1, 21.0, 14.4, 2.7, 505.0),
    "노릇두부단호박샐러디": (295, 214.6, 28.1, 12.4, 6.8, 8.4, 1.1, 214.9),
    "타코쉬림프샐러디": (230, 192.1, 11.6, 2.9, 15.7, 9.2, 3.0, 572.6),
    "프루티가든샐러디": (180, 215.9, 26.0, 16.5, 4.0, 10.8, 1.3, 141.4),
    "칠리베이컨포케볼": (297, 485.2, 61.7, 4.5, 18.7, 18.0, 5.9, 268.1),
    "그라브락스연어포케볼": (302, 461.3, 62.5, 4.4, 22.0, 14.0, 3.1, 577.1),
    "로스트삼겹포케볼": (307, 563.4, 65.0, 4.6, 18.7, 26.1, 7.7, 215.3),
    "우삼겹포케볼": (307, 618.1, 68.0, 6.2, 21.2, 29.8, 8.6, 226.0),
    "노릇노릇두부포케볼": (360, 506.6, 68.9, 4.8, 15.7, 19.3, 2.5, 207.8),
    "바베큐닭다리살포케볼": (347, 557.3, 72.5, 8.2, 26.6, 17.7, 5.9, 586.2),
    "바베큐삼겹덮밥": (381, 832.1, 98.9, 11.5, 26.1, 37.0, 8.3, 877.1),
    "로스트닭다리살마요덮밥": (401, 830.0, 98.3, 11.1, 27.8, 36.3, 7.1, 998.1),
    "우삼겹메밀면누들볼": (259, 406.6, 36.1, 5.0, 18.0, 21.2, 6.1, 350.3),
    "그라브락스연어파스타누들볼": (279, 346.2, 33.3, 3.6, 20.0, 14.4, 2.1, 609.9),
    "고소삼겹들기름파스타누들볼": (296, 445.3, 42.8, 2.8, 16.0, 24.0, 5.9, 369.0),
    "비빔메밀면누들볼": (246, 235.6, 30.0, 2.2, 13.4, 6.6, 1.8, 294.3),
    "닭다리살MAX 프로틴박스": (449, 758.7, 96.6, 7.7, 43.2, 22.3, 7.4, 885.9),
    "우삼겹MAX 프로틴박스": (419, 900.7, 87.6, 11.5, 39.4, 43.7, 16.3, 565.4),
    "치킨MAX 프로틴파스타": (464, 707.9, 66.2, 6.1, 55.1, 23.7, 6.0, 697.0),
    "[우창윤픽] 포만호르몬에그샐러디": (296, 391.9, 10.0, 3.5, 23.3, 28.0, 6.5, 669.3),
    "[우창윤픽] 포만호르몬에그": (131, 250.4, 3.6, 2.1, 13.8, 19.3, 4.4, 320.0),
    "엑스트라버진올리브오일": (10, 90.0, 0.0, 0.0, 0.0, 10.0, 1.5, 0.0),
    "[고창] 리얼수박주스": (240, 84.0, 19.0, 19.0, 1.0, 0.0, 0.0, 0.0),
    "에그마요랩": (225, 661.6, 49.7, 5.3, 19.4, 42.8, 9.8, 1054.3),
    "멕시칸랩": (234, 607.4, 52.5, 10.9, 19.4, 35.1, 9.9, 931.2),
    "시저치킨랩": (229, 500.9, 46.2, 12.4, 21.8, 25.7, 6.3, 877.4),
    "로스트닭다리살랩": (294, 549.6, 46.3, 10.3, 19.8, 31.9, 9.2, 1206.3),
    "바질치킨랩": (229, 523.9, 44.7, 12.6, 24.2, 26.8, 6.8, 932.4),
    "타코쉬림프랩": (289, 501.1, 59.4, 15.5, 15.4, 22.4, 6.0, 1123.1),
    "그라브락스연어랩": (244, 475.4, 40.0, 8.9, 17.6, 27.6, 6.1, 1014.2),
    "칠리베이컨곡물랩": (305, 730.4, 75.5, 12.9, 21.5, 37.6, 10.9, 1067.1),
    "고소우삼겹곡물랩": (305, 704.7, 79.1, 6.5, 24.0, 32.5, 9.3, 1089.8),
    "바베큐닭다리살곡물랩": (340, 717.3, 76.8, 13.5, 26.1, 34.0, 9.7, 1288.1),
    "클래식치킨샌드위치": (214, 469.0, 60.8, 13.3, 17.3, 17.8, 3.4, 733.8),
    "비프에그마요샌드위치": (275, 712.6, 64.9, 15.1, 25.5, 38.6, 11.2, 1047.3),
    "바질연어샌드위치": (289, 574.4, 70.7, 16.9, 20.6, 22.6, 4.0, 1021.5),
    "바질레몬연어샌드위치": (289, 574.4, 70.7, 16.9, 20.6, 22.6, 4.0, 1021.5),
    "잠봉샌드위치": (241, 491.2, 53.9, 8.4, 19.8, 21.6, 5.2, 1133.9),
    "프레시잠봉샌드위치": (241, 491.2, 53.9, 8.4, 19.8, 21.6, 5.2, 1133.9),
    "스파이시쉬림프샌드위치": (254, 463.7, 55.4, 8.7, 18.4, 18.5, 4.4, 1176.4),
    "불고기반미샌드위치": (254, 578.7, 61.3, 14.1, 18.7, 28.9, 8.1, 899.0),
    "BELT 시저샌드위치": (254, 570.3, 52.5, 6.3, 21.6, 29.7, 8.2, 874.4),
    "멜팅치즈치킨샌드위치": (250, 699.6, 52.7, 5.6, 37.4, 36.9, 14.4, 1154.9),
    "멜팅치즈핫쉬림프샌드위치": (240, 595.0, 54.4, 8.1, 26.4, 29.6, 11.6, 1346.7),
    "하와이안잠봉샌드위치": (254, 539.4, 72.7, 23.7, 19.0, 18.8, 5.8, 1015.3),
    "바질카프레제샌드위치": (209, 496.8, 51.8, 6.6, 18.0, 23.4, 8.5, 817.9),
    "더블에그마요샌드위치": (290, 707.0, 60.3, 9.3, 21.1, 42.3, 9.0, 1187.0),
    "이탈리안피자샌드위치": (245, 608.6, 58.0, 9.4, 21.9, 31.8, 9.9, 1266.8),
    "치즈스크램블온브레드": (135, 338.1, 32.9, 5.3, 11.2, 17.5, 4.5, 649.3),
    "베이컨스크램블온브레드": (155, 404.3, 33.6, 5.7, 14.1, 23.3, 6.6, 754.8),
}


def normalize(name: str) -> str:
    s = name.strip()
    s = s.replace("（", "(").replace("）", ")")
    s = re.sub(r"\s+", "", s)  # seed는 공백 있음, PDF는 붙여씀
    aliases = {
        "(베이스)파스타면": "파스타면",
        "(베이스)곡물밥": "곡물밥",
        "잠봉": "잠봉슬라이스",
        "화이트치즈": "화이트치즈소스",
    }
    return aliases.get(s, s)


# PDF/시드 키를 공백 제거 기준으로 통일
ING_NUTRITION = {normalize(k): v for k, v in ING_NUTRITION.items()}
MENU_NUTRITION = {normalize(k): v for k, v in MENU_NUTRITION.items()}


def tuple_to_fields(values: tuple[float, ...]) -> dict:
    serving_g, kcal, carb_g, sugar_g, protein_g, fat_g, saturated_fat_g, sodium_mg = values
    return {
        "serving_g": serving_g,
        "kcal": kcal,
        "carb_g": carb_g,
        "sugar_g": sugar_g,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "saturated_fat_g": saturated_fat_g,
        "sodium_mg": sodium_mg,
    }


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


NUTR_KEYS = (
    "serving_g",
    "kcal",
    "carb_g",
    "sugar_g",
    "protein_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
)


def update_ing_nutrition(ing_path: Path, nutr_path: Path) -> dict:
    ings = load_json(ing_path)
    nutrs = load_json(nutr_path) if nutr_path.exists() else []
    by_ing_id = {row["ing_id"]: row for row in nutrs}
    name_to_ing_id = {normalize(row["name"]): row["id"] for row in ings}

    matched = []
    unmatched = []
    for name, values in ING_NUTRITION.items():
        ing_id = name_to_ing_id.get(normalize(name))
        if ing_id is None:
            unmatched.append({"name": name})
            continue
        fields = tuple_to_fields(values)
        row = by_ing_id.get(ing_id)
        if row is None:
            row = {"id": ing_id, "ing_id": ing_id, "source_id": None}
            nutrs.append(row)
            by_ing_id[ing_id] = row
        row.update(fields)
        matched.append({"ing_id": ing_id, "name": name})

    for row in nutrs:
        for key in NUTR_KEYS:
            row.setdefault(key, None)
        row.setdefault("source_id", None)

    dump_json(nutr_path, nutrs)
    return {
        "path": str(nutr_path),
        "matched": matched,
        "unmatched": unmatched,
    }


def update_ingredients(path: Path, sold_out_key: str) -> dict:
    rows = load_json(path)
    matched = []
    unmatched = []
    for row in rows:
        name = normalize(str(row.get("name", "")))
        values = ING_NUTRITION.get(name)
        if values is None:
            # keep existing kcal/protein, only ensure new keys exist as null
            for key in NUTR_KEYS:
                row.setdefault(key, None)
            unmatched.append({"id": row.get("id"), "name": row.get("name")})
            continue
        fields = tuple_to_fields(values)
        row.update(fields)
        # preserve sold_out key style
        if sold_out_key not in row and "sold_out" in row:
            pass
        matched.append({"id": row.get("id"), "name": row.get("name")})
    dump_json(path, rows)
    return {"path": str(path), "matched": matched, "unmatched": unmatched}


def update_menu_nutrition(menu_path: Path, nutr_path: Path) -> dict:
    menus = load_json(menu_path)
    nutrs = load_json(nutr_path)
    by_menu_id = {row["menu_id"]: row for row in nutrs}
    name_to_menu_id = {normalize(m["name"]): m["id"] for m in menus}

    matched = []
    missing_menu = []
    for name, values in MENU_NUTRITION.items():
        menu_id = name_to_menu_id.get(normalize(name))
        if menu_id is None:
            missing_menu.append(name)
            continue
        row = by_menu_id.get(menu_id)
        fields = tuple_to_fields(values)
        if row is None:
            row = {"id": menu_id, "menu_id": menu_id, "source_id": 41}
            nutrs.append(row)
            by_menu_id[menu_id] = row
        row.update(
            {
                "serving_g": fields["serving_g"],
                "kcal": fields["kcal"],
                "carb_g": fields["carb_g"],
                "sugar_g": fields["sugar_g"],
                "protein_g": fields["protein_g"],
                "fat_g": fields["fat_g"],
                "saturated_fat_g": fields["saturated_fat_g"],
                "sodium_mg": fields["sodium_mg"],
            }
        )
        matched.append({"menu_id": menu_id, "name": name})

    for row in nutrs:
        for key in ("serving_g", "sugar_g", "saturated_fat_g"):
            row.setdefault(key, None)

    dump_json(nutr_path, nutrs)
    return {
        "path": str(nutr_path),
        "matched": matched,
        "missing_menu": missing_menu,
    }


def main() -> None:
    report = {
        "source": "nutrition_260715.pdf",
        "ingredients": [],
        "menus": [],
    }
    report["ingredients"].append(update_ing_nutrition(SEED_V3_ING, SEED_V3_ING_NUTR))
    report["ingredients"].append(update_ingredients(SEED_ING, "is_sold_out"))
    report["menus"].append(update_menu_nutrition(SEED_V3_MENU, SEED_V3_MENU_NUTR))
    report["menus"].append(update_menu_nutrition(SEED_MENU, SEED_MENU_NUTR))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    dump_json(REPORT, report)
    print(f"report -> {REPORT}")
    for block in report["ingredients"]:
        print(
            f"[ing] {Path(block['path']).name}: matched={len(block['matched'])} unmatched={len(block['unmatched'])}"
        )
    for block in report["menus"]:
        print(
            f"[menu_nutr] {Path(block['path']).name}: matched={len(block['matched'])} missing_menu={len(block['missing_menu'])}"
        )


if __name__ == "__main__":
    main()
