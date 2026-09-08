# Marq Buying-Stage and Forecast Evidence Model

## Authority and V1 policy status

The repository's source documents do not define complete entry/exit gates or formal forecast governance. The evidence gates below are therefore the V1 operating policy for this skill, not a claim that Marq has already adopted them as company policy.

Discover pipeline, stage, and forecast enums live on every run. The headings below name semantic buying milestones, not assumed HubSpot stored values. Map the portal's current new-business stages to these milestones using label, order, and customer evidence. Do not apply this model as authoritative to expansion, reseller, churn, partner, or archived pipelines.

## Core rule

Actual stage is the highest stage whose entry criteria are fully evidenced by customer behavior. Activity in a later stage does not compensate for a missing earlier gate. Recorded stage is evidence, never proof.

## Canonical stage model

### 1. Opportunity identified

- Entry: named ICP account/contact plus a concrete trigger, problem hypothesis, or inbound signal worth qualifying.
- Exit: a discovery/demo conversation is scheduled with a named customer participant and date.
- Customer evidence: inquiry, referral, response, or confirmed willingness to meet.
- Stakeholders: initial contact; potential problem owner identified if known.
- CRM: company, contact, owner, source, problem hypothesis, meeting date.
- False positives: list membership, intent score, outbound sequence enrollment, or rep research without customer response.
- Block advancement: no identifiable customer engagement or no plausible Marq use case.

### 2. Demo/Discovery Meeting set

- Entry: customer accepted a dated meeting with a clear discovery purpose.
- Exit: meeting occurred and produced enough evidence to qualify as SQO, or it was disqualified/no-showed and dispositioned.
- Customer evidence: accepted invitation or direct confirmation.
- Stakeholders: attendee who can explain the problem; problem owner preferred.
- CRM: meeting date, attendees, objective, current hypothesis, next-step owner.
- False positives: tentative hold, seller-sent invitation not accepted, repeated no-show, calendar meeting with no buyer purpose.
- Block advancement: meeting not held, no substantive customer exchange, or no qualifying problem.

### 3. SQO

- Entry: discovery held; customer acknowledges a material problem or desired outcome relevant to Marq; there is a plausible buyer, authority path, and reason to evaluate now.
- Exit: the problem, root cause, present process, affected groups, desired outcome, and evaluation objective are sufficiently understood for a tailored solution overview.
- Customer evidence: first-person problem statement, current-state detail, consequences, and agreement to continue evaluation.
- Stakeholders: problem owner and evaluator; economic-buyer path identified even if access is pending.
- CRM: pain, authority, source, close-date hypothesis, next step/date, associated contacts, discovery notes.
- False positives: demo interest, positive tone, feature curiosity, or seller-defined pain without customer confirmation.
- Block advancement: no material need, no authority path, no active evaluation, or unresolved size/fit issue.

### 4. Solution overview

- Entry: SQO exit evidence exists and Marq can present a use-case-specific solution tied to the customer's problem.
- Exit: customer validates the relevant workflow/capabilities and agrees on what must be proven next.
- Customer evidence: confirms use-case fit, corrects requirements, identifies success measures, and commits to a next evaluation step.
- Stakeholders: problem owner, evaluator, representative users; technical stakeholder if integration/security is central.
- CRM: validated use cases, pain/root cause, desired outcome, open requirements, next step/date.
- False positives: generic demo delivered, high attendance, praise, or many feature questions without an agreed evaluation path.
- Block advancement: unvalidated business problem, generic demo, material product-fit doubt, or no customer-owned next step.

### 5. Opportunity strategy

- Entry: customer has validated solution relevance and is actively defining how to evaluate and buy.
- Exit: buying process, decision criteria, quantified or decision-useful impact, critical event, stakeholder map, and evaluation plan are customer-confirmed.
- Customer evidence: shares internal process/criteria, helps build the business case, names stakeholders, and accepts dated mutual steps.
- Stakeholders: champion candidate, economic buyer identified, problem owner, evaluator, technical/security as applicable.
- CRM: business impact, authority, competition/status quo, critical event, decision process/criteria, stakeholder map, mutual next step.
- False positives: proposal requested, seller-created MAP, ROI model made from assumptions, or a friendly contact called a champion.
- Block advancement: impact is not decision-useful, critical event is seller-created, decision path is unknown, or contact will not mobilize access.

