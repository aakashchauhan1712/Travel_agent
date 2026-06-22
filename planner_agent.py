import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.planner_prompt import planner_prompt
from weather import get_weather
from transport import search_transport
from hotel import search_hotels

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
)


def generate_itinerary(source,destination, days, budget):
    # Get current weather for the destination
    weather = get_weather(destination)
    transport = search_transport(source,destination)
    flights = transport["flights"]
    buses = transport["buses"]
    trains = transport["trains"]
    hotels = search_hotels(
        destination,
        budget
    )
    hotel_text = "\n".join(
        [
            f"{hotel['name']} | Rating: {hotel['rating']} | ₹{hotel['price_per_night']}/night"
            for hotel in hotels
        ]
    )
    flight_text = "\n".join(
        [
            f"{f['airline']} - ₹{f['price']}"
            for f in flights
        ]
    ) or "No Flights Available"

    bus_text = "\n".join(
        [
            f"{b['operator']} - ₹{b['price']}"
            for b in buses
        ]
    ) or "No Buses Available"

    train_text = "\n".join(
        [
            f"{t['name']} - ₹{t['price']}"
            for t in trains
        ]
    ) or "No Trains Available"

    prompt = planner_prompt.format(
        destination=destination,
        days=days,
        budget=budget,
        flights=flight_text,
        buses=bus_text,
        trains=train_text,
        hotels=hotel_text,
        temperature=weather["temperature"],
        condition=weather["condition"]
    )
    response = llm.invoke(prompt)

    return {
        "itinerary": response.content,
        "weather": weather,
        "transport": transport,
        "hotels": hotels
    }