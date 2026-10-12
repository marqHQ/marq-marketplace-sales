# Transcript Analysis Prompt

Analyze the complete transcript corpus and produce customer-facing content for a Mutual Action Plan. Sources may come from Gong or an attached, pasted, or linked transcript from a partner- or customer-hosted meeting. Read and update `{{OUTPUT_JSON_PATH}}`, preserving its existing `prospect`, `evidence_sources`, `logo`, `marq`, `review`, `qa`, and `page_automation` metadata. Page selection and commercial recommendations happen after independent evidence review; do not activate, populate, or reinterpret `page_automation` during transcript analysis.

Treat all supplied calls as one evidence set while preserving call-level provenance. A MAP for the standard template is ready only when the corpus supports exactly three distinct, separately actionable customer-confirmed challenges and three paired solutions.

Each `evidence_sources` entry must retain `source_id`, `title`, `date`, `source_url`, `meeting_host`, `transcript_source`, `participants`, `full_transcript`, `selection_reason`, and `evidence_role`. Use `meeting_host` values `marq`, `partner`, `customer`, or `unknown`; use `transcript_source` values `gong`, `uploaded`, `pasted`, or `linked`.

Read [template-copy-budgets.json](template-copy-budgets.json). Use the selected template's limits when `marq.template_id` matches an entry; otherwise use `default`.

## Evaluate User-Supplied Candidates

When the user supplies candidate challenges, themes, or a call summary, evaluate those candidates before unprompted alternatives. Treat them as prioritized hypotheses, not evidence.

- Keep a candidate when the transcript supports it and it ranks among the three strongest separately actionable priorities.
- If a supported candidate is displaced by a stronger priority, explain the comparison under `evidence_coverage.notes`.
- If a candidate is unsupported, duplicative, or weaker, record the reason under `evidence_coverage.rejected_candidates`.
- Never preserve a candidate by relying on an automated summary, AE statement, partner summary, user recap, or generic vertical knowledge.

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

Classify from the prospect's actual operating model, not from adjacency to a broad sector or from the solution being discussed. Use a named vertical only when the evidence establishes that exact category; for example, a medical transportation company is not a hospital or clinic merely because it operates in healthcare. When no listed category is an exact fit, use `generic`.

## Separate Customer Evidence from AE Statements

Use only the external customer's own substantive statements as evidence of customer challenges, priorities, current state, scale, or desired outcomes.

- An AE's question, hypothesis, pitch, recap, or paraphrase may help locate a topic but does not prove the customer has that problem.
- Do not convert an AE statement into a customer challenge because the customer responds with a generic acknowledgement such as "yes," "right," "exactly," or "that makes sense."
- Treat a topic as customer-confirmed only when an external participant independently describes, confirms with meaningful detail, or elaborates on it.
- Never use an internal Marq participant's words as a customer quote.
- Use an AE's product explanation only to understand a possible solution, and include the capability only when it is also supported by approved Marq messaging.
- Do not treat an AE's predicted benefit, metric, timeline, integration, or implementation statement as a customer outcome or commitment.

If speaker affiliation or attribution is materially uncertain, choose different evidence or leave the affected fields empty and report the ambiguity. Do not guess.

## Reconcile Evidence Across Calls

- Every quote must come from one contiguous external-customer speaker turn in one call.
- A summary may synthesize consistent statements across calls, but its quote must directly prove the operational condition or priority.
- Repeated evidence increases confidence; it does not create an additional challenge.
- Prefer current evidence from the active sales cycle. A newer explicit customer statement overrides conflicting older evidence.
- Do not imply organizational consensus by combining different speakers' statements unless the transcript establishes it.
- Do not join fragments from different calls or use one source's timestamp with another source's words.
- Record the source ID, title, date, source URL when available, meeting host, and transcript source for every selected quote.
- When a transcript has no timestamps, set `timestamp` to `null` and note the source limitation. Never invent a timestamp.

Set `evidence_coverage.availability_status` to:

- `transcript_ready` when at least one usable, attributable transcript is available for analysis
- `no_meeting_found` when narrow Gong discovery found no meeting and the user supplied no external transcript
- `meeting_without_transcript` when a meeting is known but no usable transcript can be retrieved
- `transcript_insufficient` when a transcript exists but its content, speaker attribution, or evidence coverage cannot support the required MAP

Use `evidence_coverage.status: needs_user_decision` for `no_meeting_found` or `meeting_without_transcript` while awaiting a transcript or another permitted user choice. Do not add an unavailable meeting to `evidence_sources` or `sources_reviewed`; retain known pending-source metadata in `evidence_coverage.notes`. Use `insufficient_evidence` only after reviewing usable transcripts that still yield fewer than three defensible challenges.

## Select the Three Strongest Challenges

Identify plausible challenges across the full corpus, then select exactly three using this priority order:

