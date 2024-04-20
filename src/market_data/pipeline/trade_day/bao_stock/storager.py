import pandas as pd
import pymysql
import pymysql.cursors
from market_data.pipeline._base import storager_base

host = '127.0.0.1'
port = 3307
user = 'root'
password = '123456'
database = 'market_data'
charset = 'utf8mb4'
cursorclass = pymysql.cursors.DictCursor


class TradeDayStorager(storager_base.StoragerBase):
    def __init__(self, *args, **kwargs):
        super(TradeDayStorager, self).__init__(*args, **kwargs)

    def storage(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        return self.storage_trade_day_data(input_data)

    def storage_trade_day_data(self, processed_trade_day_data: pd.DataFrame) -> pd.DataFrame:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset,
                               cursorclass=cursorclass)
        # 遍历DataFrame的每一行
        with conn:
            with conn.cursor() as cursor:
                for index, row in processed_trade_day_data.iterrows():
                    # print(*row)
                    sql = "CALL insert_trade_day(%s, %s)"
                    cursor.execute(sql, (*row,))
            conn.commit()

        success = pd.DataFrame([['success']], columns=['status'])
        return success


if __name__ == '__main__':
    from producer import TradeDayProducer
    from processor import TradeDayProcessor

    try:
        success = TradeDayStorager().storage(TradeDayProcessor().process(TradeDayProducer().produce()))
        print(success)
    except Exception as e:
        print(f"Error: {e}")

    ...
