---
name: marq-deal-acceleration
description: Find and diagnose one active Marq HubSpot opportunity from a deal name, account name, HubSpot URL, or deal ID; challenge its recorded stage, momentum, close date, and forecast using customer evidence; and recommend no more than two high-leverage actions. Use for single-deal strategy, deal reviews, stalled or at-risk opportunities, and forecast inspection; do not use for multi-deal pipeline health or activity planning.
---

# Marq Deal Acceleration

Diagnose whether the customer is progressing through a buying process. Do not equate seller activity, CRM stage, meeting volume, or rep confidence with customer progress.

This skill is read-only in V1. Never change a stage, forecast, close date, or other CRM field. Propose corrections instead. Do not manufacture urgency, recommend discounts or concessions without explicit authority, or propose executive involvement without a specific buyer-side purpose.

## Scope

Analyze exactly one deal in Marq's primary new-business pipeline. The rep may identify it by deal name or account/company name; a HubSpot URL or deal ID is optional, never required. Find the matching HubSpot record and its URL as part of the workflow. If more than one active opportunity could reasonably match, show the candidates and ask the rep to choose; do not diagnose a guessed record.

For multiple deals or broader forecast coverage, use the HubSpot pipeline-health workflow instead. For a selected deal, this skill owns the strategic diagnosis even when it consults pipeline context.

## Required references

Read these before diagnosing a deal:

- [stage-and-forecast-model.md](references/stage-and-forecast-model.md) for canonical stages, legacy mappings, and forecast gates.
- [momentum-and-evidence.md](references/momentum-and-evidence.md) for evidence hierarchy, recency rules, and green/yellow/red classification.
- [strategy-rules.md](references/strategy-rules.md) for selecting at most two actions and knowing when to reset, nurture, remove from forecast, or disqualify.

Read [acceptance-scenarios.md](references/acceptance-scenarios.md) only when validating or revising the skill.

## Retrieve the record

1. Call HubSpot user-details first and confirm deal read access. If unavailable, ask the user to connect or reauthorize HubSpot.
2. Discover the portal's current pipeline, stage, and forecast-category properties and enum values. Identify the primary new-business pipeline from live configuration; do not assume internal IDs, stored values, or stage order from this skill.
3. Resolve the deal from whatever identifier the rep provides:
   - Deal name: search deal records by the supplied name, prioritizing exact matches and then close partial matches. Filter to active opportunities in the discovered primary new-business pipeline when possible.
   - Account/company name: search company records, verify the intended company, then retrieve its associated deals and filter to active opportunities in the discovered primary new-business pipeline.
   - HubSpot URL or deal ID: fetch the referenced deal directly.
   - Do not ask the rep for a HubSpot link merely because they supplied a name.
4. If resolution returns one clear active opportunity, proceed automatically. If it returns multiple plausible active opportunities, present a compact candidate list with deal name, account, owner, stage, amount, close date, and HubSpot link, then ask the rep to choose. Do not choose by amount, recency, or stage alone. If there is no active match, report the closest closed or other-pipeline matches and ask for clarification rather than creating or assuming a deal.
5. Preserve the resolved deal's HubSpot URL and confirm it is in the discovered primary new-business pipeline. If it belongs to another pipeline, state that this evidence model may not match that pipeline and ask whether the user wants a best-effort diagnosis.
6. Discover and fetch the available deal properties needed for the diagnosis, including when available:
   - name, ID, owner, company, amount and currency;
   - pipeline, stage, stage-entry timestamp, time in stage, and stalled flag;
   - close date, forecast category, forecast notes, next step, and next-step date;
   - last contacted, last activity, next activity, and number of associated contacts;
   - pain, customer challenges, authority, primary competitor, closed/disqualified fields, and relevant sales notes.
