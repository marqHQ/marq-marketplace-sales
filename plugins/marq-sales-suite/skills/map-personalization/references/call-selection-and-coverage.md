# Call Selection and Evidence Coverage

Use this reference when choosing call transcripts from Gong or an external-hosted meeting and deciding whether the standard three-card MAP is ready.

## Rank Calls for Discovery Value

Evaluate source metadata, participants, title, brief when available, and transcript content together.

Prefer:

1. Discovery conversations where external participants explain current workflows, pain, scale, consequences, or desired outcomes
2. Demos containing substantive customer elaboration rather than feature acknowledgements
3. Strategy, evaluation, or stakeholder-alignment calls with decision criteria
4. Recent calls that confirm, update, or supersede earlier evidence

Down-rank:

- Pricing-only or packaging updates
- Training and implementation sessions
- Administrative check-ins
- Calls dominated by the AE
- Very short calls or calls with only generic customer acknowledgements

A down-ranked call may still contribute evidence when the customer independently states a substantive priority.

## Incremental Retrieval

1. Retrieve the highest-ranked call in full.
2. Build a private candidate list of customer-supported priorities.
3. If fewer than three distinct, separately actionable priorities are plausible, retrieve the next-highest-ranked call.
4. Continue until three strong candidates exist or five relevant calls have been reviewed.
5. Stop earlier when additional calls are clearly redundant or outside the current sales cycle.

Do not optimize for call count. Optimize for three distinct, current, defensible, separately actionable priorities.

## Calibrate Distinctness

Treat a challenge as distinct when it is directly supported by customer evidence and describes a different operational condition, control point, or consequence that can be addressed on its own. Related challenges may coexist within the same workflow, team, or platform.

Use this test:

1. Does the customer substantively describe this condition rather than merely agree with an internal participant?
2. Would resolving another selected challenge leave this condition materially unresolved?
3. Can its summary, intervention, and expected outcome be meaningfully differentiated without inventing facts or superficial wording?

Do not consolidate challenges merely because they are related, share a stakeholder, or can be addressed by the same platform. Consolidate them when they rely on substantially the same customer evidence, describe the same operational failure, and lead to substantially the same intervention and outcome. A cause and consequence may remain separate only when the customer establishes each as a meaningful, separately actionable priority.

An automated brief, AI summary, AE note, partner summary, or user recap may nominate candidates for transcript review, but it is not customer evidence. Confirm every selected challenge in the transcript itself.

If the user supplies candidate challenges, themes, or a call summary, evaluate those candidates before unprompted alternatives. Keep a supported candidate when it is among the three strongest separately actionable priorities. If it is rejected or displaced, record a concise evidence-based reason under `rejected_candidates` or `notes`. Never preserve a user candidate by weakening the transcript-evidence standard.

## Cross-Call Synthesis

- Every quote must come from one contiguous external-customer speaker turn in one call.
- Prefer quotes that are understandable without surrounding transcript context. Reject ambiguous fragments or transcription artifacts rather than guessing what the customer intended.
- Preserve an exact raw excerpt for auditability; allow only documented display-level capitalization, boundary trimming, apostrophe, hyphenation, and punctuation cleanup.
- A summary may synthesize consistent evidence across calls, but `quote_evidence` must identify the source proving it.
- Repetition across calls increases confidence but does not create a second challenge.
- Newer explicit customer statements override conflicting older statements.
- Keep older evidence only when it remains current and no later call contradicts it.
- Treat calls from an old or closed-lost sales cycle as historical unless a newer customer statement revalidates them. For an internal test, historical evidence may be used when `notes` clearly state the call dates, prior cycle status, and that the priorities are not confirmed current. For a customer-facing MAP, set `status` to `needs_user_decision` until current validation is added or the user explicitly approves the historical-evidence path.
- Do not merge statements from different speakers into a single quote or imply organizational consensus without evidence.
- Do not import common vertical pain from the playbook into the account's evidence.

## Readiness States

Set `evidence_coverage.status` to:

- `ready`: exactly three distinct, separately actionable challenges and their paired solutions pass review.
- `insufficient_evidence`: usable transcripts were fully reviewed and fewer than three defensible challenges remain.
- `needs_user_decision`: a transcript is missing or pending, or ambiguity about the contact, sources, sales cycle, template, or hypothesis path requires user direction.

Record:

- `confirmed_challenges`: integer from 0 to 3
- `required_challenges`: always 3 for the standard template
- `availability_status`: `transcript_ready`, `no_meeting_found`, `meeting_without_transcript`, or `transcript_insufficient`
- `sources_reviewed`: source ID strings included in the analysis corpus; do not store source objects here
- `rejected_candidates`: concise internal reasons, without exposing them as customer-facing copy
- `notes`: material recency, attribution, or contradiction issues

## Creation Gate

The standard three-card project is ready only when:

- `status` is `ready`
- `confirmed_challenges` equals 3
- all three challenge quotes are resolved and correctly attributed
- all three solutions use approved Marq capabilities
- the independent reviewer returns `PASS_READY`

If any condition fails, do not create the standard project.
