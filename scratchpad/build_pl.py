#!/usr/bin/env python3
"""Append the Customer App > Personal Loan group to the field-apps and all-flows
decks. Idempotent: re-running replaces its own group (matched on _product).

Screens come from one section only — "Section 1" 4508:60510 on page
47:4723 "Module 4 - Fresh Loan Flow" of Oro User App - Master. That is the most
complete personal-loan build in the file (31 screens, including the resume,
timeout and delayed-approval states the shorter SFL PL section lacks).

    python3 scratchpad/build_pl.py
"""
import base64, io, json, os

# Each screen is embedded twice (split cards + single shot). Quantising at embed
# time halves that and is invisible at the 300px the phone frame renders.
# The PNGs in assets/pl stay untouched at full 2x.
COMPRESS = True

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/pl")
DECKS = [
    os.path.join(HOME, "oro-field-apps-walkthrough.html"),
    os.path.join(HOME, "oro-all-flows-walkthrough.html"),
]
PRODUCT = "Personal Loan"

FLOWS = [
  {
    "name": "Verify with the lender", "slug": "cx-pl-kyc", "kicker": "Lender check",
    "blurb": "From the offer on your gold loan through the lender's identity and credit checks.",
    "steps": [
      ("pl01-4508-60994.png", "Start your personal loan",
       "Your gold loan page shows you are eligible for a personal loan on top of it. "
       "Tap Avail Personal Loan."),
      ("pl02-4508-61739.png", "See the steps ahead",
       "Four steps: lender check, plan selection, signing and funds. Tap Proceed."),
      ("pl03-4508-61466.png", "Give your consent",
       "Read the identity and credit-score consents from the lender. Proceed stays off "
       "until both are agreed."),
      ("pl04-4508-61550.png", "Both consents agreed",
       "With both agreed, tap Proceed."),
      ("pl05-4508-61655.png", "Confirm it’s you",
       "Enter the six-digit code sent to your registered mobile number, and agree to the "
       "records check."),
      ("pl06-4508-61693.png", "Your code is entered",
       "With the code in and the consent agreed, tap Verify OTP."),
      ("pl07-4508-61592.png", "Fetching your details",
       "Your records are being pulled. Do not go back or close the app."),
      ("pl08-4508-62692.png", "Choose your loan purpose",
       "Pick why you need the money, then tap Proceed To Next Step."),
      ("pl09-4508-61230.png", "Pick up where you left off",
       "If you stop part-way, your gold loan page shows what you qualify for. Tap Resume Process."),
      ("pl10-4508-61830.png", "Resume the lender check",
       "The lender check shows as in progress. Tap Resume."),
      ("pl11-4508-62752.png", "Your documents are verified",
       "Your identity is confirmed from your government document wallet. Tap Proceed To Next Step."),
      ("pl12-4508-61632.png", "Your records are fetched",
       "The records check is complete. Tap Proceed."),
    ],
  },
  {
    "name": "Choose your plan", "slug": "cx-pl-plan", "kicker": "Plan",
    "blurb": "Compare the personal loan plans, confirm one, and pick where the money lands.",
    "steps": [
      ("pl13-4508-61910.png", "Move on to plans",
       "The lender check is complete. Tap Check Eligibility to see your plans."),
      ("pl14-4508-61615.png", "Loading your plans",
       "Oro checks which personal loan plans you qualify for."),
      ("pl15-4508-60778.png", "Choose your plan",
       "Compare the plans from your personal loan lender, sorted by highest value or lowest "
       "interest. Tap Select Plan."),
      ("pl16-4508-60885.png", "Check the plan details",
       "See the amount, the tenure, the fees, and how the interest steps up if you miss a "
       "payment. Tap Select Plan."),
      ("pl17-4508-60636.png", "Confirm your plan",
       "Check the plan and the amount, agree to the consent, then tap Confirm Plan."),
      ("pl18-4508-60511.png", "Pick your bank account",
       "Choose a verified account for your money, or add a new one. The account already used "
       "for your gold loan is marked."),
    ],
  },
  {
    "name": "Approval, signing and funds", "slug": "cx-pl-fund", "kicker": "Approval and funds",
    "blurb": "Approval, signing, and the money reaching your account alongside your gold loan.",
    "steps": [
      ("pl19-4508-60974.png", "Waiting for approval",
       "Your loan is going for approval. This takes five to ten minutes."),
      ("pl20-4508-62013.png", "Follow it from the steps",
       "Plan selection shows as in progress while approval runs. Tap Resume to go back to it."),
      ("pl21-4508-62287.png", "Still being approved",
       "The timer counts down while the lender decides."),
      ("pl22-4508-62823.png", "Taking a little longer",
       "If approval is slow, Oro expedites it and tells you so."),
      ("pl23-4508-62307.png", "Your loan is approved",
       "Your approved amount is shown here. Tap Proceed To Next Step to sign."),
      ("pl24-4508-62079.png", "Sign your documents",
       "Signing uses a code sent to your registered mobile number. Tap Start eSign."),
      ("pl25-4508-62229.png", "Read and sign",
       "Your loan documents open here for you to read and sign."),
      ("pl26-4508-62263.png", "Waiting for your signature",
       "If it has been five minutes, tap Check Status to move the transfer along."),
      ("pl27-4508-62244.png", "Money on its way",
       "Your transfer takes five to ten minutes. Tap Check Status for an update."),
      ("pl28-4508-62164.png", "Fund transfer in progress",
       "Three steps are done, and the transfer is the last one."),
      ("pl29-4508-62340.png", "Your money is transferred",
       "The amount, the account, the time and the transaction number are all here. "
       "Tap Go To Manage Loan."),
      ("pl30-4508-62408.png", "Both loans in one place",
       "Your gold loan and your new personal loan sit together, each with its own number "
       "and summary."),
      ("pl31-4508-62627.png", "Back to the steps",
       "The steps screen keeps showing the transfer until it settles."),
    ],
  },
]

