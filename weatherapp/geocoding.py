import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
REVERSE_GEOCODING_URL = "https://nominatim.openstreetmap.org/reverse"


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


def get_location_name(latitude: float, longitude: float):
    response = requests.get(
        REVERSE_GEOCODING_URL,
        params={
            "format": "json",
            "lat": latitude,
            "lon": longitude,
            "addressdetails": 1,
        },
        headers={"User-Agent": "weather-app/1.0"},
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    address = data.get("address", {})

    name = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("county")
        or data.get("display_name", f"{round(latitude, 2)}, {round(longitude, 2)}")
    )

    return {
        "name": name,
        "latitude": data.get("lat", latitude),
        "longitude": data.get("lon", longitude),
        "country": address.get("country_code", address.get("country")),
    }