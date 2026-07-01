#!/usr/bin/env python3
"""진행 중 이벤트만 빠르게 수집합니다."""

from __future__ import annotations

import json
from pathlib import Path

from salady_scraper import SaladyScraper


def main() -> None:
    output_dir = Path("output")
    scraper = SaladyScraper(output_dir=output_dir, delay=0.3)
    events = scraper.scrape_events()
    (output_dir / "events.json").write_text(
        json.dumps(events, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"진행중 {events['summary']['ongoing_count']}개 저장 → "
        f"{(output_dir / 'events.json').resolve()}"
    )


if __name__ == "__main__":
    main()