# PL is its own product card, placed straight after Beagle because a personal
# loan is only offered on top of a disbursed gold loan. Two sections inside it:
# User App and Admin.
AFTER_PRODUCT = "Beagle revamp"
SLUG_PREFIX = "cx-pl-"

E2E_FLOW = {
    "name": "Personal loan, end to end", "slug": "cx-pl-e2e", "kicker": "Single shot",
    "blurb": "The whole personal loan in one run, from the offer on your gold loan to the money landing.",
}

USER_META = {
    "platform": "Customer App",
    "kicker": "Personal loan · added to your gold loan",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "User App",
}

# Desktop screens follow the deck's ~2048px convention, not the 2x phone rule.
ADMIN_ASSETS = os.path.join(HOME, "assets/pl-admin")
ADMIN_META = {
    "platform": "Admin",
    "kicker": "Personal loan · how Ops triggers and approves it",
    "viewport": "desktop",
    "_product": PRODUCT,
    "_appType": "Admin",
}
ADMIN_FLOWS = [
  {
    "name": "Trigger the personal loan", "slug": "cx-pl-ad-trigger", "kicker": "Trigger",
    "blurb": "Recommend a personal loan to the customer on top of their gold loan.",
    "steps": [
      ("ad01-2457-27680.png", "See the triggered plan",
       "The banner confirms a personal loan recommendation went out. Click View Trigger for "
       "the lender, branch, plan, rate and amount."),
      ("ad02-2457-27932.png", "Trigger a personal loan",
       "Pick the lender, branch and plan, set the rate and the amount, then Confirm & Trigger."),
      ("ad03-2457-27479.png", "Approval is pending",
       "The loan has to be approved inside the window shown. The countdown and a quick check "
       "sit on the record."),
      ("ad04-2457-28201.png", "Open the approval",
       "Once the customer's side is done, Approve Personal Loan appears on the loan."),
    ],
  },
  {
    "name": "Check and approve", "slug": "cx-pl-ad-approve", "kicker": "Approval",
    "blurb": "The customer check, the approval, and what blocks it.",
    "steps": [
      ("ad05-2457-28441.png", "Run the customer check",
       "Step one validates the customer type, their name and date of birth, their PAN and the "
       "Oro approval. Steps two and three unlock once it passes."),
      ("ad06-2457-28812.png", "Amount above the limit",
       "If the amount goes over the approved loan, the field flags it and Approve Personal "
       "Loan stays off."),
      ("ad07-2457-28592.png", "Check the approval details",
       "Confirm the lender, branch, plan, rate, amount and payout account, then click "
       "Approve Personal Loan."),
      ("ad08-2457-29033.png", "Confirm the approval",
       "A last prompt shows the amount before it commits. Click Approve."),
      ("ad09-2457-29203.png", "Personal loan approved",
       "The approval lands and the record moves on. Click Done."),
    ],
  },
  {
    "name": "Fund transfer and close", "slug": "cx-pl-ad-fund", "kicker": "Funds",
    "blurb": "Both loans on one record, through to the money moving and the mismatch clearing.",
    "steps": [
      ("ad10-2457-29361.png", "Both loans on the record",
       "The gold loan and the personal loan sit side by side with their amounts and status."),
      ("ad11-2457-29593.png", "Fund transfer pending",
       "The personal loan shows as pending fund transfer, with any mismatch flagged against it."),
      ("ad12-2457-29825.png", "The funds are transferred",
       "The transfer record carries the amount, the reference number, the date and the mode."),
      ("ad13-2457-30051.png", "Gold and personal loan active",
       "Both loans are active and no mismatch is left on the record."),
    ],
  },
]

