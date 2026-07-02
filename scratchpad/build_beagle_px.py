#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
PX = os.path.join(HOME, "assets/beagle-px")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-beagle-cx-walkthrough.html")
OUT = SRC

def P(fn): return os.path.join(PX, fn)

# ---- reuse existing Customer App group verbatim (base64 untouched); idempotent on Partner App ----
src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
deck = [g for g in deck if g.get("platform") != "Partner App"]
for g in deck:
    g.setdefault("viewport", "mobile")

# ---- Partner App (branch-side) GL flows — partner voice, addressing the agent ("you") ----
PARTNER = [
  {
    "name": "Start the branch visit", "slug": "px-start-visit", "kicker": "Visit start",
    "blurb": "Open the assigned visit, reach the branch, and confirm you're there.",
    "steps": [
      ("px1-01-home.png", "Open the assigned visit",
       "Open the visit assigned to you — you'll see the customer, the branch, and the scheduled time."),
      ("px1-02-start-step1.png", "Slide to start",
       "Once you've reached the branch and the customer is with you, slide Start Visit to begin."),
      ("px1-03-start-step2.png", "Confirming your location",
       "We confirm you're at the right branch before the visit can start."),
      ("px1-04-verification.png", "Take a photo at the branch",
       "Take a live photo at the branch so we can confirm you're really there."),
      ("px1-05-verified.png", "You're verified",
       "Your presence at the branch is confirmed — you're ready to help the customer."),
    ],
  },
  {
    "name": "Verify the customer", "slug": "px-verify-customer", "kicker": "Customer checks",
    "blurb": "Confirm the customer's identity, signature, and details at the branch.",
    "steps": [
      ("px2-01-ekyc-consent.png", "Take the customer's consent",
       "Read the consent with the customer and confirm to continue with their identity check."),
      ("px2-02-ekyc.png", "Verify their identity",
       "Enter the last digits of the customer's Aadhaar number to verify who they are."),
      ("px2-03-signature.png", "Capture their signature",
       "Take a clear photo of the customer's signature."),
      ("px2-04-other-details.png", "Add their details",
       "Fill in the customer's remaining details, then confirm."),
      ("px2-05-ekyc-done.png", "Running the checks",
       "We run all the required checks on the customer — identity, records, and more. Just a moment."),
    ],
  },
  {
    "name": "Guide the customer's plan", "slug": "px-plan", "kicker": "Plan",
    "blurb": "Walk the customer through the plans and confirm their choice.",
    "steps": [
      ("px3-01-choose-plan.png", "Show the plans",
       "Walk the customer through the available plans and the amount each offers."),
      ("px3-02-preview-plan.png", "Preview the plan",
       "Preview the chosen plan — the visit tracker at the top shows where you are in the journey."),
      ("px3-03-confirm-plan.png", "Confirm the plan",
       "Go over the plan with the customer — the gold loan and any add-ons — then proceed."),
      ("px3-04-in-progress.png", "The customer is choosing",
       "The customer confirms the plan on their own phone. Wait here while they choose."),
    ],
  },
  {
    "name": "Submit for lender approval", "slug": "px-submit", "kicker": "Submit",
    "blurb": "Add the required proofs and send the loan to the lender.",
    "steps": [
      ("px4-02-ig-step1.png", "Add the proof documents",
       "Upload the documents the lender needs to assess this loan."),
      ("px4-03-ig-step2.png", "Documents uploaded",
       "Once the proofs are uploaded, confirm to continue."),
      ("px4-01-submit.png", "Submit for approval",
       "Send the loan for the lender's approval. After this, the plan and amount are locked."),
    ],
  },
  {
    "name": "Approval & money transfer", "slug": "px-disbursal", "kicker": "Approval",
    "blurb": "Track the loan from lender approval through to the money reaching the customer.",
    "steps": [
      ("px5-01-approval-in-progress.png", "Waiting for approval",
       "The loan is with the lender for approval. This usually takes about 5 minutes."),
      ("px5-02-moved-to-queue.png", "Loan in the queue",
       "If the lender is busy, the loan moves to a queue — you can keep tracking it from here."),
      ("px5-03-esign-in-progress.png", "The customer is signing",
       "The customer signs the loan documents on their phone. Wait until they're done."),
      ("px5-04-fund-transfer.png", "Money transfer underway",
       "With approval and signing done, the money transfer to the customer is underway."),
      ("px5-05-fund-transferred.png", "Funds transferred",
       "The funds are transferred — check with the customer that the money has reached them."),
      ("px5-06-visit-complete-aa.png", "Visit complete",
       "The gold loan visit is complete. The visit and loan numbers are shown here."),
    ],
  },
  {
    "name": "Confirm funds if needed", "slug": "px-confirm-funds", "kicker": "Backup proof",
    "blurb": "The backup path when the automatic confirmation hasn't arrived yet.",
    "steps": [
      ("px6-01-upload-proof-step1.png", "Check with the customer",
       "If the automatic confirmation hasn't arrived, check with the customer that the funds are credited, then upload proof."),
      ("px6-02-upload-proof-step2.png", "Upload the proof",
       "Take a photo of the customer's credit confirmation and confirm the amount transferred."),
      ("px6-03-visit-complete-noaa.png", "Visit complete",
       "Once you confirm, the gold loan visit is complete."),
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

deck.append({"platform": "Partner App", "kicker": "Beagle · what the partner does at the branch",
             "viewport": "mobile", "flows": partner_flows})

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_beagle.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
with open(OUT, "w") as f:
    f.write(html)

total = sum(len(f["steps"]) for g in deck for f in g["flows"])
print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", total, "| partner added:", n)
for grp in deck:
    gs = sum(len(f["steps"]) for f in grp["flows"])
    print("\n== %s == (%d flows, %d screens)" % (grp["platform"], len(grp["flows"]), gs))
    for f in grp["flows"]:
        print("   %-30s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
