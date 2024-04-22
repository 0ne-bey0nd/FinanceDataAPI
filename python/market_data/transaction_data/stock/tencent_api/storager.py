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
        return self.storage_transaction_data(input_data)

    def parse_stock_code(self, stock_code: str):
        code = stock_code[2:]
        exchange = stock_code[:2].upper()
        return code, exchange

    def storage_transaction_data(self, processed_transaction_data_table: pd.DataFrame) -> pd.DataFrame:
        processed_transaction_data_table = processed_transaction_data_table.copy()
        logger.debug(f"begin to storage transaction data")
        logger.debug(f"processed_transaction_data_table.shape: {processed_transaction_data_table.shape}")

        success = True
        for mysql_storage_engine_name, mysql_storage_engine in storage_engine_manager.get_mysql_storage_engine_dict().items():
            logger.debug(f"mysql_storage_engine_name: {mysql_storage_engine_name}")
            logger.debug(f"mysql_storage_engine: {mysql_storage_engine}")
            t1 = timeit.default_timer()
            conn = mysql_storage_engine.get_connection_context()
            t2 = timeit.default_timer()
            logger.debug(f"get_connection_context time cost: {t2 - t1}")
            with conn:
                for idx, row in processed_transaction_data_table.iterrows():
                    stock_code = row['stock_code']
                    processed_data_table = row['processed_data_table']
                    logger.debug(f"stock_code: {stock_code}")
                    logger.debug(f"processed_data_table.shape: {processed_data_table.shape}")
                    success = self.storage_one_stock_transaction_data(processed_data_table, stock_code, conn)
                    logger.debug(f"success: {success}")
                    if not success:
                        break

        output_table = pd.DataFrame([['success' if success else 'fail']], columns=['status'])  # maybe add detail info

        return output_table

    def storage_one_stock_transaction_data(self, one_stock_processed_transaction_data_table: pd.DataFrame,
                                           stock_code: str, conn) -> bool:
        ## check stock rationality

        one_stock_processed_transaction_data_table = one_stock_processed_transaction_data_table.copy()

        code, exchange = self.parse_stock_code(stock_code)
        formatted_stock_code = f"{code}_{exchange}"

        # try to create table
        create_procedure_name = f"create_stock_transaction_data_table"
        procedure_name = f"insert_stock_transaction_data"
        sql = f"CALL {procedure_name}( %s, %s, %s, %s, %s)"

        logger.debug(f"processed_transaction_data.shape: {one_stock_processed_transaction_data_table.shape}")

        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CALL {create_procedure_name}(%s)", (formatted_stock_code,))
                logger.debug(f"create table stock_transaction_data_{formatted_stock_code} success")
                for index, row in one_stock_processed_transaction_data_table.iterrows():
                    cursor.execute(sql, (formatted_stock_code, *row,))
            conn.commit()
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

        return True


if __name__ == '__main__':
    from producer import TransactionDataProducer
    from processor import TransactionDataProcessor
    from settings import STORAGE_CONFIG_FILE_PATH

    stock_code_list = ['sh600519', 'sz000001']
    storage_engine_manager.load_storage_config(STORAGE_CONFIG_FILE_PATH)


    def test(stock_code):
        success = TransactionDataStorager().storage(
            TransactionDataProcessor().process(TransactionDataProducer().produce(stock_code_list=stock_code_list))
        )
        print(success)


    stock_code = 'sh600519'
    t = None
    try:
        t = timeit.timeit(lambda: test(stock_code), number=1)
    except Exception as e:
        print(f"Error: {e}")
    print(f"time cost: {t}")
