"""
Time helpers for Messier Target Guidance Computer.

- Resolve timezone from lat/lon using timezonefinder (offline).
- Produce local datetimes/dates with stdlib zoneinfo (DST-aware).
"""

from __future__ import annotations

from datetime import datetime, date, time, timedelta
from functools import lru_cache
from typing import Optional

from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

# Create once; heavy init reads polygon data.
_TF = TimezoneFinder()

# ---------------------------
# Core utilities
# ---------------------------

@lru_cache(maxsize=4096)
def tzname_for_coords(lat: float, lon: float) -> str:
    """
    Return the IANA timezone name for given coordinates.

    Tries an exact polygon hit first, then nearest match. Falls back to 'UTC'
    when no zone can be determined (e.g., in the open ocean).

    Raises:
        ValueError: if lat/lon are outside [-90, 90] / [-180, 180].
    """
    
    # Handle None values gracefully
    if lat is None or lon is None:
        print("Warning: lat/lon is None, using UTC")
        return "UTC"
    
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        print(f"Warning: Invalid lat/lon values: {lat}, {lon}, using UTC")
        return "UTC"
    
    lat = float(lat)
    lon = float(lon)
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise ValueError("Invalid coordinates.")
    tzname = _TF.timezone_at(lat=lat, lng=lon) or _TF.closest_timezone_at(lat=lat, lng=lon)
    return tzname or "UTC"


def zoneinfo_for_coords(lat: float, lon: float) -> ZoneInfo:
    """
    Return a ZoneInfo object for the location, with UTC fallback.
    """
    return ZoneInfo(tzname_for_coords(lat, lon))


def local_now(lat: float, lon: float) -> datetime:
    """
    Current local datetime at the given location.
    """
    tz = zoneinfo_for_coords(lat, lon)
    return datetime.now(tz)


def local_date_iso(lat: float, lon: float) -> str:
    """
    Local calendar date (YYYY-MM-DD) for the given coordinates.
    """
    return local_now(lat, lon).date().isoformat()


def when_local(
    lat: float,
    lon: float,
    *,
    at: time,
    on: Optional[date] = None,
    rollover_if_past: bool = False,
) -> datetime:
    """
    Local datetime at a specific wall-clock time on a given (or today's) date.

    Args:
        lat, lon: Coordinates.
        at: Local wall-clock time desired (e.g. time(21, 0)).
        on: Date to use; defaults to today's date at the location.
        rollover_if_past: If True and now > target time today, return tomorrow at 'at'.

    Returns:
        Timezone-aware datetime in the location's time zone.
    """
    tz = zoneinfo_for_coords(lat, lon)
    now_local = datetime.now(tz)
    d = on or now_local.date()

    # Using 21:00 avoids DST gap/ambiguity (transitions usually happen ~02:00),
    # but this works for any 'at'. If you ever target transition times,
    # consider handling fold/nonexistent explicitly.
    dt = datetime.combine(d, at, tzinfo=tz)

    if rollover_if_past and now_local > dt:
        dt = dt + timedelta(days=1)

    return dt

# Convenience: your original API
def when_9pm_local(
    lat: float,
    lon: float,
    *,
    obs_date: date | None = None,
    rollover_if_past: bool = False
) -> datetime:
    """
    Local 21:00 (9pm) at the given coordinates.
    """
    return when_local(
        lat, lon,
        at=time(21, 0),
        on=obs_date,
        rollover_if_past=rollover_if_past,
    )
