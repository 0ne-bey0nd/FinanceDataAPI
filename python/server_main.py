from fastapi import FastAPI
import uvicorn
from settings import STORAGE_CONFIG_FILE_PATH, SCHEDULED_JOBS_CONFIG_DIR_PATH, SERVER_HOST, SERVER_PORT, RELOAD_SYMBOL
from manager.component_manager import ComponentManager
from manager.storage_engine_manager import StorageEngineManager
from manager.scheduled_jobs_manager import ScheduledJobsManager
from manager.job_manager import JobManager
from apps.job_app import job_router
from utils.log_utils import get_logger

logger = get_logger()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello FinanceDataAPI"}


@app.get("/test")
async def test():
    # logger.debug("This is the test debug message.")
    # await asyncio.sleep(3)    # 异步阻塞不会停止整个程序，但会阻塞当前路由的响应
    # time.sleep(3)             # 非异步阻塞会停止整个程序，包括其他路由的响应
    return {"message": "Hello test"}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting register component")

    component_manager = ComponentManager.get_instance()
    component_manager.register_component()

    logger.info("Starting load storage config")

    storager_manager = StorageEngineManager.get_instance()
    storager_manager.load_storage_config(STORAGE_CONFIG_FILE_PATH)

    logger.info("Starting initialize job manager")
    job_manager = JobManager.get_instance()
    job_manager.initialize()

    logger.info("Starting load scheduled jobs config")
    scheduled_jobs_manager = ScheduledJobsManager.get_instance()
    scheduled_jobs_manager.load_scheduled_jobs_config(SCHEDULED_JOBS_CONFIG_DIR_PATH)

    # logger.info("Starting BackgroundScheduler")
    # scheduled_jobs_manager.start_scheduler()

    app.include_router(job_router)


if __name__ == '__main__':
    uvicorn.run(app="server_main:app", host=SERVER_HOST, port=SERVER_PORT, reload=RELOAD_SYMBOL)
