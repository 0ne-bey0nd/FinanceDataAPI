_exchanges_table = {}  # 交易所表，key为交易所ID，value为交易所名称，id和名称一一对应，都是唯一的
_exchanges_table_reverse = {}  # 交易所表的反向映射，key为交易所名称，value为交易所ID，id和名称一一对应，都是唯一的

_exchanges_instance = {}  # 交易所实例表，key为交易所ID，value为交易所实例，id和实例一一对应，都是唯一的


def _get_exchange_name(exchange_id):
    return _exchanges_table.get(exchange_id)


def _get_exchange_id_by_name(name):
    return _exchanges_table_reverse.get(name)


def _get_exchange_instance(exchange_id):
    return _exchanges_instance.get(exchange_id)


"""
交易所实体类
"""
from market_data._base.exchange_base import ExchangeBase


class Exchange(ExchangeBase):
    def __new__(cls, code):
        """
        创建交易所实例
        :param code: 交易所代码
        :return: 交易所实例
        """
        if code not in _exchanges_table:
            raise ValueError(f"Exchange '{code}' is not registered.")
        return super(Exchange, cls).__new__(cls)

    @property
    def name(self):
        return _get_exchange_name(self._code)


"""
交易所注册类
"""


class ExchangeRegistry:
    def __init__(self):
        self.exchange_id_counter = 0

    def register_exchange(self, name: str) -> Exchange:
        if name in _exchanges_table.values():
            raise ValueError(f"Exchange '{name}' is already registered.")

        exchange_id = self.exchange_id_counter
        _exchanges_table[exchange_id] = name
        _exchanges_table_reverse[name] = exchange_id
        _exchanges_instance[exchange_id] = Exchange(exchange_id)
        self.exchange_id_counter += 1
        return _exchanges_instance[exchange_id]

    @classmethod
    def get_exchange_id_by_name(cls, name: str) -> int:
        return _get_exchange_id_by_name(name)

    @classmethod
    def get_exchange_instance(cls, exchange_id: int) -> Exchange:
        return _get_exchange_instance(exchange_id)

    @classmethod
    def get_all_exchanges(cls) -> dict:
        return _exchanges_instance
