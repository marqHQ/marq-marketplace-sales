---
name: plugin-feedback
description: Collect actionable feedback about a Marq Sales skill, redact private context, and submit the feedback record to the contribution pipeline for them. Use when a sales rep wants to report a problem, confusing step, missing behavior, bad output, or improvement idea for a skill in this plugin. No GitHub access is needed.
---

# Submit plugin feedback about a Marq Sales skill

Turn the rep's experience into a concise feedback record you submit for them. Submit the feedback itself; do not edit the affected skill, propose implementation code, or present the feedback as an approved product decision. After they submit, the pipeline logs it, opens a Slack DM thread with the rep, screens it for private data, and files it as a public GitHub issue. An automated review then drafts the change to the skill as a pull request, and the plugin owner, Nick Hatch, approves, requests changes, or rejects it in Slack. Nothing merges without him.

You submit by posting to the pipeline endpoint from the terminal. The rep does not open a browser or fill in a form. See [references/submitting.md](references/submitting.md) for the endpoint, the payload, the exact command, and the stopping conditions.

The destination repository is public. Never put customer names, contact details, deal data, call transcripts, private URLs, credentials, or tokens in the record. Summarize or redact private context while preserving what the skill owner needs to understand the problem.

Read [references/submission-template.md](references/submission-template.md) before rendering the record.

## Intake

1. Inspect the current conversation before asking questions. Identify the skill most recently used and the relevant step, inputs, outputs, errors, and corrections the rep already supplied.
2. Identify the affected skill by its folder name, for example `spiced-call-coach`. When the conversation supports one exact match, use it without asking; it appears in the confirmation summary. Ask which installed Marq Sales skill the feedback concerns only when there is no single match.
3. Gather only the missing information needed to answer:
   - What happened?
   - What should have happened instead?
   - Why does the difference matter to a rep, customer, or workflow?
   - What steps, inputs, or conditions reproduce it?
   - Is there a suggested direction, if the rep has one?
4. Take the rep's name and Marq email from the conversation or the signed-in account when either is available. Ask for them only when they are not. Do not confirm them separately: they appear in the confirmation summary, because the email is the only channel the pipeline has back to the rep.
5. Every question costs the rep a turn. Ask every question you still need, including the skill and the rep's name or email, together in one message, never one per turn. Do not force the rep to repeat facts that are already clear. Suggested direction, evidence, and reproducibility are useful but not required when the issue is already actionable, so do not ask for them then.
6. Classify the feedback as one of: `incorrect-behavior`, `missing-step`, `unclear-instruction`, `tool-failure`, `output-quality`, `workflow-friction`, `permissions-or-security`, or `enhancement`.
7. Preserve uncertainty. Distinguish what the rep observed from what you infer. Do not invent a root cause.
8. Redact sensitive content before rendering. Replace it with neutral descriptions such as `[customer]`, `[deal]`, `[amount]`, or `[private link omitted]`. Tell the rep what was redacted. The pipeline runs its own privacy screen and holds anything it flags for the owner, so do not rely on it to catch what you can see.

## Render the record

Fill the template from the reference completely, omitting optional sections that would be empty. Write a one-line summary that fits in a Slack message and starts with the skill name's effect, for example `SPICED table missing on calls over 30 minutes`.

## Confirm once, then submit

The pipeline files feedback as a public GitHub issue, so a named human must attest that the record is clean before it leaves the machine. That attestation is the rep saying yes to you, and you may not supply it on their behalf. It is the only confirmation this skill asks for, so put everything the rep needs to check into that one message.

1. Show the rep the complete record, preceded by the affected skill, the one-line summary, and their name and email in bold so a wrong address is caught here. Tell them plainly what you redacted.
2. In the same message, ask them to reply yes to confirm two things: that the record is what they want submitted, and that it contains no customer names, deal data, call transcripts, private links, or credentials.
3. Only after they confirm both, post the submission as described in [references/submitting.md](references/submitting.md), with `submission_type` set to `Feedback about an existing skill` and `skill` set to the skill's folder name.
4. If their reply corrects only the name, email, or summary, apply the correction and submit without asking again; those are not part of the record. Never alter the record after they confirm it. If the record or the affected skill must change, show the new version and ask again.
5. Report the HTTP status, then tell them to watch for the pipeline's Slack DM, which carries the tracking link and is the real receipt.

If a stopping condition in the submitting reference applies, give them the form link and the field values instead, and say why you could not post it for them.

## What happens next

Tell the rep where to watch: their Slack DM thread from the pipeline, which carries the GitHub issue link and every later update. Within about half an hour the automated review either opens a pull request for Nick's decision or explains why it made no change. The rep hears Nick's decision, or any question about the feedback, in the same thread.

## Completion report

Return the affected skill, the category, what was redacted, whether the rep confirmed the privacy attestation, the HTTP status of the submission, and whether it was submitted or is waiting on a stopping condition.
