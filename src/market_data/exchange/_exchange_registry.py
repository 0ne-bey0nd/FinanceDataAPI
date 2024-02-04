"""
交易所注册类
"""

_exchanges_table = {}  # 交易所表，key为交易所ID，value为交易所名称，id和名称一一对应，都是唯一的
_exchanges_table_reverse = {}  # 交易所表的反向映射，key为交易所名称，value为交易所ID，id和名称一一对应，都是唯一的


def _get_exchange_name(exchange_id):
    return _exchanges_table.get(exchange_id)


def _get_exchange_id(name):
    return _exchanges_table_reverse.get(name)


class ExchangeRegistry:
    def __init__(self):
        self.exchange_id_counter = 0

    def register_exchange(self, name):
        if name in _exchanges_table.values():
            raise ValueError(f"Exchange '{name}' is already registered.")

        exchange_id = self.exchange_id_counter
        _exchanges_table[exchange_id] = name
        _exchanges_table_reverse[name] = exchange_id
        self.exchange_id_counter += 1
        return exchange_id

    def get_exchange_id(self, name):
        return _get_exchange_id(name)

    def get_exchange_name(self, exchange_id):
        return _get_exchange_name(exchange_id)

    def get_all_exchanges(self):
        return _exchanges_table

