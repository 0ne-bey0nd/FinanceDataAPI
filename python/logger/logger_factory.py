import os
import logging
import threading
from settings import LOG_DIR_PATH, log_config_dict


class LoggerFactory(object):
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

    thread_id_to_logger_dict = {}

    class LoggerType:
        DEFAULT = "default"
        SERVER = "server"
        JOB = "job"

    @classmethod
    def get_logger(cls, logger_type=LoggerType.DEFAULT, log_level=DEFAULT_LEVEL):

        if logger_type == cls.LoggerType.DEFAULT:
            return cls.get_default_logger(log_level=log_level)
        elif logger_type == cls.LoggerType.SERVER:
            return cls.get_job_logger("server", log_level=log_level)
        elif logger_type == cls.LoggerType.JOB:
            return cls.get_job_logger(None, log_level=log_level)

    @classmethod
    def get_log_level_name(cls, log_level):
        return logging.getLevelName(log_level)

    @classmethod
    def create_job_logger(cls, thread_id, job_id, log_level=DEFAULT_LEVEL):
        logger = cls.create_logger(log_level=log_level, log_type=cls.LoggerType.JOB, job_id=job_id)
        cls.thread_id_to_logger_dict[thread_id] = logger
        logger.info(f"job logger created for job_id: {job_id}, thread_id: {thread_id}")
        ...

    @classmethod
    def delete_job_logger(cls, thread_id):
        job_logger = cls.thread_id_to_logger_dict.get(thread_id, None)
        if job_logger:
            del cls.thread_id_to_logger_dict[thread_id]
            cls.release_logger(job_logger)
            job_logger.info(f"job logger deleted for thread_id: {thread_id}")


    @classmethod
    def release_logger(cls, logger: logging.Logger):
        logger.handlers.clear()

    @classmethod
    def get_job_logger(cls, job_id, log_level=DEFAULT_LEVEL):

        thread_id = threading.get_ident()
        job_logger = cls.thread_id_to_logger_dict.get(thread_id, None)
        if not job_logger:
            if job_id is None:
                raise Exception("job logger has not been created yet")
            cls.create_job_logger(threading.get_ident(), job_id, log_level=log_level)

        job_logger = cls.thread_id_to_logger_dict.get(thread_id, None)
        if not job_logger:
            raise Exception("Job logger not found")
        return job_logger

    @classmethod
    def create_default_logger(cls, log_level=DEFAULT_LEVEL):
        default_logger = logging.getLogger(cls.DEFAULT_LOG_NAME)

        formatter = logging.Formatter(cls.replace_format_str(cls.DEFAULT_LOG_FORMAT_STR))
        to_console = logging.StreamHandler()
        to_console.setFormatter(formatter)
        default_logger.addHandler(to_console)

        os.makedirs(cls.DEFAULT_LOG_DIR_PATH, exist_ok=True)
        file_handler = logging.FileHandler(cls.DEFAULT_LOG_PATH, encoding=cls.DEFAULT_ENCODING)
        file_handler.setFormatter(formatter)
        default_logger.addHandler(file_handler)

        if log_level:
            default_logger.setLevel(log_level)
        return default_logger

    @classmethod
    def get_default_logger(cls, log_level=DEFAULT_LEVEL):
        if cls.default_logger:
            return cls.default_logger

        default_logger = cls.create_default_logger(log_level=log_level)
        return default_logger

    @classmethod
    def replace_format_str(cls, format_str: str, *args, **kwargs):
        try:
            replaced_formatter_str = format_str.replace("job_id", kwargs.get("job_id", "FDA_Server"))
            return replaced_formatter_str
        except KeyError:
            pass

    @classmethod
    def get_log_dir_path(cls, logger_name: str = None, log_level=DEFAULT_LEVEL, log_type: str = LoggerType.SERVER,
                         *args,
                         **kwargs) -> str:

        log_dir_path = ""
        if log_type == cls.LoggerType.SERVER:
            log_dir_path = os.path.join(cls.DEFAULT_LOG_DIR_PATH, "server")
        elif log_type == cls.LoggerType.JOB:
            job_id = kwargs.get("job_id", None)
            if not job_id:
                raise ValueError("job_id is required for job log")
            log_dir_path = os.path.join(cls.DEFAULT_LOG_DIR_PATH, job_id)

        os.makedirs(log_dir_path, exist_ok=True)
        return log_dir_path

    @classmethod
    def create_log_file_handler(cls, log_dir_path, log_level=DEFAULT_LEVEL,
                                *args,
                                **kwargs):
        formatter = logging.Formatter(cls.replace_format_str(cls.DEFAULT_LOG_FORMAT_STR, *args, **kwargs))

        log_file_path = os.path.join(log_dir_path, f"{cls.get_log_level_name(log_level)}.log")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        return file_handler

    @classmethod
    def create_stream_handler(cls, log_level=DEFAULT_LEVEL, *args, **kwargs):
        formatter = logging.Formatter(cls.replace_format_str(cls.DEFAULT_LOG_FORMAT_STR, *args, **kwargs))
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        return stream_handler

    @classmethod
    def create_logger(cls, logger_name: str = None, log_level=DEFAULT_LEVEL, log_type: str = LoggerType.SERVER, *args,
                      **kwargs):

        log_dir_path = cls.get_log_dir_path(logger_name=logger_name, log_level=log_level, log_type=log_type, *args,
                                            **kwargs)
        logger = logging.getLogger(logger_name)
        # 创建多个handler
        to_console = cls.create_stream_handler(log_level=log_level, *args, **kwargs)
        error_handler = cls.create_log_file_handler(log_dir_path, log_level=logging.ERROR, *args, **kwargs)
        info_handler = cls.create_log_file_handler(log_dir_path, log_level=logging.INFO, *args, **kwargs)
        debug_handler = cls.create_log_file_handler(log_dir_path, log_level=logging.DEBUG, *args, **kwargs)

        logger.addHandler(to_console)
        logger.addHandler(error_handler)
        logger.addHandler(info_handler)
        logger.addHandler(debug_handler)

        logger.setLevel(log_level)
        return logger


def get_logger(log_level=logging.INFO):
    current_thread_id = threading.get_ident()
    # print(f"current_thread_id: {current_thread_id}")
    if threading.current_thread() == threading.main_thread():
        logger_type = LoggerFactory.LoggerType.SERVER
    else:
        logger_type = LoggerFactory.LoggerType.JOB
    logger = LoggerFactory.get_logger(logger_type=logger_type, log_level=log_level)
    if not logger:
        logger = LoggerFactory.get_default_logger(log_level=log_level)
    return logger


if __name__ == '__main__':
    from settings import LOG_DIR_PATH
