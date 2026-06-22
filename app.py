import streamlit as st
from planner_agent import generate_itinerary

st.set_page_config(
    page_title = "AI Travel Planner Agent",
    page_icon = "✈️",
    layout = 'centered'
)

st.title("AI Travel Planner Agent ✈️")

destination = st.text_input(
    "Where do you want to go?",
    placeholder = 'Goa'
)

days = st.number_input(
    "Number of days you want to spend",
    min_value = 1,
    max_value = 30,
    value = 5
)

budget = st.number_input(
    "Enter your Budget (₹)",
    min_value = 1000,
    value = 50000,
    step = 1000
)

generate_button = st.button("Generate trip")

if generate_button:
    if not destination:
        st.warning("Please enter a destination.")
    else:
        with st.spinner("Generating your travel itinerary..."):
            result = generate_itinerary(destination, days, budget)
            weather = result['weather']
            itinerary = result["itinerary"]
            st.subheader("Current Weather")
            st.write(f"Temperature :{weather['temperature']} °C")
            st.write(f"Condition :{weather['condition']}")
            st.write(f"Wind Speed :{weather['wind_speed']} Km/h")
            st.subheader("Your Travel Itinerary")
            st.markdown(itinerary)