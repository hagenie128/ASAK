#!/usr/bin/env python3
"""Compare local wiki/docs with DevCopilot workspace 2."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import requests

BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
HEADERS = {"Content-Type": "application/json", "x-user-username": "hagenie128"}
REPO = Path(__file__).resolve().parents[2]
WIKI = REPO / "docs/wiki"
DATA = Path(__file__).parent / "notion_data.json"


def get(path: str):
    r = requests.get(BASE + path, headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()[:8]


UPLOADS = {
    "ASAK 요구사항 정의서": "requirements-definition.md",
    "ASAK 사용자 시나리오 명세": "user-scenarios.md",
    "ASAK 화면 설계 및 Figma 연동": "screen-design-figma.md",
    "ASAK DB 설계 테이블 정의서": "db-table-definition.md",
    "ASAK REST API 명세서": "rest-api-spec.md",
    "ASAK WBS 및 일정 계획": "wbs-schedule.md",
    "ASAK QA 테스트 케이스": "qa-test-cases.md",
    "ASAK 회의록 및 최종 배포 검증": "meeting-deliverables-checklist.md",
}


def main():
    wikis = get(f"/api/workspaces/{WS}/wikis")
    apis = get(f"/api/workspaces/{WS}/apis")
    reqs = get(f"/api/workspaces/{WS}/requirements")
    tasks = get(f"/api/workspaces/{WS}/tasks")
    qa = get(f"/api/workspaces/{WS}/qa")
    scenarios = get(f"/api/workspaces/{WS}/scenarios")

    wiki_by_title = {w["title"]: w for w in wikis}
    print("=== WIKI DIFF ===")
    wiki_diffs = []
    for title, fname in UPLOADS.items():
        local = (WIKI / fname).read_text(encoding="utf-8")
        w = wiki_by_title.get(title)
        if not w:
            print(f"MISSING: {title}")
            wiki_diffs.append({"title": title, "status": "missing"})
            continue
        remote = w.get("content") or ""
        match = md5(local) == md5(remote)
        day10_r = bool(re.search(r"Day\s*10|Day10", remote))
        day10_l = bool(re.search(r"Day\s*10|Day10", local))
        wiki_diffs.append(
            {
                "title": title,
                "id": w["id"],
                "match": match,
                "len_local": len(local),
                "len_remote": len(remote),
                "day10_local": day10_l,
                "day10_remote": day10_r,
            }
        )
        print(
            f"{title}: id={w['id']} match={match} "
            f"len={len(local)}/{len(remote)} day10_l={day10_l} day10_r={day10_r}"
        )

    print(f"\n=== API count={len(apis)} ===")
    day10_apis = [a for a in apis if re.search(r"Day\s*10|Day10", (a.get("title") or "") + (a.get("description") or ""))]
    print(f"day10_mentions={len(day10_apis)}")
    if apis:
        a0 = apis[0]
        print(f"sample title={a0.get('title','')[:50]}")
        print(f"sample response={ (a0.get('response_success') or '')[:100]}")

    data = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    notion_apis = [x for x in data.get("apis", []) if re.match(r"^API-0\d\d$", x.get("api_id", ""))]
    print(f"notion_data APIs={len(notion_apis)}")

    # Compare API endpoints
    remote_keys = {(a.get("method"), a.get("endpoint")) for a in apis}
    notion_keys = {(x.get("method"), x.get("endpoint")) for x in notion_apis}
    missing_on_dc = notion_keys - remote_keys
    extra_on_dc = remote_keys - notion_keys
    print(f"API missing on DevCopilot: {missing_on_dc}")
    print(f"API extra on DevCopilot: {extra_on_dc}")

    day10_reqs = [
        r
        for r in reqs
        if re.search(r"Day\s*10|Day10", (r.get("title") or "") + (r.get("description") or ""))
    ]
    print(f"\n=== REQUIREMENTS count={len(reqs)} day10={len(day10_reqs)} ===")

    day10_tasks = [
        t for t in tasks if re.search(r"Day\s*10|Day10", (t.get("title") or "") + (t.get("task_id") or ""))
    ]
    print(f"=== TASKS count={len(tasks)} day10={len(day10_tasks)} ===")
    print(f"=== QA count={len(qa)} SCENARIOS count={len(scenarios)} ===")

    notion_reqs = len(data.get("requirements", []))
    notion_tasks = len(data.get("tasks", []))
    notion_qa = len(data.get("qa", []))
    print(f"notion_data: reqs={notion_reqs} tasks={notion_tasks} qa={notion_qa} scenarios={len(data.get('scenarios',[]))}")

    out = Path(__file__).parent / "_devcopilot_compare.json"
    out.write_text(
        json.dumps(
            {
                "wiki": wiki_diffs,
                "counts": {
                    "wikis": len(wikis),
                    "apis": len(apis),
                    "reqs": len(reqs),
                    "tasks": len(tasks),
                    "qa": len(qa),
                    "scenarios": len(scenarios),
                },
                "day10": {"apis": len(day10_apis), "reqs": len(day10_reqs), "tasks": len(day10_tasks)},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
