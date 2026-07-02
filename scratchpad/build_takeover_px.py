#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
PX = os.path.join(HOME, "assets/takeover-px")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-takeover-cx-walkthrough.html")
OUT = SRC

def P(fn): return os.path.join(PX, fn)

src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
deck = [g for g in deck if g.get("platform") != "Partner App"]
for g in deck:
    g.setdefault("viewport", "mobile")

PARTNER = [
  {
    "name": "Start the visit", "slug": "tk-px-start", "kicker": "Visit start",
    "blurb": "Open the assigned visit and confirm you're at the right location.",
    "steps": [
      ("px1-01-home.png", "Open the assigned visit",
       "Open the visit assigned to you — you'll see each customer and whether their visit has started."),
      ("px1-02-location-verify.png", "Confirming your location",
       "We confirm you're at the right visit location before you begin."),
      ("px1-03-location-verified.png", "Location verified",
       "Your visit location is confirmed — you're ready to start with the customer."),
    ],
  },
  {
    "name": "Verify the customer", "slug": "tk-px-verify", "kicker": "Customer checks",
    "blurb": "Confirm the customer is present and run their verification.",
    "steps": [
      ("px2-01-onboarding-done.png", "Customer onboarded",
       "The customer has finished onboarding — you can move on to verifying them."),
      ("px2-02-cx-verify-1.png", "The visit journey",
       "Here's the visit's journey — verify the customer, their identity, the pledge card, get approval, sign, transfer funds, and submit proof. Tap to start."),
      ("px2-03-cx-verify-3.png", "Take the customer's photo",
       "Take a live photo of the customer at the visit to confirm it's them."),
      ("px2-04-silent-checks.png", "Running the checks",
       "We run the required checks on the customer in the background. Just a moment."),
    ],
  },
  {
    "name": "Customer details & eligibility", "slug": "tk-px-eligibility", "kicker": "Eligibility",
    "blurb": "Capture the customer's details and see which lenders they qualify with.",
    "steps": [
      ("px3-01-ekyc.png", "Verify their identity",
       "Enter the last digits of the customer's Aadhaar number to verify who they are."),
      ("px3-02-loan-purpose.png", "Capture their details",
       "Fill in the customer's remaining details and what the loan is for, then continue."),
      ("px3-03-precheck-results.png", "Pre-check results",
       "See the pre-check results — which checks passed and which lenders the customer is eligible with."),
      ("px3-04-eligible-lenders.png", "Eligible lenders",
       "The customer is verified — here are the lenders they're eligible with for the bridge loan."),
    ],
  },
  {
    "name": "Capture the pledge card", "slug": "tk-px-pledge", "kicker": "Pledge card",
    "blurb": "Add the customer's existing pledge card and confirm the release amount.",
    "steps": [
      ("px4-01-add-pc.png", "Add the pledge card",
       "Add the customer's existing pledge card — snap it, or import it from an earlier offer."),
      ("px4-02-upload-pc.png", "Capture the card",
       "Capture or upload a clear photo of the pledge card."),
      ("px4-03-reading-pc.png", "Reading the card",
       "The app reads the card and fills in the details automatically. Just a moment."),
      ("px4-04-fetched-pc.png", "Confirm the details",
       "Check the details pulled from the card — lender, borrower, gold weight, release amount — and confirm."),
      ("px4-05-pc-added.png", "Card added",
       "The pledge card is added to the loan."),
      ("px4-06-confirm-release.png", "Confirm the release amount",
       "Confirm the total amount needed to release the customer's gold from their current lender, then submit."),
    ],
  },
  {
    "name": "Approval & e-sign", "slug": "tk-px-approval", "kicker": "Approval",
    "blurb": "Submit for the lender's approval and have the customer sign.",
    "steps": [
      ("px5-01-submit.png", "Submit for approval",
       "Submit the loan for the lender's approval."),
      ("px5-02-approval-progress.png", "Waiting for approval",
       "The loan is with the lender for approval. Just a moment."),
      ("px5-03-approved.png", "Loan approved",
       "The bridge loan is approved — share the amount with the customer before signing."),
      ("px5-04-esign-progress.png", "The customer is signing",
       "The customer signs the loan documents on their phone. Wait until they're done."),
      ("px5-05-esign-completed.png", "Signed",
       "Signing is done. If there's a co-borrower, you can send them a link to sign too."),
    ],
  },
  {
    "name": "Transfer the funds", "slug": "tk-px-funds", "kicker": "Fund transfer",
    "blurb": "Capture the security cheque and release the bridge loan to the customer.",
    "steps": [
      ("px6-01-security-cheque.png", "Capture the security cheque",
       "Take a clear photo of the customer's security cheque to proceed with the transfer."),
      ("px6-02-submit-ft.png", "Submit for transfer",
       "Confirm to submit the loan for fund transfer."),
      ("px6-03-ft-progress.png", "Transfer underway",
       "The money transfer to the customer is underway. Just a moment."),
      ("px6-04-disbursed.png", "Funds disbursed",
       "The funds are disbursed — check the payment status to confirm the customer received them."),
      ("px6-05-payment-verified.png", "Payment verified",
       "The payment is verified — the money has reached the customer."),
    ],
  },
  {
    "name": "Prove the old loan is paid", "slug": "tk-px-proof", "kicker": "Payment proof",
    "blurb": "Settle the customer's existing loan and upload proof for each card.",
    "steps": [
      ("px7-01-pc-details.png", "The cards to settle",
       "See each pledge card and the amount owed to the customer's current lender."),
      ("px7-02-upload-proof.png", "Upload payment proof",
       "Once the customer's old loan is paid off, upload proof of payment for each card."),
      ("px7-03-proof-uploaded.png", "Proof uploaded",
       "The payment proofs are uploaded for review."),
      ("px7-04-proof-approved.png", "Proof approved",
       "The payment proof is approved — the existing loan is settled. Now schedule the release visit."),
    ],
  },
  {
    "name": "Schedule the release visit", "slug": "tk-px-release", "kicker": "Release visit",
    "blurb": "Book the visit to collect the customer's gold from their old lender.",
    "steps": [
      ("px8-01-pc-selection.png", "Choose the cards",
       "Choose which pledged items to collect in the release visit."),
      ("px8-02-appointment.png", "Pick a date and time",
       "Pick a date, time, and address for the visit to release the customer's gold."),
      ("px8-03-release-location.png", "Set the location",
       "Set where the release visit will happen."),
      ("px8-04-elr-confirmation.png", "Release visit scheduled",
       "The release visit is scheduled — you'll see it in the customer's visits, ready to collect the gold."),
    ],
  },
]

partner_flows = []
n = 0
for fl in PARTNER:
    steps = []
    for fn, title, caption in fl["steps"]:
        with open(P(fn), "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode("ascii")
        steps.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})
        n += 1
    partner_flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                          "blurb": fl["blurb"], "steps": steps})

deck.append({"platform": "Partner App", "kicker": "Takeover · what the partner does at the branch",
             "viewport": "mobile", "flows": partner_flows})

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_takeover.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
with open(OUT, "w") as f:
    f.write(html)

total = sum(len(f["steps"]) for g in deck for f in g["flows"])
print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", total, "| partner added:", n)
for grp in deck:
    gs = sum(len(f["steps"]) for f in grp["flows"])
    print("\n== %s == [%s] (%d flows, %d screens)" % (grp["platform"], grp.get("viewport"), len(grp["flows"]), gs))
    for f in grp["flows"]:
        print("   %-32s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
