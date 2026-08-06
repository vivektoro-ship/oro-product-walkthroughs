#!/usr/bin/env python3
"""Standardise the Onboarding titles and captions in the walkthrough decks.

Text only: no images are touched, no screens added, removed or reordered.
Screens are matched by flow slug + position, never by searching for old text.
The single-shot flow cx-onb-e2e repeats the same 30 screens in the same order,
so it gets the identical copy at positions 1-30.

Idempotent: it writes exact values, so a second run changes nothing.

    python3 scratchpad/fix_onboarding_copy.py
"""
import json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = [
    os.path.join(HOME, "oro-all-flows-walkthrough.html"),
    os.path.join(HOME, "oro-field-apps-walkthrough.html"),
]

# ------------------------------------------------------------------- copy ----
# Note: "Same as permanent address" (address 1) is deliberately sentence case
# and "use my current address" (bank 5) deliberately lower case — both match the
# labels printed on those screens. Do not tidy them into Title Case.

COPY = {
  "cx-onb-start": [
    ("Enter your mobile number",
     "Use the mobile number linked to your identity records, then tap Proceed."),
    ("Confirm it’s you",
     "Enter the four-digit code sent to your phone by WhatsApp or SMS, then tap Verify OTP."),
    ("Your number is verified",
     "Your mobile number is confirmed. Tap Proceed To Next Step."),
    ("Agree to the data checks",
     "Read what Oro collects and why, tick both boxes, then tap Proceed To Next Screen."),
    ("Choose your city",
     "Pick the city you are in. Oro works in these cities today."),
  ],
  "cx-onb-email": [
    ("Choose how to verify your email",
     "Verify with a code, or use Continue With Google. You can tap Skip Now and add it later."),
    ("Enter your email address",
     "Type your email address, then tap Get OTP. A six-digit code comes to that address."),
    ("Your email is verified",
     "Your email address is confirmed. Tap Proceed To Next Step."),
  ],
  "cx-onb-identity": [
    ("Allow camera access",
     "Allow access to your camera and location so the check can run. Tap Click To Allow."),
    ("Take a live photo",
     "Look straight, stay in the circle, and remove your glasses."),
    ("Your photo is accepted",
     "The live check is complete. Tap Proceed To Next Step."),
    ("Keep your documents handy",
     "You will need your identity card, your PAN card, a bank proof and an address proof. "
     "You are halfway through. Tap Proceed To Next Step."),
    ("Confirm your identity",
     "Bring your identity details across from your government document wallet. "
     "Tap Continue With Digilocker, the recommended method."),
    ("Your identity is verified",
     "Your identity details are confirmed and shown here. Tap Proceed To Next Step."),
  ],
  "cx-onb-details": [
    ("Add your father’s name",
     "Type your father’s name."),
    ("PAN details",
     "Enter the PAN number linked to your mobile number. Tap Verify PAN."),
    ("PAN verified",
     "Your PAN is confirmed. You are three quarters of the way through. "
     "Tap Proceed To Next Step."),
    ("Marital status",
     "Choose Single or Married. If you choose Married, add your spouse’s name."),
    ("Add your work details",
     "Choose your employment type, then enter your period of service."),
    ("Choose your income range",
     "Pick your annual household income, then tick the declaration below it."),
    ("Add your mother’s name",
     "Type your mother’s name as it appears on your identity card."),
  ],
  "cx-onb-address": [
    ("Add your current address",
     "Enter your pincode and full address. Tick Same as permanent address if the two are the same."),
    ("Address details",
     "Choose Rented or Own house, then add the year you moved in."),
    ("Almost done",
     "About two minutes left. Tap Proceed To Next Step."),
  ],
  "cx-onb-bank": [
    ("Bank account",
     "Confirm your account by sending ₹1 from a payment app. The ₹1 comes back once "
     "the check is done. Tap Verify With UPI."),
    ("Pick your payment app",
     "Choose the app you will send the ₹1 from."),
    ("Your bank account is added",
     "Your account is confirmed and shown here. Tap Proceed To Add Nominee, or tap Skip "
     "Nominee to add one later."),
    ("Add your nominee",
     "Add the name, age, mobile number and relationship of the person you would like as "
     "your nominee."),
    ("Add your nominee’s address",
     "Enter your nominee’s address, or tick use my current address to reuse the one you "
     "just entered."),
    ("You’re all set",
     "Your account is ready. Tap Proceed To Home Screen to start using Oro."),
  ],
}

# cx-onb-e2e repeats all 30 screens in this flow order.
E2E_SLUG = "cx-onb-e2e"
E2E_ORDER = ["cx-onb-start", "cx-onb-email", "cx-onb-identity",
             "cx-onb-details", "cx-onb-address", "cx-onb-bank"]

RENAMES = {
    "cx-onb-details": "Add your details",
    "cx-onb-address": "Add your address",
    "cx-onb-bank": "Add your bank and nominee",
}

BLURBS = {
    "cx-onb-start": "Verify your mobile number and pick your city.",
    "cx-onb-details": "Your family names, your PAN, your work and your income.",
}

# The two older single-shot groups use this kicker; match them.
E2E_KICKER_OLD = "Onboarding · single shot"
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


def flow_index(deck):
    out = {}
    for g in deck:
        for f in g["flows"]:
            out[f["slug"]] = (g, f)
    return out


def apply(path):
    html = open(path, encoding="utf-8").read()
    before = len(html)
    b, e = deck_bounds(html)
    deck = json.loads(html[b:e + 1])
    idx = flow_index(deck)

    # ---- verify everything the table expects is actually there -------------
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

    titles = captions = names = blurbs = kickers = 0

    def write_steps(slug, rows):
        nonlocal titles, captions
        steps = idx[slug][1]["steps"]
        for st, (title, caption) in zip(steps, rows):
            if st.get("title") != title:
                st["title"] = title
                titles += 1
            if st.get("caption") != caption:
                st["caption"] = caption
                captions += 1

    for slug, rows in COPY.items():
        write_steps(slug, rows)
    write_steps(E2E_SLUG, run)

    for slug, name in RENAMES.items():
        f = idx[slug][1]
        if f.get("name") != name:
            f["name"] = name
            names += 1

    for slug, blurb in BLURBS.items():
        f = idx[slug][1]
        if f.get("blurb") != blurb:
            f["blurb"] = blurb
            blurbs += 1

    for g in deck:
        if g.get("_product") == "Onboarding" and g.get("kicker") == E2E_KICKER_OLD:
            g["kicker"] = E2E_KICKER_NEW
            kickers += 1

    new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[e + 1:]
    open(path, "w", encoding="utf-8").write(new_html)
    return dict(titles=titles, captions=captions, names=names, blurbs=blurbs,
                kickers=kickers, before=before, after=len(new_html))


if __name__ == "__main__":
    for path in DECKS:
        r = apply(path)
        print("\n%s" % os.path.basename(path))
        print("  titles changed   : %d" % r["titles"])
        print("  captions changed : %d" % r["captions"])
        print("  flow renames     : %d" % r["names"])
        print("  blurbs changed   : %d" % r["blurbs"])
        print("  kickers changed  : %d" % r["kickers"])
        print("  bytes %d -> %d  (%+d)" % (r["before"], r["after"], r["after"] - r["before"]))
