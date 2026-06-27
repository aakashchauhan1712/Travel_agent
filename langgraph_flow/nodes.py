import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage, AIMessage

from tools.tool_registry import TOOLS
from config import get_google_api_key

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=get_google_api_key()
)

llm_with_tools = llm.bind_tools(TOOLS)


# -------------------------------------------------------
# Node 1: Agent
# -------------------------------------------------------
# Sends the current messages to the LLM.
# The LLM decides whether to call a tool or stop.
# -------------------------------------------------------
def agent_node(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# -------------------------------------------------------
# Conditional Edge: should_use_tool
# -------------------------------------------------------
# Checks the last LLM response.
# If it has tool calls → go to "tool" node.
# If no tool calls     → go to "planner" node.
# -------------------------------------------------------
def should_use_tool(state):
    messages = state.get("messages", [])
    if not messages:
        return "planner"

    last_message = messages[-1]
    if getattr(last_message, "tool_calls", None):
        return "tool"
    return "planner"


# -------------------------------------------------------
# Node 2: Tool
# -------------------------------------------------------
# Gemini sometimes calls multiple tools at once
# (e.g. weather + transport + hotel in one shot).
# We loop through ALL tool_calls so none are missed.
# Each result is stored as a ToolMessage AND saved
# into the state (weather / transport / hotels).
# -------------------------------------------------------
def tool_node(state):
    messages = state.get("messages", [])
    if not messages:
        return state

    last_message = messages[-1]
    tool_messages = []
    state_updates = {}

    for tool_call in getattr(last_message, "tool_calls", []) or []:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        for tool in TOOLS:
            if tool.name == tool_name:
                try:
                    result = tool.invoke(tool_args)
                except Exception as exc:
                    tool_messages.append(
                        ToolMessage(
                            content=f"Tool error: {exc}",
                            tool_call_id=tool_call["id"]
                        )
                    )
                    break

                tool_messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"]
                    )
                )

                if tool_name == "weather_tool":
                    state_updates["weather"] = result
                elif tool_name == "transport_tool":
                    state_updates["transport"] = result
                elif tool_name == "hotel_tool":
                    state_updates["hotels"] = result

                break

    return {"messages": tool_messages, **state_updates}