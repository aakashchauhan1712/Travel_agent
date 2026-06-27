import streamlit as st
from planner_agent import generate_itinerary
from rag.rag_qa import ask_travel_guidelines

st.set_page_config(
    page_title="AI Travel Planner Agent",
    page_icon="✈️",
    layout="centered",
)

st.title("AI Travel Planner Agent ✈️")

if "trip_result" not in st.session_state:
    st.session_state.trip_result = None

if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = None

source = st.text_input(
    "Where are you traveling from?",
    placeholder = "Enter your starting location..."
)

destination = st.text_input(
    "Where do you want to go?",
    placeholder = "Enter your destination..."
)

days = st.number_input(
    "Number of days you want to spend",
    min_value = 1,
    max_value = 30,
    value = 5,
    placeholder= "Enter number between 1-30"
)

budget = st.number_input(
    "Enter your Budget (₹)",
    min_value = 1000,
    value = 5000,
    step = 1000
)

generate_button = st.button("Generate trip")

if generate_button:
    if not destination:
        st.warning("Please enter a destination.")
    else:
        with st.spinner("Generating your travel itinerary..."):
            try:
                st.session_state.trip_result = generate_itinerary(
                    source,
                    destination,
                    days,
                    budget,
                )
            except Exception as exc:
                st.session_state.trip_result = None
                st.error(f"Unable to generate itinerary: {exc}")
#Setting up the UI for Itinerary with session

if st.session_state.trip_result:
    result = st.session_state.trip_result
    weather = result['weather']
    itinerary = result ['itinerary']
    transport = result['transport']
    hotels = result['hotels']

    st.subheader('Current Weather at Destination')
    st.write(f"Temperature : {weather['temperature']}°C")
    st.write(f"Condition :{weather ['condition']}")
    st.write(f"Wind Speed : {weather['wind_speed']} km/h")

    st.subheader("Available Transport Options")
    st.write("Flights:")
    for flight in transport['flights']:
        st.write(f"{flight['airline']} - ₹{flight['price']}")

    st.write("🚌 Buses:")
    for bus in transport['buses']:
        st.write(f"{bus['operator']} - ₹{bus['price']}")

    st.write("🚂 Trains:")
    for train in transport['trains']:
        st.write(f"{train['name']} - ₹{train['price']}")

    st.subheader("Recommended Hotels")
    for hotel in hotels:
        st.write(f"{hotel['name']} | Rating: {hotel['rating']} | ₹{hotel['price_per_night']}/night")
        st.divider()
    
    st.subheader("Generated Itinerary")
    st.write(itinerary)

 


with st.sidebar:

    st.header("Travel Guidelines Assistant")

    travel_question = st.text_input(
        "Ask a travel-related question",
        placeholder='eg. bali visa details'
    )

    if st.button("Get Travel Guidelines"):

        if travel_question:

            with st.spinner(
                "Fetching travel guidelines..."
            ):

                st.session_state.rag_answer = (
                    ask_travel_guidelines(
                        travel_question
                    )
                )

    if st.session_state.rag_answer:

        st.success("Answer found:")
        st.write(
            st.session_state.rag_answer
        )