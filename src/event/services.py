import datetime

from ..base.exceptions import EventDateException


def check_date(date):
    """Проверка даты"""
    if date <= datetime.datetime.now():
        raise EventDateException
    return date