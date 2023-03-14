import requests

from django.db.models import F
from kombu.exceptions import HttpError
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from rest_framework.authtoken.models import Token

from src.profiles import models
from src.team import services as services_team
from src.repository import services as services_rep
from ..base import exceptions


def add_experience(user_id: int, exp: int):
    new_exp = models.FatUser.objects.filter(id=user_id).update(expirience=F('experience') + exp)
    return new_exp


class CoinService:

    def __init__(self, user: models.FatUser):
        self.user = user

    def check_balance(self):
        return self.user.coins

    def buy(self, price):
        balance = self.check_balance()
        if balance > price:
            self.user.coins -= price
            self.user.save()
            return self.user
        raise ValueError('Недостаточно средств')


class ReputationService:
    def __init__(self, user: models.FatUser):
        self.user = user

    def increase_reputation(self, count: int, action: str):
        if action == "inc":
            self.user.reputation += count
            self.user.save()
        elif action == "dcr":
            self.user.reputation -= count
            self.user.save()


def check_token_add(code):
    """Проверка кода с github на добавление аккаунта"""
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": settings.CLINENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    }
    check = requests.post(url_token, data=data)
    return check.text.split("&")[0].split("=")[1]


def check_token(code):
    """Проверка кода с github на добавление авторизацию"""
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": settings.CLINENT_ID_FOR_AUTH,
        "client_secret": settings.CLIENT_SECRET_FOR_AUTH,
    }
    check = requests.post(url_token, data=data)
    return check.text.split("&")[0].split("=")[1]


def check_github_auth_add(code: str):
    """Проверка токена с github на добавление"""
    _token = check_token_add(code)
    if _token != 'bad_verification_code':
        return check_github_user(_token).json()
    return None


def check_github_auth(code: str):
    """Проверка токена с github на авторизацию"""
    _token = check_token(code)
    if _token != 'bad_verification_code':
        return check_github_user(_token).json()
    return None


def check_github_user(_token):
    """Получение токена с github"""
    url_check_user = 'https://api.github.com/user'
    headers = {'Authorization': f'token {_token}'}
    return requests.get(url_check_user, headers=headers)


def github_get_user_add(code: str):
    """Получение данных аккаунта с github для добавления"""
    user = check_github_auth_add(code)
    if user is not None:
        account_name = user.get('login')
        account_url = user.get('html_url')
        account_id = user.get('id')
        return account_name, account_url, account_id
    else:
        raise HttpError(403, "Bad code")


def github_get_user_auth(code: str):
    """Получение данных аккаунта с github авторизации"""
    user = check_github_auth(code)
    if user is not None:
        account_name = user.get('login')
        account_url = user.get('html_url')
        account_id = user.get('id')
        email = user.get('email')
        return account_name, account_url, account_id, email
    else:
        raise HttpError(403, "Bad code")


def create_password():
    """Создание пароля для пользователя при авторизации через github"""
    return BaseUserManager().make_random_password()


def get_provider(account_url):
    """Получение провайдера"""
    return account_url.split('/')[-2].split('.')[0]


def create_account(user, account_name, account_url, account_id):
    """Создание аккаунта для пользователя"""
    return models.Account.objects.create(
                        user=user,
                        provider=get_provider(account_url),
                        account_id=account_id,
                        account_url=account_url,
                        account_name=account_name
                    )


def add_friend(friend, user):
    if models.Application.objects.filter(getter=friend, sender=user):
        models.Application.objects.filter(getter=friend, sender=user).delete()
        return models.Friend.objects.create(friend=friend, user=user)
    else:
        raise ValueError("you have not application")


def create_user_without_email(account_id):
    """Создание пользователя без email"""
    return models.FatUser.objects.create(username=account_id)


def create_user_with_email(nik, email):
    """Создание пользователя с email"""
    return models.FatUser.objects.create(username=nik, email=email)


