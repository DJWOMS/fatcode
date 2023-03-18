import datetime
import pytz

from ..base.exceptions import EventDateException


def check_date(date):
    """Проверка даты"""
    if date <= datetime.datetime.now():
        raise EventDateException
    return date


# def clock_translation(date):
#     """Перевод часов в Europe/Moscow"""
#     time_zone = pytz.timezone('Europe/Moscow')
#     datetime_moscow = date(time_zone).strftime("%Y-%m-%d %H:%M")
#     print(datetime_moscow)
#     return datetime_moscow
