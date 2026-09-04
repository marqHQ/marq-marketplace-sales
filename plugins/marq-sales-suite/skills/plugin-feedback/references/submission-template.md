# Plugin skill feedback record

Use this structure for the feedback file. Omit optional sections that would be empty. Keep the submission concise and useful to the skill owner.

```markdown
---
submitted_at_utc: "<YYYY-MM-DDTHH:MM:SSZ>"
submitted_by: "<verified name or not provided>"
affected_skill: "<skill-name>"
category: "<category>"
status: "new"
---

# <Concise feedback summary>

## Observed behavior

<What the rep directly observed.>

## Expected behavior

<What the rep expected instead.>

## Impact

<Why the difference matters.>

## Reproduction context

<Sanitized steps, inputs, conditions, or environment details. Do not include private links or customer data.>

## Suggested direction

<Optional. Preserve this as the rep's suggestion, not an approved solution.>

## Evidence and uncertainty

<Optional sanitized evidence plus any unresolved facts or agent inferences.>
```

For `submitted_by`, use an authenticated profile name only when a connected tool exposes it reliably. Otherwise ask what name the rep wants attached, or use `not provided` if they prefer not to include one.
