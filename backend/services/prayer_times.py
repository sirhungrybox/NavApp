from datetime import date, datetime
import math
import pytz


# Prayer calculation methods with their angles
METHODS = {
    "muslim_world_league": {"fajr": 18, "isha": 17, "name": "Muslim World League"},
    "isna": {"fajr": 15, "isha": 15, "name": "ISNA"},
    "egyptian": {"fajr": 19.5, "isha": 17.5, "name": "Egyptian General Authority"},
    "umm_al_qura": {"fajr": 18.5, "isha": 90, "isha_is_minutes": True, "name": "Umm Al-Qura"},
    "dubai": {"fajr": 18.2, "isha": 18.2, "name": "Dubai"},
    "kuwait": {"fajr": 18, "isha": 17.5, "name": "Kuwait"},
    "qatar": {"fajr": 18, "isha": 90, "isha_is_minutes": True, "name": "Qatar"},
}


def calculate_prayer_times(lat: float, lng: float, target_date: date, timezone: str, method: str = "muslim_world_league") -> dict:
    """Calculate Islamic prayer times using solar position calculations."""

    method_params = METHODS.get(method, METHODS["muslim_world_league"])
    tz = pytz.timezone(timezone)

    # Julian date calculation
    year = target_date.year
    month = target_date.month
    day = target_date.day

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

    # Days since J2000
    D = JD - 2451545.0

    # Mean longitude of the Sun
    g = 357.529 + 0.98560028 * D
    g = g % 360

    # Mean longitude
    q = 280.459 + 0.98564736 * D
    q = q % 360

    # Ecliptic longitude of the Sun
    L = q + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
    L = L % 360

    # Obliquity of the ecliptic
    e = 23.439 - 0.00000036 * D

    # Declination of the Sun
    decl = math.degrees(math.asin(math.sin(math.radians(e)) * math.sin(math.radians(L))))

    # Equation of time
    RA = math.degrees(math.atan2(math.cos(math.radians(e)) * math.sin(math.radians(L)), math.cos(math.radians(L)))) / 15
    if RA < 0:
        RA += 24

    EqT = q / 15 - RA
    if EqT > 12:
        EqT -= 24
    elif EqT < -12:
        EqT += 24

    # Dhuhr time (solar noon)
    dhuhr = 12 + (-lng / 15) - EqT

    # Get timezone offset
    dt = datetime.combine(target_date, datetime.min.time())
    offset = tz.localize(dt).utcoffset().total_seconds() / 3600
    dhuhr += offset

    def sun_angle_time(angle: float, direction: int) -> float:
        """Calculate time when sun is at given angle below horizon."""
        try:
            cos_t = (math.sin(math.radians(-angle)) -
                    math.sin(math.radians(lat)) * math.sin(math.radians(decl))) / \
                   (math.cos(math.radians(lat)) * math.cos(math.radians(decl)))

            if cos_t > 1 or cos_t < -1:
                return None

            t = math.degrees(math.acos(cos_t)) / 15
            return dhuhr + direction * t
        except:
            return None

    def asr_time(shadow_factor: float = 1) -> float:
        """Calculate Asr time based on shadow length."""
        try:
            # Calculate the sun altitude when shadow = shadow_factor * object height + noon shadow
            # At Asr, the shadow length = shadow_factor * object + noon shadow
            # tan(altitude) = 1 / (shadow_factor + tan(zenith_at_noon))
            zenith_at_noon = abs(lat - decl)
            asr_altitude = math.degrees(math.atan(1 / (shadow_factor + math.tan(math.radians(zenith_at_noon)))))

            # Calculate hour angle for this altitude
            cos_ha = (math.sin(math.radians(asr_altitude)) -
                     math.sin(math.radians(lat)) * math.sin(math.radians(decl))) / \
                    (math.cos(math.radians(lat)) * math.cos(math.radians(decl)))

            if cos_ha > 1 or cos_ha < -1:
                return None

            hour_angle = math.degrees(math.acos(cos_ha)) / 15
            return dhuhr + hour_angle
        except:
            return None

    # Calculate prayer times
    fajr_angle = method_params["fajr"]
    fajr = sun_angle_time(fajr_angle, -1)

    sunrise = sun_angle_time(0.833, -1)  # Standard refraction angle

    asr = asr_time(1)  # Standard Asr (Shafi'i)

    sunset = sun_angle_time(0.833, 1)
    maghrib = sunset

    # Isha calculation
    if method_params.get("isha_is_minutes"):
        isha = maghrib + method_params["isha"] / 60 if maghrib else None
    else:
        isha_angle = method_params["isha"]
        isha = sun_angle_time(isha_angle, 1)

    def format_time(hours: float) -> str:
        if hours is None:
            return "N/A"
        hours = hours % 24
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h:02d}:{m:02d}"

    return {
        "fajr": format_time(fajr),
        "sunrise": format_time(sunrise),
        "dhuhr": format_time(dhuhr),
        "asr": format_time(asr),
        "maghrib": format_time(maghrib),
        "isha": format_time(isha),
        "method": method_params["name"]
    }
