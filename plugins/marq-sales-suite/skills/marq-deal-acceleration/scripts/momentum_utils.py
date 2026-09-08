#!/usr/bin/env python3
"""Deterministic customer-momentum classification for one opportunity."""

from __future__ import annotations

from typing import Any


ALLOWED = {
    "stage_band": {"early", "middle", "late"},
    "next_step_status": {"valid", "weak", "missing", "overdue"},
    "commitment_status": {"on_track", "one_slip", "two_or_more_missed", "unknown"},
    "stakeholder_status": {"expanding", "complete", "static", "single_threaded", "shrinking", "unknown"},
    "critical_event_status": {"credible", "plausible", "absent", "contradicted", "expired", "seller_created", "not_required", "unknown"},
    "close_date_status": {"credible", "at_risk", "moved_once", "moved_twice_or_more", "rolled_period", "infeasible", "not_in_period", "unknown"},
    "champion_status": {"mobilizing", "responsive", "silent", "defensive", "left", "cannot_mobilize", "not_required", "unknown"},
    "required_process_status": {"started", "not_started", "not_yet_required", "unknown"},
}


def require_enum(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if value not in ALLOWED[field]:
        raise ValueError(f"{field} must be one of: {', '.join(sorted(ALLOWED[field]))}")
    return value


def require_bool(data: dict[str, Any], field: str) -> bool:
    value = data.get(field)
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be a boolean")
    return value


def score_momentum(data: dict[str, Any]) -> dict[str, Any]:
    values = {field: require_enum(data, field) for field in ALLOWED}
    booleans = {
        field: require_bool(data, field)
        for field in ("agreed_longer_wait", "forecast_in_period", "customer_negative_signal", "stage_or_forecast_contradicted")
    }
    engagement = data.get("days_since_meaningful_engagement")
    if engagement is not None and (not isinstance(engagement, int) or isinstance(engagement, bool) or engagement < 0):
        raise ValueError("days_since_meaningful_engagement must be a non-negative integer or null")

    overrides: list[str] = []
    warnings: list[str] = []
    threshold = 7 if values["stage_band"] == "late" else 14

    if engagement is None:
        warnings.append("engagement_recency_unknown")
    elif engagement > 30 and not booleans["agreed_longer_wait"]:
        overrides.append("no_meaningful_engagement_over_30_days")
    elif engagement > threshold and not booleans["agreed_longer_wait"]:
        warnings.append("engagement_beyond_stage_threshold")

    if values["next_step_status"] == "missing":
        overrides.append("missing_valid_next_step")
    elif values["next_step_status"] == "overdue":
        overrides.append("customer_next_step_overdue")
    elif values["next_step_status"] == "weak":
        warnings.append("weak_next_step")

    if values["commitment_status"] == "two_or_more_missed":
        overrides.append("repeated_missed_customer_commitments")
    elif values["commitment_status"] == "one_slip":
        warnings.append("one_customer_commitment_slipped")
    elif values["commitment_status"] == "unknown":
        warnings.append("customer_commitment_status_unknown")

    if values["stakeholder_status"] == "shrinking":
        overrides.append("stakeholder_access_shrinking")
    elif values["stakeholder_status"] in {"static", "single_threaded"}:
        warnings.append(f"stakeholder_access_{values['stakeholder_status']}")
    elif values["stakeholder_status"] == "unknown":
        warnings.append("stakeholder_access_unknown")

    if booleans["forecast_in_period"] and values["critical_event_status"] in {"absent", "contradicted", "expired", "seller_created"}:
        overrides.append(f"critical_event_{values['critical_event_status']}")
    elif values["critical_event_status"] in {"plausible", "absent", "unknown"}:
        warnings.append(f"critical_event_{values['critical_event_status']}")

    if values["close_date_status"] in {"moved_twice_or_more", "rolled_period", "infeasible"}:
        overrides.append(f"close_date_{values['close_date_status']}")
    elif values["close_date_status"] in {"at_risk", "moved_once", "unknown"}:
        warnings.append(f"close_date_{values['close_date_status']}")

    if values["champion_status"] in {"silent", "defensive", "left", "cannot_mobilize"}:
        overrides.append(f"champion_{values['champion_status']}")
    elif values["champion_status"] == "responsive":
        warnings.append("champion_not_yet_mobilizing")
    elif values["champion_status"] == "unknown":
        warnings.append("champion_status_unknown")

    if values["stage_band"] == "late" and values["required_process_status"] == "not_started":
        overrides.append("required_late_stage_process_not_started")
    elif values["required_process_status"] == "unknown":
        warnings.append("required_process_status_unknown")

    if booleans["customer_negative_signal"]:
        overrides.append("direct_customer_negative_signal")
    if booleans["stage_or_forecast_contradicted"]:
        overrides.append("direct_customer_evidence_contradicts_stage_or_forecast")

    if overrides:
        color = "red"
    elif warnings:
        color = "yellow"
    else:
        color = "green"

    return {
        "color": color,
        "engagement_threshold_days": threshold,
        "warnings": warnings,
        "overrides": overrides,
    }
