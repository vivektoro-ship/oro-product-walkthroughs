#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
Q = os.path.join(HOME, "assets/beagle-queues")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-beagle-cx-walkthrough.html")
OUT = SRC

def Q_(fn): return os.path.join(Q, fn)

src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
for g in deck:
    g.setdefault("viewport", "mobile")

QUEUE_FLOWS = [
  {
    "name": "Queues — fix a lender API failure", "slug": "admin-queue-api", "kicker": "Queues · API failure",
    "blurb": "How Tech Support clears a loan stuck on a Federal Bank API failure after approval.",
    "steps": [
      ("q1-01-listing.png", "The Atlas Queues list",
       "Atlas Queues is where a loan lands when an automated step fails after approval — one loan's hold-up never blocks another. The GL API Failure queue, owned by Tech Support, lists each stuck loan with its issue, lender, customer, and how long it's waited."),
      ("q1-02-claim.png", "Claim the item",
       "Opening an item shows exactly where the automation paused and the error behind it. The owner marks it as Fix in progress to take it on — only one person can hold an item at a time."),
      ("q1-03-fix-in-progress.png", "Working on it",
       "Once claimed, the item shows who's working on it, and the Trigger Automation action becomes available."),
      ("q1-04-trigger-automation.png", "Trigger the automation",
       "After the underlying issue is sorted, the owner triggers the automation to resume — it picks up at the exact failed step and never re-runs steps already done. Who triggered it and when is recorded."),
      ("q1-05-retrying.png", "Retrying",
       "The system retries the failed step; the item shows as retrying."),
      ("q1-06-resolved.png", "Resolved",
       "On success the issue is resolved and Atlas automation continues from the next step — the loan leaves the queue."),
    ],
  },
  {
    "name": "Queues — fix a stuck fund transfer", "slug": "admin-queue-funds", "kicker": "Queues · fund transfer",
    "blurb": "How Loan Ops clears a loan whose money transfer failed or didn't validate.",
    "steps": [
      ("q2-01-listing.png", "The fund-transfer queue",
       "The GL Fund Transfer Pending queue, owned by Loan Ops, collects loans where the money transfer failed or didn't validate."),
      ("q2-02-detail.png", "Open the item",
       "Opening an item shows the reasons the transfer failed and the bank account it was going to — along with the actions to fix it."),
      ("q2-03-change-bank.png", "Switch the bank account",
       "If the account is the problem, the operator can switch the customer to one of their other accounts, or add a new one."),
      ("q2-04-bank-changed.png", "New account set",
       "The chosen account is now set on the loan, ready for another attempt."),
      ("q2-06-trigger-ft.png", "Trigger the transfer",
       "The operator triggers the fund transfer again, confirming the loan amount; the button locks while it runs so it can't be fired twice."),
      ("q2-07-initiated.png", "Transfer re-initiated",
       "The transfer is re-initiated and, on success, the automation resumes."),
      ("q2-08-rejected.png", "Auto-rejected",
       "If the loan or visit is cancelled upstream, the item is auto-rejected by the system with the reason — operators never reject items by hand."),
    ],
  },
]

def build_flows(specs):
    out = []
    n = 0
    for fl in specs:
        steps = []
        for fn, title, caption in fl["steps"]:
            with open(Q_(fn), "rb") as fp:
                b64 = base64.b64encode(fp.read()).decode("ascii")
            steps.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})
            n += 1
        out.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                    "blurb": fl["blurb"], "steps": steps})
    return out, n

queue_flows, n = build_flows(QUEUE_FLOWS)

admin = next(g for g in deck if g.get("platform") == "Admin")
# idempotent: drop any previously-added queue flows, then append
admin["flows"] = [f for f in admin["flows"] if not f["slug"].startswith("admin-queue-")]
admin["flows"].extend(queue_flows)

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_beagle.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
with open(OUT, "w") as f:
    f.write(html)

total = sum(len(f["steps"]) for g in deck for f in g["flows"])
print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", total, "| queue screens added:", n)
for grp in deck:
    gs = sum(len(f["steps"]) for f in grp["flows"])
    print("\n== %s == [%s] (%d flows, %d screens)" % (grp["platform"], grp.get("viewport"), len(grp["flows"]), gs))
    for f in grp["flows"]:
        print("   %-34s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
