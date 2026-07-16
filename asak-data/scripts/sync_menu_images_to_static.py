#!/usr/bin/env python3
"""asak-data 메뉴 이미지 → ASAK-back static + Kiosk/Admin public 동기화.

정본 URL: /assets/menu/{id}.png
소스 우선순위: images/menu-trimmed → images/menu → images/original/{id}_*
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # asak-data
ASAK = ROOT.parent
WORKSPACE = ASAK.parent

SEED = ROOT / "seed" / "menu.json"
TRIMMED = ROOT / "images" / "menu-trimmed"
MENU = ROOT / "images" / "menu"
ORIGINAL = ROOT / "images" / "original"

BACKEND_STATIC = (
    WORKSPACE / "ASAK-back" / "src" / "main" / "resources" / "static" / "assets" / "menu"
)
KIOSK_PUBLIC = WORKSPACE / "ASAK-Kiosk" / "public" / "assets" / "menu"
ADMIN_PUBLIC = WORKSPACE / "ASAK-Admin" / "public" / "assets" / "menu"

PREFIX = "/assets/menu/"


def find_source(menu_id: int) -> Path | None:
    for folder in (TRIMMED, MENU):
        png = folder / f"{menu_id}.png"
        if png.exists() and png.stat().st_size > 0:
            return png
        for ext in (".jpg", ".jpeg", ".webp"):
            p = folder / f"{menu_id}{ext}"
            if p.exists() and p.stat().st_size > 0:
                return p
    matches = sorted(ORIGINAL.glob(f"{menu_id}_*"))
    return matches[0] if matches else None


def main() -> None:
    menus = json.loads(SEED.read_text(encoding="utf-8"))
    targets = [BACKEND_STATIC, KIOSK_PUBLIC]
    if ADMIN_PUBLIC.parent.parent.exists():
        targets.append(ADMIN_PUBLIC)
    for t in targets:
        t.mkdir(parents=True, exist_ok=True)

    ok = missing = 0
    for menu in menus:
        mid = menu["id"]
        src = find_source(mid)
        if not src:
            missing += 1
            continue
        ext = src.suffix.lower() or ".png"
        # API 계약은 png 위주지만 원본 확장자 유지
        filename = f"{mid}{ext}"
        for t in targets:
            shutil.copy2(src, t / filename)
        menu["image_url"] = f"{PREFIX}{filename}"
        # snake_case seed 호환
        if "imageUrl" in menu:
            menu["imageUrl"] = menu["image_url"]
        ok += 1

    SEED.write_text(json.dumps(menus, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"synced {ok} menus → {PREFIX}{{id}}.ext")
    print(f"  source prefer: menu-trimmed > menu > original")
    print(f"  backend: {BACKEND_STATIC}")
    print(f"  kiosk:   {KIOSK_PUBLIC}")
    if missing:
        print(f"  missing: {missing}")


if __name__ == "__main__":
    main()