7. Fetch associated company and contacts. Identify roles from titles and evidence, not from title alone: champion, economic buyer, decision maker, technical/security, procurement/legal, affected leaders, and users.
8. Review customer interactions far enough back to test the current stage and any claimed recovery. Default to activity since the deal entered its current stage plus the prior stage, or the most recent 120 days if stage history is unavailable. Inspect meetings, calls, emails, notes, and customer-completed artifacts. Separate inbound/customer actions from seller actions.
9. If matched Gong transcripts are available, use only calls confidently matched by deal, company/contact, and date. Prefer transcript evidence over seller summaries when they conflict.

Do not conclude that missing data or silence means the customer said “no,” lacks pain, budget, authority, or intent, or has no stakeholder. Absence of discussion never becomes a negative CRM value. Say the evidence is unavailable, then lower confidence and recommend the smallest validation step if the gap is decision-critical. Inactivity may affect momentum, but it is not proof of failed qualification.

## Diagnose in this order

1. Build a dated evidence ledger of customer progress, customer commitments, seller actions, contradictions, and missing evidence.
2. Determine actual stage using the highest stage whose entry criteria are fully evidenced. Stage is capped by the weakest unmet entry gate; later-stage activity does not cure an earlier qualification gap.
3. Normalize the observed evidence using the momentum contract, run `scripts/score_momentum.py`, and use its returned Green/Yellow/Red result and reason codes. Do not assign a color through model judgment. If Python or the scorer is unavailable, report momentum as unscored and stop before making a color-dependent recommendation.
4. Identify the primary blocker: the single constraint whose removal would most change the probability of progress. Treat symptoms such as unanswered emails as secondary unless lack of engagement is itself the disqualifying evidence.
5. Assess qualification: business problem/root cause, quantified impact, desired outcome, authority, buying process/criteria, critical event, competition/status quo, and a credible champion.
6. Assess stakeholder coverage and whether access is expanding, static, or shrinking.
7. Test close-date feasibility by reverse-engineering remaining customer and internal steps. Test forecast category against evidence, not stage probability or rep confidence.
8. Select one or two actions from the strategy rules. An action must remove or validate the primary blocker. Prefer one action when it is sufficient.

## Evidence discipline

Ground every major conclusion in an identifiable source: property name and value, customer interaction type and date, or transcript/notes date with a concise paraphrase. Distinguish:

- Fact: directly observed.
- Inference: supported interpretation.
- Unknown: not available or not yet validated.
- Rep assertion: seller-entered claim without customer corroboration.

When sources conflict, state the conflict and prefer direct, recent customer evidence. Never invent a quote, stakeholder role, commitment, critical event, or date.

## Output

Keep the response executive-ready and compact. Include:

### Executive diagnosis

Two to four sentences stating whether the deal is qualified to close in the stated period, the actual stage, momentum, and primary blocker.

### Deal assessment

- Recorded stage → actual stage, with the decisive evidence or missing gate.
- Momentum: Green, Yellow, or Red, with dated customer evidence.
- Primary blocker.
- Secondary risks, limited to the two that could materially change the outcome.
- Qualification gaps.
- Stakeholder gaps.
- Close-date assessment: credible, at risk, or unsupported; give the reason and a realistic correction when supportable.
- Forecast assessment: recorded category → supported category, with the unmet gate.
- Confidence: high, medium, or low, and which unavailable evidence limits it.

### Recommended actions

Recommend no more than two. For each, state:

- Action and owner.
- Specific blocker it resolves.
- Evidence of completion.
- Decision enabled by the result.

At least one action should be a customer-facing next step when continued pursuit is warranted. Express it as What / Who / Why and include a date only when supported or explicitly proposed as a question. If the right answer is nurture, forecast removal, close-date push, or disqualification, say so directly.

### Rep coaching note

One candid paragraph about the rep behavior or judgment that matters most. Do not generate generic encouragement.

### Suggested CRM corrections

List only evidence-backed corrections in `Property: current → proposed — reason` form. Make no writes. Any future proposal involving the standard HubSpot next-step field must preserve prior context by appending rather than replacing it.

End with a short evidence ledger using dated bullets and the HubSpot deal link. Omit sections with no material content rather than filling them with generic language.
