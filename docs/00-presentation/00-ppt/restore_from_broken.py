"""
원본(broken) 슬라이드 XML + rels + media를 현재(열리는) PPT에 이식.
presentation.xml 등 루트 구조는 현재본 유지 → PowerPoint 호환.
"""

from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path

import win32com.client

BASE = Path(__file__).resolve().parent
ORIG = BASE / "ASAK_샐러드_스마트키오스크_2026_0902.broken.pptx"
CURR = BASE / "ASAK_샐러드_스마트키오스크_2026_0902.pptx"
BACKUP = BASE / "ASAK_샐러드_스마트키오스크_2026_0902.pre_restore.pptx"
OUT = CURR  # in-place after backup

KEEP_PREFIXES = (
    "[Content_Types].xml",
    "_rels/",
    "docProps/",
    "ppt/presentation.xml",
    "ppt/_rels/presentation.xml.rels",
    "ppt/presProps.xml",
    "ppt/viewProps.xml",
    "ppt/tableStyles.xml",
    "ppt/theme/",
    "ppt/slideMasters/",
    "ppt/slideLayouts/",
    "ppt/notesMasters/",
    "ppt/notesSlides/",
    "ppt/handoutMasters/",
)


def should_keep(name: str) -> bool:
    return any(name == p or name.startswith(p) for p in KEEP_PREFIXES)


def transplant() -> Path:
    if not ORIG.exists():
        raise FileNotFoundError(ORIG)
    if not CURR.exists():
        raise FileNotFoundError(CURR)

    shutil.copy2(CURR, BACKUP)
    print("backup:", BACKUP.name)

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "out"
        work.mkdir()

        with zipfile.ZipFile(CURR, "r") as zc:
            zc.extractall(work)

        with zipfile.ZipFile(ORIG, "r") as zo:
            orig_names = zo.namelist()
            slide_xml = 0
            slide_rels = 0
            media = 0
            for name in orig_names:
                if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                    (work / name).parent.mkdir(parents=True, exist_ok=True)
                    (work / name).write_bytes(zo.read(name))
                    slide_xml += 1
                elif name.startswith("ppt/slides/_rels/slide") and name.endswith(".xml.rels"):
                    (work / name).parent.mkdir(parents=True, exist_ok=True)
                    (work / name).write_bytes(zo.read(name))
                    slide_rels += 1
                elif name.startswith("ppt/media/"):
                    (work / name).parent.mkdir(parents=True, exist_ok=True)
                    (work / name).write_bytes(zo.read(name))
                    media += 1

        print(f"transplanted: {slide_xml} slides, {slide_rels} rels, {media} media")

        out_path = Path(tmp) / "restored.pptx"
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zw:
            for f in sorted(work.rglob("*")):
                if f.is_file():
                    arc = f.relative_to(work).as_posix()
                    zw.write(f, arc)

        shutil.copy2(out_path, OUT)
    return OUT


def com_resave(path: Path) -> None:
    app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(str(path.resolve()), WithWindow=False)
        pres.Save()
        pres.Close()
        print("COM Save OK")
    finally:
        app.Quit()


def verify_open(path: Path) -> int:
    app = win32com.client.Dispatch("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(str(path.resolve()), WithWindow=False)
        n = pres.Slides.Count
        pres.Close()
        print("PowerPoint open OK, slides:", n)
        return n
    finally:
        app.Quit()


def main():
    path = transplant()
    try:
        com_resave(path)
    except Exception as e:
        print("COM Save skipped/failed:", e)
    verify_open(path)
    print("done:", path)


if __name__ == "__main__":
    main()
