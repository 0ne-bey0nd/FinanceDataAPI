import requests
from DayK import DayK

TODAY = -1

api_host = 'yunhq.sse.com.cn'
api_port = '32041'

# 日k线 api
api = '/v1/sh1/dayk/000001'


def get_api_url(api_host=api_host, api_port=api_port, api=api, param_list=None):
    if param_list is None:
        param_list = {}
    return f"http://{api_host}:{api_port}{api}?" + "&".join(
        f"{param_key}={param_value}" for param_key, param_value in param_list.items())


def request_api(api_url):
    res = requests.request("get", api_url)
    data_in_json = res.json()

    return data_in_json


DAY_KLINE_LIST_INDEX = ['date', 'begin', 'highest', 'lowest', 'average', 'total_lot', 'total_money']


def parse_one_dayK_data_list(one_dayK_data_list):
    one_kline_data_dict = dict(zip(DAY_KLINE_LIST_INDEX, one_dayK_data_list))
    one_kline_data_dict['date'] = str(one_kline_data_dict['date'])
    return one_kline_data_dict


def get_one_dayK_instance(data_dict):
    return DayK.initDayKInstance(data_dict=data_dict)
