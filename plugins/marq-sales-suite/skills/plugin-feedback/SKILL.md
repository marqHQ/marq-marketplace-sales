---
name: plugin-feedback
description: Collect actionable feedback about another Marq Sales skill, preserve relevant conversation context, and—with the user's approval—submit a sanitized feedback record as a branch and pull request to marqHQ/marq-marketplace-sales and request review from the plugin owner. Use when a sales rep wants to report a problem, confusing step, missing behavior, bad output, or improvement idea for a skill in this plugin.
---

# Submit plugin feedback about a Marq Sales skill

Turn the rep's experience into a concise, reviewable feedback record. Submit the feedback itself; do not edit the affected skill, propose implementation code, merge the pull request, or represent the feedback as an approved product decision.

The target repository, `marqHQ/marq-marketplace-sales`, is public. Never put customer names, contact details, deal data, call transcripts, private URLs, credentials, tokens, or other confidential information in the branch, commit, or pull request. Summarize or redact private context while preserving what the skill owner needs to understand the problem.

Read [references/submission-template.md](references/submission-template.md) before preparing the submission.

## Required capabilities

Use an authenticated GitHub connector that can create branches, files, commits, pull requests, and review requests. In a local coding environment, authenticated `git` and GitHub CLI commands are an acceptable equivalent.

The feedback owner is Nick Hatch, GitHub user `@Nhatch11`. Confirm that this account still has access to the repository before preparing the submission. If GitHub write or review-request capability is unavailable, explain the missing prerequisite and stop before creating the branch. Do not substitute an untracked chat summary or claim the workflow completed.

## Intake

1. Inspect the current conversation before asking questions. Identify the skill most recently used and the relevant step, inputs, outputs, errors, and corrections already supplied by the rep.
2. Propose the affected skill when the conversation supports one exact match. Ask the rep to confirm it; otherwise ask which installed Marq Sales skill the feedback concerns.
3. Gather only missing information needed to answer:
   - What happened?
   - What should have happened instead?
   - Why does the difference matter to a rep, customer, or workflow?
   - What steps, inputs, or conditions reproduce it?
   - Is there a suggested direction, if the rep has one?
4. Ask one focused question at a time. Do not force the rep to repeat facts that are already clear from the conversation. Suggested direction, evidence, and reproducibility are useful but not required when the issue is already actionable.
5. Classify the feedback as one of: `incorrect-behavior`, `missing-step`, `unclear-instruction`, `tool-failure`, `output-quality`, `workflow-friction`, `permissions-or-security`, or `enhancement`.
6. Preserve uncertainty. Clearly distinguish what the rep observed from the agent's inference. Do not invent a root cause.
7. Detect sensitive content before submission. Replace it with neutral descriptions such as `[customer]`, `[deal]`, or `[private link omitted]`. Tell the rep what was redacted.

## Prepare the submission

1. Discover the repository's current default branch and head SHA through GitHub. Do not assume a stale base.
2. Confirm that the affected skill exists under `plugins/marq-sales-suite/skills/<skill-name>/`. Stop if the name is ambiguous or the skill is not in this plugin.
3. Create a UTC timestamp and a short lowercase slug from the feedback summary.
4. Prepare these exact artifacts without writing them yet:
   - Branch: `feedback/<skill-name>/<YYYYMMDD>-<slug>`.
   - File: `feedback/<YYYY-MM-DD>-<skill-name>-<slug>.md`.
   - If either name already exists, add the same short unique suffix to both the branch and file name.
   - Commit: `feedback(<skill-name>): <concise summary>`.
   - Pull-request title: the same text as the commit.
   - Pull-request body: a short purpose statement, affected skill path, privacy confirmation, and `Submitted via $plugin-feedback`.
   - Reviewer: GitHub user `@Nhatch11`.
5. Render the feedback file using the reference template. Include only sanitized evidence and context.

## Approval boundary

Show one consolidated preview containing:

| Action | Destination | Exact proposed content |
|---|---|---|
| Create branch and commit | Repository, base branch, branch, file path | Commit message and complete feedback file |
| Open pull request | Repository and base branch | PR title and body |
| Request review | GitHub user `@Nhatch11` | Pull-request review request |

State that approval will create externally visible GitHub artifacts and notify `@Nhatch11` through a pull-request review request. Require the rep to approve this exact package before any write. Approval of an earlier draft or materially different package is insufficient. If anything changes after approval, show the revised package and ask again.

## Submit and verify

After approval:

1. Create the branch from the discovered default-branch head.
2. Create only the proposed feedback file and commit. Do not modify the affected skill or unrelated repository files.
3. Open the pull request against the discovered default branch. Do not enable auto-merge or merge it.
4. Request review from `@Nhatch11`. Use the pull-request creation call's reviewer field when supported; otherwise create the review request immediately after the pull request.
5. Re-read the pull request through GitHub and verify its repository, base, head branch, title, body, open state, changed-file count, exact changed path, public URL, and that `Nhatch11` appears in the requested reviewers. A UI success message is not verification.

Retry a failed GitHub write at most once when the retry is identical and remains within the approved package. Otherwise stop and report the exact partial state. Never create a second pull request to hide or recover from an uncertain first attempt.

## Completion report

Return:

- A link to the verified pull request
- The affected skill and feedback category
- Confirmation that the PR changes only the feedback file
- Confirmation that GitHub requested review from Nick Hatch (`@Nhatch11`), or the exact notification failure
- Any remaining manual action
