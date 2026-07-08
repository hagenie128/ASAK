#!/usr/bin/env python3
"""Archive duplicate / empty rows in the Notion 📅 일일 워크로그 database.

Targets:
  - Title contains ``[중복`` or ``중복·통합됨`` → archive
  - Empty ``새 페이지`` template rows → archive
  - Wrong ``Git daily`` URL (missing ``{이름}/`` segment) → fix

Keeps canonical rows: 2026-07-05 이하진 4행, 팀 일일, _template, 🎯 milestones.

Usage:
  python worklog/scripts/archive_duplicate_worklogs.py --dry-run
  python worklog/scripts/archive_duplicate_worklogs.py
  python worklog/scripts/archive_duplicate_worklogs.py --fix-git-daily-only
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from worklog_paths import (  # noqa: E402
    NOTION_CONFIG_PATH,
    git_daily_url,
    load_team_config,
    team_dir_name,
)

NOTION_VERSION = "2022-06-28"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DUPLICATE_MARKERS = ("[중복", "중복·통합됨")
EMPTY_TEMPLATE_TITLES = frozenset({"새 페이지", "Untitled", ""})
KEEP_TITLE_PREFIXES = ("🎯", "_template")


def load_config() -> dict[str, Any]:
    if not NOTION_CONFIG_PATH.is_file():
        raise FileNotFoundError(f"Missing config: {NOTION_CONFIG_PATH}")
    return json.loads(NOTION_CONFIG_PATH.read_text(encoding="utf-8"))


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


def plain_text(prop: dict | None) -> str:
    if not prop:
        return ""
    chunks = prop.get("title") or prop.get("rich_text") or []
    return "".join(part.get("plain_text", "") for part in chunks).strip()


def query_all_pages(token: str, database_id: str) -> list[dict]:
    pages: list[dict] = []
    cursor: str | None = None
    while True:
        body: dict[str, Any] = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        result = notion_request(
            token,
            "POST",
            f"https://api.notion.com/v1/databases/{database_id}/query",
            body,
        )
        pages.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return pages


def parse_row(page: dict) -> dict[str, Any]:
    props = page.get("properties", {})
    title = plain_text(props.get("제목"))
    date_prop = props.get("날짜", {}).get("date") or {}
    day = (date_prop.get("start") or "")[:10]
    assignee = (props.get("담당", {}).get("select") or {}).get("name") or ""
    summary = plain_text(props.get("요약"))
    git_daily = props.get("Git daily", {}).get("url") or ""
    return {
        "page_id": page["id"],
        "url": page.get("url", ""),
        "title": title,
        "date": day,
        "assignee": assignee,
        "summary": summary,
        "git_daily": git_daily,
        "archived": page.get("archived", False),
    }


def is_duplicate_title(title: str) -> bool:
    return any(marker in title for marker in DUPLICATE_MARKERS)


def is_keep_special(title: str) -> bool:
    return title.startswith(KEEP_TITLE_PREFIXES)


def is_empty_template(row: dict) -> bool:
    title = row["title"]
    if title not in EMPTY_TEMPLATE_TITLES:
        return False
    if row["summary"]:
        return False
    if row["assignee"]:
        return False
    return not row["date"]


def assignee_folder(assignee: str) -> str:
    if assignee == "미지정":
        return team_dir_name()
    return assignee


def expected_git_daily(config: dict[str, Any], row: dict) -> str | None:
    day = row["date"]
    if not DATE_RE.match(day):
        return None
    folder = assignee_folder(row["assignee"])
    if not folder:
        return None
    return git_daily_url(config, folder, day)


def git_daily_needs_fix(config: dict[str, Any], row: dict) -> tuple[bool, str | None]:
    if is_duplicate_title(row["title"]) or is_empty_template(row) or is_keep_special(row["title"]):
        return False, None
    expected = expected_git_daily(config, row)
    if not expected:
        return False, None
    current = (row["git_daily"] or "").strip()
    if not current:
        return True, expected
    if current == expected:
        return False, None
    # Old flat path: .../daily/YYYY-MM-DD.md (no person folder)
    if re.search(r"/daily/\d{4}-\d{2}-\d{2}\.md$", current):
        return True, expected
    base = config.get("git_daily_base_url", "").rstrip("/")
    if base and current.startswith(base) and current != expected:
        return True, expected
    return False, None


def archive_page(token: str, page_id: str) -> dict:
    return notion_request(
        token,
        "PATCH",
        f"https://api.notion.com/v1/pages/{page_id}",
        {"archived": True},
    )


def fix_git_daily(token: str, page_id: str, url: str) -> dict:
    return notion_request(
        token,
        "PATCH",
        f"https://api.notion.com/v1/pages/{page_id}",
        {"properties": {"Git daily": {"url": url}}},
    )


def classify_rows(config: dict[str, Any], pages: list[dict]) -> dict[str, list[dict]]:
    active = [parse_row(p) for p in pages if not p.get("archived")]
    duplicates = [r for r in active if is_duplicate_title(r["title"])]
    empty_templates = [r for r in active if is_empty_template(r)]
    git_fixes: list[dict] = []
    for row in active:
        needs, expected = git_daily_needs_fix(config, row)
        if needs and expected:
            git_fixes.append({**row, "expected_git_daily": expected})
    kept = [
        r
        for r in active
        if r not in duplicates
        and r not in empty_templates
        and not any(r["page_id"] == g["page_id"] for g in git_fixes)
    ]
    # Re-include git-fix rows in kept (they stay, only URL changes)
    kept_ids = {r["page_id"] for r in kept}
    for g in git_fixes:
        if g["page_id"] not in kept_ids:
            kept.append(g)
    return {
        "active": active,
        "duplicates": duplicates,
        "empty_templates": empty_templates,
        "git_fixes": git_fixes,
        "kept": sorted(kept, key=lambda r: (r["date"], r["title"])),
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Archive duplicate Notion daily worklog rows")
    parser.add_argument("--dry-run", action="store_true", help="Preview only; no API writes")
    parser.add_argument(
        "--fix-git-daily-only",
        action="store_true",
        help="Only fix Git daily URLs; skip archive",
    )
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    args = parser.parse_args()

    try:
        config = load_config()
        load_team_config()
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        print("ERROR: NOTION_TOKEN 환경 변수가 설정되지 않았습니다.", file=sys.stderr)
        print("", file=sys.stderr)
        print("PowerShell:", file=sys.stderr)
        print('  $env:NOTION_TOKEN = "secret_..."', file=sys.stderr)
        print("  python worklog/scripts/archive_duplicate_worklogs.py --dry-run", file=sys.stderr)
        print("  python worklog/scripts/archive_duplicate_worklogs.py", file=sys.stderr)
        print("", file=sys.stderr)
        print("가이드: docs/GETTING_STARTED.md#part-2--워크로그-쓰기-유치원-선생님-모드", file=sys.stderr)
        return 2

    database_id = config["database_id"]
    pages = query_all_pages(token, database_id)
    groups = classify_rows(config, pages)

    archived: list[dict] = []
    fixed: list[dict] = []

    if not args.fix_git_daily_only:
        for row in groups["duplicates"] + groups["empty_templates"]:
            if args.dry_run:
                archived.append({**row, "action": "would_archive"})
            else:
                archive_page(token, row["page_id"])
                archived.append({**row, "action": "archived"})

    for row in groups["git_fixes"]:
        expected = row["expected_git_daily"]
        if args.dry_run:
            fixed.append(
                {
                    "page_id": row["page_id"],
                    "title": row["title"],
                    "from": row["git_daily"],
                    "to": expected,
                    "action": "would_fix",
                }
            )
        else:
            fix_git_daily(token, row["page_id"], expected)
            fixed.append(
                {
                    "page_id": row["page_id"],
                    "title": row["title"],
                    "from": row["git_daily"],
                    "to": expected,
                    "action": "fixed",
                }
            )

    report = {
        "database_id": database_id,
        "database_url": config.get("database_url", ""),
        "dry_run": args.dry_run,
        "fix_git_daily_only": args.fix_git_daily_only,
        "counts": {
            "active_rows": len(groups["active"]),
            "duplicate_candidates": len(groups["duplicates"]),
            "empty_template_candidates": len(groups["empty_templates"]),
            "git_daily_fix_candidates": len(groups["git_fixes"]),
            "archived_or_would": len(archived),
            "git_daily_fixed_or_would": len(fixed),
            "kept_after_cleanup": len(groups["kept"]) - len(archived),
        },
        "archived": archived,
        "git_daily_fixes": fixed,
        "kept_preview": [
            {
                "title": r["title"],
                "date": r["date"],
                "assignee": r["assignee"],
                "git_daily": r.get("git_daily") or r.get("expected_git_daily", ""),
            }
            for r in groups["kept"]
            if r["page_id"] not in {a["page_id"] for a in archived}
        ],
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        mode = "[dry-run] " if args.dry_run else ""
        print(f"{mode}일일 워크로그 DB 정리 결과")
        print(f"  DB: {config.get('database_url', database_id)}")
        print(f"  활성 행: {report['counts']['active_rows']}")
        print(f"  중복 후보: {report['counts']['duplicate_candidates']}")
        print(f"  빈 템플릿 후보: {report['counts']['empty_template_candidates']}")
        print(f"  Git daily 수정 후보: {report['counts']['git_daily_fix_candidates']}")
        print(f"  아카이브 {'예정' if args.dry_run else '완료'}: {len(archived)}")
        print(f"  Git daily {'수정 예정' if args.dry_run else '수정 완료'}: {len(fixed)}")
        if archived:
            print("\n아카이브 대상 (처음 5건):")
            for row in archived[:5]:
                print(f"  - {row['title'][:60]}")
            if len(archived) > 5:
                print(f"  ... 외 {len(archived) - 5}건")
        if fixed:
            print("\nGit daily 수정:")
            for row in fixed:
                print(f"  - {row['title']}: {row['from'] or '(없음)'} → {row['to']}")
        print("\n유지 행 미리보기:")
        for row in report["kept_preview"][:12]:
            print(f"  - {row['date']} | {row['assignee']} | {row['title'][:50]}")

    if args.dry_run:
        print("\n[dry-run] Notion에 쓰지 않았습니다. 적용: python worklog/scripts/archive_duplicate_worklogs.py", file=sys.stderr)
    else:
        print(
            f"\n완료: 아카이브 {len(archived)}건, Git daily 수정 {len(fixed)}건",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
