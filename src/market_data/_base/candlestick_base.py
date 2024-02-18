"""
candlestick
"""


class CandlestickDictKeyBase(object):
    NOW = 'now'  # 当前价格，等于收盘价格
    BEGIN = 'begin'
    HIGHEST = 'highest'
    LOWEST = 'lowest'
    TOTAL_LOT = 'total_lot'
    TOTAL_MONEY = 'total_money'


class CandlestickBase(object):
    # K线单位数据

    def __init__(self, now, begin, highest, lowest, total_lot, total_money):
        self.now = now
        self.begin = begin
        self.highest = highest
        self.lowest = lowest
        self.total_lot = total_lot
        self.total_money = total_money

    ...
