from .exchange_manager import ExchangeManager
from ._exchange_registry import Exchange


SSE = ExchangeManager().register_exchange("SSE")
SZSE = ExchangeManager().register_exchange("SZSE")

