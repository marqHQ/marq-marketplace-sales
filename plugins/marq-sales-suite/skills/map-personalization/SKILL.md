---
name: map-personalization
description: Personalize a Mutual Action Plan (MAP) for a sales prospect using HubSpot, Gong, Brandfetch, and Marq. Use when identifying a prospect, synthesizing one or more customer calls, reviewing MAP evidence, or creating an approved personalized MAP.
---

# Personalize a Mutual Action Plan

Build an evidence-backed MAP by completing each numbered step in order. Treat three challenge/solution pairs as a readiness requirement for the standard three-card template, not as a writing quota.

## Pilot Preflight

This workflow is an internal sales test until the `[TEST]` naming and pilot restrictions are deliberately removed.
For cohort setup, assigned scenarios, captured feedback, and exit criteria, read [references/pilot-test-plan.md](references/pilot-test-plan.md).

Scheduled or unattended runs are read-only. They may prepare evidence and a preview, but must stop before logo upload, project creation, or any Marq write even when the scheduling prompt requests creation.

Resolve `<skill-root>` to the absolute installed directory containing this `SKILL.md`. Substitute that resolved directory in the quoted validator paths below; never resolve bundled scripts from the user's working directory.

Before accessing prospect data:

1. Confirm that HubSpot, Marq Analytics, Brandfetch, and Marq Product are connected and callable. Confirm that subagent delegation is available. Report all missing dependencies together and stop before doing partial work.
2. Confirm that the HubSpot user can read contacts and companies, the Marq Analytics connection can search and read Gong transcripts plus approved messaging, and the Marq user can read templates, create projects, apply smart fields, and export them.
3. Confirm that the execution environment can download the credentialed Brandfetch asset URL exactly as returned. A connection that can display Brandfetch data but cannot fetch the asset bytes is not sufficient for logo insertion.
4. Run `python3 "<skill-root>/scripts/validate_template_map.py"` (canonical map version: `2026-10-06`) and read [references/template-map.json](references/template-map.json). Continue only when the validator confirms that all seven canonical keys (`higher ed`, `hospitals and clinics`, `real estate`, `manufacturing`, `insurance`, `financial services`, and `generic`) contain valid Marq template IDs. A missing, null, or malformed named-industry ID means the installed skill is stale or incomplete: stop and ask the tester to refresh the skill. Do not ask the tester to supply an ID and do not silently use generic.
5. Treat `2026-10-12` as the current pilot skill release and display it in the preview and final handoff. If an existing project being diagnosed lacks the required `[TEST] MAP - <company> - <date>` name, has rewritten table-of-contents/navigation copy, or contains writes outside the approved smart fields, classify it as noncompliant with the current release. Do not attribute that pattern to a Marq connection failure without tool-call or API-error evidence.
6. Do not activate optional-page or investment automation unless its separate catalog gate passes. During the pilot, explain that those pages are out of scope when the catalog is inactive.
7. A transient failure on a read-only lookup may be retried once. Never automatically retry project creation.

## Step 1: Find the Prospect in HubSpot

Find the supplied prospect in HubSpot without changing CRM data.

1. Treat `$ARGUMENTS` as a name, email address, HubSpot contact URL, contact ID, or company.
2. Call `get_user_details` before any CRM operation and confirm contact read access.
3. For a contact URL or ID, retrieve it directly. Otherwise discover the relevant properties and search contacts.
4. Request only useful identifying properties: first name, last name, email, job title, and company.
5. Prefer an exact email match. Otherwise compare full name and associated company.
6. If the input is a company, do not choose among several contacts yet. Use the evidence-source participants in Step 2 to resolve the relevant contact, then require one exact HubSpot match.
7. When several exact contacts participated, rank them by demonstrated ownership of the evaluated workflow or decision, then substantive participation in the evidence set, then the more senior relevant title as the tie-breaker. Ask the user only when those signals conflict or remain ambiguous; show up to five concise choices with record links. Never select by seniority alone when another participant clearly owns the work.

