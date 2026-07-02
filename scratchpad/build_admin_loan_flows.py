#!/usr/bin/env python3
"""Build a NEW standalone deck: Admin Loan Flows (Beagle + Takeover).
Bootstraps from the admin groups already in oro-all-flows, reuses the field-apps
composite template (multi-level product index), rebrands the masthead, and makes
the app-type index dynamic. Two products: Beagle (Manage Visits) and Takeover
(Manage Visits + Manage Loans). Desktop viewport."""
import json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HOME, "oro-all-flows-walkthrough.html")
TEMPLATE = os.path.join(HOME, "oro-field-apps-walkthrough.html")
OUT = os.path.join(HOME, "oro-admin-loan-flows-walkthrough.html")

def load_deck(html):
    s = html.index('const DECK'); b = html.index('[', s); d = 0
    for i in range(b, len(html)):
        if html[i] == '[': d += 1
        elif html[i] == ']':
            d -= 1
            if d == 0: break
    return b, i + 1, json.loads(html[b:i + 1])

src_html = open(SRC, encoding="utf-8").read()
_, _, src = load_deck(src_html)

def find(pred):
    for g in src:
        if pred(g): return json.loads(json.dumps(g))  # deep copy
    raise SystemExit("group not found")

beagle = find(lambda g: g.get('_product') == 'Beagle revamp' and g['platform'] == 'Admin')
tk_loans = find(lambda g: g.get('_product') == 'Takeover revamp' and g['platform'] == 'Admin — Loans')

# Loan flows only — no visit-management flows. Keep Beagle + BRL (Takeover loans).
beagle.update({"_product": "Beagle", "_appType": "Loan Flows", "viewport": "desktop",
               "platform": "Admin", "kicker": "Beagle · how Ops manages the gold loan"})
tk_loans.update({"_product": "Takeover (BRL)", "_appType": "Loan Flows", "viewport": "desktop",
                 "platform": "Admin", "kicker": "Takeover · how Ops manages the bridge loan"})

deck = [beagle, tk_loans]

# slug uniqueness
slugs = [f['slug'] for g in deck for f in g['flows']]
dupes = {x for x in slugs if slugs.count(x) > 1}
assert not dupes, "dup slugs: %s" % dupes

# ---- build the new HTML from the field-apps template ----
tpl = open(TEMPLATE, encoding="utf-8").read()
b, e, _ = load_deck(tpl)
tpl = tpl[:b] + json.dumps(deck, ensure_ascii=True) + tpl[e:]

# rebrand + dynamic app types
reps = [
 ("<title>Oro — Customer & Partner Apps</title>", "<title>Oro — Admin Loan Flows</title>"),
 ("Oro &nbsp;·&nbsp; Customer & Partner Apps", "Oro &nbsp;·&nbsp; Admin Loan Flows"),
 ("<h1>Customer & Partner <em>Apps</em></h1>", "<h1>Admin <em>Loan Flows</em></h1>"),
 ("The customer and partner app flows across Offers, Gold Loan and Takeover. Pick a product, then an app.",
  "How Loan Ops manages Beagle and Takeover loan flows in Admin. Pick a product, then an area."),
 ("var APPTYPES=['User App','Partner App'];",
  "var APPTYPES=[]; DECK.forEach(function(g){ if(APPTYPES.indexOf(g._appType)<0) APPTYPES.push(g._appType); });"),
 ("sh.textContent='Choose an app'", "sh.textContent='Choose an area'"),
]
for a, bb in reps:
    assert a in tpl, "replacement target missing: %.60s" % a
    tpl = tpl.replace(a, bb)

open(OUT, "w", encoding="utf-8").write(tpl)
tot = sum(len(f['steps']) for g in deck for f in g['flows'])
print("WROTE", os.path.basename(OUT), "| %.1f MB" % (len(tpl)/1024/1024))
print("groups: %d | flows: %d | screens: %d" % (len(deck), len(slugs), tot))
for g in deck:
    print("  %-9s / %-14s (%d flows, %d screens)" % (g['_product'], g['_appType'],
          len(g['flows']), sum(len(f['steps']) for f in g['flows'])))
