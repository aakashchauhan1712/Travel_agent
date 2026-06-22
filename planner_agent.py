import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


from prompts.planner_prompt import planner_prompt
from weather import get_weather

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
)


def generate_itinerary(destination, days, budget):
    # Get current weather for the destination
    weather = get_weather(destination)

    prompt = planner_prompt.format(
        destination=destination,
        days=days,
        budget=budget,
        temperature=weather["temperature"],
        condition=weather["condition"]
    )
    response = llm.invoke(prompt)

    return {
        "itinerary": response.content,
        "weather": weather
    }