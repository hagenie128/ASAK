"""Trim studio white / transparent margins from menu PNGs into images/menu-trimmed."""

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images" / "menu"
DST = ROOT / "images" / "menu-trimmed"

WHITE = 245
ALPHA = 12
PAD_RATIO = 0.04
MIN_PAD = 4


def trim(im: Image.Image) -> tuple[Image.Image, bool]:
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    minx, miny, maxx, maxy = w, h, -1, -1

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < ALPHA:
                continue
            if r >= WHITE and g >= WHITE and b >= WHITE:
                continue
            if min(r, g, b) >= 240 and (max(r, g, b) - min(r, g, b)) <= 8:
                continue
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)

    if maxx < 0:
        return im, False

    cw, ch = maxx - minx + 1, maxy - miny + 1
    pad = max(MIN_PAD, int(max(cw, ch) * PAD_RATIO))
    minx = max(0, minx - pad)
    miny = max(0, miny - pad)
    maxx = min(w - 1, maxx + pad)
    maxy = min(h - 1, maxy + pad)
    cropped = im.crop((minx, miny, maxx + 1, maxy + 1))
    return cropped, cropped.size != (w, h)


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    count = changed = 0
    for path in sorted(SRC.glob("*.png")):
        im = Image.open(path)
        out, did = trim(im)
        out.save(DST / path.name, "PNG", optimize=True)
        count += 1
        changed += int(did)
        print(f"{path.name}: {im.size[0]}x{im.size[1]} -> {out.size[0]}x{out.size[1]}")
    print(f"DONE count={count} changed={changed} out={DST}")


if __name__ == "__main__":
    main()
