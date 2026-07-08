#!/usr/bin/env python3
"""Comprehensive REQ linkage gap audit for DevCopilot workspace 2."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import requests

from req_link_maps import REQ_ID_RE, SCENARIO_REQ_MAP, SCR_REQ_MAP

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}


def get_json(path: str):
    r = requests.get(f"{BASE}{path}", headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def section_line(content: str, marker: str) -> str | None:
    idx = content.find(marker)
    if idx < 0:
        return None
    end = content.find("\n", idx)
    return content[idx : end if end > 0 else idx + 300]


def audit() -> dict:
    requirements = get_json(f"/api/workspaces/{WS}/requirements")
    req_ids = sorted(
        r["id"] for r in requirements if not str(r["id"]).startswith("TEST")
    )
    scenarios = get_json(f"/api/workspaces/{WS}/scenarios")
    screens = get_json(f"/api/workspaces/{WS}/screens")
    wikis = {w["id"]: w for w in get_json(f"/api/workspaces/{WS}/wikis")}

    report: dict = {
        "scenario_title_gaps": [],
        "screen_name_gaps": [],
        "wiki16_scr_line_gaps": [],
        "wiki10_sc_line_gaps": [],
        "wiki5_stale": {},
        "req_no_scenario_screen": [],
        "missing_kSD_MEMBER": [],
    }

    for s in sorted(scenarios, key=lambda x: x["id"]):
        sid = s["id"]
        expected = SCENARIO_REQ_MAP.get(sid, [])
        title = s.get("title", "")
        primary = expected[0] if expected else None
        if primary and primary not in title:
            report["scenario_title_gaps"].append(
                {"id": sid, "expected_primary": primary, "title": title}
            )

    for s in sorted(screens, key=lambda x: x["id"]):
        sid = s["id"]
        expected = SCR_REQ_MAP.get(sid, [])
        name = s.get("name", "")
        primary = expected[0] if expected else None
        if primary and primary not in name:
            report["screen_name_gaps"].append(
                {"id": sid, "missing_primary": primary, "name": name}
            )

    c16 = wikis.get(16, {}).get("content", "")
    for scr, reqs in sorted(SCR_REQ_MAP.items()):
        line = section_line(c16, f"## {scr} ")
        if not line:
            report["wiki16_scr_line_gaps"].append({"scr": scr, "issue": "section_missing"})
            continue
        missing = [r for r in reqs if r != reqs[0] and r not in line]
        if reqs and reqs[0] not in line:
            report["wiki16_scr_line_gaps"].append(
                {"scr": scr, "missing_primary": reqs[0], "line": line[:120]}
            )

    c10 = wikis.get(10, {}).get("content", "")
    for sid, reqs in sorted(SCENARIO_REQ_MAP.items()):
        line = section_line(c10, f"### {sid} ")
        if not line:
            line = section_line(c10, f"### {sid}")
        if not line:
            report["wiki10_sc_line_gaps"].append({"sc": sid, "issue": "section_missing"})
            continue
        primary = reqs[0] if reqs else None
        if primary and primary not in line:
            report["wiki10_sc_line_gaps"].append(
                {"sc": sid, "expected_primary": primary, "line": line[:120]}
            )

    c5 = wikis.get(5, {}).get("content", "")
    report["wiki5_stale"] = {
        "has_scr020": "SCR-020" in c5,
        "has_scr021": "SCR-021" in c5,
        "sc_count": c5.count("### SC-"),
    }

    all_sc_titles = " ".join(s.get("title", "") for s in scenarios)
    for rid in req_ids:
        if rid not in all_sc_titles and rid not in c16 and rid not in c10:
            report["req_no_scenario_screen"].append(rid)

    # KSD-MEMBER-001 referenced in maps but may not be a requirement
    for label, blob in [
        ("screens_json", Path(__file__).resolve().parents[2] / "docs/screens/screens.json"),
        ("req_link_maps", "SCR-021"),
    ]:
        pass
    notion_req_ids = {r["id"] for r in requirements}
    for maps_name, data in [
        ("SCR_REQ_MAP", SCR_REQ_MAP),
        ("SCENARIO_REQ_MAP", SCENARIO_REQ_MAP),
    ]:
        for _id, rlist in data.items():
            for rid in rlist:
                if rid not in notion_req_ids and rid not in report["missing_kSD_MEMBER"]:
                    report["missing_kSD_MEMBER"].append(
                        {"req": rid, "referenced_in": maps_name, "artifact": _id}
                    )

    report["summary"] = {
        "requirements": len(req_ids),
        "scenarios": len(scenarios),
        "screens": len(screens),
        "scenario_title_gaps": len(report["scenario_title_gaps"]),
        "screen_name_gaps": len(report["screen_name_gaps"]),
        "wiki16_gaps": len(report["wiki16_scr_line_gaps"]),
        "wiki10_gaps": len(report["wiki10_sc_line_gaps"]),
        "orphan_req_refs": len(report["missing_kSD_MEMBER"]),
    }
    return report


def main() -> int:
    report = audit()
    out = Path(__file__).parent / "req_link_gap_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    s = report["summary"]
    print(json.dumps(s, ensure_ascii=False, indent=2))
    if report["scenario_title_gaps"]:
        print("\nScenario gaps:", report["scenario_title_gaps"][:5])
    if report["screen_name_gaps"]:
        print("\nScreen gaps:", report["screen_name_gaps"][:5])
    if report["wiki16_scr_line_gaps"]:
        print("\nWiki16 gaps:", report["wiki16_scr_line_gaps"][:5])
    if report["wiki10_sc_line_gaps"]:
        print("\nWiki10 gaps:", report["wiki10_sc_line_gaps"][:5])
    if report["missing_kSD_MEMBER"]:
        print("\nMap refs not in requirements API:", report["missing_kSD_MEMBER"])
    print(f"\nReport: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
