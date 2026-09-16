---
name: plugin-feedback
description: Collect actionable feedback about a Marq Sales skill, redact private context, and hand the rep a ready-to-paste feedback record plus the intake form link. Use when a sales rep wants to report a problem, confusing step, missing behavior, bad output, or improvement idea for a skill in this plugin. No GitHub access is needed.
---

# Submit plugin feedback about a Marq Sales skill

Turn the rep's experience into a concise feedback record they paste into the contribution form. Submit the feedback itself; do not edit the affected skill, propose implementation code, or present the feedback as an approved product decision. After they submit, the pipeline logs it, opens a Slack thread in the intake channel, screens it for private data, and files it as a public GitHub issue that the plugin owner, Nick Hatch, triages.

Contribution form: https://marqapp.app.n8n.cloud/form/sales-plugin-contribute

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

## Hand off

Show the rep, in this order:

1. The complete record in one copyable block.
2. The form link and the values to enter: Submission type `Feedback about an existing skill`, their name and Marq email, Skill set to the skill folder name, Summary as the one-line summary, Submission as the record, and the privacy checkbox.
3. What happens next: the intake Slack thread, the GitHub issue link posted there, and the owner's triage.

Submit on the rep's behalf only when a browser tool is available, the rep asks you to, and they have confirmed the exact record. Never alter the record after confirmation.

## Completion report

Return the affected skill, the category, what was redacted, the form link, and whether the rep submitted it or still needs to.
