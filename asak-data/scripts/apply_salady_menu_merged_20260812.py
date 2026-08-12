#!/usr/bin/env python3
"""Apply salady_menu_merged_20260812.csv → seed-v3 + MySQL + Kiosk assets.

Assets (ASAK-Kiosk/public/assets):
  menu/{id}.png
  ingredients/photos/{id}.png
  ingredients/icons/{id}.svg
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed-v3"
INPUT = Path(__file__).resolve().parent / "input"
OUTPUT = Path(__file__).resolve().parent / "output"
WORKSPACE = ROOT.parent.parent
KIOSK_ASSETS = WORKSPACE / "ASAK-Kiosk" / "public" / "assets"
AUDIT_MENUS = (
    WORKSPACE / "ASAK" / "data-pipeline" / "phase1" / "audit_20260812_v3" / "menus.json"
)

DEFAULT_CSV = INPUT / "salady_menu_merged_20260812.csv"
REPORT_PATH = OUTPUT / "salady_menu_merged_20260812_report.json"

NUTR_COLS = (
    "제공량(g)",
    "열량(kcal)",
    "탄수화물(g)",
    "당류(g)",
    "단백질(g)",
    "지방(g)",
    "포화지방(g)",
    "나트륨(mg)",
)
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

CAT_MAP = {
    "샐러디": 233,
    "그레인볼": 233,
    "누들볼": 233,
    "프로틴 박스": 234,
    "프로틴박스": 234,
    "샌드위치": 236,
    "곡물랩": 235,
    "랩": 235,
}
TAG_MAP = {"BEST": 237, "NEW": 238, "LOW SUGAR": 239, "VEGAN": 240}

MENU_ALIASES = {
    "단호박노릇두부샐러디": "노릇두부단호박샐러디",
    "노릇두부단호박샐러디": "노릇두부단호박샐러디",
    "소고기비빔메밀누들볼": "비빔메밀면누들볼",
    "소고기비빔메밀면누들볼": "비빔메밀면누들볼",
}
TEMPLATE_MENU = {
    "샐러디": 1978,
    "그레인볼": 1167,
    "누들볼": 3249,
    "프로틴 박스": 3664,
    "프로틴박스": 3664,
    "샌드위치": 7264,
    "곡물랩": 6422,
    "랩": 6422,
}

ROLE_BASE = 33
ROLE_CORE = 32
ROLE_DEFAULT = 34
UNIT_TOPPING = 35

ING_ALIASES = {
    "시즈닝닭가슴살": "닭가슴살",
    "시즈닝닭가슴살x3": "닭가슴살x3",
    "그라브락스연어": "그라브락스연어",
    "그라브락스 연어": "그라브락스연어",
    "로스트닭다리살": "로스트닭다리살",
    "로스트 닭다리살": "로스트닭다리살",
    "로스트닭다리살x3": "로스트닭다리살x3",
    "닭가슴살x3": "닭가슴살x3",
    "파스타면": "파스타면, 채소",
    "메밀면": "메밀면, 채소",
    "엑스트라버진올리브오일": "엑스트라버진 올리브오일",
    "케이준쉬림프": "케이준쉬림프",
    "케이준 쉬림프": "케이준쉬림프",
    "찹베이컨": "베이컨",
    "칩베이컨": "베이컨",
    "그라운드비프": "그라운드비프",
    "우삼겹x3": "우삼겹x3",
}

BASE_MAP = {
    "채소": "채소",
    "곡물, 채소": "곡물, 채소",
    "곡물,채소": "곡물, 채소",
    "곡물(1.5배), 채소": "곡물, 채소",
    "파스타면, 채소": "파스타면, 채소",
    "메밀면, 채소": "메밀면, 채소",
    "바질 파스타면(2배), 채소": "바질 파스타면(2배), 채소",
    "파스타면": "파스타면, 채소",
    "메밀면": "메밀면, 채소",
    "*채소 미포함": "",
}

CORE_HINTS = (
    "닭가슴살",
    "닭다리살",
    "연어",
    "두부",
    "잠봉",
    "제육",
    "그라운드",
    "우삼겹",
    "삼겹",
    "새우",
    "쉬림프",
    "베이컨",
    "햄",
)
BREAD_HINTS = ("치아바타", "통밀", "바게트", "또띠야")
DRESSING_SKIP = ("미제공", "소스포함")

ALLERGEN_ING_HINTS: dict[str, tuple[str, ...]] = {
    "달걀": ("에그",),
    "우유": ("치즈", "슈레드", "요거트"),
    "대두": ("두부", "간장", "된장", "고추장", "들기름소이", "청양간장"),
    "밀": ("통밀", "치아바타", "파스타면", "메밀면", "치아"),
    "메밀": ("메밀",),
    "호두": ("견과", "호두"),
    "고등어": ("연어", "고등어"),
    "닭고기": ("닭",),
    "돼지 고기": ("잠봉", "제육", "삼겹", "베이컨", "햄"),
    "소고기": ("비프", "우삼겹", "그라운드"),
    "새우": ("새우", "쉬림프"),
    "토마토": ("토마토",),
    "조개류 (굴, 전복, 홍합포함)": ("우삼겹", "조개"),
    "아황산류 (10mg/kg 이상함유)": ("치아바타", "시저", "바질"),
}

ALLERGEN_FALLBACK_ROLE: dict[str, int] = {
    "밀": ROLE_BASE,
    "메밀": ROLE_BASE,
    "우유": ROLE_DEFAULT,
    "달걀": ROLE_CORE,
    "대두": ROLE_DEFAULT,
}

NEW_INGREDIENTS = [
    {"name": "고추장제육", "type_id": 27},
    {"name": "청양간장 드레싱", "type_id": 28},
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def strip_name(name: str) -> str:
    s = (name or "").strip().replace("（", "(").replace("）", ")")
    return re.sub(r"\s+", "", s)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return float(text)


def nutrition_from_row(row: dict[str, str]) -> dict[str, float | None]:
    return {k: parse_float(row.get(c)) for k, c in zip(NUTR_KEYS, NUTR_COLS, strict=True)}


def load_backend_env() -> None:
    here = Path(__file__).resolve()
    for env_path in (
        here.parents[3] / "ASAK-back" / ".env",
        here.parents[2] / "ASAK-back" / ".env",
    ):
        if not env_path.exists():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() and k.strip() not in os.environ:
                os.environ[k.strip()] = v.strip()
        break


def parse_jdbc_url(url: str) -> tuple[str, int, str]:
    raw = url.replace("jdbc:mysql://", "")
    host_port, _, rest = raw.partition("/")
    db = rest.split("?", 1)[0]
    host, port = host_port.split(":") if ":" in host_port else (host_port, "3306")
    return host, int(port), db


def next_id(rows: list[dict[str, Any]], key: str = "id") -> int:
    if not rows:
        return 1
    return max(int(r[key]) for r in rows) + 1


def index_menus(menus: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for m in menus:
        out.setdefault(strip_name(m["name"]), []).append(m)
    return out


LOW_PRIORITY_CATEGORIES = {231, 232}


def menu_priority(menu: dict[str, Any], policy_count: int = 0) -> tuple[int, int, int]:
    cat = int(menu.get("cat_id") or 0)
    if cat not in LOW_PRIORITY_CATEGORIES:
        cat_rank = 0
    elif cat == 231:
        cat_rank = 1
    else:
        cat_rank = 2
    return (cat_rank, -policy_count, int(menu["id"]))


def pick_canonical_menu(
    hits: list[dict[str, Any]], policy_by_menu: dict[int, int] | None = None
) -> dict[str, Any]:
    policy_by_menu = policy_by_menu or {}
    return min(
        hits,
        key=lambda m: menu_priority(m, policy_by_menu.get(int(m["id"]), 0)),
    )


def dedupe_menu_nutr(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_menu: dict[int, dict[str, Any]] = {}
    for r in rows:
        mid = int(r["menu_id"])
        prev = by_menu.get(mid)
        if prev is None:
            by_menu[mid] = r
            continue
        prev_has = prev.get("kcal") is not None
        cur_has = r.get("kcal") is not None
        if cur_has and not prev_has:
            by_menu[mid] = r
        elif cur_has == prev_has and int(r["id"]) < int(prev["id"]):
            by_menu[mid] = r
    return list(by_menu.values())


def dedupe_menu_ing(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[int, int, int]] = set()
    out: list[dict[str, Any]] = []
    for r in sorted(rows, key=lambda x: (int(x["menu_id"]), int(x.get("sort_no") or 0), int(x["id"]))):
        key = (int(r["menu_id"]), int(r["ing_id"]), int(r["role_id"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def dedupe_menu_tag(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[int, int]] = set()
    out: list[dict[str, Any]] = []
    for r in rows:
        key = (int(r["menu_id"]), int(r["tag_id"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def dedupe_menu_opt_policy(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[int, int]] = set()
    out: list[dict[str, Any]] = []
    for r in rows:
        key = (int(r["menu_id"]), int(r["policy_id"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def dedupe_ing_allergen(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[int, int]] = set()
    out: list[dict[str, Any]] = []
    for r in rows:
        key = (int(r["ing_id"]), int(r["allergen_id"]))
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def lookup_menu(index: dict[str, list], name: str) -> list[dict[str, Any]]:
    key = strip_name(name)
    for candidate in (key, MENU_ALIASES.get(key, key), re.sub(r"^\[프로틴\]", "", key)):
        hits = index.get(candidate)
        if hits:
            return hits
    return []


def index_ings(ings: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for ing in ings:
        out.setdefault(strip_name(ing["name"]), []).append(ing)
    return out


def resolve_ing(name: str, ing_by: dict[str, list[dict[str, Any]]]) -> dict[str, Any] | None:
    raw = (name or "").strip()
    if not raw:
        return None
    for candidate in (
        raw,
        ING_ALIASES.get(strip_name(raw), raw),
        BASE_MAP.get(raw, raw),
        BASE_MAP.get(strip_name(raw), raw),
    ):
        hits = ing_by.get(strip_name(candidate))
        if hits:
            return hits[0]
    key = strip_name(raw)
    for ing_key, hits in ing_by.items():
        if key in ing_key or ing_key in key:
            return hits[0]
    return None


def parse_csv_list(text: str) -> list[str]:
    parts = re.split(r"[,·]", text or "")
    out: list[str] = []
    for part in parts:
        name = part.strip()
        if name:
            out.append(name)
    return out


def is_core_ing(name: str, menu_name: str, toppings: list[str]) -> bool:
    compact = strip_name(name)
    if any(h in compact for h in CORE_HINTS):
        return True
    if compact == "에그" and ("콥" in menu_name or any("닭가슴살" in t for t in toppings)):
        return True
    return False


def is_bread(name: str) -> bool:
    compact = strip_name(name)
    return any(h in compact for h in BREAD_HINTS)


def build_menu_ing_from_csv(
    row: dict[str, str],
    menu_id: int,
    menu_name: str,
    cat_label: str,
    ing_by: dict[str, list[dict[str, Any]]],
    start_id: int,
) -> tuple[list[dict[str, Any]], int, list[str]]:
    """Build menu_ing rows from CSV composition. Returns (rows, next_id, unresolved)."""
    unresolved: list[str] = []
    toppings = parse_csv_list(row.get("토핑") or "")
    dressing = (row.get("추천/기본 드레싱") or "").strip()
    base_label = (row.get("베이스") or "").strip()

    bread: str | None = None
    rest_toppings: list[str] = []
    for t in toppings:
        if cat_label in ("샌드위치", "곡물랩", "랩") and is_bread(t):
            bread = t
        else:
            rest_toppings.append(t)

    rows: list[dict[str, Any]] = []
    nid = start_id
    sort_no = 1

    def add_row(ing: dict[str, Any], role_id: int, *, can_remove: bool, qty: int | None = None) -> None:
        nonlocal nid, sort_no
        rows.append(
            {
                "id": nid,
                "menu_id": menu_id,
                "ing_id": int(ing["id"]),
                "role_id": role_id,
                "quantity": qty,
                "unit_id": UNIT_TOPPING if role_id != ROLE_BASE else None,
                "is_default": True,
                "can_remove": can_remove,
                "sort_no": sort_no,
            }
        )
        nid += 1
        sort_no += 1

    base_name = bread or BASE_MAP.get(base_label, base_label)
    if cat_label == "샌드위치" and not bread and base_label == "채소":
        base_name = "통밀 치아바타"
    if not base_name or base_name.startswith("*") or "미포함" in base_name:
        base_name = None

    base_ing = resolve_ing(base_name, ing_by) if base_name else None
    if base_ing:
        add_row(base_ing, ROLE_BASE, can_remove=False)
    elif base_name:
        unresolved.append(base_name)

    dressing_names: list[str] = []
    if dressing and not any(skip in dressing for skip in DRESSING_SKIP):
        dressing_names.append(dressing)
    for t in list(rest_toppings):
        if "드레싱" in t or t.endswith("소스"):
            dressing_names.append(t)
            rest_toppings.remove(t)

    for dname in dressing_names:
        ding = resolve_ing(dname, ing_by)
        if ding:
            add_row(ding, ROLE_DEFAULT, can_remove=True, qty=50)
        else:
            unresolved.append(dname)

    cores: list[str] = []
    defaults: list[str] = []
    for t in rest_toppings:
        if is_core_ing(t, menu_name, toppings):
            cores.append(t)
        else:
            defaults.append(t)

    for t in cores:
        ing = resolve_ing(t, ing_by)
        if ing:
            add_row(ing, ROLE_CORE, can_remove=False)
        else:
            unresolved.append(t)

    for t in defaults:
        ing = resolve_ing(t, ing_by)
        if ing:
            add_row(ing, ROLE_DEFAULT, can_remove=True)
        else:
            unresolved.append(t)

    return rows, nid, unresolved


def clone_menu_opt_policy(
    policies: list[dict[str, Any]], template_id: int, new_menu_id: int
) -> list[dict[str, Any]]:
    return [
        {
            "menu_id": new_menu_id,
            "policy_id": int(p["policy_id"]),
            "sort_no": int(p["sort_no"]),
            "required": bool(p.get("required")),
            "priority": int(p.get("priority") or 0),
        }
        for p in policies
        if int(p["menu_id"]) == template_id
    ]


def menu_allergens_from_row(row: dict[str, str], allergens: list[dict[str, Any]]) -> set[str]:
    by_name = {a["name"]: int(a["id"]) for a in allergens}
    names: set[str] = set()
    for col, val in row.items():
        if not col.startswith("알레르기_"):
            continue
        if (val or "").strip() != "●":
            continue
        aname = col.removeprefix("알레르기_").strip()
        if aname in by_name:
            names.add(aname)
    listed = (row.get("알레르기 목록") or "").strip()
    if listed:
        for part in re.split(r"[,·]", listed):
            name = part.strip()
            if name in by_name:
                names.add(name)
    return names


def sync_ing_allergens_for_menu(
    menu_ing_rows: list[dict[str, Any]],
    allergen_names: set[str],
    ings: list[dict[str, Any]],
    ing_allergen: list[dict[str, Any]],
    allergens: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not allergen_names:
        return []
    ing_name_by_id = {int(i["id"]): i["name"] for i in ings}
    allergen_id_by_name = {a["name"]: int(a["id"]) for a in allergens}
    existing = {
        (int(l["ing_id"]), int(l["allergen_id"])) for l in ing_allergen
    }
    added: list[dict[str, Any]] = []
    next_link_id = next_id(ing_allergen)

    covered_by_menu: set[str] = set()
    for mi in menu_ing_rows:
        ing_id = int(mi["ing_id"])
        iname = ing_name_by_id.get(ing_id, "")
        compact = strip_name(iname)
        for aname in allergen_names:
            hints = ALLERGEN_ING_HINTS.get(aname, (aname,))
            if not any(strip_name(h) in compact or compact in strip_name(h) for h in hints):
                continue
            covered_by_menu.add(aname)
            aid = allergen_id_by_name.get(aname)
            if aid is None or (ing_id, aid) in existing:
                continue
            link = {"id": next_link_id, "ing_id": ing_id, "allergen_id": aid}
            ing_allergen.append(link)
            existing.add((ing_id, aid))
            added.append(link)
            next_link_id += 1

    # CSV 메뉴 알레르기가 재료 힌트로 매칭되지 않으면 역할별 대표 재료에 연결
    for aname in allergen_names:
        if aname in covered_by_menu:
            continue
        aid = allergen_id_by_name.get(aname)
        if aid is None:
            continue
        role = ALLERGEN_FALLBACK_ROLE.get(aname)
        target = None
        if role is not None:
            target = next((mi for mi in menu_ing_rows if int(mi["role_id"]) == role), None)
        if target is None and menu_ing_rows:
            target = menu_ing_rows[0]
        if not target:
            continue
        ing_id = int(target["ing_id"])
        if (ing_id, aid) in existing:
            continue
        link = {"id": next_link_id, "ing_id": ing_id, "allergen_id": aid}
        ing_allergen.append(link)
        existing.add((ing_id, aid))
        added.append(link)
        next_link_id += 1
    return added


def ensure_vegan_tag(tags: list[dict[str, Any]]) -> None:
    if any(int(t["id"]) == 240 for t in tags):
        return
    tags.append(
        {
            "id": 240,
            "code": "VEGAN",
            "name": "VEGAN",
            "color_hex": "#059669",
            "active": True,
        }
    )


def build_description(row: dict[str, str]) -> str:
    csv_desc = (row.get("설명") or "").strip()
    if csv_desc:
        return csv_desc
    topping = (row.get("토핑") or "").strip()
    dressing = (row.get("추천/기본 드레싱") or "").strip()
    parts = []
    if topping:
        parts.append(topping)
    if dressing and "미제공" not in dressing:
        parts.append(f"기본 드레싱: {dressing}")
    return " · ".join(parts)


def load_audit_images() -> dict[str, str]:
    if not AUDIT_MENUS.exists():
        return {}
    data = load_json(AUDIT_MENUS)
    out: dict[str, str] = {}
    for item in data:
        name = item.get("name_ko") or item.get("name") or ""
        url = item.get("image_url") or ""
        if name and url.startswith("http"):
            out[strip_name(name)] = url.replace(":443", "")
    return out


def asset_exists(base: Path, ing_id: int) -> bool:
    """Check png/jpg/webp for photos/menu; svg for icons."""
    if "icons" in str(base):
        return (base / f"{ing_id}.svg").exists()
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        if (base / f"{ing_id}{ext}").exists():
            return True
    return False


def download_url(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read()
        if len(data) < 500:
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except Exception as exc:
        print(f"  download fail {dest.name}: {exc}")
        return False


def ensure_ingredient_icon(ing_id: int, ing_name: str) -> bool:
    icon_dir = KIOSK_ASSETS / "ingredients" / "icons"
    dest = icon_dir / f"{ing_id}.svg"
    if dest.exists() and dest.stat().st_size > 100:
        return True
    gen_script = Path(__file__).with_name("generate_ingredient_icons.py")
    if gen_script.exists():
        subprocess.run([sys.executable, str(gen_script)], check=False, cwd=str(ROOT))
    if dest.exists():
        return True
    # minimal fallback icon
    body = (
        f'<text x="24" y="30" text-anchor="middle" font-size="10" '
        f'fill="currentColor">{ing_name[:4]}</text>'
    )
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" '
        'fill="none" stroke="currentColor" stroke-width="2">\n'
        f"  <circle cx=\"24\" cy=\"24\" r=\"20\"/>\n  {body}\n</svg>\n"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(svg, encoding="utf-8")
    return True


def clone_menu_ing(
    menu_ing: list[dict[str, Any]], template_id: int, new_menu_id: int, start_id: int
) -> tuple[list[dict[str, Any]], int]:
    added = []
    nid = start_id
    for mi in menu_ing:
        if int(mi["menu_id"]) != template_id:
            continue
        row = dict(mi)
        row["id"] = nid
        row["menu_id"] = new_menu_id
        added.append(row)
        nid += 1
    return added, nid


def apply_seed(
    csv_rows: list[dict[str, str]], audit_images: dict[str, str]
) -> dict[str, Any]:
    menus = load_json(SEED / "menu.json")
    menu_nutr = load_json(SEED / "menu_nutr.json")
    menu_ing = load_json(SEED / "menu_ing.json")
    menu_tag = load_json(SEED / "menu_tag.json")
    menu_opt_policy = load_json(SEED / "menu_opt_policy.json")
    ings = load_json(SEED / "ing.json")
    ing_nutr = load_json(SEED / "ing_nutr.json")
    ing_allergen = load_json(SEED / "ing_allergen.json")
    allergens = load_json(SEED / "allergen.json")
    tags = load_json(SEED / "tag.json")
    ensure_vegan_tag(tags)

    menu_by = index_menus(menus)
    nutr_by_menu = {int(r["menu_id"]): r for r in menu_nutr}
    ing_by = index_ings(ings)
    policy_by_menu: dict[int, int] = defaultdict(int)
    for p in menu_opt_policy:
        policy_by_menu[int(p["menu_id"])] += 1
    menus_with_policy = set(policy_by_menu)

    report: dict[str, Any] = {
        "updated_menus": [],
        "created_menus": [],
        "created_ings": [],
        "synced_menu_ing": [],
        "synced_menu_opt_policy": [],
        "synced_menu_tag": [],
        "ing_allergen_added": [],
        "unresolved_ings": [],
        "images_downloaded": [],
        "images_missing": [],
    }

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    csv_touched_menu_ids: set[int] = set()

    # --- new ingredients ---
    for spec in NEW_INGREDIENTS:
        if lookup_menu(ing_by, spec["name"]):
            continue
        iid = next_id(ings)
        ings.append({"id": iid, "name": spec["name"], "type_id": spec["type_id"], "sold_out": False})
        ing_nutr.append(
            {
                "id": iid,
                "ing_id": iid,
                "serving_g": None,
                "kcal": None,
                "carb_g": None,
                "sugar_g": None,
                "protein_g": None,
                "fat_g": None,
                "saturated_fat_g": None,
                "sodium_mg": None,
                "source_id": None,
            }
        )
        ing_by.setdefault(strip_name(spec["name"]), []).append(ings[-1])
        report["created_ings"].append({"ing_id": iid, "name": spec["name"]})

    next_menu_id = next_id(menus)
    next_mn_id = next_id(menu_nutr)
    next_mi_id = next_id(menu_ing)
    next_mt_id = next_id(menu_tag) if menu_tag else 1

    for row in csv_rows:
        name = (row.get("메뉴명") or "").strip()
        cat_label = (row.get("카테고리") or "").strip()
        hits = lookup_menu(menu_by, name)
        if hits:
            hits = [pick_canonical_menu(hits, policy_by_menu)]

        if not hits:
            template_id = TEMPLATE_MENU.get(cat_label, 1978)
            template = next(m for m in menus if int(m["id"]) == template_id)
            mid = next_menu_id
            next_menu_id += 1
            price = int(template.get("price") or 8900)
            desc = build_description(row) or (row.get("설명") or "")
            menu_row = {
                "id": mid,
                "cat_id": CAT_MAP.get(cat_label, 233),
                "name": name,
                "price": price,
                "image_url": f"/assets/menu/{mid}.png",
                "description": desc,
                "sold_out": False,
                "created_at": now,
                "updated_at": now,
            }
            menus.append(menu_row)
            menu_by.setdefault(strip_name(name), []).append(menu_row)
            hits = [menu_row]

            fields = nutrition_from_row(row)
            mn = {
                "id": next_mn_id,
                "menu_id": mid,
                "source_id": 41,
                **fields,
            }
            next_mn_id += 1
            menu_nutr.append(mn)
            nutr_by_menu[mid] = mn

            if mid not in menus_with_policy:
                cloned_policies = clone_menu_opt_policy(menu_opt_policy, template_id, mid)
                menu_opt_policy.extend(cloned_policies)
                menus_with_policy.add(mid)
                policy_by_menu[mid] = len(cloned_policies)
                report["synced_menu_opt_policy"].append({"menu_id": mid, "name": name, "count": len(cloned_policies)})

            report["created_menus"].append({"menu_id": mid, "name": name})

        fields = nutrition_from_row(row)
        desc = build_description(row) or (row.get("설명") or "").strip()
        for menu in hits:
            mid = int(menu["id"])
            csv_touched_menu_ids.add(mid)
            menu["cat_id"] = CAT_MAP.get(cat_label, menu.get("cat_id", 233))
            if desc:
                menu["description"] = desc
            menu["updated_at"] = now
            mn = nutr_by_menu.get(mid)
            if mn is None:
                mn = {"id": next_mn_id, "menu_id": mid, "source_id": 41}
                next_mn_id += 1
                menu_nutr.append(mn)
                nutr_by_menu[mid] = mn
            before_kcal = mn.get("kcal")
            mn.update(fields)
            mn["source_id"] = mn.get("source_id") or 41
            if before_kcal != mn.get("kcal"):
                report["updated_menus"].append(
                    {"menu_id": mid, "name": name, "kcal": mn.get("kcal")}
                )

            # menu_ing from CSV (replace existing rows for this menu)
            built, next_mi_id, unresolved = build_menu_ing_from_csv(
                row, mid, name, cat_label, ing_by, next_mi_id
            )
            if unresolved:
                report["unresolved_ings"].append({"menu_id": mid, "name": name, "items": unresolved})
            menu_ing = [mi for mi in menu_ing if int(mi["menu_id"]) != mid]
            menu_ing.extend(built)
            report["synced_menu_ing"].append({"menu_id": mid, "name": name, "count": len(built)})

            # menu_opt_policy from category template if missing
            if mid not in menus_with_policy:
                template_id = TEMPLATE_MENU.get(cat_label, 1978)
                cloned_policies = clone_menu_opt_policy(menu_opt_policy, template_id, mid)
                if cloned_policies:
                    menu_opt_policy.extend(cloned_policies)
                    menus_with_policy.add(mid)
                    policy_by_menu[mid] = len(cloned_policies)
                    report["synced_menu_opt_policy"].append(
                        {"menu_id": mid, "name": name, "count": len(cloned_policies)}
                    )

            # menu_tag from CSV tags
            menu_tag = [mt for mt in menu_tag if int(mt["menu_id"]) != mid]
            for tag_code in re.split(r"[|]", (row.get("태그") or "").strip()):
                tag_code = tag_code.strip()
                tid = TAG_MAP.get(tag_code)
                if tid:
                    menu_tag.append({"id": next_mt_id, "menu_id": mid, "tag_id": tid})
                    next_mt_id += 1
            report["synced_menu_tag"].append({"menu_id": mid, "name": name})

            # ing_allergen hints from CSV allergy marks
            allergen_names = menu_allergens_from_row(row, allergens)
            added_links = sync_ing_allergens_for_menu(
                built, allergen_names, ings, ing_allergen, allergens
            )
            if added_links:
                report["ing_allergen_added"].append(
                    {"menu_id": mid, "name": name, "count": len(added_links)}
                )

    report["csv_touched_menu_ids"] = sorted(csv_touched_menu_ids)

    menu_nutr = dedupe_menu_nutr(menu_nutr)
    menu_ing = dedupe_menu_ing(menu_ing)
    menu_tag = dedupe_menu_tag(menu_tag)
    menu_opt_policy = dedupe_menu_opt_policy(menu_opt_policy)
    ing_allergen = dedupe_ing_allergen(ing_allergen)

    dump_json(SEED / "menu.json", menus)
    dump_json(SEED / "menu_nutr.json", menu_nutr)
    dump_json(SEED / "menu_ing.json", menu_ing)
    dump_json(SEED / "menu_tag.json", menu_tag)
    dump_json(SEED / "menu_opt_policy.json", menu_opt_policy)
    dump_json(SEED / "ing.json", ings)
    dump_json(SEED / "ing_nutr.json", ing_nutr)
    dump_json(SEED / "ing_allergen.json", ing_allergen)
    dump_json(SEED / "tag.json", tags)

    # --- images ---
    menu_dir = KIOSK_ASSETS / "menu"
    photo_dir = KIOSK_ASSETS / "ingredients" / "photos"
    menu_dir.mkdir(parents=True, exist_ok=True)
    photo_dir.mkdir(parents=True, exist_ok=True)

    for menu in menus:
        mid = int(menu["id"])
        if asset_exists(menu_dir, mid):
            continue
        url = audit_images.get(strip_name(menu["name"]))
        if not url:
            report["images_missing"].append({"type": "menu", "id": mid, "name": menu["name"]})
            continue
        dest = menu_dir / f"{mid}.png"
        if download_url(url, dest):
            report["images_downloaded"].append({"type": "menu", "id": mid, "path": str(dest)})

    salady_dl = Path(__file__).with_name("download_ingredient_images_salady.py")
    if salady_dl.exists():
        subprocess.run([sys.executable, str(salady_dl)], check=False, cwd=str(ROOT.parent))

    for ing in ings:
        iid = int(ing["id"])
        iname = ing["name"]
        if not asset_exists(photo_dir, iid):
            src = ROOT / "images" / "ingredient-salady"
            copied = False
            if src.exists():
                for f in src.glob("*"):
                    if strip_name(iname) in strip_name(f.stem):
                        ext = f.suffix or ".jpg"
                        dest = photo_dir / f"{iid}{ext}"
                        shutil.copy2(f, dest)
                        report["images_downloaded"].append(
                            {"type": "ing_photo", "id": iid, "path": str(dest)}
                        )
                        copied = True
                        break
            if not copied:
                report["images_missing"].append({"type": "ing_photo", "id": iid, "name": iname})
        ensure_ingredient_icon(iid, iname)

    return report


def apply_db(
    menus: list,
    menu_nutr: list,
    menu_ing: list,
    menu_tag: list,
    menu_opt_policy: list,
    ings: list,
    ing_nutr: list,
    ing_allergen: list,
    csv_touched_menu_ids: list[int] | None = None,
) -> dict:
    import pymysql

    load_backend_env()
    url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    if not url or not user:
        raise RuntimeError("DB_URL / DB_USERNAME required")

    host, port, db = parse_jdbc_url(url)
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password or "",
        database=db,
        charset="utf8mb4",
        autocommit=False,
    )
    stats = {
        "menu": 0,
        "menu_nutr": 0,
        "menu_ing": 0,
        "menu_tag": 0,
        "menu_opt_policy": 0,
        "ing": 0,
        "ing_nutr": 0,
        "ing_allergen": 0,
    }
    touched = set(csv_touched_menu_ids or [])
    seed_menu_ids = {int(m["id"]) for m in menus}

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM menu")
            existing_menus = {int(r[0]) for r in cur.fetchall()}
            cur.execute("SELECT id FROM ing")
            existing_ings = {int(r[0]) for r in cur.fetchall()}

            cur.execute(
                "INSERT IGNORE INTO tag (id, code, name, color_hex, active) "
                "VALUES (240, 'VEGAN', 'VEGAN', '#059669', 1)"
            )

            for m in menus:
                mid = int(m["id"])
                cols = ["id", "cat_id", "name", "price", "image_url", "description", "sold_out"]
                if mid not in existing_menus:
                    sql = (
                        f"INSERT INTO menu ({', '.join('`'+c+'`' for c in cols)}) "
                        f"VALUES ({', '.join(['%s']*len(cols))})"
                    )
                    cur.execute(sql, tuple(m.get(c) for c in cols))
                else:
                    cur.execute(
                        "UPDATE menu SET cat_id=%s, name=%s, price=%s, image_url=%s, "
                        "description=%s, sold_out=%s, updated_at=NOW() WHERE id=%s",
                        (
                            m.get("cat_id"),
                            m.get("name"),
                            m.get("price"),
                            m.get("image_url"),
                            m.get("description"),
                            m.get("sold_out"),
                            mid,
                        ),
                    )
                stats["menu"] += 1

            nutr_by_menu = {int(r["menu_id"]): r for r in dedupe_menu_nutr(menu_nutr)}
            for mid, r in nutr_by_menu.items():
                if mid not in existing_menus and mid not in seed_menu_ids:
                    continue
                cur.execute("DELETE FROM menu_nutr WHERE menu_id=%s AND id<>%s", (mid, r["id"]))
                cur.execute(
                    """
                    INSERT INTO menu_nutr
                      (id, menu_id, kcal, protein_g, carb_g, fat_g, sodium_mg,
                       source_id, serving_g, sugar_g, saturated_fat_g)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                      menu_id=VALUES(menu_id),
                      kcal=VALUES(kcal), protein_g=VALUES(protein_g), carb_g=VALUES(carb_g),
                      fat_g=VALUES(fat_g), sodium_mg=VALUES(sodium_mg), source_id=VALUES(source_id),
                      serving_g=VALUES(serving_g), sugar_g=VALUES(sugar_g),
                      saturated_fat_g=VALUES(saturated_fat_g)
                    """,
                    (
                        r.get("id"),
                        r.get("menu_id"),
                        r.get("kcal"),
                        r.get("protein_g"),
                        r.get("carb_g"),
                        r.get("fat_g"),
                        r.get("sodium_mg"),
                        r.get("source_id"),
                        r.get("serving_g"),
                        r.get("sugar_g"),
                        r.get("saturated_fat_g"),
                    ),
                )
                stats["menu_nutr"] += 1

            for table, rows, cols, key in [
                ("ing", ings, ["id", "name", "type_id", "sold_out"], "ing"),
                (
                    "ing_nutr",
                    ing_nutr,
                    [
                        "id",
                        "ing_id",
                        "serving_g",
                        "kcal",
                        "carb_g",
                        "sugar_g",
                        "protein_g",
                        "fat_g",
                        "saturated_fat_g",
                        "sodium_mg",
                        "source_id",
                    ],
                    "ing_nutr",
                ),
            ]:
                for r in rows:
                    rid = int(r["id"])
                    if table == "ing" and rid not in existing_ings:
                        sql = (
                            f"INSERT INTO ing ({', '.join('`'+c+'`' for c in cols)}) "
                            f"VALUES ({', '.join(['%s']*len(cols))})"
                        )
                        cur.execute(sql, tuple(r.get(c) for c in cols))
                    elif table == "ing_nutr":
                        cur.execute(
                            f"""
                            INSERT INTO ing_nutr ({', '.join('`'+c+'`' for c in cols)})
                            VALUES ({', '.join(['%s']*len(cols))})
                            ON DUPLICATE KEY UPDATE
                              serving_g=VALUES(serving_g), kcal=VALUES(kcal),
                              carb_g=VALUES(carb_g), sugar_g=VALUES(sugar_g),
                              protein_g=VALUES(protein_g), fat_g=VALUES(fat_g),
                              saturated_fat_g=VALUES(saturated_fat_g),
                              sodium_mg=VALUES(sodium_mg), source_id=VALUES(source_id)
                            """,
                            tuple(r.get(c) for c in cols),
                        )
                    stats[key] += 1

            if touched:
                placeholders = ",".join(["%s"] * len(touched))
                for table in ("menu_ing", "menu_tag", "menu_opt_policy"):
                    cur.execute(
                        f"DELETE FROM `{table}` WHERE menu_id IN ({placeholders})",
                        tuple(touched),
                    )

                for mi in dedupe_menu_ing(
                    [r for r in menu_ing if int(r["menu_id"]) in touched]
                ):
                    cur.execute(
                        "INSERT INTO menu_ing "
                        "(id, menu_id, ing_id, role_id, quantity, unit_id, is_default, can_remove, sort_no) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                            mi.get("id"),
                            mi.get("menu_id"),
                            mi.get("ing_id"),
                            mi.get("role_id"),
                            mi.get("quantity"),
                            mi.get("unit_id"),
                            mi.get("is_default"),
                            mi.get("can_remove"),
                            mi.get("sort_no"),
                        ),
                    )
                    stats["menu_ing"] += 1

                for mt in dedupe_menu_tag(
                    [r for r in menu_tag if int(r["menu_id"]) in touched]
                ):
                    cur.execute(
                        "INSERT INTO menu_tag (id, menu_id, tag_id) VALUES (%s,%s,%s)",
                        (mt.get("id"), mt.get("menu_id"), mt.get("tag_id")),
                    )
                    stats["menu_tag"] += 1

                for mp in dedupe_menu_opt_policy(
                    [r for r in menu_opt_policy if int(r["menu_id"]) in touched]
                ):
                    cur.execute(
                        "INSERT INTO menu_opt_policy "
                        "(menu_id, policy_id, sort_no, required, priority) "
                        "VALUES (%s,%s,%s,%s,%s)",
                        (
                            mp.get("menu_id"),
                            mp.get("policy_id"),
                            mp.get("sort_no"),
                            1 if mp.get("required") else 0,
                            mp.get("priority") or 0,
                        ),
                    )
                    stats["menu_opt_policy"] += 1

            for link in dedupe_ing_allergen(ing_allergen):
                cur.execute(
                    "INSERT IGNORE INTO ing_allergen (id, ing_id, allergen_id) VALUES (%s,%s,%s)",
                    (link.get("id"), link.get("ing_id"), link.get("allergen_id")),
                )
                stats["ing_allergen"] += 1

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--apply-db", action="store_true")
    parser.add_argument("--skip-seed-write", action="store_true")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"missing csv: {args.csv}", file=sys.stderr)
        return 1

    with args.csv.open(encoding="utf-8-sig", newline="") as f:
        csv_rows = list(csv.DictReader(f))

    audit_images = load_audit_images()
    if args.skip_seed_write:
        report = {"skipped_seed_write": True}
    else:
        report = apply_seed(csv_rows, audit_images)

    if args.apply_db:
        menus = load_json(SEED / "menu.json")
        report["db"] = apply_db(
            menus,
            load_json(SEED / "menu_nutr.json"),
            load_json(SEED / "menu_ing.json"),
            load_json(SEED / "menu_tag.json"),
            load_json(SEED / "menu_opt_policy.json"),
            load_json(SEED / "ing.json"),
            load_json(SEED / "ing_nutr.json"),
            load_json(SEED / "ing_allergen.json"),
            report.get("csv_touched_menu_ids"),
        )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    dump_json(REPORT_PATH, report)
    print(f"report -> {REPORT_PATH}")
    print(
        "created_menus=%s updated=%s created_ings=%s images=%s missing=%s"
        % (
            len(report.get("created_menus", [])),
            len(report.get("updated_menus", [])),
            len(report.get("created_ings", [])),
            len(report.get("images_downloaded", [])),
            len(report.get("images_missing", [])),
        )
    )
    if report.get("db"):
        print("db:", report["db"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
