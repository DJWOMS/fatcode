from django.urls import reverse
from rest_framework.test import APITestCase
from src.profiles.models import FatUser
from rest_framework.authtoken.models import Token


def create_user(email, name):
    return FatUser.objects.create_user(
        username=name,
        password='password',
        email=email
    )


class CatTestCase(APITestCase):

    def setUp(self):
        self.user = create_user('zxczxczxczxxx', 'oaidoasdioasdois@mail.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_cat_list(self):
        response = self.client.get(reverse('cat_list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_cat_detail(self):
        cat = self.user.cat.first().id
        response = self.client.get(reverse('cat_detail', kwargs={"pk": cat}))
        self.assertEqual(response.status_code, 200)

    def test_cat_user_get(self):
        response = self.client.get(reverse('user_cat'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_cat_user_update(self):
        data = {
            "name": "барсик"
        }
        cat = self.user.cat.first().id
        response = self.client.patch(reverse('cat_update', kwargs={'pk': cat}), data=data, format='json')
        self.assertEqual(response.status_code, 200)
