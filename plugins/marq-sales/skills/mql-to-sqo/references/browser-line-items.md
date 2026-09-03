# MQL-to-SQO Browser Line-Item Workflow

Read this reference only when the HubSpot UI is needed to add or rebuild line items and synchronize the deal amount.

## Preconditions

- Confirm that the browser is signed into the same HubSpot portal as the deal link.
- Confirm the deal ID in the URL.
- Retain the approved complete intended line-item set, not just the incremental additions.
- Do not remove existing items unless the approval explicitly covers removal and rebuilding.

## Rebuild sequence

1. Open the supplied deal URL.
2. Open the line-item editor from the deal.
3. Compare the visible existing items with the approved proposal.
4. When rebuilding is required, remove every existing line item.
5. Add every approved product from the HubSpot product library.
6. Set each approved quantity, price or discount, billing frequency, and term.
7. Move focus out of edited numeric fields so HubSpot recalculates extended totals.
8. Compare every visible row and the total with the approved proposal.
9. Save the line items.
10. In the **Update deal amount?** prompt, verify the displayed amount.
11. Select **Update deal amount** only when it matches the approved amount.

## Recovery rules

### The amount prompt does not appear

Reopen the line-item editor and confirm the complete item set saved. If the deal already contained the items, HubSpot may not treat the edit as a rebuild. With explicit approval, remove the complete set, save or continue as the interface requires, then add the complete approved set again and save.

Do not directly overwrite the amount through an unsupported field mutation merely to bypass the UI workflow.

### Quantity or total does not recalculate

Move focus out of the field, press the interface's apply control if present, and wait for the row total to refresh. Do not save while the visible extended amount is stale.

### Product selector is ambiguous

Match the product-library record by exact name and confirm its catalog price or product ID. Stop rather than selecting a near match.

### A checkbox or row control is difficult to select

Use the browser's inspected interactive state and target the control associated with the exact product row. Reinspect after every structural change because row positions can change.

### Authentication expires

Ask the user to sign in in the selected browser and tell you when it is ready. Resume from a fresh inspection of the deal and line-item editor.

### Save partially succeeds

Do not repeat deletions blindly. Inspect the current UI state and then re-read the associated line items through the HubSpot connector. Reconcile the actual state against the approved complete set before taking another write action.

## Final verification

After accepting **Update deal amount**, use the HubSpot connector to re-read both the deal and its line items. Treat the browser confirmation as provisional until the connector confirms the saved records and synchronized amount.
