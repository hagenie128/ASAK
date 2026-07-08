#!/usr/bin/env python3
"""Create or update a single row in the Notion 📅 일일 워크로그 database.

Reads NOTION_TOKEN from the environment. Upserts by date + assignee (same as sync_daily_to_notion.py).

Usage:
  python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "SCR-003 옵션 UI"
  python asak-data/scripts/create_worklog.py --date 2026-07-06 --author 김나연 --task "API 골격" --ref WBS-002 --hours 2 --notes "스모크 통과"
  python asak-data/scripts/create_worklog.py --date today --author 이하진 --task "테스트" --dry-run

Field mapping (CLI → Notion):
  --date     → 날짜
  --author   → 담당 (select)
  --task     → 요약 (main line)
  --ref      → WBS (SCR-xxx, SC-xxx, WBS-xxx)
  --hours    → appended to 요약 as "(Nh)"
  --notes    → appended to 요약
  --git-daily → Git daily (url)
  --blocker  → 블로커 (checkbox)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

NOTION_VERSION = "2022-06-28"
ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "worklog" / "notion_config.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_ASSIGNEES = frozenset({"이하진", "김나연", "박유진", "강민준", "미지정"})


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.is_file():
        raise FileNotFoundError(f"Missing {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def resolve_date(value: str) -> str:
    if value.lower() in ("today", "오늘"):
        return date.today().isoformat()
    if not DATE_RE.match(value):
        raise ValueError(f"Invalid date: {value!r} (expected YYYY-MM-DD or 'today')")
    return value


def build_summary(task: str, hours: float | None, notes: str) -> str:
    parts = [task.strip()]
    if hours is not None:
        h = int(hours) if hours == int(hours) else hours
        parts.append(f"({h}h)")
    if notes.strip():
        parts.append(notes.strip())
    return " — ".join(parts) if len(parts) > 1 and notes.strip() else " ".join(parts)


class NotionClient:
    def __init__(self, token: str, database_id: str) -> None:
        self.token = token
        self.database_id = database_id

    def _request(self, method: str, url: str, body: dict | None = None) -> dict:
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Notion API {method} failed ({exc.code}): {detail}") from exc

    def find_existing(self, day: str, assignee: str) -> str | None:
        body = {
            "filter": {
                "and": [
                    {"property": "날짜", "date": {"equals": day}},
                    {"property": "담당", "select": {"equals": assignee}},
                ]
            }
        }
        result = self._request(
            "POST",
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            body,
        )
        rows = result.get("results", [])
        return rows[0]["id"] if rows else None

    def upsert(self, payload: dict[str, Any]) -> dict[str, str]:
        day = payload["day"]
        assignee = payload["assignee"]
        page_id = self.find_existing(day, assignee)

        properties: dict[str, Any] = {
            "제목": {"title": [{"text": {"content": payload["title"]}}]},
            "날짜": {"date": {"start": day}},
            "담당": {"select": {"name": assignee}},
            "요약": {"rich_text": [{"text": {"content": payload["summary"]}}]},
            "블로커": {"checkbox": payload["blocker"]},
        }
        if payload.get("ref"):
            properties["WBS"] = {"rich_text": [{"text": {"content": payload["ref"]}}]}
        if payload.get("git_daily"):
            properties["Git daily"] = {"url": payload["git_daily"]}

        if page_id:
            result = self._request(
                "PATCH",
                f"https://api.notion.com/v1/pages/{page_id}",
                {"properties": properties},
            )
            action = "updated"
        else:
            result = self._request(
                "POST",
                "https://api.notion.com/v1/pages",
                {"parent": {"database_id": self.database_id}, "properties": properties},
            )
            action = "created"

        return {
            "action": action,
            "page_id": result["id"],
            "url": result.get("url", ""),
            "title": payload["title"],
            "담당": assignee,
            "날짜": day,
        }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Create/update one Notion daily worklog row")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD or 'today'")
    parser.add_argument("--author", required=True, help="담당자 실명 (select 옵션과 일치)")
    parser.add_argument("--task", required=True, help="작업 한 줄 요약")
    parser.add_argument("--ref", default="", help="SCR/SC/WBS 참조 (WBS 필드)")
    parser.add_argument("--hours", type=float, default=None, help="투입 시간 (요약에 붙음)")
    parser.add_argument("--notes", default="", help="추가 메모 (요약에 붙음)")
    parser.add_argument("--git-daily", default="", help="Git daily md URL")
    parser.add_argument("--blocker", action="store_true", help="블로커 있음")
    parser.add_argument("--dry-run", action="store_true", help="API 호출 없이 payload만 출력")
    args = parser.parse_args()

    try:
        day = resolve_date(args.date)
        assignee = args.author.strip()
        if assignee not in VALID_ASSIGNEES:
            raise ValueError(
                f"담당 '{assignee}' 는 DB select 옵션에 없습니다. "
                f"허용: {', '.join(sorted(VALID_ASSIGNEES))}"
            )
        config = load_config()
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    title = f"{day} {assignee} 일일"
    summary = build_summary(args.task, args.hours, args.notes)
    payload = {
        "day": day,
        "assignee": assignee,
        "title": title,
        "summary": summary,
        "ref": args.ref.strip(),
        "git_daily": args.git_daily.strip(),
        "blocker": args.blocker,
        "database_id": config["database_id"],
        "database_url": config.get("database_url", ""),
    }

    if args.dry_run:
        print(json.dumps({"dry_run": True, "payload": payload}, ensure_ascii=False, indent=2))
        return 0

    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print(
            "NOTION_TOKEN not set. Set env var or see docs/GETTING_STARTED.md#part-2--워크로그-쓰기-유치원-선생님-모드",
            file=sys.stderr,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    try:
        client = NotionClient(token, config["database_id"])
        result = client.upsert(payload)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"{result['action']}: {result['url']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
