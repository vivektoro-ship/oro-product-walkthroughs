#!/usr/bin/env python3
"""Standardise the Renewal titles and captions in the walkthrough decks.

Same standard as scratchpad/fix_onboarding_copy.py:
  - Title: the screen's own heading in plain words, sentence case, 3-6 words,
    verb first when the customer acts, mirroring the success line on a
    confirmation.
  - Caption: one or two sentences. What the screen asks for, then the button.
    Button names exactly as printed on screen, in Title Case.
  - No button, no mention. Arrow-only screens name nothing.
  - Don't add instructions the screen doesn't give.

There was no copy table supplied for Renewal, so this is derived from those
rules against the screens themselves. Notable consequence: the Onboarding table
uses the real on-screen names (PAN, Digilocker, UPI, OTP), so Renewal now does
the same — eSign is named rather than written around.

Text only: no images touched, no screens added, removed or reordered. Screens
are matched by flow slug + position. cx-renew-e2e repeats all 34 screens in the
same order and gets identical copy. Idempotent.

    python3 scratchpad/fix_renewal_copy.py
"""
import json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = [
    os.path.join(HOME, "oro-all-flows-walkthrough.html"),
    os.path.join(HOME, "oro-field-apps-walkthrough.html"),
]

COPY = {
  "cx-renew-loan": [
    ("Start your renewal",
     "Your loans screen tells you when a loan is ready to renew. Tap Renew Loan."),
    ("Open your loan",
     "Your loan page carries the renewal card, your payments and your loan details. "
     "Tap Renew Loan."),
    ("Finding your plans",
     "Oro looks up every renewal plan you qualify for."),
    ("Choose your gold loan plan",
     "Compare the plans and filter them by processing fee or excess. Tap View Plan "
     "Details on the one you want."),
    ("Check the plan details",
     "See the amount, the interest, the fees and the dates. Tap Select Plan."),
    ("Confirm your gold loan",
     "The summary shows your new loan, what is left on the old one, and the excess "
     "coming back to you. Tap Confirm Plan."),
    ("Choose where the excess goes",
     "Take the excess into your bank account, or adjust it against the new loan. Tap Select."),
    ("Confirm your choice",
     "Check the method you picked. Tap Confirm, or Change to pick again."),
    ("Pick your bank account",
     "Choose the verified account where the excess should land, or add a new one."),
    ("Start the credit assessment",
     "Renewing needs a credit assessment before you can continue. Tap Proceed."),
    ("Choose your loan purpose",
     "Pick the reason for your loan from the list."),
    ("Add your own purpose",
     "If none of the reasons fit, choose Others and type your own. Tap Confirm."),
    ("Add your proof documents",
     "Choose your activity and business categories, then tap Upload to add your documents."),
    ("Your documents are uploaded",
     "Both categories are set and your documents are in. Tap Confirm."),
    ("Renew your personal loan",
     "Your credit assessment is complete, and your existing personal loan renews next. "
     "Tap Proceed."),
    ("Choose your personal loan plan",
     "Compare the personal loan plans the same way. Tap View Plan Details on the one you want."),
    ("Check the personal loan details",
     "See the amount, the interest and the dates for the personal loan. Tap Select Plan."),
    ("Confirm your personal loan",
     "The summary shows your new personal loan and the excess coming to you. Tap Confirm Plan."),
    ("Confirm both loans",
     "Check your gold loan and your personal loan together. Tap Confirm & Start eSign."),
  ],
  "cx-renew-sign": [
    ("Sign your documents",
     "Tick to agree to the eSign process, then tap Start eSign."),
    ("Choose your language",
     "Pick the language you want your loan documents in, alongside English. Tap Confirm."),
    ("Renewing your loan",
     "Your renewal is going through. Do not press back or close the app."),
    ("Read and sign",
     "Your loan documents open here for you to read and sign."),
    ("Signing in progress",
     "Your signing is under way. Do not press back or close the app."),
    ("Check your signing status",
     "When the timer runs out, tap Check E-Sign Status."),
    ("Your eSign is complete",
     "Signing is done, and your renewal moves on to payment."),
    ("Make your renewal payment",
     "Your renewal payment amount is shown here. Tap Make Payment."),
    ("Checking your payment",
     "Your payment is being confirmed. Do not press back or close the app."),
    ("Your payment is successful",
     "Your renewal payment has gone through."),
    ("Your request is submitted",
     "Your renewal request is in and your eSign is complete. Tap Go To Manage Loan to track it."),
    ("Follow your renewal",
     "Your lending partners are reviewing the request, and any excess transfers on the "
     "next working day."),
    ("Your loan renewal is successful",
     "Your new loan is created, and the excess on your gold loan has reached your account."),
    ("Your excess is transferred",
     "Both transfers are complete, each with its own reference number and time."),
    ("Manage your renewed loans",
     "Both loans are renewed. Tap Make Payment Now, or exit the loan during the cooling period."),
  ],
}

