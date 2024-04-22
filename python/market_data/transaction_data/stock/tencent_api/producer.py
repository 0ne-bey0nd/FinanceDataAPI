import pandas as pd
from pipeline import ProducerBase
import requests


class TransactionDataProducer(ProducerBase):

    def produce(self, *args, **kwargs) -> pd.DataFrame:
        # extract arguments
        stock_code_list = kwargs.get('stock_code_list', [])
        limit = kwargs.get('limit', 6)

        return self.get_transaction_data(stock_code_list, limit)

    def get_transaction_data(self, stock_code_list: list, limit: int) -> pd.DataFrame:
        output_data = []
        for stock_code in stock_code_list:
            raw_transaction_data = self.get_one_stock_transaction_data(stock_code, limit)
            output_data.append((stock_code, raw_transaction_data))

        return pd.DataFrame(output_data, columns=['stock_code', 'raw_data'])

    def get_one_stock_transaction_data(self, stock_code: str, limit: int = 6) -> str:
        ## stock_code rationality check

        ## limit rationality check

        url = f"https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2?code={stock_code}&limit={limit}&direction=1"

        proxy = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        response = requests.get(url, proxies=proxy)
        return response.text


if __name__ == '__main__':
    producer = TransactionDataProducer()

    stock_code_list = ['sh600519', 'sz000001']
    transaction_data_data = producer.produce(stock_code_list=stock_code_list)
    print(f"transaction_data_data: {transaction_data_data}")
    print(f"transaction_data_data.shape: {transaction_data_data.shape}")
    print(transaction_data_data['raw_data'][0])
