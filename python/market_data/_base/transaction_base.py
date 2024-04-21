import datetime
import decimal


class TransactionBase(object):
    def __init__(self):
        self.transaction_datetime: datetime.datetime = None
        self.transaction_price: decimal.Decimal = None
        self.transaction_volume: int = None
        self.transaction_type: str = None
        ...

    def __str__(self):
        return self.__class__.__name__ + "(" + ", ".join(
            [f"{key}={value}" for key, value in self.__dict__.items()]) + ")"

    def __repr__(self):
        return self.__str__()

    def get_all_argument_name_dict(self):
        return self.__dict__

    def init(self, *args, **kwargs):
        try:
            self.transaction_datetime = kwargs['transaction_datetime']
            self.transaction_price = kwargs['transaction_price']
            self.transaction_volume = kwargs['transaction_volume']
            self.transaction_type = kwargs['transaction_type']
        except Exception as e:
            print(f"Error: {e}")
        ...
