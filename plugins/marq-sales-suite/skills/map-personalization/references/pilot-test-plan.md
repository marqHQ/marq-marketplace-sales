# Two-Week Sales Pilot

Use this plan for internal testing. Every generated project must retain the `[TEST]` prefix and must be reviewed by the rep before any external use.

## Tester Preflight

- HubSpot opens and returns the tester's user details, contacts, and associated companies.
- Marq Analytics can search Gong and read a complete transcript.
- Brandfetch can return a logo and the execution environment can download its credentialed asset URL.
- Marq Product can read the configured template, create a project, apply project and data smart fields, and export the result.
- All seven canonical template-map entries are present and non-empty; a null industry ID is treated as a stale-skill setup failure.
- The tester understands that optional and investment-page automation is inactive unless the run explicitly says otherwise.

Report a connection or permission failure as a setup failure, not a content-quality failure.

## Test Matrix

Across the pilot cohort, cover:

1. Each of the six named industries and the generic fallback.
2. A transcript longer than one retrieval chunk.
3. Multiple relevant calls in the current sales cycle.
4. Fewer than three defensible challenges.
5. A meeting with no transcript and an account with no matching meeting.
6. Ambiguous contacts or multiple participating stakeholders.
7. A missing, incorrect, low-contrast, or nontransparent logo.
8. Copy near every configured length limit.
9. A transient read failure and a partial smart-field write failure.
10. An account whose company row is absent from or ambiguous in the template's company dataset.

Do not force every rep to cover every case. Assign cases across two or three ordinary sales users rather than administrators.

## Capture for Every Run

- Tester and date
- Prospect/company and selected template
- Calls reviewed and evidence-coverage result
- Total elapsed time
- Whether the run completed, stopped safely, or created an incomplete project
- Manual corrections requested before approval
- Incorrect or weak customer evidence, if any
- Missing permissions or connections
- Raw placeholders, wrong company identity, logo problems, clipping, or overflow
- Wrong AE/customer names on the go-live timeline, an incorrect named implementation-manager assignment, a missing `CSM` fallback when assignment is unknown, incorrect training owners, or any SVG image fill
- Project URL and whether an orphaned or duplicate project was created
- Rep confidence rating and concise feedback

## Exit Criteria

The pilot is ready to expand only when:

- No source template was modified.
- No duplicate project was created after a failed creation response.
- Every completed project has the correct company identity, 18 reviewed text fields, resolved `customer lead name` and `account executive name`, a resolved `implementation manager name` containing the confirmed named owner or `CSM`, and verified PNG logo binding.
- No completed project contains a raw placeholder or visible clipping on in-scope pages.
- No completed project contains an SVG image fill.
- Every quote is traceable to a customer speaker and source.
- Insufficient or missing evidence stops before project creation.
- Standard sales-user permissions work without administrator intervention.
- Known unresolved out-of-scope template fields are disclosed and do not appear on customer-facing pages.
