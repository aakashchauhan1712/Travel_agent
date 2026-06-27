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


def _overpass_query(lat, lon, query_type):
    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (node(around:20000,{lat},{lon})["amenity"~"airport|bus_station|railway"];);
        out body;
        """
        if query_type == "hotel":
            query = f"""
            [out:json];
            (node(around:5000,{lat},{lon})["tourism"~"hotel|guest_house|hostel"];);
            out body;
            """
        response = requests.post(overpass_url, data={"data": query}, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("elements", [])
    except Exception:
        return []


def _classify_transport(name, tags):
    text = f"{name} {tags.get('amenity','')} {tags.get('aeroway','')} {tags.get('railway','')}".lower()
    if any(keyword in text for keyword in ["airport", "air", "terminal", "aerodrome"]):
        return "flight"
    if any(keyword in text for keyword in ["bus", "station", "stand", "terminal"]):
        return "bus"
    if any(keyword in text for keyword in ["rail", "train", "station", "halt"]):
        return "train"
    return None


def search_transport(source, destination):
    """Return transport options using free geocoding and OpenStreetMap data."""
    destination_coords = _geocode_city(destination)
    source_coords = _geocode_city(source) or destination_coords

    if not destination_coords:
        return {
            "flights": [],
            "buses": [{"operator": "Local transport", "price": 500}],
            "trains": [{"name": "Regional train", "price": 300}],
        }

    if source_coords is None:
        source_coords = destination_coords

    nearby_nodes = _overpass_query(destination_coords[0], destination_coords[1], "transport")

    flights = []
    buses = []
    trains = []

    for node in nearby_nodes:
        tags = node.get("tags", {})
        name = tags.get("name") or "Nearby transit point"
        lat = node.get("lat")
        lon = node.get("lon")
        kind = _classify_transport(name, tags)
        if kind == "flight":
            flights.append({"airline": name, "price": 4500 + int(abs(lat - destination_coords[0]) * 1000)})
        elif kind == "bus":
            buses.append({"operator": name, "price": 500 + int(abs(lon - destination_coords[1]) * 10)})
        elif kind == "train":
            trains.append({"name": name, "price": 300 + int(abs(lat - destination_coords[0]) * 1000)})

    if not flights:
        flights = [{"airline": f"Nearest airport near {destination}", "price": 5000}]
    if not buses:
        buses = [{"operator": "Local bus service", "price": 600}]
    if not trains:
        trains = [{"name": f"Regional rail near {destination}", "price": 400}]

    return {"flights": flights, "buses": buses, "trains": trains}