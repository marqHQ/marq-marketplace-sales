# Scheduling rules

## Working hours

Default is 09:00–17:00 local, Monday to Friday, for every attendee. Override with
`--start` and `--end` when a team genuinely keeps different hours; do not override it
silently to manufacture an overlap that does not exist.

## Weekends

A slot is rejected if it falls on Saturday or Sunday in **any** attendee's local zone.
This matters across the date line: 09:00 Monday in Tokyo is 17:00 Sunday in Denver, so
a window that looks fine to one attendee can be someone else's weekend.

## Daylight saving

Offsets are resolved for the specific date supplied, never cached. The US, EU, and
Southern Hemisphere transitions land on different dates, so there are stretches each
year when a familiar gap is an hour wider or narrower than usual. This is the single
most common source of a wrong meeting time, and it is why the script takes a date
rather than assuming today.

## When nothing overlaps

Some spans genuinely have no common working hours — Los Angeles and Singapore is the
usual example. Say so directly instead of quietly relaxing a constraint. Then offer,
in this order:

1. `--allow-stretch 60`, which permits one hour outside working hours and reports
   exactly who absorbs it.
2. Splitting into two regional calls.
3. An asynchronous update instead of a call.

Rotate who absorbs the inconvenience across a recurring series rather than always
imposing it on the same region.

## Reporting

Give every candidate in all attendees' local times, not just the organizer's. State
the date in each zone when a window crosses midnight for someone.
