import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from tools.tool_registry import TOOLS

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

llm_with_tools = llm.bind_tools(TOOLS)

def run_agent(query):

    response = llm_with_tools.invoke(query)

    if not response.tool_calls:
        return response.content

    tool_call = response.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    selected_tool = None

    for tool in TOOLS:
        if tool.name == tool_name:
            selected_tool = tool
            break

    if selected_tool is None:
        return "Tool not found."

    tool_result = selected_tool.invoke(tool_args)

    final_prompt = f"""
User Question:
{query}

Tool Used:
{tool_name}

Tool Result:
{tool_result}

Provide a helpful response to the user.
"""

    final_response = llm.invoke(
        final_prompt
    )

    return final_response.content