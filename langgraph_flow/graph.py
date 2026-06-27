from langgraph.graph import StateGraph, START, END

from langgraph_flow.state import TravelState

from langgraph_flow.nodes import (
    agent_node,
    tool_node,
    should_use_tool
)

builder = StateGraph(TravelState)

# Add Nodes
builder.add_node("agent", agent_node)
builder.add_node("tool", tool_node)
# Start
builder.add_edge(START, "agent")

# Decision after the agent
builder.add_conditional_edges(
    "agent",
    should_use_tool,
    {
        "tool": "tool",
        END : END
    }
)

builder.add_edge(
    "tool",
    "agent"
)

travel_graph = builder.compile()