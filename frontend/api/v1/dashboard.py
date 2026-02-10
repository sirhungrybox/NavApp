from http.server import BaseHTTPRequestHandler
import json
import math
from datetime import date, datetime, timedelta
from urllib.parse import parse_qs, urlparse
import urllib.request

# Regional timezone definitions (lat_min, lat_max, lng_min, lng_max, tz_name, offset)
# Order matters - more specific regions first
TIMEZONE_REGIONS = [
    # === Middle East (specific first) ===
    # UAE (UTC+4)
    (22, 27, 51, 57, "Asia/Dubai", 4),
    # Oman (UTC+4)
    (16, 27, 52, 60, "Asia/Muscat", 4),
    # Qatar (UTC+3)
    (24.4, 26.5, 50.5, 52, "Asia/Qatar", 3),
    # Bahrain (UTC+3)
    (25.5, 26.5, 50, 51, "Asia/Bahrain", 3),
    # Kuwait (UTC+3)
    (28.5, 30.5, 46.5, 49, "Asia/Kuwait", 3),
    # Saudi Arabia (UTC+3)
    (16, 32, 34, 56, "Asia/Riyadh", 3),
    # Iran (UTC+3.5)
    (25, 40, 44, 63, "Asia/Tehran", 3.5),
    # Iraq (UTC+3)
    (29, 38, 38, 49, "Asia/Baghdad", 3),
    # Jordan (UTC+3)
    (29, 34, 34, 40, "Asia/Amman", 3),
    # Israel (UTC+2)
    (29, 34, 34, 36, "Asia/Jerusalem", 2),

    # === South Asia ===
    # Pakistan (UTC+5)
    (23, 37, 61, 77, "Asia/Karachi", 5),
    # India (UTC+5.5)
    (6, 36, 68, 97, "Asia/Kolkata", 5.5),
    # Sri Lanka (UTC+5.5)
    (5, 10, 79, 82, "Asia/Colombo", 5.5),
    # Nepal (UTC+5.75)
    (26, 31, 80, 89, "Asia/Kathmandu", 5.75),
    # Bangladesh (UTC+6)
    (20, 27, 88, 93, "Asia/Dhaka", 6),
    # Myanmar (UTC+6.5)
    (9, 29, 92, 102, "Asia/Yangon", 6.5),

    # === Southeast Asia ===
    # Thailand (UTC+7)
    (5, 21, 97, 106, "Asia/Bangkok", 7),
    # Vietnam (UTC+7)
    (8, 24, 102, 110, "Asia/Ho_Chi_Minh", 7),
    # Cambodia (UTC+7)
    (10, 15, 102, 108, "Asia/Phnom_Penh", 7),
    # Singapore (UTC+8)
    (1, 2, 103, 105, "Asia/Singapore", 8),
    # Malaysia (UTC+8)
    (0, 8, 99, 120, "Asia/Kuala_Lumpur", 8),
    # Indonesia West (UTC+7)
    (-8, 6, 95, 110, "Asia/Jakarta", 7),
    # Indonesia Central (UTC+8)
    (-11, 2, 110, 120, "Asia/Makassar", 8),
    # Philippines (UTC+8)
    (4, 22, 116, 128, "Asia/Manila", 8),

    # === East Asia ===
    # China, Hong Kong, Taiwan (UTC+8)
    (18, 54, 73, 135, "Asia/Shanghai", 8),
    # Japan (UTC+9)
    (24, 46, 127, 146, "Asia/Tokyo", 9),
    # Korea (UTC+9)
    (33, 43, 124, 132, "Asia/Seoul", 9),

    # === Oceania ===
    # Eastern Australia (UTC+10/11)
    (-44, -10, 140, 154, "Australia/Sydney", 10),
    # Central Australia (UTC+9.5)
    (-40, -10, 129, 141, "Australia/Adelaide", 9.5),
    # Western Australia (UTC+8)
    (-35, -14, 113, 130, "Australia/Perth", 8),
    # New Zealand (UTC+12/13)
    (-48, -34, 166, 179, "Pacific/Auckland", 12),

    # === Europe ===
    # UK, Ireland, Portugal (UTC+0/1)
    (36, 62, -11, 2, "Europe/London", 0),
    # Western Europe (UTC+1/2)
    (35, 72, 0, 17, "Europe/Paris", 1),
    # Central Europe (UTC+1/2)
    (45, 55, 5, 25, "Europe/Berlin", 1),
    # Eastern Europe (UTC+2/3)
    (34, 72, 17, 32, "Europe/Athens", 2),
    # Turkey (UTC+3)
    (36, 42, 26, 45, "Europe/Istanbul", 3),
    # Russia Moscow (UTC+3)
    (50, 70, 30, 60, "Europe/Moscow", 3),

    # === Africa ===
    # Egypt (UTC+2)
    (22, 32, 25, 35, "Africa/Cairo", 2),
    # East Africa (UTC+3)
    (-12, 12, 29, 52, "Africa/Nairobi", 3),
    # South Africa (UTC+2)
    (-35, -22, 16, 33, "Africa/Johannesburg", 2),
    # West Africa (UTC+0/+1)
    (-5, 25, -18, 16, "Africa/Lagos", 1),
    # Morocco (UTC+1)
    (27, 36, -13, -1, "Africa/Casablanca", 1),

    # === Americas ===
    # Brazil East (UTC-3)
    (-34, 6, -54, -34, "America/Sao_Paulo", -3),
    # Argentina (UTC-3)
    (-56, -21, -74, -53, "America/Argentina/Buenos_Aires", -3),
    # Chile (UTC-3/-4)
    (-56, -17, -76, -66, "America/Santiago", -3),
    # US Eastern (UTC-5/-4)
    (24, 49, -90, -66, "America/New_York", -5),
    # US Central (UTC-6/-5)
    (25, 50, -105, -89, "America/Chicago", -6),
    # US Mountain (UTC-7/-6)
    (31, 49, -117, -104, "America/Denver", -7),
    # US Pacific (UTC-8/-7)
    (32, 49, -125, -116, "America/Los_Angeles", -8),
    # Alaska (UTC-9/-8)
    (51, 72, -180, -129, "America/Anchorage", -9),
    # Hawaii (UTC-10)
    (18, 29, -162, -154, "Pacific/Honolulu", -10),
    # Mexico (UTC-6)
    (14, 33, -118, -86, "America/Mexico_City", -6),
    # Canada Eastern (UTC-5)
    (42, 63, -95, -52, "America/Toronto", -5),
]

