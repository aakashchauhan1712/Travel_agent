from langchain.tools import tool

from transport import search_transport


@tool
def transport_tool(source: str, destination: str):
    """
    Search available transport options.
    """

    return search_transport(
        source,
        destination
    )