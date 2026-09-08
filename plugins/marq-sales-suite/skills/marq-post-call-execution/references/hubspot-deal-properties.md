# HubSpot Deal Property Discovery and Mapping

HubSpot configuration is mutable. Discover live object availability, property names, types, pipeline stages, and allowed enum values on every execution. Historical portal observations are not runtime authority. This skill remains draft-only until the user approves an exact write set.

## Record resolution from a name

The rep may supply a deal name or an account/company name. Do not ask them to retrieve a HubSpot link when a name is available.

1. Call HubSpot user-details and verify COMPANY and DEAL read availability.
2. If a HubSpot URL or record ID was supplied voluntarily, retrieve that record directly.
3. Otherwise, discover the deal properties representing name, pipeline, stage, owner, amount, currency, and close date, then search DEAL records by the supplied name with those properties.
4. Also discover the company properties representing company name and domain, then search COMPANY records when the input could be an account name. For each plausible company match, search its associated DEAL records using the company object ID rather than relying only on text matching.
5. Match names case-insensitively and tolerate ordinary punctuation or legal-suffix differences, but do not treat a fuzzy match as uniquely resolved when another plausible result exists.
6. Continue automatically when there is one clear deal match, or when there is one clear company match with exactly one plausible associated deal. Read that deal's associated company, contacts, and relevant recent activities.
7. When multiple plausible deals remain, stop before analysis and show a compact choice table containing deal name, account, pipeline, stage, owner, amount/currency, close date, and clickable HubSpot URL. Ask the rep to choose; never select based only on newest activity, highest amount, or closest close date.
8. When a company is found but no associated deal exists, return the clickable company record, state that no deal was found, and continue without deal-level CRM context. Do not create a deal unless the user explicitly requests it and separately approves the write.
9. When neither a deal nor company can be found, state the search term and result count, then continue transcript-only if possible. Ask for a clarifying identifier such as domain or owner only when it is needed to distinguish or locate the record—not for a HubSpot link.

Record lookup is read-only and requires no approval. Always include the resolved clickable HubSpot URL with the tracking parameters required by the HubSpot workflow. State whether the match was direct by deal name or resolved through a company association.

## Live V1 mapping procedure

Search the live DEAL schema for the following concepts. Fetch the full definitions for the best matches and record each selected internal name, label, type, description, and allowed values before proposing changes.

| Qualification concept | Property concepts to discover | V1 use |
|---|---|---|
| Situation/current state | sales notes, call notes, deal notes | Put concise evidence-tagged current-state detail in the portal's appropriate narrative field. |
| Pain | pain point, customer challenges | Use customer-supported narrative and only live category options supported by customer evidence. |
| Business impact | value proposition, business impact | Use only a supported top-level outcome; retain detailed impact in the appropriate narrative field when no dedicated property exists. |
| Critical event | expected rollout date, critical event | Use only when the customer establishes a real event/date. Do not substitute the forecast close date. |
| Decision process and criteria | decision process, decision criteria, sales notes | Use dedicated live fields when they exist; otherwise keep evidence-tagged detail in the selected narrative field. |
| Authority, champion, economic buyer | authority, champion, economic buyer | Record only established roles and authority evidence. Keep gaps explicit. |
| End users | end users | Select only supported live enum values. |
| Competition | primary competitor, competitor write-in | Distinguish unknown from customer-confirmed no competition. Use a write-in only when the live enum requires it. |
| Next step and date | next step, next-step date | Make the next step specific and preserve existing context by appending rather than replacing. Use only a supported exact date. |
| Forecast notes | forecast notes | Use only for forecast-specific context, not general call notes. |
| Close date, stage, amount, forecast | close date, pipeline/stage, amount/currency, forecast category | Guarded executive fields. Discover live definitions and values. Never infer changes from enthusiasm or meeting activity. |

Do not update computed or automated activity properties. Do not use an ambiguous field merely because its label sounds close. If no dedicated property exists, preserve the finding in the deliverable and state the schema gap rather than forcing it into an unrelated field.

## Live enum rules

- Fetch current enum values before proposing any enum-backed change.
- Read the deal's pipeline and validate that a proposed stage belongs to that pipeline and follows its live ordering.
- Pair any amount with the live currency-code property and never aggregate or compare raw cross-currency amounts.
- Preserve the stored value and human label in the proposal so the rep can audit what will be written.
- Treat a missing option as unavailable. Do not create a new option or substitute a near match.

## Proposal and approval format

The analysis table must contain:

| Object type | ID | Property | Label | Current value | Proposed value | Evidence class | Source | Rationale |
|---|---:|---|---|---|---|---|---|---|

Before an actual HubSpot write, reduce this to the exact confirmation table required by the HubSpot skill:

| Object Type | ID | Property | Current Value | New Value |
|---|---:|---|---|---|

Ask for approval after showing it. Batch at most ten objects. Do not overwrite user-entered narrative; append the dated addition and display the full resulting value. A user approving CRM writes does not approve an email send, and vice versa. After an approved write, independently re-read the changed properties and report any mismatch.
