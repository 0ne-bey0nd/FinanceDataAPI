"""
日K线单位类
"""

from market_data._base.candlestick_base import CandlestickBase
from market_data._base.candlestick_base import CandlestickDictKeyBase


class CandlestickDictKeyDay(CandlestickDictKeyBase):
    DATE = 'date'


class CandlestickDay(CandlestickBase):
    # 日K线单位数据
    def __init__(self, date, now, begin, highest, lowest, total_lot, total_money):
        super(CandlestickDay, self).__init__(now, begin, highest, lowest, total_lot, total_money)
        self.date = date

    def __str__(self):
        return f"CandlestickDay(date={self.date}, now={self.now}, begin={self.begin}, highest={self.highest}, " \
               f"lowest={self.lowest}, total_lot={self.total_lot}, total_money={self.total_money})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def init_with_dict(cls, data_dict):
        return cls(date=data_dict[CandlestickDictKeyDay.DATE],
                   now=data_dict[CandlestickDictKeyBase.NOW],
                   begin=data_dict[CandlestickDictKeyBase.BEGIN],
                   highest=data_dict[CandlestickDictKeyBase.HIGHEST],
                   lowest=data_dict[CandlestickDictKeyBase.LOWEST],
                   total_lot=data_dict[CandlestickDictKeyBase.TOTAL_LOT],
                   total_money=data_dict[CandlestickDictKeyBase.TOTAL_MONEY])
    