---
name: plugin-feedback
description: Collect actionable feedback about a Marq Sales skill, redact private context, and submit the feedback record to the contribution pipeline for them. Use when a sales rep wants to report a problem, confusing step, missing behavior, bad output, or improvement idea for a skill in this plugin. No GitHub access is needed.
---

# Submit plugin feedback about a Marq Sales skill

Turn the rep's experience into a concise feedback record you submit for them. Submit the feedback itself; do not edit the affected skill, propose implementation code, or present the feedback as an approved product decision. After they submit, the pipeline logs it, opens a Slack thread in the intake channel, screens it for private data, and files it as a public GitHub issue that the plugin owner, Nick Hatch, triages.

You submit by posting to the pipeline endpoint from the terminal. The rep does not open a browser or fill in a form. See [references/submitting.md](references/submitting.md) for the endpoint, the payload, the exact command, and the stopping conditions.

The destination repository is public. Never put customer names, contact details, deal data, call transcripts, private URLs, credentials, or tokens in the record. Summarize or redact private context while preserving what the skill owner needs to understand the problem.

Read [references/submission-template.md](references/submission-template.md) before rendering the record.

## Intake

1. Inspect the current conversation before asking questions. Identify the skill most recently used and the relevant step, inputs, outputs, errors, and corrections the rep already supplied.
2. Propose the affected skill when the conversation supports one exact match and ask the rep to confirm it; otherwise ask which installed Marq Sales skill the feedback concerns. Use the skill's folder name, for example `spiced-call-coach`.
3. Gather only the missing information needed to answer:
   - What happened?
   - What should have happened instead?
   - Why does the difference matter to a rep, customer, or workflow?
   - What steps, inputs, or conditions reproduce it?
   - Is there a suggested direction, if the rep has one?
4. Ask one focused question at a time. Do not force the rep to repeat facts that are already clear. Suggested direction, evidence, and reproducibility are useful but not required when the issue is already actionable.
5. Classify the feedback as one of: `incorrect-behavior`, `missing-step`, `unclear-instruction`, `tool-failure`, `output-quality`, `workflow-friction`, `permissions-or-security`, or `enhancement`.
6. Preserve uncertainty. Distinguish what the rep observed from what you infer. Do not invent a root cause.
7. Redact sensitive content before rendering. Replace it with neutral descriptions such as `[customer]`, `[deal]`, `[amount]`, or `[private link omitted]`. Tell the rep what was redacted. The pipeline runs its own privacy screen and holds anything it flags for the owner, so do not rely on it to catch what you can see.

## Render the record

Fill the template from the reference completely, omitting optional sections that would be empty. Write a one-line summary that fits in a Slack message and starts with the skill name's effect, for example `SPICED table missing on calls over 30 minutes`.

## Confirm, then submit

The pipeline files feedback as a public GitHub issue, so a named human must attest that the record is clean before it leaves the machine. That attestation used to be a checkbox on a form. Now it is the rep saying yes to you, and you may not supply it on their behalf.

1. Show the rep the complete record and tell them plainly what you redacted.
2. Ask them to confirm two things in one answer: that the record is what they want submitted, and that it contains no customer names, deal data, call transcripts, private links, or credentials.
3. Only after they confirm both, post the submission as described in [references/submitting.md](references/submitting.md), with `submission_type` set to `Feedback about an existing skill` and `skill` set to the skill's folder name.
4. Never alter the record after they confirm it. If anything needs to change, show the new record and ask again.
5. Report the HTTP status, then tell them to watch for the pipeline's Slack DM, which carries the tracking link and is the real receipt.

If a stopping condition in the submitting reference applies, give them the form link and the field values instead, and say why you could not post it for them.

## What happens next

Tell the rep where to watch: the intake Slack thread, the GitHub issue link posted there, and the owner's triage.

## Completion report

Return the affected skill, the category, what was redacted, whether the rep confirmed the privacy attestation, the HTTP status of the submission, and whether it was submitted or is waiting on a stopping condition.
