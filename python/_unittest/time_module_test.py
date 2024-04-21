import unittest
from time_module.utils import get_datetime, get_date, get_date_by_ymd
from datetime import datetime, date

TIME_STR_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_STR_FORMAT = "%Y-%m-%d"

CURRENT_TIME = datetime.now()
CURRENT_DATE = CURRENT_TIME.date()

CURRENT_TIME_STR = CURRENT_TIME.strftime(TIME_STR_FORMAT)
CURRENT_DATE_STR = CURRENT_DATE.strftime(DATE_STR_FORMAT)

RANDOM_TIME_STR = "2021-01-01 12:00:00"
RANDOM_DATE_STR = "2021-01-01"


class TestTimeModule(unittest.TestCase):
    def test_get_date(self):
        module_date = get_date(CURRENT_DATE_STR)
        # type
        self.assertIsInstance(module_date, date)
        self.assertEqual(module_date, CURRENT_DATE)

    def test_get_datetime(self):
        module_datetime = get_datetime(CURRENT_TIME_STR)
        self.assertIsInstance(module_datetime, datetime)
        self.assertEqual(module_datetime.year, CURRENT_TIME.year)
        self.assertEqual(module_datetime.month, CURRENT_TIME.month)
        self.assertEqual(module_datetime.day, CURRENT_TIME.day)
        self.assertEqual(module_datetime.hour, CURRENT_TIME.hour)
        self.assertEqual(module_datetime.minute, CURRENT_TIME.minute)
        self.assertEqual(module_datetime.second, CURRENT_TIME.second)

    def test_get_date_by_ymd(self):
        YEAR = 2021
        MONTH = 1
        DAY = 1
        DATE = date(YEAR, MONTH, DAY)

        module_date = get_date_by_ymd(YEAR, MONTH, DAY)
        self.assertIsInstance(module_date, date)
        self.assertEqual(module_date, DATE)

        self.assertIsInstance(DATE.year, int)
        self.assertIsInstance(DATE.month, int)
        self.assertIsInstance(DATE.day, int)