Return the selected contact's name, email, job title, company, HubSpot contact ID, and record link. Also retain the current HubSpot user's full name from `get_user_details` as `account executive name`; retain the selected contact's full name as `customer lead name`. These values drive the go-live ownership table. Resolve `implementation manager name` from an unambiguous HubSpot implementation/onboarding owner field or association when one is available. During the pilot, the named values are `Jamison Stromberg` or `Cheyenne Bigler`. Use a named value when HubSpot resolves exactly one or the user explicitly supplies or prefers one. Otherwise set `implementation manager name` to `CSM` without asking a blocking question. Do not infer a named assignment from industry, AE, geography, or prior MAPs. Keep HubSpot read-only.

## Step 2: Build the Call Evidence Set

Use the Marq Analytics MCP for every Gong operation in this step. If it is unavailable, stop and ask the user to install and connect it.

Read [references/call-selection-and-coverage.md](references/call-selection-and-coverage.md), then:

1. Call `search_gong_calls` with the company and, when known, the contact name or email, `hasTranscript: true`, and a limit of 10.
2. If no contact-level calls match, search again using only the company.
3. If no usable Gong transcript matches, repeat the same narrow searches without `hasTranscript` to distinguish a missing meeting from a meeting that exists without a transcript. When the input was a company, inspect its exact HubSpot-associated contacts and try their names or emails before concluding that Gong has no indexed meeting.
4. When Gong has no usable transcript, read and follow [references/external-hosted-evidence.md](references/external-hosted-evidence.md). Prompt for an attached, pasted, or accessible linked transcript from the partner- or customer-hosted meeting. Do not continue to customer-confirmed MAP creation until a usable transcript is supplied.
5. Rank all usable call transcripts for discovery value instead of selecting the newest call automatically. Prefer customer discovery, demo, strategy, and workflow conversations over pricing updates, training, implementation, or administrative check-ins.
6. Retrieve or read the most promising transcript in full. When the transcript tool returns a remaining-character count or continuation offset, continue until no transcript text remains unread; never analyze only the first chunk of a long transcript. Add transcripts incrementally until three distinct, separately actionable customer-supported priorities appear possible. Start with up to three calls; expand to at most five when coverage remains weak.
7. Keep the evidence set within the current sales cycle when possible. Older calls may supply context, but newer explicit customer statements override conflicting older evidence. When the available calls belong to an old or closed-lost cycle, label them historical and not revalidated as current. Historical evidence may support a clearly labeled internal test; a customer-facing MAP requires current validation or an explicit user decision before creation.
8. If participant identity remains unclear after applying the ownership, participation, and seniority hierarchy from Step 1, ask the user to choose. Do not infer a contact from company membership alone.
9. Retain each selected source's stable ID, title, date, source URL when available, meeting host, transcript source, participants, full transcript, selection reason, and evidence role.
10. If the user supplies candidate challenges, themes, or a call summary, treat them as prioritized hypotheses to validate first. They are not evidence by themselves. Record why any supported candidate was not selected and why any substitute was stronger.

Do not stop at a narrow recent call when earlier relevant calls are likely to contain substantive discovery evidence.

## Step 3: Create the Transcript Analysis JSON

1. Create a uniquely named temporary directory with mode `0700`, then create the JSON file inside it with mode `0600`. Do not place a customer name, company name, email address, or contact ID in either filename. Retain the resolved JSON path.
2. Initialize it with the schema in [references/transcript-analysis-prompt.md](references/transcript-analysis-prompt.md), including `prospect`, `evidence_sources`, `evidence_coverage`, `industry`, `logo`, `marq`, `review`, `qa`, `page_automation`, the 18 `marq_fields`, and `quote_evidence`. Store `evidence_coverage.sources_reviewed` as source ID strings only. `page_automation` is dormant metadata unless the activation gate in Step 7 passes.
3. Call Marq Analytics `get_messaging_and_icp` before drafting any customer-facing copy. When the industry is clearly known, also call `get_vertical_playbook`; when a proposed capability needs current product validation, use `list_field_briefs` and `get_field_brief`. Treat these retrieved documents—not transcript claims or model memory—as the approved Marq messaging sources.
4. Delegate analysis to a subagent. Give it every full transcript, any user-supplied candidate challenges, the JSON path, [references/transcript-analysis-prompt.md](references/transcript-analysis-prompt.md), [references/template-copy-budgets.json](references/template-copy-budgets.json), and the approved Marq messaging sources retrieved above.
5. Run `python3 "<skill-root>/scripts/validate_map.py" "<json-path>"` and correct every reported schema, coverage, or copy-budget error before continuing. This validator checks structure, copy budgets, and exact raw-excerpt containment; it does not prove speaker affiliation, challenge distinctness, or product claims. The independent review remains required.

