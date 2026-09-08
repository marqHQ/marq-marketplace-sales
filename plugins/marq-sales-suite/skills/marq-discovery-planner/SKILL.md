---
name: marq-discovery-planner
description: Prepare a focused, evidence-grounded pre-call discovery strategy for one scheduled Marq sales conversation, named deal, or named account. Resolve the relevant HubSpot record from its name when HubSpot is available; do not require the rep to supply a record link. Use for inbound, outbound, partner, expansion, or executive-led discovery planning; do not use to audit a completed call or write post-call follow-up.
---

# Marq Discovery Planner

Prepare the seller to make the next conversation useful. Do not produce a generic questionnaire, a research dump, a premature demo script, or a complete opportunity qualification checklist.

## Required references

Read these references completely for every plan:

- [references/methodology-and-roe.md](references/methodology-and-roe.md) for the five-step/SPICED mapping, stage priorities, call-type adjustments, and rules of engagement.
- [references/research-policy.md](references/research-policy.md) for permitted sources, evidence labels, source precedence, and conflict handling.

Read these only when relevant:

- Read [references/marq-market-guide.md](references/marq-market-guide.md) when selecting personas, use cases, capabilities, proof, objections, or competitive alternatives.
- Read [references/examples.md](references/examples.md) when the seller asks for an example, the call type is unfamiliar, or the distinction between facts, hypotheses, and questions needs calibration.

## Boundary with adjacent skills

- This skill prepares one upcoming call or named-account conversation.
- `spiced-call-coach` audits a completed call from a transcript.
- A post-call execution skill should update CRM, draft follow-up, and operationalize commitments.
- Do not write a follow-up email, score a completed call, or turn public research into CRM qualification.

## Workflow

1. Resolve the planning target.
   - Accept a scheduled meeting, deal name, account name, deal link, or clear account-and-contact description. A HubSpot link is never required when the rep supplies a deal or account name.
   - When HubSpot is available, search it for the named deal or account and resolve the canonical record before asking the rep for more information.
   - For a deal name, search deal records and inspect the associated company, pipeline, stage, owner, close date, and recent activity as needed to identify the correct match.
   - For an account name, resolve the company record, then inspect its associated deals. Prefer the deal that best matches the meeting, active pipeline, participants, owner, and timing; do not assume the newest or largest deal is correct.
   - If one match is well supported, proceed and retain the HubSpot record URL in the brief. If several plausible matches remain, use supplied meeting/contact context to disambiguate; only then ask the rep to choose among concise candidates. Ask for a distinguishing detail, not for a HubSpot link.
   - If HubSpot returns no match, try reasonable name variants and associated contact/company searches. Report that no record was found and continue with other authorized context when a useful plan is still possible.
   - If no meeting, deal, account, or contact is provided, ask for the deal or account name. Do not substitute a generic industry plan.
2. Gather available context in descending evidentiary value.
   - Start with supplied notes and links, HubSpot deal/account/contact history, prior Gong calls, and email history when authorized and available.
   - Add company sources, current public research, approved internal research, and expansion usage data as applicable.
   - Reuse established context. Do not ask questions that reliable records already answer unless the information is stale, ambiguous, or needs buyer confirmation.
3. Build an evidence ledger before planning.
   - Label every material item `Fact`, `Buyer-stated`, `Internal record`, `Public signal`, `Hypothesis`, `Unknown`, or `Conflict` as defined in the research policy.
   - Public signals may motivate a question; they do not prove pain, priority, budget, urgency, authority, or fit.
4. Classify the conversation.
   - Identify call type, buyer state, deal maturity, persona, industry/use-case pattern, available time, and whether this is discovery-only or a buyer-requested demo/discovery.
   - Treat missing classifications as unknown rather than guessing.
5. Define one meeting objective and one target exit decision.
   - The exit decision must be mutual and achievable in the scheduled time.
   - Examples: proceed to a tailored validation session; add the affected workflow owner; agree on a small expansion hypothesis to validate; nurture until a named trigger; or close as not qualified.
6. Prioritize learning gaps.
   - Rank gaps by how much the answer changes fit, next step, or deal risk.
   - Select no more than six to eight core questions. Each must have one learning objective and a plausible follow-up path.
   - Sequence from context and motivation, through current workflow/root cause and impact, to decision context and next-step commitment. Do not force every framework area into the call.
7. Choose proof only after relevance is established.
   - Use current, traceable Marq capabilities and customer evidence.
   - Match proof by problem pattern and persona before industry. Never invent customer names, metrics, integrations, compliance claims, or outcomes.
   - Phrase unverified capabilities as items to validate internally, not buyer-facing promises.
8. Draft the brief in the required format and run the quality gate.

## Required output

Keep the brief concise enough to use immediately before and during the call.

### Meeting strategy

- **Meeting objective:** one sentence.
- **Target exit decision:** one sentence with both a fit-confirmed and a no-fit path where appropriate.
- **Recommended agenda / upfront contract:** a natural 20–30 second opening that states purpose, time, buyer input, and the end-of-call decision. Do not script false certainty.
- **Call posture:** call type, buyer state, deal maturity, planned duration, and demo posture.

### Participants and context

- Include the resolved HubSpot deal or company name and a clickable record link when available.
- List participants, roles, likely interests, and confidence. Do not present title-based interests as facts.
- Separate `Known facts`, `Important hypotheses`, `Qualification already established`, and `Conflicts or stale items`.
- Include source/date inline for material facts when available.

### Discovery priorities

- Name the three to five most important information gaps in priority order.
- Provide six to eight sequenced core questions maximum.
- For every question include a short `Learning objective` and one or two conditional follow-up prompts. Follow-ups do not count as additional core questions.
- Prefer one clear question at a time. Avoid compound, leading, or feature-seeding questions.

### Relevance and exits

- Include only the most relevant Marq proof points and state what buyer-validated problem each would support.
- Identify risks to avoid, including assumptions, premature positioning, missing stakeholders, and weak next-step logic.
- Propose a concrete next step using `What / Who / Why` if fit is confirmed.
- State an appropriate exit if fit is not confirmed: close, nurture with a named trigger/date, redirect, or gather one missing fact before deciding.

## Quality gate

Before returning the brief, verify:

- It is for one scheduled call or named account.
- A supplied deal or account name was searched in HubSpot when available; the rep was not asked to locate or paste the record link.
- The resolved HubSpot record is supported by association, meeting, participant, owner, stage, or timing evidence rather than name similarity alone.
- Facts, public signals, hypotheses, unknowns, and conflicts are visibly distinct.
- No question repeats a reliable answer already in context without explaining why reconfirmation matters.
- There are six to eight core questions, each tied to a decision-relevant learning objective.
- The questions adapt to call type, persona, buyer state, deal maturity, and time.
- Business impact and decision context are explored without presupposing urgency.
- Demo content, if any, follows buyer-validated relevance and is narrow enough to earn the next decision.
- Customer proof and product claims are traceable and current enough for buyer use.
- The target exit can legitimately be `not qualified` or `not now`.
- No post-call email or operational follow-through was added.

If research is too thin, return a useful low-confidence brief with explicit unknowns. Do not manufacture specificity.
