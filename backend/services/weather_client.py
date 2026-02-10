import httpx
from typing import Optional


def degrees_to_direction(degrees: float) -> str:
    """Convert wind direction in degrees to compass direction."""
    if degrees is None:
        return "N/A"

    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(degrees / 22.5) % 16
    return directions[idx]


async def fetch_marine_weather(lat: float, lng: float) -> dict:
    """Fetch marine weather data from Open-Meteo APIs."""

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Fetch marine data (waves, swell)
        marine_params = {
            "latitude": lat,
            "longitude": lng,
            "current": "wave_height,wave_period,wave_direction,swell_wave_height,swell_wave_period,swell_wave_direction"
        }

        # Fetch weather data (wind, temp, visibility)
        weather_params = {
            "latitude": lat,
            "longitude": lng,
            "current": "temperature_2m,visibility,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        }

        try:
            marine_response = await client.get(
                "https://marine-api.open-meteo.com/v1/marine",
                params=marine_params
            )
            marine_data = marine_response.json() if marine_response.status_code == 200 else {}
        except Exception:
            marine_data = {}

        try:
            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params=weather_params
            )
            weather_data = weather_response.json() if weather_response.status_code == 200 else {}
        except Exception:
            weather_data = {}

    # Extract current weather
    current_weather = weather_data.get("current", {})
    current_marine = marine_data.get("current", {})

    # Wind speed conversion: m/s to knots
    wind_speed_ms = current_weather.get("wind_speed_10m", 0)
    wind_gusts_ms = current_weather.get("wind_gusts_10m", 0)
    wind_speed_knots = round(wind_speed_ms * 1.94384, 1)
    wind_gusts_knots = round(wind_gusts_ms * 1.94384, 1)

    wind_direction = current_weather.get("wind_direction_10m", 0)

    # Visibility conversion: meters to km
    visibility_m = current_weather.get("visibility", 10000)
    visibility_km = round(visibility_m / 1000, 1)

    # Temperature
    temperature = current_weather.get("temperature_2m", 20)

    # Marine data
    wave_height = current_marine.get("wave_height", 0) or 0
    wave_period = current_marine.get("wave_period", 0) or 0
    swell_height = current_marine.get("swell_wave_height", 0) or 0
    swell_period = current_marine.get("swell_wave_period", 0) or 0
    swell_direction = current_marine.get("swell_wave_direction", 0) or 0

    return {
        "wind": {
            "speed_knots": wind_speed_knots,
            "direction": degrees_to_direction(wind_direction),
            "gusts_knots": wind_gusts_knots
        },
        "waves": {
            "height_m": round(wave_height, 1),
            "period_s": round(wave_period, 1)
        },
        "swell": {
            "height_m": round(swell_height, 1),
            "direction": degrees_to_direction(swell_direction),
            "period_s": round(swell_period, 1)
        },
        "visibility_km": visibility_km,
        "temperature_c": round(temperature, 1)
    }
