from datetime import datetime, date
from dateutil.parser import parse


# 获得具体某一天的日期
# input: date string, e.g. "20210101"
# output: date object

def get_date(date_str: str) -> date:
    return parse(date_str).date()


def get_datetime(date_str: str) -> datetime:
    return parse(date_str)


def get_now() -> datetime:
    # 不同时间的now是不同的对象
    return datetime.now()


# 获得具体某一天的日期
# input: year, month, day (int)
# output: date object

def get_date_by_ymd(year: int, month: int, day: int) -> date:
    return date(year, month, day)


def main():
    print(get_date("20240203"))
    ...


if __name__ == '__main__':
    main()
