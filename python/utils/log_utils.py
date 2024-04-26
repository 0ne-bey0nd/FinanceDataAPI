from logger.logger_factory import LoggerFactory, get_logger as _get_logger
import logging


def delete_job_logger(thread_id):
    LoggerFactory.delete_job_logger(thread_id)


def register_job_logger(thread_id, job_id, log_level=LoggerFactory.DEFAULT_LEVEL):
    LoggerFactory.create_job_logger(thread_id, job_id, log_level=log_level)


def get_logger(log_level=logging.INFO):
    return _get_logger(log_level=log_level)


if __name__ == '__main__':
    logger = get_logger(logging.DEBUG)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
