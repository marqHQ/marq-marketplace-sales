---
name: spiced-call-coach
description: Analyze B2B sales-call transcripts with the SPICED framework through an independent draft-and-audit workflow, then produce evidence-based, actionable coaching for a sales rep. Use when Codex is asked to review, score, coach, or audit a discovery call, demo/discovery call, follow-up sales call, Gong recording, or pasted sales transcript; identify Situation, Pain, Impact, Critical Event, and Decision coverage; critique seller execution; surface missed moments; or prepare a next-call coaching plan.
---

# SPICED Call Coach

Produce a transcript-grounded SPICED assessment through two independent sub-agents: one drafts the analysis and one audits it. Make the final editorial decisions in the primary agent so the audit improves the report without controlling it.

## Required reference

Read both references completely before every analysis:

- [references/analysis-prompt.md](references/analysis-prompt.md): drafting rubric, scoring anchors, and report structure.
- [references/audit-prompt.md](references/audit-prompt.md): independent accuracy and coaching-usefulness audit.

## Workflow

1. Resolve the call source in the primary agent.
   - Use a complete pasted or attached transcript when supplied.
   - For a Gong call ID or URL, use an authorized Gong transcript tool when available.
   - If the user identifies a call but does not provide its ID, search available Gong calls by the supplied participant, account, title, keyword, or date. Confirm a unique match before analyzing.
   - If no transcript source is accessible, ask the user for the transcript or call link.
2. Determine the seller, prospect/account, call type, opportunity stage, and prior-call context from supplied information or reliable metadata. Preserve uncertainty when a field is unavailable.
3. Prepare isolated artifact paths.
   - Create a unique temporary working directory when the user did not supply an output directory.
   - Use separate paths for `draft-analysis.md`, `audit.md`, and `final-analysis.md`.
   - When a long transcript exists only in conversation context, save a temporary transcript copy and pass its path. Pass a short transcript directly only when doing so is practical.
4. Spawn a fresh **analysis sub-agent** with no inherited conversation context when supported.
   - Give it only the call source, known call context, the absolute path to `references/analysis-prompt.md`, and the draft output path.
   - Instruct it to read the analysis prompt completely, retrieve or read the complete transcript, follow all continuation offsets, and write the full Markdown report to `draft-analysis.md`.
   - Do not give it expected scores, prior analyses, audit conclusions, or coaching answers.
5. Wait for the analysis sub-agent and confirm that `draft-analysis.md` exists and contains all required report sections.
6. Spawn a different fresh **audit sub-agent** with no inherited conversation context when supported.
   - Give it the same raw call source and context, `draft-analysis.md`, the absolute paths to both reference files, and the audit output path.
   - Instruct it to reread the complete transcript independently, read the draft and both references, apply `references/audit-prompt.md`, and write a concise audit to `audit.md`.
   - Do not provide suspected errors, preferred scores, or desired edits. The draft and raw source must be the audit evidence surface.
7. Wait for the audit sub-agent, then make the final editorial decision in the primary agent.
   - Read the complete draft and audit.
   - Verify disputed claims against transcript evidence before changing them.
   - Accept an audit recommendation only when it corrects a factual, evidentiary, arithmetic, or rubric error, or materially improves concise and actionable coaching.
   - Reject unsupported score preferences, stylistic churn, duplicated detail, generic advice, or edits that make the report less useful to the rep.
   - Apply accepted changes to `final-analysis.md`. The audit agent advises; it does not own the final report.
8. Verify the final analysis before delivery:
   - Every material claim is supported by transcript evidence or clearly labeled inference/metadata.
   - All five SPICED components use the reference's score anchors and coverage labels.
   - The arithmetic mean is correct to one decimal place.
   - Opportunity coverage and seller execution are separate judgments.
   - Replacement questions are singular and natural; urgency is not presupposed.
   - The report prioritizes actionable coaching over exhaustive criticism.
   - The coaching brief is tight, useful, and actionable for the rep.
   - No rejected audit suggestion leaked into the final report.
9. Return the final analysis in Markdown. If the user requested a path, place the final analysis there. Keep the draft and audit internal unless the user asks to see them; summarize material accepted edits only when useful.

If sub-agent orchestration is unavailable, say that the required independent draft-and-audit workflow cannot run. Do not silently replace it with a single-agent analysis.

## Scope

Use this skill across sellers, accounts, industries, and discovery-oriented sales calls. Calibrate coaching to the call type and stage. Do not assume that a first call should fully qualify the opportunity, and do not treat a scheduled demo as a reason to skip foundational discovery.
