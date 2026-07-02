#!/usr/bin/env python3
"""Append the comprehensive ELR partner journey (rebuilt from the ELR PX APP Figma
section, node 2665:172894) to the takeover partner group in field-apps.
Titles = real Figma frame names. Run AFTER build_takeover_px_brl.py.
Structure per Vivek: Storage-Partner -> Collect-CO -> Retrieval&Return -> Schedule Takeover."""
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HOME, "assets/elr-px-new")
DECK_FN = os.path.join(HOME, "oro-field-apps-walkthrough.html")

# (filename-stem, verbatim title). filename on disk is "<stem>.png"
S = {
 "e02-associated-visits": "Associated Visits",
 "e03-visit-details": "Visit details",
 "e04-upload-gold-photo": "Upload Gold Photo",
 "e05-uploaded": "Uploaded",
 "e07-store-at-cluster-office": "Store Gold at Cluster Office",
 "e08-select-cluster-office": "Select Cluster Office",
 "e09-tsv-created": "TSV Created",
 "e10-tsv-details": "TSV details",
 "e11-verifying-location": "Verifying visit location",
 "e12-location-verified": "Visit location verified",
 "e13-temporary-storage-visit": "Temporary Storage Visit",
 "e14-staff-verification": "Staff Verification",
 "e15-verify-partner": "Verify Partner",
 "e16-verifying-otp": "Verifying OTP",
 "e17-otp-verified": "OTP Verified",
 "e18-collect-gold-items": "Collect Gold Items",
 "e19-upload-gold-photo-co": "Upload Gold Photo",
 "e20-handover-gold-items": "Handover Gold Items",
 "e21-store-gold": "Store Gold",
 "e22-gold-stored": "Gold Stored",
 "e23-handover-completed-stored": "Handover completed Gold stored",
 "e24-retrieval-associated-visits": "Associated Visits",
 "e25-co-staff-retrieval-flow": "CO Staff Retrieval Flow",
 "e26-retrieval": "Retrieval",
 "e27-verify-partner-r": "Verify Partner",
 "e28-partner-verification": "Partner Verification",
 "e29-partner-live-photo": "Partner Live Photo",
 "e30-handover-gold-items-r": "Handover Gold Items",
 "e31-handover-gold": "Handover Gold",
 "e32-handover-completed": "Handover Completed",
 "e33-gold-collected": "Gold Collected",
 "e34-schedule-takeover": "Schedule Takeover",
 "e35-select-lender-branch": "Select Lender Branch",
 "e36-gl-appointment-booked": "GL Appointment Booked",
}

FLOWS = [
 ("Gold Storage — Partner", "elr-storage-partner", "ELR · storage",
  "After the ELR is scheduled: drop the gold at the cluster office.",
  ["e02-associated-visits","e03-visit-details","e04-upload-gold-photo","e05-uploaded",
   "e07-store-at-cluster-office","e08-select-cluster-office","e09-tsv-created","e10-tsv-details"]),
 ("Gold Collect — CO", "elr-collect-co", "ELR · CO staff",
  "Cluster-office staff receive and store the gold.",
  ["e11-verifying-location","e12-location-verified","e13-temporary-storage-visit","e14-staff-verification",
   "e15-verify-partner","e16-verifying-otp","e17-otp-verified","e18-collect-gold-items",
   "e19-upload-gold-photo-co","e20-handover-gold-items","e21-store-gold","e22-gold-stored",
   "e23-handover-completed-stored"]),
 ("Gold Retrieval & Return", "elr-retrieval-return", "ELR · retrieval",
  "Retrieve the stored gold and hand it back to the partner.",
  ["e24-retrieval-associated-visits","e25-co-staff-retrieval-flow","e26-retrieval","e27-verify-partner-r",
   "e28-partner-verification","e29-partner-live-photo","e30-handover-gold-items-r","e31-handover-gold",
   "e32-handover-completed","e33-gold-collected"]),
 ("Schedule Takeover", "elr-schedule-takeover", "ELR · schedule",
  "Book the takeover visit once the gold is released.",
  ["e34-schedule-takeover","e35-select-lender-branch","e36-gl-appointment-booked"]),
]

def datauri(stem):
    with open(os.path.join(ASSETS, stem + ".png"), "rb") as fp:
        return "data:image/png;base64," + base64.b64encode(fp.read()).decode("ascii")

new_flows = []
for name, slug, kicker, blurb, stems in FLOWS:
    steps = [{"img": datauri(st), "title": S[st], "caption": ""} for st in stems]
    new_flows.append({"name": name, "slug": slug, "kicker": kicker, "blurb": blurb, "steps": steps})

html = open(DECK_FN, encoding="utf-8").read()
s = html.index('const DECK'); b = html.index('[', s); d = 0
for i in range(b, len(html)):
    if html[i] == '[': d += 1
    elif html[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(html[b:i + 1])
gi = next(gi for gi, g in enumerate(deck)
          if g["platform"] == "Partner App" and any(f["slug"].startswith("tk-px") for f in g["flows"]))
# drop any previously-appended elr-* flows so re-runs are idempotent
deck[gi]["flows"] = [f for f in deck[gi]["flows"] if not f["slug"].startswith("elr-")]
deck[gi]["flows"].extend(new_flows)
deck[gi]["kicker"] = "Takeover · loan then gold release (BRL + ELR)"
# slug uniqueness
slugs = [f["slug"] for g in deck for f in g["flows"]]
dupes = {x for x in slugs if slugs.count(x) > 1}
assert not dupes, "dup slugs: %s" % dupes
new_html = html[:b] + json.dumps(deck, ensure_ascii=True) + html[i + 1:]
open(DECK_FN, "w", encoding="utf-8").write(new_html)
print("appended %d ELR flows to takeover group[%d]; total flows now %d | %.1f MB"
      % (len(new_flows), gi, len(deck[gi]["flows"]), len(new_html)/1024/1024))
for f in deck[gi]["flows"]:
    print("   [%s] %s (%d)" % (f["slug"], f["name"], len(f["steps"])))
