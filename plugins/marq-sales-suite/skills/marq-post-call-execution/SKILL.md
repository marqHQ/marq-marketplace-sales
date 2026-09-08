---
name: marq-post-call-execution
description: Turn a completed Marq sales call into an evidence-tagged deal summary, qualification assessment, commitment and stakeholder record, proposed HubSpot changes, specific next-step plan, and grounded customer follow-up email. Find the relevant HubSpot record from a deal or account name; a HubSpot link is optional. Use after discovery, demo, or later-stage calls when a transcript or substantive notes are available. Do not use for seller coaching or SPICED scorecards.
---

# Marq Post-Call Execution

Convert what happened on a completed call into a trustworthy operating record. Default to read-only analysis and drafts. Never write to HubSpot or send an external message without the user's approval after showing the exact proposed action.

## What this skill does

A rep provides the account or deal name plus the completed call transcript, notes, or both. The skill finds the correct HubSpot record, combines the conversation with relevant CRM history, and returns an evidence-based deal summary, qualification assessment, stakeholder and commitment record, recommended next step, proposed CRM changes, customer follow-up email, and next-call preparation. It clearly separates customer statements, CRM facts, seller interpretations, Codex inferences, and unknowns. Everything remains a draft until the rep approves a CRM update or external communication.

When explaining, introducing, or rolling out this workflow, use [references/team-summary.md](references/team-summary.md) as the shareable team overview.

## Required inputs

Require a complete transcript, substantive call notes, or both. If neither is accessible, ask for one. Establish the call date, seller, account or deal name, and call type. A HubSpot link or record ID is optional and must never be required when the rep supplies a deal or account name.

Read [references/hubspot-deal-properties.md](references/hubspot-deal-properties.md) whenever an account name, deal name, HubSpot link, or record ID is available. Call HubSpot user-details first, resolve the correct record using the reference's read-only lookup workflow, and include the clickable HubSpot record link in the deliverable. Then read the deal, associated company and contacts, and relevant recent activities. Re-fetch live property definitions before proposing enum-backed or stage values because portal configuration can change.

If one record is clearly resolved, continue without asking the rep for a link or confirmation. If multiple plausible deals remain, show a short selection table with deal name, account, pipeline, stage, owner, amount/currency, close date, and clickable link, then ask the rep to choose. Never select an ambiguous record based only on recency or a fuzzy name match. If no deal exists, return the matched company link when available, state that no associated deal was found, and continue with CRM context unavailable unless the user directs otherwise.

## Evidence discipline

Read [references/evidence-and-output.md](references/evidence-and-output.md) before analyzing a call. Apply one evidence class to every material claim and preserve a source locator. Never:

- turn a seller statement into a customer-confirmed fact;
- upgrade an inference because it sounds likely;
- convert missing qualification into positive qualification;
- hide conflict between the transcript, notes, and CRM;
- invent product capabilities, ROI, references, pricing, stakeholders, dates, or commitments.

Normalize a relative date only when the call date and wording make the date deterministic. Retain the original wording and mark the normalized date as derived from customer or seller evidence, as applicable.

## Workflow

1. Resolve the HubSpot deal from the supplied deal or account name and record which HubSpot URL is being used. Record lookup is read-only and does not require approval.
2. Separate customer statements, seller statements, CRM facts, and Codex deductions before synthesizing.
3. Adapt to the call type:
   - Discovery: emphasize current state, pain, impact, desired state, buying process, and qualification gaps.
   - Demo: connect only demonstrated capabilities to confirmed needs; capture reactions, validation gaps, objections, and stakeholder coverage.
   - Later stage: emphasize decision path, approvals, commercial or security dependencies, mutual commitments, dates, and deal risk.
4. Assess SPICED coverage without coaching or scoring the seller. Use Situation, Pain, Impact, Critical Event, and Decision as qualification lenses; mark each Confirmed, Partial, Missing, or Contradicted and cite evidence. If the user wants coaching, use the separate `spiced-call-coach` skill rather than duplicating its draft-and-audit workflow.
5. Build the deliverable in the exact order defined in [references/evidence-and-output.md](references/evidence-and-output.md). A recommended next step must state what, who, why, owner, and date. Never describe a recommendation as an agreed commitment.
6. Map only supported conclusions to HubSpot using [references/hubspot-deal-properties.md](references/hubspot-deal-properties.md). Show current value, proposed value, evidence class, source, rationale, and confidence. Put `No change proposed` when evidence is insufficient.
7. Draft the email using [references/follow-up-email.md](references/follow-up-email.md). Keep it customer-safe: customer-confirmed facts and explicit mutual commitments may be stated directly; seller interpretation or Codex inference must be omitted or framed as a question or recommendation.
8. End with an approval gate. State that no CRM update or communication has occurred. If the user asks to write later, show the exact HubSpot change table required by the HubSpot skill and obtain approval immediately before the write. Obtain separate approval immediately before sending external communication.

## Identity mapping

Use the repository mapping only to resolve owner IDs when the named rep is relevant: Justin Warner `179425909`, Brad Hardle `91714475`, Cody Cluff `96818330`, Seth Hurtado `80743422`. This mapping does not authorize impersonation, connector switching, ownership changes, or writes.

## Source limits

The founding source set contains templates, not validated real call/email/deal triplets. Read [references/source-findings.md](references/source-findings.md) when evaluating rollout readiness, extending voice rules, or changing the workflow. Treat the email length and shared-team voice rules as V1 operating defaults until representative sent-email examples are approved.
