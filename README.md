# Marq Sales Plugins

Public plugin marketplace for the Marq sales team. It contains one plugin (`marq-sales-suite`) with seven skills, packaged for both Claude Code and Codex.

The source is publicly readable for installation and inspection. It remains unlicensed; public availability does not grant permission to copy, modify, or redistribute it.

## Skills

- **mql-to-sqo** — Converts an existing HubSpot MQL deal into an SQO: Gong-backed qualification fields, product-library line items, synchronized deal amount. Every CRM write requires explicit approval of an exact proposal.
- **audit-hubspot-pipeline** — Audits a rep's full open Sales Pipeline, corroborates next steps against HubSpot activities, Google Calendar, and Gong, and scores every deal green/yellow/red with a deterministic Python scorer. Scheduled runs are always read-only; repairs are append-only and approval-gated.
- **spiced-call-coach** — Reviews a sales call using the SPICED framework and returns evidence-backed coaching.
- **map-personalization** — Builds customer-ready Mutual Action Plan copy from HubSpot and Gong, selects the approved Marq template, and creates one approval-gated test project with a verified company logo.
- **confirm** — Restates the requested outcome and obtains confirmation before acting.
- **workflow-creator** — Converts a repeatable sales workflow into a structured skill.
- **tldr** — Cognitive-load circuit breaker: rewrites the last stretch of output as a 3–7 item numbered digest you can drill into one item at a time, then pauses until you choose.

## Prerequisites

Connected and authorized as required by the selected workflow: **HubSpot**, **Gong**, **Google Calendar**, **Brandfetch**, **Marq**, and **Marq Analytics**. The mql-to-sqo skill also needs a browser tool signed into the HubSpot portal for line-item rebuilds.

## Install

### Claude Code

```
/plugin marketplace add marqHQ/marq-marketplace-sales
/plugin install marq-sales-suite@marq-sales-plugins
```

### Codex

```bash
codex plugin marketplace add https://github.com/marqHQ/marq-marketplace-sales
codex plugin add marq-sales-suite@marq-sales-plugins
```

Registering the GitHub repository without a pinned ref lets Codex track marketplace updates from its default branch. Audit deployment details, the weekly recurring-task prompt, and pilot acceptance criteria: [deployment.md](plugins/marq-sales-suite/skills/audit-hubspot-pipeline/references/deployment.md).

## Testing

```
python plugins/marq-sales-suite/skills/audit-hubspot-pipeline/scripts/run_tests.py
```

Run after any change to the scoring logic or fixtures.

## Layout

```
.claude-plugin/marketplace.json    Claude Code marketplace manifest
.agents/plugins/marketplace.json   Codex marketplace manifest
plugins/marq-sales-suite/          The plugin (skills/, both plugin manifests, assets)
```
