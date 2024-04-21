from market_data.candlestick.day import CandlestickDay
from datetime import date

class DataAPIBase:
    ...


class DataAPICandlestickBase(DataAPIBase):
    def __init__(self, api_suffix: str, param_list: dict):
        self.api_suffix = api_suffix
        self.param_list = param_list

    def prepare_param_list(self, code: str):
        raise NotImplementedError("prepare_param_list() must be implemented")

    def get_api_url(self, code: str):
        self.prepare_param_list(code)
        if self.param_list is None:
            self.param_list = {}
        return f"{self.api_suffix}?" + "&".join(
            f"{param_key}={param_value}" for param_key, param_value in self.param_list.items())

    def request_api(self, code: str, proxies=None) -> dict:
        raise NotImplementedError("request_api() must be implemented")


class DataAPICandlestickDayBase(DataAPICandlestickBase):
    def __init__(self, api_suffix: str, param_list: dict):
        super().__init__(api_suffix, param_list)

    def get_one_day_candlestick_instance(self, code: str, date: date, use_cache: bool) -> CandlestickDay:
        raise NotImplementedError("get_one_day_candlestick_instance() must be implemented")

    ...


class DataAPICandlestick5DayBase(DataAPICandlestickBase):
    def __init__(self, api_suffix: str, param_list: dict):
        super().__init__(api_suffix, param_list)
        ...


class DataAPICandlestickWeekBase(DataAPICandlestickBase):
    def __init__(self, api_suffix: str, param_list: dict):
        super().__init__(api_suffix, param_list)
        ...


class DataAPICandlestickMonthBase(DataAPICandlestickBase):
    def __init__(self, api_suffix: str, param_list: dict):
        super().__init__(api_suffix, param_list)
        ...


class DataAPICandlestickQuarterBase(DataAPICandlestickBase):
    def __init__(self, api_suffix: str, param_list: dict):
        super().__init__(api_suffix, param_list)
        ...


class DataAPICandlestickYearBase(DataAPICandlestickBase):
    def __init__(self, api_suffix: str, param_list: dict):
        super().__init__(api_suffix, param_list)
        ...
