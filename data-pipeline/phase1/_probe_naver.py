from pathlib import Path
from salady_scraper import SaladyScraper, NAVER_MENU_PROJECTIONS
import json
import re

s = SaladyScraper(output_dir=Path("output"), delay=0.2)
url = "https://m.booking.naver.com/order/bizes/425424/items/3629791"
js = s._get("https://m.booking.naver.com/order/static/js/main.0081f12f.js").text

ops = set(re.findall(r'operationName:"([^"]+)"', js))
print("total ops", len(ops))
for name in sorted(ops):
    if "menu" in name.lower() or "schedule" in name.lower() or "biz" in name.lower():
        print(" ", name)

for name in [
    "menu",
    "menuDetail",
    "menuOption",
    "categories",
    "orderBizItemSchedule",
    "bizItemMenus",
    "menuOptions",
]:
    q = s._extract_graphql_query(js, name)
    print(name, "query", "yes" if q else "no")

sq = s._extract_graphql_query(js, "orderBizItemSchedule")
sched = s._naver_graphql(
    "orderBizItemSchedule",
    sq,
    {"input": {"businessId": "425424", "bizItemId": "3629791", "lang": "ko"}},
    url,
)
print("schedule:", json.dumps(sched, ensure_ascii=False)[:1500])

menu_query = s._extract_graphql_query(js, "menu")
# try with bizItemId
for extra in [
    {},
    {"bizItemId": "3629791"},
    {"slotId": "dummy"},
]:
    menu_input = {
        "lang": "ko",
        "businessId": "425424",
        "bizItemType": "PICKUP",
        "projections": NAVER_MENU_PROJECTIONS,
        "fallback": {"isToday": False, "nextStartDate": "2026-07-02"},
        **extra,
    }
    data = s._naver_graphql("menu", menu_query, {"input": menu_input}, url)
    menus = (data.get("data") or {}).get("menu", {}).get("menus")
    print("extra", extra, "menus", None if menus is None else len(menus), "errors", data.get("errors"))
