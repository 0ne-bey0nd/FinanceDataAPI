from datetime import datetime

class DayK(object):
    # 日K单位数据
    def __init__(self, code, date, begin, highest, lowest, average, total_lot, total_money):
        self.code = code
        # Convert the 'date' string to a datetime object
        self.date = datetime.strptime(date, "%Y%m%d")
        self.begin = begin
        self.highest = highest
        self.lowest = lowest
        self.average = average
        self.total_lot = total_lot
        self.total_money = total_money

    def __str__(self):
        """
        Return a string representation of the DayK instance.

        Returns:
        - str: A string representation of the DayK instance.
        """
        return f"DayK(code={self.code}, date={self.date.strftime('%Y-%m-%d')}, begin={self.begin}, highest={self.highest}, " \
               f"lowest={self.lowest}, average={self.average}, total_lot={self.total_lot}, " \
               f"total_money={self.total_money})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def initDayKInstance(cls, data_dict):
        """
        Create a DayK instance from a dictionary of data.

        Parameters:
        - data_dict (dict): A dictionary containing data for initializing DayK instance.

        Returns:
        - DayK: An instance of the DayK class.
        """
        return cls(
            code=data_dict.get('code', ''),
            date=data_dict.get('date', ''),
            begin=data_dict.get('begin', 0.0),
            highest=data_dict.get('highest', 0.0),
            lowest=data_dict.get('lowest', 0.0),
            average=data_dict.get('average', 0.0),
            total_lot=data_dict.get('total_lot', 0),
            total_money=data_dict.get('total_money', 0.0)
        )
