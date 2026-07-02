#!/usr/bin/env python3
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
BG = os.path.join(HOME, "assets/beagle")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
OUT = os.path.join(HOME, "oro-beagle-cx-walkthrough.html")

def B(fn): return os.path.join(BG, fn)

FLOWS = [
  {
    "name": "Book a gold loan visit", "slug": "beagle-book-visit", "kicker": "Book a visit",
    "blurb": "Find an Oro branch near you and schedule a visit to bring your gold.",
    "steps": [
      ("bg1-01-pincode.png", "Enter your pincode",
       "Enter your pincode so we can find Oro branches near you."),
      ("bg1-02-branch-loading.png", "Finding branches",
       "We're finding lender branches near you. Just a moment."),
      ("bg1-03-select-branch.png", "Pick a branch",
       "Pick the branch where you'd like to bring your gold."),
      ("bg1-04-schedule.png", "Choose a date and time",
       "Choose a date and time that work for your visit, then confirm."),
      ("bg1-05-confirmation.png", "Your visit is booked",
       "Your visit is booked — here are the date, time, and branch."),
    ],
  },
  {
    "name": "Get your gold loan", "slug": "beagle-get-loan", "kicker": "Visit & loan",
    "blurb": "From starting your branch visit to the money reaching your account — the whole gold loan journey.",
    "steps": [
      ("bg2-02-partner-assigned.png", "Start your visit",
       "Your Oro partner is assigned. When you reach the branch, tap Start Visit to begin — or call them if you need to."),
      ("bg2-03-arriving.png", "Your partner is on the way",
       "Your Oro partner is heading to the branch to help you — call them if you need to."),
      ("bg2-04-presence-loading.png", "Confirming you're here",
       "Your partner is confirming you're at the branch. Just a moment."),
      ("bg2-05-presence-success.png", "You're checked in",
       "You're checked in at the branch — you're all set to continue."),
      ("bg3-01-ekyc-success.png", "Your identity is verified",
       "Your identity is verified — you're ready to continue."),
      ("bg3-02-select-email.png", "Choose your email",
       "Choose the email where we'll send your updates, or add a new one."),
      ("bg3-03-select-nominee.png", "Choose your nominee",
       "Choose who you'd like as your nominee, or add a new one."),
      ("bg3-04-valuation-loading.png", "Checking your gold",
       "Your gold is being checked and valued. This won't take long."),
      ("bg3-05-valuation-success.png", "Your gold is valued",
       "Your gold has been checked and valued — tap to see your loan plans."),
      ("bg3-06-select-plan.png", "Choose your plan",
       "Choose the loan plan that suits you — compare the amount, interest, and more."),
      ("bg3-07-confirm-plan.png", "Review and confirm",
       "Review your chosen plan — the amount, interest, and charges — then confirm. Your gold's net weight already reflects a standard purity check."),
      ("bg3-08-select-bank.png", "Pick your bank account",
       "Pick the bank account where you'd like your loan money sent."),
      ("bg3-09-account-aggregator.png", "Link your bank securely",
       "Securely link your bank account so your loan can be paid out."),
      ("bg3-10-loan-purpose.png", "Tell us the loan's purpose",
       "Tell us what the loan is for, then confirm."),
      ("bg3-11-esign-docs-ready.png", "Your documents are ready",
       "Your loan documents are ready to sign — you can also get them in your language."),
      ("bg3-12-esign.png", "Sign your documents",
       "Sign your loan documents securely to continue."),
      ("bg3-13-esign-success.png", "You've signed",
       "You've signed — now we'll send it for the lender's approval."),
      ("bg3-14-lender-approval-pending.png", "Waiting for approval",
       "Your loan is with the lender for approval. This usually takes 5 to 10 minutes."),
      ("bg3-15-loan-approved.png", "Your loan is approved",
       "Your loan is approved! Here's your loan amount — the money will be sent next."),
      ("bg3-16-fund-transfer-pending.png", "Sending your money",
       "Your money is being sent to your account. Please keep the app open for a few minutes."),
      ("bg3-17-fund-transfer-success.png", "The money is on its way",
       "The money is on its way to your account — your gold loan is done!"),
    ],
  },
  {
    "name": "Manage your loan", "slug": "beagle-manage", "kicker": "Your loans",
    "blurb": "See all your loans and open any one for the full details.",
    "steps": [
      ("bg4-01-loan-list.png", "All your loans",
       "See all your loans in one place — active, closed, and renewed — and tap any one to open it."),
      ("bg4-02-loan-detail.png", "Your loan details",
       "Open a loan to see everything about it — your amount, payments, statements, and more."),
    ],
  },
]

flows = []
n = 0
for fl in FLOWS:
    steps = []
    for fn, title, caption in fl["steps"]:
        with open(B(fn), "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode("ascii")
        steps.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})
        n += 1
    flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                  "blurb": fl["blurb"], "steps": steps})

deck = [{"platform": "Customer App", "kicker": "Beagle · gold loan journey",
         "viewport": "mobile", "flows": flows}]

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_beagle.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
with open(OUT, "w") as f:
    f.write(html)

print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", n)
for fl in flows:
    print("  %-26s %2d  [%s]" % (fl["name"], len(fl["steps"]), fl["slug"]))