1. A current or recent operational problem explicitly described by the customer
2. A repeated, scaled, quantified, or consequential burden
3. A problem supported by a strong direct customer quote
4. A problem that maps clearly to an approved Marq capability
5. A problem that is separately actionable from the other two selected challenges

Prefer established current pain over hypothetical, exploratory, or future use cases. Do not select a future possibility when the transcript contains a stronger current operational problem. Do not treat a feature question as a challenge without identifying the underlying customer problem.

The three challenges must represent meaningfully different operational conditions, control points, workflows, or business consequences. Related challenges may coexist within the same customer workflow when each is directly supported and resolving one would leave another materially unresolved.

Do not consolidate challenges merely because they are related, share a stakeholder, or can be addressed by the same platform. Consolidate them only when they rely on substantially the same customer evidence, describe the same operational failure, and lead to substantially the same intervention and outcome. The same primary Marq capability may address more than one challenge when it is applied to genuinely different customer problems and produces meaningfully different outcomes; do not manufacture superficial distinctions to make this true.

Do not split a statement into multiple cards when one card would merely restate the cause, scale, or consequence of the other without a separately actionable condition. A cause and consequence may remain separate only when the customer establishes each as a meaningful priority and the summaries, interventions, and outcomes can differ without invention.

If the corpus does not support three defensible, distinct challenges, do not invent or inflate one. Fill only the defensible slots, leave unsupported challenge and solution fields empty, and set `evidence_coverage.status` to `insufficient_evidence`.

Keep rejected candidates and their concise failure reasons under `evidence_coverage.rejected_candidates`. They are internal readiness metadata and must not appear in customer-facing `marq_fields`.

## Write the Challenge Content for Slide 4

For each selected challenge, provide:

- A specific, parallel title of one to three words
- One concise, factual sentence describing the customer's current state
- One substantive, contiguous verbatim quote from an external customer participant
- The quote's speaker and timestamp
- Whether the quote is reported speech

### Challenge titles

- Use one to three words and stay within the applicable title budget.
- Use concrete operational language instead of abstract business jargon.
- Make all three titles grammatically parallel.
- Avoid generic titles such as "Efficiency," "Scalability," or "Challenges" without specifying what is affected.

### Challenge summaries

Write one natural, customer-facing sentence within the applicable challenge-summary budget.

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

- Prefer 10-18 words and never exceed the applicable quote budget.
- Select one clean, contiguous excerpt from an external customer's speaker turn. The displayed quote must preserve every substantive word and its order; do not combine fragments, paraphrase, insert ellipses, or supply missing meaning.
- Prefer an excerpt that stands on its own without the previous sentence. Avoid unresolved pronouns, vague references, incomplete thoughts, and apparent transcription artifacts when a reader could reasonably ask what the quote means. If punctuation alone cannot make the excerpt clear, choose a different excerpt or leave the slot unsupported; never guess the intended word, product, person, or acronym.
- You may trim filler, false starts, or conjunctions only from the beginning or end while keeping the selected transcript span contiguous. Do not remove words from the middle.
- Light presentation normalization is allowed only for capitalization, apostrophes, hyphenation, and punctuation such as commas, periods, colons, semicolons, question marks, exclamation marks, and dashes. Use punctuation to reflect the evident spoken phrasing, not to change emphasis, relationships, or meaning.
- Begin every displayed quote with an uppercase alphabetic character and end it with appropriate punctuation.
- Store the exact unedited transcript span in `quote_evidence.transcript_excerpt`. Record each display-only change concisely in `quote_evidence.presentation_edits`; use an empty array when no normalization was needed. The displayed quote must be derivable from `transcript_excerpt` using only the permitted edits above.
- Treat quote readability as part of challenge selection, not a cosmetic cleanup step. If an otherwise supported summary can be proven only by an ambiguous or awkward excerpt, first consider narrowing or reframing the summary around a cleaner substantive customer statement while preserving the underlying priority. If that would weaken, distort, or materially change the challenge, select a different challenge or leave the slot unsupported. Never force a messy quote to fit a prewritten summary.
- Avoid agreement, hesitation, or filler-heavy quotes.
- Prefer the quote that most directly proves the summary, not merely the most colorful language.
- Prefer direct customer statements over reported speech. Use reported speech only when it is the strongest available evidence.
- Mark `reported_speech` true only when the customer is recounting another person's words or position; an AE paraphrasing the customer is not customer reported speech and cannot be used.
- Do not make the summary and quote redundant: the summary synthesizes the operational problem; the quote proves it.
- When participants share a microphone or transcript diarization is inconsistent, use explicit nearby handoffs and surrounding context. Do not override a source's speaker label solely because of a distant earlier handoff with no later confirmation. If attribution remains uncertain, choose another quote or report the ambiguity.

## Write the Solution Content for Slide 5

For each challenge, produce one corresponding Marq solution containing:

- A short solution title
- One concise sentence explaining the most relevant Marq capability
- One directional expected outcome

