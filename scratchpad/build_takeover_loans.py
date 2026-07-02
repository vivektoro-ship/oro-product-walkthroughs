#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
L = os.path.join(HOME, "assets/takeover-loans")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-takeover-cx-walkthrough.html")
OUT = SRC

def F(fn): return os.path.join(L, fn)

src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
for g in deck:
    g.setdefault("viewport", "mobile")

LOANS = [
  {
    "name": "A bridge loan through its lifecycle", "slug": "tkad-loan-lifecycle", "kicker": "Loan lifecycle",
    "blurb": "How a bridge loan's detail page moves from pending approval to live.",
    "steps": [
      ("l1-01-pending-approval.png", "Pending approval",
       "A new bridge loan opens pending approval — Ops reviews the release amount, pledge cards, gold weight, and co-borrower before approving."),
      ("l1-02-pledge-cards.png", "Review the pledge cards",
       "Ops checks each pledge card — gold weight, purity deduction, net weight, and the amount to release to the old lender."),
      ("l1-03-approve-panel.png", "Approve the loan",
       "Ops approves the bridge loan, confirming the plan, amount, and the account it pays into."),
      ("l1-05-brl-approved.png", "Loan approved",
       "The bridge loan is approved."),
      ("l1-06-cx-esign.png", "Customer signs",
       "Ops can see the customer's e-sign status on the loan."),
      ("l1-07-pending-fund.png", "Pending fund transfer",
       "With signing done, the loan waits for the funds to transfer."),
      ("l1-08-fund-transferred.png", "Funds transferred",
       "The bridge loan amount is transferred, with the UTR numbers and bank details recorded."),
      ("l1-09-active.png", "Loan live",
       "The loan is live; Ops now waits for the release payment proofs from the field."),
    ],
  },
  {
    "name": "Review the release payment proofs", "slug": "tkad-loan-proof", "kicker": "Payment proof",
    "blurb": "Ops checks the proof that the customer's old loan was paid off.",
    "steps": [
      ("l2-01-proof-submitted.png", "Proofs submitted",
       "When the field uploads proof the old loan was paid off, Ops reviews each release payment proof against its pledge card."),
      ("l2-02-elr-all-pending.png", "Approve or reject each proof",
       "Ops opens each proof image and marks it approved or rejected."),
      ("l2-04-reject-reason.png", "Reject with a reason",
       "If a proof is unclear, Ops rejects it with a reason so the field can re-upload."),
      ("l2-05-proof-rejected.png", "Some proofs rejected",
       "Rejected proofs send the loan back for the field to fix and resubmit."),
    ],
  },
  {
    "name": "Commit the release & close the loan", "slug": "tkad-loan-commit", "kicker": "Release & close",
    "blurb": "Releasing the amount once proofs are approved, then closing the bridge loan.",
    "steps": [
      ("l3-01-ready-to-commit.png", "Ready to commit",
       "Once every proof is approved, Ops can complete the review and release the amount."),
      ("l3-02-commit-confirm.png", "Confirm the release",
       "Ops confirms before committing the release."),
      ("l3-03-commit-success.png", "Release committed",
       "The release is committed."),
      ("l3-04-post-commit.png", "Loan closed",
       "The bridge loan is closed; any excess amount is transferred back to the customer."),
      ("l3-05-excess-complete.png", "Excess returned",
       "The excess transfer to the customer is complete, with its own transfer details."),
    ],
  },
  {
    "name": "The full loan record", "slug": "tkad-loan-record", "kicker": "Loan tabs",
    "blurb": "The tabs that hold everything attached to a bridge loan.",
    "steps": [
      ("l4-01-default.png", "Loan details",
       "The loan detail page shows the bridge loan — amount, plan, lender, pledge cards, and the linked visit."),
      ("l4-02-with-kfs.png", "Loan documents",
       "The Loan Docs tab holds the loan's documents — the key facts statement, annexures, and forms — in the customer's language."),
      ("l4-03-elr-visits-tab.png", "Associated visits",
       "The Associated Visits tab links the loan to its sales, release (ELR), storage (TSV), and gold-loan visits."),
      ("l4-04-cancelled.png", "Cancelled loan",
       "A cancelled bridge loan shows its cancelled state."),
    ],
  },
  {
    "name": "Act on a loan", "slug": "tkad-loan-actions", "kicker": "Loan actions",
    "blurb": "The actions Ops can take on a bridge loan.",
    "steps": [
      ("l5-01-dropdown.png", "Open the actions menu",
       "From the loan's menu, Ops can change its status, edit the transfer UTR, or change the start date."),
      ("l5-02-change-status.png", "Change the status",
       "Ops changes the loan's status from the status panel."),
      ("l5-03-status-success.png", "Status changed",
       "On confirm, the loan's status is updated."),
      ("l5-04-edit-utr.png", "Edit the transfer UTR",
       "Ops corrects the fund-transfer UTR and mode, noting the reason for the activity log."),
      ("l5-05-change-start-date.png", "Change the start date",
       "Ops changes the loan's start date when needed."),
    ],
  },
]

def build(specs):
    out=[]; n=0
    for fl in specs:
        steps=[]
        for fn,title,caption in fl["steps"]:
            with open(F(fn),"rb") as fp:
                b64=base64.b64encode(fp.read()).decode("ascii")
            steps.append({"img":"data:image/png;base64,"+b64,"title":title,"caption":caption}); n+=1
        out.append({"name":fl["name"],"slug":fl["slug"],"kicker":fl["kicker"],"blurb":fl["blurb"],"steps":steps})
    return out,n

loan_flows,n = build(LOANS)

admin = next(g for g in deck if g.get("platform")=="Admin")
admin["kicker"] = "Takeover · how Ops manages visits & loans"
admin["flows"] = [f for f in admin["flows"] if not f["slug"].startswith("tkad-loan-")]
admin["flows"].extend(loan_flows)

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH,"fonts.css")).read()
template = open(os.path.join(SCRATCH,"template_takeover.html")).read()
html = template.replace("/*__FONTS__*/",fonts_css).replace("__DECK__",deck_json)
open(OUT,"w").write(html)

total=sum(len(f["steps"]) for g in deck for f in g["flows"])
print("WROTE",OUT)
print("size MB: %.2f"%(os.path.getsize(OUT)/1024/1024))
print("total screens:",total,"| loan screens added:",n)
for grp in deck:
    gs=sum(len(f["steps"]) for f in grp["flows"])
    print("\n== %s == [%s] (%d flows, %d screens)"%(grp["platform"],grp.get("viewport"),len(grp["flows"]),gs))
    for f in grp["flows"]:
        print("   %-36s %2d  [%s]"%(f["name"],len(f["steps"]),f["slug"]))
