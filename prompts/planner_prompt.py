from langchain.prompts import PromptTemplate

planner_prompt = PromptTemplate(
    input_variables=["destination", "days", "budget"],
    template="""You are an expert travel planner.

Create a detailed travel itinerary based on:

Destination: {destination}
Number of Days: {days}
Budget: ₹{budget}

Instructions:
- Create a day-by-day itinerary.
- Keep activities realistic.
- Stay within the user's budget.
- Include estimated spending suggestions.
- Format the response clearly.

Travel Plan:"""
)