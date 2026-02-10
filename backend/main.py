from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime
from typing import Optional

from services.astronomy import (
    get_timezone_from_coords,
    calculate_solar,
    calculate_lunar,
    calculate_tides
)
from services.prayer_times import calculate_prayer_times, METHODS
from services.weather_client import fetch_marine_weather

app = FastAPI(
    title="NavApp API",
    description="Ocean Navigator Daily Productivity App API",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "NavApp API is running", "version": "1.0.0"}


@app.get("/api/v1/dashboard")
async def get_dashboard(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    date_str: Optional[str] = Query(None, alias="date"),
    timezone: Optional[str] = Query(None),
    prayer_method: str = Query("muslim_world_league")
):
    """Get all navigation data in a single response."""

    # Parse date or use today
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    # Get timezone from coordinates if not provided
    if not timezone:
        timezone = get_timezone_from_coords(lat, lng)

    # Calculate all data
    solar = calculate_solar(lat, lng, target_date, timezone)
    prayer = calculate_prayer_times(lat, lng, target_date, timezone, prayer_method)
    lunar = calculate_lunar(lat, lng, target_date, timezone)
    tides = calculate_tides(lunar["illumination"])
    weather = await fetch_marine_weather(lat, lng)

    return {
        "coordinates": {"lat": lat, "lng": lng},
        "date": target_date.isoformat(),
        "timezone": timezone,
        "solar": solar,
        "prayer": prayer,
        "lunar": lunar,
        "tides": tides,
        "weather": weather
    }


@app.get("/api/v1/solar")
async def get_solar(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    date_str: Optional[str] = Query(None, alias="date"),
    timezone: Optional[str] = Query(None)
):
    """Get sunrise, sunset, and twilight times."""
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    if not timezone:
        timezone = get_timezone_from_coords(lat, lng)

    return calculate_solar(lat, lng, target_date, timezone)


@app.get("/api/v1/prayer")
async def get_prayer(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    date_str: Optional[str] = Query(None, alias="date"),
    timezone: Optional[str] = Query(None),
    method: str = Query("muslim_world_league")
):
    """Get Islamic prayer times."""
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    if not timezone:
        timezone = get_timezone_from_coords(lat, lng)

    return calculate_prayer_times(lat, lng, target_date, timezone, method)


@app.get("/api/v1/prayer/methods")
async def get_prayer_methods():
    """Get available prayer calculation methods."""
    return {key: value["name"] for key, value in METHODS.items()}


@app.get("/api/v1/lunar")
async def get_lunar(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    date_str: Optional[str] = Query(None, alias="date"),
    timezone: Optional[str] = Query(None)
):
    """Get moon phase and moonrise/moonset times."""
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    if not timezone:
        timezone = get_timezone_from_coords(lat, lng)

    return calculate_lunar(lat, lng, target_date, timezone)


@app.get("/api/v1/tides")
async def get_tides(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    date_str: Optional[str] = Query(None, alias="date"),
    timezone: Optional[str] = Query(None)
):
    """Get tide tendency based on moon phase."""
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    if not timezone:
        timezone = get_timezone_from_coords(lat, lng)

    lunar = calculate_lunar(lat, lng, target_date, timezone)
    return calculate_tides(lunar["illumination"])


@app.get("/api/v1/weather")
async def get_weather(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180)
):
    """Get marine weather data."""
    return await fetch_marine_weather(lat, lng)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
