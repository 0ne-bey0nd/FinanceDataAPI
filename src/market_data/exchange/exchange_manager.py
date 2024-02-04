from ._exchange_registry import ExchangeRegistry
from market_data._base.exchange_base import ExchangeBase


class ExchangeManager:
    """
    交易所管理类，单例模式
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExchangeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.exchange_registry = ExchangeRegistry()

    def register_exchange(self, name: str) -> ExchangeBase:
        return self.exchange_registry.register_exchange(name)

    def get_exchange_instance(self, exchange_id: int) -> ExchangeBase:
        return self.exchange_registry.get_exchange_instance(exchange_id)

    def get_exchange_id_by_name(self, name: str) -> int:
        return self.exchange_registry.get_exchange_id_by_name(name)

    def get_all_exchanges(self) -> dict:
        return self.exchange_registry.get_all_exchanges()
