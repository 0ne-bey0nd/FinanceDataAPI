from fastapi import APIRouter
from entity.job import JobItem
from logger import get_manual_logger

logger = get_manual_logger()
job_router = APIRouter()


@job_router.post("/job/submit")
def job_submit(job_item: JobItem):
    logger.debug(job_item)
    component_item_dict = job_item.pipeline_structure
    for component_name, component_item in component_item_dict.items():
        logger.debug(f"component_name: {component_name} component_item: {component_item}")
    return job_item.__str__()
