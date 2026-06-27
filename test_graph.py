from langgraph_flow.graph import travel_graph

from langchain_core.messages import HumanMessage

result = travel_graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Plan a trip to Goa from Delhi"
            )
        ]
    }
)

print(result["messages"][-1].content)