#!/usr/bin/env python3
"""Render crisp HTML status legends (own design) for the Admin Loan Flows deck.
Beagle status guide = Parent Loan + Gold Loan. BRL status guide = BRL Loan + BRL Visit + ELR.
Replaces the image-based status-guide flows with an HTML step each."""
import json, os
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_FN = os.path.join(HOME, "oro-admin-loan-flows-walkthrough.html")

PARENT = ["VISIT_SCHEDULED","VISIT_AT_BRANCH","SETTING_UP_WITH_LENDER","AWAITING_CUSTOMER_ACTION","ON_HOLD",
 "AWAITING_CUSTOMER_SIGNATURE","PENDING_LENDER_APPROVAL","FUNDS_BEING_TRANSFERRED","GOLD_LOAN_COMPLETE",
 "PERSONAL_LOAN_IN_PROGRESS","AWAITING_PL_SIGNATURE","PL_FUNDS_BEING_TRANSFERRED","ALL_LOANS_COMPLETE",
 "LOAN_CANCELLED","LOAN_CLOSURE_REQUESTED","LOAN_CLOSURE_APPROVED","PAYMENT_RECEIVED_RELEASE_PENDING",
 "RELEASE_VISIT_SCHEDULED","RELEASE_VISIT_IN_PROGRESS","JOURNEY_COMPLETE","GOLD_SOLD_PRIVATELY",
 "GOLD_SOLD_PRIVATELY_PL_ACTIVE","GOLD_AUCTIONED","GOLD_AUCTIONED_PL_ACTIVE","RENEWAL_ELIGIBLE",
 "RENEWAL_IN_PROGRESS","RENEWAL_COMPLETED_BY_CUSTOMER","AWAITING_LENDER_BOOKING","RENEWAL_CLOSING_IN_PROGRESS",
 "EXCESS_TRANSFER_IN_PROGRESS","NEW_LOANS_ACTIVE","RENEWAL_TERMINATED"]
GL = ["GL_CREATED","GL_LENDER_API_INITIATED","GL_IN_QUEUE","GL_ESIGN_PENDING","GL_ESIGN_IN_PROGRESS",
 "GL_ESIGN_IN_COMPLETED","GL_LENDER_APPROVAL_PENDING","GL_LENDER_APPROVED","GL_DISBURSEMENT_IN_PROGRESS",
 "GL_DISBURSED","GL_CLOSURE_REQUESTED","GL_CLOSURE_APPROVED","GL_CANCELLED","GL_CLOSED","GL_RELEASE_SCHEDULED",
 "GL_RELEASE_IN_PROGRESS","GL_RELEASED","GL_AUCTIONED","GL_PRIVATESALE","GL_RENEWAL_IN_PROGRESS",
 "GL_RENEWAL_COMPLETED","GL_CLOSED_RENEWAL","GL_NEW_CREATED","GL_BOOKED_PENDING_EXCESS"]
BRL_LOAN = ["BRL_CREATED","BRL_PENDING_APPROVAL","BRL_APPROVED_ESIGN_PENDING","BRL_PENDING_FUND_TRANSFER",
 "PAYMENT_PROOF_PENDING","PAYMENT_PROOF_SUBMITTED","PAYMENT_PROOF_APPROVED","PAYMENT_PROOF_REJECTED",
 "BRL_ACTIVE","BRL_EXCESS_PENDING","BRL_PARTIALLY_SETTLED","BRL_CLOSED","BRL_CANCELLED"]
BRL_VISIT = ["VISIT_PLANNED","VISIT_ASSIGNED","VISIT_RESCHEDULED","PARTNER_ARRIVED","VISIT_STARTED",
 "FACE_MATCH_IN_PROGRESS","FACE_MATCH_VERIFIED","FACE_MATCH_FAILED","CO_BORROWER_CHECK_IN_PROGRESS",
 "CO_BORROWER_CHECKED","KYC_PENDING","KYC_COMPLETE","CKYC_IN_PROGRESS","FEASIBILITY_RUNNING",
 "FEASIBILITY_PASSED","FEASIBILITY_BLOCKED","EMAIL_VERIFIED","NOMINEE_ADDED","PLEDGE_CARDS_SUBMITTED",
 "PLAN_SELECTION_IN_PROGRESS","ACCOUNT_SELECTION_IN_PROGRESS","BRL_APPROVAL_PENDING","AWAITING_OPS_REVIEW",
 "FUND_TRANSFER_PENDING","BRL_APPROVED","BRL_REJECTED","ESIGN_PENDING_PRIMARY","ESIGN_COMPLETE_PRIMARY",
 "ESIGN_PENDING_COBORROWER","ESIGN_COMPLETE_ALL","FUND_TRANSFER_COMPLETE","PAYMENT_PROOF_PENDING",
 "PAYMENT_PROOF_SUBMITTED","PAYMENT_PROOF_APPROVED","PAYMENT_PROOF_REJECTED","ELR_VISITS_SCHEDULED",
 "ELR_IN_PROGRESS","GOLD_IN_CUSTODY","VISIT_COMPLETED","VISIT_CANCELLED"]
