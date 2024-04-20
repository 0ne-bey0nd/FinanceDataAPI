import asyncio
import time

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import uvicorn
import logging
import os

logger = logging.getLogger("FinanceDataAPI")

logger.setLevel(logging.DEBUG)
# 设置日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

LOG_DIR_ABS_PATH = os.path.abspath(
    "D:\PROJECT\QUANTITATIVE_INVESTING\FinanceDataAPI\log")  # todo 将path的读入改为从配置文件中获， 直接写在代码中不安全
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


def job():
    print("I'm working...")
    print("debug---------")
    print("info---------")
    print("warning---------")
    print("error---------")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting BackgroundScheduler")
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', second='*/3')
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run(app="server_main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
