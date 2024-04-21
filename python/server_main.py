import asyncio
import json
import time
from typing import Optional, Dict, Any, List
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import uvicorn
import os
from pydantic import BaseModel
from market_data.pipeline._base import *
import inspect
import importlib
from logger import get_default_logger, get_manual_logger

logger = get_manual_logger()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test")
async def test():
    # logger.debug("This is the test debug message.")
    # await asyncio.sleep(3)    # 异步阻塞不会停止整个程序，但会阻塞当前路由的响应
    # time.sleep(3)             # 非异步阻塞会停止整个程序，包括其他路由的响应
    return {"message": "Hello test"}


class ComponentItem(BaseModel):
    component_class_name: str
    pre_component_name: Optional[str]
    component_arguments: Dict[str, Any]
    ...


class JobItem(BaseModel):
    pipeline_structure: Dict[str, ComponentItem]


def register_component():
    PIPELINE_MODULE_PATH = os.path.dirname(importlib.import_module('market_data.pipeline').__file__)
    components_path = os.path.join(PIPELINE_MODULE_PATH, 'components')

    pipeline_module_path_list = []
    component_class_list = []
    component_name_to_class_dict = {}

    # 遍历components目录下的所有py文件
    for root, dirs, files in os.walk(components_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                pipeline_module_path_list.append(file_path)

    from pathlib import Path

    def _get_module_name_by_path(path, base):
        return '.'.join(path.resolve().relative_to(base.resolve()).with_suffix('').parts)

    for pipeline_module_path in pipeline_module_path_list:
        module_name = _get_module_name_by_path(Path(pipeline_module_path), Path(PIPELINE_MODULE_PATH))
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, ComponentBase):
                component_class_list.append(obj)
                component_name_to_class_dict[obj.get_component_name()] = obj

    logger.debug(component_name_to_class_dict)


@app.post("/job/submit")
def job(job_item: JobItem):
    logger.debug(job_item)
    component_item_dict = job_item.pipeline_structure
    for component_name, component_item in component_item_dict.items():
        logger.debug(f"component_name: {component_name} component_item: {component_item}")

    return job_item.__str__()


def scheduler_test():
    logger.debug("this is a scheduler test")
    # submit a job to the server

    # load json file
    json_file_path = os.path.abspath(
        r"D:\PROJECT\QUANTITATIVE_INVESTING\examples\scheduled_jobs\trade_day\bao_stock_trade_day.json")
    with open(json_file_path, "r") as f:
        job_json = json.load(f)
    logger.debug(job_json)
    # submit job

    response = requests.post("http://127.0.0.1:8000/job/submit", json=job_json)
    logger.debug(response.json())

    logger.debug(f"response status code: {response.status_code}")
    logger.debug(f"response content: {response.content}")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting BackgroundScheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduler_test, 'cron', second='*/3')
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app="server_main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
