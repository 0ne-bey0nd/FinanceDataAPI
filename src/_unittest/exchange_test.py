import unittest
from market_data.exchange.exchange_manager import ExchangeManager


class TestExchange(unittest.TestCase):
    def test_exchange_manager(self):
        exchange_manager = ExchangeManager()

        # 注册交易所
        NYSE = exchange_manager.register_exchange("NYSE")
        NASDAQ = exchange_manager.register_exchange("NASDAQ")
        LSE = exchange_manager.register_exchange("LSE")

        # 获取交易所ID
        self.assertEqual(exchange_manager.get_exchange_id("NYSE"), NYSE)
        self.assertEqual(exchange_manager.get_exchange_id("NASDAQ"), NASDAQ)
        self.assertEqual(exchange_manager.get_exchange_id("LSE"), LSE)

        # 获取所有注册的交易所
        all_exchanges = exchange_manager.get_all_exchanges()
        # self.assertDictContainsSubset({NYSE: "NYSE", NASDAQ: "NASDAQ", LSE: "LSE"}, all_exchanges)
        self.assertTrue(all_exchanges.items() >= {NYSE: "NYSE", NASDAQ: "NASDAQ", LSE: "LSE"}.items())

        # 获取交易所名称
        self.assertEqual(exchange_manager.get_exchange_name(NYSE), "NYSE")
        self.assertEqual(exchange_manager.get_exchange_name(NASDAQ), "NASDAQ")
        self.assertEqual(exchange_manager.get_exchange_name(LSE), "LSE")

        # 注册重复的交易所
        with self.assertRaises(ValueError):
            exchange_manager.register_exchange("NYSE")

    # def test_duplicate_exchange(self):
    #     # 注册重复的交易所
    #     with self.assertRaises(ValueError):
    #         exchange_manager.register_exchange("NYSE")
    # 这个测试不可以和上面的测试一起运行，测试运行顺序不确定，可能会导致上面的测试失败
