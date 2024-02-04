from ._exchange_registry import ExchangeRegistry


class ExchangeManager:
    def __init__(self):
        self.exchange_registry = ExchangeRegistry()

    def register_exchange(self, name: str) -> int:
        return self.exchange_registry.register_exchange(name)

    def get_exchange_id(self, name: str) -> int:
        return self.exchange_registry.get_exchange_id(name)

    def get_exchange_name(self, exchange_id: int) -> str:
        return self.exchange_registry.get_exchange_name(exchange_id)

    def get_all_exchanges(self):
        return self.exchange_registry.get_all_exchanges()



