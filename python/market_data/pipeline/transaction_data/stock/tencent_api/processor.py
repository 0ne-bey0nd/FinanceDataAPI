import json
import pandas as pd
from market_data.pipeline._base import processor_base
import datetime
import decimal

from market_data.pipeline.transaction_data.stock.tencent_api.tencent_api_transaction import TencentApiTransaction


class TransactionDataProcessor(processor_base.ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(TransactionDataProcessor, self).__init__(*args, **kwargs)

    def process(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        return self.process_transaction_data(input_data)

    def process_transaction_data(self, input_data: pd.DataFrame) -> pd.DataFrame:
        in_table = input_data.copy()
        in_table_raw_data_column_name = 'raw_data'

        raw_data = in_table[in_table_raw_data_column_name][0]
        data = json.loads(raw_data)['data']
        date = data['date']  # format 'yyyymmdd'

        transaction_list = data['data']

        base_transaction_list = []

        # print(transaction_list, date)
        for transaction in transaction_list:
            feature_in_str_list = transaction.split('/')

            # print(feature_in_str_list)
            transaction_index = feature_in_str_list[0]
            transaction_time = feature_in_str_list[1]  # format 'hh:mm:ss'

            transaction_datetime = datetime.datetime.strptime(date + transaction_time, '%Y%m%d%H:%M:%S')
            transaction_price = decimal.Decimal(feature_in_str_list[2])
            transaction_price_change = decimal.Decimal(feature_in_str_list[3])
            transaction_volume = int(feature_in_str_list[4])
            transaction_amount = decimal.Decimal(feature_in_str_list[5])
            transaction_type = feature_in_str_list[6]

            tencent_api_transaction = TencentApiTransaction.CreateTransaction(
                transaction_index=transaction_index,
                transaction_datetime=transaction_datetime,
                transaction_price=transaction_price,
                transaction_volume=transaction_volume,
                transaction_type=transaction_type,
                transaction_price_change=transaction_price_change,
                transaction_amount=transaction_amount
            )

            base_transaction_list.append(tencent_api_transaction)

        # print(base_transaction_list)

        transaction_data_table_column_name_list = list(TencentApiTransaction().get_all_argument_name_dict().keys())
        transaction_data = [
            [getattr(transaction, column_name) for column_name in transaction_data_table_column_name_list]
            for
            transaction
            in
            base_transaction_list]

        transaction_data_table = pd.DataFrame(transaction_data, columns=transaction_data_table_column_name_list)

        output_table_column_name_map = {
            "timestamp_in": "transaction_datetime",
            "price_in": "transaction_price",
            "volume_in": "transaction_volume",
            "type_in": "transaction_type",
        }
        output_table_column_name_list = list(output_table_column_name_map.keys())

        output_table = transaction_data_table[list(output_table_column_name_map.values())].copy()
        output_table.columns = output_table_column_name_list

        # data cleaning

        # process type_in data
        type_name_in_to_transaction_id_map = {
            'B': 1,  # Maybe can use the macro definition
            'S': 2,
            'M': 3,
        }

        output_table['type_in'] = output_table['type_in'].apply(
            lambda x: type_name_in_to_transaction_id_map.get(x, 0))

        return output_table


if __name__ == '__main__':
    from producer import TransactionDataProducer

    stock_code = 'sh600519'

    transaction_data = TransactionDataProducer().produce(stock_code=stock_code, limit=6)
    # print(trade_day_data)
    processor = TransactionDataProcessor()
    processed_trade_day_data = processor.process_transaction_data(transaction_data)

    print(processed_trade_day_data)
    for idx, column_name in enumerate(processed_trade_day_data.columns):
        print(f"column {idx + 1}: name={column_name}, type={type(processed_trade_day_data[column_name][0])}")
