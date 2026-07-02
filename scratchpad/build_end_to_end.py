#!/usr/bin/env python3
"""Add a big 'End to End Flow' section to Beagle revamp and Takeover revamp in field-apps.
Interleaves every customer (CX) and partner (PX) screen in chronological order, each tagged
with its actor. No screen skipped. Reuses steps already embedded in the deck."""
import json, os
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FN = os.path.join(HOME, "oro-field-apps-walkthrough.html")

# (flow_slug, start, end, actor)  end exclusive; None,None = all steps
BEAGLE = [
 ("bg-cx-book", None, None, "Customer"),
 ("bg-pa-start", None, None, "Partner"), ("bg-cx-verify", 0, 2, "Customer"),
 ("bg-pa-verify", 0, 2, "Partner"), ("bg-cx-verify", 2, 4, "Customer"),
 ("bg-pa-verify", 2, 6, "Partner"), ("bg-cx-verify", 4, 5, "Customer"),
 ("bg-pa-verify", 6, 10, "Partner"), ("bg-cx-verify", 5, 7, "Customer"),
 ("bg-pa-verify", 10, 14, "Partner"),
 ("bg-pa-appraisal", None, None, "Partner"), ("bg-cx-appraisal", None, None, "Customer"),
 ("bg-pa-plan", None, None, "Partner"), ("bg-cx-plan", None, None, "Customer"),
 ("bg-cx-esign", None, None, "Customer"), ("bg-pa-esign", None, None, "Partner"),
 ("bg-pa-approval", None, None, "Partner"), ("bg-cx-fund", 0, 2, "Customer"),
 ("bg-pa-fund", None, None, "Partner"), ("bg-cx-fund", 2, 4, "Customer"),
 ("beagle-manage", None, None, "Customer"),
 ("cx-gl-release", 0, 4, "Customer"), ("pa-gl-release", None, None, "Partner"),
 ("cx-gl-release", 4, 6, "Customer"),
 ("bg-px-queues", None, None, "Partner"),
]
TAKEOVER = [
 ("takeover-book", None, None, "Customer"),
 ("tk-px-start", None, None, "Partner"), ("takeover-visit", 0, 4, "Customer"),
 ("tk-px-onboarding", None, None, "Partner"), ("tk-px-verify", None, None, "Partner"),
 ("takeover-visit", 4, 6, "Customer"),
 ("tk-px-coborrower", None, None, "Partner"),
 ("takeover-verify", None, None, "Customer"),
 ("tk-px-pledge", None, None, "Partner"),
 ("takeover-setup", None, None, "Customer"),
 ("tk-px-approval", None, None, "Partner"), ("tk-cx-esign", None, None, "Customer"),
 ("tk-px-funds", None, None, "Partner"), ("tk-cx-fund", None, None, "Customer"),
 ("tk-px-proof", None, None, "Partner"),
 ("tk-px-release", None, None, "Partner"), ("elr-find", None, None, "Customer"), ("elr-items", None, None, "Customer"),
 ("elr-storage-partner", None, None, "Partner"), ("elr-track", 0, 5, "Customer"),
 ("elr-collect-co", None, None, "CO Staff"),
 ("elr-retrieval-partner", None, None, "Partner"), ("elr-track", 5, 7, "Customer"),
 ("elr-return-co", None, None, "CO Staff"),
 ("elr-schedule-takeover", None, None, "Partner"), ("elr-track", 7, 8, "Customer"),
]

h = open(FN, encoding="utf-8").read()
s = h.index('const DECK'); b = h.index('[', s); d = 0
for i in range(b, len(h)):
    if h[i] == '[': d += 1
    elif h[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(h[b:i + 1])

flows = {f['slug']: f for g in deck for f in g['flows']}

def assemble(spec):
    out = []
    for slug, a, bnd, actor in spec:
        steps = flows[slug]['steps']
        seg = steps if a is None else steps[a:bnd]
        for st in seg:
            cp = dict(st); cp['actor'] = actor
            out.append(cp)
    return out

def add_e2e(product, kicker, slug, spec):
    # remove any prior e2e group for idempotency
    for gi in [gi for gi, g in enumerate(deck) if g.get('_product') == product and g.get('_appType') == 'End to End']:
        del deck[gi]
    steps = assemble(spec)
    # insert right after the product's last existing group
    idxs = [gi for gi, g in enumerate(deck) if g.get('_product') == product]
    grp = {"platform": "End to End", "_product": product, "_appType": "End to End", "viewport": "mobile",
           "kicker": kicker, "flows": [{"name": "End to End Flow", "slug": slug, "kicker": "Customer + Partner, in order",
           "blurb": "The whole journey across both apps, screen by screen, in the real sequence.", "steps": steps}]}
    deck.insert(idxs[-1] + 1, grp)
    return len(steps)

nb = add_e2e("Beagle revamp", "Beagle · end to end (both apps)", "bg-e2e", BEAGLE)
nt = add_e2e("Takeover revamp", "Takeover · end to end (both apps)", "tk-e2e", TAKEOVER)

slugs = [f['slug'] for g in deck for f in g['flows']]
dupes = {x for x in slugs if slugs.count(x) > 1}
assert not dupes, "dup slugs: %s" % dupes
new = h[:b] + json.dumps(deck, ensure_ascii=True) + h[i + 1:]
# make the composite index show the End to End app type
new = new.replace("var APPTYPES=['User App','Partner App'];",
                  "var APPTYPES=['User App','Partner App','End to End'];")
open(FN, "w", encoding="utf-8").write(new)
print("Beagle E2E: %d screens | Takeover E2E: %d screens | %.1f MB" % (nb, nt, len(new)/1024/1024))
