#!/usr/bin/env python3
"""Build unified ingredient assets: icon + photo by ingredient_id, catalog, Kiosk public copy."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASAK = ROOT.parent
WORKSPACE = ASAK.parent

SEED = ROOT / "seed" / "ingredient.json"
CODES = ROOT / "seed" / "common_code.json"
ICON_MAP = ROOT / "images" / "ingredient-icons" / "mapping.json"
ICON_SVG = ROOT / "images" / "ingredient-icons" / "svg"
SALADY_MAP = ROOT / "images" / "ingredient-salady" / "mapping.json"
SALADY_DIR = ROOT / "images" / "ingredient-salady"

OUT = ROOT / "images" / "ingredient-assets"
OUT_ICON = OUT / "icons" / "by-id"
OUT_PHOTO = OUT / "photos" / "by-id"
CATALOG = OUT / "catalog.json"
SEED_ASSETS = ROOT / "seed" / "ingredient_assets.json"

# 정본: Spring Boot static (메뉴 /assets/menu 와 같은 규칙)
BACKEND_STATIC = (
    WORKSPACE
    / "ASAK-back"
    / "src"
    / "main"
    / "resources"
    / "static"
    / "assets"
    / "ingredients"
)
# Vite mock/로컬 전용 보조 복사
KIOSK_PUBLIC = WORKSPACE / "ASAK-Kiosk" / "public" / "assets" / "ingredients"
ADMIN_PUBLIC = WORKSPACE / "ASAK-Admin" / "public" / "assets" / "ingredients"


def run_generate_icons() -> None:
    gen = Path(__file__).with_name("generate_ingredient_icons.py")
    # ensure icons exist / refreshed
    import importlib.util

    spec = importlib.util.spec_from_file_location("gen_icons", gen)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    mod.main()


def type_name(type_id: int, codes: list[dict]) -> str:
    for c in codes:
        if c.get("id") == type_id:
            return c.get("name") or ""
    return ""


def ensure_dirs(*roots: Path) -> None:
    for root in roots:
        root.mkdir(parents=True, exist_ok=True)
        (root / "icons").mkdir(parents=True, exist_ok=True)
        (root / "photos").mkdir(parents=True, exist_ok=True)


def copy_to_targets(src: Path, relative_name: str, *roots: Path) -> None:
    for root in roots:
        dest = root / relative_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def main() -> None:
    run_generate_icons()

    ingredients = json.loads(SEED.read_text(encoding="utf-8"))
    codes = json.loads(CODES.read_text(encoding="utf-8"))
    icon_map = {
        row["ingredient_id"]: row
        for row in json.loads(ICON_MAP.read_text(encoding="utf-8"))["items"]
    }
    salady_matched = {}
    if SALADY_MAP.exists():
        for row in json.loads(SALADY_MAP.read_text(encoding="utf-8")).get("matched", []):
            salady_matched[row["ingredient_id"]] = row

    OUT_ICON.mkdir(parents=True, exist_ok=True)
    OUT_PHOTO.mkdir(parents=True, exist_ok=True)
    publish_roots = [BACKEND_STATIC, KIOSK_PUBLIC]
    if ADMIN_PUBLIC.parent.parent.exists():
        publish_roots.append(ADMIN_PUBLIC)
    ensure_dirs(*publish_roots)

    catalog = []
    photo_n = icon_n = 0

    for ing in ingredients:
        iid = ing["id"]
        icon_row = icon_map.get(iid) or {}
        icon_key = icon_row.get("icon_key") or "default"
        src_svg = ICON_SVG / f"{icon_key}.svg"
        if not src_svg.exists():
            src_svg = ICON_SVG / "default.svg"

        dest_svg = OUT_ICON / f"{iid}.svg"
        shutil.copy2(src_svg, dest_svg)
        copy_to_targets(src_svg, f"icons/{iid}.svg", *publish_roots)
        icon_n += 1

        photo_rel = None
        photo_url = None
        salady = salady_matched.get(iid)
        if salady and salady.get("local_file"):
            src_photo = SALADY_DIR / salady["local_file"]
            if src_photo.exists() and src_photo.stat().st_size > 1000:
                ext = src_photo.suffix.lower() or ".jpg"
                dest_name = f"{iid}{ext}"
                shutil.copy2(src_photo, OUT_PHOTO / dest_name)
                copy_to_targets(src_photo, f"photos/{dest_name}", *publish_roots)
                photo_rel = f"photos/by-id/{dest_name}"
                photo_url = f"/assets/ingredients/photos/{dest_name}"
                photo_n += 1

        entry = {
            "ingredientId": iid,
            "name": ing["name"],
            "typeId": ing["type_id"],
            "typeName": type_name(ing["type_id"], codes),
            "iconKey": icon_key,
            "iconPath": f"icons/by-id/{iid}.svg",
            "iconUrl": f"/assets/ingredients/icons/{iid}.svg",
            "photoPath": photo_rel,
            "photoUrl": photo_url,
            "hasPhoto": photo_rel is not None,
            "kcal": ing.get("kcal"),
            "isSoldOut": ing.get("is_sold_out", False),
        }
        catalog.append(entry)

    payload = {
        "version": 1,
        "note": "아이콘=ASAK 제작 SVG. 사진=샐러디 공개 페이지 참고(학습용). URL은 백엔드 static /assets/ingredients/* 기준.",
        "serveFrom": "ASAK-back/src/main/resources/static/assets/ingredients",
        "counts": {
            "ingredients": len(catalog),
            "withIcon": icon_n,
            "withPhoto": photo_n,
        },
        "items": catalog,
    }
    CATALOG.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    SEED_ASSETS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    for root in publish_roots:
        (root / "catalog.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # preview
    rows = []
    for e in catalog:
        photo = (
            f'<img class="photo" src="../ingredient-assets/{e["photoPath"]}" alt=""/>'
            if e["hasPhoto"]
            else '<div class="photo empty">no photo</div>'
        )
        rows.append(
            f'<div class="card">{photo}'
            f'<img class="icon" src="../ingredient-assets/{e["iconPath"]}" alt=""/>'
            f'<div class="meta"><b>{e["name"]}</b><span>#{e["ingredientId"]} · {e["typeName"]}</span>'
            f'<code>{e["iconKey"]}</code></div></div>'
        )
    html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"/><title>ASAK Ingredient Assets</title>
<style>
body{{font-family:Pretendard,system-ui,sans-serif;margin:24px;background:#f6f6f3;color:#1a1a1a}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}
.card{{background:#fff;border:1px solid #e6e6e1;border-radius:14px;padding:12px;display:grid;grid-template-columns:72px 40px 1fr;gap:10px;align-items:center}}
.photo{{width:72px;height:72px;object-fit:cover;border-radius:10px;background:#eee}}
.photo.empty{{display:flex;align-items:center;justify-content:center;font-size:10px;color:#999}}
.icon{{width:36px;height:36px;color:#2f6b3a}}
.meta{{display:flex;flex-direction:column;gap:2px;font-size:12px}}
code{{color:#888;font-size:10px}}
</style></head><body>
<h1>ASAK Ingredient Assets</h1>
<p>icons {icon_n} · photos {photo_n} / {len(catalog)}</p>
<p>Backend static: <code>ASAK-back/.../static/assets/ingredients</code></p>
<div class="grid">{"".join(rows)}</div>
</body></html>"""
    (OUT / "preview.html").write_text(html, encoding="utf-8")

    readme_lines = [
        "# ingredient-assets — 재료 아이콘 + 사진 통합팩",
        "",
        "## 어디에 두나 (정본)",
        "",
        "메뉴 사진과 같이 **백엔드 static**이 정본입니다.",
        "",
        "| 역할 | 경로 |",
        "|---|---|",
        "| **정본 (API URL)** | `ASAK-back/src/main/resources/static/assets/ingredients/` |",
        "| 브라우저 URL | `/assets/ingredients/icons/{id}.svg` · `/assets/ingredients/photos/{id}.ext` |",
        "| 소스 보관 | `asak-data/images/ingredient-assets/` |",
        "| Kiosk/Admin public | Vite mock용 **보조 복사** (백엔드 안 켤 때만) |",
        "",
        "메뉴도 같은 규칙: `/assets/menu/{id}.png` → backend `static/assets/menu`.",
        "",
        "## React",
        "```jsx",
        "<img src={`/assets/ingredients/icons/${ingredientId}.svg`} alt=\"\" />",
        "```",
        "",
        "## 다시 빌드",
        "```bash",
        "python3 asak-data/scripts/build_ingredient_assets.py",
        "```",
        "",
        f"## 통계: 재료 {len(catalog)} · 아이콘 {icon_n} · 사진 {photo_n}",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")

    print(
        f"DONE ingredients={len(catalog)} icons={icon_n} photos={photo_n}\n"
        f"  backend: {BACKEND_STATIC}\n"
        f"  kiosk:   {KIOSK_PUBLIC}"
    )


if __name__ == "__main__":
    main()
