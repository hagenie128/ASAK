#!/usr/bin/env python3
"""kiosk_design Figma frame 이름을 SCR-XXX 이름 형식으로 맞추는 도구.

- FIGMA_TOKEN(또는 FIGMA_ACCESS_TOKEN)이 있으면: 파일 구조 조회 + figma-links.template.json node_id 동기화
- 실제 rename은 Figma REST API로 불가 → docs/design/figma-rename-scr-plugin.js 를 Figma에서 실행

Usage:
  set FIGMA_TOKEN=figd_...
  python asak-data/scripts/rename_figma_scr_frames.py --list
  python asak-data/scripts/rename_figma_scr_frames.py --sync-json
  python asak-data/scripts/rename_figma_scr_frames.py --print-plugin
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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
SCREENS_JSON = REPO_ROOT / "docs" / "screens" / "screens.json"
FIGMA_LINKS = REPO_ROOT / "docs" / "design" / "figma-links.template.json"
PLUGIN_JS = REPO_ROOT / "docs" / "design" / "figma-rename-scr-plugin" / "code.js"
FILE_KEY = "iqaoVwFjFE6Zq1WpOVgjeG"

# figma_refs copy 힌트 → SCR (기존 이름 추정용)
COPY_HINTS: dict[str, list[str]] = {
    "SCR-001": ["customer page", "시작", "home", "홈"],
    "SCR-002": ["주문유형", "order type", "먹고", "포장", "dine"],
    "SCR-003": ["메뉴", "menu", "grid", "category"],
    "SCR-004": ["옵션", "option", "상세", "custom"],
    "SCR-005": ["cart", "장바구니"],
    "SCR-006": ["order review", "주문 확인", "confirm"],
    "SCR-007": ["payment", "결제", "pay"],
    "SCR-008": ["success", "완료", "complete", "pickup"],
    "SCR-009": ["order list", "주문 관리", "admin order"],
    "SCR-010": ["order detail", "주문 상세"],
    "SCR-011": ["품절", "sold", "toggle"],
    "SCR-012": ["error", "실패", "retry", "재시도"],
    "SCR-013": ["timeout", "타임아웃", "idle", "초기화"],
    "SCR-014": ["a11y", "access", "접근성"],
    "SCR-015": ["admin login", "로그인", "login"],
    "SCR-016": ["menu table", "메뉴 관리", "menu manage"],
    "SCR-017": ["menu form", "메뉴 등록", "등록/수정"],
    "SCR-018": ["pay config", "결제수단"],
    "SCR-019": ["sales", "매출", "chart"],
    "SCR-020": ["영수증", "receipt"],
    "SCR-021": ["멤버십", "쿠폰", "포인트", "loyalty", "membership"],
}

CUSTOMER_PAGE = "03. Kiosk Screens"
ADMIN_PAGE = "04. Admin Screens"


def load_scr_targets() -> list[dict]:
    screens = json.loads(SCREENS_JSON.read_text(encoding="utf-8"))
    links = json.loads(FIGMA_LINKS.read_text(encoding="utf-8"))
    page_by_scr = {s["scr_id"]: s.get("figma_page", "") for s in links["screens"]}
    out = []
    for s in screens:
        sid = s["screen_id"]
        title = s["title"]
        short = title.replace(" 화면", "").strip()
        if sid == "SCR-020":
            short = "영수증 출력"
        out.append(
            {
                "scr_id": sid,
                "title": title,
                "new_name": f"{sid} {short}",
                "figma_page": page_by_scr.get(sid, CUSTOMER_PAGE),
            }
        )
    return out


def figma_token() -> str:
    return os.environ.get("FIGMA_TOKEN") or os.environ.get("FIGMA_ACCESS_TOKEN") or ""


def figma_get(path: str) -> dict:
    token = figma_token()
    if not token:
        raise RuntimeError("FIGMA_TOKEN 또는 FIGMA_ACCESS_TOKEN 환경 변수가 필요합니다.")
    req = urllib.request.Request(
        f"https://api.figma.com/v1{path}",
        headers={"X-Figma-Token": token},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"Figma API {e.code}: {body}") from e


def collect_frames(node: dict, page_name: str, out: list[dict]) -> None:
    if node.get("type") == "FRAME":
        out.append(
            {
                "id": node["id"],
                "name": node.get("name", ""),
                "page": page_name,
                "node_id_url": node["id"].replace(":", "-"),
            }
        )
    for child in node.get("children") or []:
        collect_frames(child, page_name, out)


def list_top_level_frames(file_json: dict) -> list[dict]:
    frames: list[dict] = []
    doc = file_json.get("document", {})
    for page in doc.get("children") or []:
        if page.get("type") != "CANVAS":
            continue
        page_name = page.get("name", "")
        for child in page.get("children") or []:
            if child.get("type") == "FRAME":
                frames.append(
                    {
                        "id": child["id"],
                        "name": child.get("name", ""),
                        "page": page_name,
                        "node_id_url": child["id"].replace(":", "-"),
                    }
                )
            elif child.get("type") in ("SECTION", "GROUP"):
                collect_frames(child, page_name, frames)
    return frames


def score_match(frame_name: str, scr_id: str) -> int:
    name_l = frame_name.lower()
    if scr_id.lower() in name_l:
        return 100
    if re.search(rf"\b{scr_id[-3:]}\b", name_l):
        return 40
    score = 0
    for hint in COPY_HINTS.get(scr_id, []):
        if hint.lower() in name_l:
            score += 10
    return score


def suggest_mapping(frames: list[dict], targets: list[dict]) -> list[dict]:
    rows = []
    used_frames: set[str] = set()

    for t in targets:
        sid = t["scr_id"]
        page = t["figma_page"]
        candidates = [f for f in frames if f["page"] == page and f["id"] not in used_frames]
        if not candidates:
            candidates = [f for f in frames if f["id"] not in used_frames]

        best = max(candidates, key=lambda f: score_match(f["name"], sid), default=None)
        if best and score_match(best["name"], sid) > 0:
            used_frames.add(best["id"])
            old_name = best["name"]
            node_id = best["node_id_url"]
        else:
            old_name = "(프레임 없음 — 생성 필요)"
            node_id = ""

        rows.append(
            {
                "scr_id": sid,
                "old_name": old_name,
                "new_name": t["new_name"],
                "page": page,
                "node_id": node_id,
                "figma_url": (
                    f"https://www.figma.com/design/{FILE_KEY}/kiosk_design?node-id={node_id}"
                    if node_id
                    else ""
                ),
            }
        )
    return rows


def sync_figma_links(mapping: list[dict]) -> int:
    data = json.loads(FIGMA_LINKS.read_text(encoding="utf-8"))
    by_scr = {m["scr_id"]: m for m in mapping}
    updated = 0
    for screen in data["screens"]:
        m = by_scr.get(screen["scr_id"])
        if not m or not m["node_id"]:
            continue
        if screen.get("node_id") != m["node_id"] or screen.get("figma_url") != m["figma_url"]:
            screen["node_id"] = m["node_id"]
            screen["figma_url"] = m["figma_url"]
            updated += 1
    FIGMA_LINKS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return updated


def print_mapping_table(mapping: list[dict]) -> None:
    print(f"{'SCR':<10} {'Page':<18} {'기존 이름':<36} → {'새 이름'}")
    print("-" * 100)
    for m in mapping:
        print(
            f"{m['scr_id']:<10} {m['page']:<18} {m['old_name']:<36} → {m['new_name']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="kiosk_design SCR frame rename helper")
    parser.add_argument("--list", action="store_true", help="현재 프레임 목록 + 매핑 제안 출력")
    parser.add_argument("--sync-json", action="store_true", help="figma-links.template.json node_id 동기화")
    parser.add_argument("--print-plugin", action="store_true", help="Figma plugin JS 경로 출력")
    args = parser.parse_args()

    targets = load_scr_targets()

    if args.print_plugin:
        print(PLUGIN_JS)
        return 0

    if not args.list and not args.sync_json:
        parser.print_help()
        return 1

    if not figma_token():
        print("FIGMA_TOKEN 없음 — 아래는 figma_refs copy 힌트 기반 추정 매핑입니다.\n", file=sys.stderr)
        mapping = [
            {
                "scr_id": t["scr_id"],
                "old_name": f"(추정: {COPY_HINTS.get(t['scr_id'], ['?'])[0]} …)",
                "new_name": t["new_name"],
                "page": t["figma_page"],
                "node_id": "",
                "figma_url": "",
            }
            for t in targets
        ]
        print_mapping_table(mapping)
        print("\n토큰 설정 후 재실행: python asak-data/scripts/rename_figma_scr_frames.py --list")
        print(f"이름 변경: Figma에서 {PLUGIN_JS.relative_to(REPO_ROOT)} 실행")
        return 2

    file_json = figma_get(f"/files/{FILE_KEY}?depth=2")
    frames = list_top_level_frames(file_json)
    mapping = suggest_mapping(frames, targets)

    if args.list:
        print(f"파일: {file_json.get('name')} · 프레임 {len(frames)}개\n")
        print_mapping_table(mapping)

    if args.sync_json:
        n = sync_figma_links(mapping)
        print(f"\nfigma-links.template.json 업데이트: {n}건")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
