# Transcript Analysis Review Prompt

Independently review the completed transcript analysis.

Read:

- Every full Gong, attached, pasted, or linked transcript provided with this task
- [external-hosted-evidence.md](external-hosted-evidence.md)
- [call-selection-and-coverage.md](call-selection-and-coverage.md)
- [transcript-analysis-prompt.md](transcript-analysis-prompt.md)
- [template-copy-budgets.json](template-copy-budgets.json)
- The same approved Marq messaging sources supplied to the analysis subagent; if they are missing, report that the solution claims cannot be verified rather than returning `PASS_READY`
- The completed JSON at `{{OUTPUT_JSON_PATH}}`

Check for material problems:

- Missing, empty, or incorrectly named fields
- `evidence_sources`, `sources_reviewed`, or quote provenance that does not match the supplied corpus
- `sources_reviewed` entries that are objects rather than source ID strings
- Missing or incorrect meeting-host and transcript-source provenance for an external transcript
- A missing transcript timestamp presented as a real timestamp instead of `null`
- `availability_status` that does not distinguish no meeting, a meeting without a transcript, or an insufficient transcript
- A missing transcript labeled `insufficient_evidence` instead of the pending `needs_user_decision` state
- A known meeting without a usable transcript counted in `evidence_sources` or `sources_reviewed` rather than retained as a pending-source note
- An AE note, automated summary, partner summary, or user recap treated as customer-confirmed transcript evidence
- A call set that omits a clearly more discovery-rich supplied call without justification
- Industry classification unsupported by the prospect's actual operating model, including a merely adjacent vertical chosen instead of `generic`
- Internal Marq participants incorrectly treated as external customer participants
- Challenges, priorities, scale, or outcomes inferred from an AE's question, pitch, recap, hypothesis, or paraphrase rather than substantively stated by the customer
- A generic customer acknowledgement incorrectly treated as confirmation of an AE's claim
- Quotes containing an AE's words or attributed to the wrong speaker
- Ambiguous shared-microphone or diarization attribution presented as certain without an explicit nearby handoff or other adequate conversational evidence
- Important current customer pain missed in favor of a weaker hypothetical, exploratory, or future use case
- A user-supplied candidate accepted without transcript support, or rejected/displaced without an evidence-based reason
- Three challenges that merely restate the same customer evidence and operational failure with substantially the same intervention and outcome
- Related challenges rejected solely because they share a stakeholder, workflow, platform, or primary Marq capability, even though each is customer-supported and resolving one would leave another materially unresolved
- Feature questions presented as challenges without identifying the underlying customer problem
- Challenge titles or summaries that are vague, abstract, duplicative, unsupported, or unnecessarily long
- Summaries that robotically narrate the interview participant by name instead of describing the organization, team, workflow, or process
- Repetitive constructions such as "[Name] needs," "[Name] wants," or "[Name] lacks"
- Language that is blaming, embarrassing, or unsuitable for showing directly to the customer
- Meaningful scale or consequence omitted when clearly established by the customer
- Quotes that are not substantive, contiguous, correctly attributed, within the length limit, or faithful to the customer's substantive words, order, and meaning
- Displayed quotes that depend on missing context, contain unresolved pronouns or apparent transcription artifacts, or otherwise do not stand on their own for a customer reader
- A displayed quote that cannot be derived from `transcript_excerpt` using only documented capitalization, apostrophe, hyphenation, boundary trimming, or punctuation edits
- Missing, non-contiguous, or inexact `transcript_excerpt` values, or missing/inaccurate `presentation_edits`
- Displayed quotes whose first alphabetic character is lowercase or whose ending punctuation is missing or inappropriate
- A summary retained with a confusing quote when a cleaner customer-supported framing exists, or a challenge forced into the MAP even though no readable self-contained quote can prove it
- Titles, summaries, quotes, or outcomes that exceed the applicable template copy budget
- Incorrect speaker, timestamp, or reported-speech metadata
- Incorrect source ID, title, date, URL, meeting host, transcript source, or a quote attributed to the wrong source
- Cross-call synthesis that ignores a newer contradiction, treats repetition as a separate challenge, or implies unsupported consensus
- Historical or closed-lost-cycle evidence presented as current without an explicit internal-test limitation or required user decision
- Summaries and quotes that merely repeat one another instead of synthesis plus evidence
- Solutions that do not address their paired challenges, cram together unrelated capabilities, or rely on unsupported AE product claims
- Outcomes that repeat the solution, are generic enough for any customer, or imply unsupported guarantees
- Invented metrics, outcomes, commitments, integrations, product functionality, or implementation claims
- `evidence_coverage.status: ready` when fewer than three distinct, separately actionable pairs pass review
- `insufficient_evidence` declared while three stronger, distinct customer-supported priorities exist in the supplied corpus

Do not edit the JSON or any other file.

- Report `PASS_READY` when exactly three distinct challenge/solution pairs pass and `evidence_coverage.status` is `ready`.
- Report `PASS_INSUFFICIENT` when the analysis correctly concludes that the supplied corpus supports fewer than three and the coverage metadata is accurate.
- Otherwise report only actionable findings. For each finding, include the affected JSON field, the issue, transcript and call evidence, and a recommended correction.
