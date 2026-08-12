#!/usr/bin/env python3
"""Kiosk public PNG — 흰/회색 스튜디오 배경 제거 + 여백 트림 (in-place).

대상:
  ASAK-Kiosk/public/assets/menu/*.png
  ASAK-Kiosk/public/assets/ingredients/photos/*.{png,jpg,jpeg,webp}
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

WORKSPACE = Path(__file__).resolve().parents[3]
KIOSK_ASSETS = WORKSPACE / "ASAK-Kiosk" / "public" / "assets"

WHITE = 245
LIGHT_GRAY = 190
ALPHA = 12
PAD_RATIO = 0.02
MIN_PAD = 2

TARGET_DIRS = (
    KIOSK_ASSETS / "menu",
    KIOSK_ASSETS / "ingredients" / "photos",
)


def is_background_pixel(r: int, g: int, b: int, a: int) -> bool:
    if a < ALPHA:
        return True
    if r >= WHITE and g >= WHITE and b >= WHITE:
        return True
    # PNG 미리보기용 체커보드 / 연회색 스튜디오 배경
    if (
        min(r, g, b) >= LIGHT_GRAY
        and (max(r, g, b) - min(r, g, b)) <= 12
    ):
        return True
    if min(r, g, b) >= 240 and (max(r, g, b) - min(r, g, b)) <= 8:
        return True
    return False


def knockout_background(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if is_background_pixel(r, g, b, a):
                px[x, y] = (r, g, b, 0)
    return im


def trim(im: Image.Image) -> tuple[Image.Image, tuple[int, int], tuple[int, int]]:
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    minx, miny, maxx, maxy = w, h, -1, -1

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if is_background_pixel(r, g, b, a):
                continue
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)

    if maxx < 0:
        out = knockout_background(im)
        return out, im.size, out.size

    cw, ch = maxx - minx + 1, maxy - miny + 1
    pad = max(MIN_PAD, int(max(cw, ch) * PAD_RATIO))
    minx = max(0, minx - pad)
    miny = max(0, miny - pad)
    maxx = min(w - 1, maxx + pad)
    maxy = min(h - 1, maxy + pad)
    cropped = im.crop((minx, miny, maxx + 1, maxy + 1))
    out = knockout_background(cropped)
    return out, im.size, out.size


def iter_images(root: Path) -> list[Path]:
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    if not root.exists():
        return []
    return sorted(p for p in root.iterdir() if p.is_file() and p.suffix.lower() in exts)


def pixels_changed(before: Image.Image, after: Image.Image) -> bool:
    if before.size != after.size:
        return True
    a = before.convert("RGBA")
    b = after.convert("RGBA")
    return a.tobytes() != b.tobytes()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--backup", action="store_true", help="원본을 .bak/ 아래에 보관")
    parser.add_argument("--force", action="store_true", help="크기 동일해도 배경 제거 결과 저장")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = KIOSK_ASSETS / ".bak" / stamp if args.backup else None

    total = changed = 0
    for folder in TARGET_DIRS:
        for path in iter_images(folder):
            total += 1
            im = Image.open(path)
            original = im.convert("RGBA")
            out, before, after = trim(im)
            if (
                not args.force
                and before == after
                and not pixels_changed(original, out)
            ):
                print(f"skip {path.name}: {before[0]}x{before[1]}")
                continue

            changed += 1
            rel = path.relative_to(KIOSK_ASSETS)
            print(f"{rel}: {before[0]}x{before[1]} -> {after[0]}x{after[1]}")

            if args.dry_run:
                continue

            if backup_root is not None:
                dest = backup_root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)

            save_path = path
            if path.suffix.lower() != ".png":
                save_path = path.with_suffix(".png")
                if save_path != path:
                    path.unlink(missing_ok=True)
            out.save(save_path, "PNG", optimize=True)

    print(f"DONE total={total} changed={changed} dry_run={args.dry_run}")
    if backup_root:
        print(f"backup={backup_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
