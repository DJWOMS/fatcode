from rest_framework.test import APITestCase
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token
from src.cat import models


def create_user(email, name):
    user = FatUser.objects.create_user(
        username=name,
        password='password',
        email=email
    )
    return user


class CatTestCase(APITestCase):

    def setUp(self):
        self.user = create_user('zxczxczxczxxx', 'oaidoasdioasdois@mail.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

