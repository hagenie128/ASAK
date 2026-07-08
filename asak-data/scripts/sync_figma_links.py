#!/usr/bin/env python3
"""Figma frame node_id → Git → DevCopilot 동기화.

FIGMA_TOKEN(또는 FIGMA_ACCESS_TOKEN)으로 kiosk_design 프레임을 조회한 뒤
figma-links.template.json, screens.json, 체크리스트, Wiki를 갱신합니다.

Usage:
  set FIGMA_TOKEN=figd_...
  python asak-data/scripts/sync_figma_links.py --all
  python asak-data/scripts/sync_figma_links.py --fetch --git
  python asak-data/scripts/sync_figma_links.py --git --devcopilot
  python asak-data/scripts/sync_figma_links.py --manifest   # Notion MCP용 JSON 출력

Notion DB `Figma 링크` 갱신은 MCP notion-update-page로 manifest를 사용하세요.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
FIGMA_LINKS = REPO / "docs" / "design" / "figma-links.template.json"
SCREENS_JSON = REPO / "docs" / "screens" / "screens.json"
SCREENS_IMPORT = REPO / "docs" / "screens" / "screens-devcopilot-import-array.json"
SCREENS_LS = REPO / "docs" / "screens" / "screens-devcopilot-localstorage.json"
CHECKLIST_MD = REPO / "docs" / "design" / "SCR_FIGMA_CHECKLIST.md"
MANIFEST_OUT = Path(__file__).parent / "figma_notion_manifest.json"

# export_screens.py 와 동일
SCREEN_PAGE_IDS: dict[str, str] = {
    "SCR-001": "39251ef0-4f0b-8180-9f23-d741a44576d4",
    "SCR-002": "39251ef0-4f0b-81f3-817e-d64352907379",
    "SCR-003": "39151ef04f0b81d5bcadc90c901d56d8",
    "SCR-004": "39151ef04f0b8163bec2c6b5cd0b6f19",
    "SCR-005": "39151ef04f0b81adb474ddf94c33827d",
    "SCR-006": "39251ef0-4f0b-8187-af99-d9f6add9af64",
    "SCR-007": "39151ef04f0b8125a9dacd7c7ad95831",
    "SCR-008": "39151ef04f0b816287ceda11a8ede0f6",
    "SCR-009": "39151ef04f0b816a89b6c3b956e9974a",
    "SCR-010": "39251ef0-4f0b-81869277fd3fc980ff52",
    "SCR-011": "39151ef04f0b811189b2fc39fe4f1959",
    "SCR-012": "39251ef0-4f0b-815cb6a3cf814f31623b",
    "SCR-013": "39251ef0-4f0b-8102bff0db4c2edddd62",
    "SCR-014": "39251ef0-4f0b-8136a250c51fd7314855",
    "SCR-015": "39251ef0-4f0b-81ad9057eec10351023e",
    "SCR-016": "39251ef0-4f0b-812fba53ed19e6089d7b",
    "SCR-017": "39251ef0-4f0b-81e3bf1dcbe8caf82632",
    "SCR-018": "39251ef0-4f0b-81b084fae81a1dc8e1c7",
    "SCR-019": "39251ef0-4f0b-813d8e9ff5fa34adf007",
    "SCR-020": "39551ef0-4f0b-810a84aae4af6de3d5c7",
    "SCR-021": "39551ef0-4f0b-810cbfacfec11674a302",
}


def fetch_and_sync_template() -> list[dict]:
    """rename_figma_scr_frames --sync-json 호출 후 mapping 반환."""
    import rename_figma_scr_frames as rff

    if not rff.figma_token():
        print("ERROR: FIGMA_TOKEN 또는 FIGMA_ACCESS_TOKEN 필요", file=sys.stderr)
        return []

    file_json = rff.figma_get(f"/files/{rff.FILE_KEY}?depth=2")
    frames = rff.list_top_level_frames(file_json)
    targets = rff.load_scr_targets()
    mapping = rff.suggest_mapping(frames, targets)
    n = rff.sync_figma_links(mapping)
    print(f"figma-links.template.json: {n}건 node_id/figma_url 갱신")
    return mapping


def load_links_by_scr() -> dict[str, dict]:
    data = json.loads(FIGMA_LINKS.read_text(encoding="utf-8"))
    return {s["scr_id"]: s for s in data["screens"]}


def sync_screens_json() -> int:
    links = load_links_by_scr()
    screens = json.loads(SCREENS_JSON.read_text(encoding="utf-8"))
    updated = 0
    for s in screens:
        sid = s["screen_id"]
        link = links.get(sid, {})
        url = link.get("figma_url") or ""
        if s.get("figma_url") != url:
            s["figma_url"] = url
            updated += 1
    SCREENS_JSON.write_text(json.dumps(screens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"screens.json: {updated}건 figma_url 갱신")
    return updated


def sync_devcopilot_import() -> int:
    """screens.json figma_url → DevCopilot import/localstorage JSON."""
    screens = json.loads(SCREENS_JSON.read_text(encoding="utf-8"))
    items = [
        {
            "id": s["screen_id"],
            "name": s["title"],
            "figmaUrl": s.get("figma_url") or "",
            "inputs": s.get("input_vars") or "",
            "outputs": s.get("output_vars") or "",
            "status": s.get("status_devcopilot") or s.get("status") or "WIREFRAME",
        }
        for s in screens
    ]
    SCREENS_IMPORT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ls = {"localStorage_key": "ws_2_screens", "workspace_id": 2, "screens": items}
    SCREENS_LS.write_text(json.dumps(ls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    filled = sum(1 for i in items if i.get("figmaUrl"))
    print(f"screens-devcopilot-import-array.json: {filled}/21 figmaUrl 반영")
    return filled


def sync_checklist_md() -> None:
    links = load_links_by_scr()
    text = CHECKLIST_MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        m = re.match(r"^\| (SCR-\d{3}) \|", line)
        if m:
            sid = m.group(1)
            url = links.get(sid, {}).get("figma_url") or ""
            parts = line.split("|")
            if len(parts) >= 6:
                parts[5] = f" {url} " if url else " "
                line = "|".join(parts)
        out.append(line)
    CHECKLIST_MD.write_text("\n".join(out) + "\n", encoding="utf-8")
    filled = sum(1 for s in links.values() if s.get("figma_url"))
    print(f"SCR_FIGMA_CHECKLIST.md: {filled}/21 Figma URL 반영")


def run_export_screens() -> None:
    subprocess.run([sys.executable, str(REPO / "asak-data" / "scripts" / "export_screens.py")], check=True)


def run_gen_wiki() -> None:
    subprocess.run([sys.executable, str(REPO / "asak-data" / "scripts" / "gen_wiki_markdown.py")], check=True)


def write_notion_manifest(mapping: list[dict] | None = None) -> dict:
    links = load_links_by_scr()
    items = []
    for sid, page_id in sorted(SCREEN_PAGE_IDS.items()):
        url = links.get(sid, {}).get("figma_url") or ""
        items.append({"scr_id": sid, "notion_page_id": page_id, "figma_url": url})
    manifest = {
        "generated_by": "sync_figma_links.py",
        "notion_db": "화면 설계 데이터베이스",
        "property": "Figma 링크",
        "hub_pages": {
            "04_화면_설계": "1c751ef0-4f0b-825e-a3aa-8145f563bbc8",
            "figma_matrix": "39451ef0-4f0b-8184-9dc7-d81f8106b5ad",
            "scr_guide": "39451ef0-4f0b-8110-9d07-c01293d73c6d",
            "design_hub": "39451ef0-4f0b-8163-b1f9ebb477917efc",
        },
        "screens": items,
        "filled": sum(1 for i in items if i["figma_url"]),
        "total": len(items),
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Notion manifest: {manifest['filled']}/{manifest['total']} → {MANIFEST_OUT}")
    return manifest


def upload_devcopilot() -> None:
    subprocess.run([sys.executable, str(REPO / "asak-data" / "scripts" / "upload_screens_api.py")], check=True)
    subprocess.run(
        [
            sys.executable,
            str(REPO / "asak-data" / "scripts" / "upload_wiki.py"),
            "--title",
            "ASAK 화면 설계 및 Figma 연동",
            "--file",
            "docs/wiki/screen-design-figma.md",
        ],
        check=True,
    )
    print("DevCopilot: Screens API + wiki/5 업로드 완료")


def print_link_table() -> None:
    links = load_links_by_scr()
    print(f"\n{'SCR':<10} {'Figma URL'}")
    print("-" * 80)
    for sid in sorted(links.keys()):
        url = links[sid].get("figma_url") or "(미설정)"
        print(f"{sid:<10} {url}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Figma SCR 링크 → Git/DevCopilot 동기화")
    parser.add_argument("--fetch", action="store_true", help="Figma API로 node_id 조회")
    parser.add_argument("--git", action="store_true", help="Git 파일 갱신")
    parser.add_argument("--devcopilot", action="store_true", help="DevCopilot 업로드")
    parser.add_argument("--manifest", action="store_true", help="Notion MCP manifest 출력")
    parser.add_argument("--all", action="store_true", help="fetch + git + manifest + devcopilot")
    args = parser.parse_args()

    if args.all:
        args.fetch = args.git = args.manifest = args.devcopilot = True

    if not any((args.fetch, args.git, args.devcopilot, args.manifest)):
        parser.print_help()
        return 1

    mapping: list[dict] = []
    if args.fetch:
        mapping = fetch_and_sync_template()
        if not mapping:
            return 2

    if args.git:
        sync_checklist_md()
        run_export_screens()
        sync_screens_json()  # figma-links.template → screens.json (export가 Notion 기준으로 덮어씀)
        sync_devcopilot_import()
        run_gen_wiki()

    if args.manifest or args.git:
        write_notion_manifest(mapping if mapping else None)

    if args.devcopilot:
        upload_devcopilot()

    print_link_table()
    manifest = json.loads(MANIFEST_OUT.read_text(encoding="utf-8")) if MANIFEST_OUT.exists() else {}
    if manifest.get("filled", 0) < manifest.get("total", 21):
        print(
            f"\nNotion DB 갱신: MCP notion-update-page로 {MANIFEST_OUT} 참조 "
            f"({manifest.get('filled', 0)}/{manifest.get('total', 21)} URL 준비됨)",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
