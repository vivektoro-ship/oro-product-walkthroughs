#!/usr/bin/env python3
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
E = os.path.join(HOME, "assets/elr")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
OUT = os.path.join(HOME, "oro-elr-cx-walkthrough.html")

def F(fn): return os.path.join(E, fn)

FLOWS = [
  {
    "name": "Find your release", "slug": "elr-find", "kicker": "Your release",
    "blurb": "Open your Existing Lender Release and see the visit at a glance.",
    "steps": [
      ("e1-01-home.png", "Open your release",
       "On the home screen, open your Existing Lender Release to follow your gold being moved over to Oro."),
      ("e1-02-visits-list.png", "Your release visits",
       "See your release visits — each shows the lender and date. Tap one to follow it."),
      ("e1-03-visit-summary.png", "Visit summary",
       "See the visit at a glance — your old lender, the date, the partner helping you, your pledge cards, gold weight, and release amount."),
    ],
  },
  {
    "name": "See what's being released", "slug": "elr-items", "kicker": "Your gold",
    "blurb": "The pledge cards and gold being released — and where it's held.",
    "steps": [
      ("e2-01-pledge-cards.png", "Your pledge cards",
       "See the pledge cards being released — each card's lender, gold weight, and the amount being settled."),
      ("e2-02-gold-details.png", "Your gold details",
       "Check the details of your gold being held — its weight and photos. Your gold stays safe with Oro."),
    ],
  },
  {
    "name": "Track your gold", "slug": "elr-track", "kicker": "Track your gold",
    "blurb": "Follow your gold from your old lender, into safe storage, and back.",
    "steps": [
      ("e3-01-release-in-progress.png", "Release in progress",
       "Your gold at your old lender is being released. You can follow along here."),
      ("e3-02-release-completed.png", "Release completed",
       "Your gold has been released from your old lender."),
      ("e3-03-storage-in-progress.png", "Moving to safe storage",
       "Your gold is being moved for safe-keeping to the nearest Oro Cluster Office."),
      ("e3-04-storage-completed.png", "Safely stored",
       "Your gold is now stored securely at the nearest Oro Cluster Office."),
      ("e3-05-cluster-office.png", "Where your gold is",
       "See exactly where your gold is kept — the Oro Cluster Office, with its address and your gold's weight."),
      ("e3-06-retrieval-in-progress.png", "Retrieving your gold",
       "Your gold is being retrieved from the Oro Cluster Office."),
      ("e3-07-retrieval-completed.png", "Gold retrieved",
       "Your gold has been retrieved — your loan process will begin shortly."),
      ("e3-08-gl-visit-scheduled.png", "Loan visit scheduled",
       "Your gold loan visit with Oro is scheduled — tap to see the details and finish your loan."),
    ],
  },
]

flows = []
n = 0
for fl in FLOWS:
    steps = []
    for fn, title, caption in fl["steps"]:
        with open(F(fn), "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode("ascii")
        steps.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})
        n += 1
    flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                  "blurb": fl["blurb"], "steps": steps})

deck = [{"platform": "Customer App", "kicker": "ELR · following your gold release",
         "viewport": "mobile", "flows": flows}]

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_elr.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
open(OUT, "w").write(html)

print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", n)
for fl in flows:
    print("  %-26s %2d  [%s]" % (fl["name"], len(fl["steps"]), fl["slug"]))
