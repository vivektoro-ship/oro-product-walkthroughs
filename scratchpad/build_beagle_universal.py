#!/usr/bin/env python3
import json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
OUT = os.path.join(HOME, "oro-beagle-universal-walkthrough.html")

deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', open(os.path.join(HOME,"oro-beagle-cx-walkthrough.html")).read(), re.S).group(1))
BG = {fl["slug"]: fl for g in deck for fl in g["flows"]}

def step(slug, idx, actor):
    s = BG[slug]["steps"][idx]
    return {"img": s["img"], "title": s["title"], "caption": s["caption"],
            "actor": actor, "viewport": ("desktop" if actor == "Admin" else "mobile")}

# ---- chronological cross-actor gold-loan journey ----
PHASE1 = [  # Book & start the visit
  ("beagle-book-visit",2,"Customer"),   # customer picks a branch
  ("beagle-book-visit",4,"Customer"),   # customer: visit booked
  ("admin-lifecycle",0,"Admin"),        # it lands in admin, planned
  ("admin-actions",1,"Admin"),          # admin assigns a partner
  ("beagle-get-loan",0,"Customer"),     # customer: start the visit
  ("px-start-visit",0,"Partner"),       # partner opens the visit
  ("px-start-visit",4,"Partner"),       # partner verified at the branch
  ("beagle-get-loan",3,"Customer"),     # customer checked in
  ("admin-lifecycle",1,"Admin"),        # admin: visit starting
]
PHASE2 = [  # Verify & value the gold
  ("px-verify-customer",0,"Partner"),   # partner takes consent
  ("beagle-get-loan",4,"Customer"),     # customer identity verified
  ("px-verify-customer",4,"Partner"),   # partner runs the checks
  ("admin-lifecycle",2,"Admin"),        # admin: in progress
  ("beagle-get-loan",8,"Customer"),     # customer: gold valued
  ("px-plan",0,"Partner"),              # partner shows the plans
  ("beagle-get-loan",9,"Customer"),     # customer chooses a plan
  ("beagle-get-loan",10,"Customer"),    # customer confirms
  ("px-plan",2,"Partner"),              # partner confirms the plan
  ("admin-lifecycle",3,"Admin"),        # admin: plan selection pending
]
PHASE3 = [  # Approve, sign & disburse
  ("beagle-get-loan",11,"Customer"),    # customer picks bank account
  ("beagle-get-loan",13,"Customer"),    # customer: loan purpose
  ("px-submit",2,"Partner"),            # partner submits for approval
  ("beagle-get-loan",15,"Customer"),    # customer signs
  ("beagle-get-loan",16,"Customer"),    # customer has signed
  ("px-disbursal",0,"Partner"),         # partner: waiting for approval
  ("admin-lifecycle",4,"Admin"),        # admin: visit locked / loan approved
  ("beagle-get-loan",18,"Customer"),    # customer: loan approved
  ("px-disbursal",3,"Partner"),         # partner: money transfer underway
  ("admin-queue-api",0,"Admin"),        # if a post-approval step fails, it lands in a queue
  ("admin-queue-api",3,"Admin"),        # admin triggers the automation to resume
  ("admin-queue-api",5,"Admin"),        # admin: resolved
  ("px-disbursal",4,"Partner"),         # partner: funds transferred
  ("beagle-get-loan",20,"Customer"),    # customer: money on its way
  ("admin-lifecycle",5,"Admin"),        # admin: visit completed
  ("beagle-manage",1,"Customer"),       # customer manages the new loan
]

PHASES = [
  {"name":"1 · Book & start the visit","slug":"gl-book","kicker":"Book & start",
   "blurb":"The customer books a gold-loan visit, it reaches admin, a partner is assigned and starts the visit at the branch.",
   "seq":PHASE1},
  {"name":"2 · Verify & value the gold","slug":"gl-verify","kicker":"Verify & value",
   "blurb":"The partner verifies the customer, the gold is valued, and a plan is chosen and confirmed — with admin tracking throughout.",
   "seq":PHASE2},
  {"name":"3 · Approve, sign & disburse","slug":"gl-disburse","kicker":"Approve & disburse",
   "blurb":"The loan is submitted, approved and signed, then disbursed — including how admin clears a stuck fund transfer from the queue.",
   "seq":PHASE3},
]

flows=[]; n=0
for ph in PHASES:
    steps=[step(*r) for r in ph["seq"]]; n+=len(steps)
    flows.append({"name":ph["name"],"slug":ph["slug"],"kicker":ph["kicker"],"blurb":ph["blurb"],"steps":steps})

out_deck=[{"platform":"Universal Journey","kicker":"Customer · Admin · Partner, in event order","viewport":"mobile","flows":flows}]
deck_json=json.dumps(out_deck, ensure_ascii=True)
fonts_css=open(os.path.join(SCRATCH,"fonts.css")).read()
template=open(os.path.join(SCRATCH,"template_beagle_universal.html")).read()
open(OUT,"w").write(template.replace("/*__FONTS__*/",fonts_css).replace("__DECK__",deck_json))

print("WROTE",OUT); print("size MB: %.2f"%(os.path.getsize(OUT)/1024/1024)); print("total screens:",n)
for fl in flows:
    print("  %-26s %2d  [%s]  %s"%(fl['name'],len(fl['steps']),fl['slug'],"".join(s['actor'][0] for s in fl['steps'])))
