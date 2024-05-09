import os
import logging
import threading
from settings import LOG_DIR_PATH, log_config_dict


class LoggerFactory:
    __thread_id_to_logger_dict = {}
    __thread_id_to_handlers_dict = {}
    DEFAULT_LOG_NAME = "FinanceDataAPI_default_logger"
    DEFAULT_LOG_FORMAT_STR = log_config_dict.get("default_log_format_str",
                                                 "[%(levelname)s] [%(asctime)s] [job_id] [%(process)s:%(thread)s] - [%(module)s.%(funcName)s] [line:%(lineno)d]: %(message)s")
    DEFAULT_LEVEL = log_config_dict.get("default_level", logging.INFO)
    DEFAULT_ENCODING = log_config_dict.get("default_encoding", "utf-8")
    DEFAULT_LOG_DIR_PATH = LOG_DIR_PATH
    DEFAULT_LOG_PATH = os.path.join(LOG_DIR_PATH, "finance_data_api.log")
    default_logger = None
    log_format_dict = {
        "default": DEFAULT_LOG_FORMAT_STR,
    }

    __main_thread_logger: logging.Logger = None

    class LoggerType:
        DEFAULT = "default"
        SERVER = "server"
        JOB = "job"

    @classmethod
    def _init_main_thread_logger(cls):
        cls.__main_thread_logger = cls.create_thread_logger()
        cls.load_handlers(cls.__main_thread_logger, cls.create_handlers())

    @classmethod
    def get_main_thread_logger(cls):
        return cls.__main_thread_logger

    @classmethod
    def get_thread_id_to_logger_dict(cls):
        return cls.__thread_id_to_logger_dict

    @classmethod
    def get_thread_id_to_handlers_dict(cls):
        return cls.__thread_id_to_handlers_dict

    @classmethod
    def get_logger_by_thread_id(cls, thread_id):
        return cls.__thread_id_to_logger_dict.get(thread_id, None)

    @classmethod
    def get_logger(cls, log_level=logging.DEBUG) -> logging.Logger:
        thread_id = threading.get_ident()
        logger_type = cls.LoggerType.SERVER

        if thread_id == threading.main_thread().ident:
            return cls.__main_thread_logger
        logger = cls.__thread_id_to_logger_dict.get(thread_id, None)
        if not logger:
            logger = cls.create_thread_logger(log_level=log_level)
        handlers = cls.__thread_id_to_handlers_dict.get(thread_id, None)
        if not handlers:
            handlers = cls.create_handlers(logger_type=logger_type, log_level=log_level)
        cls.load_handlers(logger, handlers)
        return logger

    @classmethod
    def load_handlers(cls, logger: logging.Logger, handlers):
        for handler in handlers:
            logger.addHandler(handler)

    @classmethod
    def release_handlers(cls, logger: logging.Logger):
        # print(f"{logger.handlers} to release")
        for handler in logger.handlers[:]:  # this is important for avoiding changing iterable size during iteration
            logger.removeHandler(handler)

        cls.__thread_id_to_handlers_dict[threading.get_ident()] = None
        # logger.info("release_handlers")

    @classmethod
    def create_thread_logger(cls, log_level=logging.DEBUG):
        thread_id = threading.get_ident()
        logger_name = f"logger_{thread_id}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        cls.__thread_id_to_logger_dict[thread_id] = logger
        return logger

    @classmethod
    def create_handlers(cls, logger_type=LoggerType.SERVER, log_level=logging.DEBUG, job_id=None):
        handlers = []
        stream_handler = logging.StreamHandler()
        log_file_dir_path = os.path.join(cls.DEFAULT_LOG_DIR_PATH, "server")
        if logger_type == cls.LoggerType.SERVER:
            job_id = "server"
        elif logger_type == cls.LoggerType.JOB:
            if job_id is None:
                raise ValueError("job_id must be provided when logger_type is JOB")
            log_file_dir_path = os.path.join(cls.DEFAULT_LOG_DIR_PATH, job_id)
        else:
            job_id = None
        formatter = logging.Formatter(
            cls.DEFAULT_LOG_FORMAT_STR.replace(
                "job_id", str(job_id)))
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(log_level)
        stream_handler.set_name(f"stream_handler_{job_id}")

        os.makedirs(log_file_dir_path, exist_ok=True)
        debug_file_handler = logging.FileHandler(os.path.join(log_file_dir_path, "debug.log"),
                                                 encoding=cls.DEFAULT_ENCODING)
        debug_file_handler.setFormatter(formatter)
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.set_name(f"debug_file_handler_{job_id}")

        info_file_handler = logging.FileHandler(os.path.join(log_file_dir_path, "info.log"),
                                                encoding=cls.DEFAULT_ENCODING)
        info_file_handler.setFormatter(formatter)
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.set_name(f"info_file_handler_{job_id}")

        error_file_handler = logging.FileHandler(os.path.join(log_file_dir_path, "error.log"),
                                                 encoding=cls.DEFAULT_ENCODING)
        error_file_handler.setFormatter(formatter)
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.set_name(f"error_file_handler_{job_id}")

        handlers.append(stream_handler)
        handlers.append(debug_file_handler)
        handlers.append(info_file_handler)
        handlers.append(error_file_handler)
        cls.__thread_id_to_handlers_dict[threading.get_ident()] = handlers
        return handlers


LoggerFactory._init_main_thread_logger()


class LOGGER:
    @classmethod
    def debug(cls, message):
        logger = LoggerFactory.get_logger()
        logger.debug(message, stacklevel=2)

    @classmethod
    def info(cls, message):
        logger = LoggerFactory.get_logger()
        logger.info(message, stacklevel=2)
        return logger

    @classmethod
    def warning(cls, message):
        logger = LoggerFactory.get_logger()
        logger.warning(message, stacklevel=2)

    @classmethod
    def error(cls, message):
        logger = LoggerFactory.get_logger()
        logger.error(message, stacklevel=2)


if __name__ == '__main__':
    LOGGER.debug("debug")
    LOGGER.info("info")
    LOGGER.warning("warning")
    LOGGER.error("error")
