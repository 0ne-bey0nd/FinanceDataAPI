from .exchange_manager import ExchangeManager
from ._exchange_registry import Exchange

SSE = ExchangeManager().register_exchange("SSE")
