# Skill proposal bundle format

The contribution form accepts one plain-text bundle per proposal. The intake pipeline parses it with `unpack_submission.py`, so the shape below is a contract, not a suggestion.

```
---
kind: skill-proposal
skill_name: my-skill
submitted_by: Rep Name
summary: One line that fits in a Slack message
---
Why this skill exists, who uses it, what it produces, which connectors it needs,
and any external writes it performs. Note anything you could not test.

--- file: SKILL.md ---
---
name: my-skill
description: ...
---
# My skill
...
--- file: agents/openai.yaml ---
interface:
  display_name: "My Skill"
  short_description: "Between 25 and 64 characters"
  default_prompt: "Use $my-skill to ..."
--- file: references/notes.md ---
...
```

Rules the parser enforces:

- The bundle starts with `---` on the first line and the frontmatter declares `kind: skill-proposal` and `skill_name`.
- `skill_name` uses lowercase letters, digits, and single hyphens, and equals the `name` in `SKILL.md`'s frontmatter.
- Each file starts with a line `--- file: <relative path> ---`. Everything until the next marker is that file's content. Nothing may follow the last file.
- Allowed paths: `SKILL.md` (required), `agents/openai.yaml`, `references/*.md`, `scripts/*.py`, and `assets/*` with a text extension (`md`, `txt`, `json`, `yaml`, `yml`, `csv`, `html`, `svg`). No `..`, no absolute paths, no hidden files, no binaries.
- One code fence wrapping a whole file's content is stripped; anything else inside a file is kept verbatim.
- Each file under 200,000 bytes, the whole bundle under 60,000 characters when pasted into the form, at most 40 files.
- Any string that looks like a Slack, GitHub, Anthropic, OpenAI, HubSpot, Google, or AWS credential, a private key, or a JWT rejects the submission before it reaches GitHub.

What happens after submission: the pipeline installs the files under `plugins/marq-sales-suite/skills/<skill_name>/`, an automated reviewer applies the owner's checklist and fixes packaging, deterministic checks run the repository's test suites and validators, a pull request opens with the review report, and the plugin owner decides in Slack. The rep sees progress in the intake Slack thread.
