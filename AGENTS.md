# Agent guide

Dual-compatible plugin marketplace (Claude Code + Codex) for Marq sales skills. Human-facing overview and install steps: [README.md](README.md).

## Commands

No build step. Run the relevant test suites:

```
python plugins/marq-sales-suite/skills/audit-hubspot-pipeline/scripts/run_tests.py
python3 plugins/marq-sales-suite/skills/marq-deal-acceleration/scripts/run_tests.py
python3 plugins/marq-sales-suite/skills/marq-post-call-execution/scripts/check_acceptance_fixtures.py
```

Run the audit suite after any change under `audit-hubspot-pipeline/scripts/` or to `references/scoring-fixtures.json`. Run the deal-acceleration suite after any change to its momentum scorer, contract, or fixtures. Run the post-call fixture checker after changes to its workflow, evidence model, CRM mapping, or acceptance cases.

## Layout

- `plugins/marq-sales-suite/skills/<name>/` — each skill: `SKILL.md`, `references/`, optional `scripts/` and `agents/openai.yaml` (Codex interface metadata).
- Marketplace manifests: `.claude-plugin/marketplace.json` (Claude Code) and `.agents/plugins/marketplace.json` (Codex).
- Plugin manifests: `plugins/marq-sales-suite/.claude-plugin/plugin.json` and `plugins/marq-sales-suite/.codex-plugin/plugin.json`. Keep name, description, and version in sync across both when editing either.
- `under-construction/` — draft docs, not skill-formatted. Don't load or promote them without adding proper SKILL.md frontmatter.

## Invariants — do not weaken when editing skills

- Every CRM write is gated behind an exact approval table; approval of a different proposal is insufficient.
- Scheduled/unattended runs are read-only regardless of prompt wording.
- No negative inference from silence (absence of discussion never becomes `No`/`None`).
- Portal fields, stages, and enums are discovered live, never hardcoded.
- Writes are verified by an independent connector re-read, never by a UI success banner.
- `hs_next_step` remediation is append-only.

## Scoring

Green/yellow/red scoring is deterministic Python in `scripts/audit_utils.py` — never reproduce it in prose or let a model score heuristically. `references/scoring.md` is the contract; keep it and the code in sync. Fixtures live in `references/scoring-fixtures.json`; add a fixture when adding a scoring rule.

The deal-acceleration skill has its own deterministic customer-momentum classifier in `scripts/momentum_utils.py`. Its contract is `references/momentum-and-evidence.md`; fixtures live in `references/momentum-fixtures.json`. Keep all three synchronized.

## Definition of done

- Test suite passes.
- Both plugin manifests (`.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`) still agree on name, description, and version.
- Any scoring behavior change is reflected in `references/scoring.md` and covered by a fixture.
- Skill edits preserve every invariant above.
