import unittest
from market_data.stock.stock import Stock


class TestStock(unittest.TestCase):
    def test_stock(self):
        stock = Stock()
        stock.code = "AAPL"
        stock.name = "Apple Inc."
        stock.exchange = "NASDAQ"
        stock.industry = "Technology"
        stock.sector = "Consumer Electronics"
        stock.country = "United States"
        stock.currency = "USD"

        self.assertEqual(stock.code, "AAPL")
        self.assertEqual(stock.name, "Apple Inc.")
        self.assertEqual(stock.exchange, "NASDAQ")
        self.assertEqual(stock.industry, "Technology")
        self.assertEqual(stock.sector, "Consumer Electronics")
        self.assertEqual(stock.country, "United States")
        self.assertEqual(stock.currency, "USD")