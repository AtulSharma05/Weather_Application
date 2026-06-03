import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_coordinates(city: str):
    response = requests.get(
        GEOCODING_URL,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results")

    if not results:
        raise ValueError("City not found")

    city_data = results[0]

    return {
        "name": city_data["name"],
        "latitude": city_data["latitude"],
        "longitude": city_data["longitude"],
        "country": city_data.get("country"),
    }