E2E_SLUG = "cx-renew-e2e"
E2E_ORDER = ["cx-renew-loan", "cx-renew-sign"]

BLURBS = {
    "cx-renew-loan": "From your loans screen through to confirming your new plans.",
    "cx-renew-sign": "Sign your documents, pay, and watch the excess reach your account.",
}

# Match the other single-shot groups, as Onboarding now does.
E2E_KICKER_OLD = "Renewal · single shot"
E2E_KICKER_NEW = "Universal · single shot"


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


def apply(path):
    html = open(path, encoding="utf-8").read()
    before = len(html)
    b, e = deck_bounds(html)
    deck = json.loads(html[b:e + 1])
    idx = {f["slug"]: (g, f) for g in deck for f in g["flows"]}

    missing = []
    for slug, rows in COPY.items():
        if slug not in idx:
            missing.append("flow %s not found" % slug)
        elif len(idx[slug][1]["steps"]) != len(rows):
            missing.append("flow %s has %d screens, table expects %d"
                           % (slug, len(idx[slug][1]["steps"]), len(rows)))
    run = [r for s in E2E_ORDER for r in COPY[s]]
    if E2E_SLUG not in idx:
        missing.append("flow %s not found" % E2E_SLUG)
    elif len(idx[E2E_SLUG][1]["steps"]) != len(run):
        missing.append("flow %s has %d screens, table expects %d"
                       % (E2E_SLUG, len(idx[E2E_SLUG][1]["steps"]), len(run)))
    if missing:
        raise SystemExit("STOP - deck does not match the table:\n  " + "\n  ".join(missing))

    titles = captions = blurbs = kickers = 0

    def write_steps(slug, rows):
        nonlocal titles, captions
        for st, (title, caption) in zip(idx[slug][1]["steps"], rows):
            if st.get("title") != title:
                st["title"] = title
                titles += 1
            if st.get("caption") != caption:
                st["caption"] = caption
                captions += 1

    for slug, rows in COPY.items():
        write_steps(slug, rows)
    write_steps(E2E_SLUG, run)

    for slug, blurb in BLURBS.items():
        f = idx[slug][1]
        if f.get("blurb") != blurb:
            f["blurb"] = blurb
            blurbs += 1

    for g in deck:
        if g.get("_product") == "Renewal" and g.get("kicker") == E2E_KICKER_OLD:
            g["kicker"] = E2E_KICKER_NEW
            kickers += 1

    new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[e + 1:]
    open(path, "w", encoding="utf-8").write(new_html)
    return dict(titles=titles, captions=captions, blurbs=blurbs, kickers=kickers,
                before=before, after=len(new_html))


if __name__ == "__main__":
    for path in DECKS:
        r = apply(path)
        print("\n%s" % os.path.basename(path))
        print("  titles changed   : %d" % r["titles"])
        print("  captions changed : %d" % r["captions"])
        print("  blurbs changed   : %d" % r["blurbs"])
        print("  kickers changed  : %d" % r["kickers"])
        print("  bytes %d -> %d  (%+d)" % (r["before"], r["after"], r["after"] - r["before"]))
