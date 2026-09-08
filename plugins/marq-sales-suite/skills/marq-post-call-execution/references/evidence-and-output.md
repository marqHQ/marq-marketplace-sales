# Evidence Model and Post-Call Deliverable

## Evidence classes

Assign exactly one class to each material statement:

| Class | Meaning | Safe use |
|---|---|---|
| `CUSTOMER_STATED` | A customer participant explicitly said or unambiguously agreed to it on the call. | Analysis, CRM proposal, and customer email when accurately paraphrased. |
| `CRM_SUPPORTED` | It appears in a specific CRM record or activity, with the record and freshness identified. | Analysis and CRM comparison. Use in email only when it is also customer-safe and not contradicted. |
| `SELLER_INTERPRETATION` | The seller stated, inferred, or characterized it without customer confirmation. | Internal analysis only; never present as customer fact. |
| `CODEX_INFERENCE` | Codex derived it from patterns or incomplete evidence. | Internal recommendation only; never write as fact or state in the email. |
| `UNKNOWN` | The source set does not establish it. | Qualification gap; never fill with a guess. |

For every material claim, include a locator such as transcript timestamp/speaker, note section, or CRM object/property and last-updated date. Short paraphrases are preferred. Use quotation marks only for exact transcript language.

If sources conflict, display both claims and their evidence classes, name the conflict, and recommend verification. Newer evidence may be more useful but does not silently erase the older record.

## Qualification rules

Use SPICED as a coverage model, not a seller scorecard:

- Situation: current people, process, tools, scope, and constraints.
- Pain: concrete problems or friction the customer recognizes.
- Impact: operational, financial, strategic, or personal consequences. Do not fabricate quantification.
- Critical Event: a real deadline, triggering event, or consequence of delay. A seller target close date is not a customer critical event.
- Decision: decision criteria, process, stakeholders, budget/approval path, alternatives, and authority.

Coverage labels:

- Confirmed: material customer evidence answers the component for the current stage.
- Partial: some useful evidence exists but an important dimension remains open.
- Missing: no usable customer evidence exists.
- Contradicted: sources materially disagree.

Champion and economic buyer are roles, not compliments or titles. Mark a champion only when there is evidence of internal influence plus active advocacy. Mark an economic buyer only when final financial authority is established. Otherwise use potential stakeholder or Unknown.

## Required deliverable

Start with `HubSpot record used` and provide the resolved deal name, company, record ID, match method, and clickable URL. If no deal was found, say so and provide the matched company record when available.

Produce these sections in order:

1. Executive call summary — three to five factual bullets; include call type and outcome.
2. Customer priorities and pain — evidence-tagged.
3. Business impact — separate quantified and qualitative impact; use Unknown when absent.
4. Desired future state — outcomes, not assumed product features.
5. Qualification findings — Situation, Pain, Impact, Critical Event, Decision with coverage and evidence.
6. Qualification gaps — prioritized questions that would change deal strategy; avoid a generic questionnaire.
7. Stakeholder map — name, title, role, stance, influence/authority evidence, and unknowns.
8. Customer commitments — action, owner, due date, evidence, and status.
9. Marq commitments — action, owner, due date, evidence, and status.
10. Risks and objections — distinguish explicit objections, execution risks, and Codex inferences.
11. Recommended next step — what, who should attend, why it matters, Marq owner, customer owner, and specific date. If a date was not agreed, label it proposed.
12. Proposed HubSpot changes — exact internal property name, label, current value, proposed value, evidence class, source, and rationale. Include guarded executive fields even when the result is `No change proposed`.
13. Draft customer email — subject and body; visibly label it Draft.
14. Next-call preparation — three to seven specific items tied to open qualification or commitments.
15. Approval status — say `No CRM records were changed and no message was sent.` Then list the actions available for separate approval.

## Commitment capture

Capture every explicit commitment and date, including small follow-ups such as sending security material or inviting another stakeholder. Keep customer and Marq commitments separate. An action without a named or clearly implied owner is incomplete. An action without a due date is `date unknown`, not `ASAP`.

## CRM proposal threshold

Propose a routine descriptive field only when supported by `CUSTOMER_STATED` or fresh, uncontradicted `CRM_SUPPORTED` evidence. `SELLER_INTERPRETATION` and `CODEX_INFERENCE` may explain a recommendation but must not become proposed factual values. Executive fields—stage, amount, forecast category, and close date—need explicit supporting evidence and always remain approval-only.