def png_bytes(path):
    if not COMPRESS:
        with open(path, "rb") as fp:
            return fp.read()
    from PIL import Image
    im = Image.open(path).convert("RGB")
    q = im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    buf = io.BytesIO()
    q.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


_CACHE = {}


def datauri_from(dirpath, fn):
    key = dirpath + "/" + fn
    if key not in _CACHE:
        _CACHE[key] = "data:image/png;base64," + base64.b64encode(
            png_bytes(os.path.join(dirpath, fn))).decode("ascii")
    return _CACHE[key]


def mk_flows(spec, dirpath):
    out, run = [], []
    for fl in spec:
        steps = [{"img": datauri_from(dirpath, fn), "title": t, "caption": c}
                 for fn, t, c in fl["steps"]]
        out.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                    "blurb": fl["blurb"], "steps": steps})
        run.extend(steps)
    return out, run


def build_groups():
    user_flows, run = mk_flows(FLOWS, ASSETS)
    ef = dict(E2E_FLOW); ef["steps"] = run
    user_flows.append(ef)
    user = dict(USER_META); user["flows"] = user_flows

    admin_flows, _ = mk_flows(ADMIN_FLOWS, ADMIN_ASSETS)
    admin = dict(ADMIN_META); admin["flows"] = admin_flows
    return user, admin


def deck_bounds(html):
    s = html.index("const DECK")
    b = html.index("[", s)
    d = 0
    for i in range(b, len(html)):
        if html[i] == "[":
            d += 1
        elif html[i] == "]":
            d -= 1
            if d == 0:
                return b, i
    raise SystemExit("unterminated DECK array")


def inject(path, groups):
    html = open(path, encoding="utf-8").read()
    b, e = deck_bounds(html)
    deck = json.loads(html[b:e + 1])

    # idempotent: drop our own groups, and any PL flows a previous run pushed
    # into someone else's group
    deck = [g for g in deck if g.get("_product") != PRODUCT]
    for g in deck:
        g["flows"] = [f for f in g["flows"] if not f["slug"].startswith(SLUG_PREFIX)]
    deck = [g for g in deck if g["flows"]]

    # Landing-page product order follows first appearance, so insert after the
    # FIRST contiguous run of Beagle groups. Going after the last one would put
    # PL behind Takeover, because the Beagle end-to-end group sits near the end.
    first = next((i for i, g in enumerate(deck) if g.get("_product") == AFTER_PRODUCT), None)
    if first is None:
        raise SystemExit("STOP - no %s groups to sit after" % AFTER_PRODUCT)
    at = first
    while at < len(deck) and deck[at].get("_product") == AFTER_PRODUCT:
        at += 1
    deck[at:at] = list(groups)

    new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[e + 1:]
    open(path, "w", encoding="utf-8").write(new_html)
    return deck, at, len(new_html)


def apptypes(path):
    """Only offer sections the deck's landing page actually renders."""
    html = open(path, encoding="utf-8").read()
    import re
    m = re.search(r"var APPTYPES=\[([^\]]*)\]", html)
    return re.findall(r"'([^']+)'", m.group(1)) if m else []


if __name__ == "__main__":
    user, admin = build_groups()
    for path in DECKS:
        allowed = apptypes(path)
        groups = [g for g in (user, admin) if g["_appType"] in allowed]
        skipped = [g["_appType"] for g in (user, admin) if g["_appType"] not in allowed]
        deck, at, nbytes = inject(path, groups)
        total = sum(len(f["steps"]) for g in deck for f in g["flows"])
        print("\n%s" % os.path.basename(path))
        print("  landing page renders: %s" % ", ".join(allowed))
        if skipped:
            print("  SKIPPED (would not render here): %s" % ", ".join(skipped))
        print("  inserted %d group(s) at deck position %d | %.1f MB | %d screens"
              % (len(groups), at + 1, nbytes / 1024 / 1024, total))
        for g in groups:
            print("  == %s · %s == (%d flows, %d screens)"
                  % (PRODUCT, g["_appType"], len(g["flows"]),
                     sum(len(f["steps"]) for f in g["flows"])))
            for f in g["flows"]:
                print("     %-30s %3d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
        print("  product order: %s" % " | ".join(dict.fromkeys(g["_product"] for g in deck)))
