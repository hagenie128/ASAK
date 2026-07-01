from pathlib import Path
from salady_scraper import SaladyScraper
import json
import re

s = SaladyScraper(output_dir=Path("output"), delay=0.2)
url = "https://m.booking.naver.com/order/bizes/425424/items/3629791"
page = s._get(url).text
# find main js hash from page
m = re.search(r"/order/static/js/main\.([a-f0-9]+)\.js", page)
print("main hash", m.group(1) if m else "not found")
js_url = f"https://m.booking.naver.com/order/static/js/main.{m.group(1)}.js" if m else ""
js = s._get(js_url).text if js_url else ""

detail_q = s._extract_graphql_query(js, "menuDetail")
print("menuDetail query len", len(detail_q))
if detail_q:
    print(detail_q[:500])

# sample menu ids from user HTML - we need real ids; try search apollo
from salady_scraper import _extract_js_object

apollo = _extract_js_object(page, "__APOLLO_STATE__")
print("apollo keys", list(apollo.keys())[:20])

# search for Menu in js
for pat in ["menuDetail", "MenuOption", "optionGroups", "subOptions"]:
    if pat in js:
        print("found in js:", pat)

# try menuDetail with guessed input from graphql patterns in js
frag = re.findall(r'menuDetail[^}]{0,200}', js)
print("fragments", len(frag))
for f in frag[:3]:
    print(f[:180])
