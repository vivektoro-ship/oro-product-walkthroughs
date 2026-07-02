#!/usr/bin/env python3
"""Rebuild the standalone appraisal section in field-apps from the Figma
'Px App | Standalone Appraisal Module' section, with REAL page titles."""
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/appraisal-px")
DECK_FN = os.path.join(HOME, "oro-field-apps-walkthrough.html")

TITLES = {
 "01": "Manikanada Krishnan", "02": "Gold Valuation", "03": "Gold Valuations",
 "04": "Gold Valuation", "05": "Gold Valuations", "06": "Gold Valuation",
 "07": "Touchstone Photo", "08": "Edit Gold Valuation", "09": "Touchstone Photo",
 "10": "Edit Gold Valuation", "11": "Gold Valuation", "12": "Add Gold Item",
 "13": "Gold Item Added!", "14": "Gold Valuation", "15": "Valuation Completed",
}
ORDER = [f"{i:02d}" for i in range(1, 16)]

def datauri(nn):
    with open(os.path.join(ASSETS, nn + ".png"), "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

steps = [{"img": datauri(nn), "title": TITLES[nn], "caption": ""} for nn in ORDER]
new_flow = {"name": "The standalone appraisal, end to end", "slug": "appraisal",
            "kicker": "Standalone appraisal", "blurb": "Oro's own gold valuation, decoupled from a loan.",
            "steps": steps}

html = open(DECK_FN, encoding="utf-8").read()
s = html.index('const DECK'); b = html.index('[', s); d = 0
for i in range(b, len(html)):
    if html[i] == '[': d += 1
    elif html[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(html[b:i + 1])
hit = [gi for gi, g in enumerate(deck) if any(f["slug"] == "appraisal" for f in g["flows"])]
if not hit:
    raise SystemExit("no appraisal group found")
gi = hit[0]
old = sum(len(f["steps"]) for f in deck[gi]["flows"])
deck[gi]["flows"] = [new_flow]
deck[gi]["viewport"] = "mobile"
new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[i + 1:]
open(DECK_FN, "w", encoding="utf-8").write(new_html)
print("appraisal group[%d] rebuilt: %d -> %d steps | %.1f MB" % (gi, old, len(steps), len(new_html)/1024/1024))
