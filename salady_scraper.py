#!/usr/bin/env python3
"""Salady menu / nutrition / allergy data scraper."""

from __future__ import annotations

from html import unescape
import csv
import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse, parse_qs

import pdfplumber
import requests
from bs4 import BeautifulSoup

from image_ocr import ImageOcrParser

BASE_URL = "https://salady.com"
REQUEST_DELAY = 1.0
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}

MAIN_LIST_URLS = [
    f"{BASE_URL}/menu/list_1",
    f"{BASE_URL}/menu2/list_1?menu2=1",
]

POPUP_LIST_CONFIGS = [
    (f"{BASE_URL}/menu/list_2?type=topping", "salady", "토핑&드레싱", "topping"),
    (f"{BASE_URL}/menu/list_3?type=side", "salady", "음료&사이드", "side"),
    (f"{BASE_URL}/menu2/list_2?menu2=1&type=topping", "salady_sandwich", "토핑&드레싱", "topping"),
    (f"{BASE_URL}/menu2/list_3?menu2=1&type=side", "salady_sandwich", "음료&사이드", "side"),
]

CA_ID_NAV_CATEGORY = {
    "01": "샐러디",
    "02": "그레인볼",
    "03": "누들볼",
    "04": "프로틴 박스",
    "0404": "프로틴 박스",
    "05": "랩&샌드위치",
    "07": "나만의 샐러디",
}

MENU2_CA_ID_NAV_CATEGORY = {
    "01": "샌드위치",
    "02": "샐러디",
    "03": "데일리볼",
    "04": "프로틴박스",
    "05": "랩",
    "06": "나만의 샐러디",
}

POPUP_NUTRITION_KEYS = [
    "menu",
    "calories_kcal",
    "carbs_g",
    "sugar_g",
    "protein_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
]

CALORIE_AJAX_URL = f"{BASE_URL}/_subpage/kor/menu/ajax.menupop2.php"
NUTRITION_PDF_URL = f"{BASE_URL}/pdf/nutrition.pdf?ver=3"
ALLERGY_PDF_URL = f"{BASE_URL}/pdf/allergy.pdf?ver=3"

APP_PAGES = {
    "membership": f"{BASE_URL}/app/membership",
    "order": f"{BASE_URL}/app/order",
    "giftcard": f"{BASE_URL}/app/giftcard",
}

EVENT_LIST_URL = f"{BASE_URL}/kor/news/event?ca=&sel_search=&txt_search=&page={{page}}"

ADDON_PDF_CATEGORIES = {"BASE", "PROTEIN", "VEGGIES", "CRISPY", "DRESSING", "DRINK", "SIDE"}

NAVER_GRAPHQL_URL = "https://m.booking.naver.com/graphql"
NAVER_MENU_PROJECTIONS = (
    "RequiredSubOptionPrice,ReviewScoreAvg,Category,HasSubOption,BookingCount"
)
DEFAULT_SET_SIDES = ["카사바칩", "코크제로"]

STORE_MENU_SOURCES = [
    {
        "id": "passorder_sinchon",
        "platform": "passorder",
        "store_name": "샐러디 신촌역점",
        "url": "https://app.passorder.co.kr/normal/076449d4-c874-4edc-b5fc-11917c0c9664/menus",
    },
    {
        "id": "naver_mapo",
        "platform": "naver_order",
        "store_name": "샐러디 마포역점",
        "business_id": "425424",
        "biz_item_id": "3629791",
        "url": "https://m.booking.naver.com/order/bizes/425424/items/3629791",
    },
]

STORE_CATEGORY_MAP = {
    "샌드위치": "샌드위치",
    "샐러디": "샐러디",
    "누들볼": "누들볼",
    "그레인볼": "그레인볼",
    "프로틴 박스": "프로틴 박스",
    "랩": "랩",
    "곡물랩": "랩",
    "마이 샐러디": "나만의 샐러디",
    "사이드": "음료&사이드",
    "음료": "음료&사이드",
    "올데이 세트": "세트",
}

NUTRITION_COLUMNS = [
    "menu",
    "calories_kcal",
    "carbs_g",
    "sugar_g",
    "protein_g",
    "fat_g",
    "saturated_fat_g",
    "sodium_mg",
]


@dataclass
class MenuItem:
    id: str
    name_ko: str
    name_en: str = ""
    category: str = ""
    nav_category: str = ""
    menu_type: str = "main"
    brand: str = "salady"
    url: str = ""
    description: str = ""
    image_url: str = ""
    tags: list[str] = field(default_factory=list)
    base: str = ""
    toppings_text: str = ""
    default_dressing: str = ""
    vegetables: list[dict[str, str]] = field(default_factory=list)
    nutrition: dict[str, Any] = field(default_factory=dict)
    calorie_calculator: dict[str, Any] = field(default_factory=dict)
    allergy: list[str] = field(default_factory=list)


def _nav_category_for(brand: str, ca_id: str, fallback: str = "") -> str:
    mapping = MENU2_CA_ID_NAV_CATEGORY if brand == "salady_sandwich" else CA_ID_NAV_CATEGORY
    return mapping.get(ca_id, fallback)


def _normalize_menu_name(name: str) -> str:
    return re.sub(r"\s+", "", (name or "").strip().lower())


def _normalize_store_menu_name(name: str) -> str:
    text = re.sub(r"\[[^\]]+\]", "", name or "")
    text = re.sub(r"[♥♡]", "", text)
    text = re.sub(r"\s*세트\s*$", "", text.strip())
    return re.sub(r"\s+", "", text.lower())


NAV_RECOMMENDED_DRESSING = {
    "샐러디",
    "그레인볼",
    "누들볼",
    "나만의 샐러디",
    "프로틴 박스",
    "프로틴박스",
}
NAV_INCLUDED_DRESSING = {
    "샌드위치",
    "랩",
    "랩&샌드위치",
    "데일리볼",
}

DRESSING_FROM_TEXT_RE = re.compile(
    r"(추천\s*드레싱|포함\s*드레싱|추천드레싱|포함드레싱)\s*[:：]\s*([^/)]+)",
    re.IGNORECASE,
)


def _clean_dressing_raw(name: str) -> str:
    if not name:
        return ""
    text = name.strip()
    text = re.sub(r"\s*\([^)]*미제공[^)]*\)", "", text)
    text = re.sub(r"\s*\([^)]*별도[^)]*\)", "", text)
    return text.strip(" /)")


def _normalize_dressing_key(name: str) -> str:
    return re.sub(r"\s+", "", (name or "").lower())


def _canonical_dressing_spaces(name: str) -> str:
    text = name.strip()
    text = re.sub(r"\(\s*저당\s*\)", "(저당)", text)
    match = re.match(r"^\(저당\)\s*(.+)$", text)
    if match:
        return f"(저당) {match.group(1).strip()}"
    return text


def extract_dressing_from_text(text: str) -> tuple[str, str]:
    """설명 텍스트에서 (유형, 드레싱명) 추출. 유형은 recommended 또는 included."""
    if not text:
        return "", ""
    for label, raw_name in DRESSING_FROM_TEXT_RE.findall(text):
        label_compact = re.sub(r"\s+", "", label)
        dressing_type = "recommended" if "추천" in label_compact else "included"
        cleaned = _clean_dressing_raw(raw_name)
        if cleaned:
            return dressing_type, cleaned
    return "", ""


def resolve_dressing_type(nav_category: str, explicit_type: str = "") -> str:
    if explicit_type:
        return explicit_type
    if nav_category in NAV_RECOMMENDED_DRESSING:
        return "recommended"
    if nav_category in NAV_INCLUDED_DRESSING:
        return "included"
    return ""


def canonicalize_dressing_name(
    name: str,
    name_map: dict[str, str] | None = None,
) -> str:
    if not name:
        return ""
    cleaned = _canonical_dressing_spaces(_clean_dressing_raw(name))
    key = _normalize_dressing_key(cleaned)
    if name_map and key in name_map:
        return name_map[key]
    return cleaned


