import baostock as bs
import pandas as pd
import numpy as np
from market_data.pipeline._base import ProducerBase


class TradeDayProducer(ProducerBase):

    def produce(self, *args, **kwargs) -> pd.DataFrame:
        return self.get_trade_day_data()

    ...

    def get_trade_day_data(self) -> pd.DataFrame:
        lg = bs.login()
        today = np.datetime64('today') - 1
        DAY_NUM_PER_YEAR = 365
        pre_day_num = DAY_NUM_PER_YEAR * 2
        start_date = today - np.timedelta64(pre_day_num, 'D')
        end_date = np.datetime64('today', 'Y') + np.timedelta64(1, 'Y') - np.timedelta64(1, 'D')
        rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        bs.logout()
        return result


if __name__ == '__main__':
    producer = TradeDayProducer()
    trade_day_data = producer.produce()
    print(trade_day_data)
    for idx, column_name in enumerate(trade_day_data.columns):
        print(f"column {idx}: name={column_name}, type={type(trade_day_data[column_name][0])}")
