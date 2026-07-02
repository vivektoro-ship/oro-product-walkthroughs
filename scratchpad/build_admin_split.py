#!/usr/bin/env python3
"""Split the Admin Loan Flows products into sub-flows and add queue/release/excess/
other flows pulled from oro-all-flows. Reuses already-embedded step images.
Beagle -> Gold Loan flow / Atlas queues / Release.
BRL    -> Approval / BRL Payment proof approval / Excess or shortfall / Other details."""
import json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_FN = os.path.join(HOME, "oro-admin-loan-flows-walkthrough.html")
ALL = os.path.join(HOME, "oro-all-flows-walkthrough.html")

def load(fn):
    h = open(fn, encoding="utf-8").read()
    s = h.index('const DECK'); b = h.index('[', s); d = 0
    for i in range(b, len(h)):
        if h[i] == '[': d += 1
        elif h[i] == ']':
            d -= 1
            if d == 0: break
    return h, b, i + 1, json.loads(h[b:i + 1])

# --- pull reusable flows (with embedded images) from all-flows, by slug ---
_, _, _, alld = load(ALL)
flow_by_slug = {f['slug']: f for g in alld for f in g['flows']}
def grab(slug):
    return json.loads(json.dumps(flow_by_slug[slug]))  # deep copy

q_api = grab('admin-queue-api'); q_funds = grab('admin-queue-funds')
release = grab('admin-release')
excess = grab('tkadl-excess'); other = grab('tkadl-record')

# --- current admin deck (single flows already embedded) ---
h, b, e, deck = load(DECK_FN)
beagle_gi = next(i for i, g in enumerate(deck) if g.get('_product') == 'Beagle')
brl_gi = next(i for i, g in enumerate(deck) if str(g.get('_product')).startswith('Takeover'))
beagle_steps = deck[beagle_gi]['flows'][0]['steps']     # 30
brl_steps = deck[brl_gi]['flows'][0]['steps']           # 24

def flow(name, slug, kicker, steps):
    return {"name": name, "slug": slug, "kicker": kicker, "blurb": "", "steps": steps}

# Beagle: gold loan + atlas queues (both queue scenarios combined) + release
atlas_steps = q_api['steps'] + q_funds['steps']
deck[beagle_gi]['flows'] = [
    flow("Gold Loan flow", "bg-gold-loan", "Beagle admin · gold loan", beagle_steps),
    flow("Atlas queues", "bg-atlas-queues", "Beagle admin · Atlas queues", atlas_steps),
    flow("Release", "bg-release", "Beagle admin · release", release['steps']),
]

# BRL: approval (0-15) / payment-proof approval (16-23) / excess / other
deck[brl_gi]['flows'] = [
    flow("Approval", "tk-approval", "BRL admin · approval", brl_steps[:16]),
    flow("BRL Payment proof approval", "tk-pp-approval", "BRL admin · payment proof", brl_steps[16:]),
    flow("Excess or shortfall", "tk-excess", "BRL admin · excess/shortfall", excess['steps']),
    flow("Other details", "tk-other", "BRL admin · other", other['steps']),
]

slugs = [f['slug'] for g in deck for f in g['flows']]
dupes = {x for x in slugs if slugs.count(x) > 1}
assert not dupes, "dup slugs: %s" % dupes
open(DECK_FN, "w", encoding="utf-8").write(h[:b] + json.dumps(deck, ensure_ascii=True) + h[e:])
print("rebuilt | %.1f MB" % (os.path.getsize(DECK_FN)/1024/1024))
for gi in (beagle_gi, brl_gi):
    g = deck[gi]; print(f"\n{g['_product']}:")
    for f in g['flows']: print("   [%s] %s (%d)" % (f['slug'], f['name'], len(f['steps'])))
