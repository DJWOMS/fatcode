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


class SocialUserNotExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Добавить можно только свои социальные сети'
    default_code = 'error'


class TeamMemberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Участником одной команды можно стать один раз'
    default_code = 'error'


class PostNotExistsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Нет доступа для написания комментариев'
    default_code = 'error'


class PostException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Нет доступа для написания комментариев'
    default_code = 'error'


class InvitationNotExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Нет доступа регистрации'
    default_code = 'error'


class EmailExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Пользователь с таким email уже существует'
    default_code = 'error'


class UsernameExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Пользователь с таким именем уже существует'
    default_code = 'error'


class AccountExists(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Аккаунт уже существует'
    default_code = 'error'


class AccountIdExists(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Аккаунт уже привязан'
    default_code = 'error'