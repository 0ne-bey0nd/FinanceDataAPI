from pydantic import BaseModel
from typing import Optional, Any
from pipeline import Pipeline, ComponentBase
from utils.log_utils import get_logger
from manager.component_manager import ComponentManager
import threading

logger = get_logger()


class ComponentItem(BaseModel):
    component_class_name: str
    pre_component_name: Optional[str]
    component_arguments: dict[str, Any]
    ...


class JobItem(BaseModel):
    pipeline_structure: dict[str, ComponentItem]


class Job:
    class JobStatus:
        WAITING = "waiting"
        RUNNING = "running"
        FINISHED = "finished"
        FAILED = "failed"

    def __init__(self):
        self.job_item: JobItem = None
        self.job_id: str = None
        self.pipeline: Pipeline = None
        self.mutex: threading.Lock = None
        self.status: bool = False
        ...

    @staticmethod
    def create_job(job_id: str, job_item: JobItem) -> "Job":
        job = Job()
        job.job_id = job_id
        job.job_item = job_item
        job.mutex = threading.Lock()

        job.pipeline = Pipeline()
        for component_name, component_item in job_item.pipeline_structure.items():
            component_class_name = component_item.component_class_name
            if component_item.pre_component_name:
                pre_component_item = job_item.pipeline_structure.get(component_item.pre_component_name)
                # todo

            component_arguments = component_item.component_arguments
            component_class = ComponentManager.get_instance().get_component_class_by_name(component_class_name)
            logger.info(f"is subclass: {issubclass(component_class, ComponentBase)}")
            job.pipeline.add_component(component_class, component_arguments)
            logger.debug(f"Component added: {component_class_name} {component_arguments}")

        return job

    def run(self) -> bool:
        logger.info(f"{self} begin to run")
        self.pipeline.run()
        logger.info(f"{self} end to run")
        return True

    def __str__(self):
        return f"Job(job_id={self.job_id})"

    def __repr__(self):
        return self.__str__()
