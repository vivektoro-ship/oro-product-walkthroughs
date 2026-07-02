#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
AD = os.path.join(HOME, "assets/takeover-admin")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-takeover-cx-walkthrough.html")
OUT = SRC

def A(fn): return os.path.join(AD, fn)

src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
deck = [g for g in deck if g.get("platform") != "Admin"]
for g in deck:
    g.setdefault("viewport", "mobile")

ADMIN = [
  {
    "name": "Find a takeover visit", "slug": "tkad-visits", "kicker": "Visits list",
    "blurb": "Ops finds any takeover (bridge loan) visit from the central list.",
    "steps": [
      ("ad-listing.png", "The visits list",
       "Ops opens the Visits list to find any takeover visit, filtered by status — confirmed, assigned, in progress, completed, or cancelled — with search and filters by city, type, lender, date, and agent."),
    ],
  },
  {
    "name": "A visit through its lifecycle", "slug": "tkad-lifecycle", "kicker": "Visit lifecycle",
    "blurb": "How a visit's detail page changes as it moves from planned to the release scheduled.",
    "steps": [
      ("ad-lc-01-planned.png", "Planned",
       "When a visit is planned, Ops sees the customer, address, and bridge-loan details, and can assign partners."),
      ("ad-lc-02-assigned.png", "Assigned & started",
       "With partners assigned and the visit started, Ops sees who's handling it."),
      ("ad-lc-03-partner-arrived.png", "Partner arrived",
       "Once the partner reaches the customer, the visit moves forward."),
      ("ad-lc-04-liveliness.png", "Checks in progress",
       "While the visit runs, Ops watches each check in real time — partner presence, onboarding, the customer's liveliness check, and more."),
      ("ad-lc-05-pc-submission.png", "Pledge cards going in",
       "Ops sees the customer's pledge cards being submitted for the takeover."),
      ("ad-lc-06-feasibility.png", "Feasibility checks",
       "The feasibility checks run against the customer before the loan is built."),
      ("ad-lc-07-pc-submitted.png", "Pledge cards submitted",
       "All pledge cards are submitted and ready."),
      ("ad-lc-08-brl-approved.png", "Bridge loan approved",
       "The bridge loan is approved — next the customer signs."),
      ("ad-lc-09-esign-complete.png", "Signing complete",
       "Both the customer and any co-borrower have signed."),
      ("ad-lc-10-fund-complete.png", "Funds transferred",
       "The bridge loan funds have been transferred to the customer."),
      ("ad-lc-11-proof-pending.png", "Awaiting payment proof",
       "Ops waits for proof that the customer's old loan has been paid off."),
      ("ad-lc-12-proof-submitted.png", "Payment proof submitted",
       "The payment proof is submitted for review."),
      ("ad-lc-13-proof-approved.png", "Payment proof approved",
       "The payment proof is approved — the existing loan is settled."),
      ("ad-lc-14-elr-scheduled.png", "Release visits scheduled",
       "The release visits are scheduled; Ops can track the gold custody as each one completes."),
    ],
  },
  {
    "name": "The full visit record", "slug": "tkad-record", "kicker": "Visit tabs",
    "blurb": "The tabs that hold everything attached to a takeover visit.",
    "steps": [
      ("ad-tab-01-visit-details.png", "Visit details",
       "The Visit Details tab shows everything about the visit — customer, address, bridge-loan info, and the live progress."),
      ("ad-tab-02-attributions.png", "Attributions",
       "The Attributions tab shows who's credited — the calling, sales, and appraisal partners."),
      ("ad-tab-03-sales.png", "Sales details",
       "The Sales Visit Details tab carries the sales-specific information for the visit."),
      ("ad-tab-04-loan.png", "Loan details",
       "The Loan Details tab shows the customer's gold loan and the bridge loan — amounts, lender, plan, pledge cards, and gold weight."),
    ],
  },
  {
    "name": "Act on a visit", "slug": "tkad-actions", "kicker": "Visit actions",
    "blurb": "The actions Ops can take on a takeover visit.",
    "steps": [
      ("ad-act-01-assign-partner.png", "Assign a partner",
       "Ops assigns the partner agents who'll handle the visit."),
      ("ad-act-02-options-menu.png", "Open the actions menu",
       "From the actions menu, Ops can change the address, reassign the agent, reschedule, change the bridge-loan lender, change the status, or link an offer or loan."),
      ("ad-act-03-change-address.png", "Change the visit address",
       "Ops updates where the visit will happen."),
      ("ad-act-04-change-lender.png", "Change the bridge-loan lender",
       "Ops switches the bridge loan to a different lender."),
      ("ad-act-05-link-offer.png", "Link an offer",
       "Ops links the visit to the customer's offer."),
      ("ad-act-06-link-loan.png", "Link a loan",
       "Ops links the visit to a loan record."),
      ("ad-act-07-change-status.png", "Change the status",
       "Ops changes the visit's status from the status panel."),
      ("ad-act-08-status-cancelled.png", "Cancel with a reason",
       "Cancelling a visit requires picking a reason — like a doubtful or fraudulent customer."),
    ],
  },
  {
    "name": "Track the release visits", "slug": "tkad-elr", "kicker": "Release visits",
    "blurb": "The Existing Lender Release (ELR) visits that collect the customer's gold from their old lender.",
    "steps": [
      ("ad-elr-01.png", "The release visits",
       "Once the bridge loan is paid out, Ops tracks the Existing Lender Release visits — collecting the customer's gold from their old lender — and where the gold currently sits."),
      ("ad-elr-02.png", "Manage a release visit",
       "Ops can reschedule a release visit from its menu if the timing needs to change."),
      ("ad-elr-03.png", "Reschedule",
       "Ops picks a new date, time, and address for the release visit."),
      ("ad-elr-04.png", "Rescheduled",
       "The release visit is rescheduled."),
      ("ad-elr-05.png", "Release visit progress",
       "Ops can open a release visit's progress — partner presence, gold images, and where the gold goes next, like storage at a cluster office."),
    ],
  },
  {
    "name": "Storage & retrieval visits", "slug": "tkad-storage", "kicker": "Storage visits",
    "blurb": "Where the customer's released gold is stored, retrieved, and transferred.",
    "steps": [
      ("ad-tsv-01.png", "Storage visits (TSV)",
       "The storage-visit tab tracks where the customer's gold is held — with location verification, gold images, locker number, and item count."),
      ("ad-trv-01.png", "Transfer / retrieval (TRV)",
       "A transfer-and-retrieval visit shows the gold being moved or handed over, in progress."),
    ],
  },
]

admin_flows = []
n = 0
for fl in ADMIN:
    steps = []
    for fn, title, caption in fl["steps"]:
        with open(A(fn), "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode("ascii")
        steps.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})
        n += 1
    admin_flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                        "blurb": fl["blurb"], "steps": steps})

deck.append({"platform": "Admin", "kicker": "Takeover · how Ops manages the visits",
             "viewport": "desktop", "flows": admin_flows})

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_takeover.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
with open(OUT, "w") as f:
    f.write(html)

total = sum(len(f["steps"]) for g in deck for f in g["flows"])
print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", total, "| admin added:", n)
for grp in deck:
    gs = sum(len(f["steps"]) for f in grp["flows"])
    print("\n== %s == [%s] (%d flows, %d screens)" % (grp["platform"], grp.get("viewport"), len(grp["flows"]), gs))
    for f in grp["flows"]:
        print("   %-34s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
