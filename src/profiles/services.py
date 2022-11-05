import requests
from django.db.models import F
from kombu.exceptions import HttpError
from src.profiles.models import FatUser

CLINENT_ID = 'b46782c706eb9371e5b9'
CLIENT_SECRET = 'd3b9aa3d67bc5591f4624197d43e38d2ba310d71'

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


def check_token(code):
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": CLINENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    check = requests.post(url_token, data=data)
    token = check.text.split("&")[0].split("=")[1]
    return token

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

def github_get_user(code: str):
    user = check_github_auth(code)
    if user is not None:
        nik = user.get('login')
        url = user.get('html_url')
        email = github_get_email(nik)
        return nik, url, email
    else:
        raise HttpError(403, "Bad code")

def github_get_email(nik):
    user_info = requests.get(f'https://api.github.com/users/{nik}/events/public')
    mail = ''
    for info in user_info.json():
        email_info = (info.get('payload').get('commits'))
        if email_info is not None:
            cur_email = email_info[0]
            email = cur_email.get('author').get('email')
            mail = email
            break
    return mail


