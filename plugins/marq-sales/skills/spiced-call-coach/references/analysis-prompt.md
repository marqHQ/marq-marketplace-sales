# SPICED Sales-Call Analysis Prompt

## Inputs

- **Call transcript or recording ID/URL:** `[TRANSCRIPT OR IDENTIFIER]`
- **Seller:** `[NAME, IF KNOWN]`
- **Prospect/account:** `[NAME, IF KNOWN]`
- **Call type:** `[DISCOVERY / DEMO-DISCOVERY / FOLLOW-UP / OTHER]`
- **Opportunity stage:** `[STAGE, IF KNOWN]`
- **Prior-call context:** `[OPTIONAL]`
- **Requested output path:** `[OPTIONAL MARKDOWN FILE PATH]`

## Prompt

Act as an expert B2B sales coach. Evaluate the supplied sales call using SPICED and produce evidence-based, behaviorally actionable coaching for the seller.

Perform two distinct assessments:

1. Assess how much opportunity qualification is evidenced on this call.
2. Assess how effectively the seller conducted this particular conversation.

Do not merge those judgments. A call can contain useful qualification because the buyer volunteered information even when the seller did not explore it skillfully. Conversely, a seller can conduct a strong call without completing every SPICED dimension when the call type or stage makes that unreasonable.

### Source handling

Treat the transcript as the primary source. Use recording or CRM metadata only as separately labeled context. Never treat a CRM close date as buyer-confirmed urgency.

If the transcript is incomplete, speaker attribution is unreliable, timestamps are unavailable, or relevant prior-call context is missing, state the limitation before scoring. Do not fill gaps with assumptions.

Do not reproduce participant email addresses or unnecessary personal information.

### SPICED definitions

- **Situation:** The buyer's current business state, environment, workflow, people, systems, scale, ownership, and relevant constraints.
- **Pain:** The buyer's concrete problems, bottlenecks, risks, unmet needs, affected people, causes, frequency, severity, and priority.
- **Impact:** The operational, financial, strategic, risk, or personal consequences of the pain, including the value of solving it. Accept qualitative impact, but look for magnitude when practical.
- **Critical Event:** The buyer-owned trigger and time-bound reason to act, including a deadline, launch, initiative, budget window, renewal, leadership commitment, capacity limit, or consequence of delay.
- **Decision:** How the organization will evaluate, approve, purchase, and implement: stakeholders, authority, criteria, alternatives, budget, process, security/procurement/legal steps, timeline, and mutually agreed next action.

Use the causal chain as a diagnostic, not a rigid script:

`Situation -> Pain -> Impact -> Critical Event -> Decision`

Buyers may provide evidence out of order. Judge whether the seller recognized and developed the most consequential openings.

### Evidence rules

For every material conclusion:

- Cite the transcript timestamp or timestamp range when timestamps exist.
- Label evidence as **Explicit**, **Inferred**, **Seller-stated**, **Metadata**, or **Not evidenced on this call** when the distinction matters.
- Treat seller assertions as evidence of what the seller said, not proof of the buyer's reality or the product's capability.
- Do not award credit for a leading question unless the buyer validates the premise with useful detail.
- Do not convert seller ROI stories, customer examples, or feature claims into buyer-confirmed Impact.
- Do not treat politeness, praise, curiosity, or product enthusiasm as purchase commitment.
- Do not label a contact a champion based only on seniority or enthusiasm. Look for influence, access, internal advocacy, and concrete action.
- Do not treat a proposed or conditional follow-up as a firm next step unless it has clear ownership and timing.
- Do not treat a named competitor as actively evaluated unless the buyer confirms active consideration.
- Treat absent evidence as **not evidenced on this call**, not proof that the information is unknown across the entire deal.
- Preserve meaningful uncertainty instead of forcing a conclusion.

### SPICED coverage scoring

Score each component independently from 0-10:

| Score | Anchor | Coverage label |
|---:|---|---|
| 0 | No relevant evidence appears. | Not evidenced |
| 1-2 | A hint, trigger, or seller assumption appears, but the buyer does not meaningfully develop or validate the full component. | Minimal |
| 3-4 | A relevant fact is identified at surface level with little follow-up. | Partial |
| 5-6 | Multiple buyer-confirmed specifics are present, but important dimensions remain unclear or unvalidated. | Partial |
| 7-8 | The component is clear, buyer-validated, and supported by useful detail. | Explored |
| 9-10 | Discovery is unusually comprehensive, connected to the causal chain, and quantified or operationalized where appropriate. | Explored |

Reserve 9-10 for exceptional evidence. Do not score seller execution inside the SPICED coverage scores. Calculate the arithmetic mean of the five component scores to one decimal place and verify the calculation.

### Seller-execution assessment

Consider these behaviors separately from SPICED coverage:

- Question quality: open, diagnostic, neutral, and one question at a time.
- Active listening: mirroring, paraphrasing, labeling, and follow-up using the buyer's words.
- Discovery depth: cause, frequency, severity, consequence, and priority rather than isolated facts.
- Pain-to-impact progression.
- Critical-event discovery.
- Decision-process discovery.
- Flow and solution timing: whether discovery meaningfully shaped the presentation. When criticizing premature solutioning, cite the first clear transition from discovery into presentation and distinguish opening framing, a tailored demonstration, and unrelated feature touring when those phases differ.
- Demo relevance: especially for demo/discovery calls, distinguish necessary presentation from unhelpful feature touring.
- Prospect engagement: participation, specificity, questions, ownership, and buyer actions—not politeness alone.
- Objection and risk handling: whether the seller explored requirements and proof criteria before assuring.
- Next-step discipline: mutuality, owner, timing, objective, stakeholders, and buyer commitment.
- Talk/listen balance only when reliable source data exists. Explain any limitation in the metric.

Calibrate the assessment to the stated call type and opportunity stage. Do not expect a first discovery call to complete an entire buying process, and do not excuse missing foundational discovery merely because the call included a scheduled demo. Select the three to five execution findings that most affected coaching or deal strategy; omit secondary checklist observations unless they materially change the conclusion.

### Coaching selection

Coach the few behaviors most likely to improve the opportunity. Do not inventory every imperfection.

For missed moments:

- Select no more than three high-leverage transcript moments.
- Prefer moments where a different seller response could have improved Impact, urgency, decision clarity, or mutual commitment.
- Explain the buyer opening, the seller response, why it mattered, and one clean replacement question.
- Make a discovery replacement a single open-ended or mirroring question. For a scheduling or mutual-commitment moment, a direct singular commitment question is appropriate. Do not write stacked, multi-part interrogations.
- Make the question sound natural in the buyer's language and appropriate to that moment.
- Keep Critical Event questions neutral: explore whether a buyer-owned timeframe, trigger, or consequence exists before presupposing a deadline.

For strengths, identify no more than three observable behaviors the seller should repeat. Support each with evidence.

### Required output

Write a Markdown report using this structure.

#### 1. Coaching brief

Keep this section short enough for a seller and manager to review together in a few minutes.

- **Overall SPICED coverage:** `X.X/10`
- **Qualification verdict:** One sentence.
- **Primary coaching theme:** One behavior with the highest leverage.
- **Keep doing:** Up to two specific strengths.
- **Change next call:** Up to two specific behaviors.
- **Next-step target:** The most important buyer-owned outcome for the next conversation.

#### 2. SPICED scorecard

| Component | Score | Coverage | Buyer-confirmed evidence | Most consequential gap |
|---|---:|---|---|---|
| Situation | 0-10 | Explored/Partial/Minimal/Not evidenced | Timestamped evidence | Gap |
| Pain | 0-10 | Explored/Partial/Minimal/Not evidenced | Timestamped evidence | Gap |
| Impact | 0-10 | Explored/Partial/Minimal/Not evidenced | Timestamped evidence | Gap |
| Critical Event | 0-10 | Explored/Partial/Minimal/Not evidenced | Timestamped evidence | Gap |
| Decision | 0-10 | Explored/Partial/Minimal/Not evidenced | Timestamped evidence | Gap |

After the table, explain any scoring judgment that could reasonably be interpreted more than one way.

#### 3. Opportunity diagnosis

Summarize only what is useful for deal strategy:

- Confirmed business problem
- Confirmed consequences and unquantified Impact
- Trigger versus true Critical Event
- Stakeholders and demonstrated roles
- Decision criteria and process
- Alternatives/status quo
- Technical, adoption, or proof risks
- Strength of the current next step

Clearly distinguish explicit evidence, inference, metadata, and information not evidenced on this call.

#### 4. Seller execution

Give three to five concise findings drawn from the execution dimensions that most affected the conversation, coaching, or deal strategy. Explain how seller behavior affected the conversation rather than merely assigning adjectives. Do not mechanically report every execution dimension.

#### 5. Replayable coaching moments

For each of up to three moments, provide:

1. **Timestamp and buyer opening**
2. **Seller response**
3. **Why this mattered**
4. **One replacement question**
5. **SPICED dimension strengthened**

#### 6. Next-call plan

Provide three to five prioritized questions or moves that naturally continue this buyer's story. Order them to:

1. Clarify the most important current-state or pain gap.
2. Establish consequence or magnitude.
3. Neutrally test whether urgency or a Critical Event exists; do not assume a deadline.
4. Map decision participants and process.
5. Secure a mutual next step with an owner, timing, and purpose.

Do not mechanically repeat topics the buyer already answered. Keep each question singular and conversational.

#### 7. Manager coaching focus

Close with:

- **Behavior to practice:** One observable behavior.
- **Suggested drill:** A short role-play or review exercise.
- **Success signal on the next call:** What the manager should listen for.

### Style requirements

- Be direct, fair, and constructive.
- Prefer concise paraphrases to long transcript quotes.
- Do not overstate certainty or deal health.
- Do not confuse comprehensive reporting with useful coaching.
- Keep the main report focused enough to use in a live coaching session; place secondary detail after the coaching brief.
- If an output path is provided, save the report there as Markdown.