# Fallback longitude-based offsets for ocean/unknown areas
def get_lng_offset(lng):
    """Calculate timezone offset based on longitude (15° per hour)."""
    return round(lng / 15)

PRAYER_METHODS = {
    "muslim_world_league": {"fajr": 18, "isha": 17, "name": "Muslim World League"},
    "isna": {"fajr": 15, "isha": 15, "name": "ISNA"},
    "egyptian": {"fajr": 19.5, "isha": 17.5, "name": "Egyptian General Authority"},
    "umm_al_qura": {"fajr": 18.5, "isha": 90, "isha_is_minutes": True, "name": "Umm Al-Qura"},
    "dubai": {"fajr": 18.2, "isha": 18.2, "name": "Dubai"},
    "kuwait": {"fajr": 18, "isha": 17.5, "name": "Kuwait"},
    "qatar": {"fajr": 18, "isha": 90, "isha_is_minutes": True, "name": "Qatar"},
}


def get_tz(lat, lng):
    """Get timezone name and offset for coordinates."""
    # First check specific regional definitions
    for lat_min, lat_max, lng_min, lng_max, tz_name, offset in TIMEZONE_REGIONS:
        if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
            return tz_name, offset

    # Fallback to longitude-based calculation for ocean areas
    offset = get_lng_offset(lng)
    if offset == 0:
        return "UTC", 0
    elif offset > 0:
        return f"Etc/GMT-{offset}", offset  # Note: Etc/GMT sign is inverted
    else:
        return f"Etc/GMT+{abs(offset)}", offset


def fmt_time(hours):
    if hours is None:
        return "N/A"
    hours = hours % 24
    return f"{int(hours):02d}:{int((hours % 1) * 60):02d}"


def calc_solar(lat, lng, d, tz_off):
    y, m, dy = d.year, d.month, d.day
    if m <= 2:
        y -= 1
        m += 12
    JD = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + dy + 2 - (y // 100) + (y // 400) - 1524.5
    D = JD - 2451545.0
    g = (357.529 + 0.98560028 * D) % 360
    q = (280.459 + 0.98564736 * D) % 360
    L = (q + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))) % 360
    e = 23.439 - 0.00000036 * D
    decl = math.degrees(math.asin(math.sin(math.radians(e)) * math.sin(math.radians(L))))
    RA = math.degrees(math.atan2(math.cos(math.radians(e)) * math.sin(math.radians(L)), math.cos(math.radians(L)))) / 15
    if RA < 0:
        RA += 24
    EqT = q / 15 - RA
    if EqT > 12:
        EqT -= 24
    elif EqT < -12:
        EqT += 24
    noon = 12 + (-lng / 15) - EqT + tz_off

    def angle_time(ang, dr):
        try:
            ct = (math.sin(math.radians(-ang)) - math.sin(math.radians(lat)) * math.sin(math.radians(decl))) / (math.cos(math.radians(lat)) * math.cos(math.radians(decl)))
            if ct > 1 or ct < -1:
                return None
            return noon + dr * math.degrees(math.acos(ct)) / 15
        except:
            return None

    sr, ss = angle_time(0.833, -1), angle_time(0.833, 1)
    dl = f"{int(ss - sr)}h {int(((ss - sr) % 1) * 60):02d}m" if sr and ss else "N/A"

    return {
        "sunrise": fmt_time(sr), "sunset": fmt_time(ss), "solar_noon": fmt_time(noon), "day_length": dl,
        "twilight": {
            "civil": {"dawn": fmt_time(angle_time(6, -1)), "dusk": fmt_time(angle_time(6, 1))},
            "nautical": {"dawn": fmt_time(angle_time(12, -1)), "dusk": fmt_time(angle_time(12, 1))},
            "astronomical": {"dawn": fmt_time(angle_time(18, -1)), "dusk": fmt_time(angle_time(18, 1))}
        }
    }, decl, noon


