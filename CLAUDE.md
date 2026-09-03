# CLAUDE.md

Follow [AGENTS.md](AGENTS.md) — it is the canonical agent guide for this repo (layout, skill-editing invariants, scoring contract, tests).

Claude Code specifics:

- This repo is itself a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`); skills auto-discover from `plugins/marq-sales/skills/`.
- When testing skill changes locally: `/plugin marketplace add <path-to-this-repo>` then `/plugin install marq-sales@marq-sales-plugins`.
