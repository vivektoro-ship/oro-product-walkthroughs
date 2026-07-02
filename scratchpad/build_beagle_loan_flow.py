#!/usr/bin/env python3
"""Beagle admin loan as a SINGLE flow, from Figma 'Section 4' (10174:203631), HD screens.
Replaces the Beagle product group in the Admin Loan Flows deck with one continuous flow."""
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/beagle-loan-flow")
DECK_FN = os.path.join(HOME, "oro-admin-loan-flows-walkthrough.html")

# ordered (stem, title). Titles from frame names; most frames are the loan-detail states.
STEPS = [
 ("bf01", "Loans"),
 ("bf02", "Loan details"), ("bf03", "Loan details"), ("bf04", "Loan details"),
 ("bf05", "Loan details"), ("bf06", "Loan details"), ("bf07", "Loan details"),
 ("bf08", "Loan details"), ("bf09", "Loan details"), ("bf10", "Loan details"),
 ("bf11", "Loan details"), ("bf12", "Loan details"), ("bf13", "Loan details"),
 ("bf14", "Loan details"), ("bf15", "Loan details"), ("bf16", "Loan details"),
 ("bf17", "Loan details"), ("bf18", "Loan details"),
 ("bf19", "Customer Checks"), ("bf20", "Account Opening"),
 ("bf21", "Loan details"),
 ("bf22", "Pledge Card Submission & Fund Transfer"),
 ("bf23", "Loan details"), ("bf24", "Loan details"), ("bf25", "Loan details"),
 ("bf26", "Loan details"), ("bf27", "Loan details"), ("bf28", "Loan details"),
 ("bf29", "Loan details"), ("bf30", "Loan details"),
]

def datauri(stem):
    with open(os.path.join(ASSETS, stem + ".png"), "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

steps = [{"img": datauri(st), "title": t, "caption": ""} for st, t in STEPS]
flow = {"name": "The Beagle loan, end to end", "slug": "bg-loan-e2e",
        "kicker": "Beagle admin · loan", "blurb": "The full admin loan journey, screen by screen.",
        "steps": steps}
new_group = {"platform": "Admin", "_product": "Beagle", "_appType": "Loan Flows",
             "viewport": "desktop", "kicker": "Beagle · how Ops manages the gold loan", "flows": [flow]}

html = open(DECK_FN, encoding="utf-8").read()
s = html.index('const DECK'); b = html.index('[', s); d = 0
for i in range(b, len(html)):
    if html[i] == '[': d += 1
    elif html[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(html[b:i + 1])
gi = next(gi for gi, g in enumerate(deck) if g.get("_product") == "Beagle")
deck[gi] = new_group
slugs = [f["slug"] for g in deck for f in g["flows"]]
assert len({x for x in slugs if slugs.count(x) > 1}) == 0, "dup slugs"
open(DECK_FN, "w", encoding="utf-8").write(html[:b] + json.dumps(deck, ensure_ascii=True) + html[i + 1:])
print("Beagle -> single flow: %d screens | %.1f MB" % (len(steps), (os.path.getsize(DECK_FN))/1024/1024))
