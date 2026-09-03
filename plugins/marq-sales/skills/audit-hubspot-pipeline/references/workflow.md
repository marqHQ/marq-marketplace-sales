# Pipeline audit workflow

## 1. Resolve scope and schema

Call HubSpot user details before every HubSpot operation. Use the authenticated owner unless the user explicitly supplies another owner. Confirm the current portal exposes the required read surfaces.

Discover these deal concepts by property search rather than silently hardcoding them: pipeline, stage, owner, deal name, created date, close date, `next_step_date`, `hs_next_step`, last activity, last contacted, next activity, and next meeting. Current known names may be used only after discovery confirms them.

Limit v1 to pipeline `default`. Resolve the pipeline's current stage enum, then identify terminal stages by both semantics and current configuration. Exclude won, lost, clawback, disqualified, merged, and any other terminal stage.

## 2. Fetch the complete population

Search deals using one AND filter group for owner, pipeline, and nonterminal eligibility when supported. Request a stable sort and follow offsets until no records remain. Deduplicate by deal ID.

Because terminal stages can have portal-specific IDs, compute:

- `raw_owner_pipeline_total`: all owner deals in pipeline `default`.
- `terminal_ids`: unique IDs classified terminal.
- `eligible_ids`: raw IDs minus terminal IDs.

Require `len(eligible_ids)` to equal the number sent to scoring. Run `scripts/audit_utils.py reconcile --expected N --ids ...` when useful. If counts do not reconcile, report the audit incomplete and do not publish percentages.

For every eligible deal, read associations to NOTE, TASK, CALL, EMAIL, MEETING_EVENT, CONTACT, and COMPANY. Page associated records to completion. Record tool or permission gaps per deal rather than silently dropping a source.

## 3. Enrich every deal

### Calendar

Search from 30 days before through 90 days after the audit date. Start with the associated company name, then use contact names/emails and a meaningful deal-name token. Read full event details for candidates.

Accept a Calendar match only when at least two identity signals agree, such as company plus associated contact, contact email plus deal token, or exact account plus owner participation. A meeting URL alone is insufficient. Reject cross-opportunity ambiguity.

### Gong

Search from the later of 180 days before the audit date or the deal creation date. Prefer associated company and external participant email/name. Fetch transcripts only for accepted candidates, continuing through all chunks required to inspect commitments.

Accept a Gong match only when the account and at least one associated participant or opportunity-specific signal agree. Do not borrow evidence from another opportunity at the same company.

### Commitment resolution

Create an evidence ledger containing source, source ID/link, event or call date, explicit commitment date, action summary, match signals, and confidence. Only absolute dates and scheduled timestamps qualify as a commitment date.

Sort credible commitments by source occurrence time, not by the promised follow-up date. Prefer the newest explicit commitment. Mark older disagreement as superseded. Use `conflicting` only when current credible evidence cannot be ordered or resolved.

## 4. Normalize and score

Normalize each deal to `references/scoring.md`. Invoke:

```bash
python3 scripts/score_deal.py normalized-deal.json
```

Do not manually adjust the result. Add non-scoring findings such as an unknown stage, malformed deal name, or connector gap separately.

## 5. Report

Start with eligible total, scored total, average score, color counts and percentages, and stage distribution. If the recurring task contains a prior complete audit, show count and average-score deltas plus deals whose colors changed.

Show red deals first and yellow deals second. Include deal link, stage, score/components, current next step/date, activity age, close-date issue, task state, evidence ledger summary, override/warning reasons, and proposed action. Then list every green deal compactly with link, stage, next step/date, score, and healthy-status reason.

State one of these evidence conclusions exactly:

- `Corroborated by <source>.`
- `Superseded by a newer explicit commitment from <source>.`
- `Conflicting evidence requires rep input.`
- `No corroborating evidence found.`
- `Source unavailable: <source>.`

## 6. Prepare append-only remediation

Construct the proposed history line with the audit date formatted `MM / DD / YYYY`. Preserve the entire current `hs_next_step` value and append with one newline. Compare whitespace-collapsed, case-folded lines; suppress an identical existing line.

When an explicit new commitment exists, propose both the current actionable `next_step_date` and a history line naming the action/date and source. When no supported commitment exists, leave the date unchanged and propose a `NEXT STEP NEEDED` history line only if the exception is new or materially changed.

For tasks:

- Keep a matching future task or meeting unchanged.
- Propose rescheduling a matching overdue task when the new date is explicit.
- Propose a new owner-assigned task only when an explicit action/date exists and no matching future activity exists.
- Never invent a task due date.

Discover and use the live task properties corresponding to `hs_task_subject`, `hs_timestamp`, `hs_task_status`, `hs_task_body`, and `hubspot_owner_id`. Create proposed tasks as `NOT_STARTED`, assign them to the deal owner, and associate them to the exact deal ID. Include the evidence source in the task body. Do not mark priority unless the rep asks.

Scheduled runs must only report proposals. Interactive writes require the HubSpot approval table in `SKILL.md`. Batch at most ten object changes, then independently re-read deal text/date and task properties/association.
