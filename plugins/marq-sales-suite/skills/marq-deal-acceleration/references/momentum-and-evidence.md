# Momentum and Evidence

`scripts/score_momentum.py` is authoritative for the final Green/Yellow/Red classification. The model must normalize evidence into the inputs below, run the scorer, and report its reason codes. Do not reproduce or override the classification through prose judgment.

## Evidence hierarchy

Weight evidence in this order:

1. Customer-completed actions and artifacts: introductions, completed evaluation work, submitted security/procurement intake, redlines, approvals, signed documents.
2. Direct customer statements in calls, emails, or transcripts, especially commitments with owner and date.
3. Corroborated CRM fields and seller notes.
4. Seller actions: emails sent, meetings requested, collateral delivered, tasks created.
5. Rep confidence, sentiment, stage probability, and forecast label.

Seller activity can show effort but cannot make momentum green. Recent direct customer evidence beats older notes. When evidence conflicts, report the conflict.

## Meaningful customer engagement

Count engagement only when the customer advances or clarifies the buying process. Examples include disclosing impact/process, bringing a stakeholder, completing an agreed task, resolving a requirement, opening procurement/security/legal, confirming a decision/date, or candidly changing priority.

Do not count opens, clicks, seller-only meetings/tasks, automated replies, generic thank-yous, calendar acceptance alone, or feature curiosity with no buying consequence.

## Operational rating

Assess seven dimensions:

- Recency of meaningful customer engagement.
- Dated next step jointly understood by the customer.
- Completion of customer-owned commitments.
- Stakeholder access trend: expanding, static, or shrinking.
- Critical-event credibility.
- Close-date stability and feasibility.
- Champion mobilization and completion of required procurement/legal/security work for the stage.

Use the strictest material signal. Averages can hide a fatal gap. The scorer enforces that precedence.

## Scorer input contract

Pass one JSON object containing:

- `stage_band`: `early`, `middle`, or `late`, mapped from live stage configuration.
- `days_since_meaningful_engagement`: non-negative integer or null when unavailable.
- `agreed_longer_wait`: boolean; true only when the customer explicitly agreed to a longer cadence.
- `next_step_status`: `valid`, `weak`, `missing`, or `overdue`. Overdue means more than seven days past the customer-owned date without a reset.
- `commitment_status`: `on_track`, `one_slip`, `two_or_more_missed`, or `unknown`.
- `stakeholder_status`: `expanding`, `complete`, `static`, `single_threaded`, `shrinking`, or `unknown`.
- `critical_event_status`: `credible`, `plausible`, `absent`, `contradicted`, `expired`, `seller_created`, `not_required`, or `unknown`.
- `close_date_status`: `credible`, `at_risk`, `moved_once`, `moved_twice_or_more`, `rolled_period`, `infeasible`, `not_in_period`, or `unknown`.
- `champion_status`: `mobilizing`, `responsive`, `silent`, `defensive`, `left`, `cannot_mobilize`, `not_required`, or `unknown`.
- `required_process_status`: `started`, `not_started`, `not_yet_required`, or `unknown` for procurement, legal, or security required at the current stage.
- `forecast_in_period`: boolean.
- `customer_negative_signal`: boolean; true only for direct customer evidence of no priority, budget path, authority path, fit, or intent to act.
- `stage_or_forecast_contradicted`: boolean; true only when direct customer evidence contradicts the recorded stage or forecast.

Null or `unknown` means unavailable evidence, not negative evidence. The scorer treats unknowns as Yellow warnings, not customer “no” answers.

### Green — customer is progressing

All must be true:

- Meaningful customer engagement occurred within 14 days; for Procurement or later, within 7 business days unless the agreed process explicitly has a longer waiting period.
- A specific next step has What / Who / Why, a date, and customer awareness or ownership.
- Recent customer commitments were completed on time or transparently reset before due date.
- Stakeholder access is appropriate to stage and is expanding or already complete.
- A customer-backed critical event and feasible close path exist when the deal is forecast for the current period.
- Champion takes observable internal action, not merely praises Marq.
- Any stage-required procurement, legal, or security process has actually started.
- No hard-red condition exists.

### Yellow — plausible but exposed

Use when there is real customer interest but one or more material proof gaps, including:

- Last meaningful engagement was 15–30 days ago, or the cadence is slower than the jointly agreed process.
- Next step is vague, seller-owned only, undated, or not customer-confirmed.
- One customer commitment slipped without a new credible owner/date.
- Stakeholder access is static, single-threaded, or one required role is missing.
- Critical event is plausible but not fully validated.
- Close date moved once or has insufficient slack.
- Champion is responsive but has not mobilized others.
- Procurement/security/legal is expected but not opened despite approaching need.
- Business impact is qualitative when a decision requires quantified value.

Yellow should normally block Commit.

### Red — stalled, unqualified, or fictionally timed

The scorer returns Red when any hard-red condition exists:

- No meaningful customer engagement for more than 30 days without a customer-agreed reason.
- No valid next step, or the customer-owned step is more than 7 days overdue with no reset.
- Two customer commitments were missed or repeatedly postponed.
- Champion is silent, defensive, left, or cannot mobilize access; stakeholder access is shrinking.
- Critical event is absent, contradicted, expired, or seller-manufactured while the deal is forecast to close in-period.
- Close date moved two or more times, rolled into another period, or cannot fit remaining steps.
- Deal is recorded in Procurement or later but required buyer process has not started.
- Customer states there is no priority, budget, authority path, fit, or intent to act.
- Direct customer evidence contradicts the recorded stage or forecast.

Red does not always mean disqualify. It does mean the current plan and forecast are unsupported.

## Caps and interpretation

- Missing evidence is not automatically red, but it prevents green and lowers confidence.
- No customer-backed critical event caps an in-period deal at Yellow and normally makes its close date unsupported.
- No economic-buyer/authority path caps Solution Confirmation or later at Yellow and blocks Commit.
- Single-threading caps Group Consensus or later at Yellow.
- Procurement/legal/security “planned” but not started prevents an actual Procurement stage.
- A seller-created MAP does not count until the customer accepts owners and dates.
- A buyer-requested delay with a credible reason, preserved sponsor, and dated restart can be Yellow or nurture; do not punish transparency as disengagement.

## Evidence ledger

For each material item capture:

- Date.
- Source and participant.
- Observable fact or concise paraphrase.
- Evidence class: customer progress, customer commitment, seller action, contradiction, or unknown.
- Which conclusion it supports.

Use exact dates. Do not write “recently” when a timestamp exists.
