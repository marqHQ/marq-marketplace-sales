# Gong Qualification-Field Inference

Use this reference only after resolving the exact HubSpot deal and discovering the target stage's required fields and valid enumeration values.

## Match the transcript to the deal

Search with `search_gong_calls` using the associated company name and `hasTranscript: true`. Narrow or corroborate with the associated contact email, participant name, deal owner, call title, and a tight date window around the initial demo or discovery date.

Accept a call only when the evidence identifies the same opportunity. Require either exact CRM deal metadata or at least two independent matching signals, including one of:

- Associated company plus associated contact email or participant
- Associated company plus deal-specific call title or CRM metadata
- Associated contact plus a call date aligned with the deal's demo or discovery activity

Do not rely on a partial company-name match alone. If multiple opportunities or calls remain plausible, ask the rep to identify the right call or supply the missing field values.

Fetch accepted calls with `get_gong_transcript`. Use additional calls only when they independently satisfy the same matching standard.

## Evidence and confidence

Prefer explicit prospect or customer statements. Seller summaries may corroborate but should not override contradictory prospect statements or existing HubSpot data.

- **High:** Explicit statement maps unambiguously to one valid HubSpot option.
- **Medium:** Strong contextual evidence exists, but more than one valid option remains plausible. Ask the rep to confirm.
- **Low:** Evidence is absent, indirect, or contradictory. Do not propose a value.

Record the call ID and link, call date, speaker, timestamp when available, and a concise evidence summary or short excerpt. Never treat absence of discussion as evidence for `No`, `None`, or another negative option.

## Qualification mappings

| HubSpot field | Sufficient evidence | Guardrail |
|---|---|---|
| Deal Type | Explicit new purchase, expansion, renewal, downgrade, cancellation, or excluded opportunity | Prefer HubSpot account and deal history; use Gong as corroboration when history is conclusive |
| Initial Demo Disposition | Evidence that the meeting occurred plus explicit opportunity status or outcome | Attendance alone does not establish New Opportunity, Existing Opportunity, Nurturing, or Disqualified |
| DAM Integration | Explicit DAM integration requirement or explicit statement that no DAM integration is needed | No DAM discussion is not `No` |
| Customer CRM System | Prospect explicitly names Salesforce, HubSpot, Microsoft Dynamics, another CRM, or states that none is used | Do not infer from the seller's internal CRM or meeting integration |
| Value Proposition | Prospect explicitly prioritizes increasing revenue, saving time or money, or reducing risk | Map only to the portal's valid enumeration; ask if multiple outcomes are equally primary |
| End users | Prospect explicitly identifies the people who will use Marq templates | Do not infer end users from attendee job titles alone |

Discover and apply portal-specific fields beyond this table using the same evidence and confidence rules. Never hardcode enumeration values that have not been retrieved from HubSpot for the current portal.

## Approval boundary

Gong evidence reduces follow-up questions but does not authorize a write. Show every inferred value in the evidence table and the normal HubSpot change table. Preserve the existing consolidated approval step.

Do not infer product selection, quantity, price, discount, term, billing frequency, owner, development rep, or close date from a transcript unless the rep has explicitly asked the skill to use transcript evidence for that fact and the exact proposal is still approved before writing.