The analysis may use fewer than three slots only when the evidence set genuinely cannot support three distinct, separately actionable priorities. Related priorities may remain separate when each describes a different operational condition, control point, or consequence and solving one would leave another materially unresolved. It must never fill a slot from an AE hypothesis, generic vertical guidance, or an unlabeled model assumption.

## Step 4: Independently Review the Analysis

1. Spawn a second subagent. Do not reuse the analysis subagent.
2. Give it every full transcript, the JSON path, the same approved Marq messaging sources passed to the analysis subagent in Step 3, [references/transcript-analysis-prompt.md](references/transcript-analysis-prompt.md), and [references/transcript-analysis-review-prompt.md](references/transcript-analysis-review-prompt.md).
3. Instruct it to report findings without editing the JSON.
4. Evaluate the findings and make only necessary corrections.
5. If review reduces confirmed coverage below three, return to Step 2 and add the next-best call before accepting an insufficient result.
6. Save the final reviewer outcome and concise findings under `review`; the reviewer remains read-only.
7. Run `python3 "<skill-root>/scripts/validate_map.py" "<json-path>"` again and confirm the corrected JSON passes.

Review outcomes:

- `PASS_READY`: exactly three distinct, customer-supported pairs are ready.
- `PASS_INSUFFICIENT`: the analysis correctly reports fewer than three after the permitted call search is exhausted.
- Actionable findings: correct them, then re-review the affected evidence.

## Step 5: Enforce the Evidence-Coverage Gate

Continue to project creation only when `evidence_coverage.status` is `ready`, `confirmed_challenges` is 3, and review returned `PASS_READY`.

If coverage remains insufficient:

1. Do not create the standard three-card Marq project.
2. Show the confirmed content, the missing coverage, calls reviewed, and why rejected candidates failed.
3. Offer only explicit next steps: provide another call, identify a specific call to include, or hand off to a separately approved reduced-card or hypothesis workflow. Reduced-card and hypothesis creation are not implemented by this skill or its validator; do not route them through Steps 7–8 or relabel their evidence as ready.
4. Never place hypotheses into the standard template as customer-confirmed challenges. One project approval does not authorize a hypothesis conversion or a different template.

## Step 6: Get the Company Logo

Use Brandfetch as the primary source. If it is unavailable or unauthenticated, stop and report the missing connection.

