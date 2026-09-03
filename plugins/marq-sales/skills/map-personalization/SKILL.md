---
name: map-personalization
description: Personalize a Mutual Action Plan (MAP) for a sales prospect using HubSpot, Gong, Brandfetch, and Marq. Use when a user wants to start or continue the MAP workflow by identifying a prospect, finding the relevant Gong transcript, and creating personalized MAP content.
---

# Personalize a Mutual Action Plan

Build a personalized MAP by completing each numbered step in order.

## Step 1: Find the Prospect in HubSpot

Find the supplied prospect in HubSpot without changing CRM data.

### Required input

Treat the prospect supplied in the user's request as the prospect to find. Accept a name, email address, HubSpot contact URL, or HubSpot contact ID.

If the request does not identify a prospect, stop and ask for the prospect's name or email address.

### Procedure

1. Use the HubSpot connector and call `get_user_details` before any CRM operation. Confirm the account has contact read access.
2. Find the contact:
   - For a HubSpot contact URL or known contact ID, retrieve that contact directly.
   - For a name or email address, discover the relevant contact properties, then search HubSpot contacts.
3. Request only useful identifying properties: first name, last name, email, job title, and company.
4. Prefer an exact email match. Otherwise, compare the full name and company when available.
5. If one clear match exists, return the contact's name, email, job title, company, HubSpot contact ID, and a clickable HubSpot record link.
6. If several plausible matches exist, return up to five concise choices with record links and ask the user to choose one.
7. If no match exists, say so and ask for an email address or company name to narrow the search.

### Guardrails

- Keep this step read-only. Do not create, update, merge, or delete HubSpot records.
- Do not guess that a partial match is the correct person.
- Keep the response concise because the selected contact will become the input to later MAP workflow steps.

## Step 2: Find the Gong Transcript

Use the Marq Analytics MCP for every operation in this step.
If it is unavailable, stop and ask the user to install and connect the Marq Analytics MCP before continuing.

1. Call `search_gong_calls` with the contact's company, name or email, and `hasTranscript: true`. Limit results to 10.
2. If no calls match the contact, search again using only the company name.
3. Select the most recent customer call that clearly matches the contact or company. If the match is unclear, ask the user to choose from the matching calls.
4. Use `get_gong_transcript` with the selected call ID. Continue from the returned offset until the full transcript is retrieved.
5. Retain the call ID, title, date, Gong link, participants, and full transcript for the next step.

## Step 3: Create the Transcript Analysis JSON

1. Create a uniquely named JSON file in the operating system's temporary directory. Retain its resolved path.
2. Initialize it with top-level `prospect`, `gong_call`, `industry`, `logo`, and `marq` fields; a `marq_fields` object containing the 18 empty slide fields; and a `quote_evidence` object.
3. Delegate the analysis to a subagent. Give it the full transcript, the JSON path, and [references/transcript-analysis-prompt.md](references/transcript-analysis-prompt.md).
4. Confirm the completed file contains valid JSON before continuing.

## Step 4: Review the Transcript Analysis

1. Spawn a second subagent. Do not reuse the analysis subagent.
2. Give it the full transcript, the JSON path, [references/transcript-analysis-prompt.md](references/transcript-analysis-prompt.md), and [references/transcript-analysis-review-prompt.md](references/transcript-analysis-review-prompt.md).
3. Instruct it to report findings without editing the JSON.
4. Evaluate its findings and make only the corrections you judge necessary.
5. Confirm the corrected file contains valid JSON and every required field before continuing.

## Step 5: Get the Company Logo

Use the Brandfetch MCP as the primary logo source. If it is unavailable or unauthenticated, stop and report that the Brandfetch connection is missing; do not silently skip the logo step.

1. Resolve the associated HubSpot company and retrieve `name`, `domain`, and `hs_logo_url`. Treat the HubSpot company domain as the canonical identity key.
2. When the domain is known, call Brandfetch `get_brand` with that domain. Use `brand_search` only when the domain is missing or the identity is ambiguous, then require the returned brand to match the official company domain before continuing.
3. Select an asset whose Brandfetch type is `logo`, not `icon` or `symbol`. Prefer a transparent PNG suitable for a white background; use a transparent SVG when it is the best available logo and the downstream operation supports it.
4. Use the credentialed Brandfetch `src` URL exactly as returned, including its query string. Do not substitute a URL from `build_logo_urls`, because those URLs are display-only and are not suitable for downloading or Marq ingestion.
5. Download the selected asset into the run's temporary directory and verify that it is a non-empty image of the expected media type. Reject favicons, lettermarks, social banners, screenshots, and uncertain identity matches.
6. Set `logo.source_url` to the exact Brandfetch `src`, `logo.local_path` to the saved file, `logo.source` to `brandfetch`, and `logo.confirmed` to `true` only after the domain and asset validations pass.
7. If Brandfetch has no usable asset for the confirmed domain, try the matching HubSpot `hs_logo_url`, then the company's official website. Record the actual source. If the remaining match is uncertain, stop and ask the user to confirm or provide a logo.

## Step 6: Select the Template and Create the Marq Project

Use the Marq MCP for every operation in this step. If it is unavailable, stop and ask the user to install and connect it.

1. Read [references/template-map.json](references/template-map.json) and select the template ID matching `industry`. Use `generic` only when the industry is `generic` or not listed.
2. If the selected template ID is empty, stop and ask for the approved template ID. Do not guess or use an unapproved template.
3. Before creating anything in Marq, show the user a concise preview containing the prospect, selected Gong call, industry, selected template, and all proposed MAP content. Ask for explicit confirmation to create one internal test project. Do not create a project until the user approves. One approval authorizes only one project creation attempt for the current run; ask again before any retry or additional project.
4. After approval, call `document_CreateProjectFromTemplate` exactly once with the selected template ID. Name the project `[TEST] MAP - <company name> - <YYYY-MM-DD>`.
5. Confirm the creation response contains a new project ID and that it is different from the source template ID. If the new project identity is missing, ambiguous, or matches the template ID, stop without making any content writes.
6. Do not edit, rename, delete, or otherwise modify the source template. The new project must belong to the authenticated Marq user.
7. Save the template ID, verified new project ID, project URL, and project name under `marq` in the JSON.

## Step 7: Apply the MAP Personalization

Use the Marq MCP and target only the verified new project created in Step 6. Never pass the source template ID to a content-writing tool.

1. Call `dmes_GetSmartFields` before writing.
2. Confirm every key in `marq_fields` exists as a project text smart field and that `company logo` exists as a project image smart field. If any field is missing or has the wrong type, stop and report it; do not fall back to direct block edits or dataset-field writes. In particular, a legacy dataset image field named `logo_dark` does not satisfy the required `company logo` project image field.
3. Call `dmes_ApplyProjectSmartFields` with all 18 text values and one image value. For the logo entry, use `{ "name": "company logo", "dataType": "image", "value": <logo.source_url> }`. Marq uploads the external image URL into the project.
4. Apply the values in one batch or serially. Never make parallel writes to the same project, and do not modify unrelated fields, blocks, slides, datasets, or the source template.
5. Read back all 18 text smart fields and `company logo`. Confirm the text rendered with its formulas attached and the image field remains bound to `company logo` rather than `logo_dark`.
6. Visually confirm that the logo renders in the intended cover-slide image block without distortion, clipping, a broken-image placeholder, or a visible `{{logo_dark}}` placeholder. Report any overflow or binding warning and do not mark the MAP complete until the readback passes.
