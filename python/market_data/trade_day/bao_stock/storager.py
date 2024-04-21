import pandas as pd
from pipeline import StoragerBase
from manager.storage_engine_manager import StorageEngineManager
from logger import get_manual_logger

storage_engine_manager = StorageEngineManager.get_instance()
logger = get_manual_logger()


class TradeDayStorager(StoragerBase):
    def __init__(self, *args, **kwargs):
        super(TradeDayStorager, self).__init__(*args, **kwargs)

    def storage(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        return self.storage_trade_day_data(input_data)

    def storage_trade_day_data(self, processed_trade_day_data: pd.DataFrame) -> pd.DataFrame:
        sql = "CALL insert_trade_day(%s, %s)"

        logger.debug(f"processed_trade_day_data.shape: {processed_trade_day_data.shape}")
        for mysql_storage_engine_name, mysql_storage_engine in storage_engine_manager.get_mysql_storage_engine_dict().items():
            logger.debug(f"mysql_storage_engine_name: {mysql_storage_engine_name}")
            logger.debug(f"mysql_storage_engine: {mysql_storage_engine}")
            conn = mysql_storage_engine.get_connection_context()
            with conn:
                with conn.cursor() as cursor:
                    for index, row in processed_trade_day_data.iterrows():
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
