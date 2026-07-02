#!/usr/bin/env python3
"""BRL admin loan as a SINGLE HD flow, from Figma 'BRL Flow' (10250:171116).
Replaces the Takeover (BRL) product group in the Admin Loan Flows deck."""
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/brl-loan-flow")
DECK_FN = os.path.join(HOME, "oro-admin-loan-flows-walkthrough.html")

STEPS = [
 ("br01", "All Visits"), ("br02", "Visit Planned"), ("br03", "Assign Partner"),
 ("br04", "Partner Assigned"), ("br05", "Visit Assigned"), ("br06", "Partner Arrived"),
 ("br07", "Customer Liveliness Check"), ("br08", "Pledge Card Submission"),
 ("br09", "Customer Feasibility Checks"), ("br10", "Pledge Card Submission"),
 ("br11", "Pledge Cards Submitted"), ("br12", "BRL Approved"),
 ("br13", "eSign Pending — Primary"), ("br14", "eSign Complete — Primary"),
 ("br15", "eSign Pending — Co-borrower"), ("br16", "eSign Complete — All"),
 ("br17", "Fund Transfer Complete"), ("br18", "Payment Proof Pending"),
 ("br19", "Payment Proof Submitted"), ("br20", "Payment Proof Approved"),
 ("br21", "Payment Proof Approved"), ("br22", "ELR Visits Scheduled"),
 ("br23", "ELR Visits Scheduled"), ("br24", "ELR Visits Scheduled"),
]

def datauri(stem):
    with open(os.path.join(ASSETS, stem + ".png"), "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

steps = [{"img": datauri(st), "title": t, "caption": ""} for st, t in STEPS]
flow = {"name": "The BRL loan, end to end", "slug": "tk-brl-e2e",
        "kicker": "Takeover admin · BRL loan", "blurb": "The full admin BRL loan journey, screen by screen.",
        "steps": steps}
new_group = {"platform": "Admin", "_product": "Takeover (BRL)", "_appType": "Loan Flows",
             "viewport": "desktop", "kicker": "Takeover · how Ops manages the bridge loan", "flows": [flow]}

html = open(DECK_FN, encoding="utf-8").read()
s = html.index('const DECK'); b = html.index('[', s); d = 0
for i in range(b, len(html)):
    if html[i] == '[': d += 1
    elif html[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(html[b:i + 1])
gi = next(gi for gi, g in enumerate(deck) if str(g.get("_product")).startswith("Takeover"))
deck[gi] = new_group
slugs = [f["slug"] for g in deck for f in g["flows"]]
assert len({x for x in slugs if slugs.count(x) > 1}) == 0, "dup slugs"
open(DECK_FN, "w", encoding="utf-8").write(html[:b] + json.dumps(deck, ensure_ascii=True) + html[i + 1:])
print("Takeover(BRL) -> single flow: %d screens | %.1f MB" % (len(steps), os.path.getsize(DECK_FN)/1024/1024))
