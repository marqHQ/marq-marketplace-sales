#!/usr/bin/env python3
"""Deterministically validate a MAP analysis JSON before Marq creation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


TEXT_FIELDS = [
    *(f"challenge {i} {part}" for i in range(1, 4) for part in ("title", "summary", "quote")),
    *(f"solution {i} {part}" for i in range(1, 4) for part in ("title", "summary", "outcome")),
]
QUOTE_FIELDS = [f"challenge {i} quote" for i in range(1, 4)]
SOURCE_FIELDS = {
    "source_id",
    "title",
    "date",
    "source_url",
    "meeting_host",
    "transcript_source",
    "participants",
    "full_transcript",
    "selection_reason",
    "evidence_role",
}


def words(value: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", value, flags=re.UNICODE))


def require_object(value: object, path: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    return value


def load_budgets(template_id: object) -> dict:
    path = Path(__file__).resolve().parent.parent / "references" / "template-copy-budgets.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("templates", {}).get(str(template_id), payload["default"])


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read valid JSON: {exc}"]

    if not isinstance(payload, dict):
        return ["root must be an object"]

    required_top = {
        "prospect",
        "evidence_sources",
        "evidence_coverage",
        "industry",
        "logo",
        "marq",
        "review",
        "qa",
        "page_automation",
        "marq_fields",
        "quote_evidence",
    }
    missing_top = sorted(required_top - payload.keys())
    if missing_top:
        errors.append(f"missing top-level fields: {', '.join(missing_top)}")

    coverage = require_object(payload.get("evidence_coverage"), "evidence_coverage", errors)
    status = coverage.get("status")
    if status not in {"ready", "insufficient_evidence", "needs_user_decision"}:
        errors.append("evidence_coverage.status is invalid")
    availability = coverage.get("availability_status")
    if availability not in {
        "transcript_ready",
        "no_meeting_found",
        "meeting_without_transcript",
        "transcript_insufficient",
    }:
        errors.append("evidence_coverage.availability_status is invalid")
    confirmed = coverage.get("confirmed_challenges")
    if not isinstance(confirmed, int) or isinstance(confirmed, bool) or not 0 <= confirmed <= 3:
        errors.append("evidence_coverage.confirmed_challenges must be an integer from 0 to 3")
    if coverage.get("required_challenges") != 3:
        errors.append("evidence_coverage.required_challenges must equal 3")
    sources_reviewed = coverage.get("sources_reviewed")
    if not isinstance(sources_reviewed, list) or not all(isinstance(item, str) for item in sources_reviewed):
        errors.append("evidence_coverage.sources_reviewed must contain source ID strings only")
    if status == "ready" and confirmed != 3:
        errors.append("ready coverage requires exactly 3 confirmed challenges")
    if status == "ready" and availability != "transcript_ready":
        errors.append("ready coverage requires transcript_ready availability")
    if status == "ready" and not sources_reviewed:
        errors.append("ready coverage requires at least one reviewed source")
    if availability in {"no_meeting_found", "meeting_without_transcript"} and status != "needs_user_decision":
        errors.append("a missing transcript requires needs_user_decision")

    evidence_sources = payload.get("evidence_sources")
    if not isinstance(evidence_sources, list):
        errors.append("evidence_sources must be an array")
        evidence_sources = []
    source_ids: set[str] = set()
    for index, source in enumerate(evidence_sources):
        if not isinstance(source, dict):
            errors.append(f"evidence_sources[{index}] must be an object")
            continue
        missing = sorted(SOURCE_FIELDS - source.keys())
        if missing:
            errors.append(f"evidence_sources[{index}] missing: {', '.join(missing)}")
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id.strip():
            errors.append(f"evidence_sources[{index}].source_id must be a non-empty string")
        else:
            if source_id in source_ids:
                errors.append(f"evidence_sources[{index}].source_id is duplicated")
            source_ids.add(source_id)
        transcript = source.get("full_transcript")
        if not isinstance(transcript, str) or not transcript.strip():
            errors.append(f"evidence_sources[{index}].full_transcript must be a non-empty string")
        participants = source.get("participants")
        if not isinstance(participants, list) or not participants:
            errors.append(f"evidence_sources[{index}].participants must be a non-empty array")
        if source.get("meeting_host") not in {"marq", "partner", "customer", "unknown"}:
            errors.append(f"evidence_sources[{index}].meeting_host is invalid")
        if source.get("transcript_source") not in {"gong", "uploaded", "pasted", "linked"}:
            errors.append(f"evidence_sources[{index}].transcript_source is invalid")
    if status == "ready" and not evidence_sources:
        errors.append("ready coverage requires at least one usable evidence source")
    if isinstance(sources_reviewed, list):
        unknown = sorted(set(item for item in sources_reviewed if isinstance(item, str)) - source_ids)
        if unknown:
            errors.append(f"sources_reviewed contains unknown source IDs: {', '.join(unknown)}")

    fields = require_object(payload.get("marq_fields"), "marq_fields", errors)
    missing_fields = [name for name in TEXT_FIELDS if name not in fields]
    extra_fields = sorted(set(fields) - set(TEXT_FIELDS))
    if missing_fields:
        errors.append(f"marq_fields missing: {', '.join(missing_fields)}")
    if extra_fields:
        errors.append(f"marq_fields has unexpected keys: {', '.join(extra_fields)}")
    for name in TEXT_FIELDS:
        if name in fields and not isinstance(fields[name], str):
            errors.append(f"marq_fields.{name} must be a string")

    marq = require_object(payload.get("marq"), "marq", errors)
    budgets = load_budgets(marq.get("template_id"))
    for i in range(1, 4):
        checks = (
            (f"challenge {i} title", None, budgets["challenge_title_max_words"], budgets["challenge_title_max_characters"]),
            (f"challenge {i} summary", budgets["challenge_summary_min_words"], budgets["challenge_summary_max_words"], None),
            (f"challenge {i} quote", budgets["challenge_quote_min_words"], budgets["challenge_quote_max_words"], None),
            (f"solution {i} title", None, budgets["solution_title_max_words"], budgets["solution_title_max_characters"]),
            (f"solution {i} summary", budgets["solution_summary_min_words"], budgets["solution_summary_max_words"], None),
            (f"solution {i} outcome", budgets["solution_outcome_min_words"], budgets["solution_outcome_max_words"], None),
        )
        for name, minimum, maximum, max_chars in checks:
            value = fields.get(name, "")
            if not isinstance(value, str) or not value.strip():
                if status == "ready":
                    errors.append(f"marq_fields.{name} is required when coverage is ready")
                continue
            count = words(value)
            if minimum is not None and count < minimum:
                errors.append(f"marq_fields.{name} has {count} words; minimum is {minimum}")
            if count > maximum:
                errors.append(f"marq_fields.{name} has {count} words; maximum is {maximum}")
            if max_chars is not None and len(value) > max_chars:
                errors.append(f"marq_fields.{name} has {len(value)} characters; maximum is {max_chars}")

    quote_evidence = require_object(payload.get("quote_evidence"), "quote_evidence", errors)
    for name in QUOTE_FIELDS:
        evidence = require_object(quote_evidence.get(name), f"quote_evidence.{name}", errors)
        if status != "ready" and not fields.get(name):
            continue
        for key in (
            "source_id",
            "source_title",
            "source_date",
            "source_url",
            "meeting_host",
            "transcript_source",
            "speaker",
            "timestamp",
            "transcript_excerpt",
            "presentation_edits",
            "reported_speech",
        ):
            if key not in evidence:
                errors.append(f"quote_evidence.{name} missing {key}")
        source_id = evidence.get("source_id")
        if not isinstance(source_id, str) or source_id not in source_ids:
            errors.append(f"quote_evidence.{name}.source_id is not in evidence_sources")
        if isinstance(sources_reviewed, list) and source_id not in sources_reviewed:
            errors.append(f"quote_evidence.{name}.source_id is not in sources_reviewed")
        for key in ("speaker", "transcript_excerpt"):
            value = evidence.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"quote_evidence.{name}.{key} must be a non-empty string")
        matching_source = next((source for source in evidence_sources
                                if isinstance(source, dict) and source.get("source_id") == source_id), None)
        excerpt = evidence.get("transcript_excerpt")
        transcript = matching_source.get("full_transcript") if matching_source else None
        if isinstance(excerpt, str) and excerpt.strip() and isinstance(transcript, str) and excerpt not in transcript:
            errors.append(f"quote_evidence.{name}.transcript_excerpt is not contiguous in its source transcript")
        if not isinstance(evidence.get("presentation_edits"), list):
            errors.append(f"quote_evidence.{name}.presentation_edits must be an array")
        if not isinstance(evidence.get("reported_speech"), bool):
            errors.append(f"quote_evidence.{name}.reported_speech must be boolean")

    review = require_object(payload.get("review"), "review", errors)
    review_status = review.get("status")
    if review_status not in {"pending", "PASS_READY", "PASS_INSUFFICIENT", "needs_correction"}:
        errors.append("review.status is invalid")
    if review_status == "PASS_READY" and status != "ready":
        errors.append("PASS_READY requires ready evidence coverage")
    if review_status == "PASS_INSUFFICIENT" and status != "insufficient_evidence":
        errors.append("PASS_INSUFFICIENT requires insufficient_evidence coverage")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_map.py <analysis.json>", file=sys.stderr)
        return 2
    errors = validate(Path(sys.argv[1]))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MAP analysis JSON is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
