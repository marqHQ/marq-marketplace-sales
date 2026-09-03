# Transcript Analysis Prompt

Analyze the full Gong transcript and produce customer-facing content for a Mutual Action Plan. Read and update `{{OUTPUT_JSON_PATH}}`, preserving its existing `prospect`, `gong_call`, `logo`, and `marq` metadata.

## Identify Participants and Industry

Identify internal Marq participants and external customer participants before selecting evidence. Use participant affiliation, email domain, title, introductions, and conversational context together; do not assume a speaker with unknown affiliation is a customer.

Classify the prospect's industry as one of:

- higher ed
- hospitals and clinics
- real estate
- manufacturing
- insurance
- financial services
- generic

## Separate Customer Evidence from AE Statements

Use only the external customer's own substantive statements as evidence of customer challenges, priorities, current state, scale, or desired outcomes.

- An AE's question, hypothesis, pitch, recap, or paraphrase may help locate a topic but does not prove the customer has that problem.
- Do not convert an AE statement into a customer challenge because the customer responds with a generic acknowledgement such as "yes," "right," "exactly," or "that makes sense."
- Treat a topic as customer-confirmed only when an external participant independently describes, confirms with meaningful detail, or elaborates on it.
- Never use an internal Marq participant's words as a customer quote.
- Use an AE's product explanation only to understand a possible solution, and include the capability only when it is also supported by approved Marq messaging.
- Do not treat an AE's predicted benefit, metric, timeline, integration, or implementation statement as a customer outcome or commitment.

If speaker affiliation or attribution is materially uncertain, choose different evidence or leave the affected fields empty and report the ambiguity. Do not guess.

## Select the Three Strongest Challenges

Identify plausible challenges internally, then select exactly three using this priority order:

1. A current or recent operational problem explicitly described by the customer
2. A repeated, scaled, quantified, or consequential burden
3. A problem supported by a strong direct customer quote
4. A problem that maps clearly to an approved Marq capability
5. A problem distinct from the other two selected challenges

Prefer established current pain over hypothetical, exploratory, or future use cases. Do not select a future possibility when the transcript contains a stronger current operational problem. Do not treat a feature question as a challenge without identifying the underlying customer problem.

The three challenges must represent meaningfully different root causes, workflows, or business consequences. If two challenges would use substantially the same summary, solution, and outcome, consolidate them and select another priority.

Do not split a root problem from its scaling consequence into separate challenges when both lead to the same solution. For example, manual version creation and growth making that same manual work unsustainable belong in one challenge unless the customer describes a separate workflow or need.

If the transcript does not support three defensible, distinct challenges, do not invent or inflate one. Leave the unsupported challenge and solution fields empty and report that the evidence is insufficient.

Do not expose the candidate list or ranking in the JSON.

## Write the Challenge Content for Slide 4

For each selected challenge, provide:

- A specific, parallel title of one to three words
- One concise, factual sentence describing the customer's current state
- One substantive, contiguous verbatim quote from an external customer participant
- The quote's speaker and timestamp
- Whether the quote is reported speech

### Challenge titles

- Use one to three words and approximately 24 characters or fewer when practical.
- Use concrete operational language instead of abstract business jargon.
- Make all three titles grammatically parallel.
- Avoid generic titles such as "Efficiency," "Scalability," or "Challenges" without specifying what is affected.

### Challenge summaries

Write one natural, customer-facing sentence of approximately 14-24 words.

- Use the organization, team, workflow, or business process as the subject. Name the interview participant only when the individual's ownership is essential to the problem.
- Describe the operational reality, not the interview. Do not write "the customer said," "the prospect mentioned," or "during the call."
- Avoid repeatedly starting summaries with a person's name followed by "needs," "wants," "lacks," "manages," or "is evaluating."
- State who or what is affected, the present friction, and relevant scale or consequence when supported.
- Use neutral, respectful language suitable for showing directly to the customer. Do not portray individuals or teams as careless, resistant, or incompetent.
- Translate candid or negative customer language into diplomatic business language in the summary; preserve it only when used as a verbatim quote.
- Do not add causes, consequences, or scale that the customer's own statements do not establish.

Prefer:

- "The marketing team manually updates enrollment materials for every location."
- "Campus teams are creating last-minute assets outside approved brand standards."
- "Rapid location growth is increasing the volume of materials managed by the central team."

Avoid:

- "Brandon lacks time to create templates."
- "Margaret wants campus-specific materials."
- "Kailey is evaluating whether the platform is easy to use."

### Quote rules

