# Optional Pages and Investment Automation

This workflow is scaffolded but dormant. It must not change a MAP unless the activation gate below passes.

## Activation Gate

Activate only when `page-catalog.json` exists beside this file, parses as valid JSON, and contains an approved entry with `enabled: true` and a `template_id` that exactly matches the selected industry template.

If the file is missing, invalid, disabled, or has no exact template match:

- Set `page_automation.status` to `inactive_not_configured`.
- Leave the initialized `page_automation` metadata otherwise unchanged.
- Do not ask for commercial inputs.
- Do not select, add, remove, duplicate, reorder, or populate optional or investment pages. The standard protected-content baseline and SVG safety reads still cover the whole template and project; those reads do not activate page automation.
- Preserve the standard 18-field MAP creation and QA workflow exactly.

Never infer that the presence of page templates alone enables automation. Activation is an explicit configuration decision.

## Catalog Contract

The future catalog must have a top-level `schema_version` and one entry per supported industry template. Each template entry must contain:

- `template_id`: exact Marq template UUID
- `enabled`: explicit boolean activation flag
- `catalog_version`: version saved into run metadata
- `defaults`: approved platform and implementation defaults, if any
- `commercial_smart_fields`: mapping from the canonical commercial inputs and calculated outputs below to exact project smart-field names
- `core_pages`: pages that remain in every generated MAP
- `optional_pages`: approved customer-story, feature, integration, platform-detail, and implementation-detail pages
- `selection_limits`: maximum counts by optional page kind

Every page entry must contain:

- `page_key`: stable unique machine key
- `page_title`: stable unique Marq page title used to resolve the live page ID after project creation
- `source_mode`: `active_page` when the page already belongs in the project or `page_template` when it must be duplicated into the active sequence
- `kind`: `core`, `customer_story`, `feature`, `integration`, `platform_detail`, or `implementation_detail`
- `approved`: boolean content-approval status
- `selection_policy`: `always`, `default_industry`, `challenge_match`, `explicit_customer_interest`, or `rep_confirmed`
- `industries`: allowed industries
- `themes`: approved challenge or outcome tags
- `products_or_integrations`: approved product, feature, or integration tags
- `insertion_anchor`: another stable `page_key`, never a raw slide number or order value

Optional entries may include `priority`, `evidence_notes`, or a per-kind maximum. Do not place prices, discounts, page IDs from generated projects, or customer-specific values in the catalog.

Use stable page titles such as `MAP_STORY_JOHNS_HOPKINS`, `MAP_FEATURE_AI_AUTOMATION`, or `MAP_INTEGRATION_SALESFORCE`. Page numbers are not stable after optional pages are inserted.

## Selection Rules

Select pages only after the three challenge/solution pairs pass independent review.

1. Keep all approved `core` pages with `selection_policy: always`.
2. A `default_industry` customer story may be included for the matching industry without claiming that the prospect mentioned that customer.
3. Add at most one additional `challenge_match` customer story unless the catalog sets a lower limit. Require a strong match to at least one reviewed challenge or outcome and record the challenge key plus source IDs. Same-industry fit strengthens a match but does not replace thematic fit.
4. Add a `feature` or `integration` page only when an external customer participant explicitly expresses interest, asks a substantive question, describes a relevant workflow, or confirms a need. An AE demo, pitch, recap, or generic acknowledgement is insufficient.
5. Prefer no optional page over a weak match. Never add filler because a catalog entry exists.
6. Never rewrite an approved customer story, feature page, or integration page to manufacture a closer fit. Select it as approved or omit it.
7. Save selected and rejected candidates, selection reasons, source IDs, and insertion anchors under `page_automation`.

## Core Investment and Close-Plan Sequence

When configured as approved core pages, use semantic keys for this sequence rather than slide numbers:

1. `go_live_path`
2. `investment_how_it_works`
3. `abc_capacity_pricing`
4. `platform_plan_options`
5. `platform_enterprise`
6. `implementation_options`
7. `implementation_premium`
8. `investment_summary`
9. `mutual_next_steps`

Enterprise and Premium may be configured as rep-editable defaults. A default is a sales-workflow starting point, not a customer statement or model recommendation. Show it as a default in the preview and require rep confirmation before `page_automation.status` may become `approved_ready`.

