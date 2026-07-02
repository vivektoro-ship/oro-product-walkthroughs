#!/usr/bin/env python3
import json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
OUT = os.path.join(HOME, "oro-universal-takeover-walkthrough.html")

def lookup(fname):
    """All flows across ALL groups of a source deck, keyed by slug (base64 reused verbatim)."""
    deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', open(os.path.join(HOME, fname)).read(), re.S).group(1))
    return {fl["slug"]: fl for g in deck for fl in g["flows"]}

T = lookup("oro-takeover-cx-walkthrough.html")
E = lookup("oro-elr-cx-walkthrough.html")
B = lookup("oro-beagle-cx-walkthrough.html")
SRC = {"T": T, "E": E, "B": B}

def step(deck, slug, idx, actor):
    s = SRC[deck][slug]["steps"][idx]
    return {"img": s["img"], "title": s["title"], "caption": s["caption"],
            "actor": actor, "viewport": ("desktop" if actor == "Admin" else "mobile")}

# ---- the universal cross-actor chronology (Customer / Admin / Partner interleaved in event order) ----
PHASE1 = [  # Bridge loan
  ("T","takeover-book",3,"Customer"),       # customer requests / books the BRL visit
  ("T","tkad-lifecycle",0,"Admin"),         # it lands in admin, planned
  ("T","tkad-actions",0,"Admin"),           # admin assigns a partner
  ("T","takeover-visit",1,"Customer"),      # customer sees the partner assigned
  ("T","tk-px-start",0,"Partner"),          # partner opens the visit
  ("T","tk-px-start",2,"Partner"),          # partner verifies location / starts
  ("T","tk-px-verify",2,"Partner"),         # partner verifies the customer
  ("T","takeover-visit",4,"Customer"),      # customer: verified
  ("T","takeover-verify",2,"Customer"),     # customer: lender KYC done
  ("T","tk-px-pledge",3,"Partner"),         # partner captures the pledge card
  ("T","tk-px-pledge",5,"Partner"),         # partner confirms the release amount
  ("T","takeover-setup",6,"Customer"),      # customer chooses a plan
  ("T","takeover-setup",7,"Customer"),      # customer confirms the plan
  ("T","tk-px-approval",0,"Partner"),       # partner submits for approval
  ("T","tkad-loan-lifecycle",0,"Admin"),    # admin: bridge loan pending approval
  ("T","tkad-loan-lifecycle",3,"Admin"),    # admin: bridge loan approved
  ("T","takeover-sign",0,"Customer"),       # customer starts signing
  ("T","takeover-sign",2,"Customer"),       # customer has signed
  ("T","tk-px-funds",3,"Partner"),          # partner disburses the bridge loan
  ("T","takeover-sign",4,"Customer"),       # customer: money transferred
  ("T","takeover-sign",6,"Customer"),       # customer: old loan closed
  ("T","tk-px-proof",3,"Partner"),          # partner proves the old loan is paid
  ("T","tkad-loan-proof",0,"Admin"),        # admin reviews the release payment proofs
  ("T","tk-px-release",3,"Partner"),        # partner schedules the release visit
]
PHASE2 = [  # Existing Lender Release
  ("E","elr-find",0,"Customer"),            # customer follows the release
  ("E","elr-px-collect",0,"Partner"),       # partner opens the release visit
  ("E","elr-px-collect",2,"Partner"),       # partner collects the released gold
  ("E","elr-px-collect",6,"Partner"),       # partner creates a storage visit
  ("E","elr-track",0,"Customer"),           # customer: release in progress
  ("E","elr-track",1,"Customer"),           # customer: release completed
  ("E","elr-px-store",0,"Partner"),         # partner at the cluster office
  ("E","elr-px-store",2,"Partner"),         # partner verifies the staff
  ("E","elr-px-store",5,"Partner"),         # partner hands over the gold
  ("E","elr-px-co-store",4,"Partner"),      # cluster-office staff stores the gold
  ("E","elr-px-co-store",5,"Partner"),      # cluster-office staff: gold stored
  ("E","elr-track",3,"Customer"),           # customer: safely stored
  ("T","tkad-elr",0,"Admin"),               # admin tracks the release visits
  ("E","elr-px-retrieve",0,"Partner"),      # partner returns to retrieve
  ("E","elr-px-co-handback",4,"Partner"),   # cluster-office staff hands gold back
  ("E","elr-px-retrieve",5,"Partner"),      # partner: gold collected
  ("E","elr-track",6,"Customer"),           # customer: gold retrieved
  ("E","elr-px-schedule",3,"Partner"),      # partner books the gold-loan visit
  ("E","elr-track",7,"Customer"),           # customer: loan visit scheduled
]
PHASE3 = [  # Gold loan
  ("B","beagle-get-loan",0,"Customer"),     # customer at the gold-loan visit
  ("B","px-start-visit",0,"Partner"),       # partner opens the GL visit
  ("B","px-start-visit",4,"Partner"),       # partner verified at the branch
  ("B","beagle-get-loan",3,"Customer"),     # customer checked in
  ("B","beagle-get-loan",4,"Customer"),     # customer identity verified
  ("B","px-verify-customer",1,"Partner"),   # partner verifies identity
  ("B","beagle-get-loan",8,"Customer"),     # customer: gold valued
  ("B","beagle-get-loan",9,"Customer"),     # customer chooses a plan
  ("B","beagle-get-loan",10,"Customer"),    # customer confirms the plan
  ("B","px-plan",2,"Partner"),              # partner confirms the plan
  ("B","admin-lifecycle",2,"Admin"),        # admin: GL visit in progress
  ("B","px-submit",2,"Partner"),            # partner submits for approval
  ("B","beagle-get-loan",15,"Customer"),    # customer signs
  ("B","beagle-get-loan",18,"Customer"),    # customer: loan approved
  ("B","px-disbursal",4,"Partner"),         # partner: funds transferred
  ("B","beagle-get-loan",20,"Customer"),    # customer: money on its way
  ("B","admin-lifecycle",5,"Admin"),        # admin: GL visit completed
  ("B","beagle-manage",1,"Customer"),       # customer manages the new Oro loan
]

