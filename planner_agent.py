import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.planner_prompt import planner_prompt
from config import get_google_api_key
from weather import get_weather
from transport import search_transport
from hotel import search_hotels

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=get_google_api_key(),
    temperature=0.7,
)


def generate_itinerary(
    source,
    destination,
    days,
    budget,
    weather=None,
    transport=None,
    hotels=None,
):
    weather = weather or get_weather(destination)
    transport = transport or search_transport(source, destination)
    hotels = hotels or search_hotels(destination, budget)

    hotel_text = "\n".join(
        [
            f"{hotel['name']} | Rating: {hotel['rating']} | ₹{hotel['price_per_night']}/night"
            for hotel in (hotels or [])
        ]
    ) or "No Hotels Found"

    transport = transport or {}
    flight_text = "\n".join(
        [
            f"{f['airline']} - ₹{f['price']}"
            for f in transport.get("flights", [])
        ]
    ) or "No Flights Available"

    bus_text = "\n".join(
        [
            f"{b['operator']} - ₹{b['price']}"
            for b in transport.get("buses", [])
        ]
    ) or "No Buses Available"

    train_text = "\n".join(
        [
            f"{t['name']} - ₹{t['price']}"
            for t in transport.get("trains", [])
        ]
    ) or "No Trains Available"

    weather = weather or {}
    temperature = weather.get("temperature", "N/A")
    condition = weather.get("condition", "N/A")

    prompt = planner_prompt.format(
        source=source,
        destination=destination,
        days=days,
        budget=budget,
        flights=flight_text,
        buses=bus_text,
        trains=train_text,
        hotels=hotel_text,
        temperature=temperature,
        condition=condition,
    )

    response = llm.invoke(prompt)

    return {
        "itinerary": response.content,
        "weather": weather,
        "transport": transport,
        "hotels": hotels,
    }