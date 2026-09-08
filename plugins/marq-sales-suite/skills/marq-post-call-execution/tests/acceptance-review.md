# V1 Acceptance Review

Date: 2026-09-04

This is a design-time walkthrough of seven synthetic cases. It verifies that the written workflow covers the requested call mix and that each case has explicit capture and anti-fabrication assertions. It is not a substitute for an independent end-to-end model evaluation on real Marq calls.

| Case | Scenario | Expected qualification behavior | Expected CRM behavior | Expected email behavior | Design review |
|---|---|---|---|---|---|
| D1 | Strong discovery | Capture current state, quantified time impact, decision timing, and both commitments; keep economic buyer and budget unknown. | Live-discovered pain, value, authority, next-step/date, and narrative fields may be proposed; no unsupported amount or forecast change. | Confirm the demo and two commitments without claiming budget approval. | Pass |
| D2 | Strong discovery with relative date | Preserve qualitative impact, label quantified impact unknown, and normalize “next Tuesday” to 2026-09-08 while retaining the original phrase. | Propose next step/date and supported pain categories; no invented revenue impact. | Confirm the compliance meeting only as agreed; no revenue claim. | Pass |
| D3 | Strong discovery with CRM conflict | Mark Critical Event/Decision as contradicted where the call conflicts with the CRM close/forecast posture. | Surface the recorded close-date and Commit conflict; do not silently preserve or overwrite either executive field. | Use the customer’s current timing and avoid exposing internal forecast conflict. | Pass |
| W1 | Seller-led weak discovery | Mark Impact and Decision missing/partial; seller claims remain seller interpretations; date remains unknown. | No factual pain, authority, close, stage, amount, or forecast proposal. A cautious notes proposal may record the gap. | Ask a focused follow-up question; do not imply a meeting was agreed. | Pass |
| W2 | Sparse seller notes only | State that customer evidence is unavailable and all apparent facts originate in seller notes. | No competitor, pain, or next-step-date proposal from the notes alone. | Draft only a tentative follow-up; do not call the demo committed. | Pass |
| M1 | Demo | Record validated brand fit, unresolved SSO/accessibility review, and both commitments; do not declare technical win. | Propose next step/date and notes only; no stage advance. | Recap validated need and technical review path without saying SSO is approved. | Pass |
| M2 | Later-stage commercial | Capture legal/security dependency, finance approval gap, discussed price, and dated order-form commitment. | Do not update `amount`, stage, forecast, or close date merely because price is “within range.” | Mention the $42,000 price only if commercial review permits; clearly state finance approval is pending and confirm the September 7 deliverable. | Pass |

## Result

The fixture checker passes: three strong discovery cases, two weak/incomplete discovery cases, and two demo/later-stage cases. Each includes positive capture assertions and prohibited claims. Production acceptance remains open until the requested real transcript/email/deal bundles are supplied and evaluated by reviewers outside the authoring pass.

## HubSpot record-resolution cases

| Case | Input | Expected behavior | Design review |
|---|---|---|---|
| R1 | Exact deal name | Resolve the unique deal, include its link, and continue without asking for a link. | Pass |
| R2 | Account with one associated deal | Resolve the company, find its associated deal, include the deal link, and continue. | Pass |
| R3 | Account with multiple associated deals | Show linked deal choices with identifying context and URLs; ask the rep to choose. | Pass |
| R4 | Account with no associated deal | Return the company link, state that no deal exists, and continue without deal-level context. | Pass |
