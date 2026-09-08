#!/usr/bin/env python3
"""Check that the V1 acceptance pack covers its required call mix and guardrails."""

import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    fixture_path = Path(__file__).resolve().parents[1] / "tests" / "acceptance-cases.json"
    cases = json.loads(fixture_path.read_text(encoding="utf-8"))
    resolution_path = Path(__file__).resolve().parents[1] / "tests" / "record-resolution-cases.json"
    resolution_cases = json.loads(resolution_path.read_text(encoding="utf-8"))
    errors = []

    if len(cases) < 6:
        errors.append("fewer than six acceptance cases")

    kinds = Counter(case.get("call_type") for case in cases)
    strengths = Counter(case.get("strength") for case in cases)
    if strengths["strong"] < 3:
        errors.append("need at least three strong discovery cases")
    if strengths["weak"] < 2:
        errors.append("need at least two weak or incomplete cases")
    if kinds["demo"] + kinds["later-stage"] < 2:
        errors.append("need at least two demo or later-stage cases")

    required_keys = {"id", "call_type", "strength", "must_capture", "must_not_claim"}
    for case in cases:
        missing = required_keys - case.keys()
        if missing:
            errors.append(f"{case.get('id', '<unknown>')}: missing {sorted(missing)}")
        if not case.get("facts") and not case.get("notes"):
            errors.append(f"{case.get('id', '<unknown>')}: no transcript facts or notes")
        if not case.get("must_capture"):
            errors.append(f"{case.get('id', '<unknown>')}: no positive assertions")
        if not case.get("must_not_claim"):
            errors.append(f"{case.get('id', '<unknown>')}: no anti-fabrication assertions")

    expected_resolution_outcomes = {
        "continue_with_unique_deal",
        "continue_with_associated_deal",
        "ask_user_to_choose_from_linked_deals",
        "return_company_link_and_continue_without_deal_context",
    }
    actual_resolution_outcomes = {case.get("expected") for case in resolution_cases}
    if actual_resolution_outcomes != expected_resolution_outcomes:
        errors.append("record-resolution cases do not cover all required outcomes")
    for case in resolution_cases:
        if not case.get("must_include_link"):
            errors.append(f"{case.get('id', '<unknown>')}: resolved output does not require a link")
        if case.get("must_not_request") != "hubspot_link":
            errors.append(f"{case.get('id', '<unknown>')}: does not prohibit requesting a HubSpot link")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {len(cases)} cases")
    print(f"- strong discovery: {strengths['strong']}")
    print(f"- weak/incomplete discovery: {strengths['weak']}")
    print(f"- demo/later-stage: {kinds['demo'] + kinds['later-stage']}")
    print("- every case has capture and anti-fabrication assertions")
    print(f"- HubSpot record resolution: {len(resolution_cases)} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
