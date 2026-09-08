# Marq market, persona, use-case, and proof guide

Use this as planning guidance, not a license to make buyer claims. Product details, packaging, integrations, security, and metrics can change; validate buyer-facing claims against the current linked source or an approved internal source.

## High-fit account pattern

Current Marq positioning is strongest where several of these conditions coexist:

- Mid-market or enterprise scale.
- Distributed content creation across departments, locations, agents, branches, campuses, franchises, partners, or brands.
- A central brand/creative team that must enable non-designers without losing control.
- Recurring, localized, personalized, or data-driven collateral.
- Repetitive low-complexity requests that consume creative capacity.
- Brand, legal, accessibility, or regulatory governance requirements.
- Fragmented templates/assets or version-control problems.
- Need to connect templates with CRM, DAM, data, approval, print, or distribution workflows.

Industry is a prioritization signal, not the ICP by itself. Marq's own 2026 guidance says the platform can be more than a solo creator or very small centralized team needs. Do not disqualify solely by employee count; qualify workflow scale, number of creators/users, recurrence, governance, economic impact, and adoption readiness.

## Common industry patterns

- **Higher education:** distributed campus clients, admissions and event collateral, school/department autonomy, accessibility, small central creative teams, brand governance.
- **Healthcare:** multi-location/local outreach, growth or acquisition complexity, current approved assets, provider/service/location collateral, creative-request volume, regulated review. Do not claim HIPAA relevance unless the actual workflow handles protected information and Marq's approved security guidance supports the claim.
- **Financial services and insurance:** agents/branches/entities, personalized proposals and local materials, approved disclosures, audit and approval needs, CRM/data population.
- **Real estate:** agent and brokerage co-branding, listing collateral, MLS/data population, print, local speed, many non-designer creators.
- **Franchise and multi-location:** local marketing within corporate guardrails, recurring location-specific content, permissions, approvals, brand kits, print/distribution.
- **Associations and membership networks:** chapters/affiliates, distributed newsletters and event collateral, central standards with local customization.
- **Manufacturing/product organizations:** product sheets, catalogs, distributor/localization needs, PIM or other product-data automation, controlled specifications.

## Personas and likely interests

These are hypotheses to validate, not facts derived from a title.

| Persona | Likely interests | Useful discovery focus | Common concern/blocker |
|---|---|---|---|
| CMO / VP Marketing | scale, speed, brand performance, resource allocation, risk | strategic impact, cross-functional scope, investment priority, success measures | competing initiatives, unclear business case |
| Brand leader | consistency, governance, multi-brand control, adoption | where brand breaks, who creates, permissions, enforcement, visibility | fear of lost control or weak adoption |
| Creative director / design leader | request backlog, quality, workflow, strategic capacity | request types/volume, handoffs, recurring work, template governance | implementation lift, design fidelity, change management |
| Marketing operations | systems, data, automation, approvals, analytics | source systems, workflow triggers, ownership, error/rework, measurement | integration feasibility, data quality, admin burden |
| Sales enablement / revenue operations | seller speed, approved collateral, CRM workflow, usage | content moments in sales process, personalization, CRM fields, adoption | seller behavior, overlap with existing tools |
| Field/local/franchise/campus marketing | speed, autonomy, relevance, ease of use | current workaround, turnaround, local variation, approval friction | another login, training, insufficient flexibility |
| IT / security / data | architecture, identity, permissions, API, risk | systems of record, authentication, data flows, support ownership | security, maintenance, roadmap dependencies |
| Procurement / finance | value, scope, terms, consolidation, risk | validated value inputs, alternatives, usage scope, commercial process | price-to-scale mismatch, duplicate spend |
| Partner executive / alliances | joint value, target market, revenue model, effort | customer overlap, differentiated use case, referrals/resale, ownership | unclear demand, channel conflict, enablement cost |

Economic buyer candidates commonly include the executive who owns marketing/brand/creative operations, a business-unit leader funding the workflow, or an operations/technology executive sponsoring automation. Do not infer economic authority from seniority alone. Ask who owns the outcome and budget decision.

Influencers may include designers, brand managers, admins, sales enablement, local marketers, end users, implementation, and customer success. Blockers may include IT/security, procurement, existing-tool owners, change-management leaders, under-resourced admins, or end users who reject a constrained workflow. The same stakeholder may be both influencer and blocker.

## Problem -> root cause -> capability hypotheses

