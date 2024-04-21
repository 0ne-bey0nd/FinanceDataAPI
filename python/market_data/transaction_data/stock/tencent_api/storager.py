import pandas as pd
from pipeline import StoragerBase
from manager.storage_engine_manager import StorageEngineManager
from logger import get_manual_logger
import timeit

storage_engine_manager = StorageEngineManager.get_instance()
logger = get_manual_logger()


class TransactionDataStorager(StoragerBase):
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

    def storage_transaction_data(self, processed_transaction_data: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        ## check stock rationality

        processed_transaction_data = processed_transaction_data.copy()

        code, exchange = self.parse_stock_code(stock_code)
        formatted_stock_code = f"{code}_{exchange}"

        # try to create table
        create_procedure_name = f"create_stock_transaction_data_table"
        procedure_name = f"insert_stock_transaction_data"
        sql = f"CALL {procedure_name}( %s, %s, %s, %s, %s)"

        logger.debug(f"processed_transaction_data.shape: {processed_transaction_data.shape}")
        for mysql_storage_engine_name, mysql_storage_engine in storage_engine_manager.get_mysql_storage_engine_dict().items():
            logger.debug(f"mysql_storage_engine_name: {mysql_storage_engine_name}")
            logger.debug(f"mysql_storage_engine: {mysql_storage_engine}")
            t1 = timeit.default_timer()
            conn = mysql_storage_engine.get_connection_context()
            t2 = timeit.default_timer()
            logger.debug(f"establish connection time cost: {t2 - t1}")
            with conn:
                with conn.cursor() as cursor:
                    for index, row in processed_transaction_data.iterrows():
                        cursor.execute(sql, (formatted_stock_code, *row,))
                conn.commit()

        success = pd.DataFrame([['success']], columns=['status'])
        return success


if __name__ == '__main__':
    from producer import TransactionDataProducer
    from processor import TransactionDataProcessor


    def test(stock_code):
        success = TransactionDataStorager().storage(
            TransactionDataProcessor().process(TransactionDataProducer().produce(stock_code=stock_code)),
            stock_code=stock_code
        )
        print(success)


    stock_code = 'sh600519'
    try:
        t = timeit.timeit(lambda: test(stock_code), number=1)
    except Exception as e:
        print(f"Error: {e}")
    print(f"time cost: {t}")
    ...
