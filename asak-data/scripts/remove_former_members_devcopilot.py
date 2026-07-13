#!/usr/bin/env python3
"""Remove former-member names from DevCopilot workspace 2 without deleting work.

Default mode is a dry run.  Pass --apply only after reviewing its output.
Task assignees are replaced from the current Notion WBS assignment.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.request
from pathlib import Path


BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
FORMER_NAMES = ("박유진", "강민준", "김민준")
ROOT = Path(__file__).resolve().parents[2]
WBS_CSV = ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/07 WBS 개발 진행 현황/WBS 개발 진행 데이터베이스.csv"


def api(method: str, path: str, body: dict | None = None) -> object:
    token = os.getenv("DEVCOPILOT_TOKEN")
    if not token:
        raise RuntimeError("DEVCOPILOT_TOKEN is required")
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body else None
    request = urllib.request.Request(
        f"{BASE}{path}", data=data, method=method,
        headers={"Content-Type": "application/json", "x-user-username": "hagenie128",
                 "Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def contains_former_name(value: object) -> bool:
    return isinstance(value, str) and any(name in value for name in FORMER_NAMES)


def clean_text(value: str) -> str:
    for name in FORMER_NAMES:
        value = value.replace(name, "")
    return value


def assignee_map() -> dict[str, str]:
    """Use the current Notion WBS assignment; DevCopilot supports one assignee."""
    with WBS_CSV.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["작업 ID"]: row["담당자"].split(",")[0].strip()
            for row in csv.DictReader(file)
            if row.get("작업 ID") and row.get("담당자")
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="perform updates; default is dry run")
    args = parser.parse_args()
    assigned = assignee_map()

    changed = 0
    for wiki in api("GET", f"/api/workspaces/{WS}/wikis"):
        if not contains_former_name(wiki.get("content")):
            continue
        changed += 1
        print(f"wiki {wiki['id']}: remove former-member name(s)")
        if args.apply:
            api("PUT", f"/api/workspaces/{WS}/wikis/{wiki['id']}", {
                "title": wiki["title"], "content": clean_text(wiki["content"]),
            })

    for task in api("GET", f"/api/workspaces/{WS}/tasks"):
        if not contains_former_name(task.get("assignee_name")):
            continue
        changed += 1
        # UI work defaults to 김나연; a linkage/QA task not present in the
        # Notion export defaults to 이하진.  Explicit Notion WBS values win.
        replacement = assigned.get(
            task["task_id"], "이하진" if task["task_id"] == "WBS-031" else "김나연"
        )
        print(f"task {task['task_id']}: reassign to {replacement}")
        if args.apply:
            api("PUT", f"/api/workspaces/{WS}/tasks/{task['id']}", {
                "task_id": task["task_id"], "title": task["title"], "assignee_name": replacement,
                "start_date": task.get("start_date") or "2026-07-01",
                "end_date": task.get("end_date") or "2026-07-31",
                "status": task.get("status") or "TODO",
            })
    print(f"{'updated' if args.apply else 'would update'} {changed} record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