def calc_prayer(lat, lng, d, tz_off, decl, noon, method):
    mp = PRAYER_METHODS.get(method, PRAYER_METHODS["muslim_world_league"])

    def angle_time(ang, dr):
        try:
            ct = (math.sin(math.radians(-ang)) - math.sin(math.radians(lat)) * math.sin(math.radians(decl))) / (math.cos(math.radians(lat)) * math.cos(math.radians(decl)))
            if ct > 1 or ct < -1:
                return None
            return noon + dr * math.degrees(math.acos(ct)) / 15
        except:
            return None

    def asr():
        try:
            z = abs(lat - decl)
            alt = math.degrees(math.atan(1 / (1 + math.tan(math.radians(z)))))
            ct = (math.sin(math.radians(alt)) - math.sin(math.radians(lat)) * math.sin(math.radians(decl))) / (math.cos(math.radians(lat)) * math.cos(math.radians(decl)))
            if ct > 1 or ct < -1:
                return None
            return noon + math.degrees(math.acos(ct)) / 15
        except:
            return None

    ss = angle_time(0.833, 1)
    isha = (ss + mp["isha"] / 60) if mp.get("isha_is_minutes") and ss else angle_time(mp["isha"], 1)

    return {
        "fajr": fmt_time(angle_time(mp["fajr"], -1)), "sunrise": fmt_time(angle_time(0.833, -1)),
        "dhuhr": fmt_time(noon), "asr": fmt_time(asr()), "maghrib": fmt_time(ss), "isha": fmt_time(isha),
        "method": mp["name"]
    }


def calc_lunar(d):
    age = (d - date(2000, 1, 6)).days % 29.530588853
    phases = [(1.85, "New Moon"), (7.38, "Waxing Crescent"), (9.23, "First Quarter"), (14.77, "Waxing Gibbous"),
              (16.61, "Full Moon"), (22.15, "Waning Gibbous"), (23.99, "Last Quarter"), (29.53, "Waning Crescent")]
    phase = "New Moon"
    for limit, name in phases:
        if age < limit:
            phase = name
            break
    illum = min(1.0, max(0.0, (1 - abs(age - 14.765) / 14.765)))
    nf = d + timedelta(days=(14.765 - age) % 29.53)
    nn = d + timedelta(days=(29.53 - age) % 29.53)
    return {"phase": phase, "illumination": round(illum, 2), "moonrise": "05:30", "moonset": "17:45",
            "next_full_moon": nf.isoformat(), "next_new_moon": nn.isoformat()}


def calc_tides(illum):
    if illum > 0.85 or illum < 0.15:
        return {"tendency": "Spring Tide (Strong)", "description": "Near full/new moon - stronger tides", "moon_phase_factor": illum}
    elif 0.35 < illum < 0.65:
        return {"tendency": "Neap Tide (Weak)", "description": "Near quarter moon - moderate tides", "moon_phase_factor": illum}
    return {"tendency": "Moderate Tide", "description": "Transitional period", "moon_phase_factor": illum}


def get_weather(lat, lng):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current=temperature_2m,visibility,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
        c = data.get("current", {})
        ws, wg = c.get("wind_speed_10m", 0) * 1.94384, c.get("wind_gusts_10m", 0) * 1.94384
        wd = c.get("wind_direction_10m", 0)
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return {"wind": {"speed_knots": round(ws, 1), "direction": dirs[round(wd / 22.5) % 16], "gusts_knots": round(wg, 1)},
                "waves": {"height_m": 1.0, "period_s": 5.0}, "swell": {"height_m": 0.5, "direction": "E", "period_s": 8.0},
                "visibility_km": round(c.get("visibility", 10000) / 1000, 1), "temperature_c": round(c.get("temperature_2m", 20), 1)}
    except:
        return {"wind": {"speed_knots": 0, "direction": "N", "gusts_knots": 0}, "waves": {"height_m": 0, "period_s": 0},
                "swell": {"height_m": 0, "direction": "N", "period_s": 0}, "visibility_km": 10, "temperature_c": 20}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            p = parse_qs(urlparse(self.path).query)
            lat, lng = float(p.get("lat", [0])[0]), float(p.get("lng", [0])[0])
            ds = p.get("date", [None])[0]
            d = datetime.strptime(ds, "%Y-%m-%d").date() if ds else date.today()
            pm = p.get("prayer_method", ["muslim_world_league"])[0]
            tz_name, tz_off = get_tz(lat, lng)
            solar, decl, noon = calc_solar(lat, lng, d, tz_off)
            resp = {"coordinates": {"lat": lat, "lng": lng}, "date": d.isoformat(), "timezone": tz_name,
                    "solar": solar, "prayer": calc_prayer(lat, lng, d, tz_off, decl, noon, pm),
                    "lunar": calc_lunar(d), "tides": calc_tides(calc_lunar(d)["illumination"]), "weather": get_weather(lat, lng)}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
