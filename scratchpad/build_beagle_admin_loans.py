#!/usr/bin/env python3
"""Rebuild the Beagle product in the Admin Loan Flows deck from the Figma
'Beagle | Loans' admin section (node 102:36527). Replaces the bootstrapped
Beagle *visits* group with the real Beagle admin *loan* flows. Titles = frame names.
Desktop viewport."""
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/beagle-admin-loans")
DECK_FN = os.path.join(HOME, "oro-admin-loan-flows-walkthrough.html")

T = {
 "bl01-loans": "Loans",
 "bl02-loan-type": "Loan type",
 "bl03-loan-details": "Loan details",
 "bl04-summary": "Summary",
 "bl05-paisa": "Paisa",
 "bl06-ft": "FT",
 "bl07-docs": "Docs",
 "bl08-reports": "Reports",
 "bl09-activity-log": "Activity Log",
 "bl10-gold-details": "Gold details",
 "bl11-visit-details": "Visit details",
 "bl12-leads-details": "Leads details",
 "bl13-customer-checks": "Customer Checks",
 "bl14-account-opening": "Account Opening",
 "bl15-pledge-card-ft": "Pledge Card Submission & Fund Transfer",
 "bl16-fund-transfer": "Fund Transfer",
 "bl17-pending-approval": "Pending orocorp approval",
}

FLOWS = [
 ("The loans queue", "bg-loans-list", "Beagle admin · loans",
  "How Loan Ops finds and filters loans.", ["bl01-loans", "bl02-loan-type"]),
 ("Loan detail & tabs", "bg-loan-detail", "Beagle admin · detail",
  "The loan detail view and its tabs.",
  ["bl03-loan-details", "bl04-summary", "bl05-paisa", "bl06-ft", "bl07-docs", "bl08-reports", "bl09-activity-log"]),
 ("Loan sections", "bg-loan-sections", "Beagle admin · sections",
  "The detail sections Ops reviews.",
  ["bl10-gold-details", "bl11-visit-details", "bl12-leads-details", "bl13-customer-checks",
   "bl14-account-opening", "bl15-pledge-card-ft", "bl16-fund-transfer"]),
 ("Orocorp approval", "bg-loan-approval", "Beagle admin · approval",
  "Approving the loan.", ["bl17-pending-approval"]),
]

def datauri(stem):
    with open(os.path.join(ASSETS, stem + ".png"), "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

flows = []
for name, slug, kicker, blurb, stems in FLOWS:
    steps = [{"img": datauri(st), "title": T[st], "caption": ""} for st in stems]
    flows.append({"name": name, "slug": slug, "kicker": kicker, "blurb": blurb, "steps": steps})
new_group = {"platform": "Admin", "_product": "Beagle", "_appType": "Loan Flows",
             "viewport": "desktop", "kicker": "Beagle · how Ops manages the gold loan", "flows": flows}

html = open(DECK_FN, encoding="utf-8").read()
s = html.index('const DECK'); b = html.index('[', s); d = 0
for i in range(b, len(html)):
    if html[i] == '[': d += 1
    elif html[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(html[b:i + 1])
gi = next(gi for gi, g in enumerate(deck) if g.get("_product") == "Beagle")
old = sum(len(f["steps"]) for f in deck[gi]["flows"])
deck[gi] = new_group
slugs = [f["slug"] for g in deck for f in g["flows"]]
dupes = {x for x in slugs if slugs.count(x) > 1}
assert not dupes, "dup slugs: %s" % dupes
open(DECK_FN, "w", encoding="utf-8").write(html[:b] + json.dumps(deck, ensure_ascii=True) + html[i + 1:])
print("Beagle group[%d] rebuilt: %d -> %d screens, %d flows" % (gi, old, sum(len(f['steps']) for f in flows), len(flows)))
for f in flows: print("   [%s] %s (%d)" % (f['slug'], f['name'], len(f['steps'])))
