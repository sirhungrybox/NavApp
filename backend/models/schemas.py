from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class TwilightTimes(BaseModel):
    dawn: str
    dusk: str


class Twilight(BaseModel):
    civil: TwilightTimes
    nautical: TwilightTimes
    astronomical: TwilightTimes


class SolarData(BaseModel):
    sunrise: str
    sunset: str
    solar_noon: str
    day_length: str
    twilight: Twilight


class PrayerData(BaseModel):
    fajr: str
    sunrise: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str
    method: str


class LunarData(BaseModel):
    phase: str
    illumination: float
    moonrise: Optional[str]
    moonset: Optional[str]
    next_full_moon: str
    next_new_moon: str


class TideData(BaseModel):
    tendency: str
    description: str
    moon_phase_factor: float


class Wind(BaseModel):
    speed_knots: float
    direction: str
    gusts_knots: float


class Waves(BaseModel):
    height_m: float
    period_s: float


class Swell(BaseModel):
    height_m: float
    direction: str
    period_s: float


class WeatherData(BaseModel):
    wind: Wind
    waves: Waves
    swell: Swell
    visibility_km: float
    temperature_c: float


class DashboardResponse(BaseModel):
    coordinates: Coordinates
    date: str
    timezone: str
    solar: SolarData
    prayer: PrayerData
    lunar: LunarData
    tides: TideData
    weather: WeatherData
