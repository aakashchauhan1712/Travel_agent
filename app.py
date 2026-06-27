import os
import streamlit as st

from config import get_google_api_key

# -------------------------------------------------------
# API Key Setup
# -------------------------------------------------------
# On Streamlit Cloud → add GOOGLE_API_KEY in the Secrets
#   dashboard (App settings → Secrets)
# Locally → it reads from your .env file as before
# -------------------------------------------------------
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()

os.environ["GOOGLE_API_KEY"] = get_google_api_key() or os.getenv("GOOGLE_API_KEY") or ""

from langchain_core.messages import HumanMessage
from langgraph_flow.graph import travel_graph
from rag.rag_qa import ask_travel_guidelines

# ---- Page Config ----
st.set_page_config(
    page_title="AI Travel Planner Agent",
    page_icon="✈️",
    layout="centered"
)

st.title("AI Travel Planner Agent ✈️")

# ---- Session State ----
# We store results here so they survive Streamlit re-runs
if "trip_result" not in st.session_state:
    st.session_state.trip_result = None

if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = None

# ---- User Inputs ----
source = st.text_input("Where are you traveling from?")

destination = st.text_input(
    "Where do you want to go?",
    placeholder="Goa"
)

days = st.number_input(
    "Number of days you want to spend",
    min_value=1,
    max_value=30,
    value=5
)

budget = st.number_input(
    "Enter your Budget (₹)",
    min_value=1000,
    value=50000,
    step=1000
)

generate_button = st.button("Generate Trip")

# ---- Generate Trip ----
if generate_button:

    if not destination:
        st.warning("Please enter a destination.")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("Please add GOOGLE_API_KEY to your environment or Streamlit secrets before generating a trip.")
    else:

        with st.spinner("Generating your travel itinerary..."):

            # This is the message we send to the LangGraph agent.
            # It tells the agent to call all 3 tools: weather, transport, hotels.
            user_message = f"""
Plan a {days} day trip.
Source: {source}
Destination: {destination}
Budget: ₹{budget}

Please use the tools to:
1. Get the weather for {destination}
2. Find transport options from {source} to {destination}
3. Find hotels in {destination} within budget ₹{budget}
"""

            # Initial state passed into the LangGraph graph.
            # The graph will fill in weather, transport, hotels, and itinerary.
            initial_state = {
                "messages": [HumanMessage(content=user_message)],
                "source": source,
                "destination": destination,
                "days": int(days),
                "budget": int(budget),
                "weather": None,
                "transport": None,
                "hotels": None,
                "itinerary": None,
            }

            # Run the LangGraph agent — this handles everything automatically
            result = travel_graph.invoke(initial_state)

            # Save the result to session state
            st.session_state.trip_result = result

# ---- Display Results ----
if st.session_state.trip_result:

    result = st.session_state.trip_result

    weather   = result.get("weather")
    transport = result.get("transport")
    hotels    = result.get("hotels")
    itinerary = result.get("itinerary")

    # Weather
    if weather:
        st.subheader("🌤️ Current Weather at Destination")
        st.write(f"Temperature : {weather['temperature']}°C")
        st.write(f"Condition   : {weather['condition']}")
        st.write(f"Wind Speed  : {weather['wind_speed']} km/h")

    # Transport
    if transport:
        st.subheader("🚀 Available Transport Options")

        st.write("✈️ Flights:")
        for flight in transport.get("flights", []):
            st.write(f"  {flight['airline']} — ₹{flight['price']}")

        st.write("🚌 Buses:")
        for bus in transport.get("buses", []):
            st.write(f"  {bus['operator']} — ₹{bus['price']}")

        st.write("🚂 Trains:")
        for train in transport.get("trains", []):
            st.write(f"  {train['name']} — ₹{train['price']}")

    # Hotels
    if hotels:
        st.subheader("🏨 Recommended Hotels")
        for hotel in hotels:
            st.write(
                f"{hotel['name']} | "
                f"Rating: {hotel['rating']} | "
                f"₹{hotel['price_per_night']}/night"
            )
            st.divider()

    # Itinerary
    if itinerary:
        st.subheader("📋 Generated Itinerary")
        st.write(itinerary)

# ---- Sidebar: Travel Guidelines (RAG) ----
with st.sidebar:

    st.header("Travel Guidelines Assistant")

    travel_question = st.text_input("Ask a travel-related question")

    if st.button("Get Travel Guidelines"):
        if travel_question:
            with st.spinner("Fetching travel guidelines..."):
                st.session_state.rag_answer = ask_travel_guidelines(travel_question)

    if st.session_state.rag_answer:
        st.success("Answer found:")
        st.write(st.session_state.rag_answer)