def check_account_for_add(user, account_id):
    """Проверка наличия привязанного аккаунта github у пользователя"""
    if models.Account.objects.filter(user=user, account_id=account_id).exists():
        raise exceptions.AccountExists()
    if models.Account.objects.filter(account_id=account_id).exists():
        raise exceptions.AccountIdExists()
    else:
        return user


def check_or_create_token(user):
    """Проверка и создание токена пользователя"""
    try:
        current_token = Token.objects.get(user=user)
        return {'auth_token': current_token.key}
    except Token.DoesNotExist:
        current_token = Token.objects.create(user=user)
        return {'auth_token': current_token}


def check_account_for_auth(account_id):
    """Проверка и создание токена пользователя  после авторизации через github"""
    try:
        account = models.Account.objects.get(account_id=account_id)
        return check_or_create_token(account.user)
    except models.Account.DoesNotExist:
        return False


def create_user(account_id, email):
    """Проверка email и создание пользователя"""
    if email is not None:
        if check_email(email):
            return create_user_with_email(account_id, email)
    elif email is None:
        return create_user_without_email(account_id)


def create_user_and_token(account_id, email, account_name, account_url):
    """Проверка и создание пользователя, его аккаунта и токена"""
    user = create_user(account_id, email)
    password = create_password()
    user.set_password(password)
    user.save()
    create_account(user, account_name, account_url, account_id)
    return check_or_create_token(user)


def check_account(accounts, user):
    """Проверка привязанных аккаунтов пользователя"""
    if accounts is not None:
        for account in accounts:
            if not models.Account.objects.filter(user=user, account_url=account).exists():
                raise exceptions.AccountMemberExists()
    return accounts


def check_socials(user, socials):
    """Проверка социальных сетей пользователя"""
    if socials is not None:
        for social in socials:
            if not models.FatUserSocial.objects.filter(user=user, user_url=social).exists():
                raise exceptions.SocialUserNotExists()
    return socials


def check_profile(user, teams, projects, accounts, socials):
    """Проверка пользователя для создания анкеты"""
    check_teams_and_projects = services_team.check_teams(teams, user) and services_rep.check_projects(projects, user)
    check_accounts_and_socials = check_account(accounts, user) and check_socials(user, socials)
    if check_teams_and_projects and check_accounts_and_socials:
        return user


def check_invite(invite):
    """Проверка приглашения"""
    if invite:
        if not models.Invitation.objects.filter(code=invite).exists():
            raise exceptions.InvitationNotExists()
        return invite
    raise exceptions.InvitationNotExists()


def delete_invite(invite):
    """Удаление приглашения"""
    current_invite = models.Invitation.objects.filter(code=invite)
    current_invite.delete()
    return True


def check_email(email):
    """Проверка email пользователя"""
    if models.FatUser.objects.filter(email=email).exists():
        raise exceptions.EmailExists()
    return email


def check_or_update_email(instance, email, pk, middle_name, town):
    """Проверка значений на изменение email профиля"""
    if email != '':
        if models.FatUser.objects.filter(email=email).exclude(email=instance.email).exists():
            raise exceptions.EmailExists()
        else:
            instance.email = email
            instance.save()
    if middle_name != '':
        instance.middle_name = middle_name
        instance.save()
    if town != '':
        instance.town = town
        instance.save()
    return instance


def create_social(user, social_link, user_url):
    """Проверка социальных ссылок пользователя"""
    if models.FatUserSocial.objects.filter(social=social_link, user=user).exists():
        raise exceptions.SocialExists()
    try:
        current_user_url = user_url.split('/')[-1]
        return models.FatUserSocial.objects.create(social=social_link, user=user, user_url=current_user_url)
    except:
        return models.FatUserSocial.objects.create(social=social_link, user=user, user_url=user_url)


def check_or_update_social(instance, user_url):
    """Проверка социальных ссылок профиля для обновления"""
    try:
        current_user_url = user_url.split('/')[-1]
        instance.user_url = current_user_url
        instance.save()
    except:
        instance.user_url = user_url
        instance.save()
    return instance





