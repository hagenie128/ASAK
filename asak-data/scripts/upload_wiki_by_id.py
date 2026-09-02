#!/usr/bin/env python3
"""PUT markdown to DevCopilot Wiki by remote id (preserves title)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import requests

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
REPO_ROOT = Path(__file__).resolve().parents[2]


def headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "x-user-username": "hagenie128"}
    token = os.getenv("DEVCOPILOT_TOKEN")
    if not token:
        print("DEVCOPILOT_TOKEN required", file=sys.stderr)
        sys.exit(1)
    h["Authorization"] = f"Bearer {token}"
    return h


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) % 2 != 1:
        print("Usage: upload_wiki_by_id.py <wiki_id> <file> [<wiki_id> <file> ...]", file=sys.stderr)
        sys.exit(1)

    pairs: list[tuple[int, Path]] = []
    args = sys.argv[1:]
    for i in range(0, len(args), 2):
        wid = int(args[i])
        path = Path(args[i + 1])
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            print(f"Missing {path}", file=sys.stderr)
            sys.exit(1)
        pairs.append((wid, path))

    h = headers()
    r = requests.get(f"{BASE}/api/workspaces/{WS}/wikis", headers=h, timeout=180)
    if r.status_code != 200:
        print(f"FAIL list: {r.status_code} {r.text[:300]}", file=sys.stderr)
        sys.exit(1)
    by_id = {w["id"]: w for w in r.json()}

    for wid, path in pairs:
        if wid not in by_id:
            print(f"FAIL wiki id {wid} not found", file=sys.stderr)
            sys.exit(1)
        title = by_id[wid]["title"]
        content = path.read_text(encoding="utf-8")
        pr = requests.put(
            f"{BASE}/api/workspaces/{WS}/wikis/{wid}",
            headers=h,
            json={"title": title, "content": content},
            timeout=180,
        )
        if pr.status_code not in (200, 201):
            print(f"FAIL id={wid}: {pr.status_code} {pr.text[:300]}", file=sys.stderr)
            sys.exit(1)
        saved = pr.json().get("content") or ""
        print(
            f"OK id={wid} title={title} file={path.name} "
            f"bytes={len(content)} saved_len={len(saved)} "
            f"url=https://devcopilot.ai.kr/workspace/2/wiki/{wid}"
        )


if __name__ == "__main__":
    main()
