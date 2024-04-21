import sys
import os
import json

DEBUG_SYMBOL = True


def get_env_variable(var_name, check=True):
    try:
        return os.environ[var_name]
    except KeyError:
        if check:
            error_msg = f"Environment variable {var_name} is not set."
            print(error_msg)
            sys.exit(1)
        return None


def parse_config_file(config_file_path, config_type="json"):
    config_dict = None
    if config_type == "json":
        with open(config_file_path, "r") as f:
            config_dict = json.load(f)
    else:
        print(f"Unsupported config file type: {config_type}")
        sys.exit(1)
    return config_dict


QIS_PROJECT_ROOT_PATH = get_env_variable("QIS_PROJECT_ROOT_PATH")
FDA_PROJECT_ROOT_PATH = get_env_variable("FDA_PROJECT_ROOT_PATH")

CONFIG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, "conf")
LOG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, "logs")

SERVER_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "server_conf.json")
LOG_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "log_conf.json")
STORAGE_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "storage_conf.json")

server_config_dict = parse_config_file(SERVER_CONFIG_FILE_PATH)
log_config_dict = parse_config_file(LOG_CONFIG_FILE_PATH)

default_log_file_path = os.path.join(LOG_DIR_PATH, "finance_data_api.log")

from manager.storage_engine_manager import StorageEngineManager

storager_manager = StorageEngineManager.get_instance()
storager_manager.parse_storage_config(STORAGE_CONFIG_FILE_PATH)

if __name__ == '__main__':
    print(QIS_PROJECT_ROOT_PATH)
    print(FDA_PROJECT_ROOT_PATH)
    print(server_config_dict)
    print(log_config_dict)
    ...
