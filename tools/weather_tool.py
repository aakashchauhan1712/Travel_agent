from langchain.tools import tool
from weather import get_weather

@tool
def weather_tool(City: str) -> str:
    '''Get the current weather for a given city.'''
    return get_weather(City)