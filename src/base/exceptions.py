from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Не возможно стать участником'
    default_code = 'error'
