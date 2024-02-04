class ExchangeBase(object):
    # 交易所基类，每个交易所有一个对应的交易所id

    def __init__(self, exchange_id: int):
        self._exchange_id = exchange_id

    @property
    def id(self):
        return self._exchange_id

    @property
    def name(self):
        raise NotImplementedError

    def __str__(self):
        return f"ExchangeBase(id={self._exchange_id}, name={self.name})"

    def __repr__(self):
        return self.__str__()