1. Resolve the associated HubSpot company and retrieve `name`, `domain`, and `hs_logo_url`. If duplicate company records exist, prefer the selected contact's associated company. When association is missing or still ambiguous, require an official-domain match corroborated by participant email domains, HubSpot properties, and Brandfetch; do not choose by company name alone. Treat the resolved company domain as the canonical identity key.
2. Call Brandfetch `get_brand` with the domain. Use `brand_search` only when the domain is missing or ambiguous, and require an official-domain identity match.
3. Prefer a verified full wordmark or combination mark that includes the company name. Use an icon-only mark only when no usable named logo exists, or when the user explicitly prefers the icon. Prefer transparent source assets and reject unintended opaque white or colored mattes.
4. Use the credentialed Brandfetch `src` exactly as returned, including its query string. Never substitute `build_logo_urls` output for ingestion.
5. Download the asset into the run's temporary directory and verify the media type, non-zero size, identity, transparency or background suitability, legibility at the rendered cover size, and visual contrast. Compare the candidate visually with the official-domain wordmark before upload. Reject a candidate containing Marq artwork, an unrelated brand mark, duplicated geometry, a composite screenshot, or any content outside the customer's verified logo. Do not choose an icon merely because it contrasts better than the available named logo.
6. When the verified named logo is transparent but available only in a light color on a light template (or dark on dark), create a contrast-safe monochrome variant by recoloring the original vector fills to an official brand color. Preserve the supplied paths, proportions, and transparency exactly; never redraw, regenerate, or invent logo geometry.
7. Before uploading any logo to Marq, rasterize the verified asset to a transparent PNG at no less than 4× its rendered dimensions while preserving aspect ratio. Do this even when the source is SVG: any SVG image fill can force a published MAP page to render at 72 DPI. Upload the PNG, then apply its resulting Marq image `contentUrl` to `company logo` so the smart-field binding remains intact.
8. Set `logo.confirmed` true only after those checks. If no verified named logo can be made usable, try HubSpot's `hs_logo_url` and then the official website. An icon-only Brandfetch result is not an automatic fallback: show it to the user and require explicit approval before using it. Record the actual source, logo type, verified domain, dimensions, and any approved icon-only fallback in the preview and QA.

## Step 7: Select the Template and Request Approval

Use the Marq MCP for every Marq operation. Read [references/template-map.json](references/template-map.json).

1. Select the approved industry template. Use `generic` when the industry is genuinely unlisted or still unknown, or when the user explicitly requests generic. Disclose an explicit generic override in the preview.
2. The all-seven-entry validation in Pilot Preflight must pass even for an explicit generic override. If a canonical named-industry ID is empty or invalid, stop as a stale-skill setup failure; never ask the tester for an ID or use generic to bypass it.
3. Read [references/optional-pages-and-investment.md](references/optional-pages-and-investment.md). Activate optional-page and investment automation only when `references/page-catalog.json` exists, is valid, and contains an approved `enabled: true` entry whose `template_id` exactly matches the selected template. Missing, invalid, disabled, or nonmatching configuration means `page_automation.status: inactive_not_configured` and preserves the existing MAP behavior: do not ask commercial questions or add, remove, duplicate, reorder, or populate optional or investment pages.
4. When automation is active, follow the catalog and the reference to select only approved pages, resolve missing commercial inputs, validate current pricing, and save the proposed page set plus evidence under `page_automation`. Enterprise and Premium may be catalog defaults, but they are not customer-confirmed facts and require explicit rep confirmation before customer-facing investment content is created.
5. Show a preview containing pilot release `2026-10-12`, the prospect, every evidence source, evidence coverage, industry, selected or proposed fallback template, the actual logo candidate with its verified domain and logo type, the resolved implementation manager value (named when known or preferred, otherwise `CSM`), and all 18 proposed MAP fields. When automation is active, also show every proposed retained or added page, every catalog-managed page proposed for removal, each selection reason and evidence source, the page insertion anchor, commercial defaults and resolved values, unresolved commercial inputs, and pricing-source status.
6. Before requesting approval, call `dmes_GetSmartFields` on the selected source template as a read-only preflight. Retry once only when the first read fails transiently. Confirm the 18 MAP text fields plus project text field `company name` and project image field `company logo` exist. Inventory every dataset, user, and team smart-field dependency. The obsolete `aideck.company primary` dataset field must not be present. Then locate the go-live timeline table and read its styled text directly: confirm it contains shape-data spans labeled `customer lead name`, `account executive name`, and `implementation manager name`, with no raw error visible. Marq's aggregate smart-field scan may omit formulas inside table cells, so the direct table-span check is authoritative for these three fields. Save both results under `qa.template_preflight_status` and `qa.unresolved_dataset_fields`.
7. Before approval or creation, call `dmes_GetImages` across the complete source template, then `image_GetImage` for every unique returned `imageId`. Require zero non-logo blocks reported as `image/svg+xml` and zero non-logo source assets whose original `contentType` is `image/svg+xml`. If SVG-backed template artwork is present, or either scan is incomplete, stop and report that separate authorized template maintenance is required. Do not modify or rasterize template artwork during MAP personalization. The `company logo` binding is the only image replacement authorized by this workflow and will receive the verified PNG from Step 6. Capture a protected-content baseline from the selected source template: page IDs and order, page titles, all non-smart-field text, the complete table-of-contents/navigation page text, and every image block outside `company logo`. Everything in this baseline is immutable for the run unless an active, explicitly approved page-catalog operation names that exact page or block. Save the normalized baseline under `qa.protected_content_baseline`; do not rely on visual memory alone.
8. The templates may still expose `Full Name`/`Title` from the team-directory dataset. Do not treat either field as the prospect contact. Locate the pages that reference unresolved fields with the Marq page/block read tools or a template export. During the internal pilot, unresolved team-directory fields may remain only when they are confined to untouched, out-of-scope pages and are disclosed in the preview; such a project is not customer-ready. Any unresolved dependency visible on the cover, challenge, or solution pages blocks creation.
9. Ask for one explicit confirmation covering the displayed template choice, template-preflight findings, known pilot-only limitations, logo candidate, and creation of one internal test project. When automation is active, the same confirmation must explicitly cover the displayed page set and commercial defaults or values. Do not create it before approval.
10. One approval authorizes exactly one creation attempt using the displayed template and, when active, the displayed page set and commercial values for the current run. Ask again before any retry, additional project, different template, materially different page set, or changed commercial recommendation.

