#!/usr/bin/env python3
"""Deterministic scoring and append-only helpers for pipeline audits."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone
from typing import Any


THRESHOLDS = {"early": 14, "middle": 10, "late": 7}
EVIDENCE_POINTS = {"aligned": 20, "unverified": 10, "no_evidence": 10, "conflicting": 0}
TASK_POINTS = {"future_matching": 10, "none": 5, "mixed": 5, "overdue_only": 0}


def parse_date(value: str | None, field: str) -> date | None:
    if value in (None, ""):
        return None
    try:
        if "T" in value:
            normalized = value.replace("Z", "+00:00")
            return datetime.fromisoformat(normalized).astimezone(timezone.utc).date()
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an ISO date or datetime") from exc


def require_enum(data: dict[str, Any], field: str, allowed: set[str]) -> str:
    value = data.get(field)
    if value not in allowed:
        raise ValueError(f"{field} must be one of: {', '.join(sorted(allowed))}")
    return value


def score_deal(data: dict[str, Any]) -> dict[str, Any]:
    audit_date = parse_date(data.get("audit_date"), "audit_date")
    if audit_date is None:
        raise ValueError("audit_date is required")
    stage_band = require_enum(data, "stage_band", set(THRESHOLDS))
    evidence = require_enum(data, "evidence_status", set(EVIDENCE_POINTS))
    task = require_enum(data, "task_status", set(TASK_POINTS))
    actionable = data.get("has_actionable_next_step")
    weak = data.get("weak_next_step", False)
    if not isinstance(actionable, bool) or not isinstance(weak, bool):
        raise ValueError("has_actionable_next_step and weak_next_step must be booleans")

    next_date = parse_date(data.get("next_step_date"), "next_step_date")
    last_activity = parse_date(data.get("last_activity_at"), "last_activity_at")
    close_date = parse_date(data.get("close_date"), "close_date")
    threshold = THRESHOLDS[stage_band]
    days_to_next = (next_date - audit_date).days if next_date else None
    activity_age = (audit_date - last_activity).days if last_activity else None
    days_to_close = (close_date - audit_date).days if close_date else None

    next_points = (20 if next_date and days_to_next >= 0 else 0) + (20 if actionable else 0)
    if activity_age is not None and activity_age <= threshold:
        activity_points = 30
    elif activity_age is not None and activity_age <= threshold * 2:
        activity_points = 15
    else:
        activity_points = 0
    components = {
        "next_step_quality": next_points,
        "activity_recency": activity_points,
        "evidence_alignment": EVIDENCE_POINTS[evidence],
        "task_meeting_hygiene": TASK_POINTS[task],
    }
    total = sum(components.values())

    warnings: list[str] = []
    overrides: list[str] = []
    if next_date is None:
        overrides.append("missing_next_step_date")
    elif days_to_next < 0:
        overrides.append("expired_next_step_date")
    elif days_to_next <= 3:
        warnings.append("next_step_due_within_three_days")
    if not actionable:
        overrides.append("missing_actionable_next_step")
    elif weak:
        warnings.append("weak_next_step_text")
    if activity_age is None:
        overrides.append("missing_or_severely_stale_activity")
    elif activity_age > threshold * 2:
        overrides.append("severe_inactivity")
    elif activity_age > threshold:
        warnings.append("stage_threshold_inactivity")
    if close_date is not None and days_to_close < 0:
        overrides.append("past_close_date")
    if evidence == "conflicting":
        overrides.append("conflicting_evidence")
    elif evidence == "unverified":
        warnings.append("unverified_evidence")
    elif evidence == "no_evidence":
        warnings.append("no_corroborating_evidence")
    if task == "overdue_only":
        overrides.append("overdue_only_action_coverage")
    elif task == "none":
        warnings.append("no_matching_task_or_meeting")
    elif task == "mixed":
        warnings.append("mixed_task_coverage")

    if overrides or total < 50:
        color = "red"
    elif warnings or total < 80:
        color = "yellow"
    else:
        color = "green"

    return {
        "score": total,
        "color": color,
        "components": components,
        "warnings": warnings,
        "overrides": overrides,
        "threshold_days": threshold,
        "activity_age_days": activity_age,
        "days_to_next_step": days_to_next,
        "days_to_close": days_to_close,
    }


def normalize_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def append_history(existing: str | None, new_line: str) -> dict[str, Any]:
    if not new_line.strip():
        raise ValueError("new_line must not be empty")
    current = existing or ""
    normalized_new = normalize_line(new_line)
    duplicate = any(normalize_line(line) == normalized_new for line in current.splitlines())
    if duplicate:
        return {"changed": False, "value": current, "reason": "duplicate_line"}
    value = f"{current.rstrip()}\n{new_line.strip()}" if current.strip() else new_line.strip()
    return {"changed": True, "value": value, "reason": "appended"}


def reconcile(expected: int, ids: list[str]) -> dict[str, Any]:
    unique_ids = list(dict.fromkeys(ids))
    duplicates = len(ids) - len(unique_ids)
    return {
        "expected": expected,
        "received": len(ids),
        "unique": len(unique_ids),
        "duplicates": duplicates,
        "complete": len(unique_ids) == expected and duplicates == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    reconcile_parser = sub.add_parser("reconcile")
    reconcile_parser.add_argument("--expected", required=True, type=int)
    reconcile_parser.add_argument("--ids", nargs="+", required=True)
    append_parser = sub.add_parser("append")
    append_parser.add_argument("--existing", default="")
    append_parser.add_argument("--line", required=True)
    args = parser.parse_args()
    if args.command == "reconcile":
        result = reconcile(args.expected, args.ids)
    else:
        result = append_history(args.existing, args.line)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
