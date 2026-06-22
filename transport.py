def search_transport(source, destination):
    """
    Returns available transport options
    between source and destination.
    """

    # Demo data

    if destination.lower() == "goa":

        return {
            "flights": [
                {
                    "airline": "IndiGo",
                    "price": 4500
                },
                {
                    "airline": "Air India",
                    "price": 5200
                }
            ],

            "buses": [
                {
                    "operator": "VRL Travels",
                    "price": 1800
                }
            ],

            "trains": [
                {
                    "name": "Goa Express",
                    "price": 1200
                }
            ]
        }

    elif destination.lower() == "bali":

        return {
            "flights": [
                {
                    "airline": "Air India",
                    "price": 28000
                }
            ],

            "buses": [],
            "trains": []
        }

    else:

        return {
            "flights": [],
            "buses": [
                {
                    "operator": "State Transport",
                    "price": 500
                }
            ],
            "trains": [
                {
                    "name": "Express Train",
                    "price": 300
                }
            ]
        }