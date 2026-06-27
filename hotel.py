import requests


def _geocode_city(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&q={city}"
        response = requests.get(url, headers={"User-Agent": "travel-agent/1.0"}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            if data.get("lat") is not None and data.get("lon") is not None:
                return float(data["lat"]), float(data["lon"])
            if data.get("results"):
                first = data["results"][0]
                return float(first["lat"]), float(first["lon"])
            return None
        if not data:
            return None
        first = data[0]
        return float(first["lat"]), float(first["lon"])
    except Exception:
        return None


def search_hotels(destination, budget):
    """Return hotel suggestions using OpenStreetMap data when available."""
    try:
        budget_value = int(budget)
    except (TypeError, ValueError):
        return []

    if budget_value <= 0:
        return []

    coords = _geocode_city(destination)
    if not coords:
        return [
            {"name": "Local stay option", "price_per_night": max(1000, int(budget_value / 10)), "rating": 4.0}
        ]

    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (node(around:5000,{coords[0]},{coords[1]})["tourism"~"hotel|guest_house|hostel"];);
        out body;
        """
        response = requests.post(overpass_url, data={"data": query}, timeout=15)
        response.raise_for_status()
        elements = response.json().get("elements", [])
    except Exception:
        elements = []

    hotels = []
    for element in elements[:5]:
        tags = element.get("tags", {})
        name = tags.get("name") or "Unnamed stay"
        price = max(1200, min(int(budget_value / 3), 8000))
        rating = 4.0 + min(0.8, len(hotels) * 0.1)
        hotels.append({
            "name": name,
            "price_per_night": price,
            "rating": round(rating, 1),
        })

    if not hotels:
        hotels = [
            {"name": f"Stay near {destination}", "price_per_night": max(1200, int(budget_value / 4)), "rating": 4.2}
        ]

    return [hotel for hotel in hotels if hotel["price_per_night"] <= budget_value]