import logging
import logging.config
import os
from settings import LOG_DIR_PATH, default_log_file_path


def get_default_logger(log_level=None):
    default_logger = logging.getLogger("FinanceDataAPI_default_logger")

    default_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
    )
    to_console = logging.StreamHandler()
    to_console.setFormatter(formatter)
    default_logger.addHandler(to_console)

    log_dir_path = LOG_DIR_PATH
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

    file_handler = logging.FileHandler(default_log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    default_logger.addHandler(file_handler)

    if log_level:
        default_logger.setLevel(log_level)

    return default_logger


if __name__ == '__main__':
    logger = get_default_logger()
    logger.debug("debug---------")
