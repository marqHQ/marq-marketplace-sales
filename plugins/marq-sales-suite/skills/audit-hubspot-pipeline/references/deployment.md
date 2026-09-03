# Install, test, and schedule

## Install a shared copy

1. Unzip or copy the `audit-hubspot-pipeline` folder into the receiving user's Codex skills directory.
2. Confirm the final folder is named exactly `audit-hubspot-pipeline` and contains `SKILL.md` and `agents/openai.yaml` at its root.
3. Connect and authorize HubSpot and Google Calendar. Confirm the environment also exposes Gong call search and transcript tools.
4. Test the scorer: `python3 scripts/run_tests.py`.
5. Invoke `$audit-hubspot-pipeline` manually in a normal task and run a dry audit before scheduling.
6. Confirm the eligible count against HubSpot and review every red result plus samples of yellow and green.

## Recurring-task prompt

Use this exact prompt in the same recurring Codex task so prior complete reports remain available for week-over-week comparison:

```text
Use $audit-hubspot-pipeline to run my complete weekly HubSpot Sales Pipeline hygiene audit. Scope the audit to the authenticated rep's open deals in the primary Sales Pipeline. Use today's date and America/Denver. Enrich every eligible deal with HubSpot activities, Google Calendar, and Gong; reconcile the complete eligible count; score and classify every deal; compare the result with the most recent complete audit in this task; and report red, yellow, then green deals. This is an unattended scheduled run: remain read-only, make no HubSpot or Calendar changes, and prepare exact append-only next-step/date/task proposals for later approval. Notify me even when all deals are green.
```

Schedule it weekly on Monday at 7:00 AM in `America/Denver`, returning to the same task. Notify on every run.

Scheduled tasks can use skills and connected plugins, but unattended runs cannot supply the interactive HubSpot confirmation required by this skill. Keep the scheduled phase read-only and perform approved remediation in a follow-up interactive turn.

## Pilot acceptance

Run manually before enabling the schedule. Review the first three weekly reports and adjust only the skill package—not individual recurring prompts—when policy needs to change. Re-run validation and tests after every package revision.
