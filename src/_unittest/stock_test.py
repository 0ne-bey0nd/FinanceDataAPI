import unittest
from market_data.exchange import SSE,SZSE
from market_data.stock.stock import Stock


class TestStock(unittest.TestCase):
    def test_stock(self):
        stock = Stock(SZSE, '000001')
        print(stock)

        # 重复创建股票实例
        another_stock = Stock(SZSE, '000001')
        self.assertIs(stock, another_stock)
