#!/usr/bin/env python3
"""Rebuild the takeover-REVAMP (BRL) partner app flow from the new Figma section.
Titles are the REAL page titles (verbatim header, or body-status text for loan-ID
header screens). Captions intentionally empty (matches the beagle 'like this' pattern).
Patches the takeover Partner-App group in all three decks that carry it."""
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/takeover-px-brl")
DECKS = ["oro-takeover-cx-walkthrough.html",
         "oro-field-apps-walkthrough.html",
         "oro-all-flows-walkthrough.html"]

# NN -> real page title. Verbatim header where present; body-status text for the
# loan-ID-header screens (marked PENDING until the follow-up extraction lands).
TITLES = {
 "01": "My Visits",
 "02": "Reached Visit Location",              # loan-ID header -> body status
 "03": "Verifying visit location",
 "04": "Visit location verified",
 "05": "Checking customer onboarding status",
 "06": "Onboarding completed by customer",
 "07": "Customer Verification",
 "08": "Verifying customer",
 "09": "Customer Verified",
 "10": "Is there a co-borrower present?",
 "11": "Add Co-borrower",
 "12": "Add Co-borrower",
 "13": "Co-borrower OTP",
 "14": "Co-borrower OTP",
 "15": "(dropped)",                           # OMBV-only header, no body text -> removed from flow
 "16": "e-KYC",
 "17": "Upload Pledge Card",
 "18": "Reading Pledge Card",
 "19": "Confirm Details",
 "20": "Pledge Cards",
 "21": "Confirm Release Amount",
 "22": "Confirm Release Amount",
 "23": "Approval in progress", "24": "Loan Approved",
 "25": "Customer eSign in progress", "26": "Co-borrower eSign in progress",
 "27": "Bridge Loan e-Sign",
 "28": "Upload Security Cheque",
 "29": "Upload Security Cheque",
 "30": "Fund Transfer in Progress", "31": "Fund Transfer Completed",
 "32": "Checking",
 "33": "Upload Payment Proof",                 # design has double-space; normalised
 "34": "Upload Payment Proof",
 "35": "Upload Payment Proof",
 "36": "Payment Proof Approved",
 "37": "Schedule ELR",
 "38": "BRL Visit Completed",
}

# flow grouping (name/slug/kicker/blurb + ordered step NNs)
FLOWS = [
 ("Start the visit","tk-px-start","Visit start","Open the assigned visit and confirm you're at the location.",["01","02","03","04"]),
 ("Onboarding checks","tk-px-onboarding","Checks","Run the customer's onboarding checks before starting.",["05","06"]),
 ("Verify the customer","tk-px-verify","Verification","Verify the customer and run the required checks.",["07","08","09"]),
 ("Add the co-borrower","tk-px-coborrower","Co-borrower","Capture and verify the co-borrower.",["10","11","12","13","14"]),
 ("Pledge card & release","tk-px-pledge","Pledge card","Add the pledge card and confirm the release amount.",["16","17","18","19","20","21","22"]),
 ("Approval & e-sign","tk-px-approval","Approval","Get the lender's approval and have the customer sign.",["23","24","25","26","27"]),
 ("Transfer the funds","tk-px-funds","Fund transfer","Capture the security cheque and disburse the loan.",["28","29","30","31"]),
 ("Payment proof","tk-px-proof","Payment proof","Settle the old loan and upload proof.",["32","33","34","35","36"]),
 ("Schedule the release","tk-px-release","Release visit","Book the visit to collect the customer's gold.",["37","38"]),
]

def fname(nn):
    for f in os.listdir(ASSETS):
        if f.startswith(nn + "-") and f.endswith(".png"):
            return os.path.join(ASSETS, f)
    raise FileNotFoundError(nn)

def img_datauri(nn):
    with open(fname(nn), "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

def build_group():
    missing = [nn for nn, t in TITLES.items() if t is None]
    if missing:
        raise SystemExit("TITLES still pending for: " + ", ".join(sorted(missing)))
    flows = []
    for name, slug, kicker, blurb, nns in FLOWS:
        steps = [{"img": img_datauri(nn), "title": TITLES[nn], "caption": ""} for nn in nns]
        flows.append({"name": name, "slug": slug, "kicker": kicker, "blurb": blurb, "steps": steps})
    return {"platform": "Partner App", "kicker": "Takeover · what the partner does at the branch",
            "viewport": "mobile", "flows": flows}

def load_deck(html):
    s = html.index('const DECK'); b = html.index('[', s); d = 0
    for i in range(b, len(html)):
        if html[i] == '[': d += 1
        elif html[i] == ']':
            d -= 1
            if d == 0: break
    return b, i + 1, json.loads(html[b:i + 1])

def is_takeover_partner(g):
    slugs = {f["slug"] for f in g["flows"]}
    return g["platform"] == "Partner App" and ("tk-px-start" in slugs or "tk-px-pledge" in slugs)

grp = build_group()
for deck_fn in DECKS:
    path = os.path.join(HOME, deck_fn)
    html = open(path, encoding="utf-8").read()
    b, e, deck = load_deck(html)
    hit = [gi for gi, g in enumerate(deck) if is_takeover_partner(g)]
    if not hit:
        print("!! no takeover-partner group in", deck_fn, "- SKIPPED"); continue
    gi = hit[0]
    old = sum(len(f["steps"]) for f in deck[gi]["flows"])
    deck[gi] = grp
    new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[e:]
    open(path, "w", encoding="utf-8").write(new_html)
    print("%-34s group[%d] replaced: %d -> %d screens, %d flows | %.1f MB"
          % (deck_fn, gi, old, sum(len(f["steps"]) for f in grp["flows"]), len(grp["flows"]), len(new_html)/1024/1024))
print("DONE")
