import asyncio
import platform

import aiohttp
import pandas as pd
from pipeline import ProducerBase
import requests
from utils.log_utils import get_logger

logger = get_logger()

from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


if platform.system() == 'Windows':
    # Silence the exception here.
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


class TransactionDataProducer(ProducerBase):

    def produce(self, *args, **kwargs) -> pd.DataFrame:
        # extract arguments
        stock_code_list = kwargs.get('stock_code_list', [])
        limit = kwargs.get('limit', 6)

        # return asyncio.run(self.get_transaction_data_async(stock_code_list, limit))   # 听说 windows 上会报错

        logger.info("begin produce")
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)
        # print(f"thread_loop: {thread_loop} {thread_loop.is_closed()} {id(thread_loop)}")
        # print(asyncio.get_event_loop() == thread_loop)
        res = thread_loop.run_until_complete(self.get_transaction_data_async(stock_code_list, limit))
        thread_loop.close()
        return res

    async def get_transaction_data_async(self, stock_code_list: list, limit: int) -> pd.DataFrame:
        output_data = []
        task_list = []
        for stock_code in stock_code_list:
            # logger.info(f"get_transaction_data: stock_code: {stock_code}")
            # raw_transaction_data = self.get_one_stock_transaction_data(stock_code, limit)  # todo: use async
            # output_data.append((stock_code, raw_transaction_data))
            task_list.append(self.get_one_stock_transaction_data_async(stock_code, limit))

        output_data_list = await asyncio.gather(*task_list)

        output_data = list(zip(stock_code_list, output_data_list))
        return pd.DataFrame(output_data, columns=['stock_code', 'raw_data'])

    async def get_one_stock_transaction_data_async(self, stock_code: str, limit: int = 6) -> str:
        ## stock_code rationality check

        ## limit rationality check

        url = f"https://proxy.finance.qq.com/ifzqgtimg/appstock/app/dealinfo/getMingxiV2?code={stock_code}&limit={limit}&direction=1"

        proxy = "http://127.0.0.1:7890"

        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, ) as session:
            async with session.get(url, proxy=proxy) as response:
                res = await response.text()

        # await asyncio.sleep(0.1)  # 防止“Event loop is closed” 报错，问题参考 https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        return res


if __name__ == '__main__':
    producer = TransactionDataProducer()

    stock_code_list = ['sh600519', 'sz000001']
    transaction_data_data = producer.produce(stock_code_list=stock_code_list)
    print(f"transaction_data_data: {transaction_data_data}")
    print(f"transaction_data_data.shape: {transaction_data_data.shape}")
    print(transaction_data_data['raw_data'][0])
