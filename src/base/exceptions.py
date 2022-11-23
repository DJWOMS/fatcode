from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Не возможно стать участником'
    default_code = 'error'


class BadAccountId(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad account_id'
    default_code = 'error'

class BadAccountAuthor(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Добавить репозиторий возможно только для своего аккаунта'
    default_code = 'error'

class BadAccount(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Добавить репозиторий возможно только для аккаунтов привязанных к github'
    default_code = 'error'

class TeamExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Для данной команды есть проект'
    default_code = 'error'

class TeamAuthor(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Создать возможно только для своей команды'
    default_code = 'error'

class RepositoryExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Для данного репозитория уже есть проект'
    default_code = 'error'

class TeamMemberExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Добавить можно только команду, в которой состоите'
    default_code = 'error'

class ProjectMemberExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Добавить можно только проект, в котором состоите'
    default_code = 'error'


class AccountMemberExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Добавить можно только свои социальные сети'
    default_code = 'error'


class QuestionnaireUserExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Создать анкету можно только один раз'
    default_code = 'error'


class EmailNotExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Email обязательное поле'
    default_code = 'error'