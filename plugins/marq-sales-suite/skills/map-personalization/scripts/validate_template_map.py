#!/usr/bin/env python3
"""Fail fast when a MAP skill installation has a stale template map."""

import json
import re
import sys
from pathlib import Path


REQUIRED_KEYS = (
    "higher ed",
    "hospitals and clinics",
    "real estate",
    "manufacturing",
    "insurance",
    "financial services",
    "generic",
)
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def main() -> int:
    default_path = Path(__file__).resolve().parent.parent / "references" / "template-map.json"
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else default_path

    try:
        template_map = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"STALE_TEMPLATE_MAP: cannot read {path}: {exc}", file=sys.stderr)
        return 1

    if not isinstance(template_map, dict):
        print("STALE_TEMPLATE_MAP: template map must be an object", file=sys.stderr)
        return 1

    invalid = [
        key
        for key in REQUIRED_KEYS
        if not isinstance(template_map.get(key), str)
        or not UUID_RE.fullmatch(template_map[key])
    ]
    if invalid:
        print(
            "STALE_TEMPLATE_MAP: refresh the MAP personalization skill; invalid keys: "
            + ", ".join(invalid),
            file=sys.stderr,
        )
        return 1

    print("MAP template map valid (version 2026-10-06):")
    for key in REQUIRED_KEYS:
        print(f"- {key}: {template_map[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
