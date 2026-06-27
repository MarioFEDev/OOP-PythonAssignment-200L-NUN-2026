"""
weather_state.py — State for the weather dashboard.

Fetches live weather data from the Open-Meteo API using the user's
chosen city (stored in UserState). Defaults to Abuja, Nigeria.
API: https://api.open-meteo.com/v1/forecast (free, no key required)

Data fetched:
  - current: temperature, relative_humidity, wind_speed, weather_code,
             apparent_temperature, precipitation
  - daily:   weather_code, temperature_2m_max, temperature_2m_min,
             precipitation_probability_max (7 days)
  - hourly:  temperature_2m, weather_code (for 3-slot home preview)
"""

import httpx
import reflex as rx
from Project.state.user_state import UserState
from datetime import datetime


# ---------------------------------------------------------------------------
# WMO weather-code → (Lucide icon tag, human-readable label)
# Reference: https://open-meteo.com/en/docs#weathervariables
# ---------------------------------------------------------------------------
_WMO_ICON: dict[int, str] = {
    0: "sun",
    1: "sun",
    2: "cloud-sun",
    3: "cloud",
    45: "cloud-fog",
    48: "cloud-fog",
    51: "cloud-drizzle",
    53: "cloud-drizzle",
    55: "cloud-drizzle",
    61: "cloud-rain",
    63: "cloud-rain",
    65: "cloud-rain",
    71: "cloud-snow",
    73: "cloud-snow",
    75: "cloud-snow",
    80: "cloud-rain",
    81: "cloud-rain",
    82: "cloud-rain",
    95: "cloud-lightning",
    96: "cloud-lightning",
    99: "cloud-lightning",
}

_WMO_LABEL: dict[int, str] = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Icy Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Slight Showers",
    81: "Moderate Showers",
    82: "Heavy Showers",
    95: "Thunderstorm",
    96: "Thunderstorm w/ Hail",
    99: "Thunderstorm w/ Hail",
}

# Short day-name abbreviations
_DAY_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Open-Meteo base URL
_BASE_URL = "https://api.open-meteo.com/v1/forecast"


def _wmo_icon(code: int) -> str:
    """Return a Lucide icon tag for the given WMO weather code."""
    return _WMO_ICON.get(code, "cloud")


def _wmo_label(code: int) -> str:
    """Return a human-readable label for the given WMO weather code."""
    return _WMO_LABEL.get(code, "Unknown")


