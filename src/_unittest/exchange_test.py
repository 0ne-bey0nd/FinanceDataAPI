import unittest
from market_data.exchange.exchange_manager import ExchangeManager
from market_data.exchange import SSE


class TestExchange(unittest.TestCase):
    def test_exchange_manager(self):
        exchange_manager = ExchangeManager()

        # 测试交易所管理器是否为单例
        another_exchange_manager = ExchangeManager()
        self.assertIs(exchange_manager, another_exchange_manager)

        # 注册交易所
        NYSE = exchange_manager.register_exchange("NYSE")
        NASDAQ = exchange_manager.register_exchange("NASDAQ")
        LSE = exchange_manager.register_exchange("LSE")

        # 获取交易所ID
        self.assertEqual(exchange_manager.get_exchange_id_by_name("NYSE"), NYSE.id)
        self.assertEqual(exchange_manager.get_exchange_id_by_name("NASDAQ"), NASDAQ.id)
        self.assertEqual(exchange_manager.get_exchange_id_by_name("LSE"), LSE.id)

        # 获取所有注册的交易所
        all_exchanges = exchange_manager.get_all_exchanges()
        # self.assertDictContainsSubset({NYSE: "NYSE", NASDAQ: "NASDAQ", LSE: "LSE"}, all_exchanges)
        # print(all_exchanges)
        self.assertTrue(all_exchanges.items() >= {NYSE.id: NYSE, NASDAQ.id: NASDAQ, LSE.id: LSE}.items())

        # 获取交易所名称
        self.assertEqual(NYSE.name, "NYSE")
        self.assertEqual(NASDAQ.name, "NASDAQ")
        self.assertEqual(LSE.name, "LSE")

        # 注册重复的交易所
        with self.assertRaises(ValueError):
            exchange_manager.register_exchange("NYSE")

    # def test_duplicate_exchange(self):
    #     # 注册重复的交易所
    #     with self.assertRaises(ValueError):
    #         exchange_manager.register_exchange("NYSE")
    # 这个测试不可以和上面的测试一起运行，测试运行顺序不确定，可能会导致上面的测试失败


class TestSSE(unittest.TestCase):
    def test_exchange(self):
        exchange_manager = ExchangeManager()

        # print(exchange_manager.get_all_exchanges())

        with self.assertRaises(ValueError):
            exchange_manager.register_exchange("SSE")

        sse = exchange_manager.get_exchange_instance(exchange_manager.get_exchange_id_by_name("SSE"))
        self.assertIs(sse, SSE)

        print(SSE)