| Business problem pattern | Root causes to test | Relevant Marq capabilities to validate |
|---|---|---|
| Creative team is buried in small requests | centralized creation, no reusable governed templates, manual handoffs | brand templates, granular locking, shared libraries, approvals, collaboration |
| Off-brand or outdated content appears | fragmented assets/templates, no permissions/version controls, user workarounds | brand kits/assets, locked elements, permissions, centralized template management |
| Local teams cannot move quickly | every change requires central design, tools are too complex, approval bottleneck | simplified templated self-service, editable fields, groups/roles, approvals |
| Personalized collateral is slow or error-prone | copy/paste, disconnected CRM/data, manual calculations | smart fields, connected data, APIs, CRM/template automation where currently supported |
| Multi-location or multi-brand content does not scale | duplicated masters, local variation, inconsistent access | brand mapping/kits, group permissions, reusable templates, localized data |
| Content-to-print/distribution is fragmented | separate ordering, export, vendor, and approval steps | print integrations, export/publishing, approvals, workflow/API connections where supported |
| Product/spec content is manually maintained | disconnected PIM/product data and document generation | APIs, data-backed smart fields, automated project creation; confirm exact integration path |

Do not position a capability until the buyer validates the corresponding problem or desired outcome.

## Current proof library

Prefer the most analogous verified problem pattern. Quote or use metrics only with a source and context.

- **PT Solutions (healthcare, current 2026 case study):** 550 clinics across 25 states; 300+ recurring creative requests per month before the new system; Marq templating with MediaValet enabled 300+ self-served projects monthly and reduced flyer turnaround from 2–4 weeks to same day. Use for distributed clinics, local collateral, DAM + templating, brand-safe self-service, and creative capacity. Source: https://www.marq.com/customers/case-studies/pt-solutions/
- **Western Colorado University:** a small creative team serving campus clients faced 2–3 week waits for smaller requests; branded templates, approvals, and collaborative editing enabled non-designers to self-serve and freed the team for larger work. Use for higher education workflow and governance; avoid implying the result applies automatically to a larger institution. Source: https://www.marq.com/customers/case-studies/western-colorado-university/
- **Reinhart Realtors:** 160 admins and agents used locked templates and shared brand assets; the case study reports an estimated two hours saved per user per week. Use only as customer-reported real-estate evidence and retain the estimation context. Source: https://www.marq.com/customers/case-studies/realtors/
- **National Association of Home Builders:** central designers created locked newsletter templates for a distributed federation representing more than 140,000 members, enabling local customization with a consistent national brand. Use for associations/chapters and distributed newsletters. Source: https://www.marq.com/customers/case-studies/national-association-of-home-builders/

The repository's broad aggregate ROI claims and uncited customer metrics are not approved proof merely because they appear in `marq-comprehensive-guide.md`. Verify against current customer pages or approved internal collateral before use.

## Current platform positioning

Current public sources support these broad capability families:

- Import or create content and convert it into governed brand templates.
- Lock critical template elements and control editable areas.
- Use brand assets, permissions, groups, and smart fields for governed personalization.
- Connect custom data sources and supported systems through integrations and APIs.
- Centralize templates, images, and projects.
- Collaborate and apply configurable approval workflows.
- Support digital sharing, export, social publishing, and print workflows where configured.

Primary sources:

- Platform overview: https://www.marq.com/pages/platform/
- Brand templating help: https://help.marq.com/intro-to-brand-templating
- Developer concepts: https://developers.marq.com/docs/brand-templates-concept
- Approvals: https://developers.marq.com/docs/approvals-concept
- Content automation: https://developers.marq.com/docs/content-automation

Do not promise a particular import type, integration, export, AI feature, security certification, implementation package, user minimum, or price without current approved confirmation.

## Common objections and the discovery behind them

- **"We already use Canva/Adobe/PowerPoint."** Determine whether the issue is creation quality or governed distribution, repeatability, data, approvals, and non-designer self-service. Marq may complement creative tools; do not create a false rip-and-replace choice.
- **"We have a DAM."** Determine whether users can activate approved assets into governed, editable collateral. A DAM and templating layer can be complementary.
- **"We can do this manually."** Test frequency, volume, time, error, opportunity cost, and whether the manual process is actually a priority to change.
- **"Another login will hurt adoption."** Understand user sophistication, current destination workflow, identity/integration options, training ownership, and whether the benefit is large enough to change behavior.
- **"Implementation is too much work."** Identify template count, source formats, data readiness, admin ownership, rollout cohort, and internal change capacity before discussing services or timeline.
- **"The price is too high."** Do not defend price reflexively. Compare the required scope and verified value to alternatives. If workflow maturity, adoption, or economic impact cannot support the commercial model, `not qualified/not now` is correct.
- **"We need more flexibility."** Identify which elements/users require freedom and which require governance. Excessive locking can drive users outside the system.

## Competitive alternatives

Alternatives include doing nothing; central design service; freelancers/agencies; editable PDFs; shared drives/SharePoint; PowerPoint/Word/Publisher; Adobe Express/Creative Cloud; Canva; a DAM alone; a print portal; homegrown templates or workflow automation; and other enterprise brand-template or content-automation platforms.

Ask what the buyer is comparing, why, and what decision criteria matter. Do not make unsupported competitor claims. The most important competitor is often the acceptable manual process, not another vendor.
