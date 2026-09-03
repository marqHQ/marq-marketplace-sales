# Transcript Analysis Review Prompt

Independently review the completed transcript analysis.

Read:

- The full Gong transcript provided with this task
- [transcript-analysis-prompt.md](transcript-analysis-prompt.md)
- The completed JSON at `{{OUTPUT_JSON_PATH}}`

Check for material problems:

- Missing, empty, or incorrectly named fields
- Industry classification unsupported by the transcript
- Internal Marq participants incorrectly treated as external customer participants
- Challenges, priorities, scale, or outcomes inferred from an AE's question, pitch, recap, hypothesis, or paraphrase rather than substantively stated by the customer
- A generic customer acknowledgement incorrectly treated as confirmation of an AE's claim
- Quotes containing an AE's words or attributed to the wrong speaker
- Ambiguous shared-microphone or diarization attribution presented as certain without an explicit nearby handoff or other adequate conversational evidence
- Important current customer pain missed in favor of a weaker hypothetical, exploratory, or future use case
- Three challenges that are duplicative symptoms rather than distinct priorities, including a root problem and its scaling consequence separated even though both map to the same solution
- Feature questions presented as challenges without identifying the underlying customer problem
- Challenge titles or summaries that are vague, abstract, duplicative, unsupported, or unnecessarily long
- Summaries that robotically narrate the interview participant by name instead of describing the organization, team, workflow, or process
- Repetitive constructions such as "[Name] needs," "[Name] wants," or "[Name] lacks"
- Language that is blaming, embarrassing, or unsuitable for showing directly to the customer
- Meaningful scale or consequence omitted when clearly established by the customer
- Quotes that are not verbatim, substantive, contiguous, correctly attributed, or within the length limit
- Incorrect speaker, timestamp, or reported-speech metadata
- Summaries and quotes that merely repeat one another instead of synthesis plus evidence
- Solutions that do not address their paired challenges, cram together unrelated capabilities, or rely on unsupported AE product claims
- Outcomes that repeat the solution, are generic enough for any customer, or imply unsupported guarantees
- Invented metrics, outcomes, commitments, integrations, product functionality, or implementation claims

Do not edit the JSON or any other file. If no material issue exists, report `PASS`. Otherwise, report only actionable findings. For each finding, include the affected JSON field, the issue, transcript evidence, and a recommended correction.
