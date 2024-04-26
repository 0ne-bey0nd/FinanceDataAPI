from typing import Any
from pydantic import BaseModel
from entity.job import ComponentItem

class ScheduledJobTrigger(BaseModel):
    type: str
    arguments: dict[str, Any]


class ScheduledJobItem(BaseModel):
    pipeline_structure: dict[str, ComponentItem]
    trigger: ScheduledJobTrigger
