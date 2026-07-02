from pathlib import Path

from bs4 import BeautifulSoup
from salady_scraper import SaladyScraper, POPUP_LIST_CONFIGS, POPUP_NUTRITION_KEYS

s = SaladyScraper(Path("output"))
found = []
for list_url, brand, nav_category, menu_type in POPUP_LIST_CONFIGS:
    soup = BeautifulSoup(s._get(list_url).text, "lxml")
    for li in soup.select(".menu_list li"):
        strong = li.select_one("strong")
        name = strong.get_text(" ", strip=True) if strong else ""
        anchor = li.select_one("a.pop_click, a[href*='pop_view']")
        href = anchor.get("href", "") if anchor else ""
        if any(k in name for k in ("시저", "허니", "들기름", "드레싱")):
            nut = s._parse_popup_nutrition(href) if href else {}
            found.append((name, nut, list_url))

Path("_popup_dressings.txt").write_text(
    "\n".join(f"{n}\t{nut}\t{url}" for n, nut, url in found),
    encoding="utf-8",
)
print("found", len(found))
