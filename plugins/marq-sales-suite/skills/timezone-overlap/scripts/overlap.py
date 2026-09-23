#!/usr/bin/env python3
"""Find times of day when every attendee is inside working hours.

Deterministic: the same arguments always produce the same windows. Offsets are
resolved for the supplied date, so daylight-saving transitions are handled
correctly rather than assumed away.

  python3 overlap.py --date 2026-10-14 --zones America/Denver,Europe/London --duration 30
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - Python < 3.9
    print("Requires Python 3.9 or newer for zoneinfo.", file=sys.stderr)
    raise SystemExit(2)

STEP_MINUTES = 15


def load_zones(names):
    zones = []
    for name in names:
        try:
            zones.append((name, ZoneInfo(name)))
        except ZoneInfoNotFoundError:
            print(
                "Unknown time zone: {}\n"
                "Use an IANA name such as America/Denver. If every name fails, the "
                "IANA database is missing; on Windows install it with: pip install tzdata".format(name),
                file=sys.stderr,
            )
            raise SystemExit(2)
    return zones


def parse_hhmm(value, flag):
    try:
        hh, mm = value.split(":")
        return int(hh) * 60 + int(mm)
    except ValueError:
        print("{} must look like 09:00, got {!r}".format(flag, value), file=sys.stderr)
        raise SystemExit(2)


def minutes_outside(local, start_min, end_min):
    """How far this local time sits outside the working window, in minutes."""
    if local.weekday() >= 5:
        return None  # weekend: never acceptable, not merely a stretch
    pos = local.hour * 60 + local.minute
    if pos < start_min:
        return start_min - pos
    if pos >= end_min:
        return pos - end_min + STEP_MINUTES
    return 0


def evaluate(slot_utc, zones, start_min, end_min, duration, stretch):
    """Return per-zone cost for a slot, or None if it is unusable."""
    worst = 0
    detail = []
    for name, tz in zones:
        for offset in (0, duration - STEP_MINUTES):
            local = (slot_utc + timedelta(minutes=offset)).astimezone(tz)
            cost = minutes_outside(local, start_min, end_min)
            if cost is None or cost > stretch:
                return None
            worst = max(worst, cost)
        local = slot_utc.astimezone(tz)
        detail.append((name, local, cost))
    return worst, detail


def main():
    ap = argparse.ArgumentParser(description="Find working-hours overlap across time zones.")
    ap.add_argument("--date", required=True, help="Meeting date, YYYY-MM-DD, in the first zone listed")
    ap.add_argument("--zones", required=True, help="Comma-separated IANA zones")
    ap.add_argument("--duration", type=int, default=30, help="Meeting length in minutes (default 30)")
    ap.add_argument("--start", default="09:00", help="Working-hours start, local (default 09:00)")
    ap.add_argument("--end", default="17:00", help="Working-hours end, local (default 17:00)")
    ap.add_argument("--allow-stretch", type=int, default=0, metavar="MIN",
                    help="Permit this many minutes outside working hours (default 0)")
    args = ap.parse_args()

    names = [z.strip() for z in args.zones.split(",") if z.strip()]
    if len(names) < 2:
        print("Give at least two zones; a single zone needs no overlap check.", file=sys.stderr)
        raise SystemExit(2)
    zones = load_zones(names)

    if args.duration % STEP_MINUTES:
        print("--duration must be a multiple of {} minutes.".format(STEP_MINUTES), file=sys.stderr)
        raise SystemExit(2)

    start_min = parse_hhmm(args.start, "--start")
    end_min = parse_hhmm(args.end, "--end")
    if start_min >= end_min:
        print("--start must be earlier than --end.", file=sys.stderr)
        raise SystemExit(2)

    try:
        day = datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("--date must be YYYY-MM-DD, got {!r}".format(args.date), file=sys.stderr)
        raise SystemExit(2)

    anchor = day.replace(tzinfo=zones[0][1])
    scan_start = anchor.astimezone(timezone.utc) - timedelta(hours=24)
    steps = int(72 * 60 / STEP_MINUTES)

    found = []
    for i in range(steps):
        slot = scan_start + timedelta(minutes=i * STEP_MINUTES)
        if slot.astimezone(zones[0][1]).date() != day.date():
            continue
        result = evaluate(slot, zones, start_min, end_min, args.duration, args.allow_stretch)
        if result is not None:
            found.append((result[0], slot, result[1]))

    if not found:
        print("No window on {} keeps every attendee inside {}-{}.".format(args.date, args.start, args.end))
        if not args.allow_stretch:
            print("Try --allow-stretch 60 to see who would absorb an hour outside hours.")
        raise SystemExit(1)

    found.sort(key=lambda r: (r[0], r[1]))
    print("{} window(s) on {} for {} minutes:\n".format(len(found), args.date, args.duration))
    for cost, slot, detail in found[:8]:
        tag = "clean" if cost == 0 else "{} min outside hours".format(cost)
        print("  {}  [{}]".format(slot.strftime("%H:%M UTC"), tag))
        for name, local, _ in detail:
            print("      {:<22} {}".format(name, local.strftime("%a %Y-%m-%d %H:%M")))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
