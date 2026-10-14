# External-Hosted Meeting Evidence

Use this fallback only after the narrow Gong searches in Step 2 find no usable transcript.

## Rep-Facing Prompt

Say:

> I couldn't find a usable Gong transcript for this opportunity. Was the meeting hosted by a partner or the customer? If so, attach or paste the transcript, or provide an accessible transcript link. I'll apply the same evidence and review standards. If no transcript is available, you can create the MAP manually or explicitly approve a separately labeled hypothesis-only internal draft.

When a Gong meeting exists without a transcript, replace the first sentence with: "I found the meeting, but it does not have a usable Gong transcript."

## Accepted Transcript Inputs

Accept:

- Transcript text pasted directly into the conversation
- An attached transcript file such as TXT, DOCX, or PDF
- An accessible transcript link from a partner- or customer-hosted Zoom, Teams, or similar meeting platform

A recording link is usable only when its transcript can be retrieved. Do not claim to have reviewed an inaccessible recording.

## Provenance

For every source, record:

- `source_id`: Gong call ID or a stable generated ID for an external transcript
- `title` and meeting `date`
- `source_url` when available
- `meeting_host`: `marq`, `partner`, `customer`, or `unknown`
- `transcript_source`: `gong`, `uploaded`, `pasted`, or `linked`
- Participants and their affiliations when known

Use the same transcript-selection, attribution, quotation, evidence-coverage, and independent-review standards regardless of source.

## Evidence Boundaries

- A customer statement in a partner- or customer-hosted transcript is valid customer evidence when its speaker is identifiable.
- A transcript without timestamps may still be used; set the timestamp to `null` and note that the source did not provide one. Never invent a timestamp.
- A transcript without reliable speaker labels cannot support attributed customer quotes. Treat it as insufficient evidence unless the ambiguity can be resolved from nearby introductions or explicit handoffs.
- AE notes, CRM notes, Gong AI summaries, partner summaries, and user-written recaps are not customer-confirmed evidence. They may nominate hypotheses only.
- Distinguish `no_meeting_found`, `meeting_without_transcript`, and `transcript_insufficient` in `evidence_coverage.availability_status`.
- When the rep confirms that a partner- or customer-hosted meeting exists but has not supplied a usable transcript, set `availability_status` to `meeting_without_transcript` and `status` to `needs_user_decision` while awaiting the transcript or the user's choice of another permitted path.
- Do not add a meeting without a usable transcript to `evidence_sources` or `sources_reviewed`. Record any known date, title, host, participants, and link as a pending-source note under `evidence_coverage.notes` until a usable transcript is supplied.
- Reserve `status: insufficient_evidence` for a completed review of usable transcripts that yields fewer than three defensible challenges; a missing transcript is a pending user decision, not failed content analysis.
- If no usable transcript is available, stop before customer-confirmed project creation. Offer manual creation or a handoff to a separately approved, labeled hypothesis-only workflow. This skill and its validator do not implement that alternative; do not continue through standard creation with hypothesis evidence.