## Step 8: Create and Personalize the Marq Project

1. Call `document_CreateProjectFromTemplate` exactly once with the approved template. Name it `[TEST] MAP - <company name> - <YYYY-MM-DD>`.
2. Confirm the response contains a new project ID different from the source template ID and that the resulting project name exactly matches `[TEST] MAP - <company name> - <YYYY-MM-DD>`. If identity or naming is missing, ambiguous, mismatched, or matches the template, stop without content writes.
3. Save the template ID, project ID, URL, and name under `marq` in the JSON.
4. Read [references/template-copy-budgets.json](references/template-copy-budgets.json), using the selected template's limits when present and `default` otherwise. Call `dmes_GetSmartFields` on the new project before writing and compare its complete smart-field inventory with the approved template preflight. Stop on material drift. Confirm all 18 MAP text keys plus `company name` exist as project text fields and `company logo` exists as a project image field. `logo_dark` does not satisfy this requirement. Directly reread the go-live timeline table and confirm the `customer lead name`, `account executive name`, and `implementation manager name` formula spans survived project creation.
5. Apply only the 18 reviewed MAP text values, the exact HubSpot company name to `company name`, the selected contact's full name to `customer lead name`, the current HubSpot user's full name to `account executive name`, the HubSpot-resolved or user-confirmed named value—or the default `CSM`—to `implementation manager name`, and the rasterized PNG to `company logo`, using only the applicable smart-field APIs in one batch or serially. Store challenge quote values without leading or trailing quotation marks because the MAP template supplies the visible quote punctuation. When page automation is inactive, direct styled-text writes, block replacement, page creation/deletion/reordering, page-title edits, and layout edits are forbidden—even if the model believes they would improve personalization. If a required value cannot be expressed through its approved smart field, stop. Never write to the source template, modify a dataset, or make parallel writes to the same project.
6. When `page_automation.status` is `approved_ready`, follow [references/optional-pages-and-investment.md](references/optional-pages-and-investment.md) to resolve the approved catalog entries against live page titles in the new project, retain or duplicate the approved pages at semantic anchors, remove only catalog-managed unselected pages, and populate only explicitly approved commercial values. Stop on missing or duplicate page-title matches, stale pricing, unresolved required commercial inputs, or any mismatch from the approved preview. Never mutate the source template.
7. Inspect every write result. A failed idempotent smart-field write may be retried once, serially, in the same approved project after confirming that the successful writes are intact. Read back all required project fields, including `company name`, and directly read the go-live timeline table cells to confirm that `customer lead name`, `account executive name`, and `implementation manager name` render the selected contact, current user, and the chosen named value or `CSM` fallback. A table-cell span may report state `unknown`; accept it only when the rendered replacement exactly equals the applied value and no raw expression or error is visible. When active, also read back the final catalog-managed page inventory. Confirm every in-scope formula remains attached, every required value resolves, the image remains bound to `company logo`, and the page set and order match the approval. Save the verification under `qa` and `page_automation.qa`.
8. Re-read the full project content and compare it with `qa.protected_content_baseline`. Require exact matches for page count/order/titles, table-of-contents/navigation copy, every non-smart-field text value, and every image block outside `company logo`, except for explicitly approved catalog-managed changes. Any unexplained difference is a hard failure: set `qa.protected_content_status` to `failed`, mark the existing project `INCOMPLETE`, list the changed blocks, and stop without attempting creative repair.
9. Call `dmes_GetImages` across the complete generated project, then call `image_GetImage` once for every unique returned `imageId`. Require zero blocks reported as `image/svg+xml` and zero underlying source assets whose original `contentType` is `image/svg+xml` before export. A block-level PNG label does not prove that its source asset was rasterized. If either scan is incomplete or any SVG-backed fill remains, mark the existing project `INCOMPLETE` and stop without replacing protected artwork. Report the affected blocks for separate authorized template maintenance. This check applies to template artwork as well as the customer logo and does not authorize additional image writes.
10. Export and visually inspect the cover, table-of-contents/navigation, challenge, solution, and go-live timeline slides. When automation is active, also inspect every added optional page, the investment summary, and both next-step views that remain. On the cover, compare the rendered customer-logo region with the approved candidate and require the same wordmark, proportions, and brand identity with no Marq `q`, Marq logo, unrelated artwork, duplicate mark, clipping, or bounding-box collision inside the customer-logo region. Confirm resolved company/AE/customer names, correct implementation owners, unchanged protected navigation copy, absence of raw placeholders, correct page order, consistent commercial values, and no personalized-copy clipping or overflow. Save the export location and result under `qa`, including `logo_render_status` and `protected_content_status`. Treat overflow telemetry as a diagnostic signal: when it reports overflow, inspect the rendered export before deciding whether personalized copy needs repair.
11. If an intentionally blank value exposes a raw placeholder, stop. Do not silently replace it with filler; return to the evidence gate or the commercial-input gate, or hand off to a separately approved reduced-card workflow outside this skill.
12. If personalized copy visibly clips, truncates, or overflows in the rendered export, repair only the affected field without changing its supported meaning. For a quote, choose a shorter contiguous excerpt from the same customer turn and update its evidence metadata if needed. Update the JSON, reapply only affected fields serially, reread them, and re-export only affected slides. This is repair of the approved project, not another creation attempt. Make at most two repair passes per field; if it still fails, stop and report it.
13. Do not change template layout, font sizes, or unrelated content to force copy to fit. Report fixed-template overflow and telemetry-only warnings separately from personalized-copy overflow. A telemetry warning may pass only when the rendered export shows the complete intended text with no clipping or truncation; record that visual determination under `qa`. Do not mark the MAP complete while personalized fields, active page automation, or commercial fields are unresolved or visibly clipped.

If project creation succeeded but a later write or QA step fails, return the existing project URL marked `INCOMPLETE`, list the failed checks, and stop. Do not create a replacement project without a new preview and explicit approval.

## Step 9: Clean Up and Hand Off

1. Return the `[TEST]` project URL, the evidence and review status, template-preflight result, known unresolved out-of-scope fields, and QA result. State explicitly that the rep must review the project before sharing it externally.
2. Delete the temporary directory containing full transcripts and the analysis JSON after successful handoff, cancellation, or a terminal failure. Keep it only while actively awaiting the approval needed to continue the same run.
3. Do not copy full transcripts into the repository, a durable artifact, HubSpot, or Marq. Retain only the concise provenance and QA summary shown to the user.

Do not modify HubSpot, unrelated Marq fields, datasets, blocks, slides, or the source template.
