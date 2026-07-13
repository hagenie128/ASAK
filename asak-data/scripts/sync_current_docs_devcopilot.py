#!/usr/bin/env python3
"""Upsert the current ASAK operating docs to DevCopilot workspace 2.

Uses only the Python standard library so it can run in the project environment.
Set DEVCOPILOT_TOKEN to a valid bearer token before executing it.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path


BASE = "https://devproject-hub-backend.onrender.com"
WS = 2
ROOT = Path(__file__).resolve().parents[2]
# These are the pages linked from the DevCopilot project navigation.  Updating
# by ID deliberately prevents duplicate wiki pages when a title changes.
TARGETS = {
    "현재 운영 기준": (23, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/00 현재 운영 기준.md"),
    "요구사항 정의": (9, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/02 요구사항 정의.md"),
    "사용자 시나리오": (10, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/03 사용자 시나리오.md"),
    "화면 설계 (Figma)": (5, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/04 화면 설계.md"),
    "DB 설계 (Modeler)": (11, ROOT / "05 DB 설계 1d951ef04f0b83019b4281f04c7b12cc.md"),
    "API 명세서": (12, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/06 API 명세.md"),
    "WBS & 칸반 보드": (13, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/07 WBS 개발 진행 현황.md"),
    "QA 테스트 & 버그": (14, ROOT / "docs/notion/ASAK 키오스크 프로젝트/키오스크 풀스택 프로젝트/09 테스트 오류 관리.md"),
}


def request(method: str, path: str, body: dict | None = None) -> object:
    token = os.getenv("DEVCOPILOT_TOKEN")
    if not token:
        raise RuntimeError("DEVCOPILOT_TOKEN is required")
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body else None
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=data,
        method=method,
        headers={
            "Content-Type": "application/json",
            "x-user-username": "hagenie128",
            "Authorization": f"Bearer {token}",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    wikis = {wiki["id"]: wiki for wiki in request("GET", f"/api/workspaces/{WS}/wikis")}
    for section, (wiki_id, file) in TARGETS.items():
        if wiki_id not in wikis:
            raise RuntimeError(f"Missing target wiki {wiki_id} for {section}; no page was created")
        body = {"title": wikis[wiki_id]["title"], "content": file.read_text(encoding="utf-8")}
        result = request("PUT", f"/api/workspaces/{WS}/wikis/{wiki_id}", body)
        print(f"updated: {result['id']} {section}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