PHASES = [
  {"name":"1 · Bridge loan","slug":"u-bridge-loan","kicker":"Bridge loan",
   "blurb":"Oro arranges a short-term bridge loan and pays off the old lender — followed across the customer, admin, and partner as each hands off to the next.",
   "seq":PHASE1},
  {"name":"2 · Release the gold","slug":"u-release","kicker":"Release",
   "blurb":"With the old loan settled, the partner releases the gold, stores it at a cluster office and retrieves it — while the customer watches and admin tracks.",
   "seq":PHASE2},
  {"name":"3 · Gold loan","slug":"u-gold-loan","kicker":"Gold loan",
   "blurb":"The fresh Oro gold loan against the released gold — customer, partner, and admin together complete the move.",
   "seq":PHASE3},
]

flows = []
n = 0
for ph in PHASES:
    steps = [step(*ref) for ref in ph["seq"]]
    n += len(steps)
    flows.append({"name":ph["name"],"slug":ph["slug"],"kicker":ph["kicker"],"blurb":ph["blurb"],"steps":steps})

deck = [{"platform":"Universal Journey","kicker":"Customer · Admin · Partner, in event order",
         "viewport":"mobile","flows":flows}]

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH,"fonts.css")).read()
template = open(os.path.join(SCRATCH,"template_universal.html")).read()
html = template.replace("/*__FONTS__*/",fonts_css).replace("__DECK__",deck_json)
open(OUT,"w").write(html)

print("WROTE",OUT)
print("size MB: %.2f"%(os.path.getsize(OUT)/1024/1024))
print("total screens:",n)
for fl in flows:
    actors=[s['actor'][0] for s in fl['steps']]
    print("  %-22s %2d  [%s]  %s"%(fl['name'],len(fl['steps']),fl['slug'],"".join(actors)))
