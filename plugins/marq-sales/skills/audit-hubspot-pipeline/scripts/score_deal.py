#!/usr/bin/env python3
"""Score one normalized deal JSON object from a file or stdin."""

from __future__ import annotations

import argparse
import json
import sys

from audit_utils import score_deal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="JSON input path; omit to read stdin")
    args = parser.parse_args()
    try:
        if args.path:
            with open(args.path, encoding="utf-8") as source:
                data = json.load(source)
        else:
            data = json.load(sys.stdin)
        print(json.dumps(score_deal(data), indent=2, sort_keys=True))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
