"""Inspect slide order in both PPT zips."""
import re
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent


def slide_parts(path: Path):
    z = zipfile.ZipFile(path)
    xml = z.read("ppt/presentation.xml").decode("utf-8")
    ids = re.findall(r'<p:sldId[^>]*r:id="([^"]+)"', xml)
    rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8")
    targets = {}
    for m in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels):
        targets[m.group(1)] = m.group(2)
    slides = [targets.get(r, r) for r in ids]
    media = [n for n in z.namelist() if n.startswith("ppt/media/")]
    z.close()
    return slides, media


for name in [
    "ASAK_샐러드_스마트키오스크_2026_0902.broken.pptx",
    "ASAK_샐러드_스마트키오스크_2026_0902.pptx",
]:
    p = BASE / name
    slides, media = slide_parts(p)
    print(name)
    print("  count", len(slides))
    print("  media", len(media))
    for i, s in enumerate(slides, 1):
        print(f"  {i:2}: {s}")
