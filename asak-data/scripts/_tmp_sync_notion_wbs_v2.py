# -*- coding: utf-8 -*-
"""Sync ASAK docs/wiki/wbs-v2-2026-07-16.md → Notion WBS DB (WBS2 only)."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

TOKEN = os.environ.get("NOTION_TOKEN", "").strip()
if not TOKEN:
    sys.exit("NOTION_TOKEN not set")

API = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
WBS_DB = "dfd51ef0-4f0b-820e-9b5a-01f2c1343d16"
WBS_DOC = "1ab51ef0-4f0b-8330-afca-012a4e8d14fa"
REPO = Path(__file__).resolve().parents[2]
MD = REPO / "docs/wiki/wbs-v2-2026-07-16.md"
DATES = REPO / "docs/ai-reports/2026-08-07/wbs-date-rebase-plan.json"
OUT = REPO / "docs/ai-reports/2026-08-07/asak-notion-wbs-v2-sync.md"

STATUS_MAP = {
    "DONE": "완료",
    "TODO": "예정",
    "IN_PROGRESS": "진행중",
    "BLOCKED": "지연",
    "DELAYED": "지연",
    "IN_REVIEW": "검토중",
}

# Hub rebase windows by bucket (fallback if id missing in plan)
DEFAULT_DATES = {
    "p0_order": ("2026-08-07", "2026-08-11"),
    "p1_menu": ("2026-08-11", "2026-08-14"),
    "p2_sales": ("2026-08-14", "2026-08-18"),
    "p3_qa": ("2026-08-18", "2026-08-21"),
    "p4_docs": ("2026-08-14", "2026-08-21"),
    "backlog_design": ("2026-08-18", "2026-08-25"),
    "backlog_be": ("2026-08-14", "2026-08-20"),
}

BUCKET = {
    **{f"WBS2-{i:03d}": "p0_order" for i in list(range(18, 32)) + [35, 36, 37, 50, 51, 53, 55, 57, 58, 59]},
    **{f"WBS2-{i:03d}": "p1_menu" for i in [38, 39, 48, 49, 52]},
    **{f"WBS2-{i:03d}": "p2_sales" for i in [33, 34] + list(range(40, 45)) + [54]},
    **{f"WBS2-{i:03d}": "p3_qa" for i in [24, 29, 30, 32, 45, 60, 61, 62, 63]},
    **{f"WBS2-{i:03d}": "p4_docs" for i in [5, 6, 7, 8, 56, 64, 65, 66]},
    **{f"WBS2-{i:03d}": "backlog_design" for i in list(range(10, 17))},
    **{f"WBS2-{i:03d}": "backlog_be" for i in [3, 4, 46, 47]},
    "WBS2-001": "p4_docs",
    "WBS2-002": "p4_docs",
    "WBS2-009": "backlog_design",
    "WBS2-017": "p0_order",
    "WBS2-022": "p0_order",
    "WBS2-023": "p0_order",
}


def phase_meta(phase: str) -> tuple[str, str]:
    """Return (구분, 단계)."""
    if phase.startswith("P1"):
        return "문서", "PLAN"
    if phase.startswith("P2"):
        return "디자인", "PLAN"
    if phase.startswith("P3"):
        return "프론트엔드", "FWD"
    if phase.startswith("P4"):
        return "프론트엔드", "LMIS"
    if phase.startswith("P5"):
        return "백엔드", "DEV"
    if phase.startswith("P6"):
        return "협업", "DEV"
    if phase.startswith("P7"):
        return "테스트", "TEST"
    if "Presentation" in phase or "Demo" in phase:
        return "발표", "PRESENT"
    if phase.startswith("P8"):
        return "문서", "PRESENT"
    return "협업", "DEV"


def parse_md() -> list[dict]:
    rows = []
    for line in MD.read_text(encoding="utf-8").splitlines():
        m = re.match(
            r"\| (WBS2-\d{3}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| (DONE|TODO|IN_PROGRESS|BLOCKED|DELAYED|IN_REVIEW) \| ([^|]+) \| ([^|]+) \|",
            line,
        )
        if not m:
            continue
        tid, phase, task, repo, owners, status, handoff, evidence = [
            x.strip() for x in m.groups()
        ]
        primary = owners.split("/")[0].strip()
        primary = primary.replace("하진", "이하진").replace("나연", "김나연")
        if primary in ("NEEDS_CONFIRMATION", "—", "-"):
            primary = ""
        gubun, dangye = phase_meta(phase)
        rows.append(
            {
                "id": tid,
                "phase": phase,
                "task": task,
                "repo": repo,
                "owners": owners,
                "assignee": primary,
                "status": status,
                "notion_status": STATUS_MAP[status],
                "handoff": handoff,
                "evidence": evidence[:1800],
                "구분": gubun,
                "단계": dangye,
            }
        )
    return rows


def load_dates() -> dict[str, tuple[str, str]]:
    dates: dict[str, tuple[str, str]] = {}
    if DATES.exists():
        for u in json.loads(DATES.read_text(encoding="utf-8")):
            dates[u["task_id"]] = (u["start_date"], u["end_date"])
    # DONE items not in rebase: short historical window
    for tid in ("WBS2-001", "WBS2-002", "WBS2-009", "WBS2-017", "WBS2-022", "WBS2-023"):
        dates.setdefault(tid, ("2026-07-16", "2026-07-22"))
    for tid, bucket in BUCKET.items():
        dates.setdefault(tid, DEFAULT_DATES[bucket])
    # release/demo longer
    dates["WBS2-065"] = ("2026-08-14", "2026-08-28")
    dates["WBS2-066"] = ("2026-08-14", "2026-08-28")
    return dates


def rt(content: str):
    return [{"type": "text", "text": {"content": (content or "")[:1900]}}]


def list_existing() -> dict[str, str]:
    """Map 작업 ID -> page_id."""
    found: dict[str, str] = {}
    cursor = None
    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        r = requests.post(
            f"{API}/databases/{WBS_DB}/query", headers=HEADERS, json=body, timeout=60
        )
        r.raise_for_status()
        data = r.json()
        for p in data.get("results", []):
            prop = p["properties"].get("작업 ID") or {}
            texts = prop.get("rich_text") or []
            wid = "".join(t.get("plain_text", "") for t in texts).strip()
            if wid:
                found[wid] = p["id"]
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return found


def props_for(row: dict, start: str, end: str) -> dict:
    note = f"[{row['phase']}] {row['repo']} · handoff: {row['handoff']} · {row['evidence']}"
    note = note[:1900]
    return {
        "작업명": {"title": rt(f"{row['id']} {row['task']}")},
        "작업 ID": {"rich_text": rt(row["id"])},
        "상태": {"select": {"name": row["notion_status"]}},
        "담당자": {"rich_text": rt(row["assignee"] or row["owners"])},
        "시작일": {"date": {"start": start}},
        "종료일": {"date": {"start": end}},
        "구분": {"select": {"name": row["구분"]}},
        "단계": {"select": {"name": row["단계"]}},
        "우선순위": {"select": {"name": "상"}},
        "진척률": {
            "number": 100
            if row["status"] == "DONE"
            else (50 if row["status"] == "IN_PROGRESS" else 0)
        },
        "관련 산출물": {"rich_text": rt(f"wbs-v2 · {row['repo']}")},
        "비고": {"rich_text": rt(note)},
    }


def upsert(row: dict, start: str, end: str, existing: dict[str, str]) -> str:
    body_props = props_for(row, start, end)
    page_id = existing.get(row["id"])
    if page_id:
        r = requests.patch(
            f"{API}/pages/{page_id}",
            headers=HEADERS,
            json={"properties": body_props},
            timeout=60,
        )
        action = "updated"
    else:
        r = requests.post(
            f"{API}/pages",
            headers=HEADERS,
            json={"parent": {"database_id": WBS_DB}, "properties": body_props},
            timeout=60,
        )
        action = "created"
    if r.status_code not in (200, 201):
        raise RuntimeError(f"{row['id']} {action} fail {r.status_code} {r.text[:400]}")
    pid = page_id or r.json()["id"]
    return f"{action} {row['id']} {pid}"


def update_parent_doc() -> None:
    # append callout children to WBS parent page
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📌"},
                "rich_text": rt(
                    "2026-08-07: 실행 정본은 Git wbs-v2-2026-07-16.md (WBS2-001~066). "
                    "Notion DB에 WBS2 행을 upsert함. 레거시 WBS-00x·SCHEDULE은 참고용."
                ),
            },
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Git wbs-v2",
                            "link": {
                                "url": "https://github.com/hagenie128/ASAK/blob/main/docs/wiki/wbs-v2-2026-07-16.md"
                            },
                        },
                    }
                ]
            },
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Hub WBS 상태·일정",
                            "link": {
                                "url": "https://devcopilot.ai.kr/workspace/2/wiki/81"
                            },
                        },
                    }
                ]
            },
        },
    ]
    r = requests.patch(
        f"{API}/blocks/{WBS_DOC}/children",
        headers=HEADERS,
        json={"children": children},
        timeout=60,
    )
    print("parent_doc", r.status_code)


def main() -> None:
    rows = parse_md()
    dates = load_dates()
    print("parsed", len(rows))
    existing = list_existing()
    print("existing_ids", len(existing), "wbs2_existing", sum(1 for k in existing if k.startswith("WBS2-")))

    logs = []
    for i, row in enumerate(rows, 1):
        start, end = dates.get(row["id"], ("2026-08-07", "2026-08-21"))
        try:
            msg = upsert(row, start, end, existing)
            print(f"[{i}/{len(rows)}] {msg}")
            logs.append(msg)
        except Exception as e:
            print(f"[{i}/{len(rows)}] FAIL {row['id']}: {e}")
            logs.append(f"FAIL {row['id']}: {e}")
        time.sleep(0.35)

    update_parent_doc()

    created = sum(1 for x in logs if x.startswith("created"))
    updated = sum(1 for x in logs if x.startswith("updated"))
    failed = sum(1 for x in logs if x.startswith("FAIL"))
    report = f"""# Notion WBS ← wbs-v2 동기화 (2026-08-07)

- 정본: `docs/wiki/wbs-v2-2026-07-16.md`
- Notion DB: https://app.notion.com/p/dfd51ef04f0b820e9b5a01f2c1343d16
- 상위 문서: https://app.notion.com/p/1ab51ef04f0b8330afca012a4e8d14fa

| 결과 | 건수 |
|---|---|
| created | {created} |
| updated | {updated} |
| fail | {failed} |

상태 매핑: DONE→완료, IN_PROGRESS→진행중, TODO→예정, BLOCKED/DELAYED→지연, IN_REVIEW→검토중.
일정: Hub 8/7 rebase 계획(`wbs-date-rebase-plan.json`) 우선.
레거시 `WBS-00x` / `SCHEDULE-*` 행은 삭제하지 않음(참고 유지).
"""
    OUT.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
