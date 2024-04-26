import threading
from entity.job import Job
import queue
from utils.log_utils import get_logger, register_job_logger, delete_job_logger

logger = get_logger()


class JobExecutor(threading.Thread):
    def __init__(self, executor_id: int, job_queue: queue.Queue):
        super().__init__()
        self.executor_id = executor_id
        self.job_queue = job_queue
        self.current_job: Job = None
        self.start()

    def run_a_job(self, job: Job) -> bool:
        if not job:
            logger.error("Job is not set!")
            return False
        if job.status != job.JobStatus.WAITING:
            logger.error(f"{job} is {job.status}, not waiting!")
            return False

        register_job_logger(self.ident, job.job_id)
        logger.info(f"Thread id {self.ident} begin to run job: {job}")
        with job.mutex:
            job.status = job.JobStatus.RUNNING
            try:
                success = job.run()
            except Exception as e:
                logger.error(f"Job failed: {job}, error: {e}")
                success = False
                job.status = job.JobStatus.FAILED
            if success:
                logger.info(f"Job success finished: {job}")
                job.status = job.JobStatus.FINISHED
            else:
                logger.error(f"Job failed: {job}")
                job.status = job.JobStatus.FAILED
        logger.info(f"Thread id {self.ident} end to run job: {job}")
        delete_job_logger(self.ident)
        return success

    def run(self) -> None:
        while True:
            job = self.job_queue.get(block=True)
            logger.info(f"JobExecutor {self.executor_id}:{self.ident} get a job: {job}")
            self.current_job = job

            self.run_a_job(job)

            self.current_job = None
            self.job_queue.task_done()


class JobExecuteMainThread(threading.Thread):
    _job_executor_instance_dict: dict[int:JobExecutor] = {}
    _job_queue = queue.Queue()
    _job_queue_mutex = threading.Lock()

    def __init__(self, max_executors: int = 4):
        super().__init__()
        self.max_executors = max_executors

    def initialize(self):
        logger.info(f"start job execute main thread with {self.max_executors} executors")

        for i in range(self.max_executors):
            job_executor = JobExecutor(i, self._job_queue)
            logger.info(f"JobExecutor {i}:{job_executor.ident} is created")
            self._job_executor_instance_dict[job_executor.ident] = job_executor

    def run(self) -> None:
        self.initialize()
        for job_executor_thread_ident, job_executor in self._job_executor_instance_dict.items():
            job_executor.join()

    @classmethod
    def add_job_to_execute(cls, job: Job):
        logger.debug(f"JobExecuteMainThread.add_job_to_execute: {job}")
        with cls._job_queue_mutex:
            cls._job_queue.put(job)
            logger.info(f"Job added to the queue: {job}")

    @classmethod
    def get_job_executor_by_thread_id(cls, thread_id):
        return cls._job_executor_instance_dict.get(thread_id, None)


if __name__ == '__main__':
    logger.info("JobExecutor test")
    job_execute_main_thread = JobExecuteMainThread()
    job_execute_main_thread.start()
    job_execute_main_thread.join()
