import os
from urllib import response
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
    print("\nTool Calls:")
    print(response.tool_calls)

    if not response.tool_calls:
        return response.content

    tool_results = []

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = None

        for tool in TOOLS:
            if tool.name == tool_name:
                selected_tool = tool
                break

        if selected_tool is None:
            continue

        result = selected_tool.invoke(tool_args)

        tool_results.append(
            {
                "tool": tool_name,
                "result": result
            }
        )

    final_prompt = f"""
User Question:
{query}

Tool Results:
{tool_results}

Using the tool results above,
provide a complete and helpful response.
"""

    final_response = llm.invoke(final_prompt)

    return final_response.content