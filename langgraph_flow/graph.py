from langgraph.graph import StateGraph, START, END

from langgraph_flow.state import TravelState
from langgraph_flow.nodes import agent_node, tool_node, should_use_tool
from langgraph_flow.planner_node import planner_node

# -------------------------------------------------------
# Graph Flow:
#
#   START
#     ↓
#   agent  ← ← ← ← ← ← ←
#     ↓                   ↑
#   (should_use_tool?)     |
#     ↓ tool calls         |
#   tool  → → → → → → → →
#     ↓ no tool calls
#   planner
#     ↓
#   END
#
# The agent loops with the tool node until the LLM
# has finished calling all tools (weather, transport,
# hotels). Then control moves to the planner which
# generates the final itinerary.
# -------------------------------------------------------

builder = StateGraph(TravelState)

# Register nodes
builder.add_node("agent",   agent_node)
builder.add_node("tool",    tool_node)
builder.add_node("planner", planner_node)

# Entry point
builder.add_edge(START, "agent")

# After agent runs, decide: call a tool OR go to planner
builder.add_conditional_edges(
    "agent",
    should_use_tool,
    {
        "tool":    "tool",
        "planner": "planner"
    }
)

# After tool runs, go back to agent for the next decision
builder.add_edge("tool", "agent")

# After planner runs, we're done
builder.add_edge("planner", END)

travel_graph = builder.compile()