#!/usr/bin/env python3
# Appends / refreshes the "What Changes" group (current live partner-app offer module)
# on oro-offer-walkthrough.html. Idempotent. Screens live in assets/offer-current/sel/
# (already padded with a top margin so they clear the phone-frame rounded corner).
import base64, json, os, re
SCRATCH = os.path.dirname(os.path.abspath(__file__))   # scratchpad/
HOME = os.path.dirname(SCRATCH)                         # handoff root
SEL  = os.path.join(HOME, "assets/offer-current/sel")
SRC  = os.path.join(HOME, "oro-offer-walkthrough.html")

def img(fn): return "data:image/png;base64,"+base64.b64encode(open(os.path.join(SEL,fn),"rb").read()).decode("ascii")

WC = [
 {"name":"Today: create a takeover offer","slug":"wc-takeover","kicker":"Current · takeover",
  "blurb":"The current live partner-app takeover offer — a single manual form — and what the revamp changes.",
  "steps":[
   ("c-09_30-21507.png","Start by adding a pledge card","Today, the agent adds a pledge card by choosing the lender and typing every field by hand. What changes: capture the card with the camera and the app reads the details for you."),
   ("c-06_30-22224.png","Type in every field","Today, gross weight, stone deduction, net weight, card number and release amount are all keyed in manually — no photo read. What changes: these auto-fill from the card and are only reviewed."),
   ("c-01_28-12924.png","Generate the offer","Today, one long form lists the cards with a free-text comment and generates the offer in a single step. What changes: a guided, step-by-step flow with a clear pledge-card list."),
   ("c-02_29-17484.png","Edit cards inline","Today, cards are edited or removed inline on the same form. What changes: dedicated steps to view, edit, add, or import pledge cards."),
  ]},
 {"name":"Today: create a fresh offer","slug":"wc-fresh","kicker":"Current · fresh",
  "blurb":"The current live fresh-offer form, and what the revamp changes.",
  "steps":[
   ("c-04_29-19043.png","Enter customer & gold details","Today, for a fresh loan the agent types the customer and gold details — weight, purity, carats — on a single form. What changes: a guided fresh-offer flow with loan-basis and plan selection."),
   ("c-05_29-19082.png","Upload gold photos","Today, gold photos are uploaded manually here. What changes: guided capture with clearer prompts."),
   ("c-03_29-18623.png","Offer created","Today, a simple success screen with 'View Offer Image'. What changes: the offer opens directly, ready to share or modify."),
  ]},
]
flows=[]; n=0
for fl in WC:
    steps=[{"img":img(fn),"title":t,"caption":c} for fn,t,c in fl["steps"]]; n+=len(steps)
    flows.append({"name":fl["name"],"slug":fl["slug"],"kicker":fl["kicker"],"blurb":fl["blurb"],"steps":steps})
group={"platform":"What Changes","kicker":"Current partner app · before the revamp","viewport":"mobile","flows":flows}
html=open(SRC).read()
deck=json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);',html,re.S).group(1))
deck=[g for g in deck if g.get("platform")!="What Changes"]     # idempotent
deck.append(group)
nj=json.dumps(deck, ensure_ascii=True)
open(SRC,"w").write(re.sub(r'const DECK\s*=\s*\[.*?\];', lambda _:'const DECK = '+nj+';', html, count=1, flags=re.S))
print("What Changes refreshed:", n, "screens")
