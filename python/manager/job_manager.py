import uuid
from datetime import datetime

from entity.job import JobItem, Job
from logger import get_manual_logger

logger = get_manual_logger()


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

    def load_job(self, job_item: JobItem):
        timestamp = datetime.now()
        job_id = f"{timestamp.strftime('%Y%m%d%H%M%S%f')}-{uuid.uuid4()}"
        logger.info(f"job_id: {job_id}")
        job = Job.create_job(job_id, job_item)
        self.job_ready_to_run_dict[job_id] = job
        trigger_type, schedule = job_item.trigger.get("type"), job_item.trigger.get("arguments")
        logger.debug(f"trigger_type: {trigger_type}, schedule: {schedule}")

    def run_job(self, job_id):
        job: Job = self.job_ready_to_run_dict.get(job_id, None)
        if job is None:
            logger.error(f"Job not found: {job_id}")
            return
        success = job.run()
        if success:
            self.job_ready_to_run_dict.pop(job_id)
        return success

    def run_all_jobs(self):
        for job_id in self.job_ready_to_run_dict.keys():
            self.run_job(job_id)

    def __init__(self):
        self.job_ready_to_run_dict: dict[str:Job] = {}


if __name__ == '__main__':
    job_manager = JobManager.get_instance()

    ...
