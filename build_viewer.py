#!/usr/bin/env python3
"""뷰어 + output JSON을 정적 사이트(docs/)로 빌드 — GitHub Pages 등에 배포용."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIEWER_DIR = ROOT / "viewer"
OUTPUT_DIR = ROOT / "output"
DOCS_DIR = ROOT / "docs"

DATA_FILES = (
    "menus.json",
    "dressings.json",
    "store_menus.json",
    "dressing_nutrition_supplements.json",
)


def build_meta() -> dict:
    from run_viewer import build_meta as _build_meta

    return _build_meta()


def build(dest: Path = DOCS_DIR) -> Path:
    if not VIEWER_DIR.exists():
        raise SystemExit(f"viewer 폴더가 없습니다: {VIEWER_DIR}")
    if not OUTPUT_DIR.exists():
        raise SystemExit(f"output 폴더가 없습니다: {OUTPUT_DIR}")

    data_dir = dest / "data"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    for name in ("index.html",):
        shutil.copy2(VIEWER_DIR / name, dest / name)
    for sub in ("css", "js"):
        shutil.copytree(VIEWER_DIR / sub, dest / sub)

    data_dir.mkdir()
    copied = []
    for name in DATA_FILES:
        src = OUTPUT_DIR / name
        if src.exists():
            shutil.copy2(src, data_dir / name)
            copied.append(name)

    (dest / ".nojekyll").touch()
    meta = build_meta()
    meta["deploy"] = {"data_files": copied, "dest": str(dest)}
    (data_dir / "_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    total_kb = sum((data_dir / n).stat().st_size for n in copied) // 1024
    print(f"빌드 완료: {dest.resolve()}")
    print(f"  데이터: {', '.join(copied)} ({total_kb} KB)")
    print("  GitHub Pages: 저장소 Settings → Pages → Branch main /docs")
    print("  예상 URL: https://hagenie128.github.io/Greens/")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="뷰어 정적 사이트 빌드")
    parser.add_argument("-o", "--output", type=Path, default=DOCS_DIR)
    args = parser.parse_args()
    build(args.output)


if __name__ == "__main__":
    main()
