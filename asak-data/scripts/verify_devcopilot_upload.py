#!/usr/bin/env python3
"""Verify DevCopilot wiki/scenario/API uploads."""
from __future__ import annotations

import json
import sys

import requests

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}


def main() -> int:
    wikis = requests.get(f"{BASE}/api/workspaces/{WS}/wikis", headers=HEADERS, timeout=120).json()
    print("=== Wiki pages (screen/scenario related) ===")
    for w in wikis:
        t = w.get("title", "")
        if any(k in t for k in ("화면", "시나리오", "SCR")):
            c = w.get("content", "")
            print(
                f"id={w['id']} title={t!r} chars={len(c)} "
                f"SCR-020={('SCR-020' in c)} SCR-021={('SCR-021' in c)} "
                f"SC-024={('SC-024' in c)} SC_count={c.count('### SC-')}"
            )

    sc = requests.get(f"{BASE}/api/workspaces/{WS}/scenarios", headers=HEADERS, timeout=120).json()
    ids = sorted(s["id"] for s in sc)
    print(f"\n=== Scenarios count={len(sc)} range={ids[0]}..{ids[-1]} ===")
    for sid in ["SC-003", "SC-006", "SC-015", "SC-016", "SC-024"]:
        s = next(x for x in sc if x["id"] == sid)
        m = s.get("mermaid_script", "")
        print(f"{sid}: title={s.get('title','')!r} SCR_in_mermaid={'SCR-' in m} mermaid_chars={len(m)}")

    apis = requests.get(f"{BASE}/api/workspaces/{WS}/apis", headers=HEADERS, timeout=120).json()
    api_endpoints = sorted((a.get("endpoint", ""), a.get("method", ""), a.get("title", "")) for a in apis)
    print(f"\n=== APIs count={len(apis)} ===")
    for endpoint, method, title in api_endpoints:
        if "membership/stamps" in endpoint or "receipt-print" in endpoint or "/device/scan" in endpoint:
            print(f"  {method} {endpoint} -> {title!r}")

    qa = requests.get(f"{BASE}/api/workspaces/{WS}/qa", headers=HEADERS, timeout=120).json()
    print("\n=== EXCLUDED marker samples ===")
    for tc_id in ("TC-009", "TC-016"):
        row = next((q for q in qa if q.get("id") == tc_id), None)
        if row:
            print(f"  {tc_id}: title={row.get('title','')!r}")
    sc016 = next((s for s in sc if s.get("id") == "SC-016"), None)
    if sc016:
        print(f"  SC-016: title={sc016.get('title','')!r}")

    reqs = requests.get(f"{BASE}/api/workspaces/{WS}/requirements", headers=HEADERS, timeout=120).json()
    for rid in ("KSD-MEMBER-001", "RTOS-DEVICE-004", "LMIS-AUTH-001"):
        row = next((r for r in reqs if r.get("id") == rid), None)
        if row:
            print(f"  {rid}: status={row.get('status')} title={row.get('title','')!r}")

    screens = requests.get(f"{BASE}/api/workspaces/{WS}/screens", headers=HEADERS, timeout=30).json()
    print("\n=== Screens API probe ===")
    print(f"GET /screens -> count={len(screens)}")
    for sid in ("SCR-015", "SCR-021"):
        row = next((s for s in screens if s.get("id") == sid), None)
        if row:
            print(f"  {sid}: name={row.get('name','')!r}")

    missing_ext = [
        ep for ep in ("/api/membership/stamps", "/api/orders/{orderId}/receipt-print", "/api/device/scan")
        if not any(a.get("endpoint") == ep for a in apis)
    ]
    if missing_ext:
        print(f"\nFAIL missing APIs: {missing_ext}", file=sys.stderr)
        return 1
    print("\nOK API-018~020 present on Hub")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
