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

GROUP_META = {
    "platform": "Customer App",
    "kicker": "Personal loan · added to your gold loan",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "User App",
}
E2E_META = {
    "platform": "Personal Loan — End to end",
    "kicker": "Universal · single shot",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "Universal",
}
E2E_FLOW = {
    "name": "End to end flow", "slug": "cx-pl-e2e", "kicker": "Universal · single shot",
    "blurb": "The whole personal loan in one run, from the offer on your gold loan to the money landing.",
}


def png_bytes(fn):
    path = os.path.join(ASSETS, fn)
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


def datauri(fn):
    if fn not in _CACHE:
        _CACHE[fn] = "data:image/png;base64," + base64.b64encode(png_bytes(fn)).decode("ascii")
    return _CACHE[fn]


def build_groups():
    flows, run = [], []
    for fl in FLOWS:
        steps = [{"img": datauri(fn), "title": t, "caption": c} for fn, t, c in fl["steps"]]
        flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                      "blurb": fl["blurb"], "steps": steps})
        run.extend(steps)
    g = dict(GROUP_META); g["flows"] = flows
    e2e = dict(E2E_META)
    ef = dict(E2E_FLOW); ef["steps"] = run
    e2e["flows"] = [ef]
    return g, e2e


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
    before = len(deck)
    deck = [g for g in deck if g.get("_product") != PRODUCT]
    replaced = before != len(deck)
    deck.extend(groups)
    new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[e + 1:]
    open(path, "w", encoding="utf-8").write(new_html)
    return deck, replaced, len(new_html)


if __name__ == "__main__":
    groups = build_groups()
    added = sum(len(f["steps"]) for g in groups for f in g["flows"])
    for path in DECKS:
        deck, replaced, nbytes = inject(path, groups)
        total = sum(len(f["steps"]) for g in deck for f in g["flows"])
        print("\n%s" % os.path.basename(path))
        print("  %s %s groups | %.1f MB | %d screens in deck"
              % ("replaced" if replaced else "added", PRODUCT, nbytes / 1024 / 1024, total))
        for g in groups:
            print("  == %s == (%d flows, %d screens)"
                  % (g["kicker"], len(g["flows"]), sum(len(f["steps"]) for f in g["flows"])))
            for f in g["flows"]:
                print("     %-30s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
        print("  added by this script: %d screens" % added)
