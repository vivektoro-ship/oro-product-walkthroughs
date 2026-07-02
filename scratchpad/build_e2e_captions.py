#!/usr/bin/env python3
"""Add agent-facing narration captions to the End-to-End flows (bg-e2e, tk-e2e).
Presenter is explaining TO the agent, so captions read as 'Agent does X' / 'Customer does X'."""
import json, os
FN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "oro-field-apps-walkthrough.html")
FN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "oro-field-apps-walkthrough.html"))

CAP = {
 # booking (customer, pre-visit)
 "Enter your pincode":"Customer enters their pincode to find nearby branches.",
 "Finding branches":"The app finds branches near the customer.",
 "Pick a branch":"Customer picks a branch.",
 "Choose a date and time":"Customer chooses a date and time.",
 "Your visit is booked":"Customer's visit is booked.",
 "Start from home":"Customer starts from the home screen.",
 "Checking lender branches":"The app checks the customer's lender branches.",
 "Choose your address":"Customer chooses their address.",
 "Pick a date and time":"Customer picks a date and time.",
 "See it in your visits":"Customer sees the booked visit in their list.",
 # agent visit start
 "Your visits":"Agent opens their assigned visits.",
 "My Visits":"Agent opens their assigned visits.",
 "Open the assigned visit":"Agent opens the assigned visit.",
 "Start the visit":"Agent starts the visit.",
 "Reached Visit Location":"Agent marks they've reached the visit location.",
 "Verifying visit location":"Agent's location is being verified.",
 "Visit location verified":"Agent's location is verified.",
 # customer app during visit
 "Start your visit":"Customer starts the visit on their phone.",
 "Your partner is on the way":"Customer sees the agent is on the way.",
 "Confirming you're here":"Customer's presence is being confirmed.",
 "You're checked in":"Customer is checked in.",
 "Your identity is verified":"Customer's identity is verified.",
 "Choose your email":"Customer chooses their email.",
 "Choose your nominee":"Customer chooses their nominee.",
 "Your visit details":"Customer sees their visit details.",
 "Your partner is assigned":"Customer sees their agent is assigned.",
 "Start your appointment":"Customer starts their appointment.",
 "You're verified":"Customer is verified.",
 "Ready for the next step":"Customer is ready for the next step.",
 # partner verify
 "Partner verification":"Agent verifies themselves.",
 "Partner photo captured":"Agent captures their selfie.",
 "Customer verification":"Agent verifies the customer.",
 "Customer Verification":"Agent verifies the customer.",
 "Verifying customer":"Agent runs the customer's verification.",
 "Customer photo captured":"Agent captures the customer's photo.",
 "Verification failed":"Verification fails — agent retries.",
 "Customer verified":"Customer is verified.",
 "Customer Verified":"Customer is verified.",
 "eKYC":"Agent runs the customer's eKYC.",
 "e-KYC":"Agent runs the customer's e-KYC.",
 "eKYC other details":"Agent fills the customer's other eKYC details.",
 "eKYC consent":"Agent takes the customer's eKYC consent.",
 "Customer signature":"Agent captures the customer's signature.",
 "Running the checks":"The checks run in the background.",
 "Error":"An error appears during the checks.",
 "Error details":"Agent reviews the error details.",
 "eKYC done":"eKYC is complete.",
 "Checking customer onboarding status":"Agent checks the customer's onboarding status.",
 "Onboarding completed by customer":"Customer has completed onboarding.",
 # co-borrower
 "Is there a co-borrower present?":"Agent checks if a co-borrower is present.",
 "Add Co-borrower":"Agent adds the co-borrower.",
 "Co-borrower OTP":"Agent verifies the co-borrower with an OTP.",
 # lender verification (takeover)
 "Give your consent":"Customer gives consent to fetch their loan details.",
 "Confirm it's you":"Customer confirms their identity.",
 "Confirm it’s you":"Customer confirms their identity.",
 "Details fetched":"The existing loan details are fetched.",
 "Next lender — give consent":"Customer gives consent for the next lender.",
 "Documents verified":"The customer's documents are verified.",
 # appraisal (partner)
 "Start gold valuation":"Agent starts the gold valuation.",
 "Bank appraisal details 1":"Agent enters the bank appraisal details.",
 "Bank appraisal sheet":"Agent uploads the bank appraisal sheet.",
 "Bank appraisal details 2":"Agent confirms the bank appraisal details.",
 "Security Details":"Agent reviews the security (collateral) details.",
 "Collateral Details":"Agent adds each collateral item.",
 "Carat Details":"Agent reviews the carat details of the appraised security.",
 "Parameter Details":"Agent adds the carat parameters.",
 "Consolidated Details":"Agent enters the consolidated weight details.",
 "Bank Appraisal Details":"Agent submits the bank appraisal details.",
 "Checking your gold":"Customer sees their gold being checked.",
 "Gold valuation completed":"Customer sees the valuation is complete.",
 # pledge card (takeover)
 "Upload Pledge Card":"Agent uploads the customer's pledge card.",
 "Reading Pledge Card":"The app reads the pledge card.",
 "Confirm Details":"Agent confirms the pledge card details.",
 "Pledge Cards":"Agent reviews the pledge cards.",
 "Confirm Release Amount":"Agent confirms the release amount.",
 # plan (partner)
 "Preview plan":"Agent previews the plan.",
 "Choose plan":"Agent chooses the plan.",
 "Confirm plan":"Agent confirms the plan.",
 "Plan selection in progress 1":"Plan selection is in progress.",
 "Plan selection in progress 2":"Plan selection continues.",
 "Add gold item (IG Tier 2) 1":"Agent adds gold items for IG Tier 2.",
 "Additionally for IG Tier 2 1":"Agent adds the additional IG Tier 2 details.",
 "Add gold item (IG Tier 2) 2":"Agent adds more gold items for IG Tier 2.",
 "Additionally for IG Tier 2 2":"Agent completes the additional IG Tier 2 details.",
 # plan / setup (customer)
 "Choose your plan":"Customer chooses their plan.",
 "Review and confirm":"Customer reviews and confirms.",
 "Pick your bank account":"Customer picks their bank account.",
 "Link your bank securely":"Customer links their bank securely.",
 "Tell us the loan's purpose":"Customer states the loan's purpose.",
 "Sharing your existing loan":"Customer shares their existing loan.",
 "Reviewing your loan":"The customer's loan is reviewed.",
 # esign
 "Your documents are ready":"Customer's documents are ready.",
 "Sign your documents":"Customer signs the documents.",
 "You've signed":"Customer has signed.",
 "eSign in progress":"Agent waits while the customer e-signs.",
 "Start signing":"Customer starts signing.",
 "Read your documents":"Customer reads their documents.",
 "Approval in progress":"Approval is in progress.",
 "Loan Approved":"The loan is approved.",
 "Customer eSign in progress":"Agent waits while the customer e-signs.",
 "Co-borrower eSign in progress":"Agent waits while the co-borrower e-signs.",
 "Bridge Loan e-Sign":"The bridge loan e-sign is complete.",
 # approval (beagle partner)
 "Submit for approval":"Agent submits the loan for approval.",
 "Loan moved to queue":"The loan moves to the ops queue.",
 "View in queue":"Agent views the loan in the queue.",
 "Waiting for approval":"Customer waits for approval.",
 "Your loan is approved":"Customer's loan is approved.",
 # fund transfer
 "Fund transfer in progress 1":"Fund transfer is in progress.",
 "Fund transfer in progress 2":"Fund transfer continues.",
 "Funds transferred":"Funds are transferred.",
 "Gold loan visit complete 1":"The gold loan visit is complete.",
 "Upload proof 1":"Agent uploads the disbursement proof.",
 "Upload proof 2":"Agent uploads more proof.",
 "Upload proof 3":"Agent uploads the proof.",
 "Upload proof 4":"Agent finishes uploading proof.",
 "Gold loan visit complete 2":"The gold loan visit is complete.",
 "Visit cancelled":"If it can't proceed, the agent cancels the visit.",
 "Sending your money":"Customer sees the money being sent.",
 "The money is on its way":"Customer sees the money is on its way.",
 "Upload Security Cheque":"Agent uploads the customer's security cheque.",
 "Fund Transfer in Progress":"Fund transfer is in progress.",
 "Fund Transfer Initiated":"Fund transfer initiated — agent uploads the transfer proof.",
 "Fund Transfer Completed":"Fund transfer is complete.",
 "The money is transferred":"Customer sees the money is transferred.",
 "Manage your new loan":"Customer manages their new loan.",
 # payment proof (takeover)
 "Checking":"The system runs a check.",
 "Payment Proof":"Agent uploads the payment proof to settle the old loan.",
 "Payment Proof Approved":"The payment proof is approved.",
 # manage
 "All your loans":"Customer views all their loans.",
 "Your loan details":"Customer views their loan details.",
 # release (beagle)
 "Your release visit":"Customer sees their release visit.",
 "Awaiting a partner":"Customer awaits an agent.",
 "Partner assigned":"An agent is assigned.",
 "Partner arriving soon":"Customer sees the agent arriving soon.",
 "Release in progress":"Release is in progress.",
 "Gold released":"The customer's gold is released.",
 "Start the release visit":"Agent starts the release visit.",
 "The release visit":"Agent opens the release visit.",
 "Verify the customer":"Agent verifies the customer.",
 "Visit progress":"Agent tracks the visit progress.",
 "Hand over the gold":"Agent hands over the gold to the customer.",
 "Capture the release document":"Agent captures the release document.",
 "Document captured":"The release document is captured.",
 "Release documents":"Agent reviews the release documents.",
 "Finish the visit":"Agent finishes the visit.",
 "Release visit complete":"The release visit is complete.",
 # queues
 "Your queues":"Team lead opens the queues.",
 "Open a loan's queues":"Team lead opens a loan's queues.",
 "See all the queues":"Team lead sees all the queues.",
 "No queues":"No queues remain.",
 # schedule ELR (takeover partner)
 "Schedule ELR":"Agent schedules the ELR (gold release).",
 "Schedule ELR Visit":"Agent sets the ELR visit details.",
 "Add ELR Address":"Agent adds the ELR visit address.",
 "Associated Visits":"Agent reviews the associated visits.",
 "BRL Visit Completed":"The BRL visit is complete.",
 # ELR customer
 "Open your release":"Customer opens their release.",
 "Your release visits":"Customer sees their release visits.",
 "Visit summary":"Customer sees the visit summary.",
 "Your pledge cards":"Customer sees their pledge cards.",
 "Your gold details":"Customer sees their gold details.",
 "Release completed":"Customer sees the release is complete.",
 "Moving to safe storage":"Customer sees the gold moving to safe storage.",
 "Safely stored":"Customer sees the gold is safely stored.",
 "Where your gold is":"Customer sees where their gold is.",
 "Retrieving your gold":"Customer sees their gold being retrieved.",
 "Gold retrieved":"Customer sees their gold is retrieved.",
 "Loan visit scheduled":"Customer sees the takeover loan visit is scheduled.",
 # storage / collect (partner + CO)
 "Visit details":"Agent opens the visit details.",
 "Upload Gold Photo":"Agent uploads a photo of the gold.",
 "Uploaded":"The gold photo is uploaded.",
 "Store Gold at Cluster Office":"Agent stores the gold at the cluster office.",
 "Select Cluster Office":"Agent selects the cluster office.",
 "TSV Created":"A temporary storage visit is created.",
 "TSV details":"Agent reviews the temporary-storage-visit details.",
 "Temporary Storage Visit":"CO staff open the temporary storage visit.",
 "Staff Verification":"CO staff verify themselves.",
 "Verify Partner":"CO staff verify the agent.",
 "Verifying OTP":"CO staff verify the OTP.",
 "OTP Verified":"The OTP is verified.",
 "Collect Gold Items":"CO staff collect the gold items.",
 "Handover Gold Items":"The gold items are handed over.",
 "Store Gold":"CO staff store the gold.",
 "Gold Stored":"The gold is stored.",
 "Handover completed Gold stored":"Handover complete — the gold is stored.",
 # retrieval / return
 "Retrieval":"Agent starts the gold retrieval.",
 "CO Staff Retrieval Flow":"CO staff open the retrieval flow.",
 "Partner Verification":"CO staff verify the agent.",
 "Partner Live Photo":"CO staff capture the agent's live photo.",
 "Handover Gold":"CO staff hand the gold back to the agent.",
 "Handover Completed":"The handover is complete.",
 "Gold Collected":"The gold is collected.",
 "Schedule Takeover":"Agent schedules the takeover GL visit.",
 "Select Lender Branch":"Agent selects the lender branch.",
 "GL Appointment Booked":"The GL appointment is booked.",
}

h = open(FN, encoding="utf-8").read()
s = h.index('const DECK'); b = h.index('[', s); d = 0
for i in range(b, len(h)):
    if h[i] == '[': d += 1
    elif h[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(h[b:i + 1])
n = miss = 0
missing = set()
for g in deck:
    for f in g['flows']:
        if f['slug'] in ('bg-e2e', 'tk-e2e'):
            for st in f['steps']:
                t = st['title']
                if t in CAP:
                    st['caption'] = CAP[t]; n += 1
                else:
                    who = 'Customer' if st.get('actor') == 'Customer' else 'Agent'
                    st['caption'] = "%s: %s." % (who, t); miss += 1; missing.add(t)
open(FN, "w", encoding="utf-8").write(h[:b] + json.dumps(deck, ensure_ascii=True) + h[i + 1:])
print("captioned %d from map, %d via fallback" % (n, miss))
if missing: print("fallback titles:", sorted(missing))
