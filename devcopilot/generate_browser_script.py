#!/usr/bin/env python3
"""scenarios_import.json → 브라우저 콘솔용 JS 파일 생성."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "scenarios_import.json"
OUT_PATH = ROOT / "import_in_browser.generated.js"
TEMPLATE_PATH = ROOT / "import_in_browser.js"


def main() -> None:
    scenarios = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    json_str = json.dumps(scenarios, ensure_ascii=False, indent=2)
    # null placeholder를 실제 JSON으로 교체
    generated = template.replace(
        "const SCENARIOS = /* JSON_DATA_START */ null; /* JSON_DATA_END - 아래 loadScenariosFromJson() 사용 권장 */",
        f"const SCENARIOS = {json_str};",
    )

    # loadScenariosFromJson 에러 throw 제거하고 바로 사용 가능하게
    generated += "\n\n// 자동 생성됨 — 바로 실행:\n// importAllScenarios()\n// importMvpOnly()\n"

    OUT_PATH.write_text(generated, encoding="utf-8")
    print(f"생성 완료: {OUT_PATH}")
    print(f"시나리오 {len(scenarios)}개 포함")


if __name__ == "__main__":
    main()
