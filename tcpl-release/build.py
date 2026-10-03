#!/usr/bin/env python3
"""Builds index.html for the TCPL release visit walkthrough.

Screens are 2x Figma exports (third-party partner screens at 1.48x, the
section is wider than Figma's export cap) from file T5JDdFqTJVi2pgTGeCzU3S,
sections 2639:65883 (customer app), 2639:70726 (partner app, normal release)
and 2639:74066 (partner app, third-party release). Spec: ENG-5409.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent

# id -> (app, section label, title, caption)
S = {
# ---------------- customer app: booking ----------------
'2660-16517': ('cx','Loan closed','Loan closed, release pending','The gold loan shows the new status Loan closed – release pending. Schedule release visit is available directly from the manage loan page.'),
'2639-68742': ('cx','Loan closed','Foreclosure request accepted','The customer’s foreclosure request is accepted. Make payment now starts the closure and release booking.'),
'2639-68958': ('cx','Book the visit','Pay closure amount','The full closure amount is shown with its breakup: gold loan, personal loan and charges.'),
'2639-67605': ('cx','Book the visit','Schedule release','The release address is the Tenmark branch and cannot be changed. The customer picks a date.'),
'2639-67047': ('cx','Book the visit','Choose a time slot','Slots are grouped into morning, afternoon and evening.'),
'2639-68052': ('cx','Book the visit','Confirm and pay','Date and time are set. Confirm & make payment moves to checkout.'),
'2639-68673': ('cx','Book the visit','Choose payment method','UPI, debit card, net banking or NEFT/RTGS/IMPS.'),
'2639-68519': ('cx','Book the visit','Payment received','The release appointment is booked. The Release Visit card shows Visit confirmed with date, time and branch. Proceed to home screen continues.'),
'2639-65884': ('cx','Book the visit','Home: release appointment','On visit day the home screen carries a Start Appointment strip for the release visit.'),
'2639-66252': ('cx','Book the visit','Home: release appointment','On visit day the home screen carries a Start Appointment strip for the release visit.'),
# ---------------- customer app: visit ----------------
'2639-66620': ('cx','At the branch','Release visit: partner not yet assigned','Visit ID, date, time, branch location and loan IDs. The partner card waits for a Tenmark partner to pick up the visit.'),
'2639-66682': ('cx','At the branch','Release visit: partner not yet assigned','Visit ID, date, time, branch location and loan IDs. The partner card waits for a Tenmark partner to pick up the visit.'),
'2639-66744': ('cx','At the branch','Partner assigned','Once a partner self-assigns, their name and call button appear on the visit.'),
'2639-66818': ('cx','At the branch','Partner assigned','Once a partner self-assigns, their name and call button appear on the visit.'),
'2639-69024': ('cx','At the branch','Your visit is being started','Shown while the partner selects the release path and verifies presence at the branch.'),
'2639-69046': ('cx','At the branch','Your visit is being started','Shown while the partner selects the release path and verifies the third party at the branch.'),
'2639-66892': ('cx','Gold verification','Your gold release is in progress','Shown while the partner verifies every gold item against the valuation record.'),
'2639-66955': ('cx','Gold verification','Your gold release is in progress','Shown while the partner verifies gold items after central approval.'),
'2639-69130': ('cx','Gold verification','Your gold release is in progress','Status the customer sees between steps of the release.'),
'2639-66934': ('cx','Third party','Third party release eSign in progress','The customer is told a third party is collecting and signing the declaration at the branch. The customer does not sign on this path.'),
# ---------------- customer app: eSign + completion ----------------
'2639-69177': ('cx','eSign','Start eSign','Normal release only. The customer signs the release document from their own app using Aadhaar OTP.'),
'2639-69228': ('cx','eSign','Release document','The release document lists loan details, items released, condition of collateral, discharge and declaration. It can be read before signing.'),
'2639-66913': ('cx','eSign','eSign in progress','Shown while the Aadhaar OTP signature is processed.'),
'2639-67031': ('cx','eSign','eSign failed','A failed eSign can be retried. The flow resumes without creating a duplicate document.'),
'2639-69151': ('cx','eSign','eSign Completed','“Your release document has been signed. Please collect your gold items from the partner.”'),
'2639-69068': ('cx','Gold released','Congratulations: gold released','“Your gold has been successfully released.” Visit ID, gold loan ID and personal loan ID are shown with the handover photo. Go back to home closes the visit.'),
'2639-69099': ('cx','Gold released','Congratulations: gold released','The same completion screen on the third-party path, with the handover photo and loan IDs. Go back to home closes the visit.'),
# ---------------- customer app: rejection / blocked ----------------
'2639-70675': ('cx','Rejected','Third party release rejected','The approver’s rejection reason is shown. Reschedule visit lets the customer book a fresh visit at no extra charge.'),
'2639-69787': ('cx','Reschedule','Schedule release','The customer picks a new date. The appointment address stays fixed at the branch.'),
'2639-69252': ('cx','Reschedule','Choose a time slot','Same slot picker as the first booking.'),
'2639-70221': ('cx','Reschedule','Confirm new slot','Date and time are set. Confirm & make payment books the new visit; the closure amount is already paid and is not charged again.'),
'2639-70702': ('cx','Reschedule','Release Visit Booked','A new visit is created with a new visit ID. It starts from zero: fresh pickup, verification and gold check, on either path. Back to home returns to the home screen.'),
'2639-66976': ('cx','Blocked','Release blocked','Shown when any gold item is marked not matched. The customer sees a generic technical message; the mismatch reason is not shown.'),
'2639-66996': ('cx','Cancelled','Release cancelled','Shown when the visit is cancelled. The customer is told the team will get back shortly.'),
# ---------------- partner app: pickup (shared ids per section) ----------------
'2639-71180': ('px','Pickup','My Visits','The Tenmark partner sees release visits in My Visits with status chips. Confirmed visits are ready to pick up.'),
'2639-74397': ('px','Pickup','My Visits','The Tenmark partner sees release visits in My Visits with status chips. Confirmed visits are ready to pick up.'),
'2639-70727': ('px','Pickup','Release visit detail','Branch, visit time, customer and gold details (5 items, 100 g). The partner drags Start Visit to begin.'),
'2639-74103': ('px','Pickup','Release visit detail','Branch, visit time, customer and gold details (5 items, 100 g). The partner drags Start Visit to begin.'),
'2639-70784': ('px','Pickup','Self-assign this release visit?','Confirm assigns the visit to this partner for its lifetime. Cancel goes back.'),
'2639-74160': ('px','Pickup','Self-assign this release visit?','Confirm assigns the visit to this partner for its lifetime. Cancel goes back.'),
'2639-70854': ('px','Pickup','Visit self-assigned','A green toast confirms the assignment.'),
'2639-74230': ('px','Pickup','Visit self-assigned','A green toast confirms the assignment.'),
'2639-70910': ('px','Pickup','Start Visit','The visit is now owned by this partner.'),
'2639-74286': ('px','Pickup','Start Visit','The visit is now owned by this partner.'),
'2639-70964': ('px','Pickup','Visit already started','Any other partner opening the visit sees who started it. Self-assign is not available to them.'),
'2639-74340': ('px','Pickup','Visit already started','Any other partner opening the visit sees who started it. Self-assign is not available to them.'),
'2639-71718': ('px','Pickup','Gold details','Read-only record of the latest valuation: item count, weights, 22C net weight and locker number.'),
'2639-74681': ('px','Pickup','Gold details','Read-only record of the latest valuation: item count, weights, 22C net weight and locker number.'),
'2639-71661': ('px','Pickup','Item details','Per item: weights, gold markings, valuation remarks and the valuation photo set.'),
'2639-74624': ('px','Pickup','Item details','Per item: weights, gold markings, valuation remarks and the valuation photo set.'),
# ---------------- partner app: normal path ----------------
'2639-71444': ('px','Release path','Select Release Path: Regular Release','The path is chosen before verification, because the two paths verify differently.'),
'2639-71021': ('px','Customer verification','Visit stepper','Three steps: Customer Verification, Gold Verification, Gold Handover.'),
'2773-27953': ('px','Customer verification','Customer live photo','The customer must be inside the visit location. The photo is used for face match and geolocation.'),
'2773-27933': ('px','Customer verification','Photo captured','The partner confirms the captured photo.'),
'2773-27925': ('px','Customer verification','Verifying customer presence','Face match against the onboarding photo and a geolocation check run together.'),
'2639-71867': ('px','Customer verification','Verification failed: far from branch','If the location check fails the partner must be inside the branch and try again.'),
'2639-71849': ('px','Customer verification','Verification failed: face mismatch','If the face does not match the record, the partner recaptures the photo.'),
'2773-27973': ('px','Customer verification','Customer presence verified','Both checks passed.'),
'2639-71074': ('px','Customer verification','Step 1 completed','Customer Verification is marked completed on the stepper.'),
'2639-71431': ('px','Release type','Release type: Full Release','Full Release is the only option and is preselected. It is recorded against the visit.'),
'2639-71461': ('px','Gold verification','Gold verification listing','Every item is under Pending verification and progress reads 0 of 5 items verified. Start Verification opens the first item.'),
'2639-71534': ('px','Gold verification','Gold items summary','Expanded summary: item count, gross weight, deduction, net weight and 22C net weight.'),
'2639-71878': ('px','Gold verification','Verify gold item','The partner compares the item with its valuation photos, weights, markings and remarks. Matched or Not matched.'),
'2639-72096': ('px','Gold verification','Capture gold item','A photo is mandatory before the item can be marked either way.'),
'2639-72111': ('px','Gold verification','Item captured','The item must sit fully inside the frame.'),
'2639-72126': ('px','Gold verification','Mark as matched','Add more photos and item remarks, then confirm.'),
'2639-72383': ('px','Gold verification','You marked as item matched','The verification image shows as Uploaded. Mark as not matched can still reverse the outcome before submission.'),
'3036-63625': ('px','Gold verification','Item marked as matched','A toast confirms and the app returns to the listing. The partner picks the next item.'),
'2639-72146': ('px','Gold verification','5 of 5 items verified','Complete Verification enables only when every item has an outcome.'),
'2639-72220': ('px','Gold verification','Complete verification?','After submission the outcome cannot be edited in the app.'),
'2639-72303': ('px','Gold verification','Verification completed','All items matched.'),
'2639-71127': ('px','Gold verification','Step 2 completed','Customer and gold verification are complete; handover is next.'),
'2639-71407': ('px','eSign','Customer eSign in progress','The customer signs the release document in their own app. Check status refreshes.'),
'2639-71419': ('px','eSign','Customer eSign completed','“Hand over the gold items to the customer.” Handover Gold moves to the release proof.'),
'2639-71609': ('px','Handover','Release proof','Photo of the customer holding the gold items. Mandatory: this is the proof of receipt.'),
'2639-71622': ('px','Handover','Release proof captured','Face and items must both be clearly visible.'),
'2639-71635': ('px','Handover','Congratulations: release visit complete','Visit ID and loan ID are shown. Go back to home ends the visit. CORE and Oro Admin show Release completed.'),
# ---------------- partner app: third-party path ----------------
'2639-74067': ('px','Release path','Select Release Path: Third Party Release','Used when the customer cannot collect in person: deceased, missing, abroad or unwell.'),
'3716-83576': ('px','Third party verification','Visit stepper','Step 1 becomes Third Party Verification.'),
'2773-28144': ('px','Third party verification','Third party live photo','Geolocation only. There is no face match, since the customer is not present.'),
'2773-28124': ('px','Third party verification','Photo captured','The partner confirms the captured photo.'),
'2773-28164': ('px','Third party verification','Verifying third party presence','Geolocation check against the branch.'),
'2639-74092': ('px','Third party verification','Verification failed: far from branch','The partner must be inside the branch and try again.'),
'2773-28274': ('px','Third party verification','Third party presence verified','Location confirmed.'),
'2639-74882': ('px','Third party details','Third party details','Relationship to the customer, mobile number and email. All fields are mandatory.'),
'2639-74894': ('px','Third party details','Details filled','Relationship is picked from a fixed list (25 values, with Other as free text).'),
'3732-13892': ('px','Third party details','Verify email OTP','A 4-digit OTP is sent to the third party’s email.'),
'3732-13919': ('px','Third party details','OTP entered','Resend becomes available after 30 seconds.'),
'3732-13952': ('px','Third party details','Verifying OTP','The 4-digit code is checked.'),
'3732-13988': ('px','Third party details','OTP Verified!','The third party’s email is confirmed. Start Visit continues to DigiLocker.'),
'3732-14183': ('px','Third party details','Invalid OTP','A wrong code can be retried.'),
'2639-74906': ('px','DigiLocker','DigiLocker Verification','“Get your documents from DigiLocker.” The third party taps Start and signs in with their Aadhaar-linked mobile. Name, age, address, PAN and Aadhaar are fetched.'),
'3732-13836': ('px','DigiLocker','Unable to verify','Shown if DigiLocker verification cannot be completed. The partner can try again.'),
'2639-74926': ('px','DigiLocker','Third party identity verified','DigiLocker confirmed the third party’s identity. Proceed to next opens Upload Documents.'),
'2639-75047': ('px','Documents','Reason for release','Four reasons: Death Case, customer deceased · Customer Missing · Regular Third Party, customer abroad or out of city · Regular Third Party, customer sick or hospitalised.'),
'2639-75108': ('px','Documents','Death case: details','Customer death date, death certificate and legal heir certificate or family tree.'),
'2639-75066': ('px','Documents','Upload option','Capture with camera, upload from gallery or add a file.'),
'2639-75211': ('px','Documents','Document upload','Several pages can be added per document and removed before upload.'),
'2639-75124': ('px','Documents','Documents uploaded','Each document shows the number of files uploaded.'),
'2639-75139': ('px','Documents','Death case: complete','Every document for the reason is uploaded; all are mandatory. Submit for approval first takes the collector to the declaration eSign.'),
'2639-75155': ('px','Documents','Customer missing','Missing-since date, FIR number, FIR date, police station, FIR copy, non-traceable report and legal heir certificate.'),
'2639-75175': ('px','Documents','Customer abroad or out of city','Request letter date, emailed request, signed letter, video call confirmation and travel ticket or visa.'),
'2639-75193': ('px','Documents','Customer sick or hospitalised','Request letter date, emailed request, signed letter, video call confirmation and medical certificate.'),
'2639-74940': ('px','Declaration eSign','Third party release eSign','The collector reads the release documents and taps Start e-sign to sign the declaration-cum-indemnity on the partner’s device with Aadhaar OTP.'),
'2639-74980': ('px','Declaration eSign','Declaration view','The declaration covers the release reason, collector details and items released.'),
'3349-83094': ('px','Declaration eSign','Release eSign in progress','A timer shows while the signature is processed.'),
'3349-83141': ('px','Declaration eSign','Release eSign failed','A failed signature can be retried.'),
'2639-74991': ('px','Declaration eSign','Release eSign completed','The declaration is signed. Submit for approval sends the visit to Tenmark CORE.'),
'2639-75004': ('px','Approval','Submit for approval?','The approver reviews the documents and the signed declaration. Nothing can be changed after sending.'),
'2639-74870': ('px','Approval','Approval in progress','The gold cannot be handed over until a Tenmark approver acts in CORE.'),
'2639-74794': ('px','Approval','Approval in progress','The pending state survives a session gap; Check status refreshes it.'),
'2639-76076': ('px','Approval','Third party release rejected','The approver’s reason is shown. The visit closes and the customer can reschedule.'),
'2639-74806': ('px','Approval','Third party release approved','Approved in CORE. The visit continues to release type and gold verification.'),
'2639-74817': ('px','Approval','Step 1 completed','Third Party Verification is completed.'),
'2639-75287': ('px','Release type','Release type: Full Release','Selected after approval on this path.'),
'2639-75300': ('px','Gold verification','Gold verification listing','Runs after approval, identical to the normal path.'),
'2639-75373': ('px','Gold verification','Gold items summary','Item count and weights against the latest valuation.'),
'2639-75500': ('px','Gold verification','Verify gold item','Compare with the valuation photo set, then mark matched or not matched.'),
'2639-76005': ('px','Gold verification','You marked as item matched','Mark as not matched can still reverse the outcome before submission.'),
'2639-75718': ('px','Gold verification','Capture gold item','A photo is mandatory for both outcomes.'),
'2639-75733': ('px','Gold verification','Item captured',''),
'2639-75748': ('px','Gold verification','Mark as matched','Photos and remarks are saved with the item.'),
'3036-63744': ('px','Gold verification','Item marked as matched','The app returns to the listing.'),
'2639-75768': ('px','Gold verification','5 of 5 items verified','Complete Verification is now enabled.'),
'2639-75842': ('px','Gold verification','Complete verification?',''),
'2639-75925': ('px','Gold verification','Verification completed','All items matched.'),
'2639-75234': ('px','Gold verification','Step 2 completed','Handover is next. The declaration is already signed, so no customer eSign is needed.'),
'2639-75448': ('px','Handover','Release proof','Photo of the person collecting, holding the gold items. Tagged with their role.'),
'2639-75461': ('px','Handover','Release proof captured',''),
'2639-75474': ('px','Handover','Congratulations: release visit complete','Visit ID and loan ID are shown. Go back to home ends the visit. CORE and Oro Admin show Release completed.'),
}

def L(s): return s.split()

BOOK = L('2660-16517 2639-68742 2639-68958 2639-67605 2639-67047 2639-68052 2639-68673 2639-68519')
PX_PICK = L('2639-71180 2639-70727 2639-70784 2639-70854 2639-70910')
PX_PICK_T = L('2639-74397 2639-74103 2639-74160 2639-74230 2639-74286')

FLOWS = [
 # group, key, tab label, intro, ids
 ('e2e','e2e-normal','Normal release','The customer closes the loan and books a visit, the partner verifies the customer and every gold item, the customer eSigns in their app, and the partner hands over the gold.',
  BOOK + L('2639-65884 2639-66620') + PX_PICK + L('2639-66744 2639-69024 2639-71444 2639-71021 2773-27953 2773-27933 2773-27925 2773-27973 2639-71074 2639-71431 2639-66892 2639-71461 2639-71878 2639-72096 2639-72111 2639-72126 3036-63625 2639-72146 2639-72220 2639-72303 2639-71127 2639-71407 2639-69177 2639-69228 2639-66913 2639-69151 2639-71419 2639-71609 2639-71622 2639-71635 2639-69068')),
 ('e2e','e2e-tp','Third-party release','The customer cannot attend. A third party verifies at the branch, uploads the reason documents and signs the declaration. A Tenmark approver reviews and approves in CORE, then gold verification and handover follow.',
  BOOK + L('2639-66252 2639-66682') + PX_PICK_T + L('2639-66818 2639-69046 2639-74067 3716-83576 2773-28144 2773-28124 2773-28164 2773-28274 2639-74882 2639-74894 3732-13892 3732-13919 3732-13952 3732-13988 2639-74906 2639-74926 2639-75047 2639-75108 2639-75066 2639-75211 2639-75124 2639-75139 2639-74940 2639-66934 2639-74980 2639-74991 2639-75004 2639-74870 2639-76439 2639-76669 2639-77648 2639-78443 2639-74806 2639-74817 2639-75287 2639-66955 2639-75300 2639-75500 2639-75718 2639-75733 2639-75748 3036-63744 2639-75768 2639-75842 2639-75925 2639-75234 2639-75448 2639-75461 2639-75474 2639-69099')),
 ('e2e','e2e-reject','Third party rejected','The approver rejects in CORE with a reason and the visit closes. The payment and the closed ledger stay as they are, and the customer books a new visit from zero.',
  L('2639-75004 2639-74870 2639-77417 2639-77881 2639-78156 2639-78676 2639-80702 2639-76076 2639-70675 2639-69787 2639-69252 2639-70221 2639-70702')),
 ('cx','cx-book','Booking','From loan closure to a confirmed release visit.', BOOK + L('2639-65884')),
 ('cx','cx-normal','Normal release','What the customer sees during a normal release, including their own eSign.',
  L('2639-66620 2639-66744 2639-69024 2639-66892 2639-69177 2639-69228 2639-66913 2639-67031 2639-69151 2639-69130 2639-69068')),
 ('cx','cx-tp','Third-party release','What the customer sees while a third party collects on their behalf. The customer does not sign.',
  L('2639-66252 2639-66682 2639-66818 2639-69046 2639-66934 2639-66955 2639-69099')),
 ('cx','cx-end','Rejected, blocked, cancelled','The three ways a release can stop, and how the customer reschedules after a rejection.',
  L('2639-70675 2639-69787 2639-69252 2639-70221 2639-70702 2639-66976 2639-66996')),
 ('px','px-normal','Normal release','Tenmark Partner App, regular path with all items matched. Edge screens are included where they occur.',
  PX_PICK + L('2639-70964 2639-71718 2639-71661 2639-71444 2639-71021 2773-27953 2773-27933 2773-27925 2639-71867 2639-71849 2773-27973 2639-71074 2639-71431 2639-71461 2639-71534 2639-71878 2639-72096 2639-72111 2639-72126 2639-72383 3036-63625 2639-72146 2639-72220 2639-72303 2639-71127 2639-71407 2639-71419 2639-71609 2639-71622 2639-71635')),
 ('px','px-tp','Third-party release','Tenmark Partner App, third-party path: details, DigiLocker, reason documents for all four reasons, declaration eSign, approval, gold verification and handover.',
  PX_PICK_T + L('2639-74340 2639-74681 2639-74624 2639-74067 3716-83576 2773-28144 2773-28124 2773-28164 2639-74092 2773-28274 2639-74882 2639-74894 3732-13892 3732-13919 3732-13952 3732-13988 3732-14183 2639-74906 3732-13836 2639-74926 2639-75047 2639-75108 2639-75066 2639-75211 2639-75124 2639-75139 2639-75155 2639-75175 2639-75193 2639-74940 2639-74980 3349-83094 3349-83141 2639-74991 2639-75004 2639-74870 2639-74794 2639-76076 2639-74806 2639-74817 2639-75287 2639-75300 2639-75373 2639-75500 2639-76005 2639-75718 2639-75733 2639-75748 3036-63744 2639-75768 2639-75842 2639-75925 2639-75234 2639-75448 2639-75461 2639-75474')),
]

# ---------------- Tenmark CORE (admin) ----------------
S.update({
'2639-81789': ('core','Visits','All Visits','Every release visit with a status filter bar: Release confirmed, Release assigned, Release in progress, Release completed, Release cancelled. Columns: visit ID and date, customer and mobile, assigned agent, loan amount and ID, visit status.'),
'2639-78951': ('core','Visit detail','Visit details: release in progress','Release details, customer, assigned agent and the Gold Verification Details list with each item’s Matched status. Normal releases are view-only in CORE.'),
'2639-79720': ('core','Visit detail','Item detail: matched','Gold verification status, remarks, weights and the valuation photo set. View images opens the full-height viewer.'),
'2639-80033': ('core','Visit detail','Release completed','The visit status changes to Release completed once the partner captures the release proof.'),
'2639-82913': ('core','Activity log','Activity log: normal release','Every event with actor and timestamp, earliest first, with Export. One line per item verified.'),
'2639-79173': ('core','Item mismatch','Release blocked','“Release blocked due to a gold item mismatch. 2 items were marked as not matched.” The not-matched item is flagged in red in the list.'),
'2639-79400': ('core','Item mismatch','Item detail: not matched','Not matched reasons, remarks and the captured images. There is no action to unblock in CORE; resolution is manual.'),
'2639-82651': ('core','Approval','All Loans: Release approval pending','The Release approval pending tab lists loans waiting for a third-party decision. The approver opens one from here.'),
'2639-81157': ('core','Approval','All Visits','The same visit sits in the Gold Release Visits list.'),
'2639-76095': ('core','Approval','Visit details: release assigned','Before submission the visit shows Release assigned, with release details, customer and assigned agent.'),
'2639-76439': ('core','Approval','Third party release requires approval','A blue banner appears once the partner submits. Review Documents opens the Release Documents tab.'),
'2639-76669': ('core','Approval','Release Documents: death case','Release details, third party details, customer live photo, release proof and every uploaded document. Reject and Approve sit in the banner.'),
'2639-77281': ('core','Approval','Document viewer','Any image opens at full height with zoom, rotate and next/previous.'),
'2639-77648': ('core','Approval','Approve the release?','No reason is needed to approve. Cancel or Approve.'),
'2639-78443': ('core','Approval','Release approved','The visit moves to Release in progress and the partner continues to gold verification. Done closes the dialog.'),
'2639-83085': ('core','Activity log','Activity log: third-party release','Third party category, details, each document upload and the approval submission are logged with actor and time.'),
'2639-76797': ('core','Reason documents','Customer passed away','Release reason Death Case, customer deceased, with the customer passed away date and the death certificate set.'),
'2639-76925': ('core','Reason documents','Customer is missing','Missing-since date, FIR number, FIR date and police station, with the FIR and supporting documents.'),
'2639-77062': ('core','Reason documents','Customer is out of station or sick','Customer’s request letter date with the request letter, video call confirmation and travel or medical proof.'),
'2639-77190': ('core','Reason documents','Release Documents after a decision','Once decided, the tab shows the same documents without the approval banner.'),
'2639-81473': ('core','Rejection','All Visits','The approver opens a visit waiting for approval.'),
'2639-76267': ('core','Rejection','Visit details','Release details and the assigned agent.'),
'2639-77417': ('core','Rejection','Third party release requires approval','Approve and Reject are available to users with the Approve Third Party Release permission.'),
'2639-77881': ('core','Rejection','Reject the release?','Cancel or Reject.'),
'2639-78156': ('core','Rejection','Reject Third Party Release','A reason is mandatory. Confirm records it with the approver and time.'),
'2639-78676': ('core','Rejection','Release rejected','Done closes the dialog. The visit becomes Release cancelled; payment and ledger are unchanged.'),
'2639-80474': ('core','Rejection','Rejected banner','“Third party release rejected by <approver> on <date, time>.” View Reason shows why.'),
'2639-80702': ('core','Rejection','Rejected Reason','The reason entered by the approver. The customer sees the same reason with Reschedule visit.'),
'2639-82197': ('core','Loan status','Loan closed release pending','From closure payment until the release completes, the gold loan shows Loan closed release pending.'),
'2639-82424': ('core','Loan status','Loan closed','After the release visit completes, the loan moves to Loan closed.'),
})
FLOWS += [
 ('core','core-normal','Normal release','View-only tracking of a normal release, from the visit list to completion and the activity log.', L('2639-81789 2639-78951 2639-79720 2639-80033 2639-82913')),
 ('core','core-tp','Third-party approval','The approver reviews the third party’s documents and approves. Gold verification then continues in the partner app.', L('2639-82651 2639-81157 2639-76095 2639-76439 2639-76669 2639-77281 2639-77648 2639-78443 2639-83085')),
 ('core','core-docs','Reason documents','What the approver sees for each of the four release reasons.', L('2639-76797 2639-76925 2639-77062 2639-77190')),
 ('core','core-reject','Third-party rejection','Rejecting requires a reason. The visit is cancelled and the customer is offered Reschedule visit.', L('2639-81473 2639-76267 2639-77417 2639-77881 2639-78156 2639-78676 2639-80474 2639-80702')),
 ('core','core-blocked','Item mismatch','Any item marked not matched blocks the release. CORE shows the flagged item with reasons and images.', L('2639-79173 2639-79400')),
 ('core','core-loan','Loan status','The two loan statuses around a release.', L('2639-82197 2639-82424')),
]

for _,_,_,_,ids in FLOWS:
    for i in ids:
        assert i in S, i
        app = S[i][0]
        assert (ROOT/'assets'/app/f'{i}.jpg').exists(), i

data = {
  'screens': {k: {'a': v[0], 'l': v[1], 't': v[2], 'c': v[3]} for k, v in S.items()},
  'flows': [{'g': g, 'k': k, 'n': n, 'd': d, 'ids': ids} for g, k, n, d, ids in FLOWS],
}
tpl = (ROOT/'template.html').read_text()
(ROOT/'index.html').write_text(tpl.replace('/*DATA*/', json.dumps(data, ensure_ascii=False, separators=(',', ':'))))
print('flows', [(f[1], len(f[4])) for f in FLOWS])
