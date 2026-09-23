# Contributing skills and feedback

Sales reps contribute without touching GitHub. The pipeline has three stages, each owned by a different system so no single credential can do everything.

## 1. Submit

- **Feedback about an existing skill:** run `plugin-feedback` in ChatGPT or Codex. It interviews you, redacts customer data, shows you the record, and submits it once you confirm it.
- **A new skill:** run `upload-new-skill`. It normalizes your draft into a single text bundle, shows it to you, and submits it once you confirm it. Skills are text, so nothing is zipped or uploaded.

Both reach the same pipeline. The skills post your submission for you, so you never open a browser; if you have no terminal, the hosted form at <https://marqapp.app.n8n.cloud/form/sales-plugin-contribute> does the same thing by hand. One n8n workflow logs the submission to the ledger, DMs you in Slack, screens the text for private data, and files a GitHub issue on your behalf. You never need a GitHub account, and every later update arrives as a reply in that same Slack DM thread.

## 2. Review

- **Feedback** issues get the `feedback` label, which starts [`review-feedback.yml`](.github/workflows/review-feedback.yml):
  1. A shell step resolves the skill from the issue's ``## Feedback on `<skill>` `` heading and confirms it exists. Deterministic, no model involved.
  2. Claude, running the [`apply-feedback`](.claude/skills/apply-feedback/SKILL.md) skill, drafts the smallest change that addresses the feedback, or explains why it made none (`needs-info`, `no-change`, `reject`). It has no git or GitHub tools.
  3. A shell step voids the run if the change touches anything outside that skill, the README, or the two plugin manifests.
  4. `verify_repo.py` reruns the test suites and validators (`--removed` when the feedback deletes a skill).
  5. A plain shell step commits to `claude/feedback-<issue>-<skill>`, opens or updates the pull request, comments on the issue, and posts the outcome to the same n8n webhook.
- **Skill proposals** get the `skill-proposal` label, which starts [`review-skill-proposal.yml`](.github/workflows/review-skill-proposal.yml):
  1. `unpack_submission.py` rejects unsafe paths, disallowed file types, secrets, name collisions, and oversize bundles. Deterministic, no model involved. Failures are commented on the issue and the label flips to `needs-changes`.
  2. Claude, running the [`review-submission`](.claude/skills/review-submission/SKILL.md) skill, applies the [review checklist](.claude/skills/review-submission/references/review-checklist.md), fixes packaging, integrates the skill, and writes a report. It has no git or GitHub tools.
  3. `verify_repo.py` reruns the test suites and validators and checks manifests and README. Its results go in the pull-request body whether they pass or fail.
  4. A plain shell step commits to `claude/skill-proposal-<issue>-<skill>`, opens or updates the pull request, comments on the issue, and posts the outcome to the n8n webhook (`N8N_REVIEW_WEBHOOK`, whose unguessable path suffix is the shared secret).

To change the review criteria, edit the checklist file or the `apply-feedback` skill. The workflows read them on every run.

## 3. Approve and ship

The whole pipeline is one n8n workflow, *Sales plugin contribution pipeline*, so there is a single place to watch it run.

The same workflow receives that outcome, for skill proposals and feedback alike, and sends the plugin owner one Slack DM with the verdict, the deterministic check results, and the pull-request link. He picks Approve and merge, Request changes, or Reject. A review that produced no pull request (for feedback: `needs-info`, `no-change`, or `reject`) sends him a notice instead, and the submitter is told why. Approve merges the pull request through the GitHub API. Request changes posts his notes to the issue and re-runs the review. Reject closes both. Nothing merges automatically, nothing pushes to `main` except a merged pull request, and the submitter is told the outcome either way.

A merge to `main` triggers the private mirror sync and is picked up by the ChatGPT workspace's daily marketplace sync.

## Running the checks locally

```
python3 .claude/skills/review-submission/scripts/test_unpack_submission.py
python3 .claude/skills/review-submission/scripts/verify_repo.py --skill <name> --out /tmp/verify.md
claude plugin validate --strict plugins/marq-sales-suite
```

## Bundle format for skill proposals

```
---
kind: skill-proposal
skill_name: my-skill
submitted_by: Your Name
summary: One line
---
Why this skill exists, who uses it, expected output.

--- file: SKILL.md ---
<file content>
--- file: agents/openai.yaml ---
<file content>
--- file: references/notes.md ---
<file content>
```

Allowed paths: `SKILL.md`, `agents/openai.yaml`, `references/*.md`, `scripts/*.py`, and text assets under `assets/`.
