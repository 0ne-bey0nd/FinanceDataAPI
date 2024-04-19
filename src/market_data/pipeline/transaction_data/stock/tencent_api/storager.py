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


class TransactionDataStorager(storager_base.StoragerBase):
    def __init__(self, *args, **kwargs):
        super(TransactionDataStorager, self).__init__(*args, **kwargs)

    def storage(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        # extract arguments
        stock_code = kwargs.get('stock_code', '')

        return self.storage_transaction_data(input_data, stock_code=stock_code)

    def parse_stock_code(self, stock_code: str):
        code = stock_code[2:]
        exchange = stock_code[:2].upper()
        return code, exchange

    def storage_transaction_data(self, input_data: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        ## check stock rationality

        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database, charset=charset,
                               cursorclass=cursorclass)

        processed_trade_day_data = input_data.copy()

        code, exchange = self.parse_stock_code(stock_code)

        formatted_stock_code = f"{code}_{exchange}"

        # try to create table
        create_procedure_name = f"create_stock_transaction_data_table"

        with conn:
            with conn.cursor() as cursor:
                sql = f"CALL {create_procedure_name}( %s)"
                cursor.execute(sql, (formatted_stock_code,))
            conn.commit()

            # 遍历DataFrame的每一行
            procedure_name = f"insert_stock_transaction_data"

            with conn.cursor() as cursor:
                for index, row in processed_trade_day_data.iterrows():
                    # print(*row)
                    sql = f"CALL {procedure_name}( %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (formatted_stock_code, *row,))
            conn.commit()

        success = pd.DataFrame([['success']], columns=['status'])
        return success


if __name__ == '__main__':
    from producer import TransactionDataProducer
    from processor import TransactionDataProcessor

    stock_code = 'sh600519'

    try:
        success = TransactionDataStorager().storage(
            TransactionDataProcessor().process(TransactionDataProducer().produce(stock_code=stock_code)),
            stock_code=stock_code
        )
        print(success)
    except Exception as e:
        print(f"Error: {e}")

    ...
