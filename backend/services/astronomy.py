from datetime import date, datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import ephem
import math
from timezonefinder import TimezoneFinder
import pytz


tf = TimezoneFinder()


def get_timezone_from_coords(lat: float, lng: float) -> str:
    """Get timezone string from coordinates."""
    tz = tf.timezone_at(lat=lat, lng=lng)
    return tz if tz else "UTC"


def format_time(dt: datetime, tz_str: str) -> str:
    """Format datetime to HH:MM string in the given timezone."""
    if dt is None:
        return "N/A"
    tz = pytz.timezone(tz_str)
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    local_dt = dt.astimezone(tz)
    return local_dt.strftime("%H:%M")


def calculate_solar(lat: float, lng: float, target_date: date, timezone: str) -> dict:
    """Calculate sunrise, sunset, twilight times."""
    location = LocationInfo(latitude=lat, longitude=lng, timezone=timezone)
    tz = pytz.timezone(timezone)

    try:
        s = sun(location.observer, date=target_date, tzinfo=tz)
    except ValueError:
        # Polar day or night - sun doesn't rise or set
        return {
            "sunrise": "Polar",
            "sunset": "Polar",
            "solar_noon": "N/A",
            "day_length": "24h 00m" if lat > 0 else "0h 00m",
            "twilight": {
                "civil": {"dawn": "N/A", "dusk": "N/A"},
                "nautical": {"dawn": "N/A", "dusk": "N/A"},
                "astronomical": {"dawn": "N/A", "dusk": "N/A"}
            }
        }

    sunrise = s.get("sunrise")
    sunset = s.get("sunset")
    noon = s.get("noon")

    # Calculate day length
    if sunrise and sunset:
        day_length = sunset - sunrise
        hours = int(day_length.total_seconds() // 3600)
        minutes = int((day_length.total_seconds() % 3600) // 60)
        day_length_str = f"{hours}h {minutes:02d}m"
    else:
        day_length_str = "N/A"

    # Calculate twilight times using ephem for better accuracy
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lng)
    obs.date = datetime.combine(target_date, datetime.min.time())
    obs.elevation = 0

    def get_twilight(depression: float) -> dict:
        obs.horizon = str(-depression)
        try:
            dawn = obs.previous_rising(ephem.Sun(), use_center=True).datetime()
            dusk = obs.next_setting(ephem.Sun(), use_center=True).datetime()
            return {
                "dawn": format_time(dawn, timezone),
                "dusk": format_time(dusk, timezone)
            }
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            return {"dawn": "N/A", "dusk": "N/A"}

    # Reset observer date for twilight calculations
    obs.date = datetime.combine(target_date, datetime.min.time().replace(hour=12))

    return {
        "sunrise": format_time(sunrise, timezone) if sunrise else "N/A",
        "sunset": format_time(sunset, timezone) if sunset else "N/A",
        "solar_noon": format_time(noon, timezone) if noon else "N/A",
        "day_length": day_length_str,
        "twilight": {
            "civil": get_twilight(6),
            "nautical": get_twilight(12),
            "astronomical": get_twilight(18)
        }
    }


def calculate_lunar(lat: float, lng: float, target_date: date, timezone: str) -> dict:
    """Calculate moon phase, moonrise/moonset, and upcoming events."""
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lng)
    obs.elevation = 0
    obs.date = datetime.combine(target_date, datetime.min.time().replace(hour=12))

    moon = ephem.Moon()
    moon.compute(obs)

    # Moon illumination
    illumination = moon.phase / 100.0

    # Determine moon phase name
    phase_angle = moon.phase
    if phase_angle < 1:
        phase_name = "New Moon"
    elif phase_angle < 25:
        phase_name = "Waxing Crescent"
    elif phase_angle < 50:
        phase_name = "First Quarter"
    elif phase_angle < 75:
        phase_name = "Waxing Gibbous"
    elif phase_angle < 99:
        phase_name = "Full Moon" if phase_angle > 95 else "Waxing Gibbous"
    else:
        phase_name = "Full Moon"

    # More accurate phase determination using moon age
    moon_age_days = (target_date - date(2000, 1, 6)).days % 29.530588853
    if moon_age_days < 1.85:
        phase_name = "New Moon"
    elif moon_age_days < 7.38:
        phase_name = "Waxing Crescent"
    elif moon_age_days < 9.23:
        phase_name = "First Quarter"
    elif moon_age_days < 14.77:
        phase_name = "Waxing Gibbous"
    elif moon_age_days < 16.61:
        phase_name = "Full Moon"
    elif moon_age_days < 22.15:
        phase_name = "Waning Gibbous"
    elif moon_age_days < 23.99:
        phase_name = "Last Quarter"
    else:
        phase_name = "Waning Crescent"

    # Moonrise and moonset
    obs.date = datetime.combine(target_date, datetime.min.time())
    try:
        moonrise = obs.next_rising(moon).datetime()
        moonrise_str = format_time(moonrise, timezone)
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        moonrise_str = None

    try:
        moonset = obs.next_setting(moon).datetime()
        moonset_str = format_time(moonset, timezone)
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        moonset_str = None

    # Next full moon and new moon
    obs.date = datetime.combine(target_date, datetime.min.time())
    next_full = ephem.next_full_moon(obs.date).datetime().date()
    next_new = ephem.next_new_moon(obs.date).datetime().date()

    return {
        "phase": phase_name,
        "illumination": round(illumination, 2),
        "moonrise": moonrise_str,
        "moonset": moonset_str,
        "next_full_moon": next_full.isoformat(),
        "next_new_moon": next_new.isoformat()
    }


def calculate_tides(illumination: float) -> dict:
    """Calculate tide tendency based on moon illumination."""
    if illumination > 0.85 or illumination < 0.15:
        return {
            "tendency": "Spring Tide (Strong)",
            "description": "Near full/new moon - expect higher high tides and lower low tides",
            "moon_phase_factor": illumination
        }
    elif 0.35 < illumination < 0.65:
        return {
            "tendency": "Neap Tide (Weak)",
            "description": "Near quarter moon - expect moderate tidal range",
            "moon_phase_factor": illumination
        }
    else:
        return {
            "tendency": "Moderate Tide",
            "description": "Transitional period between spring and neap tides",
            "moon_phase_factor": illumination
        }
