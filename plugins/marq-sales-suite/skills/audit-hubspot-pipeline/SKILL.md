---
name: audit-hubspot-pipeline
description: Audit a sales rep's complete open HubSpot Sales Pipeline, corroborate next steps against HubSpot activities, Google Calendar, and Gong, score every deal green/yellow/red, surface stale or inaccurate pipeline records, and prepare append-only next-step and task changes for approval. Use for weekly pipeline hygiene audits, stale-deal reviews, next-step cleanup, past-due follow-up detection, or evidence-backed updates to a specific HubSpot deal.
---

# Audit HubSpot Pipeline

Audit every eligible deal before proposing repairs. Treat scheduled runs as read-only and make CRM changes only in an interactive turn after explicit approval.

## Required references

Read [references/workflow.md](references/workflow.md) before every audit. It defines discovery, enrichment, matching, reporting, and write safety.

Read [references/scoring.md](references/scoring.md) before normalizing deals or interpreting scores. Use `scripts/score_deal.py`; do not reproduce scoring heuristically.

Read [references/deployment.md](references/deployment.md) only when installing, sharing, testing, or scheduling this skill.

## Inputs and defaults

- Default to the authenticated HubSpot user's owner ID, pipeline `default`, current date, and `America/Denver`.
- Accept an explicit owner, one HubSpot deal URL, an audit date, or dry-run mode.
- Treat a scheduled or automation run as dry-run regardless of wording. Never create or update CRM records unattended.
- For a full audit, fetch and score the entire eligible population. Never substitute a sample or top-N list.

## Audit workflow

1. Call HubSpot user details first. Confirm DEAL, NOTE, TASK, CALL, EMAIL, and MEETING_EVENT read access. Confirm DEAL and TASK write access only when interactive remediation is requested.
2. Discover live property names and enum values. Do not assume portal-specific fields, stages, or owners even when the defaults in the workflow reference still exist.
3. Retrieve every current-owner deal in Sales Pipeline `default`, page to completion, exclude terminal stages, and reconcile fetched eligible IDs against the reported total.
4. Read associated notes, tasks, calls, emails, meetings, contacts, and company context for every eligible deal.
5. Enrich every deal with bounded Calendar and Gong searches using the rules in `references/workflow.md`. Record unavailable sources and ambiguous matches explicitly.
6. Normalize one JSON object per deal to the contract in `references/scoring.md`. Run `scripts/score_deal.py` for each object and preserve its output unchanged.
7. Produce the full scorecard: summary and trend, red deals, yellow deals, then a compact row for every green deal. Include a clickable HubSpot URL for every listed deal.
8. In scheduled runs, stop after the report and exact proposed changes. In interactive runs, show the required approval table and wait.
9. Apply only approved fields and tasks, in batches of at most ten objects. Re-read every affected record and report mismatches.

## Evidence rules

- Use only an absolute date from a source or an actual scheduled timestamp. Never turn “next week,” “soon,” or similar relative language into a CRM date.
- Prefer the newest explicit commitment. Show any older contradictory commitment as superseded evidence.
- Do not treat missing Calendar or Gong evidence as contradiction. Label it `no corroborating evidence found`.
- Reject an enrichment match when company, contact, participant, or opportunity identity remains ambiguous.
- Preserve user-entered context. Evidence may support a proposed append or date change but never authorizes it.

## Remediation rules

- Preserve all existing `hs_next_step` text. Add a new line only for a material update, newly detected exception, or changed evidence.
- Suppress a proposed line when its normalized text already exists in `hs_next_step`.
- Format appended lines as `MM / DD / YYYY - action/date - source or reason` or `MM / DD / YYYY - NEXT STEP NEEDED - reason`.
- Keep `next_step_date` as the single current actionable date. Do not invent a date when no explicit source supports one.
- Reuse or reschedule a matching task before proposing a new one. Do not duplicate a future task or meeting.
- Surface close-date and stage anomalies, but do not edit close date or stage in v1.

Before any write, show:

| Object Type | ID | Property | Current Value | New Value |
|---|---:|---|---|---|

Ask for explicit approval. On the first confirmation, add: `Want to skip confirmations for this chat? Just ask.` Treat confirmation waivers as interactive-session-only; they never apply to scheduled runs.

## Completion criteria

Do not call an audit complete unless:

- scored deal count equals the full eligible population;
- every deal has a color, score, component scores, evidence status, and reason;
- every recommendation names evidence or requests rep input;
- the report distinguishes missing corroboration from contradiction;
- no scheduled-run write occurred; and
- every approved write was independently re-read and verified.