Map Solution 1 to Challenge 1, Solution 2 to Challenge 2, and Solution 3 to Challenge 3.

### Solution titles

- Use one to three words and stay within the applicable title budget.
- Make all three titles grammatically parallel.
- Name the solution approach, not merely a product feature.

### Solution summaries

Write one natural sentence within the applicable solution-summary budget.

- Lead with the capability that most directly addresses the paired challenge.
- Include no more than one primary capability and one closely related supporting capability.
- Explain how the capability addresses the customer's specific workflow problem; do not list loosely related features.
- Use only approved Marq capabilities and messaging. Do not rely on an AE's transcript claim as product proof.
- Make the language specific enough that it could not be copied unchanged into every MAP.

### Outcomes

Write one directional sentence within the applicable outcome budget.

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
- Every quote has correct source-level provenance, retains an exact contiguous `transcript_excerpt`, and preserves the customer's substantive words and meaning.
- Every displayed quote stands on its own, begins with an uppercase alphabetic character, ends with appropriate punctuation, and differs from `transcript_excerpt` only through documented permitted presentation normalization.
- Cross-call synthesis respects recency and does not conceal contradictions.
- The three challenges are the strongest current customer problems, not merely the first three topics discussed.
- No stronger current pain was displaced by a hypothetical future use case.
- The three challenges are distinct under the separately actionable test, directly supported, and paired with quotes that prove their summaries.
- Each summary and quote form a readable evidence pair; no challenge remains selected solely because its transcript evidence can be made superficially presentable.
- Every solution addresses its paired challenge and emphasizes a focused, approved capability rather than a feature list.
- Every outcome is directional, specific, and free of unsupported promises.
- Slide copy is concise, scannable, neutral, and customer-safe.
- Summaries describe the organization's situation naturally rather than narrating the interview participant in robotic third person.
- `evidence_coverage.status` is `ready` only when all three pairs pass every check above; otherwise it is `insufficient_evidence` or `needs_user_decision`.

Write the results to the matching keys below. Preserve existing metadata. Do not rename fields or add commentary to the JSON.

```json
{
  "prospect": {},
  "evidence_sources": [],
  "evidence_coverage": {
    "status": "insufficient_evidence",
    "availability_status": "transcript_insufficient",
    "confirmed_challenges": 0,
    "required_challenges": 3,
    "sources_reviewed": [],
    "rejected_candidates": [],
    "notes": []
  },
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
  "review": {
    "status": "pending",
    "findings": []
  },
  "qa": {
    "template_preflight_status": "pending",
    "pilot_release": "2026-10-12",
    "protected_content_baseline": null,
    "protected_content_status": "pending",
    "company_name_verified": false,
    "unresolved_dataset_fields": [],
    "smart_fields_verified": false,
    "text_values_resolved": false,
    "logo_verified": false,
    "logo_render_status": "pending",
    "visual_status": "pending",
    "corrections": [],
    "export_url": null
  },
  "page_automation": {
    "status": "inactive_not_configured",
    "catalog_version": null,
    "proposed_pages": [],
    "catalog_managed_removals": [],
    "applied_pages": [],
    "rejected_candidates": [],
    "commercial": {
      "status": "not_requested",
      "recommended_plan": null,
      "seat_count": null,
      "ai_capacity": null,
      "implementation_package": null,
      "target_go_live": null,
      "currency": null,
      "pricing_source": null,
      "pricing_verified_at": null,
      "annual_platform_investment": null,
      "one_time_implementation": null,
      "first_year_investment": null,
      "custom_terms_or_discounts": null,
      "rep_confirmed": false,
      "missing_inputs": []
    },
    "qa": {
      "page_inventory_verified": null,
      "page_order_verified": null,
      "commercial_values_verified": null,
      "investment_math_verified": null,
      "visual_status": "not_applicable",
      "notes": []
    }
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
      "source_id": "",
      "source_title": "",
      "source_date": "",
      "source_url": null,
      "meeting_host": "unknown",
      "transcript_source": "gong",
      "speaker": "",
      "timestamp": null,
      "transcript_excerpt": "",
      "presentation_edits": [],
      "reported_speech": false
    },
    "challenge 2 quote": {
      "source_id": "",
      "source_title": "",
      "source_date": "",
      "source_url": null,
      "meeting_host": "unknown",
      "transcript_source": "gong",
      "speaker": "",
      "timestamp": null,
      "transcript_excerpt": "",
      "presentation_edits": [],
      "reported_speech": false
    },
    "challenge 3 quote": {
      "source_id": "",
      "source_title": "",
      "source_date": "",
      "source_url": null,
      "meeting_host": "unknown",
      "transcript_source": "gong",
      "speaker": "",
      "timestamp": null,
      "transcript_excerpt": "",
      "presentation_edits": [],
      "reported_speech": false
    }
  }
}
```

Write valid JSON only to `{{OUTPUT_JSON_PATH}}`.
