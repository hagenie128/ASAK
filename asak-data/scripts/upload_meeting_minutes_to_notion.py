#!/usr/bin/env python3
"""Upload ASAK weekly meeting-minutes to Notion and print URLs for Hub wiki.

Requires: NOTION_TOKEN in environment.
Parent: ASAK Notion hub page (키오스크 풀스택 프로젝트).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

API = "https://api.notion.com/v1"
VERSION = "2022-06-28"
PARENT_HUB = "39151ef04f0b808f99f8ea068efb5790"  # ASAK Notion hub
GH = "https://github.com/hagenie128/ASAK/blob/main"
ROOT = Path(__file__).resolve().parents[2]
OPS = ROOT / "docs" / "operations" / "meeting-minutes"
OUT = ROOT / "docs" / "ai-reports" / "2026-08-07" / "asak-notion-meeting-minutes-upload.json"

WEEKS = [
    ("W27", "2026-W27.md", "회의록 2026-W27 — 킥오프·기획 정비"),
    ("W28", "2026-W28.md", "회의록 2026-W28 — 디자인 방향·관리자 UI 골격"),
    ("W29", "2026-W29.md", "회의록 2026-W29 — 저장소 분리·Figma→코드·구현 경계"),
    ("W30", "2026-W30.md", "회의록 2026-W30 — mock 완성·백엔드 골격·제출"),
    ("W31", "2026-W31.md", "회의록 2026-W31 — Admin API·계약 통일·연동 시작"),
    ("W32", "2026-W32.md", "회의록 2026-W32 — 실연동·관리자 CRUD·문서화"),
]


def headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": VERSION,
        "Content-Type": "application/json",
    }


def rich(text: str) -> list[dict]:
    # Notion rich_text limit 2000 per item
    chunks = []
    s = text
    while s:
        chunks.append({"type": "text", "text": {"content": s[:1900]}})
        s = s[1900:]
    return chunks or [{"type": "text", "text": {"content": ""}}]


def md_to_blocks(md: str) -> list[dict]:
    """Minimal markdown → Notion blocks (paragraph/heading/bulleted/divider/code)."""
    blocks: list[dict] = []
    lines = md.splitlines()
    i = 0
    # skip first H1 (page title)
    if lines and lines[0].startswith("# "):
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1

    # intro callout
    blocks.append(
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📌"},
                "rich_text": rich(
                    f"Git 정본: {GH}/docs/operations/meeting-minutes/"
                ),
                "color": "gray_background",
            },
        }
    )

    buf: list[str] = []

    def flush_para() -> None:
        nonlocal buf
        text = "\n".join(buf).strip()
        buf = []
        if not text:
            return
        blocks.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": rich(text[:1900])},
            }
        )

    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            flush_para()
            blocks.append({"object": "block", "type": "divider", "divider": {}})
            i += 1
            continue
        if line.startswith("# "):
            flush_para()
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {"rich_text": rich(line[2:].strip())},
                }
            )
            i += 1
            continue
        if line.startswith("## "):
            flush_para()
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": rich(line[3:].strip())},
                }
            )
            i += 1
            continue
        if line.startswith("### "):
            flush_para()
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {"rich_text": rich(line[4:].strip())},
                }
            )
            i += 1
            continue
        if line.startswith("|"):
            flush_para()
            # collect table as code block (Notion API table creation is heavy)
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                tbl.append(lines[i])
                i += 1
            blocks.append(
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "language": "plain text",
                        "rich_text": rich("\n".join(tbl)[:1900]),
                    },
                }
            )
            continue
        if line.startswith("- "):
            flush_para()
            while i < len(lines) and lines[i].startswith("- "):
                item = lines[i][2:].strip()
                blocks.append(
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": rich(item[:1900])},
                    }
                )
                i += 1
            continue
        if not line.strip():
            flush_para()
            i += 1
            continue
        buf.append(line)
        i += 1
    flush_para()
    return blocks[:90]  # safety; append rest later if needed


def append_blocks(token: str, page_id: str, blocks: list[dict]) -> None:
    # Notion allows max 100 children per request
    for start in range(0, len(blocks), 90):
        chunk = blocks[start : start + 90]
        r = requests.patch(
            f"{API}/blocks/{page_id}/children",
            headers=headers(token),
            json={"children": chunk},
            timeout=120,
        )
        if r.status_code not in (200, 201):
            raise RuntimeError(f"append blocks failed: {r.status_code} {r.text[:400]}")
        time.sleep(0.35)


def search_page(token: str, title: str) -> dict | None:
    r = requests.post(
        f"{API}/search",
        headers=headers(token),
        json={
            "query": title,
            "filter": {"value": "page", "property": "object"},
            "page_size": 20,
        },
        timeout=60,
    )
    r.raise_for_status()
    for item in r.json().get("results", []):
        props = item.get("properties") or {}
        for prop in props.values():
            if prop.get("type") == "title":
                plain = "".join(t.get("plain_text", "") for t in prop.get("title") or [])
                if plain.strip() == title.strip():
                    return item
    return None


def create_page(token: str, title: str, parent_id: str) -> dict:
    body = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": "📝"},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
    }
    r = requests.post(f"{API}/pages", headers=headers(token), json=body, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"create page failed: {r.status_code} {r.text[:500]}")
    return r.json()


def clear_children(token: str, page_id: str) -> None:
    cursor = None
    while True:
        url = f"{API}/blocks/{page_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        r = requests.get(url, headers=headers(token), timeout=60)
        r.raise_for_status()
        data = r.json()
        for b in data.get("results", []):
            requests.delete(f"{API}/blocks/{b['id']}", headers=headers(token), timeout=60)
            time.sleep(0.2)
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")


def ensure_index_parent(token: str) -> str:
    title = "ASAK 주차별 회의록 (2026-07~08)"
    existing = search_page(token, title)
    if existing:
        return existing["id"]
    page = create_page(token, title, PARENT_HUB)
    return page["id"]


def page_url(page_id: str) -> str:
    return f"https://www.notion.so/{page_id.replace('-', '')}"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        return 1

    # verify
    me = requests.get(f"{API}/users/me", headers=headers(token), timeout=30)
    if me.status_code != 200:
        print(f"ERROR: token invalid {me.status_code} {me.text[:200]}", file=sys.stderr)
        return 1
    print("OK auth", me.json().get("name") or me.json().get("bot", {}))

    parent_id = ensure_index_parent(token)
    print("index_parent", parent_id, page_url(parent_id))

    results = {"index": {"id": parent_id, "url": page_url(parent_id), "title": "ASAK 주차별 회의록 (2026-07~08)"}, "weeks": {}}

    # refresh index body with links (after weeks created we rewrite)
    week_meta = []
    for key, fname, title in WEEKS:
        existing = search_page(token, title)
        if existing:
            pid = existing["id"]
            action = "update"
            clear_children(token, pid)
        else:
            page = create_page(token, title, parent_id)
            pid = page["id"]
            action = "create"
        md = (OPS / fname).read_text(encoding="utf-8")
        # soften relative links to GitHub
        md = re.sub(
            r"\]\(\./([^)]+)\)",
            rf"]({GH}/docs/operations/meeting-minutes/\1)",
            md,
        )
        md = re.sub(
            r"\]\(\.\./\.\./\.\./worklog/weekly/([^)]+)\)",
            rf"]({GH}/worklog/weekly/\1)",
            md,
        )
        blocks = md_to_blocks(md)
        append_blocks(token, pid, blocks)
        url = page_url(pid)
        print(action, key, url)
        results["weeks"][key] = {"id": pid, "url": url, "title": title, "file": fname, "action": action}
        week_meta.append((key, title, url, fname))
        time.sleep(0.4)

    # rewrite index page content
    clear_children(token, parent_id)
    index_blocks = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📌"},
                "rich_text": rich(
                    f"Git 정본 폴더: {GH}/docs/operations/meeting-minutes/"
                ),
                "color": "blue_background",
            },
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rich("주차별 회의록")},
        },
    ]
    # table as bullets with links
    for key, title, url, fname in week_meta:
        index_blocks.append(
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"{key} · {title} — ", "link": None},
                        },
                        {
                            "type": "text",
                            "text": {"content": "Notion", "link": {"url": url}},
                        },
                        {"type": "text", "text": {"content": " · "}},
                        {
                            "type": "text",
                            "text": {
                                "content": fname,
                                "link": {
                                    "url": f"{GH}/docs/operations/meeting-minutes/{fname}"
                                },
                            },
                        },
                    ]
                },
            }
        )
    # also include README summary lightly
    readme = (OPS / "README.md").read_text(encoding="utf-8")
    index_blocks.append({"object": "block", "type": "divider", "divider": {}})
    index_blocks.append(
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rich("팀·결정 요약 (README)")},
        }
    )
    index_blocks.extend(md_to_blocks(readme)[1:40])  # skip duplicate callout-ish
    append_blocks(token, parent_id, index_blocks)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("WROTE", OUT)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
