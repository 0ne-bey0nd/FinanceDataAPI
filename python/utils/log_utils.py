from logger import LOGGER,LoggerFactory


def release_logger_handlers(thread_id):
    logger = LoggerFactory.get_logger()
    LoggerFactory.release_handlers(logger)


def register_job_logger(job_id):
    thread_logger = LoggerFactory.create_thread_logger()
    LoggerFactory.load_handlers(thread_logger,
                                LoggerFactory.create_handlers(logger_type=LoggerFactory.LoggerType.JOB,
                                                              job_id=job_id))

def get_server_logger():
    return LoggerFactory.get_main_thread_logger()

def get_logger_by_thread_id(thread_id):
    return LoggerFactory.get_logger_by_thread_id(thread_id)

def get_logger():
    return LOGGER


if __name__ == '__main__':
    logger = get_logger()
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    server_logger = get_server_logger()
    server_logger.debug("Server Debug message")
    server_logger.info("Server Info message")
    server_logger.warning("Server Warning message")
    server_logger.error("Server Error message")