ELR = ["ELR_VISITS_SCHEDULED","ELR_VISIT_RESCHEDULED","ELR_VISIT_IN_PROGRESS","ELR_VISIT_COMPLETED",
 "ELR_VISIT_CANCELLED","GL_VISIT_SCHEDULED","TSV_HANDOVER_IN_PROGRESS","TSV_HANDOVER_COMPLETE","TRV_COMPLETE"]

# semantic palette: (text, border, bg)
C = {
 "red":    ("#B42318", "#F0B4AE", "#FDECEA"),
 "gray":   ("#475467", "#D0D5DD", "#F2F4F7"),
 "green":  ("#177245", "#A6E0BC", "#E9F7EF"),
 "amber":  ("#B54708", "#F1CE93", "#FCF2E1"),
 "blue":   ("#1D4ED8", "#BAD0FB", "#EDF3FE"),
 "violet": ("#6941C6", "#CDBEF4", "#F4EFFE"),
}
def cat(s):
    t = s.upper()
    def has(*ks): return any(k in t for k in ks)
    if has("CANCEL","REJECT","FAIL","BLOCK","TERMINAT"): return "red"
    if has("CLOSED","CLOSURE","ON_HOLD","AUCTION","SOLD","PRIVATE","CUSTODY"): return "gray"
    if has("COMPLETE","APPROVE","VERIFI","PASSED","DISBURS","RELEASED","SETTLED","ACTIVE","CHECKED","ADDED","ELIGIBLE","HANDOVER_COMPLETE","TRV_COMPLETE"): return "green"
    if has("PENDING","AWAITING","QUEUE","RUNNING","SUBMITT","REQUEST","RESCHEDUL","REVIEW"): return "amber"
    if has("PROGRESS","INITIAT","STARTED","STARTING","TRANSFER","SETTING","SELECTION","CKYC","KYC"): return "blue"
    return "violet"  # created / planned / scheduled / assigned / arrived / new / email

def pill(s):
    txt, bd, bg = C[cat(s)]
    label = s.replace("_", " ")
    return ('<span class="sg-pill" style="color:%s;border-color:%s;background:%s">%s</span>'
            % (txt, bd, bg, label))

def group(title, labels):
    return ('<div class="sg-group"><div class="sg-gt">%s</div><div class="sg-pills">%s</div></div>'
            % (title, "".join(pill(s) for s in labels)))

def page(sub, groups):
    return ('<div class="sg-h">Status guide</div><div class="sg-sub">%s</div>%s'
            % (sub, "".join(groups)))

beagle_html = page("Every status a loan can be in", [
    group("Parent loan (OML)", PARENT), group("Gold loan (GL)", GL)])
brl_html = page("Every status a BRL loan / visit can be in", [
    group("BRL loan", BRL_LOAN), group("BRL visit", BRL_VISIT), group("ELR / TSV", ELR)])

h = open(DECK_FN, encoding="utf-8").read()
s = h.index('const DECK'); b = h.index('[', s); d = 0
for i in range(b, len(h)):
    if h[i] == '[': d += 1
    elif h[i] == ']':
        d -= 1
        if d == 0: break
deck = json.loads(h[b:i + 1])
def setstatus(slug, title, html):
    f = next(f for g in deck for f in g['flows'] if f['slug'] == slug)
    f['steps'] = [{"img": "", "html": html, "title": title, "caption": ""}]
setstatus("bg-status", "Loan statuses", beagle_html)
setstatus("tk-status", "BRL & ELR statuses", brl_html)
open(DECK_FN, "w", encoding="utf-8").write(h[:b] + json.dumps(deck, ensure_ascii=True) + h[i + 1:])
print("status guides rendered as HTML. Beagle groups: Parent(%d)+GL(%d); BRL groups: Loan(%d)+Visit(%d)+ELR(%d)"
      % (len(PARENT), len(GL), len(BRL_LOAN), len(BRL_VISIT), len(ELR)))
