#!/usr/bin/env python3
import base64, json, os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # handoff root
TK = os.path.join(HOME, "assets/takeover")
SCRATCH = os.path.dirname(os.path.abspath(__file__))  # this scratchpad/ folder
OUT = os.path.join(HOME, "oro-takeover-cx-walkthrough.html")

def T(fn): return os.path.join(TK, fn)

FLOWS = [
  {
    "name": "Book your visit", "slug": "takeover-book", "kicker": "Book a visit",
    "blurb": "Set up a branch visit to start shifting your gold loan to Oro.",
    "steps": [
      ("tk1-01-current-visits.png", "Your visits",
       "See your visits in one place. Tap your bridge loan visit to get started with shifting your gold loan to Oro."),
      ("tk1-02-select-address.png", "Choose your address",
       "Choose where you'd like your visit — pick a saved address or add a new one."),
      ("tk1-03-book-appointment.png", "Pick a date and time",
       "Pick a date and time that work for you, then confirm your appointment."),
      ("tk1-04-appointment-booked.png", "Your visit is booked",
       "Your visit is booked — here are the date, time, and place."),
    ],
  },
  {
    "name": "Your branch visit", "slug": "takeover-visit", "kicker": "Your visit",
    "blurb": "Meet your Oro partner and get verified to begin.",
    "steps": [
      ("tk2-01-visit-details.png", "Your visit details",
       "See your booked visit at a glance — date, time, and address. An Oro partner will be assigned to help you soon."),
      ("tk2-02-partner-assigned.png", "Your partner is assigned",
       "Your Oro partner is assigned — you can call them, and tap Start Visit when you're ready."),
      ("tk2-03-start-appointment.png", "Start your appointment",
       "From your home screen, tap Start to begin your loan appointment."),
      ("tk2-04-arriving.png", "Your partner is on the way",
       "Your Oro partner is on the way to meet you — call them if you need to."),
      ("tk2-05-presence-verified.png", "You're verified",
       "Your partner has confirmed you're together — you're all set to continue."),
      ("tk2-06-lender-verified.png", "Ready for the next step",
       "Your identity is confirmed and you're ready to start your lender verification."),
      ("tk2-07-stepper-1.png", "Your journey",
       "Here's your journey — verify yourself, complete the lender's check, pick a plan, get it approved, sign, and receive your money. You're on the first step."),
      ("tk2-08-stepper-2.png", "Pick up where you left off",
       "Your verification is done — next is the lender's check. You can pick up right where you left off anytime."),
    ],
  },
  {
    "name": "Verify with the lender", "slug": "takeover-verify", "kicker": "Lender check",
    "blurb": "A quick identity check with the lender funding your bridge loan.",
    "steps": [
      ("tk3-01-kyc-consent.png", "Give your consent",
       "Read and agree to let the lender check your identity and credit, then continue."),
      ("tk3-02-ckyc-otp.png", "Confirm it's you",
       "Enter the code sent to your phone to confirm it's you."),
      ("tk3-03-ckyc-success.png", "Details fetched",
       "Your details are fetched from the records — that part's done."),
      ("tk3-04-digilocker-success.png", "Documents verified",
       "Your documents are verified — you're ready for the next step."),
    ],
  },
  {
    "name": "Set up your loan", "slug": "takeover-setup", "kicker": "Loan setup",
    "blurb": "Add your details, link your bank, and choose your bridge loan plan.",
    "steps": [
      ("tk4-01-choose-email.png", "Choose your email",
       "Choose the email where we'll send your updates, or add a new one."),
      ("tk4-02-choose-nominee.png", "Choose your nominee",
       "Choose who you'd like as your nominee, or add a new one."),
      ("tk4-03-choose-bank.png", "Pick your bank account",
       "Pick the bank account where you'd like your loan money sent."),
      ("tk4-04-aa-sdk.png", "Link your bank securely",
       "Securely link your bank account so your loan can be paid out."),
      ("tk4-05-pledge-card.png", "Sharing your existing loan",
       "Your partner uploads your existing pledge card so we can shift your loan. Just a moment."),
      ("tk4-06-reviewing-loan.png", "Reviewing your loan",
       "We're reviewing your loan details. This won't take long."),
      ("tk4-07-choose-plan.png", "Choose your plan",
       "Choose the bridge loan plan that suits you — compare the amount, interest, and charges."),
      ("tk4-08-confirm-plan.png", "Review and confirm",
       "Review your bridge loan amount and confirm to go ahead."),
    ],
  },
  {
    "name": "Sign and get your money", "slug": "takeover-sign", "kicker": "Sign & funds",
    "blurb": "Sign your documents and watch the bridge loan pay off your old loan.",
    "steps": [
      ("tk5-01-esign-start.png", "Start signing",
       "Your bridge loan is approved — tap to sign your documents. You can also get them in your language."),
      ("tk5-02-esign-view.png", "Read your documents",
       "Read through your loan documents before you sign."),
      ("tk5-03-esign-success.png", "You've signed",
       "You've signed. If you have a co-borrower, you can send them a link to sign too."),
      ("tk5-04-fund-waiting.png", "Sending your money",
       "Your money is being sent. Please keep the app open for a few minutes."),
      ("tk5-05-fund-success.png", "The money is transferred",
       "The money is transferred — here's your bridge loan amount, which pays off your old loan."),
      ("tk5-06-loan-created.png", "Manage your new loan",
       "Your new loan is ready to manage — make payments, see receipts, and track everything here."),
      ("tk5-07-loan-closed.png", "Takeover complete",
       "All done — your old loan is now closed and the shift to Oro is complete."),
    ],
  },
]

flows = []
n = 0
for fl in FLOWS:
    steps = []
    for fn, title, caption in fl["steps"]:
        with open(T(fn), "rb") as fp:
            b64 = base64.b64encode(fp.read()).decode("ascii")
        steps.append({"img": "data:image/png;base64," + b64, "title": title, "caption": caption})
        n += 1
    flows.append({"name": fl["name"], "slug": fl["slug"], "kicker": fl["kicker"],
                  "blurb": fl["blurb"], "steps": steps})

deck = [{"platform": "Customer App", "kicker": "Takeover · shift your gold loan",
         "viewport": "mobile", "flows": flows}]

deck_json = json.dumps(deck, ensure_ascii=True)
fonts_css = open(os.path.join(SCRATCH, "fonts.css")).read()
template = open(os.path.join(SCRATCH, "template_takeover.html")).read()
html = template.replace("/*__FONTS__*/", fonts_css).replace("__DECK__", deck_json)
with open(OUT, "w") as f:
    f.write(html)

print("WROTE", OUT)
print("size MB: %.2f" % (os.path.getsize(OUT) / 1024 / 1024))
print("total screens:", n)
for fl in flows:
    print("  %-26s %2d  [%s]" % (fl["name"], len(fl["steps"]), fl["slug"]))
