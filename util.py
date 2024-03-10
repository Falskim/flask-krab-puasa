
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

    if difference.days < 1:
        difference -= timedelta(days=1)

    return difference.days