def build_dressings_catalog(
    extra_toppings: dict[str, list[dict[str, Any]]] | None = None,
    calorie_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    seen: set[str] = set()
    items: list[dict[str, Any]] = []

    def add(
        name: str,
        nutrition: dict[str, Any] | None = None,
        kcal: float | None = None,
    ) -> None:
        if not name:
            return
        canon = canonicalize_dressing_name(name)
        key = _normalize_dressing_key(canon)
        if key in seen:
            return
        seen.add(key)
        entry: dict[str, Any] = {"name": canon, "name_normalized": key}
        if nutrition:
            entry["nutrition_pdf"] = nutrition
        if kcal is not None:
            entry["kcal"] = kcal
        items.append(entry)

    if extra_toppings:
        for row in extra_toppings.get("Dressing", []):
            add(row.get("menu", ""), nutrition=row)

    if calorie_data:
        for row in calorie_data.get("topping_categories", {}).get("드레싱 선택", []):
            add(
                row.get("name", ""),
                nutrition=row.get("nutrition_pdf"),
                kcal=row.get("kcal"),
            )

    items.sort(key=lambda item: item["name"])
    return {
        "count": len(items),
        "name_map": {item["name_normalized"]: item["name"] for item in items},
        "items": items,
    }


def enrich_menu_dressings(
    menus: list[dict[str, Any]],
    dressings_catalog: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    name_map = (dressings_catalog or {}).get("name_map", {})

    for menu in menus:
        store_sources: dict[str, str] = {}
        store_types: list[str] = []
        store_names: list[str] = []

        for store_key, pricing in (menu.get("store_pricing") or {}).items():
            if "__set__" in store_key:
                continue
            desc = pricing.get("description", "")
            dressing_type, dressing_name = extract_dressing_from_text(desc)
            if not dressing_name:
                continue
            store_id = store_key.split("__", 1)[0]
            canon = canonicalize_dressing_name(dressing_name, name_map)
            store_sources[store_id] = canon
            store_types.append(dressing_type)
            store_names.append(canon)

        desc_type, desc_name = extract_dressing_from_text(menu.get("description", ""))
        official_raw = _clean_dressing_raw(menu.get("default_dressing", ""))
        official_name = (
            canonicalize_dressing_name(official_raw, name_map) if official_raw else ""
        )
        nav_category = menu.get("nav_category", "")

        dressing_type = ""
        dressing_name = ""

        if store_names:
            dressing_type = store_types[0] or resolve_dressing_type(nav_category)
            dressing_name = store_names[0]
            if len(set(store_names)) == 1:
                dressing_name = store_names[0]
            elif official_name:
                dressing_name = official_name
        elif desc_name:
            dressing_type = desc_type or resolve_dressing_type(nav_category)
            dressing_name = canonicalize_dressing_name(desc_name, name_map)
        elif official_name:
            dressing_type = resolve_dressing_type(nav_category)
            dressing_name = official_name

        if dressing_name and not dressing_type:
            dressing_type = resolve_dressing_type(nav_category)

        menu["dressing_type"] = dressing_type
        menu["recommended_dressing"] = (
            dressing_name if dressing_type == "recommended" else ""
        )
        menu["included_dressing"] = (
            dressing_name if dressing_type == "included" else ""
        )

        if dressing_name:
            dressing_info: dict[str, Any] = {
                "name": dressing_name,
                "type": dressing_type,
            }
            if official_name:
                dressing_info["official"] = official_name
            if store_sources:
                dressing_info["store_sources"] = store_sources
            menu["dressing"] = dressing_info
        else:
            menu.pop("dressing", None)

    return menus


def write_menus_csv(menus: list[dict[str, Any]], output_dir: Path) -> None:
    if not menus:
        return
    keys = sorted({key for item in menus for key in item.keys()})
    with (output_dir / "menus.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for item in menus:
            flat = {
                k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                for k, v in item.items()
            }
            writer.writerow(flat)


def _parse_price_krw(price_text: str) -> int | None:
    if not price_text:
        return None
    digits = re.sub(r"[^\d]", "", price_text)
    return int(digits) if digits else None


def _parse_set_info(name: str, description: str) -> dict[str, Any]:
    desc = (description or "").replace("\r\n", "\n").replace("더보기", "").strip()
    is_set = bool(re.search(r"세트", name or "")) or (
        "카사바칩" in desc and "코크제로" in desc
    )
    base_name = re.sub(r"\s*세트\s*$", "", (name or "").strip())
    set_components: list[str] = []
    first_line = desc.split("\n")[0] if desc else ""
    if "+" in first_line:
        tail = first_line
        if is_set and "+" in first_line:
            tail = first_line.split("+", 1)[1] if "+" in first_line else first_line
        for side in DEFAULT_SET_SIDES:
            if side in tail or side in first_line:
                set_components.append(side)
    elif is_set:
        set_components = DEFAULT_SET_SIDES.copy()
    return {
        "is_set": is_set,
        "base_menu_name": base_name,
        "set_components": set_components,
    }


def _extract_js_object(html: str, marker: str) -> dict[str, Any]:
    idx = html.find(marker)
    if idx < 0:
        return {}
    start = html.find("{", idx)
    if start < 0:
        return {}
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(html)):
        ch = html[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[start : i + 1])
    return {}


def _clean_event_title(text: str) -> str:
    title = unescape(re.sub(r"\s+", " ", (text or "").strip()))
    return title


def _parse_event_period(text: str) -> dict[str, str]:
    raw = re.sub(r"\s+", " ", (text or "").strip())
    match = re.search(r"(\d{4}/\d{2}/\d{2})\s*~\s*(\d{4}/\d{2}/\d{2})", raw)
    if not match:
        return {"raw": raw, "start": "", "end": ""}
    return {"raw": raw, "start": match.group(1), "end": match.group(2)}


def _event_page_url(page: int) -> str:
    return EVENT_LIST_URL.format(page=page)


def _normalize_pdf_category(category: str) -> str:
    return re.sub(r"\s+", " ", (category or "")).strip().upper()

    return re.sub(r"\s+", " ", (category or "")).strip().upper()


class SaladyScraper:
    def __init__(self, output_dir: Path, delay: float = REQUEST_DELAY, download_images: bool = False):
        self.output_dir = output_dir
        self.delay = delay
        self.download_images = download_images
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.images_dir = output_dir / "images"
        self.pdf_dir = output_dir / "pdf"
        self.ocr_dir = output_dir / "ocr"
        self.image_ocr = ImageOcrParser(cache_dir=self.ocr_dir)

    def _fetch_image_bytes(self, url: str) -> bytes:
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        return response.content

    def _enrich_group_order_ocr(self, group_order: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(group_order)
        enriched["set_menus"] = self.image_ocr.enrich_set_menus(
            group_order.get("set_menus", []),
            self._fetch_image_bytes,
        )
        return enriched

    def _enrich_membership_ocr(self, app_services: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(app_services)
        if "membership" in enriched:
            enriched["membership"] = self.image_ocr.enrich_membership(
                enriched["membership"],
                self._fetch_image_bytes,
            )
        return enriched

    def _get(self, url: str) -> requests.Response:
        time.sleep(self.delay)
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response

    def _download_file(self, url: str, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            return dest
        time.sleep(self.delay)
        response = self.session.get(url, timeout=120)
        response.raise_for_status()
        dest.write_bytes(response.content)
        return dest

    def _parse_popup_nutrition(self, href: str) -> dict[str, Any]:
        match = re.search(r"open',\s*'([^']+)'", href or "")
        if not match:
            return {}
        parts = [p.strip() for p in match.group(1).split("|")]
        if len(parts) < 2:
            return {}
        row: dict[str, Any] = {}
        for key, value in zip(POPUP_NUTRITION_KEYS, parts):
            if key == "menu":
                row[key] = value
            else:
                row[key] = self._parse_numeric(value)
        return row

    def collect_popup_items(self) -> list[MenuItem]:
        items: dict[str, MenuItem] = {}

        for list_url, brand, nav_category, menu_type in POPUP_LIST_CONFIGS:
            soup = BeautifulSoup(self._get(list_url).text, "lxml")

            for li in soup.select(".menu_list li"):
                anchor = li.select_one("a.pop_click, a[href*='pop_view']")
                if not anchor:
                    continue

                strong = li.select_one("strong")
                en_el = li.select_one("p")
                name_ko = strong.get_text(" ", strip=True) if strong else ""
                if not name_ko:
                    continue

                tags: list[str] = []
                if re.search(r"VEGAN", name_ko, re.I):
                    tags.append("VEGAN")
                    name_ko = re.sub(r"VEGAN", "", name_ko, flags=re.I).strip()

                name_en = en_el.get_text(" ", strip=True) if en_el else ""
                popup_nutrition = self._parse_popup_nutrition(anchor.get("href", ""))
                if popup_nutrition.get("menu"):
                    name_ko = popup_nutrition["menu"]

                image_url = ""
                img_el = li.select_one(".img img, img")
                if img_el and img_el.get("src"):
                    image_url = urljoin(BASE_URL, img_el["src"])

                item_id = f"{brand}_{menu_type}_{_normalize_menu_name(name_ko)}"
                if item_id in items:
                    continue

                items[item_id] = MenuItem(
                    id=item_id,
                    name_ko=name_ko,
                    name_en=name_en,
                    category=nav_category,
                    nav_category=nav_category,
                    menu_type=menu_type,
                    brand=brand,
                    url=list_url,
                    image_url=image_url,
                    tags=tags,
                    nutrition=popup_nutrition,
                )

        return list(items.values())

    def collect_menu_links(self) -> list[dict[str, str]]:
        links: dict[str, dict[str, str]] = {}

        for list_url in MAIN_LIST_URLS:
            soup = BeautifulSoup(self._get(list_url).text, "lxml")
            brand = "salady_sandwich" if "/menu2/" in list_url else "salady"

            for li in soup.select(".menu_list li"):
                anchor = li.select_one('a[href*="view_1"]')
                if not anchor:
                    continue

                href = anchor.get("href", "")
                if "idx=" not in href:
                    continue

                full_url = urljoin(BASE_URL, href)
                parsed = urlparse(full_url)
                params = parse_qs(parsed.query)
                idx = params.get("idx", [""])[0]
                if not idx:
                    continue

                name_ko = ""
                name_en = ""
                h6 = li.select_one("h6")
                en_el = li.select_one("p")
                if h6:
                    name_ko = h6.get_text(" ", strip=True)
                if en_el:
                    name_en = re.sub(
                        r"\s*(NEW|BEST|LOW\s*SUGAR|VEGAN)+\s*",
                        " ",
                        en_el.get_text(" ", strip=True),
                        flags=re.I,
                    ).strip()

                category = ""
                heading = li.find_previous(["h4", "h5"])
                if heading:
                    category = heading.get_text(strip=True)

                ca_id = params.get("ca_id", [""])[0]
                key = f"{brand}:{idx}"
                if key in links:
                    continue

                nav_category = _nav_category_for(brand, ca_id, category)

                links[key] = {
                    "id": idx,
                    "url": full_url,
                    "name_ko": name_ko,
                    "name_en": name_en,
                    "category": category,
                    "nav_category": nav_category,
                    "menu_type": "main",
                    "brand": brand,
                    "ca_id": ca_id,
                    "list_source": list_url,
                }

        return list(links.values())

    def parse_menu_detail(self, link: dict[str, str]) -> MenuItem:
        soup = BeautifulSoup(self._get(link["url"]).text, "lxml")

        title_el = soup.select_one(".view_top h3, .view_tit h3, h3.conTit")
        name_ko = title_el.get_text(strip=True) if title_el else link.get("name_ko", "")

        name_en = link.get("name_en", "")
        if not name_en:
            sub_el = soup.select_one(".view_top p, .view_top .en")
            if sub_el:
                name_en = sub_el.get_text(strip=True)

        desc_el = soup.select_one(".view_top .txt, .view_top > p")
        description = desc_el.get_text(" ", strip=True) if desc_el else ""

        image_url = ""
        img_el = soup.select_one(".left_img img, .view_cont .left_img img")
        if img_el and img_el.get("src"):
            image_url = urljoin(BASE_URL, img_el["src"])

        tags = [span.get_text(strip=True) for span in soup.select(".tag_box span") if span.get_text(strip=True)]

        base = toppings_text = default_dressing = ""
        for block in soup.select(".right_txt .text, .view_cont .right_txt .text"):
            label = block.select_one("strong")
            value = block.select_one("p")
            if not label or not value:
                continue
            label_text = label.get_text(strip=True)
            value_text = value.get_text(" ", strip=True)
            if "베이스" in label_text:
                base = value_text
            elif "토핑" in label_text:
                toppings_text = value_text
            elif "드레싱" in label_text:
                default_dressing = value_text

        vegetables: list[dict[str, str]] = []
        for li in soup.select(".info_box ul li"):
            name_el = li.select_one("p")
            img = li.select_one("img")
            if not name_el:
                continue
            veg: dict[str, str] = {"name": name_el.get_text(strip=True)}
            if img and img.get("src"):
                veg["image_url"] = urljoin(BASE_URL, img["src"])
            vegetables.append(veg)

        nutrition: dict[str, Any] = {}
        table = soup.select_one(".ing_table table, .ingredient table")
        if table:
            rows = table.select("tr")
            if len(rows) >= 2:
                headers = [th.get_text(strip=True) for th in rows[0].select("th")]
                values = [td.get_text(strip=True) for td in rows[1].select("td")]
                if headers and values:
                    nutrition = dict(zip(headers, values))

        category = link.get("category", "")
        if not category:
            for anchor in soup.select(".location a, .path a, .breadcrumb a"):
                text = anchor.get_text(strip=True)
                if text and text not in ("홈", "메뉴", "메뉴 소개", "HOME"):
                    category = text
                    break

        nav_category = link.get("nav_category", "")
        if not nav_category:
            ca_id = parse_qs(urlparse(link["url"]).query).get("ca_id", [""])[0]
            nav_category = _nav_category_for(link.get("brand", "salady"), ca_id, category)

        return MenuItem(
            id=link["id"],
            name_ko=name_ko or link.get("name_ko", ""),
            name_en=name_en,
            category=category,
            nav_category=nav_category,
            menu_type=link.get("menu_type", "main"),
            brand=link.get("brand", "salady"),
            url=link["url"],
            description=description,
            image_url=image_url,
            tags=tags,
            base=base,
            toppings_text=toppings_text,
            default_dressing=default_dressing,
            vegetables=vegetables,
            nutrition=nutrition,
        )

    def parse_calorie_calculator(self) -> dict[str, Any]:
        soup = BeautifulSoup(self._get(CALORIE_AJAX_URL).text, "lxml")

        note_el = soup.select_one(".kalCon .top span")
        note = note_el.get_text(" ", strip=True) if note_el else ""

        base_addons: dict[str, float] = {}
        for label in soup.select(".checkbox label"):
            input_el = label.select_one("input")
            if not input_el:
                continue
            name = input_el.get("name", "")
            text = label.get_text(strip=True)
            base_addons[name] = {"label": text}

        menus: list[dict[str, Any]] = []
        menu_select = soup.select_one("#menuData")
        if menu_select:
            for option in menu_select.select("option"):
                name = option.get_text(strip=True)
                value = option.get("value", "")
                if not name or not value:
                    continue
                menus.append(
                    {
                        "name": name,
                        "base_kcal": float(value),
                        "addon_kcal": {
                            "vegetable": float(option.get("data-vegetable", 0) or 0),
                            "grain": float(option.get("data-grain", 0) or 0),
                            "buckwheat": float(option.get("data-buckwheat", 0) or 0),
                            "noodles": float(option.get("data-noodles", 0) or 0),
                        },
                    }
                )

        topping_categories: dict[str, list[dict[str, Any]]] = {}
        for li in soup.select(".addTopping li"):
            title_el = li.select_one(".tit")
            select_el = li.select_one("select")
            if not title_el or not select_el:
                continue
            category = title_el.get_text(strip=True)
            if category == "메뉴 선택":
                continue
            items: list[dict[str, Any]] = []
            for option in select_el.select("option"):
                name = option.get_text(strip=True)
                value = option.get("value", "")
                if not name or not value:
                    continue
                items.append({"name": name, "kcal": float(value)})
            topping_categories[category] = items

        return {
            "note": note,
            "menus": menus,
            "topping_categories": topping_categories,
        }

    def _normalize_header(self, text: str) -> str:
        text = re.sub(r"\s+", "", (text or "").replace("\n", ""))
        mapping = {
            "구분": "category",
            "메뉴": "menu",
            "메뉴명": "menu",
            "내용량(g)": "weight_g",
            "중량(g)": "weight_g",
            "제공량(g)": "weight_g",
            "내용량": "weight_g",
            "열량(kcal)": "calories_kcal",
            "열량(Kcal)": "calories_kcal",
            "열량": "calories_kcal",
            "탄수화물(g)": "carbs_g",
            "탄수화물": "carbs_g",
            "당류(g)": "sugar_g",
            "당류": "sugar_g",
            "단백질(g)": "protein_g",
            "단백질": "protein_g",
            "지방(g)": "fat_g",
            "지방": "fat_g",
            "포화지방(g)": "saturated_fat_g",
            "포화지방": "saturated_fat_g",
            "나트륨(mg)": "sodium_mg",
            "나트륨": "sodium_mg",
        }
        return mapping.get(text, text)

    def _parse_numeric(self, value: str) -> str | float:
        value = (value or "").strip().replace(",", "")
        if not value or value in ("-", "–"):
            return ""
        try:
            return float(value)
        except ValueError:
            return value

    def _is_nutrition_header(self, cells: list[str]) -> bool:
        joined = "".join(cells).lower()
        return "메뉴" in joined and ("kcal" in joined or "열량" in joined)

    def parse_pdf_tables(self, pdf_path: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        column_keys: list[str] | None = None
        current_category = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables() or []:
                    if not table:
                        continue
                    for raw_row in table:
                        cells = [(cell or "").strip() for cell in raw_row]
                        if not any(cells):
                            continue

                        if self._is_nutrition_header(cells):
                            column_keys = [self._normalize_header(c) for c in cells]
                            current_category = ""
                            continue

                        if not column_keys:
                            continue

                        row_map = {
                            key: cell
                            for key, cell in zip(column_keys, cells)
                            if key not in ("", None)
                        }
                        menu_name = row_map.get("menu", "")
                        if not menu_name:
                            continue

                        category = row_map.get("category") or current_category
                        if row_map.get("category"):
                            current_category = row_map["category"]

                        row: dict[str, Any] = {
                            "category": category,
                            "menu": menu_name,
                        }
                        for key, cell in row_map.items():
                            if key in ("category", "menu"):
                                continue
                            row[key] = self._parse_numeric(cell)
                        rows.append(row)

        return rows

    def _is_allergy_marker(self, value: str) -> bool:
        value = (value or "").strip()
        return value in ("●", "•", "◯", "○", "O", "o", "◎", "■")

    def parse_allergy_pdf(self, pdf_path: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        allergen_names: list[str] = []
        current_category = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables() or []:
                    if not table:
                        continue

                    for raw_row in table:
                        cells = [(cell or "").strip().replace("\n", " ") for cell in raw_row]
                        if not any(cells):
                            continue

                        if "메뉴" in cells[0] and "표시대상" in "".join(cells):
                            allergen_names = []
                            continue

                        if not allergen_names and cells[0] == "" and any(
                            name in "".join(cells) for name in ("달걀", "우유", "메밀", "땅콩", "대두")
                        ):
                            allergen_names = [c for c in cells[2:] if c]
                            continue

                        if not allergen_names:
                            continue

                        category = cells[0] or current_category
                        menu_name = cells[1] if len(cells) > 1 else ""
                        if cells[0]:
                            current_category = cells[0]
                        if not menu_name:
                            continue

                        markers = [
                            allergen
                            for allergen, value in zip(allergen_names, cells[2:])
                            if self._is_allergy_marker(value)
                        ]
                        rows.append(
                            {
                                "category": category,
                                "menu": menu_name,
                                "allergens": markers,
                            }
                        )

        return rows

    def extract_addon_toppings(self, nutrition_pdf_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """영양 PDF에서 커스터마이징용 추가 토핑/베이스/드레싱 추출."""
        groups: dict[str, list[dict[str, Any]]] = {}

        for row in nutrition_pdf_rows:
            menu = row.get("menu", "")
            if not menu or str(menu).startswith("*"):
                continue

            cat = _normalize_pdf_category(row.get("category", ""))
            if cat in ADDON_PDF_CATEGORIES:
                cat_key = cat.title() if cat == cat.upper() else cat
            elif "SAUCE" in cat or "MOUSSE" in cat:
                cat_key = "Sauce & Mousse"
            else:
                continue

            item = {k: v for k, v in row.items() if k != "category"}
            groups.setdefault(cat_key, []).append(item)

        return groups

    def enrich_calorie_toppings(
        self,
        calorie_data: dict[str, Any],
        nutrition_pdf_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """칼로리 계산기 토핑에 PDF 영양성분 병합."""
        pdf_by_name = {
            _normalize_menu_name(r.get("menu", "")): r
            for r in nutrition_pdf_rows
            if r.get("menu") and not str(r.get("menu")).startswith("*")
        }

        enriched = json.loads(json.dumps(calorie_data, ensure_ascii=False))
        for category, items in enriched.get("topping_categories", {}).items():
            for item in items:
                pdf_row = pdf_by_name.get(_normalize_menu_name(item.get("name", "")))
                if pdf_row:
                    item["nutrition_pdf"] = pdf_row
        return enriched

    def scrape_group_order(self) -> dict[str, Any]:
        soup = BeautifulSoup(self._get(f"{BASE_URL}/group/group").text, "lxml")

        set_menus: list[dict[str, Any]] = []
        for li in soup.select(".group-wrap .group_1 li"):
            title_el = li.select_one(".tit")
            if not title_el:
                continue
            images = {
                "pc": "",
                "mobile": "",
                "all": [],
            }
            for img in li.select("img"):
                src = urljoin(BASE_URL, img.get("src", ""))
                images["all"].append(src)
                classes = " ".join(img.get("class", []))
                if "__mo" in classes:
                    images["mobile"] = src
                else:
                    images["pc"] = src
            set_menus.append(
                {
                    "title": title_el.get_text(strip=True),
                    "images": images,
                }
            )

        how_to_order: list[dict[str, str]] = []
        for li in soup.select(".group_2 ol li"):
            step = li.select_one(".num")
            title = li.select_one("strong")
            desc = li.select_one("p")
            how_to_order.append(
                {
                    "step": step.get_text(strip=True) if step else "",
                    "title": title.get_text(strip=True) if title else "",
                    "description": desc.get_text(" ", strip=True) if desc else "",
                }
            )

        faq: list[dict[str, str]] = []
        for li in soup.select(".qna_list li"):
            question = li.select_one(".question_box p")
            answer = li.select_one(".answer_box")
            if not question:
                continue
            faq.append(
                {
                    "question": question.get_text(strip=True),
                    "answer": answer.get_text("\n", strip=True) if answer else "",
                }
            )

        form_soup = BeautifulSoup(self._get(f"{BASE_URL}/group/group_order").text, "lxml")
        representative_menus = [
            {
                "name": opt.get_text(strip=True),
                "value": opt.get("value", ""),
            }
            for opt in form_soup.select("#mySelect option")
            if opt.get("value")
        ]

        order_types = [
            opt.get_text(strip=True)
            for opt in form_soup.select("#wm_type option, select[name='wm_type'] option")
            if opt.get("value")
        ]

        return {
            "url": f"{BASE_URL}/group/group",
            "order_form_url": f"{BASE_URL}/group/group_order",
            "set_menus": set_menus,
            "representative_menus": representative_menus,
            "order_types": order_types,
            "how_to_order": how_to_order,
            "faq": faq,
        }

    def scrape_group_order_with_ocr(self) -> dict[str, Any]:
        group_order = self.scrape_group_order()
        return self._enrich_group_order_ocr(group_order)

    def _parse_membership_notices(self, text: str) -> dict[str, list[str]]:
        sections: dict[str, list[str]] = {}
        current = "general"
        sections[current] = []

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current = line.strip("[]")
                sections.setdefault(current, [])
                continue
            if line.startswith("- "):
                sections.setdefault(current, []).append(line[2:].strip())
            elif line.startswith("* "):
                sections.setdefault(current, []).append(line[2:].strip())

        return sections

    def scrape_app_services(self) -> dict[str, Any]:
        services: dict[str, Any] = {}

        for key, url in APP_PAGES.items():
            soup = BeautifulSoup(self._get(url).text, "lxml")
            content = soup.select_one("#content") or soup
            title_el = content.select_one("h3.conTit, h3")
            images = [
                urljoin(BASE_URL, img.get("src", ""))
                for img in content.select("img")
                if img.get("src") and "/images/" in img.get("src", "")
            ]

            page_data: dict[str, Any] = {
                "url": url,
                "title": title_el.get_text(strip=True) if title_el else key,
                "images": images,
                "sections": [],
            }

            if key == "membership":
                text = content.get_text("\n", strip=True)
                stamp_desc = []
                for p in content.select("p"):
                    t = p.get_text(" ", strip=True)
                    if t and "스탬프" in t and len(t) < 120:
                        stamp_desc.append(t)
                page_data["stamp"] = {
                    "summary": stamp_desc,
                    "notices": self._parse_membership_notices(text),
                }
            elif key == "order":
                highlights = [
                    p.get_text(" ", strip=True)
                    for p in content.select("p, strong")
                    if p.get_text(strip=True)
                ]
                page_data["highlights"] = [h for h in highlights if len(h) > 5][:10]
            elif key == "giftcard":
                gift_types = []
                for strong in content.select("strong"):
                    t = strong.get_text(strip=True)
                    if "선물" in t or "자동" in t:
                        gift_types.append(t)
                steps = [
                    li.get_text(" ", strip=True)
                    for li in content.select("ol li, ul li")
                    if li.get_text(strip=True)
                ]
                page_data["gift_types"] = gift_types
                page_data["steps"] = steps

            services[key] = page_data

        app_popup = f"{BASE_URL}/inc/ajax.saladyApp.php"
        try:
            popup_html = self._get(app_popup).text
            services["app_download_popup"] = {
                "url": app_popup,
                "has_content": len(popup_html) > 100,
            }
        except requests.RequestException:
            services["app_download_popup"] = {"url": app_popup, "has_content": False}

        return services

    def scrape_app_services_with_ocr(self) -> dict[str, Any]:
        services = self.scrape_app_services()
        return self._enrich_membership_ocr(services)

    def _parse_event_list_item(self, li) -> dict[str, Any] | None:
        link = li.select_one("a.link[href*='idx=']")
        if not link:
            return None

        href = urljoin(BASE_URL, link.get("href", ""))
        query = parse_qs(urlparse(href).query)
        event_id = (query.get("idx") or [""])[0]
        if not event_id:
            return None

        if li.select_one(".ico_ing"):
            status = "ongoing"
        elif li.select_one(".ico_end"):
            status = "ended"
        else:
            status = "unknown"

        title_el = li.select_one(".sbj")
        title = _clean_event_title(title_el.get_text(" ", strip=True) if title_el else "")
        date_el = li.select_one(".date")
        period = _parse_event_period(date_el.get_text(" ", strip=True) if date_el else "")

        thumb_el = li.select_one(".tmb img")
        thumbnail_url = urljoin(BASE_URL, thumb_el.get("src", "")) if thumb_el else ""

        return {
            "id": event_id,
            "title": title,
            "status": status,
            "period": period,
            "thumbnail_url": thumbnail_url,
            "url": href,
            "is_notice": bool(li.select_one(".sbj img[src*='notice']")),
        }

    def _parse_event_detail(self, html: str, url: str) -> dict[str, Any]:
        soup = BeautifulSoup(html, "lxml")
        view = soup.select_one("#sb-view") or soup

        title = ""
        title_el = view.select_one(".titWrap .sbj")
        if title_el:
            title = _clean_event_title(title_el.get_text(" ", strip=True))

        period = {"raw": "", "start": "", "end": ""}
        for wrap in view.select(".titWrap"):
            text = wrap.get_text(" ", strip=True)
            if "이벤트 기간" in text:
                period = _parse_event_period(text.replace("이벤트 기간 :", "").strip())
                break

        posted_at = ""
        views = None
        for li in view.select(".info li"):
            label = li.select_one("em")
            label_text = label.get_text(strip=True) if label else ""
            value = li.get_text(" ", strip=True).replace(label_text, "", 1).strip()
            if label_text == "작성일":
                posted_at = value
            elif label_text == "조회":
                views = int(re.sub(r"[^\d]", "", value) or 0)

        memo = view.select_one(".memoWrap")
        images: list[str] = []
        body_text = ""
        if memo:
            for img in memo.select("img"):
                src = urljoin(BASE_URL, img.get("src", ""))
                if src and "sb_ico_" not in src:
                    images.append(src)
            body_text = memo.get_text("\n", strip=True)

        attachments: list[dict[str, str]] = []
        for file_li in view.select("ul.file li"):
            file_link = file_li.select_one("a.filename")
            if not file_link:
                continue
            byte_el = file_li.select_one(".byte")
            attachments.append(
                {
                    "name": file_link.get_text(strip=True),
                    "url": urljoin(BASE_URL, file_link.get("href", "")),
                    "meta": byte_el.get_text(" ", strip=True) if byte_el else "",
                }
            )

        return {
            "title": title,
            "period": period,
            "posted_at": posted_at,
            "views": views,
            "images": images,
            "body_text": body_text,
            "attachments": attachments,
            "url": url,
        }

    def _collect_event_list(self) -> tuple[list[dict[str, Any]], int]:
        all_items: list[dict[str, Any]] = []
        max_page = 1

        first_html = self._get(_event_page_url(1)).text
        first_soup = BeautifulSoup(first_html, "lxml")
        count_match = re.search(r"boardTotalCount\s*=\s*'(\d+)'", first_html)
        total_count = int(count_match.group(1)) if count_match else 0

        paging = first_soup.select_one("#sb-paging")
        if paging:
            page_numbers = [1]
            for a in paging.select("a[href]"):
                text = a.get_text(strip=True)
                if text.isdigit():
                    page_numbers.append(int(text))
                href = a.get("href", "")
                page_match = re.search(r"[?&]page=(\d+)", href)
                if page_match:
                    page_numbers.append(int(page_match.group(1)))
            max_page = max(page_numbers)

        seen_ids: set[str] = set()
        for page in range(1, max_page + 1):
            html = first_html if page == 1 else self._get(_event_page_url(page)).text
            soup = BeautifulSoup(html, "lxml")
            for li in soup.select("ul#sb-event > li"):
                item = self._parse_event_list_item(li)
                if item and item["id"] not in seen_ids:
                    seen_ids.add(item["id"])
                    all_items.append(item)

        return all_items, total_count

    def scrape_events(self) -> dict[str, Any]:
        list_items, total_count = self._collect_event_list()
        target_items = [item for item in list_items if item["status"] == "ongoing"]

        detailed_events: list[dict[str, Any]] = []
        for item in target_items:
            detail_html = self._get(item["url"]).text
            detail = self._parse_event_detail(detail_html, item["url"])
            detailed_events.append({**item, **detail})

        ongoing = [item for item in list_items if item["status"] == "ongoing"]
        ended = [item for item in list_items if item["status"] == "ended"]

        return {
            "source_url": _event_page_url(1),
            "total_count": total_count,
            "summary": {
                "list_count": len(list_items),
                "ongoing_count": len(ongoing),
                "ended_count": len(ended),
                "detailed_count": len(detailed_events),
            },
            "ongoing_events": detailed_events,
            "all_events": list_items,
        }

    def _extract_graphql_query(self, js_text: str, query_name: str) -> str:
        marker = f"query {query_name}"
        idx = js_text.find(marker)
        if idx < 0:
            return ""
        end = idx
        for pos in range(idx, min(idx + 12000, len(js_text))):
            if js_text[pos : pos + 2] == '"]':
                end = pos
                break
        return js_text[idx:end].replace("\\n", "\n")

    def _naver_graphql(
        self,
        operation_name: str,
        query: str,
        variables: dict[str, Any],
        referer: str,
    ) -> dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Origin": "https://m.booking.naver.com",
            "Referer": referer,
        }
        response = self.session.post(
            NAVER_GRAPHQL_URL,
            headers=headers,
            json={
                "operationName": operation_name,
                "query": query,
                "variables": variables,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def _parse_passorder_row(self, row, category: str, store_id: str) -> dict[str, Any]:
        name_el = row.select_one("span.text-b1-extrabold.text-gray-800")
        name = name_el.get_text(strip=True) if name_el else ""
        price_text = ""
        for span in row.select("span"):
            text = span.get_text(strip=True)
            if text.endswith("원") and any(ch.isdigit() for ch in text):
                price_text = text
                break
        desc_el = row.select_one("span.truncate.text-b3-regular")
        description = desc_el.get_text(" ", strip=True) if desc_el else ""
        img_el = row.select_one("img")
        badges = [badge.get_text(strip=True) for badge in row.select("span.border-solid")]
        stock = ""
        for span in row.select("span.text-c1-extrabold"):
            stock = span.get_text(strip=True)
        set_info = _parse_set_info(name, description)
        price_krw = _parse_price_krw(price_text)
        return {
            "store_id": store_id,
            "name": name,
            "name_normalized": _normalize_store_menu_name(name),
            "category": category,
            "nav_category": STORE_CATEGORY_MAP.get(category, category),
            "price_krw": price_krw,
            "price_text": price_text,
            "description": description,
            "image_url": img_el.get("src", "") if img_el else "",
            "badges": badges,
            "stock": stock,
            "is_store_exclusive": category in {
                "선착순 한정 이벤트",
                "[선재스님] 신메뉴",
                "[김희은셰프] 신메뉴",
            },
            **set_info,
        }

    def _scrape_passorder_store(self, config: dict[str, Any]) -> dict[str, Any]:
        store_id = config["id"]
        html = self._get(config["url"]).text
        soup = BeautifulSoup(html, "lxml")
        categories: list[dict[str, Any]] = []
        items: list[dict[str, Any]] = []

        for section in soup.select("main section"):
            header = section.select_one("header span")
            category = header.get_text(strip=True) if header else ""
            category_items = []
            for row in section.select('div[role="button"]'):
                item = self._parse_passorder_row(row, category, store_id)
                if not item["name"]:
                    continue
                category_items.append(item)
                items.append(item)
            if category or category_items:
                categories.append({"name": category, "item_count": len(category_items)})

        singles = [item for item in items if not item["is_set"]]
        sets = [item for item in items if item["is_set"]]
        return {
            **config,
            "item_count": len(items),
            "categories": categories,
            "items": items,
            "summary": {
                "single_menus": len(singles),
                "set_menus": len(sets),
                "store_exclusive": sum(1 for item in items if item["is_store_exclusive"]),
            },
        }

    def _scrape_naver_store(self, config: dict[str, Any]) -> dict[str, Any]:
        store_id = config["id"]
        referer = config["url"]
        page_html = self._get(referer).text
        apollo = _extract_js_object(page_html, "__APOLLO_STATE__")
        biz_item_key = f"BizItem:{config['business_id']}_{config['biz_item_id']}"
        biz_item = apollo.get(biz_item_key, {})
        available_start = biz_item.get("availableStartDate")

        js_bundle = self._get(
            "https://m.booking.naver.com/order/static/js/main.0081f12f.js"
        ).text
        schedule_query = self._extract_graphql_query(js_bundle, "orderBizItemSchedule")
        menu_query = self._extract_graphql_query(js_bundle, "menu")
        categories_query = self._extract_graphql_query(js_bundle, "categories")

        schedule_input = {
            "businessId": config["business_id"],
            "bizItemId": config["biz_item_id"],
            "lang": "ko",
        }
        schedule_data = (
            self._naver_graphql(
                "orderBizItemSchedule",
                schedule_query,
                {"input": schedule_input},
                referer,
            )
            if schedule_query
            else {}
        )
        schedule_block = (
            (schedule_data.get("data") or {}).get("orderBizItemSchedule") or {}
        )
        schedule = schedule_block.get("schedule") or {}
        slot_id = schedule.get("slotId")
        unit_start = schedule.get("unitStartDateTime") or available_start

        menu_input: dict[str, Any] = {
            "lang": "ko",
            "businessId": config["business_id"],
            "bizItemType": biz_item.get("bizItemType") or "PICKUP",
            "projections": NAVER_MENU_PROJECTIONS,
            "fallback": {
                "isToday": True,
                "nextStartDate": unit_start,
            },
        }
        if slot_id:
            menu_input["slotId"] = slot_id

        menu_data = (
            self._naver_graphql("menu", menu_query, {"input": menu_input}, referer)
            if menu_query
            else {}
        )
        menu_block = (menu_data.get("data") or {}).get("menu") or {}
        raw_menus = menu_block.get("menus") or []

        categories_data = (
            self._naver_graphql(
                "categories",
                categories_query,
                {
                    "input": {
                        "businessId": config["business_id"],
                        "bizItemId": config["biz_item_id"],
                        "lang": "ko",
                        "slotId": slot_id,
                        "bizItemType": menu_input["bizItemType"],
                    }
                },
                referer,
            )
            if categories_query and slot_id
            else {}
        )
        raw_categories = (categories_data.get("data") or {}).get("categories") or []
        category_by_id = {
            str(cat.get("categoryId")): cat.get("name", "")
            for cat in raw_categories
        }

        items: list[dict[str, Any]] = []
        for raw in raw_menus:
            category_ids = raw.get("categoryIds") or []
            category_name = ""
            if category_ids:
                category_name = category_by_id.get(str(category_ids[0]), "")
            name = raw.get("name", "")
            description = raw.get("desc", "") or ""
            price_krw = raw.get("price") or raw.get("sumPrice")
            if isinstance(price_krw, str):
                price_krw = _parse_price_krw(price_krw)
            set_info = _parse_set_info(name, description)
            items.append(
                {
                    "store_id": store_id,
                    "name": name,
                    "name_normalized": _normalize_store_menu_name(name),
                    "category": category_name,
                    "nav_category": STORE_CATEGORY_MAP.get(
                        category_name, category_name
                    ),
                    "price_krw": price_krw,
                    "price_text": f"{price_krw:,}원" if price_krw else "",
                    "description": description,
                    "image_url": raw.get("titleImageUrl", ""),
                    "badges": (raw.get("tagJson") or {}).get("tags", []),
                    "stock": raw.get("remainStock"),
                    "is_store_exclusive": False,
                    "naver_menu_id": raw.get("id"),
                    "naver_option_id": raw.get("optionId"),
                    **set_info,
                }
            )

        categories = [
            {"name": cat.get("name", ""), "item_count": 0}
            for cat in raw_categories
            if cat.get("depth", 1) == 1
        ]
        error = None
        if not items:
            errors = (menu_data.get("errors") or schedule_data.get("errors") or [])
            if errors:
                error = errors[0].get("message")
            elif not slot_id:
                error = (
                    "영업 슬롯(slotId)을 가져오지 못했습니다. "
                    "매장 영업시간 외에는 네이버 주문 메뉴가 비어 있을 수 있습니다."
                )

        singles = [item for item in items if not item["is_set"]]
        sets = [item for item in items if item["is_set"]]
        return {
            **config,
            "item_count": len(items),
            "categories": categories,
            "items": items,
            "schedule": {
                "slot_id": slot_id,
                "unit_start": unit_start,
                "available_start_date": available_start,
                "is_closed": schedule_block.get("isClosed"),
            },
            "error": error,
            "summary": {
                "single_menus": len(singles),
                "set_menus": len(sets),
                "store_exclusive": sum(
                    1 for item in items if item["is_store_exclusive"]
                ),
            },
        }

    def scrape_store_menus(self) -> dict[str, Any]:
        stores: list[dict[str, Any]] = []
        for config in STORE_MENU_SOURCES:
            print(f"매장 메뉴 수집 중: {config['store_name']} ({config['platform']})...")
            if config["platform"] == "passorder":
                store = self._scrape_passorder_store(config)
            elif config["platform"] == "naver_order":
                store = self._scrape_naver_store(config)
            else:
                continue
            print(
                f"  → {store['item_count']}개 "
                f"(단품 {store['summary']['single_menus']}, "
                f"세트 {store['summary']['set_menus']})"
            )
            if store.get("error"):
                print(f"  [경고] {store['error']}")
            stores.append(store)

        store_only: list[dict[str, Any]] = []
        for store in stores:
            for item in store["items"]:
                if item.get("is_store_exclusive"):
                    store_only.append(item)

        return {
            "sources": [cfg["id"] for cfg in STORE_MENU_SOURCES],
            "stores": stores,
            "store_exclusive_menus": store_only,
        }

    def merge_store_menus(
        self,
        menus: list[dict[str, Any]],
        store_payload: dict[str, Any],
    ) -> list[dict[str, Any]]:
        appended: list[dict[str, Any]] = []
        appended_keys: set[str] = set()

        def _menus_for_key(key: str) -> list[dict[str, Any]]:
            return [
                menu
                for menu in menus
                if _normalize_store_menu_name(menu["name_ko"]) == key
            ]

        for store in store_payload.get("stores", []):
            store_id = store["id"]
            price_by_name: dict[str, int | None] = {}
            for item in store.get("items", []):
                if item.get("is_set"):
                    continue
                if item.get("price_krw") is not None:
                    price_by_name[_normalize_store_menu_name(item["name"])] = item[
                        "price_krw"
                    ]

            for item in store.get("items", []):
                pricing = {
                    "price_krw": item.get("price_krw"),
                    "price_text": item.get("price_text", ""),
                    "category": item.get("category", ""),
                    "nav_category": item.get("nav_category", ""),
                    "url": store.get("url", ""),
                    "image_url": item.get("image_url", ""),
                    "description": item.get("description", ""),
                }

                if item.get("is_set"):
                    base_key = _normalize_store_menu_name(
                        item.get("base_menu_name", item["name"])
                    )
                    base_price = price_by_name.get(base_key)
                    current_price = item.get("price_krw")
                    set_info = {
                        "name": item["name"],
                        "base_menu_name": item.get("base_menu_name", ""),
                        "set_components": item.get("set_components", []),
                        "base_price_krw": base_price,
                        "set_premium_krw": (
                            current_price - base_price
                            if current_price is not None and base_price is not None
                            else None
                        ),
                        "price_krw": current_price,
                    }
                    pricing["set_info"] = set_info
                    matched = _menus_for_key(base_key)
                    if matched:
                        for menu in matched:
                            menu.setdefault("set_variants", []).append(
                                {"store_id": store_id, **set_info}
                            )
                            menu.setdefault("store_pricing", {})[
                                f"{store_id}__set__{_normalize_store_menu_name(item['name'])}"
                            ] = pricing
                        continue

                    store_exclusive = bool(item.get("is_store_exclusive"))
                    item_key = _normalize_store_menu_name(item["name"])
                    if item_key in appended_keys:
                        continue
                    new_item = {
                        "id": f"store_{store_id}_{base_key}_set",
                        "name_ko": item["name"],
                        "name_en": "",
                        "category": item.get("category", ""),
                        "nav_category": item.get("nav_category", ""),
                        "menu_type": "store_exclusive" if store_exclusive else "store",
                        "brand": "salady",
                        "url": store.get("url", ""),
                        "description": item.get("description", ""),
                        "image_url": item.get("image_url", ""),
                        "tags": item.get("badges", []),
                        "store_pricing": {store_id: pricing},
                        "store_exclusive": store_exclusive,
                        "set_variants": [{"store_id": store_id, **set_info}],
                        "nutrition": {},
                        "calorie_calculator": {},
                        "allergy": [],
                    }
                    item_key = _normalize_store_menu_name(item["name"])
                    appended_keys.add(item_key)
                    appended.append(new_item)
                    continue

                key = _normalize_store_menu_name(item["name"])
                matched = _menus_for_key(key)
                if matched:
                    for menu in matched:
                        menu.setdefault("store_pricing", {})[store_id] = pricing
                    continue

                store_exclusive = bool(item.get("is_store_exclusive"))
                if key in appended_keys:
                    continue
                new_item = {
                    "id": f"store_{store_id}_{key}",
                    "name_ko": item["name"],
                    "name_en": "",
                    "category": item.get("category", ""),
                    "nav_category": item.get("nav_category", ""),
                    "menu_type": "store_exclusive" if store_exclusive else "store",
                    "brand": "salady",
                    "url": store.get("url", ""),
                    "description": item.get("description", ""),
                    "image_url": item.get("image_url", ""),
                    "tags": item.get("badges", []),
                    "store_pricing": {store_id: pricing},
                    "store_exclusive": store_exclusive,
                    "nutrition": {},
                    "calorie_calculator": {},
                    "allergy": [],
                }
                appended_keys.add(key)
                appended.append(new_item)

        return menus + appended

    def _load_existing_json(self, filename: str) -> list[dict[str, Any]]:
        path = self.output_dir / filename
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def _save_image(self, url: str, menu_id: str) -> str:
        if not url or not self.download_images:
            return ""
        parsed = urlparse(url)
        ext = Path(parsed.path).suffix or ".jpg"
        dest = self.images_dir / f"{menu_id}{ext}"
        self._download_file(url, dest)
        return str(dest.relative_to(self.output_dir))

    def merge_data(
        self,
        menus: list[MenuItem],
        calorie_data: dict[str, Any],
        nutrition_pdf_rows: list[dict[str, Any]],
        allergy_rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        calorie_by_name = {
            _normalize_menu_name(m["name"]): m for m in calorie_data.get("menus", [])
        }
        nutrition_by_name = {
            _normalize_menu_name(r.get("menu", "")): r
            for r in nutrition_pdf_rows
            if r.get("menu")
        }
        allergy_by_name = {
            _normalize_menu_name(r.get("menu", "")): r.get("allergens", [])
            for r in allergy_rows
            if r.get("menu")
        }

        merged: list[dict[str, Any]] = []
        for menu in menus:
            data = asdict(menu)
            key = _normalize_menu_name(menu.name_ko)
            calc = calorie_by_name.get(key)
            if calc:
                data["calorie_calculator"] = calc

            pdf_nutrition = nutrition_by_name.get(key)
            if pdf_nutrition:
                data["nutrition_pdf"] = pdf_nutrition
            elif menu.nutrition:
                data["nutrition_pdf"] = menu.nutrition

            allergy = allergy_by_name.get(key)
            if allergy:
                data["allergy"] = allergy if isinstance(allergy, list) else [allergy]

            if menu.image_url:
                local_image = self._save_image(menu.image_url, menu.id)
                if local_image:
                    data["image_local"] = local_image

            merged.append(data)

        return merged

    def save_outputs(
        self,
        menus: list[dict[str, Any]],
        calorie_data: dict[str, Any],
        nutrition_pdf_rows: list[dict[str, Any]],
        allergy_rows: list[dict[str, Any]],
        group_order: dict[str, Any] | None = None,
        app_services: dict[str, Any] | None = None,
        extra_toppings: dict[str, list[dict[str, Any]]] | None = None,
        store_menus: dict[str, Any] | None = None,
        events: dict[str, Any] | None = None,
        dressings_catalog: dict[str, Any] | None = None,
    ) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        (self.output_dir / "menus.json").write_text(
            json.dumps(menus, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (self.output_dir / "calorie_calculator.json").write_text(
            json.dumps(calorie_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if nutrition_pdf_rows:
            (self.output_dir / "nutrition_pdf.json").write_text(
                json.dumps(nutrition_pdf_rows, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if allergy_rows:
            (self.output_dir / "allergy_pdf.json").write_text(
                json.dumps(allergy_rows, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if group_order:
            (self.output_dir / "group_order.json").write_text(
                json.dumps(group_order, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if app_services:
            (self.output_dir / "app_services.json").write_text(
                json.dumps(app_services, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if extra_toppings:
            (self.output_dir / "extra_toppings.json").write_text(
                json.dumps(extra_toppings, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if store_menus:
            (self.output_dir / "store_menus.json").write_text(
                json.dumps(store_menus, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if events:
            (self.output_dir / "events.json").write_text(
                json.dumps(events, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if dressings_catalog:
            (self.output_dir / "dressings.json").write_text(
                json.dumps(dressings_catalog, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        write_menus_csv(menus, self.output_dir)

    def run(
        self,
        skip_pdfs: bool = False,
        max_menus: int | None = None,
        skip_store_menus: bool = False,
        skip_events: bool = False,
        skip_image_ocr: bool = False,
    ) -> None:
        print("메인 메뉴 링크 수집 중...")
        links = self.collect_menu_links()
        if max_menus:
            links = links[:max_menus]
        print(f"  → {len(links)}개 메인 메뉴")

        print("메인 메뉴 상세 페이지 크롤링 중...")
        menus: list[MenuItem] = []
        for i, link in enumerate(links, 1):
            print(f"  [{i}/{len(links)}] {link.get('name_ko') or link['id']}")
            menus.append(self.parse_menu_detail(link))

        if not max_menus:
            print("토핑·드레싱·음료·사이드 수집 중...")
            popup_items = self.collect_popup_items()
            print(f"  → {len(popup_items)}개 추가")
            menus.extend(popup_items)
        print(f"  → 총 {len(menus)}개 메뉴")

        print("칼로리 계산기 데이터 수집 중...")
        calorie_data = self.parse_calorie_calculator()

        nutrition_pdf_rows: list[dict[str, Any]] = []
        allergy_rows: list[dict[str, Any]] = []

        if not skip_pdfs:
            print("영양성분 PDF 다운로드 및 파싱 중...")
            nutrition_pdf = self._download_file(NUTRITION_PDF_URL, self.pdf_dir / "nutrition.pdf")
            nutrition_pdf_rows = self.parse_pdf_tables(nutrition_pdf)
            print(f"  → {len(nutrition_pdf_rows)}행 추출")

            print("알레르기 PDF 다운로드 및 파싱 중...")
            allergy_pdf = self._download_file(ALLERGY_PDF_URL, self.pdf_dir / "allergy.pdf")
            allergy_rows = self.parse_allergy_pdf(allergy_pdf)
            print(f"  → {len(allergy_rows)}행 추출")
        else:
            nutrition_pdf_rows = self._load_existing_json("nutrition_pdf.json")
            allergy_rows = self._load_existing_json("allergy_pdf.json")

        calorie_data = self.enrich_calorie_toppings(calorie_data, nutrition_pdf_rows)
        print(f"  → 메뉴 {len(calorie_data.get('menus', []))}개, "
              f"토핑 카테고리 {len(calorie_data.get('topping_categories', {}))}개")

        extra_toppings: dict[str, list[dict[str, Any]]] = {}
        if nutrition_pdf_rows:
            extra_toppings = self.extract_addon_toppings(nutrition_pdf_rows)
            print(f"추가 토핑(PDF) 추출: {sum(len(v) for v in extra_toppings.values())}개")

        group_order: dict[str, Any] | None = None
        app_services: dict[str, Any] | None = None
        if not max_menus:
            print("단체주문 정보 수집 중...")
            group_order = self.scrape_group_order()
            if not skip_image_ocr:
                group_order = self._enrich_group_order_ocr(group_order)
            print(f"  → 세트메뉴 {len(group_order.get('set_menus', []))}개, "
                  f"대표메뉴 {len(group_order.get('representative_menus', []))}개")

            print("앱·멤버십·기프트카드 정보 수집 중...")
            app_services = self.scrape_app_services()
            if not skip_image_ocr:
                app_services = self._enrich_membership_ocr(app_services)
            print(f"  → {len(app_services)}개 페이지")
            if not skip_image_ocr and app_services.get("membership", {}).get("grade_table"):
                grades = app_services["membership"]["grade_table"].get("grades", [])
                print(f"  → 멤버십 등급표 {len(grades)}단계 파싱")

        events: dict[str, Any] | None = None
        if not skip_events and not max_menus:
            print("진행 중 이벤트 수집 중...")
            events = self.scrape_events()
            print(
                f"  → 진행중 {events['summary']['ongoing_count']}개 "
                f"(전체 게시 {events['total_count']}개)"
            )

        print("데이터 병합 및 저장 중...")
        merged = self.merge_data(menus, calorie_data, nutrition_pdf_rows, allergy_rows)

        store_menus: dict[str, Any] | None = None
        if not skip_store_menus and not max_menus:
            store_menus = self.scrape_store_menus()
            merged = self.merge_store_menus(merged, store_menus)

        dressings_catalog = build_dressings_catalog(extra_toppings, calorie_data)
        merged = enrich_menu_dressings(merged, dressings_catalog)
        dressing_menus = sum(
            1 for m in merged if m.get("recommended_dressing") or m.get("included_dressing")
        )
        print(
            f"  → 드레싱 카탈로그 {dressings_catalog['count']}개, "
            f"메뉴 드레싱 {dressing_menus}개"
        )

        self.save_outputs(
            merged,
            calorie_data,
            nutrition_pdf_rows,
            allergy_rows,
            group_order=group_order,
            app_services=app_services,
            extra_toppings=extra_toppings,
            store_menus=store_menus,
            events=events,
            dressings_catalog=dressings_catalog,
        )
        print(f"완료: {self.output_dir.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Salady 메뉴/영양 데이터 크롤러")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output"),
        help="결과 저장 디렉터리 (기본: output)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=REQUEST_DELAY,
        help="요청 간 대기 시간(초)",
    )
    parser.add_argument(
        "--images",
        action="store_true",
        help="메뉴 이미지 다운로드",
    )
    parser.add_argument(
        "--skip-pdfs",
        action="store_true",
        help="PDF 다운로드/파싱 생략",
    )
    parser.add_argument(
        "--max-menus",
        type=int,
        default=None,
        help="테스트용 최대 메뉴 수",
    )
    parser.add_argument(
        "--skip-store-menus",
        action="store_true",
        help="패스오더·네이버 매장 메뉴판 수집 생략",
    )
    parser.add_argument(
        "--skip-events",
        action="store_true",
        help="진행 중 이벤트 수집 생략",
    )
    parser.add_argument(
        "--skip-image-ocr",
        action="store_true",
        help="세트메뉴·멤버십 등급표 이미지 OCR 생략",
    )
    args = parser.parse_args()

    scraper = SaladyScraper(
        output_dir=args.output,
        delay=args.delay,
        download_images=args.images,
    )
    scraper.run(
        skip_pdfs=args.skip_pdfs,
        max_menus=args.max_menus,
        skip_store_menus=args.skip_store_menus,
        skip_events=args.skip_events,
        skip_image_ocr=args.skip_image_ocr,
    )


if __name__ == "__main__":
    main()
