"""
candlestick
"""


class CandlestickBase(object):
    # K线单位数据

    def __init__(self, code, date, begin, highest, lowest, average, total_lot, total_money):
        self.code = code
        # Convert the 'date' string to a datetime object
        self.date = date
        self.begin = begin
        self.highest = highest
        self.lowest = lowest
        self.average = average
        self.total_lot = total_lot
        self.total_money = total_money
    ...