### 6. Group consensus

- Entry: the relevant buying group is engaged around a shared problem, outcome, and evaluation approach.
- Exit: affected and approving stakeholders agree on requirements, value, change implications, and the route to a decision.
- Customer evidence: cross-functional participation, internal introductions, questions resolved by role, and explicit alignment or documented dissent with a resolution path.
- Stakeholders: champion, economic buyer or delegate, problem owner, users, technical/security, procurement/legal where timing requires.
- CRM: stakeholder roles, support/opposition, consensus gaps, decision meeting/date, next commitments.
- False positives: multiple attendees from one function, copied executives, or one contact claiming everyone agrees.
- Block advancement: single-threading, material stakeholder opposition, economic-buyer path absent, or unresolved adoption/technical risk.

### 7. Solution confirmation

- Entry: buying group agrees Marq meets the material business and technical requirements and commercial scope is sufficiently clear.
- Exit: customer confirms preferred path/intent and formally initiates the required approval, security, legal, or procurement process.
- Customer evidence: explicit solution confirmation, agreed scope, success criteria, evaluation complete, and named remaining approvals.
- Stakeholders: champion, economic buyer/authorized decision maker, technical/security approver, affected leaders.
- CRM: confirmed requirements, scope, amount, products, success criteria, approval map, target decision date.
- False positives: successful demo, verbal enthusiasm, quote request, or champion preference without buying-group confirmation.
- Block advancement: unresolved must-have requirement, unapproved scope, absent decision authority, or competitive evaluation still materially open.

### 8. Procurement

- Entry: the customer's procurement, legal, security, or vendor process has actually begun with named owners and requirements.
- Exit: material procurement/security/legal issues are cleared and final commercial/contract execution steps are defined.
- Customer evidence: intake submitted, security review opened, legal redlines exchanged, vendor forms requested, or procurement owner engaged.
- Stakeholders: procurement, legal, security/IT as applicable, champion, economic buyer, Marq deal owner/deal desk.
- CRM: process owner, start date, requirements, redline/security status, dependencies, target completion date.
- False positives: documents sent proactively, buyer says procurement will be easy, or a security link was shared but no review opened.
- Block advancement: process not started, owner unknown, unresolved security/legal blocker, or budget/authority still unconfirmed.

### 9. Closing

- Entry: solution and commercial path are approved in substance; remaining work is controlled contract, signature, purchase-order, or final execution work.
- Exit: required approval is formally submitted/completed and no substantive buyer decision remains.
- Customer evidence: agreed redlines/commercials, signer identified, signature/PO path and date confirmed.
- Stakeholders: authorized signer/economic buyer, procurement/legal, champion, Marq deal desk/approver.
- CRM: final amount/currency, term, products, approvers, signer, contract status, dated execution plan, close date.
- False positives: proposal sent, contract sent without buyer agreement, end-of-quarter hope, or rep says “verbal yes.”
- Block advancement: unresolved value/scope/price objection, no signer, no contract process, or buyer-controlled date missing.

### 10. Pending approval

- Entry: all substantive customer decisions are complete and a specific, named approval is formally pending.
- Exit: approval granted and deal moves to payment/bookable completion, or approval fails and the deal is reset/lost.
- Customer evidence: approval request exists, approver and expected decision date are known, no new evaluation remains.
- Stakeholders: named approver/signatory, champion, deal owner, applicable Marq approver.
- CRM: approval type, owner, submitted date, status, expected completion, fallback if rejected.
- False positives: vague “waiting on leadership,” unsent approval request, or approval used to mask unresolved objections.
- Block advancement: approval not submitted, approver/date unknown, or commercial/solution issues remain.

### 11. Closed - awaiting payment

- Entry: agreement/order is executed or otherwise accepted under Marq policy, and only payment/booking completion remains.
- Exit: payment/bookability requirements are satisfied and the deal is closed won, or acceptance reverses.
- Customer evidence: executed order/contract, accepted quote, PO, or invoice/payment event as policy requires.
- Stakeholders: finance/AP, signer, procurement, Marq finance/deal desk.
- CRM: executed-document status, invoice/payment/PO status, amount, currency, dates.
- False positives: verbal acceptance, signature promised, or invoice sent without accepted agreement.
- Block advancement: execution not complete, payment prerequisite absent, or material conditions remain.

### 12. Closed won