- Target 12-22 words; never exceed 28 words.
- Use the external customer's exact recorded words from one speaker turn.
- Use one clean, contiguous excerpt; do not rewrite, combine excerpts, or insert ellipses.
- Avoid agreement, hesitation, or filler-heavy quotes.
- Prefer the quote that most directly proves the summary, not merely the most colorful language.
- Prefer direct customer statements over reported speech. Use reported speech only when it is the strongest available evidence.
- Mark `reported_speech` true only when the customer is recounting another person's words or position; an AE paraphrasing the customer is not customer reported speech and cannot be used.
- Do not make the summary and quote redundant: the summary synthesizes the operational problem; the quote proves it.
- When participants share a microphone or Gong diarization is inconsistent, use explicit nearby handoffs and surrounding context. Do not override Gong's speaker label solely because of a distant earlier handoff with no later confirmation. If attribution remains uncertain, choose another quote or report the ambiguity.

## Write the Solution Content for Slide 5

For each challenge, produce one corresponding Marq solution containing:

- A short solution title
- One concise sentence explaining the most relevant Marq capability
- One directional expected outcome

Map Solution 1 to Challenge 1, Solution 2 to Challenge 2, and Solution 3 to Challenge 3.

### Solution titles

- Use one to three words and approximately 24 characters or fewer when practical.
- Make all three titles grammatically parallel.
- Name the solution approach, not merely a product feature.

### Solution summaries

Write one natural sentence of approximately 14-24 words.

- Lead with the capability that most directly addresses the paired challenge.
- Include no more than one primary capability and one closely related supporting capability.
- Explain how the capability addresses the customer's specific workflow problem; do not list loosely related features.
- Use only approved Marq capabilities and messaging. Do not rely on an AE's transcript claim as product proof.
- Make the language specific enough that it could not be copied unchanged into every MAP.

### Outcomes

Write one directional sentence of approximately 10-18 words.

- Begin with a clear result-oriented verb when natural, such as "Reduce," "Give," "Keep," "Support," or "Protect."
- Describe why the change matters operationally rather than repeating the capability.
- Tie the outcome directly to the paired challenge.
- Do not promise guaranteed results or invent metrics, ROI, dates, adoption levels, or implementation commitments.
- Avoid vague outcomes such as "Improve efficiency," "Drive growth," or "Save time" without explaining what improves.
- Do not make the solution summary and outcome redundant: the summary explains how Marq helps; the outcome explains why it matters.

## Final Quality Check

Before writing the JSON, confirm:

- All challenge evidence comes from external customer participants, not Marq AEs.
- Every customer claim is independently stated or substantively confirmed by the customer rather than inferred from a leading AE question or recap.
- The three challenges are the strongest current customer problems, not merely the first three topics discussed.
- No stronger current pain was displaced by a hypothetical future use case.
- The three challenges are distinct, directly supported, and paired with quotes that prove their summaries.
- Every solution addresses its paired challenge and emphasizes a focused, approved capability rather than a feature list.
- Every outcome is directional, specific, and free of unsupported promises.
- Slide copy is concise, scannable, neutral, and customer-safe.
- Summaries describe the organization's situation naturally rather than narrating the interview participant in robotic third person.

Write the results to the matching keys below. Preserve existing metadata. Do not rename fields or add commentary to the JSON.

```json
{
  "prospect": {},
  "gong_call": {},
  "industry": "generic",
  "logo": {
    "source_url": null,
    "local_path": null,
    "source": null,
    "confirmed": false
  },
  "marq": {
    "template_id": null,
    "project_id": null,
    "project_url": null,
    "project_name": null
  },
  "marq_fields": {
    "challenge 1 title": "",
    "challenge 1 summary": "",
    "challenge 1 quote": "",
    "challenge 2 title": "",
    "challenge 2 summary": "",
    "challenge 2 quote": "",
    "challenge 3 title": "",
    "challenge 3 summary": "",
    "challenge 3 quote": "",
    "solution 1 title": "",
    "solution 1 summary": "",
    "solution 1 outcome": "",
    "solution 2 title": "",
    "solution 2 summary": "",
    "solution 2 outcome": "",
    "solution 3 title": "",
    "solution 3 summary": "",
    "solution 3 outcome": ""
  },
  "quote_evidence": {
    "challenge 1 quote": {
      "speaker": "",
      "timestamp": "",
      "reported_speech": false
    },
    "challenge 2 quote": {
      "speaker": "",
      "timestamp": "",
      "reported_speech": false
    },
    "challenge 3 quote": {
      "speaker": "",
      "timestamp": "",
      "reported_speech": false
    }
  }
}
```

Write valid JSON only to `{{OUTPUT_JSON_PATH}}`.
