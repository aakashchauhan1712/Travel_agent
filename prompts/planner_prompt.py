from langchain.prompts import PromptTemplate

planner_prompt = PromptTemplate(
    input_variables=["destination", "days", "budget", "hotels"],
    template="""You are an expert travel planner.

Create a detailed travel itinerary based on:

Destination: {destination}
Number of Days: {days}
Budget: ₹{budget}

Current weather :

Temperature : {temperature}°C
Condition : {condition}

Available Transport :

Flights : {flights}
Buses : {buses}
Trains : {trains}

Recommended hotels : {hotels}

Current weather is important to consider while planning the trip. Please take it into account while creating the itinerary.

Instructions:
- Create a day-by-day itinerary.
- Keep activities realistic.
- Stay within the user's budget.
- Avoid outdoor activities if weather is rainy.
- Include estimated spending suggestions.
- Format the response clearly.

Travel Plan:"""
)