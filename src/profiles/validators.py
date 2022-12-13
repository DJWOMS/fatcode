from django.core.exceptions import ValidationError


def phone_validator(phone):
    conditions = [
        not phone[1:].isdigit(),
        phone[0] != '+',
        len(phone) != 12
    ]
    if any(conditions):
        raise ValidationError('Поле должно быть формата +79876543211')