def search_hotels(destination, budget):
    """
    Returns hotel recommendations based on destination and budget.
    """

    try:
        budget_value = int(budget)
    except (TypeError, ValueError):
        return []

    if budget_value <= 0:
        return []

    if destination.lower() == "goa":
        hotels = [
            {
                "name": "Sea View Resort",
                "price_per_night": 2500,
                "rating": 4.5
            },
            {
                "name": "Beach Paradise",
                "price_per_night": 3500,
                "rating": 4.7
            },
            {
                "name": "Budget Inn",
                "price_per_night": 1500,
                "rating": 4.0
            }
        ]
    elif destination.lower() == "bali":
        hotels = [
            {
                "name": "Bali Luxury Resort",
                "price_per_night": 7000,
                "rating": 4.8
            },
            {
                "name": "Ocean Breeze Hotel",
                "price_per_night": 5000,
                "rating": 4.6
            }
        ]
    else:
        hotels = [
            {
                "name": "City Comfort Hotel",
                "price_per_night": 2000,
                "rating": 4.2
            },
            {
                "name": "Traveler's Stay",
                "price_per_night": 1200,
                "rating": 4.0
            }
        ]

    return [hotel for hotel in hotels if hotel["price_per_night"] <= budget_value]