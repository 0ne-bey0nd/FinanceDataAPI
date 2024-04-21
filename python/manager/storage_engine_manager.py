import json
import pymysql
import pymysql.cursors
from settings import STORAGE_CONFIG_FILE_PATH


class MySQLStorageEngine:
    def __init__(self, host, port, user, password, database, charset, cursorClass):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.cursorClass = cursorClass

    def __str__(self):
        return f"MySQLStorageEngine(host={self.host}, port={self.port}, user={self.user}, password={self.password}, " \
               f"database={self.database}, charset={self.charset}, cursorClass={self.cursorClass})"

    def __repr__(self):
        return self.__str__()

    def get_connection_context(self) -> pymysql.connections.Connection:
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                               database=self.database, charset=self.charset, cursorclass=self.cursorClass)

        return conn

    @classmethod
    def from_dict(cls, config_dict):
        host = config_dict.get("host")
        port = config_dict.get("port")
        user = config_dict.get("user")
        password = config_dict.get("password")
        database = config_dict.get("database")
        charset = config_dict.get("charset")
        if config_dict.get("cursorClass") == "DictCursor":
            cursorClass = pymysql.cursors.DictCursor
        else:
            raise ValueError(f"Unsupported cursor class: {config_dict.get('cursorClass')}")
        return cls(host, port, user, password, database, charset, cursorClass)


class StorageEngineManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if StorageEngineManager.__instance is None:
            StorageEngineManager.__instance = object.__new__(cls)
        return StorageEngineManager.__instance

    @staticmethod
    def get_instance() -> 'StorageEngineManager':
        if StorageEngineManager.__instance is None:
            StorageEngineManager()
        return StorageEngineManager.__instance

    def __init__(self):
        self.storage_engine_type_list: list = []
        self.mysql_storage_engine_dict: dict = {}

    def read_storage_config(self, storage_config_file_path):
        try:
            with open(storage_config_file_path, "r") as f:
                storage_config_dict = json.load(f)
        except FileNotFoundError:
            print(f"Storage config file not found: {storage_config_file_path}")
            exit(1)
        except json.JSONDecodeError:
            print(f"Storage config file is not a valid JSON file: {storage_config_file_path}")
            exit(1)
        except Exception as e:
            print(f"Error occurred while reading storage config file: {storage_config_file_path}")
            print(e)
            exit(1)
        return storage_config_dict

    def load_storage_config(self, storage_config_file_path):
        storage_config_dict = self.read_storage_config(storage_config_file_path)
        self.storage_engine_type_list = list(storage_config_dict.keys())

        mysql_storage_config_dict = storage_config_dict.get("mysql")
        for database_name, database_storage_config in mysql_storage_config_dict.items():
            mysql_storage_config = MySQLStorageEngine.from_dict(database_storage_config)
            self.mysql_storage_engine_dict[database_name] = mysql_storage_config

    def get_mysql_storage_engine_dict(self) -> dict[str, MySQLStorageEngine]:
        return self.mysql_storage_engine_dict



if __name__ == '__main__':
    storager_manager = StorageEngineManager.get_instance()
    from settings import STORAGE_CONFIG_FILE_PATH

    storager_manager.load_storage_config(STORAGE_CONFIG_FILE_PATH)
    print(storager_manager)
    print(storager_manager.storage_engine_type_list)
    print(storager_manager.mysql_storage_engine_dict)
    ...
