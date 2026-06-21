import streamlit as st

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
    st.success('Trip Request received! Generating your trip plan...')

    st.write(f"**Destination:** {destination}")
    st.write("Days",days)
    st.write("Budget",budget)
