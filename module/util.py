
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

import pytz

load_dotenv()

DEFAULT_TIMEZONE = "Asia/Jakarta"
DEFAULT_START_PUASA_DATE = "2024-03-12"


def get_timezone_info() -> pytz.timezone:
    return pytz.timezone(get_timezone_string())


def get_timezone_string() -> str:
    return os.getenv('TZ') or DEFAULT_TIMEZONE


def seconds_difference_between_datetime(begin: datetime, end: datetime, title=None):
    # If end older than begin datetime, add offset 1 day
    if end < begin:
        print(f"{title} end date is older than begin date, giving offset 1 day")
        end += timedelta(days=1)

    diff = (end - begin)
    print(f"{title} time difference : {diff}")
    return diff.total_seconds()


def get_puasa_day() -> int:
    start_date_string = os.getenv(
        'START_PUASA_DATE') or DEFAULT_START_PUASA_DATE

    date_part = start_date_string.split('-')
    if len(date_part) != 3:
        raise Exception('Invalid date format, must be YYYY-MM-DD')

    timezone = get_timezone_info()

    start_date = datetime(
        year=int(date_part[0]),
        month=int(date_part[1]),
        day=int(date_part[2]),
        tzinfo=timezone
    )

    current_date = datetime.now(tz=timezone)

    # dimulai dari 1
    difference = current_date + timedelta(days=1) - start_date

    return difference.days


def get_tarawih_day() -> int:
    # Give 1 day offset, because tarawih start oneday before puasa
    return get_puasa_day() + 1
