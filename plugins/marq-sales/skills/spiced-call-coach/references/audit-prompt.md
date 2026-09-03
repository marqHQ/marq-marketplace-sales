# Independent SPICED Coaching Audit Prompt

Audit a draft SPICED sales-call analysis for factual accuracy and usefulness to the sales rep. Keep the audit tight, evidence-based, and editorially actionable. Do not rewrite the entire analysis.

## Inputs

- **Complete transcript or recording ID/URL:** `[TRANSCRIPT SOURCE]`
- **Draft analysis path:** `[DRAFT PATH]`
- **Analysis prompt path:** `[ANALYSIS PROMPT PATH]`
- **Known call context:** `[OPTIONAL CONTEXT]`
- **Audit output path:** `[AUDIT PATH]`

## Required process

1. Read the complete transcript independently. For a recording ID or URL, retrieve every transcript chunk by following continuation offsets until no text remains.
2. Read the complete draft analysis and analysis prompt.
3. Check each material conclusion against the transcript rather than trusting the draft's summary.
4. Evaluate two distinct qualities:
   - **Accuracy:** evidence fidelity, timestamps, attribution, inference labels, score anchors, coverage labels, arithmetic, and uncertainty.
   - **Coaching usefulness:** behavioral specificity, prioritization, natural replacement questions, practical next-call guidance, concision, and fairness to the call type and stage.

## Accuracy checks

- Buyer statements, seller claims, metadata, and inference are not conflated.
- CRM dates, seller ROI claims, enthusiasm, titles, conditional next steps, and named competitors are not overinterpreted.
- SPICED coverage is not confused with seller execution.
- Scores match the stated anchors. Do not recommend a score change merely because another score within the same reasonable range is possible.
- The overall score is the correct arithmetic mean to one decimal place.
- Timestamps support the exact claim being made.
- Missing evidence is described as not evidenced on this call, not as universally unknown.

## Usefulness checks

- The report has one clear primary coaching theme.
- Strengths are observable behaviors worth repeating.
- No more than three missed moments carry the coaching.
- Replacement discovery questions are singular, open or mirroring, and sound natural; direct commitment questions are allowed for scheduling or mutual next steps.
- Critical Event questions do not presuppose a deadline.
- The next-call plan continues the buyer's story instead of mechanically rerunning discovery.
- Advice is specific enough to practice and short enough to use in a manager-rep coaching session.
- Repetition, generic advice, and low-value criticism are removed.

## Required audit output

Write a concise Markdown audit with these sections:

### Verdict

Give one sentence on accuracy and one sentence on coaching usefulness.

### Must fix

List only material factual, evidentiary, arithmetic, rubric, or harmful-coaching issues. For each item provide:

- Draft section or claim
- Transcript evidence and timestamp
- Why it matters
- Exact recommended correction

Write `None` when there are no material errors.

### Recommended improvements

Give at most three optional edits that materially improve clarity, concision, or actionability. Do not suggest stylistic churn.

### Preserve

Name the strongest elements that should remain unchanged.

### Final edit list

Provide a short numbered list labeled `Accept as must-fix`, `Consider`, or `Do not change`. The primary agent will make the final decision.
