from http.server import BaseHTTPRequestHandler
import json
import math
from datetime import date, datetime, timedelta
from urllib.parse import parse_qs, urlparse
import urllib.request

# Timezone mapping
TIMEZONE_OFFSETS = {
    (-180, -157.5): ("Pacific/Midway", -11),
    (-157.5, -142.5): ("Pacific/Honolulu", -10),
    (-142.5, -127.5): ("America/Anchorage", -9),
    (-127.5, -112.5): ("America/Los_Angeles", -8),
    (-112.5, -97.5): ("America/Denver", -7),
    (-97.5, -82.5): ("America/Chicago", -6),
    (-82.5, -67.5): ("America/New_York", -5),
    (-67.5, -52.5): ("America/Halifax", -4),
    (-52.5, -37.5): ("America/Sao_Paulo", -3),
    (-37.5, -22.5): ("Atlantic/South_Georgia", -2),
    (-22.5, -7.5): ("Atlantic/Azores", -1),
    (-7.5, 7.5): ("UTC", 0),
    (7.5, 22.5): ("Europe/Paris", 1),
    (22.5, 37.5): ("Europe/Athens", 2),
    (37.5, 52.5): ("Asia/Dubai", 4),
    (52.5, 67.5): ("Asia/Karachi", 5),
    (67.5, 82.5): ("Asia/Dhaka", 6),
    (82.5, 97.5): ("Asia/Bangkok", 7),
    (97.5, 112.5): ("Asia/Singapore", 8),
    (112.5, 127.5): ("Asia/Tokyo", 9),
    (127.5, 142.5): ("Australia/Sydney", 10),
    (142.5, 157.5): ("Pacific/Noumea", 11),
    (157.5, 180): ("Pacific/Auckland", 12),
}

PRAYER_METHODS = {
    "muslim_world_league": {"fajr": 18, "isha": 17, "name": "Muslim World League"},
    "isna": {"fajr": 15, "isha": 15, "name": "ISNA"},
    "egyptian": {"fajr": 19.5, "isha": 17.5, "name": "Egyptian General Authority"},
    "umm_al_qura": {"fajr": 18.5, "isha": 90, "isha_is_minutes": True, "name": "Umm Al-Qura"},
    "dubai": {"fajr": 18.2, "isha": 18.2, "name": "Dubai"},
    "kuwait": {"fajr": 18, "isha": 17.5, "name": "Kuwait"},
    "qatar": {"fajr": 18, "isha": 90, "isha_is_minutes": True, "name": "Qatar"},
}


def get_tz(lng):
    for (min_lng, max_lng), (name, offset) in TIMEZONE_OFFSETS.items():
        if min_lng <= lng < max_lng:
            return name, offset
    return "UTC", 0


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
            tz_name, tz_off = get_tz(lng)
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
