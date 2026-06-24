import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.tool_registry import TOOLS


load_dotenv()

llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        google_api_key = os.getenv("GOOGLE_API_KEY")
)


llm_with_tools = llm.bind_tools(TOOLS)

query = "What is the current weather in New York City?"

response = llm_with_tools.invoke(query)

print(response)