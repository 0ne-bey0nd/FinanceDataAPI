from market_data import TransactionBase
import decimal


class TencentApiTransaction(TransactionBase):
    def __init__(self):
        super().__init__()
        self.transaction_index: int = None
        self.transaction_price_change: decimal.Decimal = None
        self.transaction_amount: decimal.Decimal = None

    def init(self, *args, **kwargs):
        try:
            super().init(*args, **kwargs)
            self.transaction_index = kwargs['transaction_index']
            self.transaction_price_change = kwargs['transaction_price_change']
            self.transaction_amount = kwargs['transaction_amount']
        except Exception as e:
            print(f"Error: {e}")
        ...

    @staticmethod
    def CreateTransaction(*args, **kwargs) -> 'TencentApiTransaction':
        transaction = TencentApiTransaction()
        transaction.init(*args, **kwargs)
        return transaction

