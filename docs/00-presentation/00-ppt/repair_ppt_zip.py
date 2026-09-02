"""
PPTX ZIP 구조 복구:
- sldId 중복 ID 수정
- presentation에 없는 orphan slide part 제거
- Content_Types 정리
"""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

SRC = Path(__file__).resolve().parent / "ASAK_샐러드_스마트키오스크_2026_0902.pptx"
OUT = Path(__file__).resolve().parent / "ASAK_샐러드_스마트키오스크_2026_0902.pptx"
TMP = OUT.with_suffix(".repaired.pptx")

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

ET.register_namespace("p", NS_P)
ET.register_namespace("r", NS_R)


def load_items(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path, "r") as z:
        return {name: z.read(name) for name in z.namelist()}


def save_items(path: Path, items: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items.items():
            z.write_bytes = None
            z.writestr(name, data)


def repair() -> None:
    items = load_items(SRC)
    pres = ET.fromstring(items["ppt/presentation.xml"])
    rels = ET.fromstring(items["ppt/_rels/presentation.xml.rels"])

    sld_lst = pres.find(f".//{{{NS_P}}}sldIdLst")
    assert sld_lst is not None

    # rId -> Target
    rid_target: dict[str, str] = {}
    for rel in rels:
        if rel.tag.endswith("Relationship"):
            target = rel.attrib.get("Target", "")
            if target.startswith("slides/"):
                rid_target[rel.attrib["Id"]] = target

    used_rids: list[str] = []
    for sld in list(sld_lst):
        rid = sld.attrib[f"{{{NS_R}}}id"]
        used_rids.append(rid)

    used_targets = {rid_target[rid] for rid in used_rids if rid in rid_target}
    print("referenced slides:", len(used_targets))

    # sldId id 고유값 재부여
    next_id = 256
    for sld in sld_lst.findall(f"{{{NS_P}}}sldId"):
        sld.set("id", str(next_id))
        next_id += 1

    items["ppt/presentation.xml"] = ET.tostring(pres, encoding="utf-8", xml_declaration=True)

    # presentation.xml.rels: slide rel 중 미사용 제거
    for rel in list(rels):
        if not rel.tag.endswith("Relationship"):
            continue
        target = rel.attrib.get("Target", "")
        if target.startswith("slides/") and rel.attrib["Id"] not in used_rids:
            rels.remove(rel)

    items["ppt/_rels/presentation.xml.rels"] = ET.tostring(rels, encoding="utf-8", xml_declaration=True)

    # orphan slide xml / rels 제거
    keep = set()
    remove = []
    for name in items:
        m = re.match(r"ppt/slides/(slide\d+\.xml)$", name)
        if m:
            target = f"slides/{m.group(1)}"
            if target not in used_targets:
                remove.append(name)
            else:
                keep.add(name)
        m2 = re.match(r"ppt/slides/_rels/(slide\d+\.xml\.rels)$", name)
        if m2:
            slide = m2.group(1)
            target = f"slides/{slide}"
            if target not in used_targets:
                remove.append(name)

    for name in remove:
        del items[name]
    print("removed orphan slide files:", len(remove))

    # [Content_Types].xml 정리
    ct = ET.fromstring(items["[Content_Types].xml"])
    for ov in list(ct):
        if not ov.tag.endswith("Override"):
            continue
        part = ov.attrib.get("PartName", "")
        if part.startswith("/ppt/slides/slide") and part.lstrip("/") not in {f"ppt/{t}" for t in used_targets}:
            ct.remove(ov)
    items["[Content_Types].xml"] = ET.tostring(ct, encoding="utf-8", xml_declaration=True)

    save_items(TMP, items)
    backup = OUT.with_suffix(".corrupt_backup.pptx")
    if OUT.exists():
        shutil.copy2(OUT, backup)
    shutil.move(TMP, OUT)
    print("repaired ->", OUT)
    print("backup ->", backup)


if __name__ == "__main__":
    repair()
