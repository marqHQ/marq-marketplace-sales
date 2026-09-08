# Marq Post-Call Execution

## Team summary

Marq Post-Call Execution turns a completed customer call into the work that needs to happen afterward. It gives reps one consistent way to document the deal, evaluate qualification, plan the next move, prepare accurate HubSpot updates, and draft a customer follow-up—without turning assumptions into facts.

The goal is not to create more sales administration. The goal is to help a rep leave every meaningful call with a reliable deal record, a specific next step, and a customer-ready follow-up.

## What the rep provides

The rep supplies:

- the deal name or account name;
- the completed call transcript, notes, or both;
- any relevant context that is not captured in the call or CRM.

The rep does not need to find or paste a HubSpot link. The skill searches HubSpot and resolves the relevant record. If one account has several plausible deals, it shows the options and asks the rep to choose.

## What the skill does

1. Finds the appropriate HubSpot deal from the deal or account name.
2. Reads relevant deal, company, contact, and recent activity context.
3. Analyzes the call using SPICED qualification concepts without duplicating the separate call-coaching workflow.
4. Captures what the customer said, what the seller concluded, what CRM history supports, and what remains unknown.
5. Identifies stakeholders, customer commitments, Marq commitments, risks, objections, and qualification gaps.
6. Recommends a concrete next step with what, who, why, owner, and date.
7. Proposes exact HubSpot field changes using Marq's actual property names and allowed values.
8. Drafts a concise customer follow-up email grounded in the conversation.
9. Prepares focused questions and materials for the next call.

## What the rep receives

After each call, the rep receives:

- an executive call summary;
- customer priorities, pain, business impact, and desired future state;
- SPICED qualification findings and gaps;
- a stakeholder map;
- separate customer and Marq commitments;
- risks and objections;
- a recommended next step;
- proposed HubSpot changes;
- a draft customer email;
- next-call preparation items;
- a link to the HubSpot record used in the analysis.

## Evidence standard

Every important conclusion is classified as one of five things:

- Customer stated: explicitly said or agreed to by the customer.
- CRM supported: present in an identified HubSpot record or activity.
- Seller interpretation: the rep's conclusion without customer confirmation.
- Codex inference: a reasonable deduction that still requires validation.
- Unknown: not established by the available evidence.

This distinction matters. A reasonable interpretation is not the same as a customer-confirmed fact. The skill does not fabricate missing qualification, ROI, product claims, stakeholders, dates, pricing, or commitments.

## Approval and control

The default workflow is read-only and draft-only.

- Looking up and reading the HubSpot record does not require approval.
- The skill shows the exact proposed CRM changes before any write.
- The rep must approve CRM changes before they are made.
- The rep must separately approve any external communication before it is sent.
- Stage, amount, forecast category, and close date are never changed automatically.

## How this differs from SPICED Call Coach

SPICED Call Coach evaluates seller execution and provides coaching. Marq Post-Call Execution handles deal operations after the conversation. It uses compatible qualification concepts, but its job is to create an accurate operating record and move the deal forward—not grade the rep.

## Example request

“Run post-call execution for the Acme deal using this transcript.”

From there, the skill finds the HubSpot record, performs the analysis, and presents drafts and proposed changes for review.
