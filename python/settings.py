import os
from utils.config_utils import get_env_variable, parse_config_file

QIS_PROJECT_ROOT_PATH = get_env_variable("QIS_PROJECT_ROOT_PATH")
FDA_PROJECT_ROOT_PATH = get_env_variable("FDA_PROJECT_ROOT_PATH")

CONFIG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, "conf")
LOG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, "logs")

QIS_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "qis_conf.json")

qis_config_dict = parse_config_file(QIS_CONFIG_FILE_PATH)

storage_config_file_name = qis_config_dict.get("storage_config_file_name", "storage_conf.json")

STORAGE_CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, storage_config_file_name)

SCHEDULED_JOBS_CONFIG_DIR_PATH = qis_config_dict.get("scheduled_jobs_config_dir_path", "examples/scheduled_jobs")
SCHEDULED_JOBS_CONFIG_DIR_PATH = os.path.join(QIS_PROJECT_ROOT_PATH, SCHEDULED_JOBS_CONFIG_DIR_PATH)

log_config_dict = qis_config_dict.get("log_config", {})


server_config_dict = qis_config_dict.get("server_config", {})
SERVER_HOST = server_config_dict.get("host", "0.0.0.0")
SERVER_PORT = server_config_dict.get("port", 8000)

DEBUG_SYMBOL = qis_config_dict.get("debug", False)
RELOAD_SYMBOL = qis_config_dict.get("reload", False)

if __name__ == '__main__':
    print(SCHEDULED_JOBS_CONFIG_DIR_PATH)
    ...
