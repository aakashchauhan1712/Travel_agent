import unittest

from hotel import search_hotels


class HotelSearchTests(unittest.TestCase):
    def test_filters_hotels_by_budget(self):
        hotels = search_hotels("Goa", 2000)
        self.assertTrue(hotels)
        self.assertTrue(all(hotel["price_per_night"] <= 2000 for hotel in hotels))

    def test_returns_empty_when_no_hotel_matches_budget(self):
        hotels = search_hotels("Goa", 1000)
        self.assertEqual(hotels, [])


if __name__ == "__main__":
    unittest.main()
