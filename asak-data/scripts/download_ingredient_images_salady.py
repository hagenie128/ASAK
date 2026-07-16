"""Parse Salady topping/dressing pages → map names to image URLs → download + match ASAK ingredients."""

from __future__ import annotations

import json
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed" / "ingredient.json"
OUT_DIR = ROOT / "images" / "ingredient-salady"
MAP_PATH = ROOT / "images" / "ingredient-salady" / "mapping.json"
REPORT_PATH = ROOT / "images" / "ingredient-salady" / "match_report.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

PAGES = [
    ("topping", "https://salady.com/menu/list_2?type=topping"),
    ("dressing", "https://salady.com/menu/list_2?type=dressing"),
]

# Manual alias: ASAK seed name → Salady page name (when wording differs)
ALIASES = {
    "로스트 닭다리살": "로스트닭다리살",
    "그라브락스연어": "그라브락스 연어",
    "그라브락스 연어": "그라브락스 연어",
    "케이준쉬림프": "케이준 쉬림프",
    "케이준 쉬림프": "케이준 쉬림프",
    "잠봉슬라이스": "잠봉 슬라이스",
    "스크램블에그": "스크램블 에그",
    "화이트치즈": "화이트치즈소스",
    "화이트치즈소스": "화이트치즈소스",
    "당근라페": "당근라페",
    "양파플레이크": "양파플레이크",
    "슈레드치즈": "슈레드치즈",
    "크리미칠리": "크리미칠리",
    "(무료) 발사믹": "발사믹",
    "(무료) 렌치": "렌치",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read().decode("utf-8", "replace")


def prefer_full_image(url: str) -> str:
    """list page uses /topping/thumb/; larger file is usually /topping/ same filename."""
    return url.replace("/topping/thumb/", "/topping/")


def abs_url(u: str) -> str:
    u = unescape(u.strip())
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("/"):
        return "https://salady.com" + u
    return u.replace("https://salady.com:443", "https://salady.com")


def normalize_name(name: str) -> str:
    s = name.strip()
    s = re.sub(r"\s+", "", s)
    s = s.replace("VEGAN", "").replace("vegan", "")
    s = re.sub(r"^\(무료\)", "", s)
    s = s.lower()
    # hangul stays
    return s


def parse_items(html: str, kind: str) -> list[dict]:
    """Extract (korean_name, image_url) from Salady topping/dressing list HTML."""
    items: list[dict] = []
    # Official pattern: pop_view(..., '닭가슴살|kcal|...') then nearby thumb img
    for m in re.finditer(
        r"pop_view\(\s*'pop_\d+'\s*,\s*'open'\s*,\s*'([^|']+)\|[^']*'\s*\)[\s\S]{0,600}?"
        r"""src=["']([^"']*topping/thumb/[^"']+)["']""",
        html,
        re.I,
    ):
        name = unescape(m.group(1)).strip()
        name = re.sub(r"\s*VEGAN\s*", "", name, flags=re.I).strip()
        thumb = abs_url(m.group(2))
        full = prefer_full_image(thumb)
        if name:
            items.append(
                {
                    "name": name,
                    "image_url": full,
                    "thumb_url": thumb,
                    "kind": kind,
                }
            )

    seen: set[str] = set()
    out: list[dict] = []
    for it in items:
        key = normalize_name(it["name"])
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def download(url: str, dest: Path, fallback: str | None = None) -> bool:
    if dest.exists() and dest.stat().st_size > 5000:
        return True
    last: Exception | None = None
    # replace tiny leftover thumbs
    for candidate in (url, fallback):
        if not candidate:
            continue
        try:
            req = urllib.request.Request(candidate, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read()
            if len(data) < 500:
                continue
            dest.write_bytes(data)
            return True
        except Exception as exc:
            last = exc
            continue
    print(f"  FAIL {dest.name}: {last}")
    return False


def best_match(ing_name: str, salady_by_norm: dict[str, dict]) -> dict | None:
    aliases = ALIASES.get(ing_name, ing_name)
    for candidate in (ing_name, aliases):
        key = normalize_name(candidate)
        if key in salady_by_norm:
            return salady_by_norm[key]
    # fuzzy contains
    key = normalize_name(ing_name)
    for sk, item in salady_by_norm.items():
        if key and (key in sk or sk in key):
            return item
    return None


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    salady_items: list[dict] = []
    for kind, url in PAGES:
        print(f"fetch {url}")
        html = fetch(url)
        parsed = parse_items(html, kind)
        print(f"  parsed {len(parsed)}")
        for p in parsed:
            print(f"   - {p['name']}")
        salady_items.extend(parsed)

    # download all salady topping images with slug name
    for it in salady_items:
        safe = re.sub(r"[^\w가-힣]+", "-", it["name"]).strip("-")[:40]
        ext = Path(it["image_url"].split("?")[0]).suffix or ".jpg"
        fname = f"{it['kind']}_{safe}{ext}"
        dest = OUT_DIR / fname
        # force refresh if previous run saved 60x60 thumbs
        if dest.exists() and dest.stat().st_size < 5000:
            dest.unlink()
        ok = download(it["image_url"], dest, fallback=it.get("thumb_url"))
        it["local_file"] = fname if ok else None
        time.sleep(0.12)

    salady_by_norm = {normalize_name(it["name"]): it for it in salady_items}

    ingredients = json.loads(SEED.read_text(encoding="utf-8"))
    matched = []
    unmatched = []
    for ing in ingredients:
        hit = best_match(ing["name"], salady_by_norm)
        row = {
            "ingredient_id": ing["id"],
            "ingredient_name": ing["name"],
            "type_id": ing["type_id"],
        }
        if hit:
            row.update(
                {
                    "salady_name": hit["name"],
                    "salady_kind": hit["kind"],
                    "image_url": hit["image_url"],
                    "local_file": hit.get("local_file"),
                }
            )
            matched.append(row)
        else:
            unmatched.append(row)

    mapping = {
        "source": "https://salady.com/menu/list_2?type=topping|dressing",
        "note": "학습/참고용. 상업 배포 전 권리 확인 필요.",
        "salady_items": salady_items,
        "matched": matched,
        "unmatched": unmatched,
    }
    MAP_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(
        json.dumps(
            {
                "salady_count": len(salady_items),
                "matched_count": len(matched),
                "unmatched_count": len(unmatched),
                "unmatched_names": [u["ingredient_name"] for u in unmatched],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"DONE salady={len(salady_items)} matched={len(matched)} "
        f"unmatched={len(unmatched)} out={OUT_DIR}"
    )


if __name__ == "__main__":
    main()
