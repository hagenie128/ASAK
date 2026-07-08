#!/usr/bin/env python3
"""Verify NOTION_TOKEN and access to the ASAK daily worklog database.

Usage:
  python asak-data/scripts/verify_notion_token.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

NOTION_VERSION = "2022-06-28"
ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "worklog" / "notion_config.json"


def notion_request(token: str, method: str, url: str, body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
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


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print("ERROR: NOTION_TOKEN 환경 변수가 설정되지 않았습니다.", file=sys.stderr)
        print("  PowerShell: $env:NOTION_TOKEN = \"secret_...\"", file=sys.stderr)
        print("  가이드: docs/GETTING_STARTED.md#part-2--워크로그-쓰기-유치원-선생님-모드", file=sys.stderr)
        return 1

    me = notion_request(token, "GET", "https://api.notion.com/v1/users/me")
    bot_name = me.get("name") or me.get("bot", {}).get("owner", {}).get("user", {}).get("name", "(unknown)")
    print(f"OK: Integration 연결됨 — bot/user: {bot_name}")

    if not CONFIG_PATH.is_file():
        print(f"WARN: {CONFIG_PATH} 없음 — DB 접근 테스트 생략", file=sys.stderr)
        return 0

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    database_id = config["database_id"]
    db = notion_request(token, "GET", f"https://api.notion.com/v1/databases/{database_id}")
    title_parts = db.get("title", [])
    db_title = "".join(part.get("plain_text", "") for part in title_parts) or database_id
    print(f"OK: 워크로그 DB 접근 — {db_title}")
    print(f"    URL: {config.get('database_url', '')}")

    query = notion_request(
        token,
        "POST",
        f"https://api.notion.com/v1/databases/{database_id}/query",
        {"page_size": 1},
    )
    count_hint = len(query.get("results", []))
    print(f"OK: DB query 성공 (샘플 {count_hint}건 조회)")
    print("\n다음 단계:")
    print("  python worklog/scripts/sync_daily_to_notion.py --date today --dry-run")
    print("  python asak-data/scripts/create_worklog.py --date today --author 이하진 --task \"테스트\" --dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
