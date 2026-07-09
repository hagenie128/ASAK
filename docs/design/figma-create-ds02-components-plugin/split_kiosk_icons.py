#!/usr/bin/env python3
"""Split 4x4 kiosk icon sheet into individual PNGs (black #000 -> transparent)."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ICON_NAMES = [
    "home",
    "takeout",
    "menu-grid",
    "customize",
    "sold-out",
    "cart",
    "order-confirm",
    "card-pay",
    "qr-pay",
    "points",
    "coupon",
    "complete",
    "receipt",
    "accessibility",
    "language",
    "back",
]

GRID = 4
BLACK = (0, 0, 0)

PLUGIN_DIR = Path(__file__).resolve().parent
DEFAULT_SRC = PLUGIN_DIR / "assets" / "asak-kiosk-icons-4x4.png"
DEFAULT_OUT = PLUGIN_DIR / "assets" / "icons"

# PascalCase keys used in code.js KIOSK_ICON_SPECS (row-major)
SPEC_NAME_BY_FILE = {
    "home": "Home",
    "takeout": "Takeout",
    "menu-grid": "MenuGrid",
    "customize": "Customize",
    "sold-out": "SoldOut",
    "cart": "Cart",
    "order-confirm": "OrderConfirm",
    "card-pay": "CardPay",
    "qr-pay": "QRPay",
    "points": "Points",
    "coupon": "Coupon",
    "complete": "Complete",
    "receipt": "Receipt",
    "accessibility": "Accessibility",
    "language": "Language",
    "back": "Back",
}


def black_to_transparent(im: Image.Image) -> Image.Image:
    rgba = im.convert("RGBA")
    pixels = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if (r, g, b) == BLACK:
                pixels[x, y] = (0, 0, 0, 0)
            elif a == 0:
                pixels[x, y] = (r, g, b, 255)
    return rgba


def split_sheet(src: Path, out_dir: Path) -> list[Path]:
    if len(ICON_NAMES) != GRID * GRID:
        raise ValueError("ICON_NAMES must contain 16 entries")
    sheet = Image.open(src)
    w, h = sheet.size
    if w % GRID or h % GRID:
        raise ValueError(f"Sheet size {w}x{h} is not divisible by {GRID}")
    cell_w, cell_h = w // GRID, h // GRID
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for idx, stem in enumerate(ICON_NAMES):
        row, col = divmod(idx, GRID)
        box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
        tile = black_to_transparent(sheet.crop(box))
        dest = out_dir / f"{stem}.png"
        tile.save(dest, "PNG", optimize=True)
        written.append(dest)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC, help="4x4 icon sheet PNG")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory")
    args = parser.parse_args()
    if not args.src.is_file():
        raise SystemExit(f"Missing source image: {args.src}")
    paths = split_sheet(args.src, args.out)
    print(f"Source: {args.src}")
    print(f"Output: {args.out.resolve()}")
    for p in paths:
        print(f"  {p.name}\t{p.stat().st_size} bytes")


if __name__ == "__main__":
    main()
