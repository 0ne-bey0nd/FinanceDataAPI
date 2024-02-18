# api_url = 'https://www.szse.cn/api/market/ssjjhq/getHistoryData?cycleType=32&marketId=1&code=000001'
# 有反爬

API_SUFFIX = 'https://www.szse.cn/api/market/ssjjhq/getHistoryData'

import requests
from market_data.data_api._base import DataAPICandlestickDayBase
from datetime import date, datetime
from market_data.candlestick.day import CandlestickDay
import pandas as pd

# 日k线 api

PARAM_LIST = {
    'cycleType': '32',
    'marketId': '1',
    # 'code': '000001'
}

from market_data.candlestick.day import CandlestickDay, CandlestickDictKeyDay

DAY_KLINE_LIST_INDEX_NAME = [CandlestickDictKeyDay.DATE,
                             CandlestickDictKeyDay.BEGIN,
                             CandlestickDictKeyDay.NOW,
                             CandlestickDictKeyDay.LOWEST,
                             CandlestickDictKeyDay.HIGHEST,
                             'rise and fall',
                             'ratio of rise and fall',
                             CandlestickDictKeyDay.TOTAL_LOT,
                             CandlestickDictKeyDay.TOTAL_MONEY, ]


class DataAPICandlestickDaySZSE(DataAPICandlestickDayBase):
    def __init__(self):
        super().__init__(api_suffix=API_SUFFIX, param_list=PARAM_LIST)
        self.cache_data: dict[str, pd.DataFrame] = {}

    def prepare_param_list(self, code: str):
        self.param_list['code'] = code

    def request_api(self, code: str, proxies=None) -> dict:
        if proxies is None:
            proxies = {'http': None, 'https': None}
        api_url = self.get_api_url(code=code)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'}
        res = requests.request("get", api_url, proxies=proxies, headers=headers)
        data_in_json = res.json()

        return data_in_json

    def parse_one_day_candlestick_data_list(self, one_dayK_data_list):
        one_kline_data_dict = dict(zip(DAY_KLINE_LIST_INDEX_NAME, one_dayK_data_list))
        one_kline_data_dict['date'] = str(one_kline_data_dict['date'])
        return one_kline_data_dict

    def refresh_cache_data(self, code: str):
        data_in_json = self.request_api(code)
        code = data_in_json['data']['code']
        name = data_in_json['data']['name']
        kline_data_list = data_in_json['data']['picupdata']
        self.cache_data[code] = pd.DataFrame(kline_data_list, columns=DAY_KLINE_LIST_INDEX_NAME)
        self.cache_data[code][CandlestickDictKeyDay.DATE] = pd.to_datetime(
            self.cache_data[code][CandlestickDictKeyDay.DATE])

    def get_one_day_candlestick_instance(self, code: str, date: date) -> CandlestickDay:
        if code not in self.cache_data:
            self.refresh_cache_data(code)
        data = self.cache_data[code]
        # print(data)
        # print(data.dtypes)

        one_day_data = data[data[CandlestickDictKeyDay.DATE] == pd.to_datetime(date)]
        # print(one_day_data)
        if one_day_data.empty:
            return None
        one_day_data = one_day_data.iloc[0]
        return CandlestickDay.init_with_dict(one_day_data.to_dict())


if __name__ == '__main__':
    code = "399300"
    date = datetime.today().date()
    # date = datetime(2023, 10, 4).date()
    api = DataAPICandlestickDaySZSE()
    # print(api.get_api_url(code))
    # print(api.request_api(code))
    print(api.get_one_day_candlestick_instance(code=code, date=date))

    # code01 = "000333"
    # code02 = "002415"
    #
    # print(api.get_one_day_candlestick_instance(code=code01, date=date))
    # print(api.get_one_day_candlestick_instance(code=code02, date=date))
