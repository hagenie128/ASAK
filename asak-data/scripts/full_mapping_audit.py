#!/usr/bin/env python3
"""Comprehensive Hub mapping audit vs req_link_maps.py and notion_data.json."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests

from req_link_maps import (
    API_REQ_MAP,
    API_EXTRA_REQS,
    EXCLUDED_REQ_IDS,
    SCENARIO_REQ_MAP,
    SCR_REQ_MAP,
    TC_REQ_OVERRIDE,
    TC_SCENARIO_MAP,
    format_req_label,
)

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}
SCRIPT_DIR = Path(__file__).parent
NOTION_PATH = SCRIPT_DIR / "notion_data.json"


def get_json(path: str):
    r = requests.get(f"{BASE}{path}", headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def load_notion() -> dict:
    if NOTION_PATH.exists():
        return json.loads(NOTION_PATH.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    report: dict = {
        "critical": [],
        "warnings": [],
        "ok": {},
        "excluded_samples": {},
        "api_018_020": {},
        "matrix": {},
    }

    reqs = get_json(f"/api/workspaces/{WS}/requirements")
    scenarios = get_json(f"/api/workspaces/{WS}/scenarios")
    screens = get_json(f"/api/workspaces/{WS}/screens")
    qa = get_json(f"/api/workspaces/{WS}/qa")
    apis = get_json(f"/api/workspaces/{WS}/apis")
    wikis = get_json(f"/api/workspaces/{WS}/wikis")
    notion = load_notion()

    # --- Requirements ---
    req_ids = [r["id"] for r in reqs if not str(r.get("id", "")).startswith("TEST")]
    dup = [x for x in req_ids if req_ids.count(x) > 1]
    if dup:
        report["critical"].append({"area": "requirements", "issue": "duplicate_ids", "ids": sorted(set(dup))})

    excluded_hub = sorted(r["id"] for r in reqs if r.get("status") == "EXCLUDED")
    excluded_expected = sorted(EXCLUDED_REQ_IDS)
    if set(excluded_hub) != set(excluded_expected):
        report["warnings"].append({
            "area": "requirements",
            "issue": "excluded_mismatch",
            "hub": excluded_hub,
            "expected": excluded_expected,
        })

    todo_count = sum(1 for r in reqs if r.get("status") != "EXCLUDED" and not str(r.get("id", "")).startswith("TEST"))
    report["ok"]["requirements"] = {
        "total": len(req_ids),
        "todo": todo_count,
        "excluded": len(excluded_hub),
        "duplicates": len(set(dup)),
    }

    # Notion comparison
    notion_reqs = {r["id"]: r for r in notion.get("requirements", [])}
    notion_only = set(notion_reqs) - set(req_ids)
    hub_only = set(req_ids) - set(notion_reqs)
    if notion_only:
        report["warnings"].append({"area": "requirements", "issue": "notion_only", "ids": sorted(notion_only)})
    if hub_only:
        report["warnings"].append({"area": "requirements", "issue": "hub_only", "ids": sorted(hub_only)})

    # --- Scenarios ---
    sc_ids = sorted(s["id"] for s in scenarios)
    expected_sc = [f"SC-{i:03d}" for i in range(1, 25)]
    missing_sc = [x for x in expected_sc if x not in sc_ids]
    if missing_sc:
        report["critical"].append({"area": "scenarios", "issue": "missing", "ids": missing_sc})

    for s in scenarios:
        sid = s["id"]
        title = s.get("title", "")
        expected = SCENARIO_REQ_MAP.get(sid, [])
        primary = expected[0] if expected else None
        if primary and primary not in title:
            report["critical"].append({
                "area": "scenarios", "id": sid, "issue": "wrong_primary_req",
                "expected": primary, "title": title,
            })
        if primary and primary in EXCLUDED_REQ_IDS:
            label = format_req_label(primary)
            if label not in title:
                report["critical"].append({
                    "area": "scenarios", "id": sid, "issue": "missing_excluded_marker",
                    "expected": label, "title": title,
                })
        mermaid = s.get("mermaid_script", "") or ""
        if sid not in ("SC-019", "SC-023") and "SCR-" not in mermaid and len(mermaid) > 0:
            report["warnings"].append({"area": "scenarios", "id": sid, "issue": "no_scr_in_mermaid"})

    report["ok"]["scenarios"] = {"count": len(scenarios), "range": f"{sc_ids[0]}..{sc_ids[-1]}" if sc_ids else "none"}

    # --- Screens ---
    scr_ids = sorted(s["id"] for s in screens)
    expected_scr = [f"SCR-{i:03d}" for i in range(1, 22)]
    missing_scr = [x for x in expected_scr if x not in scr_ids]
    if missing_scr:
        report["critical"].append({"area": "screens", "issue": "missing", "ids": missing_scr})

    figma_count = sum(1 for s in screens if s.get("figmaUrl") or s.get("figma_url"))
    for s in screens:
        sid = s["id"]
        name = s.get("name", "")
        expected = SCR_REQ_MAP.get(sid, [])
        primary = expected[0] if expected else None
        if primary and primary not in name:
            report["critical"].append({
                "area": "screens", "id": sid, "issue": "wrong_primary_req",
                "expected": primary, "name": name,
            })
        for sec in expected[1:]:
            if sec in EXCLUDED_REQ_IDS:
                label = format_req_label(sec)
                if sec in name and "(EXCLUDED)" not in name:
                    report["warnings"].append({
                        "area": "screens", "id": sid, "issue": "secondary_excluded_no_marker",
                        "req": sec, "name": name,
                    })

    report["ok"]["screens"] = {"count": len(screens), "figmaUrl_count": figma_count}

    # --- QA/TC ---
    tc_ids = sorted(q["id"] for q in qa)
    expected_tc = [f"TC-{i:03d}" for i in range(1, 17)]
    missing_tc = [x for x in expected_tc if x not in tc_ids]
    if missing_tc:
        report["critical"].append({"area": "qa", "issue": "missing", "ids": missing_tc})

    for q in qa:
        tc_id = q["id"]
        title = q.get("title", "")
        purpose = q.get("purpose", "") or ""
        expected_reqs = TC_REQ_OVERRIDE.get(tc_id, [])
        for rid in expected_reqs:
            if rid not in title and rid not in purpose:
                report["critical"].append({
                    "area": "qa", "id": tc_id, "issue": "missing_req_ref",
                    "expected": rid, "title": title,
                })
            if rid in EXCLUDED_REQ_IDS and format_req_label(rid) not in title:
                report["critical"].append({
                    "area": "qa", "id": tc_id, "issue": "missing_excluded_marker",
                    "expected": format_req_label(rid), "title": title,
                })

    # TC-014 specific check
    tc014 = next((q for q in qa if q["id"] == "TC-014"), None)
    if tc014:
        t = tc014.get("title", "") + (tc014.get("purpose", "") or "")
        if "FWD-MENU-001" in t and "LMIS-ORDER-001" not in t:
            report["critical"].append({"area": "qa", "id": "TC-014", "issue": "wrong_req_FWD-MENU-001"})
        if "LMIS-ORDER-001" not in t or "LMIS-ORDER-003" not in t:
            report["warnings"].append({
                "area": "qa", "id": "TC-014", "issue": "expected_LMIS-ORDER-001/003",
                "title": tc014.get("title", ""),
            })

    report["ok"]["qa"] = {"count": len(qa)}

    # --- APIs ---
    api_by_id: dict[str, dict] = {}
    for a in apis:
        title = a.get("title", "")
        m = re.search(r"API-(\d{3})", title)
        if m:
            api_by_id[f"API-{m.group(1)}"] = a

    expected_api = [f"API-{i:03d}" for i in range(1, 21)]
    missing_api = [x for x in expected_api if x not in api_by_id]
    if missing_api:
        report["critical"].append({"area": "apis", "issue": "missing", "ids": missing_api})

    for api_id in ("API-018", "API-019", "API-020"):
        row = api_by_id.get(api_id)
        expected_req = API_REQ_MAP.get(api_id)
        notion_api = next((a for a in notion.get("apis", []) if a.get("api_id") == api_id), None)
        report["api_018_020"][api_id] = {
            "on_hub": row is not None,
            "endpoint": row.get("endpoint") if row else None,
            "expected_req": expected_req,
            "notion_title": notion_api.get("title") if notion_api else None,
        }
        if row:
            desc = (row.get("description") or "") + (row.get("title") or "")
            if expected_req and expected_req not in desc:
                report["warnings"].append({
                    "area": "apis", "id": api_id, "issue": "req_not_in_description",
                    "expected": expected_req,
                })

    report["ok"]["apis"] = {"count": len(apis), "mapped_ids": len(api_by_id)}

    # --- Wiki ---
    wiki_by_id = {w["id"]: w for w in wikis}
    wiki_titles = [(w["id"], w.get("title", "")) for w in wikis]
    dup18 = [w for w in wikis if w.get("id") == 18]
    report["ok"]["wiki"] = {
        "wiki10_exists": 10 in wiki_by_id,
        "wiki14_exists": 14 in wiki_by_id,
        "wiki18_count": len(dup18),
        "wiki10_sc_count": (wiki_by_id.get(10, {}).get("content", "") or "").count("### SC-"),
        "wiki16_scr020": "SCR-020" in (wiki_by_id.get(16, {}).get("content", "") or ""),
        "wiki16_scr021": "SCR-021" in (wiki_by_id.get(16, {}).get("content", "") or ""),
    }
    if len(dup18) > 1:
        report["critical"].append({"area": "wiki", "issue": "duplicate_wiki_18"})

    # --- EXCLUDED samples ---
    for label, items, key in [
        ("scenario", scenarios, "title"),
        ("screen", screens, "name"),
        ("tc", qa, "title"),
    ]:
        for item in items:
            for rid in EXCLUDED_REQ_IDS:
                raw = item.get(key, "")
                if rid in raw:
                    report["excluded_samples"].setdefault(label, []).append({
                        "id": item["id"],
                        "text": raw,
                        "has_marker": "(EXCLUDED)" in raw,
                    })

    # --- Mapping matrix ---
    report["matrix"] = {
        "SC_to_REQ": {k: v[0] if v else None for k, v in sorted(SCENARIO_REQ_MAP.items())},
        "SCR_to_REQ_primary": {k: v[0] if v else None for k, v in sorted(SCR_REQ_MAP.items())},
        "TC_to_REQ": dict(sorted(TC_REQ_OVERRIDE.items())),
        "TC_to_SC": dict(sorted(TC_SCENARIO_MAP.items())),
        "API_to_REQ": dict(sorted(API_REQ_MAP.items())),
    }

    # Print summary
    out_path = SCRIPT_DIR / "full_mapping_audit_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== FULL MAPPING AUDIT ===")
    print(f"Critical errors: {len(report['critical'])}")
    for c in report["critical"][:30]:
        print(f"  CRITICAL: {json.dumps(c, ensure_ascii=False)}")
    print(f"\nWarnings: {len(report['warnings'])}")
    for w in report["warnings"][:20]:
        print(f"  WARN: {json.dumps(w, ensure_ascii=False)}")
    print(f"\nOK: {json.dumps(report['ok'], ensure_ascii=False, indent=2)}")
    print(f"\nAPI 018-020: {json.dumps(report['api_018_020'], ensure_ascii=False, indent=2)}")
    print(f"\nEXCLUDED samples:")
    for k, v in report.get("excluded_samples", {}).items():
        for s in v[:3]:
            print(f"  {k} {s['id']}: marker={s['has_marker']} text={s['text']!r}")
    print(f"\nReport: {out_path}")
    return 1 if report["critical"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
