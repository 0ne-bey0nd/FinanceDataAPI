# 定时任务管理器
import datetime
import json
import os

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from settings import scheduled_jobs_config_dir_path
from entity.job import JobItem, ComponentItem, Job
from logger import get_manual_logger
import uuid
from pipeline import Pipeline
from manager.component_manager import ComponentManager

logger = get_manual_logger()


class ScheduledJobsManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ScheduledJobsManager.__instance is None:
            ScheduledJobsManager.__instance = object.__new__(cls)
        return ScheduledJobsManager.__instance

    @staticmethod
    def get_instance() -> 'ScheduledJobsManager':
        if ScheduledJobsManager.__instance is None:
            ScheduledJobsManager()
        return ScheduledJobsManager.__instance

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.job_item_list = []

    def load_scheduled_jobs_config(self, scheduled_jobs_config_dir_path):
        logger.debug(f"Loading scheduled jobs config: {scheduled_jobs_config_dir_path}")
        # 读取配置目录下的所有json文件
        if not os.path.exists(scheduled_jobs_config_dir_path):
            logger.error(f"Config directory not found: {scheduled_jobs_config_dir_path}")
            exit(1)

        for root, dirs, files in os.walk(scheduled_jobs_config_dir_path):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    self.load_scheduled_job_config(file_path)

        pass

    def load_scheduled_job_config(self, scheduled_job_config_path):
        logger.debug(f"Loading scheduled job config: {scheduled_job_config_path}")

        ComponentManager.get_instance().register_component()
        with open(scheduled_job_config_path, "r") as f:
            job_item = JobItem.parse_raw(f.read())
            self.add_scheduled_job(job_item)
        ...

    def add_scheduled_job(self, job_item: JobItem):
        self.job_item_list.append(job_item)
        trigger_type, schedule = job_item.trigger.get("type"), job_item.trigger.get("arguments")
        logger.debug(f"trigger_type: {trigger_type}, schedule: {schedule}")

        def submit_scheduled_job():
            logger.debug("this is a scheduler test")
            # submit a job to the server
            job_json = json.loads(job_item.json())

            logger.debug(f"job_json: {job_json}")
            logger.debug(f"type(job_json): {type(job_json)}")
            # submit job
            response = requests.post("http://127.0.0.1:8000/job/submit", json=job_json)
            logger.debug(response.content)

            logger.debug(f"response status code: {response.status_code}")
            logger.debug(f"response content: {response.content}")
            ...

        self.scheduler.add_job(submit_scheduled_job, trigger=trigger_type, **schedule)
        logger.debug(f"Scheduler job added: {job_item}")

    def start_scheduler(self):
        self.scheduler.start()
        logger.info("Scheduler started.")


if __name__ == '__main__':
    scheduled_jobs_manager = ScheduledJobsManager.get_instance()
    scheduled_jobs_manager.load_scheduled_jobs_config(scheduled_jobs_config_dir_path)
    ...
