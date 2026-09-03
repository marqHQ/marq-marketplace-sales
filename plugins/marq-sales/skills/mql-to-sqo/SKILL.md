---
name: mql-to-sqo
description: Convert an existing HubSpot deal from MQL to SQO in the appropriate AE pipeline, use matched Gong transcripts to propose evidence-backed required qualification fields, add rep-specified product-library line items, and synchronize and verify the deal amount. Use when a rep identifies a HubSpot deal by link, deal ID, deal name, or company name and asks to qualify, convert, promote, or build the deal with specific products, quantities, pricing, ownership, or development-rep details.
---

# Convert a HubSpot MQL to an SQO

Convert the existing deal in place. Do not create a duplicate deal.

## Required input

Require one deal locator before beginning: a HubSpot deal-record link, deal ID, deal name, or company name. If the user supplies a deal or company name, search HubSpot and confirm the resolved deal instead of requiring a URL.

Also obtain the line-item instructions before proposing changes:

- Product or line-item name
- Quantity
- Any explicit price, discount, term, or billing-frequency instruction

Use the current HubSpot product-library price when no override is requested, but expose that price in the approval proposal. Never infer or invent a discount.

## Use the right surfaces

Use the HubSpot connector for record lookup, property discovery, semantic writes it supports, and final verification. Follow the installed HubSpot skill, including its initial user-details check and write-approval requirements.

Use `search_gong_calls` and `get_gong_transcript` when available to resolve missing SQO qualification fields before asking the rep. Read [references/gong-field-inference.md](references/gong-field-inference.md) before using transcript evidence. Gong enrichment proposes values but never authorizes CRM writes or replaces the required line-item instructions.

Use the browser only for HubSpot UI operations that the connector cannot complete reliably, especially rebuilding line items and selecting **Update deal amount**. Before browser work, follow the installed in-app Browser skill and its connector-first routing rule.

Read [references/browser-line-items.md](references/browser-line-items.md) before editing line items in the HubSpot UI.

## Workflow

### 1. Resolve and inspect the exact deal

1. Call HubSpot user details and confirm deal, product, and line-item access.
2. Resolve the supplied locator:
   - For a HubSpot deal URL or deal ID, extract the ID and fetch that exact record.
   - For a deal name, search the authenticated rep's accessible HubSpot deals by deal name.
   - For a company name, search HubSpot companies by company name, resolve the exact company, and retrieve its associated deals.
   - Page through all search results. If the connector cannot establish that the result set is complete, treat the result as ambiguous.
3. Compare candidate deal name, company, owner, pipeline, stage, and other available context:
   - If there is one clear match, show its deal name, ID, company, owner, pipeline, stage, and clickable HubSpot URL, then ask the user to confirm it. Do not require the user to provide the URL.
   - If there are multiple plausible matches, list the candidates with those identifying details and ask the user to choose.
   - If there is no plausible match, ask for a more specific identifier or the HubSpot deal-record link.
4. After confirmation, fetch the resolved deal by ID.
5. Inspect:
   - Deal name, pipeline, and stage
   - Deal owner and development rep
   - Associated contact and company
   - Current close date and qualification fields
   - Existing line items
   - Amount, TCV, ACV, and ARR when available
6. Include the clickable HubSpot deal URL when reporting the resolved record.

Treat a mismatch between the resolved record and the rep's description as a blocker. Do not silently act on a similarly named deal.

### 2. Discover portal-specific fields and values

Do not hardcode pipeline, stage, or qualification-field internal values. Use HubSpot property discovery to identify:

- The AE pipeline and sales-qualified-opportunity stage
- Required properties for moving into that stage
- Valid enumeration values
- Owner and development-rep identifiers

Preserve existing user-entered values unless the rep explicitly approves replacing them. Before asking the rep for missing qualification facts, run the Gong enrichment step below. Ask only for facts that cannot be supported confidently by the deal, its associations, or a matched transcript.

### 2.5 Enrich required fields from Gong

