import requests

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

    Args:
        city (str): Name of the city

    Returns:
        dict: Weather information
    """

    # Step 1: Convert city name to latitude & longitude
    geo_url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1"
    )

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    # Check if city was found
    if "results" not in geo_data:
        return {
            "error": f"Could not find city: {city}"
        }

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    # Step 2: Get current weather
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,weather_code,wind_speed_10m"
    )

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    current = weather_data["current"]

    weather_code = current["weather_code"]

    return {
        "city": city,
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": WEATHER_CODES.get(
            weather_code,
            "Unknown"
        )
    }


# Test block
if __name__ == "__main__":

    city = "Lucknow"

    weather = get_weather(city)

    print(weather)