Treat `go_live_path` as the broader implementation journey and `mutual_next_steps` as the immediate pre-signature action plan. Keep both only when their labels and content preserve that distinction.

## Commercial Input and Pricing Gate

Resolve known commercial values from approved connected sources when available, then ask one compact question for only the missing inputs. Required inputs for a customer-facing investment summary are:

- recommended platform plan
- seat count or approved custom-seat basis
- AI capacity tier
- implementation package
- target go-live date when the page displays one
- currency
- current approved pricing source and verification time
- any custom terms or discounts, explicitly supplied or confirmed by the rep

Call Marq Analytics `get_pricing_and_packaging` at runtime and use its current approved pricing and packaging document. Do not trust stale template text, transcript pricing, memory, or a value encoded only in this skill. Never invent or infer discounts, negotiated terms, implementation commitments, or custom pricing.

Implementation units must match that runtime source exactly. In the current model, Essentials, Standard, and Premium included scope is measured in pages; Partner included scope and the $1,000-per-100 overage are measured in templates. Do not normalize all packages to one unit based on visual consistency or rep assumption.

When an ABC capacity-pricing page is included, explain the subscribed total-capacity tier rather than presenting ABCs as individually purchased credits or a usage rate. The paid tier replaces the plan's included limit; it is not added on top. Show customer-facing tier increments and annual subscription price increments from the runtime source, not an internal per-ABC benchmark or an older named-tier ladder.

Calculate annual platform investment, one-time implementation, and first-year investment from the confirmed inputs. Keep included AI capacity separate from purchased capacity and do not double-count it. Record calculation inputs and results under `page_automation.commercial`.

If a required input, current pricing, or rep confirmation is missing:

- Keep `page_automation.status` at `needs_commercial_input` or `needs_rep_confirmation`.
- Show the missing items in the approval preview.
- Do not populate or create a customer-facing investment summary with plausible-looking placeholders.
- Do not silently fall back to Enterprise, Premium, a seat count, AI capacity, discount, date, or total.

## Approval Preview

When active, add these items to the ordinary MAP preview:

- each core page to retain
- each optional page to add or retain
- each catalog-managed page proposed for removal
- page kind, stable page key, and insertion anchor
- selection reason and supporting source IDs
- Enterprise, Premium, or other configured defaults clearly labeled as defaults
- resolved commercial inputs, calculated totals, pricing source status, and missing inputs

One explicit approval must cover the template, page set, commercial defaults or values, and one project creation attempt. A material page-set or recommendation change requires a new preview and approval.

## Project Operations

After creating the approved project and calling `dmes_GetSmartFields`:

1. Call `dmes_GetPages` with template pages included and resolve every approved catalog entry by exact `page_title`.
2. Stop on missing or duplicate matches. Do not guess by page order, visible copy, or similarity.
3. Retain entries whose `source_mode` is `active_page`, or duplicate entries whose `source_mode` is `page_template` with `dmes_CreatePage(sourcePageId)` at the configured semantic anchor.
4. Remove only unselected pages explicitly listed as catalog-managed. Never remove an unrelated page merely because it was not selected.
5. Apply commercial smart fields only after the commercial gate and approval pass.
6. Run structural edits serially or in one ordered batch. Partial application requires inspecting action results and retrying only failed actions after user approval when the resulting page set would differ materially.
7. Never modify the source template.

## QA

Read back the final page inventory and commercial smart fields, then export and inspect all added optional pages plus the investment summary and remaining next-step pages.

Confirm:

- every approved page appears exactly once unless the catalog explicitly permits otherwise
- every catalog-managed unselected page is absent
- semantic order matches the approved preview
- customer-story, feature, and integration pages remain unmodified approved content
- plan, seats, AI capacity, implementation package, pricing, dates, and totals are consistent across pages
- formulas remain attached and no raw placeholders or fallback copy are visible
- annual, one-time, and first-year calculations reconcile
- no page is clipped, truncated, duplicated unintentionally, or visually broken

Save results under `page_automation.qa`. Do not mark the MAP complete until all active checks pass.
