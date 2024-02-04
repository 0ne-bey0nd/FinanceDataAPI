class ExchangeBase(object):
    # 交易所基类

    def __init__(self, code):
        self._code = code

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        raise NotImplementedError

    def __str__(self):
        return f"ExchangeBase(code={self._code}, name={self.name})"

    def __repr__(self):
        return self.__str__()
