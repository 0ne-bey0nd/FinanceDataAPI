import os
from utils.config_utils import get_env_variable, parse_config_file

DEBUG_SYMBOL = True

QIS_PROJECT_ROOT_PATH = get_env_variable("QIS_PROJECT_ROOT_PATH")
FDA_PROJECT_ROOT_PATH = get_env_variable("FDA_PROJECT_ROOT_PATH")

CONFIG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, "conf")
LOG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, "logs")

SERVER_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "server_conf.json")

server_config_dict = parse_config_file(SERVER_CONFIG_FILE_PATH)

log_config_file_name = server_config_dict.get("log_config_file_name", "log_conf.json")
storage_config_file_name = server_config_dict.get("storage_config_file_name", "storage_conf.json")

scheduled_jobs_config_dir_path = server_config_dict.get("scheduled_jobs_config_dir_path", "examples/scheduled_jobs")
scheduled_jobs_config_dir_path = os.path.join(QIS_PROJECT_ROOT_PATH, scheduled_jobs_config_dir_path)

LOG_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, log_config_file_name)
STORAGE_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, storage_config_file_name)

log_config_dict = parse_config_file(LOG_CONFIG_FILE_PATH)
default_log_file_path = os.path.join(LOG_DIR_PATH, "finance_data_api.log")

if __name__ == '__main__':
    # print(QIS_PROJECT_ROOT_PATH)
    # print(FDA_PROJECT_ROOT_PATH)
    # print(server_config_dict)
    # print(log_config_dict)
    print(scheduled_jobs_config_dir_path)
    ...
