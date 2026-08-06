#!/usr/bin/env python3
"""Append the Customer App > Renewal group to the field-apps and all-flows
decks. Idempotent: re-running replaces its own group (matched on _product)
rather than adding a duplicate.

    python3 scratchpad/build_renewal.py
"""
import base64, io, json, os

# Each screen is embedded twice (once in the split-up cards, once in the
# single-shot run), so the deck carries two copies of every PNG. Quantising to
# 256 colours at embed time halves that and is invisible at the 300px width the
# phone frame renders. The PNGs in assets/ are never touched — set COMPRESS to
# False to embed them byte-for-byte instead.
COMPRESS = True

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/renewal")
DECKS = [
    os.path.join(HOME, "oro-field-apps-walkthrough.html"),
    os.path.join(HOME, "oro-all-flows-walkthrough.html"),
]
PRODUCT = "Renewal"

# ---------------------------------------------------------------- the flows --
# Split at the Confirm Renewal -> start signing boundary: the first card ends
# on a confirmation, the second opens on a new task.

FLOWS = [
  {
    "name": "Renew your loan", "slug": "cx-renew-loan", "kicker": "Renewal",
    "blurb": "From your loans screen through to confirming your new plans.",
    "steps": [
      ("r01-6252-75650.png", "Start your renewal",
       "Your loans screen tells you when a loan is ready to renew. Tap Renew Loan to begin."),
      ("r02-6252-75976.png", "Open your loan",
       "Your loan page carries the renewal card, your payment options and everything else "
       "about the loan. Tap Renew Loan."),
      ("r03-6252-75459.png", "Finding your plans",
       "Oro looks up every renewal plan you qualify for."),
      ("r04-6252-75264.png", "Choose your gold loan plan",
       "Compare the plans and sort them by no processing fee, with excess, or no excess. "
       "Tap View Plan Details on the one you want."),
      ("r05-6252-74404.png", "Check the plan details",
       "See the amount, the interest, the processing fee and the dates before you commit. "
       "Tap Select Plan."),
      ("r06-6252-74496.png", "Confirm your gold loan",
       "Your new loan replaces the old one, and the summary shows the renewal amount and "
       "the extra coming back to you. Tap Confirm Plan."),
      ("r07-6252-74639.png", "Choose where the extra goes",
       "Take the extra amount into your bank account, or set it against the new loan. Tap Select."),
      ("r08-6252-74834.png", "Confirm your choice",
       "Check the method you picked, then tap Confirm."),
      ("r09-6252-76631.png", "Pick your bank account",
       "Choose the verified account where the extra amount should land, or add a new one."),
      ("r10-6252-75575.png", "Start the income check",
       "Renewing needs a short income check. Tap Proceed."),
      ("r11-6252-77223.png", "Choose why you need it",
       "Pick the reason for your loan from the list."),
      ("r12-6252-77260.png", "Add your own reason",
       "If none of the reasons fit, choose Others and type your own. Tap Confirm."),
      ("r13-6252-77280.png", "Add your proof documents",
       "Choose your activity and business categories, then tap Upload to add your documents."),
      ("r14-6252-77332.png", "Your documents are uploaded",
       "Both categories are set and your documents are in. Tap Confirm."),
      ("r15-6252-75475.png", "Renew your personal loan",
       "Your income check is done, and your personal loan renews alongside your gold loan. "
       "Tap Proceed."),
      ("r16-6252-75366.png", "Choose your personal loan plan",
       "Compare the personal loan plans the same way. Tap View Plan Details on the one you want."),
      ("r17-6252-75172.png", "Review the personal loan",
       "See the amount, the interest and the dates for the personal loan. Tap Select Plan."),
      ("r18-6252-75029.png", "Confirm your personal loan",
       "The summary shows the new amount, what is left on the old loan, and the extra coming "
       "to you. Tap Confirm Plan."),
      ("r19-6252-76781.png", "Confirm both loans",
       "Check your gold loan and your personal loan side by side, then confirm to start signing."),
    ],
  },
  {
    "name": "Sign and pay", "slug": "cx-renew-sign", "kicker": "Signing and payment",
    "blurb": "Sign your documents, pay, and watch the extra amount reach your account.",
    "steps": [
      ("r20-6252-77349.png", "Sign your documents",
       "Agree to sign, then start. You'll confirm with a code sent to your phone."),
      ("r21-6252-77395.png", "Choose your language",
       "Get your loan documents in your own language as well as English, then tap Confirm."),
      ("r22-6252-76923.png", "Renewing your loan",
       "Your renewal is going through. Don't press back or close the app."),
      ("r23-6252-76887.png", "Read and sign",
       "Your loan documents open here for you to read and sign."),
      ("r24-6252-76899.png", "Signing in progress",
       "Your signing is under way. Don't press back or close the app."),
      ("r25-6252-76966.png", "Check your signing status",
       "If the timer runs out, tap the status button to see how far it got."),
      ("r26-6252-80608.png", "Your documents are signed",
       "Signing is complete. Your renewal moves on to payment."),
      ("r27-6252-76757.png", "Make your renewal payment",
       "Your renewal payment amount is shown here. Tap Make Payment."),
      ("r28-6252-76946.png", "Checking your payment",
       "Your payment is being confirmed. Don't press back or close the app."),
      ("r29-6252-76990.png", "Your payment went through",
       "Your renewal payment is confirmed."),
      ("r30-6252-78415.png", "Your request is in",
       "Your renewal request is submitted. Tap Go To Manage Loan to follow it."),
      ("r31-6252-77467.png", "Follow your renewal",
       "Your loans screen shows the request under review, and the extra amount waiting to "
       "be transferred."),
      ("r32-6252-77950.png", "Your new loan is created",
       "Your renewal is done, and the extra amount on your gold loan has reached your bank account."),
      ("r33-6252-77700.png", "The extra amount is paid",
       "Both transfers are complete, each with its own reference number and time."),
      ("r34-6252-78195.png", "Your renewed loans",
       "Both loans are renewed and ready to manage. You can make a payment, or exit during "
       "the cooling period."),
    ],
  },
]

