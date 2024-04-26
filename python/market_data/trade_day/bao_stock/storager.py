import pandas as pd
from pipeline import StoragerBase
from manager.storage_engine_manager import StorageEngineManager
from utils.log_utils import get_logger

storage_engine_manager = StorageEngineManager.get_instance()
logger = get_logger()


class TradeDayStorager(StoragerBase):
    def __init__(self, *args, **kwargs):
        super(TradeDayStorager, self).__init__(*args, **kwargs)

    def storage(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        return self.storage_trade_day_data(input_data)

    def storage_trade_day_data(self, processed_trade_day_data: pd.DataFrame) -> pd.DataFrame:
        singal_sql = "CALL insert_trade_day('{}', '{}');"
        final_sql = ""

        logger.debug(f"processed_trade_day_data.shape: {processed_trade_day_data.shape}")
        for mysql_storage_engine_name, mysql_storage_engine in storage_engine_manager.get_mysql_storage_engine_dict().items():
            logger.debug(f"mysql_storage_engine_name: {mysql_storage_engine_name}")
            logger.debug(f"mysql_storage_engine: {mysql_storage_engine}")
            conn = mysql_storage_engine.get_connection_context()
            with conn:
                with conn.cursor() as cursor:
                    for index, row in processed_trade_day_data.iterrows():
                        logger.debug(f"row: {row}")
                        sql = singal_sql.format(*row)
                        final_sql += sql + "\n"
                    logger.debug(f"before execute final_sql: {final_sql}")
                    cursor.execute(final_sql)
                    logger.debug(f"after execute")
                conn.commit()
        logger.debug(f"finish storage!")

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
