#!/usr/bin/env python3
"""Append the Customer App > Onboarding group to the field-apps and all-flows
decks. Idempotent: re-running replaces its own group (matched on _product)
rather than adding a duplicate.

    python3 scratchpad/build_onboarding.py
"""
import base64, io, json, os

# Each screen is embedded twice (once in the split-up cards, once in the
# single-shot run), so the deck carries two copies of every PNG. Quantising to
# 256 colours at embed time halves that and is invisible at the 300px width the
# phone frame renders. The PNGs in assets/ are never touched — set COMPRESS to
# False to embed them byte-for-byte instead.
COMPRESS = True

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/onboarding")
DECKS = [
    os.path.join(HOME, "oro-field-apps-walkthrough.html"),
    os.path.join(HOME, "oro-all-flows-walkthrough.html"),
]
PRODUCT = "Onboarding"

# ---------------------------------------------------------------- the flows --
# Customer voice throughout: speak to the customer as "you", plain English,
# no jargon or acronyms, button names exactly as they appear on screen.

FLOWS = [
  {
    "name": "Get started", "slug": "cx-onb-start", "kicker": "Getting started",
    "blurb": "Verify your mobile number and tell us where you are.",
    "steps": [
      ("s01-mobile-04-1504-34310.png", "Enter your mobile number",
       "Enter the mobile number linked to your identity records, then tap Proceed."),
      ("s01-mobile-06-1504-34169.png", "Confirm it's you",
       "Enter the four-digit code sent to your phone, then tap Verify OTP."),
      ("s01-mobile-07-1504-34582.png", "Your number is verified",
       "Your mobile number is confirmed. Tap Proceed To Next Step to carry on."),
      ("s01-mobile-10-2123-40881.png", "Agree to the data checks",
       "Read what Oro collects and why, agree to both, then tap Proceed To Next Screen."),
      ("s02-city-02-1504-35162.png", "Choose your city",
       "Pick the city you're in. Oro works in these cities today."),
    ],
  },
  {
    "name": "Verify your email", "slug": "cx-onb-email", "kicker": "Email",
    "blurb": "Add the email address where your updates will go.",
    "steps": [
      ("s03-email-01-1504-35253.png", "Choose how to verify",
       "Verify your email with a code, or continue with your Google account."),
      ("s03-email-03-1504-35513.png", "Enter your email address",
       "Type the email where you want your updates, then tap Get OTP."),
      ("s03-email-05-1504-35853.png", "Your email is verified",
       "Your email address is confirmed. Tap Proceed To Next Step."),
    ],
  },
  {
    "name": "Prove it's you", "slug": "cx-onb-identity", "kicker": "Identity",
    "blurb": "A live photo and your identity details, checked in a few seconds.",
    "steps": [
      ("s04-liveliness-02-1504-36129.png", "Allow camera access",
       "Allow access to your camera and location so the check can run. Tap Click To Allow."),
      ("s04-liveliness-03-1504-36029.png", "Take a live photo",
       "Look straight at the camera, stay inside the circle, and take off your glasses."),
      ("s04-liveliness-06-1504-36156.png", "Your photo is accepted",
       "The live check is done. Tap Proceed To Next Step."),
      ("s05-identity-01-1504-37467.png", "Keep your documents handy",
       "You'll need your identity card, your tax card, a bank proof and an address proof. "
       "You're halfway through."),
      ("s05-identity-02-1504-37290.png", "Confirm your identity",
       "Use the recommended route to bring your identity details across in a few seconds."),
      ("s05-identity-04-1504-37322.png", "Your identity is verified",
       "Your identity details are confirmed and shown here. Tap Proceed To Next Step."),
    ],
  },
  {
    "name": "Your details", "slug": "cx-onb-details", "kicker": "About you",
    "blurb": "Your tax card, your family names, your work and your income.",
    "steps": [
      ("s06-father-02-1504-28349.png", "Add your father's name",
       "Type your father's name as it appears on your identity card."),
      ("s07-pan-02-1504-44174.png", "Enter your tax card number",
       "Enter the number on your tax card. It has to be the one linked to your mobile number."),
      ("s07-pan-04-1504-44272.png", "Your tax card is verified",
       "Your tax card is confirmed. You're three quarters of the way through."),
      ("s08-personal-03-1504-45222.png", "Tell us your marital status",
       "Choose single or married. If you're married, add your spouse's name."),
      ("s08-personal-06-1504-28494.png", "Add your work details",
       "Choose what you do, and how many months you've been doing it."),
      ("s08-personal-10-1504-33261.png", "Choose your income range",
       "Pick your annual household income, then agree to the declaration below it."),
      ("s08-personal-12-1504-33239.png", "Add your mother's name",
       "Type your mother's name as it appears on your identity card."),
    ],
  },
  {
    "name": "Where you live", "slug": "cx-onb-address", "kicker": "Address",
    "blurb": "Your current address and how long you've been there.",
    "steps": [
      ("s09-address-02-1504-30487.png", "Add your current address",
       "Enter your pincode and full address. Tick Same As Permanent Address if they match."),
      ("s09-address-05-1504-31361.png", "Tell us about your home",
       "Choose whether you rent or own, and the year you moved in."),
      ("s09-address-06-1504-31551.png", "Almost done",
       "About two minutes left. Tap Proceed To Next Step."),
    ],
  },
  {
    "name": "Bank account and nominee", "slug": "cx-onb-bank", "kicker": "Money and nominee",
    "blurb": "Link the account your money goes to, and name your nominee.",
    "steps": [
      ("s10-bank-01-1504-29659.png", "Add your bank account",
       "Confirm your account by sending ₹1 from your bank app. The ₹1 comes back to you "
       "once the check is done."),
      ("s10-bank-03-1504-29764.png", "Pick your payment app",
       "Choose the app you'll send the ₹1 from."),
      ("s10-bank-05-1504-29900.png", "Your bank account is added",
       "Your account is confirmed and shown here. Tap Proceed To Add Nominee."),
      ("s11-nominee-04-1504-29489.png", "Add your nominee",
       "Add the name, age, mobile number and relationship of the person you'd like as your nominee."),
      ("s11-nominee-06-1504-29530.png", "Add your nominee's address",
       "Enter your nominee's address, or tick Use My Current Address."),
      ("s11-nominee-07-1504-29091.png", "You're all set",
       "Your account is ready. Tap Proceed To Home Screen to start using Oro."),
    ],
  },
]

GROUP_META = {
    "platform": "Customer App",
    "kicker": "Onboarding · getting set up with Oro",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "User App",
}

# The same 30 screens again as one uninterrupted run, for anyone who wants to
# watch onboarding start to finish without stepping between cards.
E2E_META = {
    "platform": "Onboarding — End to end",
    "kicker": "Onboarding · single shot",
    "viewport": "mobile",
    "_product": PRODUCT,
    "_appType": "Universal",
}
E2E_FLOW = {
    "name": "End to end flow", "slug": "cx-onb-e2e", "kicker": "Onboarding · single shot",
    "blurb": "The whole of onboarding in one run, from your mobile number to your home screen.",
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
