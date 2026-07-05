#!/usr/bin/env python3
"""Create a personal entry markdown from template if missing.

Usage:
  python worklog/scripts/init_entry.py --slug scr-003-menu-option-ui
  python worklog/scripts/init_entry.py --person 이하진 --date 2026-07-02 --slug scr-003
  python worklog/scripts/init_entry.py --slug api-bugfix --title "주문 API 버그 수정"
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from worklog_paths import ENTRIES_DIR, TEMPLATES_DIR, entries_path, resolve_person  # noqa: E402

ENTRY_TEMPLATE = TEMPLATES_DIR / "template-entry-stub.md"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def resolve_date(value: str) -> str:
    if value.lower() in ("today", "오늘"):
        return date.today().isoformat()
    if not DATE_RE.match(value):
        raise ValueError(f"Invalid date: {value!r} (expected YYYY-MM-DD or 'today')")
    return value


def normalize_slug(raw: str) -> str:
    slug = raw.strip().lower().replace("_", "-")
    slug = re.sub(r"[^a-z0-9-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug or not SLUG_RE.match(slug):
        raise ValueError(f"Invalid slug: {raw!r} (use lowercase letters, digits, hyphens)")
    return slug


def render_template(template_path: Path, day: str, person: str, title: str) -> str:
    text = template_path.read_text(encoding="utf-8")
    return (
        text.replace("{{DATE}}", day)
        .replace("{{PERSON}}", person)
        .replace("{{TITLE}}", title)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize personal worklog entry markdown")
    parser.add_argument("--slug", required=True, help="짧은 설명 (예: scr-003-menu-option-ui)")
    parser.add_argument("--date", default="today", help="YYYY-MM-DD or 'today'")
    parser.add_argument(
        "--person",
        default=None,
        help="담당자 실명. 생략 시 git user → team_config.json",
    )
    parser.add_argument("--title", default="", help="H1 제목 (기본: slug를 읽기 쉽게)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    try:
        day = resolve_date(args.date)
        person = resolve_person(args.person)
        slug = normalize_slug(args.slug)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not ENTRY_TEMPLATE.is_file():
        print(f"Error: missing template {ENTRY_TEMPLATE}", file=sys.stderr)
        return 1

    filename = f"{day}-{slug}.md"
    target = entries_path(person, filename)
    if target.is_file() and not args.force:
        print(f"Exists: {target}")
        return 0

    title = args.title.strip() or slug.replace("-", " ")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_template(ENTRY_TEMPLATE, day, person, title), encoding="utf-8")
    print(f"Created: {target}")
    print(f"Link in daily: entries/{person}/{filename}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
