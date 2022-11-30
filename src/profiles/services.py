import binascii
import os

import requests
from django.contrib.auth.hashers import make_password
from django.db.models import F
from kombu.exceptions import HttpError
from rest_framework import status
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from src.team.models import TeamMember
from src.repository.models import ProjectMember
from src.profiles.models import FatUser, Account, Friends, Applications, Invitation
from ..base import exceptions
from .models import Questionnaire, FatUserSocial
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


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
    return check.text.split("&")[0].split("=")[1]



def check_token(code):
    url_token = 'https://github.com/login/oauth/access_token'
    data = {
        "code": code,
        "client_id": settings.CLINENT_ID_FOR_AUTH,
        "client_secret": settings.CLIENT_SECRET_FOR_AUTH,
    }
    check = requests.post(url_token, data=data)
    return check.text.split("&")[0].split("=")[1]



def check_github_auth_add(code: str):
    _token = check_token_add(code)
    if _token != 'bad_verification_code':
        return check_github_user(_token).json()
    return None


def check_github_auth(code: str):
    _token = check_token(code)
    if _token != 'bad_verification_code':
        return check_github_user(_token).json()
    return None


def check_github_user(_token):
    url_check_user = 'https://api.github.com/user'
    headers = {'Authorization': f'token {_token}'}
    return requests.get(url_check_user, headers=headers)



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


def github_auth(user):
    token = binascii.hexlify(os.urandom(20)).decode()
    return token


def create_password():
    return BaseUserManager().make_random_password()


def get_provider(account_url):
    return account_url.split('/')[-2].split('.')[0]


def create_account(user, account_name, account_url, account_id):
    return Account.objects.create(
                        user=user,
                        provider=get_provider(account_url),
                        account_id=account_id,
                        account_url=account_url,
                        account_name=account_name
                    )


def add_friend(friend, user):
    if Applications.objects.filter(getter=friend, sender=user):
        Applications.objects.filter(getter=friend, sender=user).delete()
        return Friends.objects.create(friend=friend, user=user)
    else:
        raise ValueError("you have not application")


def check_user_with_email(account_id, email):
    if user := FatUser.objects.filter(username=account_id, email=email).exists():
        raise exceptions.EmailExists()
    else:
        user = FatUser.objects.create(username=account_id, email=email)
    return user


def create_user_without_email(account_id):
    return FatUser.objects.create(username=account_id)


def create_user_with_email(nik, email):
    return FatUser.objects.create(username=nik, email=email)


def check_account_for_add(user, account_id):
    if Account.objects.filter(user=user, account_id=account_id).exists():
        raise exceptions.AccountExists()
    if Account.objects.filter(account_id=account_id).exists():
        raise exceptions.AccountIdExists()
    else:
        return user


def check_or_create_token(user):
    try:
        cur_token = Token.objects.get(user=user)
        if cur_token:
            token = {'auth_token': cur_token.key}
            return token
    except:
        internal_token = github_auth(user)
        cur_token = Token.objects.create(key=internal_token, user=user)
        token = {'auth_token': cur_token}
        return token


def check_account_for_auth(account_id):
    try:
        account = Account.objects.get(account_id=account_id)
        return check_or_create_token(account.user)
    except Account.DoesNotExist:
        return False


def create_user(account_id, email):
    if email is not None:
        user = check_user_with_email(account_id, email)
    elif email is None:
        user = create_user_without_email(account_id)
    return user


def create_user_and_token(account_id, email, account_name, account_url):
    user = create_user(account_id, email)
    password = create_password()
    user.set_password(password)
    user.save()
    create_account(user, account_name, account_url, account_id)
    return check_or_create_token(user)


def check_teams(teams, user):
    if teams is not None:
        for team in teams:
            if not TeamMember.objects.filter(user=user, team=team).exists():
                raise exceptions.TeamMemberExists()
    return teams


def check_projects(projects, user):
    if projects is not None:
        for project in projects:
            cur_project = ProjectMember.objects.filter(user=user, project=project).exists()
            if not cur_project:
                raise exceptions.ProjectMemberExists()
    return projects


def check_account(accounts, user):
    if accounts is not None:
        for account in accounts:
            cur_account = Account.objects.filter(user=user, account_url=account).exists()
            if not cur_account:
                raise exceptions.AccountMemberExists()
    return accounts


def questionnaire_create(user, teams, projects, accounts, toolkits, languages, socials, **validated_data):
    questionnaire = Questionnaire.objects.create(user=user,**validated_data)
    for team in teams:
        questionnaire.teams.add(team)
    for toolkit in toolkits:
        questionnaire.toolkits.add(toolkit)
    for project in projects:
        questionnaire.projects.add(project)
    for account in accounts:
        questionnaire.accounts.add(account)
    for language in languages:
        questionnaire.languages.add(language)
    for social in socials:
        questionnaire.socials.add(social)
    return questionnaire


def check_socials(user, socials):
    if socials is not None:
        for social in socials:
            cur_social = FatUserSocial.objects.filter(user=user, user_url=social).exists()
            if not cur_social:
                raise exceptions.SocialUserNotExists()
    return socials


def check_profile(user, teams, projects, accounts, socials):
    check_teams_and_projects = check_teams(teams, user) and check_projects(projects, user)
    check_accounts_and_socials = check_account(accounts, user) and check_socials(user, socials)
    if check_teams_and_projects and check_accounts_and_socials:
        return user


def questionnaire_update(instance, teams, toolkits, projects, accounts, languages, socials):
    instance.teams.clear()
    instance.toolkits.clear()
    instance.accounts.clear()
    instance.projects.clear()
    instance.languages.clear()
    instance.socials.clear()
    for team in teams:
        instance.teams.add(team)
    for toolkit in toolkits:
        instance.toolkits.add(toolkit)
    for project in projects:
        instance.projects.add(project)
    for language in languages:
        instance.languages.add(language)
    for account in accounts:
        instance.accounts.add(account)
    for social in socials:
        instance.socials.add(social)
    return instance


def check_invite(invite, username, email, password):
    if check_email(email):
        if invite != '':
            cur_invite = Invitation.objects.filter(code=invite)
            if cur_invite:
                cur_invite.delete()
                return create_user_with_password(username, email, password)
            else:
                raise exceptions.InvitationNotExists()
        else:
            return create_user_with_password(username, email, password)


def create_user_with_password(username, email, password):
    user = FatUser.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
    return user


def check_email(email):
    cur_email = FatUser.objects.filter(email=email).exists()
    if cur_email:
        raise exceptions.EmailExists()
    return email


def check_password(password, re_password):
    print(make_password(re_password))
    print(make_password(password))
    if password == make_password(re_password):
        print('ok')
    return password


def check_username(username):
    cur_user = FatUser.objects.filter(username=username).exists()
    if cur_user:
        raise exceptions.UsernameExists()
    return username


