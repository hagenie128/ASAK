#!/usr/bin/env python3
"""Sync REQ ID tags into DevCopilot screens API names and wiki/16 headers."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests

from req_link_maps import EXCLUDED_REQ_IDS, SCR_REQ_MAP, format_req_label, title_with_req

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}
if token := os.getenv("DEVCOPILOT_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {token}"
REPO = Path(__file__).resolve().parents[2]
SCREENS_JSON = REPO / "docs" / "screens" / "screens-devcopilot-import-array.json"
WIKI_MD = REPO / "docs" / "screens" / "screens-wiki.md"
WIKI_ID = 16


def api(method: str, path: str, **kwargs) -> requests.Response:
    return requests.request(method, f"{BASE}{path}", headers=HEADERS, timeout=120, **kwargs)


def screen_display_name(base_name: str, scr_id: str) -> str:
    req_ids = SCR_REQ_MAP.get(scr_id, [])
    primary = req_ids[0] if req_ids else None
    return title_with_req(base_name.strip(), req_ids, primary_only=True, primary=primary)


def strip_req_suffix(name: str) -> str:
    name = re.sub(r"\s*\([A-Z]+-[A-Z]+-\d{3}\s*\(EXCLUDED\)\)\s*$", "", name)
    name = re.sub(r"\s*\([A-Z]+-[A-Z]+-\d{3}\)\s*$", "", name)
    return name.strip()


def sync_screen_names() -> tuple[int, int]:
    screens = json.loads(SCREENS_JSON.read_text(encoding="utf-8"))
    existing = {s["id"]: s for s in api("GET", f"/api/workspaces/{WS}/screens").json()}
    ok = 0
    for item in screens:
        sid = item["id"]
        base = strip_req_suffix(item.get("name") or item.get("base_name") or "")
        new_name = screen_display_name(base, sid)
        item["name"] = new_name
        body = {
            "id": sid,
            "name": new_name,
            "inputs": item.get("inputs") or "",
            "outputs": item.get("outputs") or "",
            "status": item.get("status") or "WIREFRAME",
            "figma_url": item.get("figmaUrl") or "",
        }
        if sid in existing:
            r = api("PUT", f"/api/workspaces/{WS}/screens/{sid}", json=body)
        else:
            r = api("POST", f"/api/workspaces/{WS}/screens", json=body)
        if r.status_code in (200, 201):
            ok += 1
            print(f"OK  {sid} -> {new_name}")
        else:
            print(f"FAIL {sid}: {r.status_code} {r.text[:200]}", file=sys.stderr)
    SCREENS_JSON.write_text(
        json.dumps(screens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return ok, len(screens)


def sync_wiki_headers() -> bool:
    content = WIKI_MD.read_text(encoding="utf-8")
    updated = content
    for scr_id, req_list in sorted(SCR_REQ_MAP.items()):
        if not req_list:
            continue
        pattern = rf"(## {scr_id} [^\n]+)"
        primary = req_list[0]

        def repl(m: re.Match, pick: str = primary) -> str:
            line = m.group(1)
            suffix = f" ({format_req_label(pick)})"
            plain_suffix = f" ({pick})"
            if suffix in line:
                return line
            if plain_suffix in line and pick in EXCLUDED_REQ_IDS and "(EXCLUDED)" not in line:
                return line.replace(plain_suffix, suffix, 1)
            return f"{line}{suffix}"

        updated = re.sub(pattern, repl, updated)
    if updated != content:
        WIKI_MD.write_text(updated, encoding="utf-8")
        print(f"Updated local {WIKI_MD.name}")
    body = {
        "title": "ASAK 화면설계 (SCR-001~021)",
        "content": updated,
    }
    r = api("PUT", f"/api/workspaces/{WS}/wikis/{WIKI_ID}", json=body)
    if r.status_code not in (200, 201):
        print(f"FAIL wiki/{WIKI_ID}: {r.status_code} {r.text}", file=sys.stderr)
        return False
    print(f"Wiki updated id={WIKI_ID} url=https://devcopilot.ai.kr/workspace/2/wiki/{WIKI_ID}")
    return True


def main() -> int:
    ok, total = sync_screen_names()
    print(f"Screens synced {ok}/{total}")
    if not sync_wiki_headers():
        return 1
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
