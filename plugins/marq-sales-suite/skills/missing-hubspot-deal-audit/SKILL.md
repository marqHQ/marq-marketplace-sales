---
name: missing-hubspot-deal-audit
description: Audit a sales rep's external demos, discovery calls, and other buying conversations over a date range to identify conversations that lack a corresponding HubSpot deal. Use when asked whether a recent demo, meeting, or call was never added as a HubSpot deal. Do not use for follow-up-task extraction, general pipeline health, or CRM writes.
---

# Missing HubSpot Deal Audit

Identify genuinely missing HubSpot deals without confusing an unassociated meeting, a company record, or a call-recording CRM-stage label for a deal.

This is a read-only workflow. Do not create or modify deals, associations, companies, contacts, meetings, tasks, or other CRM records unless the user separately requests that work. Treat a scheduled or unattended run as read-only regardless of prompt wording; this audit has no write path.

## Required capabilities and stopping conditions

- Require authenticated, read-only access to HubSpot companies, contacts, deals, and meeting engagements. If HubSpot is unavailable or those objects cannot be read, stop and explain that the audit cannot determine whether deals are missing.
- Use an authenticated call-recording or conversation-intelligence source, such as Gong, when available to find calls and read transcripts. If it is unavailable, continue with HubSpot meetings and substantive notes, clearly label call-source coverage as incomplete, and do not claim that all external conversations were reviewed.
- If neither transcripts nor substantive meeting notes are available for a conversation, retain it as `Needs review` rather than classifying it from the title alone.

## Inputs and scope

- Accept an explicit date range when supplied.
- Otherwise use the current calendar week: Monday at 12:00 a.m. through the current time in the user's local timezone.
- Treat the requested end date as inclusive.
- Scope HubSpot reads to the current user's owner ID and call-source reads to the current user's email or participant identity.
- Report the exact date range and timezone used.

## 1. Discover meetings and calls

1. Use the HubSpot connector to retrieve the current user's identity and available object access. Confirm that meeting engagements, companies, contacts, and deals are readable. Retain the user's HubSpot owner ID and email.
2. Search HubSpot meeting engagements within the UTC-converted date boundaries and owned by the current user. Retrieve at least the title, start time, end time, outcome, activity type, owner ID, attendee owner IDs, record ID, associations, and any substantive notes or summary. Sort chronologically and paginate until all results are retrieved.
3. Search the available call-recording source for calls in the same local-date range with the current user as a participant. Paginate until all results are retrieved.
4. Combine both sources. Deduplicate records representing the same conversation using normalized title or account plus start times within a reasonable tolerance. Preserve every available source identifier and link, especially the HubSpot meeting ID and call-recording ID.
5. Retain transcript availability, external participants, CRM account or stage metadata, and source provenance. Report source totals, the deduplicated total, and any coverage discrepancy. A call-source-only call or HubSpot-only meeting must remain in scope.

## 2. Keep only sales-relevant conversations

When a transcript exists, read it. Otherwise use substantive HubSpot meeting notes or summaries when available. Do not classify from the title alone when stronger evidence exists.

Include an external conversation when a prospect or customer is actively evaluating a new purchase or distinct paid expansion. Useful signals include:

- demo, discovery, evaluation, or solution review;
- buying requirements, pain, use cases, or technical fit;
- pricing, budget, procurement, competitive evaluation, or decision process;
- a concrete paid expansion that should reasonably have its own opportunity.

Exclude:

- internal meetings;
- partner-only coordination;
- routine account anniversaries, QBRs, and customer-success check-ins;
- support, training, and post-sale implementation calls;
- renewals that do not represent a distinct new opportunity.

If an existing-customer call contains a concrete upsell or expansion, include only that opportunity. If the evidence is insufficient, retain the conversation as `Needs review` rather than guessing.

## 3. Resolve the prospect account

Resolve one canonical HubSpot company before matching deals.

1. Search company records directly associated with the HubSpot meeting engagement.
2. Validate the company against associated contacts, external attendee email domains, the meeting title, transcript context, and call-source CRM account metadata.
3. If no company is directly associated, inspect associated contacts and search HubSpot companies by normalized account name and domain.
4. Prefer an exact domain match over a loose name resemblance.
5. Keep parent companies, subsidiaries, similarly named companies, partners, and the actual prospect distinct unless the evidence clearly connects them.
6. If multiple plausible companies remain, mark the account `Needs review` instead of selecting one.

Retain the canonical company ID, name, domain, supporting contacts, HubSpot URL, and the evidence used to resolve it.

## 4. Check direct deal associations

For each sales-relevant HubSpot meeting, search deals directly associated with its meeting engagement ID.

Retrieve at least the deal name, company name, deal stage, pipeline, owner ID, creation date, last-modified date, and close date.

- One contextually correct deal is strong evidence for `Deal found and associated`.
- If several deals are directly associated, compare company, active or closed status, timing, and conversation context. Use `Needs review` if one cannot be selected confidently.
- No direct association is not proof that the deal is missing. Continue to fallback matching.
- Calls without a HubSpot meeting ID go directly to fallback matching.

## 5. Find unassociated deals

Search in this order:

1. Deals associated with the canonical HubSpot company ID.
2. Deals found by normalized company or account-name variants.
3. When useful, exact domain or additional transcript-derived account identifiers.

Use HubSpot property metadata to translate pipeline and deal-stage IDs into human-readable labels.

Rank candidate deals using:

- exact company association and domain or account identity;
- deal and company-name alignment;
- open versus historical or closed status;
- creation, modification, and close dates relative to the conversation;
- owner, pipeline, stage, product, and transcript context.

An exact company-associated, contextually aligned active deal is a confirmed match even when the meeting is not associated with it. Do not accept an unrelated historical deal merely because the company names match. Name-only matches, multiple plausible active deals, unclear subsidiaries, or mismatched context require review.

Classify `No corresponding deal found` only after the direct meeting association, company association, normalized-name, and relevant domain or account searches all fail. A company, contact, lead, meeting, or call-source CRM-stage label does not prove that a HubSpot deal exists.

## 6. Assign one final classification

Use exactly one of these classifications for every sales-relevant conversation:

1. `Deal found and associated` — a contextually correct deal is directly associated with the meeting.
2. `Deal found but meeting not associated` — a confirmed corresponding deal exists through company or account matching, but the meeting is not linked to it.
3. `Probable deal match requiring review` — plausible deals exist, but the evidence is insufficient to select confidently.
4. `No corresponding deal found` — the prospect account is reasonably resolved and exhaustive matching found no credible deal.

Keep sales-relevance confidence separate from deal-match confidence. Surface unresolved accounts or insufficient evidence as review cases, not definitive missing deals.

## 7. Report

Lead with the outcome. Include:

- exact date range and timezone;
- HubSpot and call-source totals, deduplicated conversation count, and whether retrieval was complete or sampled;
- number and identities of missing-deal candidates;
- a compact table of every sales-relevant conversation with date and title, resolved account, final classification, matched deal when present, and clickable HubSpot or call-recording links;
- a separate note for meetings that merely lack a deal association;
- ambiguous or insufficient-evidence cases;
- a brief list of excluded conversations and why they were excluded;
- an explicit statement that no CRM changes were made.

Do not add follow-up recommendations, task lists, email drafts, or deal-creation steps unless the user separately asks for them.
