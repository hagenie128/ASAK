from pathlib import Path
from salady_scraper import SaladyScraper, NAVER_MENU_PROJECTIONS, _extract_js_object
import json
import re

s = SaladyScraper(output_dir=Path("output"), delay=0.2)
referer = "https://m.booking.naver.com/order/bizes/425424/items/3629791"
page = s._get(referer).text
apollo = _extract_js_object(page, "__APOLLO_STATE__")
biz = apollo.get("BizItem:425424_3629791", {})
print("BizItem keys", list(biz.keys()))
print(json.dumps({k: biz[k] for k in list(biz.keys())[:30]}, ensure_ascii=False, indent=2)[:2000])

m = re.search(r"/order/static/js/main\.([a-f0-9]+)\.js", page)
js = s._get(f"https://m.booking.naver.com/order/static/js/main.{m.group(1)}.js").text
sq = s._extract_graphql_query(js, "orderBizItemSchedule")
mq = s._extract_graphql_query(js, "menu")
dq = s._extract_graphql_query(js, "menuDetail")

# try schedule variations
for date in ["2026-07-01", "2026-07-02", "2026-06-30"]:
    for is_today in [True, False]:
        inp = {
            "businessId": "425424",
            "bizItemId": "3629791",
            "lang": "ko",
            "fallback": {"isToday": is_today, "nextStartDate": date},
        }
        data = s._naver_graphql("orderBizItemSchedule", sq, {"input": inp}, referer)
        sched = (data.get("data") or {}).get("orderBizItemSchedule")
        slot = (sched or {}).get("schedule", {}).get("slotId") if sched else None
        print(f"schedule date={date} isToday={is_today} -> slot={slot} sched_null={sched is None}")

# if we find a slot, try menu; else try menu with bizItemId from apollo
biz_type = biz.get("bizItemType") or "PICKUP"
for slot_id in [None, biz.get("slotId")]:
    menu_input = {
        "lang": "ko",
        "businessId": "425424",
        "bizItemId": "3629791",
        "bizItemType": biz_type,
        "projections": NAVER_MENU_PROJECTIONS,
        "fallback": {"isToday": False, "nextStartDate": biz.get("availableStartDate") or "2026-07-02"},
    }
    if slot_id:
        menu_input["slotId"] = slot_id
    data = s._naver_graphql("menu", mq, {"input": menu_input}, referer)
    menus = (data.get("data") or {}).get("menu", {}).get("menus")
    print("menu with slot", slot_id, "count", None if menus is None else len(menus))

# Search JS for MenuParams / fallback usage
for term in ["MenuParams", "nextStartDate", "slotId", "isClosed"]:
    idx = js.find(term)
    print(term, "at", idx)
