from langchain.tools import tool

from hotel import search_hotels


@tool
def hotel_tool(
    destination: str,
    budget: int
):
    """
    Search hotels for destination.
    """

    return search_hotels(
        destination,
        budget
    )