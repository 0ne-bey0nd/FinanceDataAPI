from fastapi import APIRouter
from entity.job import JobItem
from logger import get_manual_logger
from manager.job_manager import JobManager

logger = get_manual_logger()
job_router = APIRouter()


@job_router.post("/job/submit")
def job_submit(job_item: JobItem):
    logger.debug(f"received job: {job_item}")
    job_manager = JobManager.get_instance()

    logger.info(f"loading job: {job_item}")
    job_manager.load_job(job_item)

    # here may be replaced by scheduler programme
    logger.info(f"begin to run job: {job_item}")
    job_manager.run_all_jobs()
