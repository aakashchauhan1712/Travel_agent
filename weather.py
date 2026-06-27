import requests
from urllib.parse import quote

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    95: "Thunderstorm"
}

def get_weather(city):
    """
    Fetch current weather information for a given city.
    """

    city_name = (city or "").strip()
    if not city_name:
        return {"error": "Please provide a city name."}

    try:
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={quote(city_name)}&count=1"
        )
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
    except requests.RequestException:
        return {"error": f"Could not fetch location data for {city_name}."}
    except ValueError:
        return {"error": f"Could not parse location data for {city_name}."}

    if "results" not in geo_data or not geo_data["results"]:
        return {"error": f"Could not find city: {city_name}"}

    try:
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            "&current=temperature_2m,weather_code,wind_speed_10m"
        )
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        current = weather_data["current"]
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return {"error": f"Could not fetch weather for {city_name}."}

    weather_code = current["weather_code"]

    return {
        "city": city_name,
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": WEATHER_CODES.get(weather_code, "Unknown")
    }


# Test block
if __name__ == "__main__":

    city = "Lucknow"

    weather = get_weather(city)

    print(weather)