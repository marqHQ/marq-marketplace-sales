# Founding Source Findings and Rollout Dependencies

## Reviewed sources

Repository: `ChandlerMARQ/Deal-Command-Center`, default branch `main`, tree `45a7599e48f012667dab791d6d0d75108535fac2`.

- `Marq Sales Assistant - Discovery & Follow-Up System.md` supplies the five-step discovery model, current-state/root-cause/impact/buying-process questions, and a daily deal-summary shape.
- `Follow-Up Email Generator.md` supplies discovery, demo, stakeholder, and stalled-call templates plus Justin-derived writing guidance.
- `Marq Prospect Notes & Follow-Up System.md` supplies deal, contact, pain, impact, competition, last-interaction, next-step, and momentum concepts. Its named deal example is a template example, not verified production evidence.
- `justin-voice-guide (1).md` is explicitly a LinkedIn voice guide. It supports Justin-specific tendencies but is not evidence of a shared sales-email voice.
- `Updated Project Users IDs.txt` maps Justin Warner `179425909`, Brad Hardle `91714475`, Cody Cluff `96818330`, and Seth Hurtado `80743422`.
- Local `spiced-call-coach/SKILL.md` supplies the compatible SPICED vocabulary and keeps coaching in a separate independent draft-and-audit workflow.

## What the source set does not contain

The repository tree reviewed on 2026-09-04 contains no real transcript → rep conclusion → HubSpot record → sent-email bundles. It also contains no authoritative HubSpot property catalog. An initial schema review informed the concept map, but production execution must discover current property names, types, stages, and enum values live rather than relying on that snapshot.

## Launch dependencies

Collect and approve, ideally anonymized:

- three strong discovery calls;
- two weak or incomplete discovery calls;
- two demos or later-stage calls;
- the actual sent follow-up for each call;
- the associated deal snapshot before and after the call, when available;
- two or three strong sent emails from each participating rep.

For each bundle, retain the call date/type, transcript, seller notes or conclusion, CRM changes, sent email, and reviewer judgment about what was correct or missing. Do not use these examples as facts for another customer.

RevOps must also decide whether to create dedicated properties for Situation, detailed Impact, Critical Event, Decision Process, Decision Criteria, Champion, and Economic Buyer. Until then, V1 keeps those as evidence-tagged analysis and uses a live-discovered appropriate narrative or authority field only when the mapping is unambiguous.

The connected HubSpot portal reported onboarding incomplete on 2026-09-04. That does not prevent read-only schema discovery, but live execution should verify connector availability and permissions before relying on it.
