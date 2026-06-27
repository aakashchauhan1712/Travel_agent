from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class TravelState(TypedDict):

    messages: Annotated[list, add_messages]

    source: str

    destination: str

    days: int

    budget: int

    weather: dict | None

    transport: dict | None

    hotels: list | None

    itinerary: str | None