- Entry: Marq's booking policy is satisfied; the transaction is not merely expected.
- Exit: terminal for new-business diagnosis; later reversal belongs in clawback/appropriate operational process.
- Customer evidence: executed and bookable commercial commitment.
- Stakeholders: finance/deal desk and implementation/customer success handoff owners.
- CRM: final amount, currency, products/line items, contract dates, implementation notes, closed-won date.
- False positives: verbal win, unapproved exception, signature without required payment/PO.
- Block advancement: any unmet booking requirement.

### Closed or administrative outcomes

#### Closed lost

- Entry: customer chose another path, decided not to act, is unreachable after a defined close-out attempt, or qualification failed after SQO.
- Required CRM: evidence-based reason and description, final stage, competitor/status quo where known, outcome date.
- False positive: moving a temporarily mistimed but mutually active opportunity to lost rather than nurture.

#### Demo disqualified

- Entry: pre-SQO/demo qualification fails on demo not held, size, need, authority, or pain.
- Required CRM: disqualification reason and concise evidence. Do not use to hide poor follow-up.

#### Merged opportunity

- Entry: this record duplicates another active opportunity. Link or identify the surviving record; it is not a win or loss.

#### Closed - clawback

- Entry: a previously booked deal is reversed under Marq policy. This is an operational outcome, not an acceleration stage.

## Legacy terminology mapping

Use the live primary new-business pipeline labels in outputs. Map older source language as follows, then apply evidence gates rather than the name alone:

| Legacy term | Canonical stage(s) | Interpretation |
|---|---|---|
| Discovery | Demo/Discovery Meeting set → SQO | A scheduled meeting is not completed discovery; SQO requires a validated problem and active evaluation. |
| Demo | Solution overview | Only when the demo is tailored and the customer validates use-case relevance. |
| Solution Validation | Solution overview → Opportunity strategy → Group consensus → Solution confirmation | The old umbrella spans four distinct customer decisions. |
| Proposal | Opportunity strategy or Solution confirmation | A proposal request does not prove confirmation or procurement. |
| Decision Process | Opportunity strategy → Group consensus → Solution confirmation → Procurement | Determine which buyer decision has actually occurred. |
| Negotiation / Final Negotiations | Closing, sometimes Procurement | If legal/procurement is still opening, it is Procurement; if substantive value/scope is unresolved, it may be earlier. |
| Solution presented | Solution overview | Reseller legacy label. |
| Discovery meeting held | SQO only if qualification gates are met | A held meeting alone is insufficient. |

## Forecast model

Resolve the portal's current forecast labels and stored values live. Map them to these concepts rather than assuming a particular enum:

| Forecast concept | V1 evidence standard |
|---|---|
| Pipeline / not forecasted | Default for an open qualified deal that lacks a defensible path to close in the forecast period. Use the live portal option that represents open pipeline excluded from the active forecast. |
| Best case / upside | There is a customer-backed critical event and feasible path within the period, but at least one material gate remains outside the team's control. Use whichever current portal label maps to this concept. |
| Commit | Buyer-validated value and scope, active champion, economic-buyer/authority access, confirmed decision and procurement path, dated mutual plan, and enough calendar time for all remaining steps. No unresolved material fit, budget, legal, or security risk. |
| Closed / closed won | Booking policy is actually satisfied. Never forecast an expected signature as Closed. |

Forecast category may be changed only by people authorized in HubSpot under Marq governance. The repository does not name those roles. The skill challenges the recorded category and proposes a correction; it never writes one.

## Critical-event and close-date validation

A critical event is credible only when the customer states the event, explains the consequence of missing it, owns or is affected by the date, and has begun prerequisite work. A seller deadline, expiring quote, quarter end, or unsupported implementation hope is not a critical event.

Reverse-engineer the close date from the customer event through every remaining step: evaluation, business case/budget, economic approval, security, legal, procurement, contract/signature, PO/payment, and any Marq approval. Mark the date:

- Credible: owners, durations, dependencies, and customer commitments fit with contingency.
- At risk: path is credible but one material dependency is unproven or schedule has little slack.
- Unsupported: no customer-backed event, remaining steps do not fit, or dates are seller-entered guesses.

Recommend pushing the date when unsupported. Do not replace it with another arbitrary date; use the earliest supportable date or say the date must be reset after a named validation step.
