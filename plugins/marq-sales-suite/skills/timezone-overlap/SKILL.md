---
name: timezone-overlap
description: Find the times of day when everyone on a multi-region call is inside working hours, using a deterministic script rather than mental arithmetic. Use when scheduling across two or more time zones, or when a proposed slot needs checking against attendees elsewhere. Do not use for single-time-zone scheduling, for reading or writing a calendar, or for deciding who should attend.
---

# Time zone overlap

Reps schedule across regions constantly and DST arithmetic is where it goes wrong: the offset that held last week may not hold next week, and the failure is silent — a confidently stated time that is simply an hour off.

Do not compute overlaps in your head. Run the script.

## Workflow

1. Collect each attendee's IANA time zone (`America/Denver`, `Europe/London`, `Asia/Tokyo`). If someone gives a city or an abbreviation, convert it and say which zone you used, because abbreviations like `CST` are ambiguous.
2. Establish the meeting date. A zone's offset depends on the date, so never reuse an overlap computed for a different day.
3. Run the script:

   ```
   python3 scripts/overlap.py --date 2026-10-14 --zones America/Denver,Europe/London,Asia/Tokyo --duration 30
   ```

4. Report the windows it returns, rendered in each attendee's local time. Lead with the option that puts the fewest people outside 09:00–17:00.
5. If it returns no window, say so plainly and offer the least-bad options it lists under `--allow-stretch`. Do not invent a slot.

See [references/scheduling-rules.md](references/scheduling-rules.md) for the working-hours convention, how weekends and date-line crossings are handled, and what to do when no overlap exists.

## Constraints

- The script is the source of truth for every stated time. If you find yourself adding or subtracting hours in prose, stop and re-run it.
- Report the zone you assumed whenever an attendee gave a city rather than an IANA zone.
- This skill reads and writes nothing. It does not open, check, or modify a calendar. Scheduling the meeting is a separate step the user takes.
- Requires the IANA time zone database. On Windows that usually means `pip install tzdata`; the script stops with that message rather than guessing.
- If no tool for running a local command or script is available, say so and stop. Do not fall back to computing the overlap in prose.
