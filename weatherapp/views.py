from django.shortcuts import render
from weatherapp.services import (get_weather,parse_weather,parse_hourly_forecast,parse_daily_forecast)
from weatherapp.geocoding import get_coordinates
def home(request):
    city = request.GET.get("city", "Delhi")
    try:
        location = get_coordinates(city)
        weather_data = get_weather(
            location["latitude"],
            location["longitude"],
        )

        weather = parse_weather(weather_data)
        hourly= parse_hourly_forecast(weather_data)
        daily=parse_daily_forecast(weather_data)

    except Exception as e:
        weather = {"error": str(e)}
        location = None

    return render(
        request,
        "weatherapp/home.html",
        {
            "weather": weather,
            "city": city,
            "location": location,
            "hourly":hourly,
            "daily":daily,
        },
    )
