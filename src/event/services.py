import datetime
import pytz

from ..base import exceptions
from ..questionnaire.models import Questionnaire


def check_date(user, date):
    """Проверка даты"""
    try:
        user_time_zona = Questionnaire.objects.get(user=user)
        tz1 = pytz.timezone(user_time_zona.timezone)
        tz2 = pytz.timezone('Europe/Moscow')
        dt_tz2 = tz1.localize(date).astimezone(tz2).strftime("%Y-%m-%d %H:%M")
        if date.strftime("%Y-%m-%d %H:%M") >= datetime.datetime.now().astimezone(tz1).strftime("%Y-%m-%d %H:%M"):
            return dt_tz2
        raise exceptions.EventDateException()
    except Questionnaire.DoesNotExist:
        raise exceptions.QuestionnaireTimezonaException()
