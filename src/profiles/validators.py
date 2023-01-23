import datetime

from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

def phone_validator(phone):
    conditions = [
        not phone[1:].isdigit(),
        phone[0] != '+',
        len(phone) != 12
    ]
    if any(conditions):
        raise ValidationError('Поле должно быть формата +79876543211')


def birthday_validator(birthday):
    year_today = datetime.date.today()
    max_date = year_today - relativedelta(years=10)
    min_date = year_today - relativedelta(years=60)
    if birthday >= max_date:
        raise ValidationError(f'Участник не может быть младше  {max_date.year}')
    if birthday <= min_date:
        raise ValidationError(f'Участник не может быть старше {min_date.year}')
