# Deterministic scoring contract

## Input

Pass one JSON object to `scripts/score_deal.py`:

```json
{
  "audit_date": "2026-08-13",
  "stage_band": "early",
  "next_step_date": "2026-08-20",
  "has_actionable_next_step": true,
  "weak_next_step": false,
  "last_activity_at": "2026-08-10T15:00:00Z",
  "close_date": "2026-09-30",
  "evidence_status": "aligned",
  "task_status": "future_matching"
}
```

Required enums:

- `stage_band`: `early`, `middle`, or `late`.
- `evidence_status`: `aligned`, `unverified`, `no_evidence`, or `conflicting`.
- `task_status`: `future_matching`, `none`, `mixed`, or `overdue_only`.

Dates must be ISO dates or datetimes. Normalize semantic judgments before calling the script:

- `has_actionable_next_step`: true only when the text names a concrete action and responsible party or customer commitment.
- `weak_next_step`: true for vague, stale, purely historical, or warning-only text.
- `aligned`: the newest explicit commitment agrees with the CRM date/action.
- `unverified`: evidence exists but does not clearly verify the CRM commitment.
- `no_evidence`: bounded source searches returned no corroborating evidence or a connector was unavailable.
- `conflicting`: two credible sources disagree and the newest current commitment cannot be resolved.
- `future_matching`: an open task or future meeting covers the current action.
- `overdue_only`: the only activity representing the action is past due or already occurred.
- `mixed`: both overdue and future activity exist, or coverage is incomplete.

## Stage bands

Resolve live stage values first. For the default Sales Pipeline, classify semantically:

- Early, 14-day activity threshold: opportunity identified, demo/discovery scheduled, SQO.
- Middle, 10-day threshold: solution overview, opportunity strategy, group consensus.
- Late, 7-day threshold: solution confirmation, procurement, closing, pending approval, awaiting payment.

Unknown nonterminal stages default to early and add a reporting warning outside the scorer.

## Points and colors

- Next-step quality, 40: 20 for a non-expired date and 20 for actionable text.
- Activity recency, 30: 30 within the stage threshold, 15 within twice the threshold, otherwise 0.
- Evidence alignment, 20: 20 aligned, 10 unverified or no evidence, 0 conflicting.
- Task/meeting hygiene, 10: 10 future matching, 5 none or mixed, 0 overdue only.

Green is 80–100 with no warnings or overrides. Yellow is 50–79 or any non-red warning. Red is below 50 or any red override.

Warnings are due within three days, activity beyond the first stage threshold, weak next-step text, unverified evidence, no corroborating evidence, no matching task/meeting, or mixed task coverage.

Red overrides are missing or expired next-step date, missing actionable next-step text, activity beyond twice the stage threshold, past close date on an open deal, overdue-only action coverage, or conflicting evidence.

The scorer returns `score`, `color`, `components`, `warnings`, `overrides`, `threshold_days`, and calculated day intervals.
