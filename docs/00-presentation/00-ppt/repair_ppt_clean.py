"""PPTX 무결성 진단 및 깨끗한 파일로 재저장."""

from __future__ import annotations

import re
import shutil
import zipfile
from collections import Counter
from pathlib import Path

from pptx import Presentation

PPT = Path(__file__).resolve().parent / "ASAK_샐러드_스마트키오스크_2026_0902.pptx"
CLEAN = PPT.with_name("ASAK_샐러드_스마트키오스크_2026_0902_clean.pptx")


def diagnose(path: Path) -> None:
    print(f"\n=== {path.name} ===")
    with zipfile.ZipFile(path) as z:
        z.testzip()
        pres = z.read("ppt/presentation.xml").decode("utf-8")
        rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8")

    ids = re.findall(r'sldId id="(\d+)"', pres)
    print("sldId:", len(ids), "unique:", len(set(ids)))
    dup = [k for k, v in Counter(ids).items() if v > 1]
    if dup:
        print("DUPLICATE sldId ids:", dup)

    pres_rids = set(re.findall(r'r:id="(rId\d+)"', pres))
    rel_ids = set(re.findall(r'Id="(rId\d+)"', rels))
    missing = sorted(pres_rids - rel_ids)
    if missing:
        print("missing rels:", missing)

    slide_rels = re.findall(r'Id="(rId\d+)" Type="[^"]+" Target="slides/([^"]+)"', rels)
    pres_slide_rids = set(re.findall(r'sldId[^>]+r:id="(rId\d+)"', pres))
    used_targets = [t for rid, t in slide_rels if rid in pres_slide_rids]
    dup_targets = [k for k, v in Counter(used_targets).items() if v > 1]
    if dup_targets:
        print("DUPLICATE slide targets:", dup_targets)

    orphan = [(rid, t) for rid, t in slide_rels if rid not in pres_slide_rids]
    print("orphan slide parts:", len(orphan))


def rebuild_clean() -> None:
    prs = Presentation(str(PPT))
    print(f"loaded {len(prs.slides)} slides")
    prs.save(str(CLEAN))
    print(f"saved clean -> {CLEAN.name} ({CLEAN.stat().st_size} bytes)")
    diagnose(CLEAN)


if __name__ == "__main__":
    diagnose(PPT)
    rebuild_clean()
