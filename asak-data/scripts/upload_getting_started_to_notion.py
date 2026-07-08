#!/usr/bin/env python3
"""Upload docs/GETTING_STARTED.md to Notion under project hub."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
MD_PATH = REPO_ROOT / "docs" / "GETTING_STARTED.md"
PARENT_PAGE_ID = "39151ef04f0b808f99f8ea068efb5790"
PAGE_TITLE = "🚀 ASAK 처음 시작하기 (팀 온보딩)"
GITHUB_BASE = "https://github.com/hagenie128/ASAK/blob/main"

NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"


def _token() -> str:
    t = os.environ.get("NOTION_TOKEN", "").strip()
    if not t:
        sys.exit("NOTION_TOKEN not set")
    return t


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def md_to_github_links(text: str) -> str:
    """Convert relative doc links to GitHub URLs."""

    def repl(m: re.Match[str]) -> str:
        label, href = m.group(1), m.group(2)
        if href.startswith("http"):
            return m.group(0)
        if href.startswith("../"):
            path = href[3:]
        elif href.startswith("guides/"):
            path = f"docs/{href}"
        elif href.startswith("wiki/"):
            path = f"docs/{href}"
        else:
            path = href
        path = path.split("#")[0]
        anchor = ""
        if "#" in href:
            anchor = "#" + href.split("#", 1)[1]
        return f"[{label}]({GITHUB_BASE}/{path}{anchor})"

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, text)


def md_table_to_notion_html(table_lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in table_lines:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    parts = ['<table header-row="true">']
    for row in rows:
        parts.append("<tr>")
        for cell in row:
            parts.append(f"<td>{cell}</td>")
        parts.append("</tr>")
    parts.append("</table>")
    return "\n".join(parts)


def md_to_notion_markdown(raw: str) -> str:
    lines = raw.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # skip top title (page property handles it)
        if i == 0 and line.startswith("# "):
            i += 1
            continue
        # markdown table block
        if line.strip().startswith("|"):
            tbl: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            html = md_table_to_notion_html(tbl)
            if html:
                out.append(html)
            continue
        # checklist -> notion todo
        m = re.match(r"^- \[([ xX])\] (.+)$", line)
        if m:
            mark = "x" if m.group(1).lower() == "x" else " "
            out.append(f"- [{mark}] {m.group(2)}")
            i += 1
            continue
        out.append(line)
        i += 1
    text = "\n".join(out)
    text = md_to_github_links(text)
    # Git canonical stub at top (Notion URL filled after create)
    stub = (
        '<callout icon="📌" color="blue_bg">\n'
        "**Notion 정본** · Git mirror: "
        f"[`docs/GETTING_STARTED.md`]({GITHUB_BASE}/docs/GETTING_STARTED.md)\n"
        "</callout>\n---\n"
    )
    return stub + text.strip() + "\n"


def search_existing_page(token: str, title: str) -> str | None:
    r = requests.post(
        f"{API}/search",
        headers=_headers(token),
        json={"query": title, "filter": {"value": "page", "property": "object"}},
        timeout=60,
    )
    r.raise_for_status()
    for item in r.json().get("results", []):
        props = item.get("properties", {})
        for prop in props.values():
            if prop.get("type") == "title":
                plain = "".join(t.get("plain_text", "") for t in prop.get("title", []))
                if "처음 시작하기" in plain or "GETTING_STARTED" in plain:
                    return item["id"]
    return None


def create_or_replace_page(token: str, content: str, page_id: str | None) -> str:
    if page_id:
        # replace via Notion MCP is easier; use blocks append after clear is complex.
        # Use PATCH properties + delete children is heavy. Create new child and archive old?
        # For update: use notion-update-page replace_content via separate step.
        return page_id

    body = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "🚀"},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": PAGE_TITLE}}]}
        },
    }
    r = requests.post(f"{API}/pages", headers=_headers(token), json=body, timeout=60)
    r.raise_for_status()
    return r["id"] if False else r.json()["id"]  # noqa: SIM212


def main() -> None:
    token = _token()
    raw = MD_PATH.read_text(encoding="utf-8")
    notion_md = md_to_notion_markdown(raw)

    out_path = REPO_ROOT / "asak-data" / "scripts" / "_getting_started_notion.md"
    out_path.write_text(notion_md, encoding="utf-8")

    existing = search_existing_page(token, PAGE_TITLE)
    if existing:
        print(f"EXISTING_PAGE_ID={existing}")
        print(f"NOTION_MD_PATH={out_path}")
        print("Use notion-update-page replace_content with content from NOTION_MD_PATH")
        return

    page_id = create_or_replace_page(token, notion_md, None)
    url = f"https://www.notion.so/{page_id.replace('-', '')}"
    print(f"CREATED_PAGE_ID={page_id}")
    print(f"PAGE_URL={url}")
    print(f"NOTION_MD_PATH={out_path}")
    print("Run MCP notion-update-page replace_content with NOTION_MD_PATH content")


if __name__ == "__main__":
    main()
