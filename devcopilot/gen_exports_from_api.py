#!/usr/bin/env python3
"""Fetch DevCopilot scenarios and export scenarios_import.json + user-scenarios.md."""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}
ROOT = Path(__file__).resolve().parents[1]
IMPORT_PATH = ROOT / "devcopilot" / "scenarios_import.json"
WIKI_PATH = ROOT / "docs" / "wiki" / "user-scenarios.md"


def api_get(path: str) -> list | dict:
    req = urllib.request.Request(f"{BASE}{path}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def scenario_to_import(s: dict) -> dict:
    m = s.get("mermaid_script") or s.get("mermaid") or ""
    return {
        "scenarioId": s["id"],
        "title": re.sub(r"\s*\([^)]*\)\s*$", "", s.get("title") or s["id"]).strip(),
        "preCondition": s.get("pre_condition") or s.get("preCondition") or "",
        "postCondition": s.get("post_condition") or s.get("postCondition") or "",
        "normalFlow": s.get("normal_flow") or s.get("normalFlow") or "",
        "alternativeFlow": s.get("alternative_flow") or s.get("alternativeFlow") or "",
        "mermaid": m,
        "status": s.get("status") or "DRAFT",
    }


def gen_user_scenarios_md(scenarios: list[dict]) -> str:
    wanted = [s for s in scenarios if re.match(r"SC-0\d\d", s["id"])]
    wanted.sort(key=lambda x: x["id"])
    lines = [
        "# ASAK 사용자 시나리오 명세",
        "",
        "> Notion 03. 사용자 시나리오 · SC-001~024 (2026-07-06 DevCopilot 동기화)",
        "",
        "## 전체 주문 흐름",
        "",
        "```mermaid",
        "flowchart LR",
        "    A[홈·매장/포장 SCR-001] --> C[메뉴선택 SCR-003]",
        "    C --> D[옵션선택 SCR-004]",
        "    D --> E[장바구니·주문확인 SCR-005]",
        "    E --> G[결제·로딩 SCR-007]",
        "    G --> H[완료 SCR-008]",
        "    H --> I[관리자 SCR-009/010]",
        "```",
        "",
        f"## 시나리오 목록 ({len(wanted)}건)",
        "",
    ]
    for s in wanted:
        sid = s["id"]
        title = s.get("title") or sid
        pre = s.get("pre_condition") or s.get("preCondition") or ""
        post = s.get("post_condition") or s.get("postCondition") or ""
        normal = s.get("normal_flow") or s.get("normalFlow") or ""
        alt = s.get("alternative_flow") or s.get("alternativeFlow") or "—"
        status = s.get("status") or "DRAFT"
        lines += [
            f"### {sid} {title}",
            "",
            f"- **시작**: {pre}",
            f"- **종료**: {post}",
            f"- **기본 흐름**: {normal}",
            f"- **예외**: {alt or '—'}",
            f"- **상태**: {status}",
            "",
        ]
        mmd = (s.get("mermaid_script") or s.get("mermaid") or "").strip()
        if mmd:
            lines += ["```mermaid", mmd, "```", ""]
    return "\n".join(lines)


def main() -> int:
    scenarios = api_get(f"/api/workspaces/{WS}/scenarios")
    if not isinstance(scenarios, list):
        print("FAIL: unexpected API response", file=sys.stderr)
        return 1
    import_rows = [scenario_to_import(s) for s in sorted(scenarios, key=lambda x: x["id"])]
    IMPORT_PATH.write_text(
        json.dumps(import_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {IMPORT_PATH} ({len(import_rows)} scenarios)")
    WIKI_PATH.write_text(gen_user_scenarios_md(scenarios), encoding="utf-8")
    print(f"Wrote {WIKI_PATH}")
    scr_count = sum(1 for s in import_rows if "SCR-" in s.get("mermaid", ""))
    print(f"Mermaid with SCR ID: {scr_count}/{len(import_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
