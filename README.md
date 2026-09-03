# Marq Sales Plugins

Public plugin marketplace for the Marq sales team. It contains one plugin (`marq-sales`) with five skills, packaged for both Claude Code and Codex.

The source is publicly readable for installation and inspection. It remains unlicensed; public availability does not grant permission to copy, modify, or redistribute it.

## Skills

- **mql-to-sqo** — Converts an existing HubSpot MQL deal into an SQO: Gong-backed qualification fields, product-library line items, synchronized deal amount. Every CRM write requires explicit approval of an exact proposal.
- **audit-hubspot-pipeline** — Audits a rep's full open Sales Pipeline, corroborates next steps against HubSpot activities, Google Calendar, and Gong, and scores every deal green/yellow/red with a deterministic Python scorer. Scheduled runs are always read-only; repairs are append-only and approval-gated.
- **spiced-call-coach** — Reviews a sales call using the SPICED framework and returns evidence-backed coaching.
- **confirm** — Restates the requested outcome and obtains confirmation before acting.
- **workflow-creator** — Converts a repeatable sales workflow into a structured skill.

## Prerequisites

Connected and authorized: **HubSpot**, **Gong**, and **Google Calendar**. The mql-to-sqo skill also needs a browser tool signed into the HubSpot portal for line-item rebuilds.

## Install

### Claude Code

```
/plugin marketplace add mikemarqq/marq-sales-plugins
/plugin install marq-sales@marq-sales-plugins
```

### Codex

Register this repository as a marketplace, then install `marq-sales`. The Marq Plugin Directory is the canonical source for the exact approved repository revision.

Repository updates are not applied automatically. Refresh the marketplace and update the installed plugin explicitly, then start a fresh task so the updated skills are loaded.

## Testing

```
python plugins/marq-sales/skills/audit-hubspot-pipeline/scripts/run_tests.py
```

Run after any change to the scoring logic or fixtures.

## Layout

```
.claude-plugin/marketplace.json    Claude Code marketplace manifest
.agents/plugins/marketplace.json   Codex marketplace manifest
plugins/marq-sales/                The plugin (skills/, both plugin manifests, assets)
```
