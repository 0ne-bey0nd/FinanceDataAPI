import concurrent
import threading

import pandas as pd
from pipeline import StoragerBase
from manager.storage_engine_manager import StorageEngineManager
from utils.log_utils import get_logger, get_logger_by_thread_id
import timeit

storage_engine_manager = StorageEngineManager.get_instance()
logger = get_logger()


class TransactionDataStorager(StoragerBase):
    def __init__(self, *args, **kwargs):
        super(TransactionDataStorager, self).__init__(*args, **kwargs)

    def storage(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        # extract arguments
        return self.storage_multi_thread(input_data, *args, **kwargs)

    def parse_stock_code(self, stock_code: str):
        code = stock_code[2:]
        exchange = stock_code[:2].upper()
        return code, exchange

    def get_table_name(self, stock_code: str):
        code, exchange = self.parse_stock_code(stock_code)
        return f"stock_transaction_data_{code}_{exchange}"

    def sql_check_and_create_stock_transaction_data_table(self, stock_code):
        table_name = self.get_table_name(stock_code)
        sql = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (time DATETIME PRIMARY KEY, price DECIMAL(10, 3), volume INT, transaction_type_id INT,FOREIGN KEY (transaction_type_id) REFERENCES transaction_type_table(transaction_type_id));'
        return sql

    def sql_insert_stock_transaction_data(self, stock_code, one_stock_processed_transaction_data_table: pd.DataFrame):
        table_name = self.get_table_name(stock_code)
        insert_values = ", ".join(
            f'("{time}", {price}, {volume}, {transaction_type_id})'
            for _, (time, price, volume, transaction_type_id) in
            one_stock_processed_transaction_data_table.iterrows()
        )
        sql = f'INSERT INTO {table_name} (time, price, volume, transaction_type_id) VALUES {insert_values} ON DUPLICATE KEY UPDATE price=VALUES(price), volume=VALUES(volume), transaction_type_id=VALUES(transaction_type_id);'
        return sql

    def storage_multi_thread(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        # extract arguments
        return self.storage_transaction_data_multi_thread(input_data)

    def storage_transaction_data_multi_thread(self, processed_transaction_data_table: pd.DataFrame) -> pd.DataFrame:
        processed_transaction_data_table = processed_transaction_data_table.copy()
        logger.debug(f"begin to storage transaction data")
        logger.debug(f"processed_transaction_data_table.shape: {processed_transaction_data_table.shape}")

        task_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for mysql_storage_engine_name, mysql_storage_engine in storage_engine_manager.get_mysql_storage_engine_dict().items():
                logger.info(f"mysql_storage_engine_name: {mysql_storage_engine_name}")
                logger.info(f"mysql_storage_engine: {mysql_storage_engine}")
                task_list.append(executor.submit(self.storage_one_stock_transaction_data_multi_thread,
                                                 processed_transaction_data_table, mysql_storage_engine,
                                                 threading.get_ident()))
            result_list = [future.result() for future in task_list]
            logger.info(f"result_list: {result_list}")
            success = all(result_list)
        output_table = pd.DataFrame([['success' if success else 'fail']], columns=['status'])  # maybe add detail info
        return output_table

    def storage_one_stock_transaction_data_multi_thread(self, processed_transaction_data_table: pd.DataFrame,
                                                        mysql_storage_engine, parent_thread_id) -> bool:
        ## check stock rationality
        logger = get_logger_by_thread_id(parent_thread_id)
        processed_transaction_data_table = processed_transaction_data_table.copy()

        # try to create table

        create_table_sql = ""
        insert_data_sql = ""
        logger.info(f"processed_transaction_data.shape: {processed_transaction_data_table.shape}")
        conn = mysql_storage_engine.get_connection_context()
        for idx, row in processed_transaction_data_table.iterrows():
            stock_code = row['stock_code']

            one_stock_processed_transaction_data_table = row['processed_data_table']
            create_table_sql += self.sql_check_and_create_stock_transaction_data_table(stock_code) + "\n"

            insert_data_sql += self.sql_insert_stock_transaction_data(stock_code,
                                                                      one_stock_processed_transaction_data_table) + "\n"
        try:
            with conn:
                with conn.cursor() as cursor:
                    logger.info(f"before execute sql")
                    # logger.info(f"create_table_sql: {create_table_sql}")
                    # logger.info(f"insert_data_sql: {insert_data_sql}")
                    cursor.execute(create_table_sql)
                    cursor.execute(insert_data_sql)
                    conn.commit()
                    logger.info(f"after execute")
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

        return True


if __name__ == '__main__':
    from producer import TransactionDataProducer
    from processor import TransactionDataProcessor
    from settings import STORAGE_CONFIG_FILE_PATH

    stock_code_list = ['sh600519', 'sz000001']
    stock_code_list = ["sh600000", "sh600009", "sh600010", "sh600011", "sh600015", "sh600016", "sh600018",
                       "sh600019", "sh600023", "sh600025", "sh600028", "sh600029", "sh600030", "sh600031",
                       "sh600036", "sh600039", "sh600048", "sh600050", "sh600061", "sh600085", "sh600089",
                       "sh600104", "sh600111", "sh600115", "sh600132", "sh600150", "sh600176", "sh600183",
                       "sh600188", "sh600196", "sh600219", "sh600233", "sh600276", "sh600309", "sh600332",
                       "sh600346", "sh600362", "sh600372", "sh600406", "sh600426", "sh600436", "sh600438",
                       "sh600460", "sh600489", "sh600515", "sh600519", "sh600547", "sh600570", "sh600584",
                       "sh600585", "sh600588", "sh600600", "sh600606", "sh600660", "sh600674", "sh600690",
                       "sh600732", "sh600741", "sh600745", "sh600754", "sh600760", "sh600795", "sh600803",
                       "sh600809", "sh600837", "sh600845", "sh600875", "sh600886", "sh600887", "sh600893",
                       "sh600900", "sh600905", "sh600918", "sh600919", "sh600926", "sh600938", "sh600941",
                       "sh600958", "sh600989", "sh600999", "sh601006", "sh601009", "sh601012", "sh601021",
                       "sh601059", "sh601066", "sh601088", "sh601100", "sh601111", "sh601117", "sh601138",
                       "sh601155", "sh601166", "sh601169", "sh601186", "sh601211", "sh601225", "sh601229",
                       "sh601236", "sh601238", "sh601288", "sh601318", "sh601319", "sh601328", "sh601336",
                       "sh601360", "sh601377", "sh601390", "sh601398", "sh601600", "sh601601", "sh601607",
                       "sh601615", "sh601618", "sh601628", "sh601633", "sh601658", "sh601668", "sh601669",
                       "sh601688", "sh601689", "sh601698", "sh601699", "sh601728", "sh601766", "sh601788",
                       "sh601799", "sh601800", "sh601808", "sh601816", "sh601818", "sh601838", "sh601857",
                       "sh601865", "sh601868", "sh601872", "sh601877", "sh601878", "sh601881", "sh601888",
                       "sh601898", "sh601899", "sh601901", "sh601916", "sh601919", "sh601939", "sh601985",
                       "sh601988", "sh601989", "sh601995", "sh601998", "sh603019", "sh603195", "sh603259",
                       "sh603260", "sh603288", "sh603290", "sh603369", "sh603392", "sh603486", "sh603501",
                       "sh603659", "sh603799", "sh603806", "sh603833", "sh603899", "sh603986", "sh603993",
                       "sh605117", "sh605499", "sh688008", "sh688012", "sh688036", "sh688041", "sh688065",
                       "sh688111", "sh688126", "sh688187", "sh688223", "sh688256", "sh688271", "sh688303",
                       "sh688363", "sh688396", "sh688561", "sh688599", "sh688981", "sz000001", "sz000002",
                       "sz000063", "sz000069", "sz000100", "sz000157", "sz000166", "sz000301", "sz000333",
                       "sz000338", "sz000408", "sz000425", "sz000538", "sz000568", "sz000596", "sz000617",
                       "sz000625", "sz000651", "sz000661", "sz000708", "sz000725", "sz000733", "sz000768",
                       "sz000776", "sz000786", "sz000792", "sz000800", "sz000858", "sz000876", "sz000877",
                       "sz000895", "sz000938", "sz000963", "sz000977", "sz000983", "sz000999", "sz001289",
                       "sz001979", "sz002001", "sz002007", "sz002027", "sz002049", "sz002050", "sz002074",
                       "sz002129", "sz002142", "sz002179", "sz002180", "sz002202", "sz002230", "sz002236",
                       "sz002241", "sz002252", "sz002271", "sz002304", "sz002311", "sz002352", "sz002371",
                       "sz002410", "sz002415", "sz002459", "sz002460", "sz002466", "sz002475", "sz002493",
                       "sz002555", "sz002594", "sz002601", "sz002603", "sz002648", "sz002709", "sz002714",
                       "sz002736", "sz002812", "sz002821", "sz002841", "sz002916", "sz002920", "sz002938",
                       "sz003816", "sz300014", "sz300015", "sz300033", "sz300059", "sz300122", "sz300124",
                       "sz300142", "sz300223", "sz300274", "sz300308", "sz300316", "sz300347", "sz300408",
                       "sz300413", "sz300433", "sz300450", "sz300454", "sz300496", "sz300498", "sz300628",
                       "sz300661", "sz300750", "sz300751", "sz300759", "sz300760", "sz300763", "sz300782",
                       "sz300896", "sz300919", "sz300957", "sz300979", "sz300999", "sz301269"]
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
