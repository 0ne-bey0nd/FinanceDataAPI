import threading

from fastapi import APIRouter
from entity.job import JobItem
from utils.log_utils import get_logger
from manager.job_manager import JobManager

logger = get_logger()
job_router = APIRouter()


@job_router.post("/job/submit")
async def job_submit(job_item: JobItem):
    print(threading.main_thread().ident)
    print(threading.get_ident())
    logger.debug(f"received job: {job_item}")
    job_manager = JobManager.get_instance()

    logger.info(f"loading job: {job_item}")
    job_manager.generate_job(job_item)

    # here may be replaced by scheduler programme
    logger.info(f"begin to run job: {job_item}")
    job_manager.run_all_jobs()

    logger.info(f"job is running: {job_item}")
    return {"status": "success", "message": "job is running"}
