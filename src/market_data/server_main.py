import asyncio
import json
import time
from typing import Optional, Dict, Any, List

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import uvicorn
import logging
import os

from pydantic import BaseModel

logger = logging.getLogger("FinanceDataAPI")

logger.setLevel(logging.DEBUG)
# 设置日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

LOG_DIR_ABS_PATH = os.path.abspath(
    r"D:\PROJECT\QUANTITATIVE_INVESTING\FinanceDataAPI\log")  # todo 将path的读入改为从配置文件中获， 直接写在代码中不安全
LOG_FILE_NAME = os.path.join(LOG_DIR_ABS_PATH, "FinanceDataAPI.log")

# 输出到日志文件
to_file = logging.FileHandler(LOG_FILE_NAME, mode='a', encoding='utf-8')
to_file.setFormatter(formatter)
logger.addHandler(to_file)

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


@app.post("/job/submit")
def job(job_item: JobItem):
    print(job_item)
    return job_item.__str__()
    ...


def scheduler_test():
    print("this is a scheduler test")
    # submit a job to the server

    # load json file
    json_file_path = os.path.abspath(
        r"D:\PROJECT\QUANTITATIVE_INVESTING\FinanceDataAPI\examples\scheduled_jobs\trade_day\bao_stock_trade_day.json")
    with open(json_file_path, "r") as f:
        job_json = json.load(f)
    print(job_json)
    # submit job

    response = requests.post("http://127.0.0.1:8000/job/submit", json=job_json)
    print(response.json())

    print(f"response status code: {response.status_code}")
    print(f"response content: {response.content}")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting BackgroundScheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduler_test, 'cron', second='*/3')
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app="server_main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
