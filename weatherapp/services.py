from weatherapp.constants import (WEATHER_CODES,WEATHER_ICONS,)
from datetime import datetime
API_URL = "https://api.open-meteo.com/v1/forecast"
import requests
def get_weather(lat: str, lon: str):
    params = {
        "latitude": lat,
        "longitude": lon,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "pressure_msl",
              "visibility",
                 "is_day",

        ],

        "hourly": [
            "temperature_2m",
             "weather_code",
        ],

        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
        ],

        "forecast_days": 7,
        "timezone": "auto",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()



def get_weather_theme(code):
    if code in [0, 1]:
        return "sunny"
    if code in [2, 3]:
        return "cloudy"
    if code in [45, 48]:
        return "foggy"
    if code in [51, 53, 55, 61, 63, 65, 80, 95]:
        return "rainy"
    if code in [71]:
        return "snowy"
    return "default"

def parse_weather(data):
    current = data["current"]

    return {
    "temperature": current.get("temperature_2m"),
    "humidity": current.get("relative_humidity_2m"),
    "feels_like": current.get("apparent_temperature"),
    "wind_speed": current.get("wind_speed_10m"),
    "precipitation": current.get("precipitation", 0),
    "code": current.get("weather_code"),
    "theme": get_weather_theme(current.get("weather_code")),
    "condition": WEATHER_CODES.get(
        current.get("weather_code"),
        "Unknown"
    ),
    "pressure": current.get("pressure_msl"),
        "visibility": round(current.get("visibility", 0) / 1000, 1),
        "is_day": bool(current.get("is_day")),
    "icon": WEATHER_ICONS.get( current.get("weather_code"),"🌍"),
}

from datetime import datetime


def parse_hourly_forecast(data: dict) -> list[dict]:
    hourly = data.get("hourly", {})

    times = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    weather_codes = hourly.get("weather_code", [])

    current_hour = datetime.now().replace(
        minute=0,
        second=0,
        microsecond=0,
    )

    start_index = 0

    for i, time_str in enumerate(times):
        forecast_time = datetime.fromisoformat(time_str)

        if forecast_time >= current_hour:
            start_index = i
            break

    end_index = start_index + 24

    return [
        {
            "time": datetime.fromisoformat(time_str).strftime("%H:%M"),
            "temperature": temp,
            "condition": WEATHER_CODES.get(
                code,
                "Unknown",
            ),
            "icon": WEATHER_ICONS.get(
                code,
                "☁️",
            ),
        }
        for time_str, temp, code in zip(
            times[start_index:end_index],
            temperatures[start_index:end_index],
            weather_codes[start_index:end_index],
        )
    ]

def parse_daily_forecast(data: dict) -> list[dict]:
    daily = data.get("daily", {})

    dates = daily.get("time", [])[:7]
    highs = daily.get("temperature_2m_max", [])[:7]
    lows = daily.get("temperature_2m_min", [])[:7]
    weather_codes = daily.get("weather_code", [])[:7]

    forecast = []

    for date, high, low, code in zip(
        dates,
        highs,
        lows,
        weather_codes,
    ):
        day_name = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%a")

        forecast.append(
            {
                "date": day_name,
                "high": high,
                "low": low,
                "condition": WEATHER_CODES.get(
                    code,
                    "Unknown"
                ),
                "icon": WEATHER_ICONS.get(
                    code,
                    "☁️"
                ),
            }
        )

    return forecast