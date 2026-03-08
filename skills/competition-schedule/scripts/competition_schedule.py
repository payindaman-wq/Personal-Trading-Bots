#!/usr/bin/env python3
"""
competition_schedule.py - Schedule the next competition sprint via cron.

Parses a natural-language datetime string, converts PST to UTC,
and adds a one-time cron entry to launch competition-start.

Usage:
  python3 competition_schedule.py "Monday 5am PST"
  python3 competition_schedule.py "tomorrow 9am PST" --hours 6
  python3 competition_schedule.py --list
  python3 competition_schedule.py --cancel
"""
import sys
import os
import re
import argparse
import subprocess
from datetime import datetime, timezone, timedelta

COMPETITION_START = "/root/.openclaw/skills/competition-start/scripts/competition_start.py"
COMPETITION_LOG   = "/root/.openclaw/workspace/competition.log"
CRON_MARKER       = "# competition-schedule"

PST_OFFSET = timedelta(hours=-8)  # PST = UTC-8 (no DST adjustment)

WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}


def parse_datetime(text):
    """
    Parse expressions like:
      "Monday 5am PST"
      "tomorrow 9am PST"
      "2026-03-10 13:00 PST"
    Returns a UTC datetime (timezone-aware).
    """
    text = text.strip().lower()
    now_utc = datetime.now(timezone.utc)
    now_pst = now_utc + PST_OFFSET

    # Extract hour (e.g. "5am", "13:00", "9:30am")
    time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
    if not time_match:
        raise ValueError(f"Could not parse time from: {text}")
    hour = int(time_match.group(1))
    minute = int(time_match.group(2)) if time_match.group(2) else 0
    ampm = time_match.group(3)
    if ampm == "pm" and hour != 12:
        hour += 12
    if ampm == "am" and hour == 12:
        hour = 0

    # Determine the date in PST
    date_pst = None

    # ISO date?
    iso_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if iso_match:
        date_pst = datetime.strptime(iso_match.group(1), "%Y-%m-%d").date()

    # "tomorrow"?
    if date_pst is None and "tomorrow" in text:
        date_pst = (now_pst + timedelta(days=1)).date()

    # "today"?
    if date_pst is None and "today" in text:
        date_pst = now_pst.date()

    # Weekday name?
    if date_pst is None:
        for name, wd in WEEKDAYS.items():
            if name in text:
                days_ahead = (wd - now_pst.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # next occurrence
                date_pst = (now_pst + timedelta(days=days_ahead)).date()
                break

    if date_pst is None:
        raise ValueError(f"Could not parse date from: {text}")

    # Build PST datetime and convert to UTC
    pst_dt = datetime(date_pst.year, date_pst.month, date_pst.day,
                      hour, minute, tzinfo=timezone(PST_OFFSET))
    utc_dt = pst_dt.astimezone(timezone.utc)

    if utc_dt <= now_utc:
        raise ValueError(f"Scheduled time {pst_dt.strftime('%Y-%m-%d %H:%M PST')} is in the past.")

    return utc_dt, pst_dt


def get_crontab():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout


def set_crontab(content):
    proc = subprocess.run(["crontab", "-"], input=content, text=True)
    if proc.returncode != 0:
        raise RuntimeError("Failed to update crontab")


def list_scheduled():
    crontab = get_crontab()
    lines = [l for l in crontab.splitlines() if CRON_MARKER in l or
             (l.strip() and not l.startswith("#") and COMPETITION_START in l)]
    if not lines:
        print("  No competition sprints scheduled.")
    else:
        print("  Scheduled sprints:")
        for l in lines:
            print(f"    {l}")


def cancel_scheduled():
    crontab = get_crontab()
    new_lines = [l for l in crontab.splitlines()
                 if COMPETITION_START not in l and CRON_MARKER not in l]
    set_crontab("\n".join(new_lines) + "\n")
    print("  All scheduled competition sprints cancelled.")


def schedule(utc_dt, pst_dt, duration_hours):
    # Remove any existing scheduled sprint first
    crontab = get_crontab()
    filtered = [l for l in crontab.splitlines()
                if COMPETITION_START not in l and CRON_MARKER not in l]

    entry = (
        f"{CRON_MARKER} — {pst_dt.strftime('%Y-%m-%d %H:%M PST')}\n"
        f"{utc_dt.minute} {utc_dt.hour} {utc_dt.day} {utc_dt.month} * "
        f"python3 {COMPETITION_START} {duration_hours} "
        f">> {COMPETITION_LOG} 2>&1"
    )
    filtered.append(entry)
    set_crontab("\n".join(filtered) + "\n")
    print(f"  Scheduled: {pst_dt.strftime('%A %Y-%m-%d %H:%M PST')} "
          f"({utc_dt.strftime('%H:%M UTC')}), {duration_hours}h sprint")


def main():
    parser = argparse.ArgumentParser(description="Schedule a competition sprint")
    parser.add_argument("when", nargs="?",
                        help='When to start, e.g. "Monday 5am PST", "tomorrow 9am PST"')
    parser.add_argument("--hours", type=float, default=4.0,
                        help="Sprint duration in hours (default: 4)")
    parser.add_argument("--list",   action="store_true", help="List scheduled sprints")
    parser.add_argument("--cancel", action="store_true", help="Cancel scheduled sprints")
    args = parser.parse_args()

    if args.list:
        list_scheduled()
        return

    if args.cancel:
        cancel_scheduled()
        return

    if not args.when:
        parser.print_help()
        sys.exit(1)

    try:
        utc_dt, pst_dt = parse_datetime(args.when)
    except ValueError as e:
        print(f"  Error: {e}")
        sys.exit(1)

    schedule(utc_dt, pst_dt, args.hours)


if __name__ == "__main__":
    main()
