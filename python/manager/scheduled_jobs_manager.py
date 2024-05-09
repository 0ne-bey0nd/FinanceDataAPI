import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from entity.scheduled_job import ScheduledJobItem
from utils.log_utils import get_logger
from settings import SERVER_HOST, SERVER_PORT

logger = get_logger()


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
        self.job_app_url = f"http://{'127.0.0.1' if SERVER_HOST=='0.0.0.0' else SERVER_HOST}:{SERVER_PORT}/job/submit"

    def load_scheduled_jobs_config(self, scheduled_jobs_config_dir_path):
        logger.info(f"Loading scheduled jobs config: {scheduled_jobs_config_dir_path}")
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
        logger.info(f"Loading scheduled job config: {scheduled_job_config_path}")

        with open(scheduled_job_config_path, "r") as f:
            scheduled_job_item = ScheduledJobItem.parse_raw(f.read())
            self.add_scheduled_job(scheduled_job_item)
        ...

    def add_scheduled_job(self, scheduled_job_item: ScheduledJobItem):
        self.job_item_list.append(scheduled_job_item)

        def submit_scheduled_job():
            logger.info("submit scheduled job")
            # submit a job to the server
            job_json_dict = json.loads(scheduled_job_item.json())

            logger.debug(f"job_json: {job_json_dict}")
            logger.debug(f"type(job_json): {type(job_json_dict)}")

            # submit job
            response = requests.post(self.job_app_url, json=job_json_dict)

            logger.debug(f"response status code: {response.status_code}")
            logger.info(f"response content: {response.content}")
            ...

        trigger_type = scheduled_job_item.trigger.type
        schedule = scheduled_job_item.trigger.arguments
        self.scheduler.add_job(submit_scheduled_job, trigger=trigger_type, **schedule)
        logger.info(f"Scheduler job added: {scheduled_job_item}")

    def start_scheduler(self):
        self.scheduler.start()
        logger.info("Scheduler started.")


if __name__ == '__main__':
    from settings import SCHEDULED_JOBS_CONFIG_DIR_PATH

    scheduled_jobs_manager = ScheduledJobsManager.get_instance()
    scheduled_jobs_manager.load_scheduled_jobs_config(SCHEDULED_JOBS_CONFIG_DIR_PATH)
    ...
