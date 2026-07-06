#!/usr/bin/env python3
"""
DevCopilot 시나리오 자동 입력 (Playwright)

사전 준비:
  pip install playwright
  playwright install chromium

사용법:
  1) 첫 실행 — 로그인 세션 저장:
     python devcopilot/import_scenarios_playwright.py --login

  2) 시나리오 일괄 입력:
     python devcopilot/import_scenarios_playwright.py
     python devcopilot/import_scenarios_playwright.py --mvp-only
     python devcopilot/import_scenarios_playwright.py --start 5
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "scenarios_import.json"
STATE_PATH = ROOT / ".devcopilot_auth.json"
URL = "https://devcopilot.ai.kr/workspace/2/scenarios"

MVP_IDS = {
    "SC-001", "SC-002", "SC-003", "SC-004", "SC-005",
    "SC-007", "SC-008", "SC-009", "SC-012", "SC-014",
}

FIELD_LABELS = [
    ("시나리오 ID", "scenarioId"),
    ("시나리오 제목", "title"),
    ("시작 조건", "preCondition"),
    ("종료 조건", "postCondition"),
    ("기본 흐름", "normalFlow"),
    ("예외 흐름", "alternativeFlow"),
    ("Mermaid", "mermaid"),
]


def load_scenarios(mvp_only: bool) -> list[dict]:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    if mvp_only:
        data = [s for s in data if s.get("scenarioId") in MVP_IDS]
    return data


def fill_by_label(page, partial_label: str, value: str) -> None:
    page.evaluate(
        """([label, val]) => {
            const labels = [...document.querySelectorAll('label')];
            const found = labels.find(l => l.textContent.replace(/\\s+/g,' ').trim().includes(label));
            if (!found) return false;
            let el = found.htmlFor ? document.getElementById(found.htmlFor) : null;
            if (!el) {
                const c = found.closest('div')?.parentElement || found.parentElement;
                el = c?.querySelector('input, textarea, select');
            }
            if (!el) return false;
            const proto = el.tagName === 'TEXTAREA'
                ? window.HTMLTextAreaElement.prototype
                : window.HTMLInputElement.prototype;
            const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
            if (setter) setter.call(el, val); else el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }""",
        [partial_label, value or ""],
    )


def click_text(page, *texts: str) -> bool:
    for text in texts:
        loc = page.get_by_role("button", name=text)
        if loc.count() > 0:
            loc.first.click()
            return True
        loc2 = page.locator(f"button:has-text('{text}')")
        if loc2.count() > 0:
            loc2.first.click()
            return True
    return False


def import_one(page, scenario: dict) -> None:
    if not click_text(page, "추가"):
        raise RuntimeError("'추가' 버튼을 찾지 못했습니다.")
    page.wait_for_timeout(800)

    for label, key in FIELD_LABELS:
        fill_by_label(page, label, scenario.get(key, ""))
        page.wait_for_timeout(80)

    status = (scenario.get("status") or "DRAFT").upper()
    if status == "APPROVED":
        page.locator("text=검토완료").first.click()
    else:
        page.locator("text=임시").first.click()

    page.wait_for_timeout(200)
    click_text(page, "저장", "등록", "Save") or click_text(page, "확인")
    page.wait_for_timeout(1200)


def run_login() -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(URL)
        print("브라우저에서 DevCopilot에 로그인한 뒤, 이 터미널에서 Enter를 누르세요...")
        input()
        context.storage_state(path=str(STATE_PATH))
        print(f"세션 저장: {STATE_PATH}")
        browser.close()


def run_import(mvp_only: bool, start: int) -> None:
    from playwright.sync_api import sync_playwright

    if not STATE_PATH.exists():
        print("로그인 세션이 없습니다. 먼저 --login 을 실행하세요.", file=sys.stderr)
        sys.exit(1)

    scenarios = load_scenarios(mvp_only)[start:]
    print(f"입력 대상: {len(scenarios)}개 (start={start}, mvp_only={mvp_only})")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(storage_state=str(STATE_PATH))
        page = context.new_page()
        page.goto(URL)
        page.wait_for_timeout(2000)

        for i, scenario in enumerate(scenarios, start=start + 1):
            sid = scenario.get("scenarioId", "?")
            title = scenario.get("title", "")
            print(f"[{i}] {sid} - {title}")
            try:
                import_one(page, scenario)
            except Exception as e:
                print(f"  오류: {e}")
                print("  이 시나리오부터 수동으로 이어가거나 --start 옵션으로 재시도하세요.")
                break
            time.sleep(0.3)

        print("완료. 브라우저에서 결과를 확인하세요.")
        input("Enter를 누르면 브라우저를 닫습니다...")
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="로그인 후 세션 저장")
    parser.add_argument("--mvp-only", action="store_true", help="MVP 시나리오만 입력")
    parser.add_argument("--start", type=int, default=0, help="시작 인덱스 (0-based)")
    args = parser.parse_args()

    if args.login:
        run_login()
    else:
        run_import(args.mvp_only, args.start)


if __name__ == "__main__":
    main()
