import uuid
from datetime import datetime
from entity.job import JobItem, Job
from utils.log_utils import get_logger
from manager.component_manager import ComponentManager
from workers.job_executor import JobExecuteMainThread

logger = get_logger()


class JobManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if JobManager.__instance is None:
            JobManager.__instance = super(JobManager, cls).__new__(cls)
        return JobManager.__instance

    @staticmethod
    def get_instance() -> 'JobManager':
        if JobManager.__instance is None:
            JobManager()
        return JobManager.__instance

    def __init__(self):
        self.job_id_to_job_dict: dict[str:Job] = {}  # todo: solve the problem of memory leak
        self.job_execute_main_thread = None

    def initialize(self, max_executors: int = 4):
        self.job_execute_main_thread: JobExecuteMainThread = JobExecuteMainThread(max_executors)
        self.job_execute_main_thread.start()

        logger.info(f"job manager initialized")

    def generate_job_id(self):
        timestamp = datetime.now()
        return f"{timestamp.strftime('%Y%m%d%H%M%S%f')}-{uuid.uuid4()}"

    def generate_job(self, job_item: JobItem):
        ComponentManager.get_instance().register_component()  # 每次加载job时都重新注册一次组件

        job_id = self.generate_job_id()
        logger.info(f"job_id: {job_id}")
        job = Job.create_job(job_id, job_item)
        logger.info(f"job created: {job}")
        job.status = Job.JobStatus.WAITING
        self.job_id_to_job_dict[job_id] = job

    def get_current_job_by_thread_id(self, thread_id):
        job_executor = JobExecuteMainThread.get_job_executor_by_thread_id(thread_id)
        if not job_executor:
            return None
        return job_executor.current_job

    def submit_job_to_execute(self, job_id):
        job: Job = self.job_id_to_job_dict.get(job_id, None)
        if job is None:
            logger.error(f"Job not found: {job_id}")
            return

        JobExecuteMainThread.add_job_to_execute(job)

    def get_job_status(self, job_id):
        job: Job = self.job_id_to_job_dict.get(job_id, None)
        if job is None:
            logger.error(f"Job not found: {job_id}")
            return None

        return job.status

    def run_all_jobs(self):
        current_job_dict = self.job_id_to_job_dict.copy()

        for job_id, job in current_job_dict.items():
            if job.status == Job.JobStatus.WAITING:
                self.submit_job_to_execute(job_id)


if __name__ == '__main__':
    job_manager = JobManager.get_instance()

    ...
