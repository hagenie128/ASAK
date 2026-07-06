#!/usr/bin/env python3
"""Upload ASAK screens to DevCopilot Screens API (workspace 2)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}
REPO = Path(__file__).resolve().parents[2]
SCREENS_JSON = REPO / "docs" / "screens" / "screens-devcopilot-import-array.json"
WIKI_MD = REPO / "docs" / "screens" / "screens-wiki.md"


def api(method: str, path: str, **kwargs) -> requests.Response:
    return requests.request(method, f"{BASE}{path}", headers=HEADERS, timeout=120, **kwargs)


def to_body(item: dict) -> dict:
    return {
        "id": item["id"],
        "name": item["name"],
        "inputs": item.get("inputs") or "",
        "outputs": item.get("outputs") or "",
        "status": item.get("status") or "WIREFRAME",
        "figma_url": item.get("figmaUrl") or "",
    }


def upload_screens() -> tuple[int, int]:
    screens = json.loads(SCREENS_JSON.read_text(encoding="utf-8"))
    existing = {s["id"]: s for s in api("GET", f"/api/workspaces/{WS}/screens").json()}
    ok = 0
    for item in screens:
        sid = item["id"]
        body = to_body(item)
        if sid in existing:
            r = api("PUT", f"/api/workspaces/{WS}/screens/{sid}", json=body)
            action = "updated"
        else:
            r = api("POST", f"/api/workspaces/{WS}/screens", json=body)
            action = "created"
        if r.status_code in (200, 201):
            ok += 1
            print(f"OK  {sid} {action}")
        else:
            print(f"FAIL {sid} {action}: {r.status_code} {r.text[:200]}", file=sys.stderr)
    return ok, len(screens)


def upsert_wiki_16() -> None:
    content = WIKI_MD.read_text(encoding="utf-8")
    body = {"title": "ASAK 화면설계 (SCR-001~021)", "content": content}
    r = api("PUT", f"/api/workspaces/{WS}/wikis/16", json=body)
    if r.status_code not in (200, 201):
        print(f"FAIL wiki/16: {r.status_code} {r.text}", file=sys.stderr)
        sys.exit(1)
    print(f"Wiki updated id=16 url=https://devcopilot.ai.kr/workspace/2/wiki/16")


def main() -> int:
    ok, total = upload_screens()
    print(f"Screens synced {ok}/{total}")
    upsert_wiki_16()
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
