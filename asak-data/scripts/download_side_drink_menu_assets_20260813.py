#!/usr/bin/env python3
"""Download the approved side/drink menu images as /assets/menu/{id}.png."""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
from collections import deque

import requests
from PIL import Image


ASAK = Path(__file__).resolve().parents[2]
WORKSPACE = ASAK.parent
SEED = ASAK / "asak-data" / "seed-v3" / "menu.json"
TARGETS = (
    WORKSPACE / "ASAK-Kiosk" / "public" / "assets" / "menu",
    WORKSPACE / "ASAK-Admin" / "public" / "assets" / "menu",
    WORKSPACE / "ASAK-back" / "src" / "main" / "resources" / "static" / "assets" / "menu",
)
HEADERS = {"User-Agent": "ASAK menu asset sync/1.0"}


def remove_white_background_and_crop(image: Image.Image) -> Image.Image:
    """Remove only edge-connected near-white pixels, then keep a small transparent margin."""
    result = image.convert("RGBA")
    pixels = result.load()
    width, height = result.size
    visited = set()
    queue = deque()

    def is_near_white(x: int, y: int) -> bool:
        red, green, blue, alpha = pixels[x, y]
        return alpha > 0 and min(red, green, blue) >= 245 and max(red, green, blue) - min(red, green, blue) <= 12

    for x in range(width):
        queue.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        queue.extend(((0, y), (width - 1, y)))

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited or not is_near_white(x, y):
            continue
        visited.add((x, y))
        pixels[x, y] = (0, 0, 0, 0)
        for next_x, next_y in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= next_x < width and 0 <= next_y < height:
                queue.append((next_x, next_y))

    alpha = result.getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError("Background removal removed the entire image")

    left, top, right, bottom = bounds
    # Keep the original aspect ratio: forcing a square canvas leaves large side
    # gaps around tall drink containers even after their white background is gone.
    padding = 2
    crop_left = max(0, left - padding)
    crop_top = max(0, top - padding)
    crop_right = min(width, right + padding)
    crop_bottom = min(height, bottom + padding)
    return result.crop((crop_left, crop_top, crop_right, crop_bottom))


def main() -> None:
    menus = json.loads(SEED.read_text(encoding="utf-8"))
    selected = [menu for menu in menus if 10776 <= int(menu["id"]) <= 10790]
    if len(selected) != 15:
        raise RuntimeError(f"Expected 15 approved menus, found {len(selected)}")
    for target in TARGETS:
        target.mkdir(parents=True, exist_ok=True)

    for menu in selected:
        menu_id = int(menu["id"])
        url = menu.get("image_url") or ""
        if not url.startswith("http"):
            raise RuntimeError(f"Menu {menu_id} does not have an external image URL")
        response = requests.get(url, headers=HEADERS, timeout=45)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.load()
        normalized = remove_white_background_and_crop(image)
        for target in TARGETS:
            normalized.save(target / f"{menu_id}.png", format="PNG", optimize=True)
        print(f"{menu_id}.png transparent {normalized.width}x{normalized.height} {menu['name']}")


if __name__ == "__main__":
    main()
