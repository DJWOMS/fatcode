import requests
from django.db.models import F
from kombu.exceptions import HttpError
from src.profiles.models import FatUser, Account
from src.profiles.tokenizator import create_token
from django.contrib.auth.base_user import BaseUserManager


CLINENT_ID = '11eac0936dc86e03a233'
CLIENT_SECRET = '8b7793d919a4d9541c9856309c949cd5bc512b2c'

CLINENT_ID_FOR_AUTH = 'da8b2e32d27020f8c5b4'
CLIENT_SECRET_FOR_AUTH = '3b973329bbe53574b50d1f41d418b0381b98130f'

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
        "client_id": CLINENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    check = requests.post(url_token, data=data)
    token = check.text.split("&")[0].split("=")[1]
    return token

def check_token(code):
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": CLINENT_ID_FOR_AUTH,
        "client_secret": CLIENT_SECRET_FOR_AUTH,
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
        nik = user.get('login')
        url = user.get('html_url')
        email = user.get('email', None)
        return nik, url, email
    else:
        raise HttpError(403, "Bad code")

def github_get_user_auth(code: str):
    user = check_github_auth(code)
    if user is not None:
        nik = user.get('login')
        url = user.get('html_url')
        email = user.get('email', None)
        return nik, url, email
    else:
        raise HttpError(403, "Bad code")

def github_auth(user_id) -> tuple:
    internal_token = create_token(user_id)
    return user_id, internal_token

def add_account(user, nik, url, email):
    return Account.objects.create(
        user=user,
        nickname_git=nik,
        url=url,
        email=email
    )

def create_password():
    password = BaseUserManager().make_random_password()
    return password