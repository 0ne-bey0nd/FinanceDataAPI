"""
股票类
由交易所和股票代码唯一确定
每个股票只能有一个实例
"""

from market_data._base.exchange_base import ExchangeBase
from market_data.candlestick.day import CandlestickDay


class Stock(object):
    _instances = {}  # 保存所有股票实例的字典，多级字典，第一级键为交易所，第二级键为股票代码

    def __new__(cls, exchange: ExchangeBase, code: str):
        """
        创建股票实例
        :param exchange: 交易所
        :param code: 股票代码
        :return: 股票实例
        """
        if exchange not in cls._instances:
            cls._instances[exchange] = {}
        if code not in cls._instances[exchange]:
            cls._instances[exchange][code] = super(Stock, cls).__new__(cls)
        return cls._instances[exchange][code]

    def __init__(self, exchange: ExchangeBase, code: str):
        """
        初始化股票实例
        :param exchange: 交易所
        :param code: 股票代码
        """
        self.exchange = exchange
        self.code = code

    def __str__(self):
        """
        返回股票实例的字符串表示
        :return: 股票实例的字符串表示
        """
        return f"Stock(exchange={self.exchange}, code={self.code})"

    def __repr__(self):
        return self.__str__()

    def get_day_candlestick(self, date):
        """
        获取日K线数据
        :param date: 日期
        :return: 日K线数据
        """
        return CandlestickDay(date, 1, 2, 3, 4, 5, 6)
