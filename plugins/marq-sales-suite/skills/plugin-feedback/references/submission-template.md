# Plugin skill feedback record

Use this structure for the record the rep pastes into the contribution form. Omit optional sections that would be empty. Keep it concise and useful to the skill owner. The pipeline wraps the record with the skill name, submitter, and timestamp, so do not repeat those.

```markdown
**Category:** <incorrect-behavior | missing-step | unclear-instruction | tool-failure | output-quality | workflow-friction | permissions-or-security | enhancement>
**Platform:** <ChatGPT | Codex | Claude Code> · **Skill version, if known:** <plugin version or "unknown">

## Observed behavior

<What the rep directly observed.>

## Expected behavior

<What the rep expected instead.>

## Impact

<Why the difference matters to a rep, customer, or workflow.>

## Reproduction context

<Sanitized steps, inputs, conditions, or environment details. No private links or customer data.>

## Suggested direction

<Optional. Preserve this as the rep's suggestion, not an approved solution.>

## Evidence and uncertainty

<Optional. Sanitized evidence plus unresolved facts, and which statements are the agent's inference rather than the rep's observation.>

## Redactions

<What was replaced with placeholders, so the owner knows what is missing.>
```
