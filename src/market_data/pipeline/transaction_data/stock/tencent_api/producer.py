import pandas as pd
from market_data.pipeline._base import ProducerBase
import requests


class TransactionDataProducer(ProducerBase):

    def produce(self, *args, **kwargs) -> pd.DataFrame:
        # extract arguments
        stock_code = kwargs.get('stock_code', '')
        limit = kwargs.get('limit', 6)

        return self.get_transaction_data(stock_code, limit)

    def get_transaction_data(self, stock_code: str, limit: int = 6) -> pd.DataFrame:
        ## stock_code rationality check

        ## limit rationality check

        url = f"https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2?code={stock_code}&limit={limit}&direction=1"

        proxy = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        response = requests.get(url, proxies=proxy)

        output_table = pd.DataFrame([[response.text]], columns=['raw_data'])
        return output_table


if __name__ == '__main__':
    producer = TransactionDataProducer()

    stock_code = 'sh600519'
    transaction_data_data = producer.produce(stock_code=stock_code)
    print(transaction_data_data)
    print(transaction_data_data['raw_data'][0])
