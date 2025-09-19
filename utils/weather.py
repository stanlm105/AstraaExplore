"""
Weather helpers for the Target Guidance Computer.

Fetches Open-Meteo hourly data and returns:
- A concise HTML summary for the UI panel
- A normalized dict (wx) used by assessment logic

Best practice: call this with a timezone-aware `when` produced by
utils.time_helpers.when_9pm_local(lat, lon) so all downstream calculations
refer to the same observing time.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Tuple
import requests

# WMO thunderstorm weather codes used by Open-Meteo (95 thunderstorm, 96/99 with hail)
_THUNDER_CODES = {95, 96, 99}
_REQ_TIMEOUT_SECS = 8


def _safe_hour_label(dt: datetime) -> str:
    """Return a friendly hour label like '9pm' from a datetime."""
    # %I gives 01-12; strip leading zero, lowercase AM/PM
    return dt.strftime("%I%p").lstrip("0").lower()


def get_night_weather(lat: float, lon: float, when: datetime) -> Tuple[str, Dict]:
    """
    Get weather conditions around the requested observing time.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        when (datetime): Target local datetime (timezone-aware). Prefer 9pm local.

    Returns:
        tuple[str, dict]: (html_summary, wx_dict)
            - html_summary: Short colored summary + details line.
            - wx_dict keys (all optional floats unless noted):
                cloud_pct, visibility_km, temp_c, precip_mm_per_hr,
                snow_mm_per_hr, wind_kph, gust_kph, thunder_prob (0/1),
                precip_prob_pct (percent), hour_iso (str)
    """
    # Open-Meteo returns local-time ISO strings if timezone=auto is used.
    target_date = when.date().isoformat()
    target_hour_iso = when.strftime("%Y-%m-%dT%H:00")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "timeformat": "iso8601",
        "hourly": ",".join(
            [
                "cloudcover",
                "visibility",
                "temperature_2m",
                "precipitation",              # mm/h water equivalent
                "rain",                       # mm/h rain only
                "snowfall",                   # cm/h snowfall rate
                "precipitation_probability",  # %
                "windspeed_10m",              # km/h (see windspeed_unit)
                "windgusts_10m",
                "weathercode",
            ]
        ),
        "windspeed_unit": "kmh",
        "start_date": target_date,
        "end_date": target_date,
    }

    try:
        resp = requests.get(url, params=params, timeout=_REQ_TIMEOUT_SECS)
        resp.raise_for_status()
        data = resp.json()

        hours = data["hourly"]["time"]  # e.g. ["2025-09-17T20:00", "2025-09-17T21:00", ...]
        # Exact match to the requested hour first
        try:
            idx = hours.index(target_hour_iso)
        except ValueError:
            # Fallback: prefer 21:00 on that date; if absent, choose nearest hour
            fallback_iso = f"{target_date}T21:00"
            if fallback_iso in hours:
                idx = hours.index(fallback_iso)
            else:
                # Nearest hour by absolute delta (Open-Meteo times are local naive strings)
                idx = min(
                    range(len(hours)),
                    key=lambda i: abs(
                        datetime.fromisoformat(hours[i]) - datetime.fromisoformat(target_hour_iso)
                    ),
                )

        # Helper to safely extract an hourly series element
        def pick(key: str, default=0.0):
            arr = data["hourly"].get(key)
            if not arr:
                return default
            val = arr[idx]
            return default if val is None else val

        cloud = float(pick("cloudcover", 0.0))                    # %
        vis_m = pick("visibility", None)                          # meters
        vis_km = (vis_m / 1000.0) if isinstance(vis_m, (int, float)) else None
        temp_c = float(pick("temperature_2m", 0.0))               # °C
        precip = float(pick("precipitation", 0.0))                # mm/h (water equiv)
        rain = float(pick("rain", 0.0))                           # mm/h
        snowfall_cm = float(pick("snowfall", 0.0))                # cm/h
        snow_mm_equiv = snowfall_cm * 10.0                        # approx 10:1 ratio
        wind = float(pick("windspeed_10m", 0.0))                  # km/h
        gust = float(pick("windgusts_10m", wind))                 # km/h
        wcode = int(pick("weathercode", 0))
        ppop = pick("precipitation_probability", None)            # %

        thunder_prob = 1.0 if wcode in _THUNDER_CODES else 0.0

        # Normalize for assessment
        wx = {
            "cloud_pct": cloud,
            "visibility_km": vis_km,
            "temp_c": temp_c,
            "precip_mm_per_hr": precip,
            "snow_mm_per_hr": snow_mm_equiv,
            "wind_kph": wind,
            "gust_kph": gust,
            "thunder_prob": thunder_prob,
            "precip_prob_pct": ppop,
            "hour_iso": hours[idx],
        }

        # Human-readable summary: lead indicator first, then details
        hour_label = _safe_hour_label(when)  # e.g., "9pm"
        vis_txt = f"{vis_km:.1f} km" if vis_km is not None else "—"
        details = (
            f"At {hour_label}, Cloud cover: {cloud:.0f}%, Visibility: {vis_txt}, "
            f"Temp: {temp_c:.1f}°C, Wind: {wind:.0f} km/h (gust {gust:.0f}), "
            f"Precip: {precip:.1f} mm/h, Rain: {rain:.1f} mm/h, Snow: {snowfall_cm:.1f} cm/h."
        )

        # Traffic-light lead (quick read; hard-stops are enforced elsewhere)
        if thunder_prob >= 0.3 or precip >= 0.1 or snowfall_cm >= 0.1:
            lead = '<font color="red"><b>Poor/Unsafe</b>: Wet or stormy conditions.</font>'
        elif cloud < 30 and (vis_km is None or vis_km > 10) and wind < 25:
            lead = '<font color="green"><b>Good Conditions</b>: Promising for stargazing.</font>'
        elif cloud > 80 or (vis_km is not None and vis_km < 5):
            lead = '<font color="red"><b>Poor Conditions</b>: Too cloudy or low visibility.</font>'
        else:
            lead = '<font color="orange"><b>Mixed Conditions</b>: Check the sky before observing.</font>'

        return f"{lead}<br>{details}", wx

    except Exception as e:
        print(f"Weather fetch error: {e}")
        return "Unable to fetch weather conditions.", {}