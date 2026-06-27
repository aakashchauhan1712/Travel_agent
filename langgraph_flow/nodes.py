import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage
from langgraph.graph import END

from tools.tool_registry import TOOLS

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

llm_with_tools = llm.bind_tools(TOOLS)

def agent_node(state):
    response = llm_with_tools.invoke(
        state['messages']
    )
    return {
        'messages':[response]
    }

def should_use_tool(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool"
    return END

from langchain_core.messages import ToolMessage

def tool_node(state):

    last_message = state["messages"][-1]

    tool_call = last_message.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    for tool in TOOLS:

        if tool.name == tool_name:

            result = tool.invoke(tool_args)

            return {
                "messages": [
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"]
                    )
                ]
            }

    return {
        "messages": [
            ToolMessage(
                content="Tool not found.",
                tool_call_id=tool_call["id"]
            )
        ]
    }