class WeatherState(rx.State):
    """
    Manages all weather-related data for the app.

    Live data is fetched from Open-Meteo on page load via
    fetch_weather(). All temperatures are in °C.

    State vars:
        city               — Display name of the city
        current_temp       — Current temperature (°C, int)
        feels_like         — Apparent temperature (°C, int)
        current_condition  — Human-readable weather description
        current_icon       — Lucide icon tag for current conditions
        humidity           — Relative humidity with % suffix
        wind_speed         — Wind speed with km/h suffix
        rain_chance        — Precipitation probability with % suffix
        hourly_preview     — 3-slot list for the home-page weather card
        weekly_forecast    — 7-day forecast list for weather page grid
        is_loading         — True while a fetch is in progress
        error_message      — Non-empty if the last fetch failed
        last_updated       — Timestamp string of the last successful fetch
    """

    # ---- Location (driven by UserState) ----
    city: str = "Abuja"

    # ---- Current Conditions ----
    current_temp: int = 0
    feels_like: int = 0
    current_condition: str = "Loading…"
    current_icon: str = "cloud"

    # ---- Weather Stats ----
    humidity: str = "—"
    wind_speed: str = "—"
    rain_chance: str = "—"

    # ---- Hourly Preview (for Home Page) ----
    # Each entry: time label, icon name, temperature
    hourly_preview: list[dict[str, str]] = [
        {"time": "Now", "icon": "cloud", "temp": "—°"},
        {"time": "3 PM", "icon": "cloud", "temp": "—°"},
        {"time": "6 PM", "icon": "cloud", "temp": "—°"},
    ]

    # ---- Weekly Forecast ----
    # Each entry: day name, icon, high temp (°C), low temp (°C)
    weekly_forecast: list[dict[str, str]] = [
        {"day": "Mon", "icon": "cloud", "high": "—°", "low": "—°"},
        {"day": "Tue", "icon": "cloud", "high": "—°", "low": "—°"},
        {"day": "Wed", "icon": "cloud", "high": "—°", "low": "—°"},
        {"day": "Thu", "icon": "cloud", "high": "—°", "low": "—°"},
        {"day": "Fri", "icon": "cloud", "high": "—°", "low": "—°"},
        {"day": "Sat", "icon": "cloud", "high": "—°", "low": "—°"},
        {"day": "Sun", "icon": "cloud", "high": "—°", "low": "—°"},
    ]

    # ---- UI Control ----
    is_loading: bool = False
    error_message: str = ""
    last_updated: str = ""

    # ---- Event Handlers ----

    @rx.event
    async def fetch_weather(self):
        """
        Fetch live weather data from Open-Meteo for the user's city.

        Reads lat/lon from UserState (set during onboarding).
        Called on page load and on manual refresh.
        """
        self.is_loading = True
        self.error_message = ""
        yield

        # Pull coordinates from UserState
        user_state = await self.get_state(UserState)
        try:
            lat = float(user_state.location_lat)
            lon = float(user_state.location_lon)
        except (ValueError, TypeError):
            lat, lon = 9.0579, 7.4951
        self.city = user_state.display_city

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "weather_code",
                "wind_speed_10m",
                "precipitation",
            ],
            "hourly": [
                "temperature_2m",
                "weather_code",
                "precipitation_probability",
            ],
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
            ],
            "forecast_days": 7,
            "timezone": "auto",
            "wind_speed_unit": "kmh",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()

            # ---- Parse current conditions ----
            current = data.get("current", {})
            temp = int(round(current.get("temperature_2m", 0)))
            feels = int(round(current.get("apparent_temperature", temp)))
            humidity_val = int(round(current.get("relative_humidity_2m", 0)))
            wind_val = int(round(current.get("wind_speed_10m", 0)))
            code = int(current.get("weather_code", 0))

            self.current_temp = temp
            self.feels_like = feels
            self.current_condition = _wmo_label(code)
            self.current_icon = _wmo_icon(code)
            self.humidity = f"{humidity_val}%"
            self.wind_speed = f"{wind_val} km/h"

            # ---- Parse hourly for rain chance (today average) ----
            hourly = data.get("hourly", {})
            precip_probs: list[int] = hourly.get(
                "precipitation_probability", []
            )[:24]
            if precip_probs:
                avg_rain = int(round(sum(precip_probs) / len(precip_probs)))
            else:
                avg_rain = 0
            self.rain_chance = f"{avg_rain}%"

            # ---- Build hourly_preview (Now, +3h, +6h) ----
            hourly_times: list[str] = hourly.get("time", [])
            hourly_temps: list[float] = hourly.get("temperature_2m", [])
            hourly_codes: list[int] = hourly.get("weather_code", [])

            now_hour = datetime.now().hour
            preview_slots: list[dict[str, str]] = []
            offsets = [0, 3, 6]
            labels = ["Now", "+3h", "+6h"]

            for i, offset in enumerate(offsets):
                idx = now_hour + offset
                if idx < len(hourly_temps):
                    slot_temp = int(round(hourly_temps[idx]))
                    slot_code = int(hourly_codes[idx]) if idx < len(hourly_codes) else 0
                    slot_icon = _wmo_icon(slot_code)
                else:
                    slot_temp = temp
                    slot_icon = _wmo_icon(code)
                preview_slots.append(
                    {
                        "time": labels[i],
                        "icon": slot_icon,
                        "temp": f"{slot_temp}°",
                    }
                )

            self.hourly_preview = preview_slots

            # ---- Build weekly_forecast (7 days) ----
            daily = data.get("daily", {})
            daily_dates: list[str] = daily.get("time", [])
            daily_codes: list[int] = daily.get("weather_code", [])
            daily_highs: list[float] = daily.get("temperature_2m_max", [])
            daily_lows: list[float] = daily.get("temperature_2m_min", [])

            forecast: list[dict[str, str]] = []
            for i in range(min(7, len(daily_dates))):
                # Parse "YYYY-MM-DD" to get weekday name
                try:
                    dt = datetime.strptime(daily_dates[i], "%Y-%m-%d")
                    day_name = _DAY_ABBR[dt.weekday()]
                except (ValueError, IndexError):
                    day_name = "—"

                d_code = int(daily_codes[i]) if i < len(daily_codes) else 0
                d_high = int(round(daily_highs[i])) if i < len(daily_highs) else 0
                d_low = int(round(daily_lows[i])) if i < len(daily_lows) else 0

                forecast.append(
                    {
                        "day": day_name,
                        "icon": _wmo_icon(d_code),
                        "high": f"{d_high}°",
                        "low": f"{d_low}°",
                    }
                )

            self.weekly_forecast = forecast

            # ---- Update timestamp ----
            self.last_updated = datetime.now().strftime("%H:%M")

        except httpx.TimeoutException:
            self.error_message = "Request timed out. Check your connection."
        except httpx.HTTPStatusError as e:
            self.error_message = f"API error: {e.response.status_code}"
        except Exception as e:
            self.error_message = f"Offline Mode. Using simulated data. ({str(e)})"
            self.city = "Sim City (Offline)"
            self.current_temp = 28
            self.feels_like = 30
            self.current_condition = "Sunny"
            self.current_icon = "sun"
            self.humidity = "45%"
            self.wind_speed = "12 km/h"
            self.rain_chance = "10%"
            self.hourly_preview = [
                {"time": "Now", "icon": "sun", "temp": "28°"},
                {"time": "+3h", "icon": "cloud-sun", "temp": "26°"},
                {"time": "+6h", "icon": "cloud", "temp": "24°"},
            ]
            self.weekly_forecast = [
                {"day": "Mon", "icon": "sun", "high": "30°", "low": "22°"},
                {"day": "Tue", "icon": "cloud", "high": "28°", "low": "21°"},
                {"day": "Wed", "icon": "cloud-rain", "high": "25°", "low": "20°"},
                {"day": "Thu", "icon": "sun", "high": "29°", "low": "22°"},
                {"day": "Fri", "icon": "cloud-sun", "high": "27°", "low": "21°"},
                {"day": "Sat", "icon": "sun", "high": "31°", "low": "23°"},
                {"day": "Sun", "icon": "cloud", "high": "26°", "low": "20°"},
            ]
            self.last_updated = datetime.now().strftime("%H:%M")
        finally:
            self.is_loading = False
