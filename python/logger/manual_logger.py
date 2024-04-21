import logging
import logging.config
import os
from settings import log_config_dict, default_log_file_path
from .default_logger import get_default_logger


def get_manual_logger(log_level=logging.DEBUG):
    for handler_name in log_config_dict["handlers"]:
        handler = log_config_dict["handlers"][handler_name]
        if "filename" in handler:
            log_file_path = handler["filename"]
            if not os.path.exists(log_file_path):
                handler["filename"] = default_log_file_path
    try:
        # 从配置文件中读取日志配置
        if log_config_dict:
            logging.config.dictConfig(log_config_dict)
        else:
            # 如果配置文件中没有配置日志，使用默认配置
            return get_default_logger()
    except FileNotFoundError:
        # 如果目标日志文件路径不存在，使用默认配置
        return get_default_logger()

    manual_logger = logging.getLogger("FinanceDataAPI_manual_logger")
    if log_level:
        manual_logger.setLevel(log_level)
    return manual_logger


if __name__ == '__main__':
    logger = get_manual_logger(logging.INFO)
    print(logger)
    logger.debug("debug---------")
    logger.info("info---------")
    logger.warning("warning---------")
    logger.error("error---------")
