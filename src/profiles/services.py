import requests
from django.db.models import F
from kombu.exceptions import HttpError
from rest_framework import status
from rest_framework.exceptions import APIException
from src.profiles.models import FatUser, Account
from src.profiles.tokenizator import create_token
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from rest_framework.response import Response


def add_experience(user_id: int, exp: int):
    new_exp = FatUser.objects.filter(id=user_id).update(expirience=F('experience') + exp)
    return new_exp


class CoinService:

    def __init__(self, user: FatUser):
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


def check_token_add(code):
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": settings.CLINENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    }
    check = requests.post(url_token, data=data)
    token = check.text.split("&")[0].split("=")[1]
    return token

def check_token(code):
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": settings.CLINENT_ID_FOR_AUTH,
        "client_secret": settings.CLIENT_SECRET_FOR_AUTH,
    }
    check = requests.post(url_token, data=data)
    token = check.text.split("&")[0].split("=")[1]
    return token

def check_github_auth_add(code: str):
    _token = check_token_add(code)
    if _token != 'bad_verification_code':
        user = check_github_user(_token)
        return user.json()
    return None

def check_github_auth(code: str):
    _token = check_token(code)
    if _token != 'bad_verification_code':
        user = check_github_user(_token)
        return user.json()
    return None

def check_github_user(_token):
    url_check_user = 'https://api.github.com/user'
    headers = {'Authorization': f'token {_token}'}
    user = requests.get(url_check_user, headers=headers)
    return user

def github_get_user_add(code: str):
    user = check_github_auth_add(code)
    if user is not None:
        account_name = user.get('login')
        account_url = user.get('html_url')
        account_id = user.get('id')
        return account_name, account_url, account_id
    else:
        raise HttpError(403, "Bad code")

def github_get_user_auth(code: str):
    user = check_github_auth(code)
    if user is not None:
        account_name = user.get('login')
        account_url = user.get('html_url')
        account_id = user.get('id')
        email = user.get('email')
        return account_name, account_url, account_id, email
    else:
        raise HttpError(403, "Bad code")

def github_auth(user_id) -> tuple:
    internal_token = create_token(user_id)
    return user_id, internal_token

def create_password():
    password = BaseUserManager().make_random_password()
    return password

def get_provider(account_url):
    provider = account_url.split('/')[-2].split('.')[0]
    return provider

def create_account(user, account_name, account_url, account_id):
    return Account.objects.create(
                        user=user,
                        provider=get_provider(account_url),
                        account_id=account_id,
                        account_url=account_url,
                        account_name=account_name
                    )

def check_user_with_email(account_id, email, account_name, account_url):
    if user := FatUser.objects.filter(username=account_id, email=email).exists():
        raise APIException(
            detail='Пользователь стаким email уже существует',
            code=status.HTTP_400_BAD_REQUEST
        )
    else:
        user = FatUser.objects.create(username=account_id, email=email)
        password = create_password()
        user.set_password(password)
        user.save()
        create_account(user, account_name, account_url, account_id)
        user_id, internal_token = github_auth(user.id)
        return internal_token

def create_user(account_id):
    return FatUser.objects.create(username=account_id)

def check_account_for_add(user, account_id):
    if Account.objects.filter(user=user, account_id=account_id).exists():
        raise APIException(
            detail='Аккаунт уже существует',
            code=status.HTTP_403_FORBIDDEN
        )
    if Account.objects.filter(account_id=account_id).exists():
        raise APIException(
            detail='Аккаунт уже привязан',
            code=status.HTTP_403_FORBIDDEN
        )
    else:
        return user

def check_account_for_auth(account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        user_id, internal_token = github_auth(account.user.id)
        return internal_token
    except Account.DoesNotExist:
        return False

def create_user_and_token(account_id, email, account_name, account_url):
    if email is not None:
        return check_user_with_email(account_id, email, account_name, account_url)
    elif email is None:
        user = create_user(account_id)
        password = create_password()
        user.set_password(password)
        user.save()
        create_account(user, account_name, account_url, account_id)
        user_id, internal_token = github_auth(user.id)
        return internal_token
