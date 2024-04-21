from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pipeline import Pipeline
from logger import get_manual_logger
from manager.component_manager import ComponentManager

logger = get_manual_logger()


class ComponentItem(BaseModel):
    component_class_name: str
    pre_component_name: Optional[str]
    component_arguments: Dict[str, Any]
    ...


class JobItem(BaseModel):
    pipeline_structure: Dict[str, ComponentItem]
    trigger: Dict[str, Any]


class Job:

    def __init__(self):
        self.job_item: JobItem = None
        self.job_id: str = None
        self.pipeline = None
        ...

    @staticmethod
    def create_job(job_id, job_item):
        job = Job()
        job.job_id = job_id
        job.job_item = job_item

        logger.debug(job_item.trigger)

        job.pipeline = Pipeline()
        for component_name, component_item in job_item.pipeline_structure.items():
            component_class_name = component_item.component_class_name
            if component_item.pre_component_name:
                pre_component_item = job_item.pipeline_structure.get(component_item.pre_component_name)
                # todo

            component_arguments = component_item.component_arguments
            component_class = ComponentManager.get_instance().get_component_class_by_name(component_class_name)
            job.pipeline.add_component_class(component_class)
            logger.debug(f"Component added: {component_class_name} {component_arguments}")

        return job

    def run(self):
        logger.info(f"job begin to run: {self}")
        self.pipeline.run()
        logger.info(f"job end to run: {self}")
        ...

    def __str__(self):
        return f"Job(job_id={self.job_id}, job_item={self.job_item})"

    def __repr__(self):
        return self.__str__()
