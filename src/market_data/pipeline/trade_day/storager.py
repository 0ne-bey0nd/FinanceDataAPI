import pandas as pd
import pymysql
import pymysql.cursors
host = '127.0.0.1'
port = 3307
user = 'root'
password = '123456'
database = 'market_data'
charset = 'utf8mb4'
cursorclass = pymysql.cursors.DictCursor

from producer import get_trade_day_data
from processor import process_trade_day_data


def storage_trade_day_data(processed_trade_day_data: pd.DataFrame) -> pd.DataFrame:
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
    try:
        success = storage_trade_day_data(process_trade_day_data(get_trade_day_data()))
        print(success)
    except Exception as e:
        print(f"Error: {e}")


    ...
