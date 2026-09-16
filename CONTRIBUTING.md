# Contributing skills and feedback

Sales reps contribute without touching GitHub. The pipeline has three stages, each owned by a different system so no single credential can do everything.

## 1. Submit

- **Feedback about an existing skill:** run `plugin-feedback` in ChatGPT or Codex. It interviews you, redacts customer data, and hands you a filled-in form link.
- **A new skill:** run `upload-new-skill`. It normalizes your draft into a single text bundle and hands you the form link. Skills are text, so nothing is zipped or uploaded.

Both go to one intake form. n8n logs the submission, opens a Slack thread in the intake channel, and files a GitHub Issue on your behalf. You never need a GitHub account.

## 2. Review

- **Feedback** issues get the `feedback` label. The plugin owner triages them; `@claude` on the issue can draft a fix.
- **Skill proposals** get the `skill-proposal` label, which starts [`review-skill-proposal.yml`](.github/workflows/review-skill-proposal.yml):
  1. `unpack_submission.py` rejects unsafe paths, disallowed file types, secrets, name collisions, and oversize bundles. Deterministic, no model involved. Failures are commented on the issue and the label flips to `needs-changes`.
  2. Claude, running the [`review-submission`](.claude/skills/review-submission/SKILL.md) skill, applies the [review checklist](.claude/skills/review-submission/references/review-checklist.md), fixes packaging, integrates the skill, and writes a report. It has no git or GitHub tools.
  3. `verify_repo.py` reruns the test suites and validators and checks manifests and README. Its results go in the pull-request body whether they pass or fail.
  4. A plain shell step commits to `claude/skill-proposal-<issue>-<skill>`, opens or updates the pull request, comments on the issue, and notifies n8n.

To change the review criteria, edit the checklist file. The workflow reads it on every run.

## 3. Approve and ship

n8n sends the plugin owner one Slack message with the report summary, the pull-request link, and Approve / Request changes / Reject. Approve merges the pull request. Request changes posts the note to the issue and re-runs the review. Nothing merges automatically, and nothing pushes to `main` except a merged pull request.

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
