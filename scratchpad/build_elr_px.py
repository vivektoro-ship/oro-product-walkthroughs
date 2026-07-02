#!/usr/bin/env python3
import base64, json, os, re

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
PX = os.path.join(HOME, "assets/elr-px")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
SRC = os.path.join(HOME, "oro-elr-cx-walkthrough.html")
OUT = SRC

def P(fn): return os.path.join(PX, fn)

src_html = open(SRC).read()
deck = json.loads(re.search(r'const DECK\s*=\s*(\[.*?\]);', src_html, re.S).group(1))
deck = [g for g in deck if g.get("platform") != "Partner App"]
for g in deck:
    g.setdefault("viewport", "mobile")

PARTNER = [
  {
    "name": "Collect the released gold", "slug": "elr-px-collect", "kicker": "Collect gold",
    "blurb": "The field partner collects the customer's gold from the old lender.",
    "steps": [
      ("px1-01-my-visits.png", "Open your visit",
       "Open the release visit assigned to you — you'll see each customer and the lenders to visit."),
      ("px1-02-visit-details.png", "Start the visit",
       "At the lender, review the visit details and pledge cards, then tap Start Visit."),
      ("px1-03-upload-collected.png", "Collect the gold",
       "Once the lender releases the gold, tap to upload a photo of what you've collected."),
      ("px1-04-capture-photo.png", "Photograph the gold",
       "Take a clear photo of the released gold items."),
      ("px1-05-uploaded.png", "Photo uploaded",
       "The gold photo is uploaded, with the total weight recorded."),
      ("px1-06-select-cluster.png", "Pick a cluster office",
       "Choose the nearest Oro Cluster Office to store the gold, then create the storage visit."),
      ("px1-07-tsv-created.png", "Storage visit created",
       "The temporary storage visit is created — you'll take the gold there next."),
    ],
  },
  {
    "name": "Store the gold at the cluster office", "slug": "elr-px-store", "kicker": "Storage visit",
    "blurb": "The partner takes the gold to the cluster office and hands it over for storage.",
    "steps": [
      ("px2-01-tsv-details.png", "At the cluster office",
       "At the cluster office, review the storage visit — the gold in custody and the staff you'll hand it to — then tap Reached."),
      ("px2-02-location-verified.png", "Location verified",
       "Your location at the cluster office is confirmed."),
      ("px2-03-staff-photo.png", "Verify the staff",
       "Take a live photo of the cluster-office staff to confirm who's receiving the gold."),
      ("px2-04-staff-otp.png", "Confirm with a code",
       "Enter the code from the cluster-office staff to verify them."),
      ("px2-05-otp-verified.png", "Staff verified",
       "The staff is verified — you can hand over the gold."),
      ("px2-06-handover-checklist.png", "Hand over the gold",
       "Go through the checklist and hand over each gold item to the staff."),
      ("px2-07-gold-stored.png", "Gold stored",
       "Handover complete — the gold is stored at the cluster office, to be collected back during the takeover visit."),
    ],
  },
  {
    "name": "Retrieve the gold", "slug": "elr-px-retrieve", "kicker": "Retrieve gold",
    "blurb": "The partner returns to the cluster office to collect the stored gold.",
    "steps": [
      ("px3-01-retrieval.png", "At the cluster office",
       "When it's time, go to the cluster office to retrieve the stored gold and tap Reached."),
      ("px3-02-location-verified.png", "Location verified",
       "Your location at the cluster office is confirmed."),
      ("px3-03-staff-otp-share.png", "Share your code",
       "Share the code shown here with the cluster-office staff so they can verify you."),
      ("px3-04-collect-gold.png", "Collect the gold",
       "Collect each gold item from the cluster-office staff."),
      ("px3-05-photo-uploaded.png", "Photograph the gold",
       "Photograph the collected gold to confirm what you've taken."),
      ("px3-06-gold-collected.png", "Gold collected",
       "The gold is collected and ready for the customer's loan."),
    ],
  },
  {
    "name": "Schedule the gold loan visit", "slug": "elr-px-schedule", "kicker": "Schedule GL",
    "blurb": "The partner books the takeover gold-loan visit to complete the move to Oro.",
    "steps": [
      ("px4-01-lender-select.png", "Pick the lender",
       "Start scheduling the takeover gold-loan visit by choosing the lender the customer is eligible with."),
      ("px4-02-lender-branch.png", "Pick the branch",
       "Choose the lender branch for the visit."),
      ("px4-03-date-time.png", "Pick a date and time",
       "Pick a date and time for the customer's gold-loan visit, then confirm."),
      ("px4-04-appointment-booked.png", "Visit booked",
       "The gold-loan visit is booked — the takeover can now be completed."),
    ],
  },
  {
    "name": "Cluster office: receive & store", "slug": "elr-px-co-store", "kicker": "Cluster office · store",
    "blurb": "The cluster-office staff receives the gold from the partner and stores it.",
    "steps": [
      ("px5-01-co-staff-view.png", "The storage queue",
       "The cluster-office staff sees the storage visits coming in — gold to receive, store, or that's been retrieved."),
      ("px5-02-verify-partner.png", "Verify the partner",
       "The staff shares a code with the partner to verify who's delivering the gold."),
      ("px5-03-collect-gold.png", "Collect the gold",
       "The staff collects each gold item from the partner."),
      ("px5-04-photo-uploaded.png", "Photo uploaded",
       "The staff photographs the gold being received."),
      ("px5-05-store-gold.png", "Store the gold",
       "The staff records the locker where the gold is stored and submits."),
      ("px5-06-gold-stored.png", "Gold stored",
       "The gold is stored and logged — its weight, photos, and locker — ready to hand back later."),
    ],
  },
  {
    "name": "Cluster office: hand back", "slug": "elr-px-co-handback", "kicker": "Cluster office · hand back",
    "blurb": "The cluster-office staff hands the stored gold back to the partner.",
    "steps": [
      ("px6-01-co-retrieval.png", "The retrieval queue",
       "When the partner returns, the cluster-office staff opens the retrieval to hand the gold back."),
      ("px6-02-verify-partner.png", "Verify the partner",
       "The staff verifies the partner before handing over the gold."),
      ("px6-03-partner-otp.png", "Confirm with a code",
       "The staff enters the code from the partner to verify them."),
      ("px6-04-otp-verified.png", "Partner verified",
       "The partner is verified — the gold can be handed back."),
      ("px6-05-handover-items.png", "Hand back the gold",
       "The staff hands each gold item back to the partner."),
      ("px6-06-handover-summary.png", "Handover complete",
       "Handover complete — the gold has left the cluster office, with weight, photos, and locker logged."),
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

deck.append({"platform": "Partner App", "kicker": "ELR · the partner & cluster-office side",
             "viewport": "mobile", "flows": partner_flows})

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_elr.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
open(OUT, "w").write(html)

total = sum(len(f["steps"]) for g in deck for f in g["flows"])
print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", total, "| partner added:", n)
for grp in deck:
    gs = sum(len(f["steps"]) for f in grp["flows"])
    print("\n== %s == [%s] (%d flows, %d screens)" % (grp["platform"], grp.get("viewport"), len(grp["flows"]), gs))
    for f in grp["flows"]:
        print("   %-36s %2d  [%s]" % (f["name"], len(f["steps"]), f["slug"]))
