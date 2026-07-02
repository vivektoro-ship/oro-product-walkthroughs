#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
AD = os.path.join(HOME, "assets/beagle-admin")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-beagle-cx-walkthrough.html")
OUT = SRC

def A(fn): return os.path.join(AD, fn)

# ---- reuse existing groups verbatim; idempotent on Admin ----
src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
deck = [g for g in deck if g.get("platform") != "Admin"]
for g in deck:
    g.setdefault("viewport", "mobile")

# ---- Admin (Ops) desktop flows — third-person about Ops; internal terms fine ----
ADMIN = [
  {
    "name": "Browse gold loan visits", "slug": "admin-visits", "kicker": "Visits list",
    "blurb": "Ops finds any gold loan visit from the central list.",
    "steps": [
      ("ad-listing.png", "The visits list",
       "Ops opens the Visits list to find any gold loan visit, filtered by status — confirmed, assigned, in progress, completed, or cancelled — with search and filters by city, type, lender, date, and agent."),
    ],
  },
  {
    "name": "A visit through its lifecycle", "slug": "admin-lifecycle", "kicker": "Visit lifecycle",
    "blurb": "How a visit's detail page changes as it moves from planned to complete.",
    "steps": [
      ("ad-lc-01-planned.png", "Planned",
       "When a visit is planned, Ops sees the customer, branch, and time, and can assign partners to it."),
      ("ad-lc-02-starting.png", "Starting",
       "Once the partner starts the visit, the detail page shows it underway with its assigned partners."),
      ("ad-lc-03-in-progress.png", "In progress",
       "While the visit is active, Ops can watch the customer checks run and the loan progress in real time."),
      ("ad-lc-04-plan-pending.png", "Plan selection pending",
       "When the checks pass, the visit waits for the customer to choose their plan."),
      ("ad-lc-05-locked.png", "Locked",
       "Once the plan is locked, the visit and its loan details are fixed."),
      ("ad-lc-06-completed.png", "Completed",
       "A completed visit shows the finished gold loan visit end to end."),
      ("ad-lc-07-cancelled.png", "Cancelled",
       "A cancelled visit shows a red banner with who cancelled it and when — Ops can view the reason."),
    ],
  },
  {
    "name": "The full visit record", "slug": "admin-record", "kicker": "Visit tabs",
    "blurb": "The tabs that hold everything attached to a visit.",
    "steps": [
      ("ad-tab-01-attributions.png", "Attributions",
       "The Attributions tab shows who's credited for the visit — the calling, sales, and appraisal partners."),
      ("ad-tab-02-sales.png", "Sales details",
       "The Sales Visit Details tab carries the sales-specific information for the visit."),
      ("ad-tab-03-loan.png", "Loan details",
       "The Loan Details tab shows the linked gold loan and any personal loan — amounts, lender, gold weight, plan, and purpose. It appears once the visit is locked."),
    ],
  },
  {
    "name": "Act on a visit", "slug": "admin-actions", "kicker": "Visit actions",
    "blurb": "The write actions Ops can take, all sharing a confirm-then-success pattern.",
    "steps": [
      ("ad-act-01-dropdown.png", "Open the actions menu",
       "From a visit, Ops opens the actions menu to change the address, reassign the partner, change the branch, change the status, or edit the visit data."),
      ("ad-act-02-assign-partner.png", "Assign a partner",
       "Ops assigns the partner agents who'll handle the visit."),
      ("ad-act-03-change-address.png", "Change the visit address",
       "Ops updates where the visit will happen — the full address block."),
      ("ad-act-04-reassign-agent.png", "Reassign the partner",
       "Ops moves the visit to a different partner agent."),
      ("ad-act-05-change-branch.png", "Change the partner branch",
       "Ops switches the visit to a different partner branch."),
      ("ad-act-06-change-status.png", "Change the status",
       "Ops changes the visit's status; cancelling it requires picking one or more reasons."),
      ("ad-act-07-status-confirm.png", "Confirm the change",
       "Every write action asks Ops to confirm before it's applied."),
      ("ad-act-08-status-success.png", "Change applied",
       "On success, Ops sees a confirmation that the change is saved."),
      ("ad-act-09-edit-data.png", "Edit visit data",
       "Ops edits the visit's underlying data when something needs correcting."),
    ],
  },
  {
    "name": "Manage a release visit", "slug": "admin-release", "kicker": "Release visit",
    "blurb": "Where the customer's gold is returned — its own detail page and mail flow.",
    "steps": [
      ("ad-rel-01-planned.png", "Release planned",
       "Release visits — where the customer's gold is returned — have their own detail page, starting when the release is planned."),
      ("ad-rel-02-at-branch.png", "At the branch",
       "The visit updates once the customer reaches the branch for the release."),
      ("ad-rel-03-in-progress.png", "Release in progress",
       "While the release is underway, Ops sees the assigned partners and the release documents."),
      ("ad-rel-04-completed.png", "Release completed",
       "A completed release visit shows the customer's gold has been returned."),
      ("ad-rel-05-cancelled.png", "Release cancelled",
       "A cancelled release visit shows the cancellation along with its reason."),
      ("ad-rel-06-mail-open.png", "Send the release mail",
       "Ops can send the release mail to the bank from the actions menu."),
      ("ad-rel-07-mail-sent.png", "Mail sent",
       "On success, Ops sees that the release mail has been sent."),
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

deck.append({"platform": "Admin", "kicker": "Beagle · how Ops manages gold loan visits",
             "viewport": "desktop", "flows": admin_flows})

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_beagle.html")).read()
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
        print("   %-32s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
