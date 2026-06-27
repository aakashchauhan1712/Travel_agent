from langchain_core.messages import AIMessage

from planner_agent import generate_itinerary


def planner_node(state):

    source = state["source"]
    destination = state["destination"]
    days = state["days"]
    budget = state["budget"]

    itinerary = generate_itinerary(
        source=source,
        destination=destination,
        days=days,
        budget=budget,
        weather=state["weather"],
        transport=state["transport"],
        hotels=state["hotels"]
    )

    return {
        "itinerary": itinerary,
        "messages": [
            AIMessage(content=itinerary)
        ]
    }