1. Search Gong for calls with transcripts using the associated company, contact email or participant, deal owner, and a narrow date range around the initial demo or discovery activity.
2. Match calls to the exact deal using the rules in [references/gong-field-inference.md](references/gong-field-inference.md). Stop on an ambiguous match rather than borrowing evidence from a similarly named account or another opportunity.
3. Fetch the strongest matching transcript and any additional clearly matched discovery or demo transcript needed to cover the required fields.
4. Infer only missing required fields, constrained to the valid HubSpot values discovered in Step 2. Do not infer `No`, `None`, or another negative value from silence.
5. Record the Gong call ID and link, call date, evidence summary or short excerpt with timestamp when available, and confidence for every proposed value.
6. Propose high-confidence values in the approval package. Ask the rep to resolve medium-confidence, conflicting, or missing values. Do not propose low-confidence values.
7. Preserve existing HubSpot values. Transcript evidence may support a proposed replacement only when the approval explicitly shows the existing and proposed values.

If the Gong tools are unavailable or no exact call can be matched, continue without transcript enrichment and ask the rep for the missing required facts.

### 3. Resolve products and calculate the proposal

Resolve every requested item against the HubSpot product library. Stop on an ambiguous or missing match.

For each product, show:

- Exact catalog product name and product ID
- Quantity
- Unit list price
- Any requested override or discount
- Billing frequency or term
- Extended amount

Calculate the proposed deal amount from the complete intended line-item set. Distinguish one-time and recurring revenue so TCV, ACV, and ARR are not incorrectly treated as interchangeable.

### 4. Obtain approval before any write

Present one consolidated proposal covering:

| Object | ID | Field or line item | Current value | Proposed value |
|---|---:|---|---|---|

For transcript-derived values, precede the change table with:

| Proposed field | Proposed value | Gong source | Evidence | Confidence |
|---|---|---|---|---|

Use concise evidence and include the Gong call link. Make clear which values came from HubSpot, Gong, or the rep.

Explicitly disclose:

- Target pipeline and stage
- Owner and development rep changes, if any
- Required qualification-field changes
- Every line item, quantity, price, billing frequency, and amount
- Expected total deal amount
- Whether existing line items will be removed and rebuilt
- That rebuilding replaces the line-item record IDs

Do not change the CRM until the user approves the exact proposal. Treat approval of a materially different proposal as insufficient.

### 5. Update the opportunity fields

Use the HubSpot connector for supported field updates. Move the resolved deal—not a new record—into the approved AE pipeline and stage, and apply only the approved qualification, owner, development-rep, and close-date changes.

If HubSpot rejects the stage change because fields are required, discover the missing fields and obtain values from existing evidence or the user. Do not guess.

### 6. Build the approved line-item set

Use the HubSpot line-item editor in the browser when the UI is required to synchronize the deal amount.

If existing line items must be removed to surface HubSpot's amount-update prompt, delete them only after the approval explicitly covers removal and rebuilding. Recreate the complete intended set from the product library; do not rebuild only the newly requested additions.

Follow [references/browser-line-items.md](references/browser-line-items.md) for the detailed UI sequence and recovery rules.

### 7. Synchronize the deal amount

After saving the complete line-item set, select **Update deal amount** in HubSpot's confirmation prompt. Confirm that the amount shown in the prompt matches the calculated proposal before accepting it.

If the prompt does not appear, do not claim success. Reopen the editor, verify that the intended complete set was saved, and use the recovery path in the browser reference.

### 8. Verify independently

Re-read the deal and its associated line items through the HubSpot connector. Verify:

- Exact deal ID and URL
- Pipeline and sales-qualified stage
- Owner and development rep
- Required qualification fields
- Product IDs, names, quantities, unit prices, discounts, and billing frequencies
- Extended amount for every line item
- Sum of line-item amounts
- Deal amount
- TCV, ACV, and ARR when available

Do not rely only on a browser success banner. If any value is stale or inconsistent, report the discrepancy and continue only within the already approved scope.

## Completion report

Report:

- The resolved deal and final pipeline/stage
- Final owner and development rep
- A concise line-item table
- Final deal amount and available revenue metrics
- Whether line-item IDs were replaced
- Any partial failure or remaining manual action

Never report the conversion as complete unless the final connector read confirms the intended line items and deal amount.