GROUP_META = {
    "platform": "Customer App",
    "kicker": "Renewal · renew your gold loan",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "User App",
}

# The same 34 screens again as one uninterrupted run, for anyone who wants to
# watch a renewal start to finish without stepping between cards.
E2E_META = {
    "platform": "Renewal — End to end",
    "kicker": "Renewal · single shot",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "Universal",
}
E2E_FLOW = {
    "name": "End to end flow", "slug": "cx-renew-e2e", "kicker": "Renewal · single shot",
    "blurb": "A whole renewal in one run, from your loans screen to the money landing.",
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
    if fn not in _CACHE:   # same screen is embedded twice; encode it once
        _CACHE[fn] = "data:image/png;base64," + base64.b64encode(png_bytes(fn)).decode("ascii")
    return _CACHE[fn]


def build_groups():
    """Returns (split-into-cards group, single-shot end-to-end group)."""
    flows, run = [], []
    for fl in FLOWS:
        steps = [{"img": datauri(fn), "title": t, "caption": c}
                 for fn, t, c in fl["steps"]]
        flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                      "blurb": fl["blurb"], "steps": steps})
        run.extend(steps)                     # flow order == the Figma sequence

    g = dict(GROUP_META)
    g["flows"] = flows

    e2e = dict(E2E_META)
    e2e_flow = dict(E2E_FLOW)
    e2e_flow["steps"] = run
    e2e["flows"] = [e2e_flow]
    return g, e2e


def deck_bounds(html):
    """Locate the DECK array literal by bracket matching."""
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
    deck = [g for g in deck if g.get("_product") != PRODUCT]   # idempotent
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
                  % (g["kicker"], len(g["flows"]),
                     sum(len(f["steps"]) for f in g["flows"])))
            for f in g["flows"]:
                print("     %-28s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
        print("  added by this script: %d screens" % added)
